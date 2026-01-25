import json
from filesystem import load_fs, save_fs
from audit import log_event


def set_user_acl(path, user, perms, actor):
    fs = load_fs()

    if path not in fs:
        return False

    fs[path]["acl"]["users"][user] = perms
    save_fs(fs)
    log_event(actor, "setfacl", f"{path} user:{user}:{perms}")
    return True


def set_group_acl(path, group, perms, actor):
    fs = load_fs()

    if path not in fs:
        return False

    fs[path]["acl"]["groups"][group] = perms
    save_fs(fs)
    log_event(actor, "setfacl", f"{path} group:{group}:{perms}")
    return True


def get_acl(path):
    fs = load_fs()
    if path not in fs:
        return None
    return fs[path]["acl"]
