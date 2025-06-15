import click
from datetime import datetime
from core.storage import get_data_paths
from core.timer_utils import is_timer_running, get_last_session_title

@click.command(name="resume")
@click.argument("timer_id", type=int)
def resume_timer_command(timer_id):
    """Resume the last session for TIMER_ID using the same title."""
    paths = get_data_paths()
    log_path = paths["log"]
    timestamp = datetime.now().isoformat(timespec='minutes')

    if is_timer_running(timer_id):
        with log_path.open("a") as f:
            f.write(f"{timer_id}|{timestamp}|Stop\n")

    last_title = get_last_session_title(timer_id)
    with log_path.open("a") as f:
        f.write(f"{timer_id}|{timestamp}|Start|{last_title}\n")

    click.echo(f"🔁 Timer {timer_id} resumed ({last_title})")
