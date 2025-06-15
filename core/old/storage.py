import json
from pathlib import Path

# Define base data directory
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

TIMERS_PATH = DATA_DIR / "timers.json"
ACTIVE_LOG_PATH = DATA_DIR / "active_log.txt"
LOG_MD_PATH = DATA_DIR / "log.md"

# Ensure timers.json exists
if not TIMERS_PATH.exists():
    TIMERS_PATH.write_text("[]")
if not ACTIVE_LOG_PATH.exists():
    ACTIVE_LOG_PATH.write_text("")

def load_timers():
    with TIMERS_PATH.open() as f:
        return json.load(f)

def save_timers(timers):
    with TIMERS_PATH.open("w") as f:
        json.dump(timers, f, indent=2)

def get_data_paths():
    return {
        "timers": TIMERS_PATH,
        "log": ACTIVE_LOG_PATH,
        "markdown": LOG_MD_PATH,
    }
