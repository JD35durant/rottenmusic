from db import get_db
from core.review import Review
from repositories.user_repo import UserRepository

class ReviewRepository:

    @staticmethod
    def get_reviews(item_type, item_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM reviews
            WHERE item_type=%s AND item_id=%s
            ORDER BY created_at DESC
        """, (item_type, item_id))
        rows = cursor.fetchall()
        cursor.close()
        db.close()

        return [Review(UserRepository.get(r["user_id"]), r["rating"], r["comment"]) for r in rows]

    @staticmethod
    def add_review(user_id, item_type, item_id, rating, comment):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO reviews (user_id, item_type, item_id, rating, comment)
            VALUES (%s,%s,%s,%s,%s)
        """, (user_id, item_type, item_id, rating, comment))
        db.commit()
        cursor.close()
        db.close()
