import json
import os
from permissions import has_permission
from audit import log_event

FILESYSTEM_FILE = "data/filesystem.json"


def load_fs():
    if not os.path.exists(FILESYSTEM_FILE):
        return {}
    with open(FILESYSTEM_FILE, "r") as f:
        return json.load(f)


def save_fs(fs):
    with open(FILESYSTEM_FILE, "w") as f:
        json.dump(fs, f, indent=2)


def create_dir(path, owner, group=None, permissions=None):
    fs = load_fs()

    if path in fs:
        return False

    parent = get_parent(path)

    if parent and parent in fs:
        parent_obj = fs[parent]
        group = parent_obj["group"]
        permissions = parent_obj["permissions"]
        acl = parent_obj["acl"].copy()
    else:
        acl = {"users": {}, "groups": {}}
        permissions = permissions or "rwxr-x---"
        group = group or owner

    fs[path] = {
        "type": "dir",
        "owner": owner,
        "group": group,
        "permissions": permissions,
        "acl": acl
    }

    save_fs(fs)
    log_event(owner, "mkdir", path)
    return True



def create_file(path, owner, group=None, permissions=None):
    fs = load_fs()

    if path in fs:
        return False

    parent = get_parent(path)

    if parent and parent in fs:
        parent_obj = fs[parent]
        group = parent_obj["group"]
        permissions = parent_obj["permissions"]
        acl = parent_obj["acl"].copy()
    else:
        acl = {"users": {}, "groups": {}}
        permissions = permissions or "rw-r-----"
        group = group or owner

    fs[path] = {
        "type": "file",
        "owner": owner,
        "group": group,
        "permissions": permissions,
        "acl": acl
    }

    save_fs(fs)
    log_event(owner, "touch", path)
    return True


def list_dir(user, user_groups):
    fs = load_fs()
    visible = []

    for path, obj in fs.items():
        if has_permission(obj, user, user_groups, "read"):
            visible.append(path)

    return visible


def read_file(path, user, user_groups):
    fs = load_fs()

    if path not in fs:
        return None

    obj = fs[path]
    if obj["type"] != "file":
        return None

    if not has_permission(obj, user, user_groups, "read"):
        return "PERMISSION_DENIED"

    log_event(user, "read", path)
    return f"Reading file: {path}"



def get_parent(path):
    if "/" not in path.strip("/"):
        return None
    return "/" + "/".join(path.strip("/").split("/")[:-1])
