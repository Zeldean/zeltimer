import subprocess
from pathlib import Path
import time
from zeltimer.core import timer_manager

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
    seconds = int(seconds)
    hours = seconds // 3600
    remainder = seconds % 3600
    minutes = remainder // 60
    seconds = remainder % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def runPomo(timer_id):
    """Run a 5-cycle test Pomodoro loop using timer ID."""
    for cycle in range(1, 6):
        subprocess.run(["zeltimer", "start", str(timer_id)])
        notify("Zeltimer", f"🔔 Pomodoro cycle {cycle} started.")
        target_time = 25 * 60

        while (totulDuration(cycle) < target_time):
            # comment:
            print(f"Cycle {cycle} in progress...")

        time.sleep(120)  # Simulated work period
        subprocess.run(["zeltimer", "stop", str(timer_id)])
        time.sleep(5)   # Simulated break period

    notify("Zeltimer", "✅ Pomodoro test completed.")

def totulDuration(cycle):
    
    return cycle*2

def alarm(alarm_time):
    """Play an alarm sound."""
    while datetime.datetime.now() < alarm_time:
        # Wait until the alarm time is reached
        continue
    subprocess.run(["paplay", r"/home/zeldean/Media/aud/Muisic/Out/brennan_savage_bulletproof.mp3"])
    notify("Zeltimer", "🔔 Alarm! Time's up!")