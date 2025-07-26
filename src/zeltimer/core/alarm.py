"""zeltimer.py - tiny importable alarm helper.

Example
-------
from zeltimer import alarm
alarm("14:30")          # today at 14:30 or tomorrow if already past
alarm("10m", message="Stretch!")
alarm(datetime.datetime.now()+datetime.timedelta(seconds=5))
"""

from __future__ import annotations

import datetime as dt
import subprocess
import time
from pathlib import Path
from typing import Union

__all__ = ["alarm"]

_DEFAULT_AUDIO = (
    Path.home()
    / "Media"
    / "aud"
    / "Music"
    / "Out"
    / "brennan_savage_bulletproof.mp3"
)
_POLL = 0.5  # seconds between wake‑ups while waiting


def _parse_when(spec: str, now: dt.datetime) -> dt.datetime:
    """Translate a user‑friendly *spec* into an absolute datetime."""
    spec = spec.strip().lower()

    # Relative format like "5m" or "2h30m"
    if any(c in spec for c in "hm"):
        hrs = mins = 0
        num = ""
        for ch in spec:
            if ch.isdigit():
                num += ch
            elif ch == "h":
                hrs += int(num)
                num = ""
            elif ch == "m":
                mins += int(num)
                num = ""
        return now + dt.timedelta(hours=hrs, minutes=mins)

    # Bare clock "HH:MM"
    if ":" in spec and len(spec) <= 5:
        hour, minute = map(int, spec.split(":"))
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if candidate <= now:
            candidate += dt.timedelta(days=1)
        return candidate

    # Full ISO timestamp
    return dt.datetime.fromisoformat(spec)


def _sleep_until(target: dt.datetime) -> None:
    """Sleep in *POLL*‑sized chunks until *target* arrives."""
    while True:
        remaining = (target - dt.datetime.now(target.tzinfo)).total_seconds()
        if remaining <= 0:
            break
        time.sleep(min(_POLL, remaining))


def _play_audio(path: Path) -> None:
    """Try a few common players until one works."""
    players = [
        ["paplay", str(path)],
        ["ffplay", "-nodisp", "-autoexit", str(path)],
    ]
    for cmd in players:
        try:
            subprocess.run(cmd, check=False)
            return
        except FileNotFoundError:
            continue


def _notify(title: str, body: str) -> None:
    subprocess.run(["notify-send", title, body], check=False)


def alarm(
    when: Union[str, dt.datetime],
    *,
    audio: Path | str | None = None,
    message: str = "🔔 Alarm! Time's up!",
    tz: dt.tzinfo | None = None,
) -> None:
    """Block until *when*, then play sound + desktop notification.

    Parameters
    ----------
    when : str | datetime
        • "15m" or "2h30m" → relative dur.
        • "23:45"           → today/tomorrow at that clock time.
        • ISO string        → full timestamp.
        • datetime object   → used as‑is.
    audio : Path | str | None
        Custom sound file; None uses default.
    message : str
        Text shown in the desktop notification.
    tz : tzinfo | None
        Timezone to interpret naive datetimes; default local.

    Notes
    -----
    This call is **blocking** – it doesn't return until the alarm fires.
    """
    if isinstance(when, str):
        now = dt.datetime.now(tz)
        target = _parse_when(when, now)
    else:
        target = when

    _sleep_until(target)

    sound = Path(audio) if audio else _DEFAULT_AUDIO
    if sound.exists():
        _play_audio(sound)

    _notify("Zeltimer", message)
