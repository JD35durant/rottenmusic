from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from repositories.user_repo import UserRepository
from core.user import User

class AuthService:

    @staticmethod
    def login():
        if request.method == "POST":
            user = UserRepository.get_by_email(request.form["email"])
            if user and check_password_hash(user.password_hash, request.form["password"]):
                session["user_id"] = user.id
                session["username"] = user.username
                return redirect("/")
        return render_template("login.html")

    @staticmethod
    def register():
        if request.method == "POST":
            UserRepository.create(
                request.form["username"],
                request.form["email"],
                generate_password_hash(request.form["password"])
            )
            return redirect("/login")
        return render_template("register.html")

    @staticmethod
    def logout():
        session.clear()
        return redirect("/")

    @staticmethod
    def get_current_user():
        return UserRepository.get(session["user_id"]) if "user_id" in session else User(0, "Invité")
