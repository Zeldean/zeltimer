import subprocess
from pathlib import Path

ICON_PATH = Path(__file__).resolve().parent.parent / "assets" / "zeltimer_icon.png"

def notify(title, message, app="Zeltimer"):
    subprocess.run([
        "notify-send",
        "-a", app,
        "-i", str(ICON_PATH),
        title,
        message
    ])

def timeBreakdown(seconds):
    """Convert seconds to HH:MM:SS (always whole numbers)."""
    seconds = int(seconds)  # ✅ FIX here
    hours = seconds // 3600
    remainder = seconds % 3600
    minutes = remainder // 60
    seconds = remainder % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
