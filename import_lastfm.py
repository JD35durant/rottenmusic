import requests
import random
import time
from db import get_db

# =========================
# CONFIG
# =========================
API_KEY = "f7d88ac3ab6fb74cb62d386f90e814fc"
LASTFM_URL = "http://ws.audioscrobbler.com/2.0/"
MB_SEARCH_URL = "https://musicbrainz.org/ws/2/artist/"
COVER_ART_URL = "https://coverartarchive.org/artist/"

DEFAULT_ARTIST_IMAGE = "/static/images/artists/default_artist.png"

# Mapping API Last.fm → DB locale
GENRE_MAP = {
    "rock": "rock",
    "pop": "pop",
    "rap": "rap",
    "electronic": "electro",
    "jazz": "jazz"
}

HEADERS_MB = {
    "User-Agent": "MusicDB/1.0 ( school.project@example.com )"
}



# =========================
# IMPORT ALBUMS (50 / GENRE)
# =========================
def import_albums(api_genre, db_genre, limit=50):
    params = {
        "method": "tag.gettopalbums",
        "tag": api_genre,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }

    r = requests.get(LASTFM_URL, params=params)
    data = r.json()

    db = get_db()
    cursor = db.cursor(dictionary=True)

    for album in data["albums"]["album"]:
        title = album["name"]
        image = album["image"][-1]["#text"] or "/static/images/no-image.png"

        # associer à un artiste existant
        cursor.execute("SELECT id FROM artists ORDER BY RAND() LIMIT 1")
        artist = cursor.fetchone()
        if not artist:
            continue

        year = random.randint(1990, 2024)

        cursor.execute(
            """
            INSERT IGNORE INTO albums (title, artist_id, year, genre, image_url)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (title, artist["id"], year, db_genre, image)
        )

    db.commit()
    cursor.close()
    db.close()

    print(f"✅ Albums importés | genre API='{api_genre}' → DB='{db_genre}'")


# =========================
# GÉNÉRATION DE REVIEWS
# =========================
def generate_reviews(count=200):
    db = get_db()
    cursor = db.cursor()

    for _ in range(count):
        cursor.execute(
            """
            INSERT INTO reviews (user_id, item_type, item_id, rating, comment)
            VALUES (
                1,
                'artist',
                (SELECT id FROM artists ORDER BY RAND() LIMIT 1),
                %s,
                'Avis généré automatiquement'
            )
            """,
            (random.randint(6, 10),)
        )

    db.commit()
    cursor.close()
    db.close()
    print("✅ Reviews générées")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    for api_genre, db_genre in GENRE_MAP.items():
      import_albums(api_genre, db_genre, 50)
      generate_reviews(200)