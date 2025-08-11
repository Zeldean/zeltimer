# ⏱️ Zeltimer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Last Commit](https://img.shields.io/github/last-commit/Zeldean/zeltimer)
![Issues](https://img.shields.io/github/issues/Zeldean/zeltimer)
![Repo Size](https://img.shields.io/github/repo-size/Zeldean/zeltimer)

**Zeltimer** is a terminal-based time tracker for managing multiple timers, recording sessions, and keeping your work organized.  
It supports session resuming, archiving inactive timers, and will soon feature a full **Pomodoro mode** for focused work cycles.

Part of the **Zel-suite** of tools:
- [`zeltimer`](https://github.com/Zeldean/zeltimer) — time tracking
- `zeltask` — task tracking *(coming soon)*
- `zeljournal` — exports timers & tasks to Markdown *(coming soon)*

---

## 🚀 Overview

Zeltimer helps you track how you spend your time — whether it's studying, coding, or working on personal projects — directly from the terminal.

- **Multiple concurrent timers**  
- **Persistent logs** between sessions  
- **Quick start/stop/resume commands**  
- **Archiving** for timers you’re not using  
- **Pomodoro support** *(planned feature)*  
- **Desktop notifications** with custom icon  

---

## 📦 Installation

### From source
```bash
git clone https://github.com/Zeldean/zeltimer.git
cd zeltimer
pip install -e .
````

### With `pipx` (recommended for CLI tools)

```bash
pipx install git+https://github.com/Zeldean/zeltimer.git
```

**Requirements**:

* Python 3.10+
* [click](https://pypi.org/project/click/)
* Linux desktop with `notify-send` for notifications

---

## 💻 Usage

General syntax:

```bash
zeltimer [COMMAND] [ARGS]
```

### Commands

| Command                     | Description                                             |
| --------------------------- | ------------------------------------------------------- |
| `new <name>`                | Create a new timer                                      |
| `start <id> [session name]` | Start a timer (auto-stops active session on same timer) |
| `stop <id>`                 | Stop the current session                                |
| `resume <id>`               | Resume the last session                                 |
| `status [id]`               | Show session breakdown for one or all timers            |

### Example session

```bash
# Create a new timer
zeltimer new "Study Session"

# Start it with a session name
zeltimer start 1 "Math Homework"

# Stop the timer
zeltimer stop 1

# Check status
zeltimer status 1
```

---

## ✨ Features

✅ Multiple timers with separate sessions
✅ Auto-stop on new session start for same timer
✅ Persistent storage in `~/.local/state/zel`
✅ Resume support for previous sessions
✅ Archive timers when not in use
📢 Desktop notifications (with icon)
🔄 Pomodoro cycles *(planned)*

---

## 🛠 Planned Features

* **Pomodoro Mode**: Per-timer configuration for cycles, work time, break time.
* Timer archiving toggle.
* Date filtering for session history (`--today`, `--date <YYYY-MM-DD>`).
* TUI frontend.
* Full integration with `zeljournal`.

---

## 📂 Data Storage

Your data is stored in the XDG state directory:

```
~/.local/state/zel/
```

* `timers.json` — all timers and sessions
* `log.txt` — raw event log

You can back up or sync these files if needed.

---

## 🤝 Related Projects

* `zeltask` — terminal-based task tracker *(coming soon)*
* `zeljournal` — exports timers & tasks to Markdown *(coming soon)*

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
