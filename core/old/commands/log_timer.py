import click
from datetime import datetime
from core.storage import get_data_paths, load_timers, save_timers
from core.timer_utils import parse_sessions_from_log, is_timer_running, insert_stop_before_start
from core.formatter import generate_markdown

@click.command(name="log")
@click.option("--clear", is_flag=True, help="Clear log after processing.")
def log_timer_command(clear):
    """Process log and update timers.json with sessions. Write log.md summary."""
    paths = get_data_paths()
    log_path = paths["log"]

    # Finalize any open sessions
    active_ids = _get_active_timer_ids(log_path.read_text().splitlines())
    timestamp = datetime.now().isoformat(timespec='minutes')
    for tid in active_ids:
        if is_timer_running(tid):
            insert_stop_before_start(tid, timestamp)

    # Parse and aggregate sessions
    sessions_by_id = parse_sessions_from_log()
    timers = load_timers()

    for timer in timers:
        tid = timer["id"]
        new_sessions = sessions_by_id.get(tid, [])
        timer["sessions"].extend(new_sessions)

    save_timers(timers)

    # Write markdown report
    md = generate_markdown(timers)
    paths["markdown"].write_text(md)

    if clear:
        log_path.write_text("")

    click.echo("📋 Sessions logged. Markdown saved to log.md.")

def _get_active_timer_ids(lines):
    active = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) < 3:
            continue
        tid, _, action = parts[0], parts[1], parts[2]
        active[tid] = action
    return [int(k) for k, v in active.items() if v == "Start"]
