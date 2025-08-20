# auth.py
import pandas as pd
from flask import jsonify

USERS_FILE = "users.csv"

def ensure_users_file():
    """Ensure the users CSV exists."""
    import os
    if not os.path.exists(USERS_FILE):
        pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)

def signup_user(username, password):
    """Signup logic."""
    users = pd.read_csv(USERS_FILE)
    if username in users["username"].values:
        return {"status": "fail", "message": "User already exists"}, 409

    pd.DataFrame([[username, password]], columns=["username", "password"]).to_csv(
        USERS_FILE, mode="a", header=False, index=False
    )
    return {"status": "success", "message": "Signup successful"}, 200

def login_user(username, password):
    """Login logic."""
    users = pd.read_csv(USERS_FILE)
    if ((users["username"] == username) & (users["password"] == password)).any():
        return {"status": "success", "message": "Login successful"}, 200
    return {"status": "fail", "message": "Invalid credentials"}, 401
