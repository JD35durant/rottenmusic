import os
import pymysql
from flask import Flask, render_template, request, redirect, session, jsonify
#from core.media_factory import MediaFactory
from services.auth_service import AuthService
from services.ranking_service import RankingService
from services.image_service import ImageService
from repositories.artist_repo import ArtistRepository
from repositories.album_repo import AlbumRepository
from repositories.review_repo import ReviewRepository
from services.auth_service import AuthService
from db import get_db
app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY"  # à changer en production


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

# ============================================
# POINT D'ENTRÉE (IMPORTANT pour Render)
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
