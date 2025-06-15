import click
from datetime import datetime
from core.storage import get_data_paths
from core.timer_utils import is_timer_running

@click.command(name="stop")
@click.argument("timer_id", type=int)
def stop_timer_command(timer_id):
    """Stop the currently running session for TIMER_ID."""
    if not is_timer_running(timer_id):
        click.echo(f"⚠️ Timer {timer_id} is not currently running.")
        return

    timestamp = datetime.now().isoformat(timespec='minutes')
    log_path = get_data_paths()["log"]

    with log_path.open("a") as f:
        f.write(f"{timer_id}|{timestamp}|Stop\n")

    click.echo(f"⏹️ Timer {timer_id} stopped at {timestamp}")
