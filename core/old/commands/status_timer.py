import click
from datetime import datetime
from core.storage import load_timers
from core.timer_utils import get_last_session_start, is_timer_running

@click.command(name="status")
@click.argument("timer_id", required=False, type=int)
def status_timer_command(timer_id):
    """Show status for one timer or all timers."""
    timers = load_timers()
    total_all_seconds = 0

    def render_duration(seconds):
        h = seconds // 3600
        m = (seconds % 3600) % 60
        s = seconds % 60
        return f"{h}:{m:02}:{s:02}"

    if timer_id:
        timers = [t for t in timers if t["id"] == timer_id]

    output_lines = []
    for timer in timers:
        tid = timer["id"]
        ttitle = timer["title"]
        sessions = timer.get("sessions", [])
        running = is_timer_running(tid)

        # Add running session to the session list preview
        if running:
            result = get_last_session_start(tid)
            if result:
                start_time, session_title = result
                elapsed = datetime.now() - start_time
                elapsed_seconds = int(elapsed.total_seconds())
                sessions = sessions + [{
                    "title": session_title,
                    "duration_seconds": elapsed_seconds,
                    "running": True
                }]

        # Total timer duration
        total_seconds = sum(s["duration_seconds"] for s in sessions)
        total_all_seconds += total_seconds
        output_lines.append(f"{tid} {ttitle} {render_duration(total_seconds)}")

        # Sessions
        for i, session in enumerate(sessions, start=1):
            title = session.get("title", f"Session {i}")
            dur = render_duration(session["duration_seconds"])
            suffix = "..." if session.get("running") else ""
            branch = "└──" if i == len(sessions) else "├──"
            output_lines.append(f"{branch} {i} {title} {dur}{suffix}")

    output_lines.insert(0, f"Total Time {render_duration(total_all_seconds)}")
    click.echo("\n".join(output_lines))
