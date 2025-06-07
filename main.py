from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.user import fetch_username
from services.database import supabase
from utils.word_tools import process_submission
from utils.helpers import is_valid_word, is_palindrome

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def reverse_string():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    result = None
    if request.method == "POST":
        word = request.form.get("text")
        if not is_valid_word(word):
            flash("Not a valid English word.")
        else:
            result = process_submission(word)

    submissions = fetch_user_submissions(session["user_id"])
    leaderboard = fetch_leaderboard()

    return render_template(
        "index.html",
        username=session.get("username"),
        result=result,
        submissions=submissions,
        leaderboard=leaderboard
    )
