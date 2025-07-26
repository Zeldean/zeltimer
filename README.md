# ⏱️ Zeltimer – Terminal Time Tracker

A simple yet powerful CLI tool for tracking multiple timers and recording session data. Designed for time tracking in study blocks, work sessions, meetings, or projects — right from your terminal.

---

## 📁 Project Structure

```

zeltimer/
├── app.py                      # Main CLI entry point (Click-based)
├── core/                       # Core logic and utilities
│   ├── timer\_manager.py        # Timer + session logic and logging
│   ├── storage.py              # JSON and log file helpers
│   └── utils.py                # Formatters and notifications
├── data/
│   ├── timers.json             # Structured timer & session history
│   ├── log.txt                 # Append-only raw log of events
│   └── log.md                  # Markdown export (optional)
├── assets/
│   └── zeltimer\_icon.png       # Icon for notify-send messages

````

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -e .
````

Make sure you have `libnotify` installed for desktop notifications (`notify-send`).

---

### 2. Run the app

```bash
zeltimer [COMMAND]
```

---

## ✅ Commands

### `zeltimer new <title>`

Create a new timer with a custom title.

```bash
zeltimer new "Study Timer"
```

---

### `zeltimer start <id> <session title> [--pomodoro]`

Start a new session.

* If one is already running, it auto-inserts a `Stop`.
* With `--pomodoro`, starts a Pomodoro-style cycle (see below).

```bash
zeltimer start 1 "WPR381 Reading"
zeltimer start 1 "Focused Session" --pomodoro --cycles 4 --work 25 --break 5
```

---

### `zeltimer stop <id>`

Stops the running session for the given timer.

```bash
zeltimer stop 1
```

---

### `zeltimer resume <id>`

Resumes the last session title of the given timer.

```bash
zeltimer resume 1
```

---

### `zeltimer status [id]`

Show session breakdown for a timer, or all active timers if no ID is given.

```bash
zeltimer status        # Shows all active timers
zeltimer status 1      # Shows one timer breakdown
```

Output looks like:

```
Timer 1 - Study Session
├── MLG382 Recap - 00:04:20
├── WPR381 - 00:12:17 (running)
└── Total Time Breakdown:
Total Time: 00:16:37
```

---

## 📦 Data Format

### `log.txt`

Append-only raw log:

```
1|2025-06-07T14:00:02|Start|Prep
1|2025-06-07T15:00:15|Stop
```

---

### `timers.json`

Structured cache built from log:

```json
[
  {
    "id": 1,
    "name": "Study Timer",
    "sessions": [
      {
        "title": "Prep",
        "start": "2025-06-07T14:00:02",
        "stop": "2025-06-07T15:00:15",
        "duration_seconds": 3613
      }
    ],
    "total_time": 3613,
    "archived": false
  }
]
```

---

## 🔔 Notifications

Zeltimer uses `notify-send` with a custom icon.

### Requirements

* `libnotify`
* Desktop WM that supports notifications (e.g. Hyprland, GNOME, KDE)

---

## 🧠 Design Principles

* Timers are persistent and can run concurrently
* Logs are append-only (`log.txt`)
* `timers.json` is rebuilt from logs on-demand
* Sessions have optional titles
* `Start` is always paired with `Stop` (auto if needed)

---

## 🌟 Planned Features

| Feature         | Description                                             | Status     |
| --------------- | ------------------------------------------------------- | ---------- |
| Pomodoro mode   | Auto-run start/stop cycles with break notifications     | 🔜 Planned     |
| `list` command  | Show all timers with active status + time summary       | 🔜 Planned |
| Session tags    | Add tags to group/filter sessions                       | 🔜 Planned |
| Markdown export | Save logs as a readable Markdown session report         | 🔜 Planned  |
| CSV export      | Export all sessions to CSV format                       | 🔜 Planned |
| Timer rename    | Rename a timer by ID                                    | 🔜 Planned |
| Archive toggle  | Hide unused timers from status unless explicitly listed | 🔜 Planned     |
| Curses UI       | Interactive terminal UI for managing timers             | 🔜 Planned |

---

## 🛠 Developer Tips

Test locally with:

```bash
zeltimer new "Test"
zeltimer start 1 "Reading"
zeltimer stop 1
zeltimer status 1
```

To test Pomodoro:

```bash
zeltimer start 1 "Pomodoro" --pomodoro --cycles 2 --work 1 --break 1
```

---

## 🧩 Credits

Built by **zeldean**
MIT Licensed
Logo and icon included in `/assets`

---
