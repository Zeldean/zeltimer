import click
from datetime import datetime
from core.storage import get_data_paths
from core.timer_utils import is_timer_running

@click.command(name="start")
@click.argument("timer_id", type=int)
@click.argument("title", required=False, default="")
def start_timer_command(timer_id, title):
    """Start a new session for the given TIMER_ID, with optional TITLE."""
    paths = get_data_paths()
    log_path = paths["log"]
    timestamp = datetime.now().isoformat(timespec='minutes')

    # If already running, auto-stop first
    if is_timer_running(timer_id):
        with log_path.open("a") as f:
            f.write(f"{timer_id}|{timestamp}|Stop\n")

    with log_path.open("a") as f:
        f.write(f"{timer_id}|{timestamp}|Start|{title}\n")

    click.echo(f"▶️ Timer {timer_id} started{' (' + title + ')' if title else ''}")
