# ⏱️ Terminal Time Tracker

A simple yet powerful CLI tool for tracking multiple timers and recording session data. Designed for time tracking in meetings, work sessions, study blocks, or projects — right from your terminal.

---

## 📁 Project Structure

```
time_tracker/
├── timer.py                  # Main CLI entry point using Click
├── commands/                 # CLI command modules
│   ├── new_timer.py
│   ├── start_timer.py
│   ├── stop_timer.py
│   ├── status_timer.py
│   └── log_timer.py
├── core/                     # Core logic and utilities
│   ├── storage.py            # Handles file paths and JSON I/O
│   ├── timer_utils.py        # Session and timer logic
│   └── formatter.py          # Markdown formatting
├── data/                     # Automatically managed data files
│   ├── timers.json           # Stores all timers and session history
│   ├── active_log.txt        # Append-only raw log of Start/Stop events
│   └── log.md                # Generated Markdown session report
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install click
```

### 2. Run the app

```bash
python timer.py [COMMAND]
```

---

## ✅ Commands

### `new <title>`

Create a new timer with a custom title.

```bash
python timer.py new "Client Meeting"
```

### `start <id> <optional session title>`

Start a new session for the given timer ID. If a session is already active, it auto-inserts a `Stop` **just before** this new start.

```bash
python timer.py start 1 "Prep Time"
```

### `stop <id>`

Stops the currently running session (if active).

```bash
python timer.py stop 1
```

### `status <id>`

Shows the current status of the timer and elapsed time if it’s running.

```bash
python timer.py status 1
```

### `log [--clear]`

Finalizes all active sessions, parses the event log, calculates durations, updates `timers.json`, and writes a summary to `log.md`.

```bash
python timer.py log --clear
```

---

## 📦 Data File Format

### `active_log.txt` (raw log)

```
1|2025-06-07T14:00|Start|Prep
1|2025-06-07T15:00|Stop
1|2025-06-07T15:00|Start|Intro
```

### `timers.json` (structured)

```json
[
  {
    "id": 1,
    "title": "Client Meeting",
    "sessions": [
      {
        "title": "Prep",
        "start": "2025-06-07T14:00",
        "stop": "2025-06-07T15:00",
        "duration_seconds": 3600
      }
    ]
  }
]
```

---

## 📝 `log.md` Example Output

```
# Timer Report

## Client Meeting

| Session       | Start               | Stop                | Duration |
|---------------|---------------------|---------------------|----------|
| Prep          | 2025-06-07T14:00    | 2025-06-07T15:00    | 1h 0m    |
```

---

## 🌟 Planned / Optional Features

| Feature       | Description                                     | Status     |
| ------------- | ----------------------------------------------- | ---------- |
| `edit <id>`   | Rename a timer                                  | 🔜 Planned |
| `delete <id>` | Delete a timer and its sessions                 | 🔜 Planned |
| `list`        | Show all timers with total time + active status | 🔜 Planned |
| Export CSV    | Export session data to `.csv`                   | 🔜 Planned |
| Tag Sessions  | Add tags to sessions for filtering              | 🔜 Planned |
| `export`      | Export all data to `.json` or `.csv`            | 🔜 Planned |

---

## 🧠 Design Principles

* **Multiple timers** can run independently.
* Every `Start` is always paired with a `Stop` (auto-inserted if needed).
* All raw data is kept in `active_log.txt` and parsed on-demand.
* Structured and readable summaries are saved to `timers.json` and `log.md`.

---

## 🛠 Developer Tips

* To test in dev, try:

```bash
python timer.py new "Example"
python timer.py start 1 "Session A"
python timer.py stop 1
python timer.py start 1 "Session B"
python timer.py log --clear
```

---
