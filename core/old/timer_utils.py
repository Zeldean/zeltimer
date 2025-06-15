from datetime import datetime
from core.storage import get_data_paths

def is_timer_running(timer_id):
    """Check if the given timer has an unclosed Start."""
    log_path = get_data_paths()["log"]
    lines = log_path.read_text().strip().splitlines()
    state = None
    for line in lines:
        parts = line.split('|')
        if parts[0] == str(timer_id):
            state = parts[2]
    return state == "Start"

def insert_stop_before_start(timer_id, timestamp):
    """Insert a Stop log entry before the next Start."""
    log_path = get_data_paths()["log"]
    lines = log_path.read_text().strip().splitlines()
    new_lines = []
    stop_inserted = False

    for i, line in enumerate(lines):
        parts = line.strip().split('|')
        if not stop_inserted and parts[0] == str(timer_id) and parts[2] == "Start":
            new_lines.append(f"{timer_id}|{timestamp}|Stop")
            stop_inserted = True
        new_lines.append(line)

    if stop_inserted:
        log_path.write_text('\n'.join(new_lines) + '\n')

def get_last_session_start(timer_id):
    """Returns (start_datetime, session_title) if running, else None."""
    log_path = get_data_paths()["log"]
    lines = log_path.read_text().strip().splitlines()
    last_event = None
    last_title = ""

    for line in lines:
        parts = line.split('|')
        if parts[0] != str(timer_id):
            continue
        if parts[2] == "Start":
            last_event = parts[1]
            last_title = parts[3] if len(parts) > 3 else ""
        elif parts[2] == "Stop":
            last_event = None

    if last_event:
        return datetime.fromisoformat(last_event), last_title
    return None

def get_last_session_title(timer_id):
    """Finds the most recent session title for this timer (even if closed)."""
    log_path = get_data_paths()["log"]
    lines = log_path.read_text().strip().splitlines()
    last_title = ""
    current = None
    for line in reversed(lines):
        parts = line.split('|')
        if parts[0] != str(timer_id):
            continue
        if parts[2] == "Start":
            last_title = parts[3] if len(parts) > 3 else ""
            break
    return last_title

def parse_sessions_from_log():
    """
    Parse the active_log.txt file and return sessions grouped by timer ID.

    Returns:
        dict[int, list[dict]]: { timer_id: [ { start, stop, duration_seconds, title }, ... ] }
    """
    log_path = get_data_paths()["log"]
    lines = log_path.read_text().strip().splitlines()

    sessions_by_id = {}
    current_sessions = {}

    for line in lines:
        parts = line.strip().split('|')
        if len(parts) < 3:
            continue

        tid = int(parts[0])
        timestamp = parts[1]
        action = parts[2]
        title = parts[3] if len(parts) > 3 else ""

        if action == "Start":
            current_sessions[tid] = {
                "start": timestamp,
                "title": title
            }
        elif action == "Stop" and tid in current_sessions:
            start_time = datetime.fromisoformat(current_sessions[tid]["start"])
            stop_time = datetime.fromisoformat(timestamp)
            duration = int((stop_time - start_time).total_seconds())

            session = {
                "title": current_sessions[tid]["title"],
                "start": current_sessions[tid]["start"],
                "stop": timestamp,
                "duration_seconds": duration
            }

            sessions_by_id.setdefault(tid, []).append(session)
            del current_sessions[tid]

    return sessions_by_id
