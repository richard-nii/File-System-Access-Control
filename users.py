import json
import os

USERS_FILE = "data/users.json"
GROUPS_FILE = "data/groups.json"


def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)


# -------- GROUP MANAGEMENT --------

def create_group(group_name):
    groups = load_json(GROUPS_FILE)

    if group_name in groups:
        return False

    groups[group_name] = []
    save_json(GROUPS_FILE, groups)
    return True


def add_user_to_group(username, group_name):
    users = load_json(USERS_FILE)
    groups = load_json(GROUPS_FILE)

    if username not in users or group_name not in groups:
        return False

    if username not in groups[group_name]:
        groups[group_name].append(username)

    if group_name not in users[username]["groups"]:
        users[username]["groups"].append(group_name)

    save_json(GROUPS_FILE, groups)
    save_json(USERS_FILE, users)
    return True


def get_user_groups(username):
    users = load_json(USERS_FILE)
    return users.get(username, {}).get("groups", [])
