import streamlit as st
import requests
import base64
import time
import random

BACKEND = "http://127.0.0.1:5000"

# --- PAGE CONFIG: call exactly once and early ---
is_logged_in = st.query_params.get("logged_in", "false") == "true"
st.set_page_config(page_title="reco.in", layout=("wide" if is_logged_in else "centered"))

st.title("🎼 Reco: for Recommendations")
st.caption("Login or sign up, pick a mood, and play songs instantly!")

# --- SESSION STATE ---
if "username" not in st.session_state:
    st.session_state.username = None
if "songs" not in st.session_state:
    st.session_state.songs = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# --- LOGIN / SIGNUP PAGE ---
def login_page():
    st.subheader("Login / Signup")
    tab_login, tab_signup = st.tabs(["☑️ Login", "🆕 Signup"])

    with tab_login:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            resp = requests.post(BACKEND + "/login", json={"username": username, "password": password})
            if resp.status_code == 200 and resp.json().get("status") == "success":
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.query_params["logged_in"] = "true"
                time.sleep(0.4)
                st.rerun()
            else:
                st.error(resp.json().get("message", "Error"))

    with tab_signup:
        username = st.text_input("New Username", key="signup_user")
        password = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Create Account"):
            resp = requests.post(BACKEND + "/signup", json={"username": username, "password": password})
            if resp.status_code == 200 and resp.json().get("status") == "success":
                st.success("🎉 Account created successfully! Logging you in...")
                st.session_state.username = username
                st.query_params["logged_in"] = "true"
                time.sleep(0.4)
                st.rerun()
            else:
                st.error(resp.json().get("message", "Error"))

# --- MAIN SONG PAGE ---
def main_page():
    st.subheader(f"Welcome, _{st.session_state.username}_ 👋")
    if st.button("Logout"):
        st.session_state.username = None
        st.success("👋 Logged out successfully!")
        st.query_params["logged_in"] = "false"
        time.sleep(0.4)
        st.rerun()

    mood = st.selectbox(
        "Select Mood",
        ["Happy","Sad","Relaxed","Energetic","Romantic","Chill","Focused","Party","Uplifting","Rainy Day","Calm"]
    )

    if st.button("Get Songs"):
        resp = requests.get(f"{BACKEND}/songs/{mood}")
        if resp.status_code == 200:
            songs = resp.json()
            if not songs:
                st.session_state.songs = []
                st.session_state.current_song = None
                st.info("No songs found for this mood.")
            else:
                st.session_state.songs = songs
                st.session_state.current_song = random.choice(songs)

    # Show exactly one song (if available)
    s = st.session_state.current_song
    if s:
        st.write(f"**{s['title']}** — {s['artist']}")
        try:
            audio_bytes = base64.b64decode(s["audio_data"])
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error(f"Error playing song: {e}")

        # 🎲 Choose another song (avoid immediate repeat if possible)
        if st.button("🎲 Choose another song"):
            if len(st.session_state.songs) <= 1:
                # Only one song available; just re-show it
                st.rerun()
            else:
                next_song = random.choice(st.session_state.songs)
                # avoid same pick back-to-back
                tries = 0
                while next_song is s and tries < 5:
                    next_song = random.choice(st.session_state.songs)
                    tries += 1
                st.session_state.current_song = next_song
                st.rerun()

# --- ROUTER ---
if st.session_state.username:
    main_page()
else:
    login_page()
