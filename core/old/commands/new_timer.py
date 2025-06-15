import click
from core.storage import load_timers, save_timers

@click.command(name="new")
@click.argument("title")
def new_timer_command(title):
    """Create a new timer with the given TITLE."""
    timers = load_timers()
    new_id = max((t["id"] for t in timers), default=0) + 1
    timers.append({
        "id": new_id,
        "title": title,
        "sessions": []
    })
    save_timers(timers)
    click.echo(f"✅ Created timer {new_id}: {title}")
