import os
import pymysql
from flask import Flask, render_template, request, redirect, session, jsonify 
from core.media_factory import MediaFactory
from services.auth_service import AuthService
from services.ranking_service import RankingService
from services.image_service import ImageService
from repositories.artist_repo import ArtistRepository
from repositories.album_repo import AlbumRepository
from repositories.review_repo import ReviewRepository
from services.auth_service import AuthService
from db import get_db
app = Flask(__rottenmusic__)





    try:
        
        connection = pymysql.connect(
            host=os.environ.get('MYSQL_HOST', 'mysql-208df5e7-rottenmusic1.h.aivencloud.com'),
            port=int(os.environ.get('MYSQL_PORT', 15702)),
            user=os.environ.get('MYSQL_USER', 'avnadmin'),
            password=os.environ.get('MYSQL_PASSWORD', 'AVNS_-WeW01A2jy_U9Lmd_Fe'),
            database=os.environ.get('MYSQL_DATABASE', 'defaultdb'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            ssl={'ca': '/app/ca.pem'}  # Important pour Aiven
        )
        return connection
    except Exception as e:
        print(f"Erreur de connexion MySQL: {e}")
        raise

@app.route('/')
def index():
    return {
        "status": "ok", 
        "message": "Flask + Aiven MySQL sur Render fonctionne !"
    }

@app.route('/test-db')
def test_db():
    """Test de connexion à MySQL"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION() as mysql_version, NOW() as current_time")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "status": "success", 
            "message": "Connexion MySQL réussie !",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e)
        }, 500
# -------------------------------------
# ROUTE : HOME (liste des artistes et albums)
# -------------------------------------

@app.route("/")
def index():
    artists = ArtistRepository.get_all(limit=12)
    albums = AlbumRepository.get_all(limit=12)

    return render_template("index.html", artists=artists, albums=albums)


# -------------------------------------
# ROUTE : AFFICHAGE ITEM (artist/album/song)
# -------------------------------------
@app.route("/item/<item_type>/<int:item_id>")
def item_view(item_type, item_id):
    item = MediaFactory.load(item_type, item_id)
    return render_template("item.html", item=item)


# -------------------------------------
# ROUTE : AJOUT DE CRITIQUE
# -------------------------------------
@app.route("/review/<item_type>/<int:item_id>", methods=["GET", "POST"])
def review_item(item_type, item_id):
    item = MediaFactory.load(item_type, item_id)

    if request.method == "POST":

        rating = int(request.form["rating"])
        comment = request.form["comment"]

        user = AuthService.get_current_user()

        ReviewRepository.add_review(
            user_id=user.id,
            item_type=item_type,
            item_id=item.id,
            rating=rating,
            comment=comment
        )

        return redirect(f"/item/{item_type}/{item_id}")

    return render_template("review_form.html", item=item)


# -------------------------------------
# ROUTE : RECHERCHE
# -------------------------------------
@app.route("/search")
def search():
    query = request.args.get("q", "")
    results = ArtistRepository.search(query) if query else []
    return render_template("search.html", query=query, results=results)


# -------------------------------------
# ROUTE : TOP 10 PAR GENRE

@app.route("/top10/artists/<genre>")
def top10_artists(genre):
    artists = RankingService.top10_artists_by_genre(genre)
    return render_template("top10_artists.html", artists=artists, genre=genre)


@app.route("/top10/albums/<genre>")
def top10_albums(genre):
    albums = RankingService.top10_albums_by_genre(genre)
    return render_template("top10_albums_result.html", albums=albums, genre=genre)
# -------------------------------------
@app.route("/top-artists")
def top_artists():
    genres = ["rock", "pop", "rap", "jazz", "electro"]
    return render_template("top_artists.html", genres=genres)


@app.route("/top-albums")
def top_albums():
    genres = ["rock", "pop", "rap", "jazz", "electro"]
    return render_template("top_albums.html", genres=genres)

# -------------------------------------
# ROUTE : LOGIN
# -------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    return AuthService.login()


# -------------------------------------
# ROUTE : REGISTER
# -------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    return AuthService.register()


# -------------------------------------
# ROUTE : LOGOUT
# -------------------------------------
@app.route("/logout")
def logout():
    return AuthService.logout()

@app.route("/debug")
def debug():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT genre FROM artists")
    return str(cursor.fetchall())
# -------------------------------------
# POINT D'ENTRÉE
# -------------------------------------
if __name__ == "__main__":
    app.run(debug=True)