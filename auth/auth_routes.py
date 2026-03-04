from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_dance.contrib.google import google

from auth.user_model import User

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()


# ================= REGISTER =================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if not username or not password:
            flash("Username & Password wajib diisi")
            return redirect("/register")

        hashed = bcrypt.generate_password_hash(password).decode()

        created = User.create(username, hashed)

        if not created:
            flash("Username sudah digunakan")
            return redirect("/register")

        flash("Register berhasil, silakan login")
        return redirect("/login")

    return render_template("register.html")


# ================= LOGIN =================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user_data = User.find_by_username(username)

        if not user_data:
            flash("User tidak ditemukan")
            return redirect("/login")

        if not bcrypt.check_password_hash(
            user_data["password"],
            password
        ):
            flash("Password salah")
            return redirect("/login")

        user_obj = User(user_data["id"], user_data["username"])
        login_user(user_obj)

        return redirect("/")

    return render_template("login.html")


# ================= GOOGLE LOGIN =================
@auth_bp.route("/google_login")
def google_login():

    if not google.authorized:
        return redirect("/login/google")

    resp = google.get("/oauth2/v2/userinfo")

    email = resp.json()["email"]

    user_data = User.find_by_username(email)

    if not user_data:
        User.create(email, "google_login")
        user_data = User.find_by_username(email)

    user_obj = User(user_data["id"], user_data["username"])
    login_user(user_obj)

    return redirect("/")


# ================= TELEGRAM LOGIN =================
@auth_bp.route("/telegram_login")
def telegram_login():

    username = request.args.get("username")

    if not username:
        flash("Telegram login gagal")
        return redirect("/login")

    user_data = User.find_by_username(username)

    if not user_data:
        User.create(username, "telegram_login")
        user_data = User.find_by_username(username)

    user_obj = User(user_data["id"], user_data["username"])
    login_user(user_obj)

    return redirect("/")


# ================= LOGOUT =================
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect("/login")