def parse_permissions(perm):
    return {
        "owner": perm[0:3],
        "group": perm[3:6],
        "others": perm[6:9]
    }


def has_permission(fs_obj, user, user_groups, action):
    # 1️⃣ Check user ACL
    user_acl = fs_obj.get("acl", {}).get("users", {})
    if user in user_acl:
        return action[0] in user_acl[user]

    # 2️⃣ Check group ACL
    group_acl = fs_obj.get("acl", {}).get("groups", {})
    for g in user_groups:
        if g in group_acl:
            return action[0] in group_acl[g]

    # 3️⃣ Fall back to Unix permissions
    perm = fs_obj["permissions"]

    if fs_obj["owner"] == user:
        scope = perm[0:3]
    elif fs_obj["group"] in user_groups:
        scope = perm[3:6]
    else:
        scope = perm[6:9]

    return action[0] in scope

