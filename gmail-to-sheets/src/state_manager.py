import json
import os

STATE_FILE = "state/processed_emails.json"


def load_processed_ids():
    if not os.path.exists(STATE_FILE):
        return set()

    with open(STATE_FILE, "r") as f:
        data = json.load(f)

    return set(data.get("processed_ids", []))


def save_processed_ids(processed_ids):
    with open(STATE_FILE, "w") as f:
        json.dump({"processed_ids": list(processed_ids)}, f, indent=2)
