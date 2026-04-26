from db import get_db
from core.user import User
import mysql.connector

class UserRepository:

    @staticmethod
    def get(id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
        r = cursor.fetchone()
        cursor.close()
        db.close()
        return User(r["id"], r["username"], r["email"], r["password_hash"]) if r else None

    @staticmethod
    def get_by_email(email):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        r = cursor.fetchone()
        cursor.close()
        db.close()
        return User(r["id"], r["username"], r["email"], r["password_hash"]) if r else None

    @staticmethod
    def create(username, email, password):
        db = get_db()
        cursor = db.cursor()

        try:
           cursor.execute(
              """
              INSERT INTO users (username, email, password)
              VALUES (%s, %s, %s)
              """,
              (username, email, password)
           )
           db.commit()
           return True, None

        except mysql.connector.IntegrityError:
           db.rollback()
           return False, "Email déjà utilisé."

        except Exception:
          db.rollback()
          return False, "Erreur serveur, veuillez réessayer."

        finally:
           cursor.close()
           db.close()