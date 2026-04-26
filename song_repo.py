from db import get_db
from core.song import Song
from repositories.artist_repo import ArtistRepository

class SongRepository:

    @staticmethod
    def get(id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM songs WHERE id=%s", (id,))
        r = cursor.fetchone()
        cursor.close()
        db.close()

        artist = ArtistRepository.get(r["artist_id"])
        return Song(r["id"], r["title"], artist, r["duration"], r["image_url"])
