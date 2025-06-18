import click
from zeltimer.core import timer_manager

@click.group()
def cli():
    """Zeltimer CLI - Time tracking tool"""
    pass

@cli.command()
@click.argument("name")
def new(name):
    """Create new timer"""
    timer_manager.new_timer(name)

@cli.command()
@click.argument("timer_id", type=int)
@click.argument("session_name", required=False, default="Unnamed Session")
def start(timer_id, session_name):
    """Start timer"""
    timer_manager.start_timer(timer_id, session_name)

@cli.command()
@click.argument("timer_id", type=int)
def stop(timer_id):
    """Stop timer"""
    timer_manager.stop_timer(timer_id)

@cli.command()
@click.argument("timer_id", type=int)
def resume(timer_id):
    """Resume timer"""
    timer_manager.resume_timer(timer_id)

@cli.command()
@click.argument("timer_id", type=int)
def status(timer_id):
    """Show timer time breakdown"""
    timers = timer_manager.load_timers()
    timer = next((t for t in timers if t["id"] == timer_id), None)
    if not timer:
        click.echo(f"Timer ID {timer_id} not found.")
        return

    click.echo(f"Timer {timer_id} - {timer['name']}")
    total_minutes = timer["total_time"] // 60
    click.echo(f"Total Time: {total_minutes} min")

    for i, session in enumerate(timer["sessions"], 1):
        minutes = session["duration_seconds"] // 60
        click.echo(f"├── {session['title']} - {minutes} min")

# Entry point
if __name__ == "__main__":
    cli()
