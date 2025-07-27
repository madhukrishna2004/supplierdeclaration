from flask import Blueprint, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
import mysql.connector
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY, DB_HOST, DB_USER, DB_PASS, MAIN_DB, GMAIL_SCOPES
from db_setup import create_user_database

auth = Blueprint("auth", __name__)
oauth = OAuth()

google = oauth.remote_app(
    "google",
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET,
    request_token_params={"scope": " ".join(GMAIL_SCOPES)},
    base_url="https://www.googleapis.com/oauth2/v1/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
)

@auth.route("/login")
def login():
    return google.authorize(callback=url_for("auth.callback", _external=True))

@auth.route("/callback")
def callback():
    response = google.authorized_response()
    if response is None:
        return "Access Denied"
    
    session["google_token"] = (response["access_token"], "")
    user_info = google.get("userinfo").data
    user_email = user_info["email"]

    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=MAIN_DB)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (email) VALUES (%s)", (user_email,))
        conn.commit()
        user_id = cursor.lastrowid
        create_user_database(user_id)
    else:
        user_id = user["id"]

    cursor.close()
    conn.close()

    session["user_id"] = user_id
    session["user_email"] = user_email

    return redirect(url_for("email_handler.dashboard"))

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@google.tokengetter
def get_google_oauth_token():
    return session.get("google_token")
