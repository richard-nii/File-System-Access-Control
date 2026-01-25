import json
import datetime

AUDIT_FILE = "data/audit.log"


def log_event(user, action, target):
    entry = {
        "time": datetime.datetime.now().isoformat(),
        "user": user,
        "action": action,
        "target": target
    }

    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
