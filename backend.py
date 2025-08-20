# backend.py
from flask import Flask, request, jsonify
from auth import ensure_users_file, signup_user, login_user
from data_manager import ensure_songs_file, get_songs_by_mood, ensure_songs_folder
from data_manager import get_random_song_by_mood


app = Flask(__name__)

# Ensure files and folders exist
ensure_users_file()
ensure_songs_file()
ensure_songs_folder()

@app.route("/")
def home():
    return {"message": "Welcome to Reco API"}

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return {"status": "fail", "message": "Both fields required"}, 400

    return signup_user(username, password)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    return login_user(username, password)

@app.route("/songs/<mood>", methods=["GET"])
def get_songs(mood):
    results = get_songs_by_mood(mood)
    return jsonify(results), 200

@app.route("/songs/<mood>/random", methods=["GET"])
def get_random_song(mood):
    s = get_random_song_by_mood(mood)
    if not s:
        return jsonify([]), 200
    return jsonify([s]), 200

if __name__ == "__main__":
    app.run(debug=True)
