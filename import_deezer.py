import requests
from db import get_db

# =========================
# GENRES OFFICIELS DEEZER
# =========================
GENRES = {
    "rock": 152,
    "pop": 132,
    "rap": 116,
    "jazz": 129,
    "electro": 106
}

# =========================
# NETTOYAGE BASE
# =========================
def clean_database(cursor):
    print("🧹 Nettoyage de la base...")
    cursor.execute("DELETE FROM albums")
    cursor.execute("DELETE FROM reviews")
    cursor.execute("DELETE FROM artists")
    print("✅ Base nettoyée")

# =========================
# IMPORT ARTISTES DEEZER
# =========================
def import_artists():
    db = get_db()
    cursor = db.cursor()

    # ✅ cursor existe maintenant
    clean_database(cursor)

    for genre_name, genre_id in GENRES.items():
        print(f"🎵 Import artistes Deezer | genre={genre_name}")

        url = f"https://api.deezer.com/genre/{genre_id}/artists"
        response = requests.get(url, timeout=10)
        data = response.json()

        for artist in data.get("data", [])[:50]:
            name = artist.get("name")
            image = artist.get("picture_big")

            if not name or not image:
                continue

            cursor.execute(
                """
                INSERT INTO artists (name, genre, image_url)
                VALUES (%s, %s, %s)
                """,
                (name, genre_name, image)
            )

    db.commit()
    cursor.close()
    db.close()

    print("✅ Artistes Deezer importés avec succès")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    import_artists()