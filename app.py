import os
import pymysql
from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'SUPER_SECRET_KEY')

# ============================================
# CONNEXION À MySQL (version corrigée)
# ============================================
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.environ.get('MYSQL_HOST', 'mysql-208df5e7-rottenmusic1.h.aivencloud.com'),
            port=int(os.environ.get('MYSQL_PORT', 15702)),
            user=os.environ.get('MYSQL_USER', 'avnadmin'),
            password=os.environ.get('MYSQL_PASSWORD', 'AVNS_-WeW01A2jy_U9Lmd_Fe'),
            database=os.environ.get('MYSQL_DATABASE', 'defaultdb'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            ssl={'ca': '/app/ca.pem'}
        )
        return connection
    except Exception as e:
        print(f"Erreur de connexion MySQL: {e}")
        raise

# ============================================
# ROUTE : TEST / HOME
# ============================================
@app.route('/')
def index():
    # Test simple pour vérifier que l'app tourne
    return {
        "status": "ok", 
        "message": "Flask + Aiven MySQL sur Render fonctionne !"
    }

@app.route('/test-db')
def test_db():
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

# ============================================
# ROUTES API (version minimaliste)
# ============================================
@app.route('/artists')
def get_artists():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artists LIMIT 20")
        artists = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"status": "success", "artists": artists}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/albums')
def get_albums():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM albums LIMIT 20")
        albums = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"status": "success", "albums": albums}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/genres')
def get_genres():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT genre FROM artists WHERE genre IS NOT NULL")
        genres = [row['genre'] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return {"status": "success", "genres": genres}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

# ============================================
# POINT D'ENTRÉE (IMPORTANT pour Render)
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)