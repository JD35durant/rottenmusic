from db import get_db

class RankingService:

    @staticmethod
    def top10_artists_by_genre(genre):
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.*, COALESCE(AVG(r.rating), 0) AS avg_rating
            FROM artists a
            LEFT JOIN reviews r ON r.item_id = a.id AND r.item_type = 'artist'
            WHERE LOWER(a.genre) = LOWER(%s)
            GROUP BY a.id
            ORDER BY avg_rating DESC
            LIMIT 10
        """, (genre,))

        return cursor.fetchall()


    @staticmethod
    def top10_albums_by_genre(genre):
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT al.*, ar.name AS artist_name, COALESCE(AVG(r.rating), 0) AS avg_rating
            FROM albums al
            JOIN artists ar ON al.artist_id = ar.id
            LEFT JOIN reviews r ON r.item_id = al.id AND r.item_type = 'album'
            WHERE LOWER(al.genre) = LOWER(%s)
            GROUP BY al.id
            ORDER BY avg_rating DESC
            LIMIT 10
        """, (genre,))

        return cursor.fetchall()
        
        
    @staticmethod
    def get_home_artists(limit=8):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, genre, image_url FROM artists LIMIT %s",
            (limit,)
        )
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        return rows

    @staticmethod
    def get_home_albums(limit=8):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, title, genre, image_url FROM albums LIMIT %s",
            (limit,)
        )
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        return rows
