import json
from pathlib import Path
import datetime
import os

# Resolve base directory safely
BASE_DIR = Path(__file__).resolve().parent.parent
_DATA_ROOT = Path(os.getenv("XDG_STATE_HOME", "~/.local/state")).expanduser() / "zel"
LOG_PATH = _DATA_ROOT / "timer_log.txt"
TIMER_PATH = _DATA_ROOT / "timers.json"

# TIMER MANAGEMENT ==========================================

def new_timer(timer_name="New Timer"):
    timers = load_timers()
    existing_ids = [timer["id"] for timer in timers]
    new_id = max(existing_ids, default=0) + 1
    new_timer = {
        "id": new_id,
        "name": timer_name,
        "pomodoro": {
            "cycles": 4,
            "work_time": 25,
            "break_time": 5
        },
        "sessions": [],
        "total_time": 0,
        "archived": False
    }
    timers.append(new_timer)
    save_timers(timers)
    print(f"Created new timer: ID={new_id}, Name='{timer_name}'")

def archive_timer(timer_id):
    timers = load_timers()
    for timer in timers:
        if timer["id"] == timer_id:
            timer["archived"] = True
            print(f"Archived timer ID {timer_id}.")
            break
    else:
        print(f"No timer found with ID {timer_id}.")
    save_timers(timers)

# TIMER OPERATIONS ==========================================

def start_timer(timer_id, session_name):
    logs = get_logs()
    filtered_logs = [log for log in logs if log[0] == str(timer_id)]
    logs_append = []
    log_time = datetime.datetime.now().isoformat(timespec="seconds")

    if filtered_logs and filtered_logs[-1][2] == "Start":
        logs_append.append([str(timer_id), log_time, "Stop"])
    logs_append.append([str(timer_id), log_time, "Start", session_name])

    log(logs_append)
    print(f"Timer {timer_id} started.")

def start_pomodoro(timer_id, session_name):
    logs = get_logs()
    filtered_logs = [log for log in logs if log[0] == str(timer_id)]
    logs_append = []
    log_time = datetime.datetime.now().isoformat(timespec="seconds")

    if filtered_logs and filtered_logs[-1][2] == "Start":
        logs_append.append([str(timer_id), log_time, "Stop"])
    logs_append.append([str(timer_id), log_time, "Start", session_name])

    log(logs_append)
    print(f"Timer {timer_id} started.")

def stop_timer(timer_id):
    logs = get_logs()
    filtered_logs = [log for log in logs if log[0] == str(timer_id)]
    
    if not filtered_logs:
        print(f"No log entries found for timer ID {timer_id}.")
        return

    last_event = filtered_logs[-1][2]

    if last_event == "Stop":
        print(f"Timer {timer_id} is already stopped.")
        return

    log_time = datetime.datetime.now().isoformat(timespec="seconds")
    logs_append = [[str(timer_id), log_time, "Stop"]]

    log(logs_append)
    print(f"Timer {timer_id} stopped.")

def resume_timer(timer_id):
    session_name, active = get_last_session(timer_id)

    if session_name is None:
        print(f"No previous sessions for timer {timer_id}. Cannot resume.")
        return

    if active:
        print(f"Timer {timer_id} is already running.")
        return

    log_time = datetime.datetime.now().isoformat(timespec="seconds")
    logs_append = [[str(timer_id), log_time, "Start", session_name]]
    log(logs_append)
    print(f"Resumed timer {timer_id} with session: {session_name}")

# FILE IO (JSON / LOG) ==========================================

def load_timers():
    if not TIMER_PATH.exists():
        return []
    with open(TIMER_PATH, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

def save_timers(timers):
    with open(TIMER_PATH, "w") as f:
        json.dump(timers, f, indent=4)

def create_save():
    # meant to store the timers in a more permanant json file save.json and then clear the log.txt should only be able to save stoped timers
    print(".")

def load_save():
    # meant to load the save.json file content into the timers.json file and then work on timers as normal need to be loaded before any other operations on timers.json becuse it sessions list is cleard on status call
    print(".")

def get_logs():
    if not LOG_PATH.exists():
        return []
    with open(LOG_PATH, "r") as f:
        logs = f.readlines()
        logs_split = [log.strip().split('|', 4) for log in logs]
    return logs_split

def log(logs):
    with open(LOG_PATH, "a") as f:
        f.writelines(['|'.join(log) + '\n' for log in logs])

# SESSION PARSING ==========================================

def get_last_session(timer_id):
    logs = get_logs()
    filtered_logs = [log for log in logs if log[0] == str(timer_id)]

    for log in reversed(filtered_logs):
        if log[2] == "Start":
            session_name = log[3] if len(log) > 3 else f"Session {timer_id}"
            index = filtered_logs.index(log)
            active = True
            if index + 1 < len(filtered_logs):
                if filtered_logs[index + 1][2] == "Stop":
                    active = False
            return session_name, active
    return None, False

# LOG PARSING -> STATE BUILDING ==========================================

def build_state_from_log():
    """
    Parses full log.txt into rebuilt timer state.
    Returns list of timers with sessions and total time.
    """
    logs = get_logs()
    timers = load_timers()

    # Build timer lookup for fast access
    timer_lookup = {t["id"]: t for t in timers}

    # Reset sessions and total_time for rebuild
    for t in timer_lookup.values():
        t["sessions"] = []
        t["total_time"] = 0

    for log in logs:
        timer_id = int(log[0])
        timestamp = datetime.datetime.fromisoformat(log[1])
        action = log[2]
        title = log[3] if len(log) > 3 else f"Session {timer_id}"

        # Create timer if it doesn't exist
        if timer_id not in timer_lookup:
            timer_lookup[timer_id] = {
                "id": timer_id,
                "name": f"Timer {timer_id}",
                "sessions": [],
                "total_time": 0,
                "archived": False
            }

        timer = timer_lookup[timer_id]

        if action == "Start":
            timer["sessions"].append({
                "title": title,
                "start": timestamp.isoformat(timespec="seconds"),
                "stop": None,
                "duration_seconds": 0
            })
        elif action == "Stop":
            if timer["sessions"]:
                current = timer["sessions"][-1]
                if current["stop"] is None:
                    current["stop"] = timestamp.isoformat(timespec="seconds")
                    delta = (datetime.datetime.fromisoformat(current["stop"]) - datetime.datetime.fromisoformat(current["start"])).total_seconds()
                    current["duration_seconds"] = int(delta)
                    timer["total_time"] += int(delta)

    return list(timer_lookup.values())


# SYNC STATE ==========================================

def sync_state():
    """
    Rebuild state from logs and save it into timers.json.
    """
    state = build_state_from_log()
    save_timers(state)
