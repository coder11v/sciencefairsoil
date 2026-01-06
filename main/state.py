import json
import os
from datetime import datetime

STATE_FILE = "out/state.json"

DEFAULT_STATE = {
    "last_watered_dumb": None,
    "last_smart_alert": None,
    "smart_soak_cycles": 0,
    "smart_system_disabled": False,
    "last_emergency_shutdown": None,
    "smart_disabled_count": 0
}

def _ensure_dir():
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

def load_state():
    _ensure_dir()

    if not os.path.exists(STATE_FILE):
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE.copy()

    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        # Corrupt state → fail safe
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE.copy()

def save_state(state):
    _ensure_dir()

    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, STATE_FILE)  # atomic write
