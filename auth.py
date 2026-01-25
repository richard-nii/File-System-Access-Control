import json
import hashlib
import os

USERS_FILE = "data/users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate(username, password):
    users = load_users()
    if username not in users:
        return False

    hashed = hash_password(password)
    return users[username]["password"] == hashed


def create_user(username, password):
    users = load_users()
    if username in users:
        return False

    users[username] = {
        "password": hash_password(password),
        "groups": []
    }
    save_users(users)
    return True
