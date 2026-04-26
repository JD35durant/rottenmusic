from db import get_db
from core.album import Album
from repositories.artist_repo import ArtistRepository

class AlbumRepository:

    @staticmethod
    def get(id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM albums WHERE id=%s", (id,))
        r = cursor.fetchone()
        cursor.close()
        db.close()

        artist = ArtistRepository.get(r["artist_id"])
        return Album(r["id"], r["title"], artist, r["year"], r["genre"], r["image_url"])

    @staticmethod
    def get_all(limit=8):
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM albums LIMIT %s", (limit,))
        results = cursor.fetchall()

        cursor.close()
        db.close()

        return results
    
    @staticmethod
    def search(query):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM albums WHERE name LIKE %s", (f"%{query}%",))
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        return [Album(r["id"], r["name"], r["genre"], r["image_url"]) for r in rows]