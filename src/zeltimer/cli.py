import click
from zeltimer.core import timer_manager
from zeltimer.core.alarm import alarm
from zeltimer.core import utils
import datetime

@click.group()
def timer() -> None:
    """Zeltimer CLI - Time tracking tool"""
    pass

@timer.command()
@click.argument("name")
def new(name):
    """Create new timer"""
    timer_manager.new_timer(name)
    utils.notify("Zeltimer", f"New timer '{name}' created.")

@timer.command()
@click.argument("timer_id", type=int)
@click.argument("session_name", required=False, default="Unnamed Session")
def start(timer_id, session_name):
    """Start timer"""
    timer_manager.start_timer(timer_id, session_name)
    utils.notify("Zeltimer", f"Timer {timer_id} started: {session_name}")

@timer.command()
@click.argument("timer_id", type=int)
def stop(timer_id):
    """Stop timer"""
    timer_manager.stop_timer(timer_id)
    utils.notify("Zeltimer", f"Timer {timer_id} stopped.")

@timer.command()
@click.argument("timer_id", type=int)
def resume(timer_id):
    """Resume timer"""
    timer_manager.resume_timer(timer_id)
    utils.notify("Zeltimer", f"Timer {timer_id} resumed.")

@timer.command()
@click.argument("timer_id", required=False, type=int)
def status(timer_id):
    """Show timer time breakdown (single or all timers)"""
    timer_manager.sync_state()
    timers = timer_manager.load_timers()

    def display_timer(timer):
        click.echo(f"\nTimer {timer['id']} - {timer['name']}")
        total_seconds = timer["total_time"]

        for session in timer["sessions"]:
            if session["stop"]:
                dur = session["duration_seconds"]
                live = ""
            else:
                start = datetime.datetime.fromisoformat(session["start"])
                dur = (datetime.datetime.now() - start).total_seconds()
                live = " (running)"
                total_seconds += dur

            click.echo(f"├── {session['title']} - {utils.timeBreakdown(dur)}{live}")

        click.echo(f"Total Time: {utils.timeBreakdown(total_seconds)}")

    if timer_id:
        timer = next((t for t in timers if t["id"] == timer_id), None)
        if not timer:
            click.echo(f"Timer ID {timer_id} not found.")
            utils.notify("Zeltimer", f"Timer {timer_id} not found.")
            return
        display_timer(timer)
    else:
        visible = [t for t in timers if not t.get("archived", False)]
        if not visible:
            click.echo("No active timers found.")
            return
        for t in visible:
            display_timer(t)

@timer.command()
@click.argument("timer_id", type=int)
def pomoTest(timer_id):
    """Run Pomodoro test with the given timer ID"""
    print("Pomodoro test Started.")
    utils.runPomo(timer_id);

@timer.command()
@click.argument("alarm_time", type=str)
def set_alarm(alarm_time):
    alarm(alarm_time)
    

# Entry point
if __name__ == "__main__":
    timer()
