# services/auth.py

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import requests
from services.database import get_rest_headers, SUPABASE_AUTH_URL, SUPABASE_REST_URL
from utils.helpers import sanitize_username
from models.user import fetch_username

auth_bp = Blueprint("auth", __name__, url_prefix="")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        step = request.form.get("step")
        email = request.form.get("email")

        if step == "check_email":
            session['pending_email'] = email
            response = requests.get(
                f"{SUPABASE_REST_URL}/submissions?email=eq.{email}&limit=1",
                headers=get_rest_headers()
            )

            if response.status_code == 200 and response.json():
                flash("Welcome back! Sending your magic link.")
                requests.post(
                    f"{SUPABASE_AUTH_URL}/magiclink",
                    json={"email": email},
                    headers=get_rest_headers()
                )
                return render_template("login.html", email_sent=True)
            else:
                return render_template("login_username.html", email=email)

        elif step == "register_username":
            email = session.get("pending_email")
            username_input = request.form.get("username")
            username = sanitize_username(username_input)

            if not username:
                flash("Username cannot be empty or contain only invalid characters.")
                return render_template("login_username.html", email=email)

            check = requests.get(
                f"{SUPABASE_REST_URL}/submissions?username=eq.{username}&limit=1",
                headers=get_rest_headers()
            )

            if check.status_code == 200 and check.json():
                flash("Username already taken. Please choose another.")
                return render_template("login_username.html", email=email)

            session['pending_username'] = username
            flash("Magic link sent! Check your email.")
            requests.post(
                f"{SUPABASE_AUTH_URL}/magiclink",
                json={"email": email},
                headers=get_rest_headers()
            )
            return render_template("login.html", email_sent=True)

    return render_template("login.html", email_sent=False)


@auth_bp.route("/callback")
def callback():
    access_token = request.args.get("access_token")
    if access_token:
        session["access_token"] = access_token
        user_info = requests.get(
            f"{SUPABASE_AUTH_URL}/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "apikey": get_rest_headers()["apikey"]
            }
        )

        if user_info.status_code == 200:
            user_data = user_info.json().get("user", {}) or user_info.json()
            session["user_id"] = user_data.get("id")
            session["email"] = user_data.get("email") or session.pop("pending_email", None)
            session["username"] = session.pop("pending_username", None)

            if not session.get("username"):
                session["username"] = fetch_username(session["user_id"], session.get("email"))

        return redirect(url_for("main.reverse_string"))

    return render_template("callback.html")
