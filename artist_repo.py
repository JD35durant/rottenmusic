from db import get_db
from core.artist import Artist

class ArtistRepository:

    @staticmethod
    def get_all(limit=20):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM artists LIMIT %s", (limit,))
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        return [Artist(r["id"], r["name"], r["genre"], r["image_url"]) for r in rows]

    @staticmethod
    def get(id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM artists WHERE id=%s", (id,))
        r = cursor.fetchone()
        cursor.close()
        db.close()
        return Artist(r["id"], r["name"], r["genre"], r["image_url"]) if r else None

    @staticmethod
    def search(query):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM artists WHERE name LIKE %s", (f"%{query}%",))
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        return [Artist(r["id"], r["name"], r["genre"], r["image_url"]) for r in rows]
