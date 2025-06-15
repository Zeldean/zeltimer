def generate_markdown(timers):
    """Generate a markdown report of all timers and their sessions."""
    lines = ["# Timer Report", ""]

    for timer in timers:
        lines.append(f"## {timer['title']} (ID: {timer['id']})")
        lines.append("")
        lines.append("| Session Title | Start Time         | End Time           | Duration  |")
        lines.append("|---------------|--------------------|--------------------|-----------|")

        total_seconds = 0

        for session in timer.get("sessions", []):
            title = session.get("title", "")
            start = session["start"]
            stop = session["stop"]
            duration = format_duration(session["duration_seconds"])
            total_seconds += session["duration_seconds"]

            lines.append(f"| {title or '-'} | {start} | {stop} | {duration} |")

        lines.append(f"\n**Total Time: {format_duration(total_seconds)}**\n")
        lines.append("---")

    return "\n".join(lines)


def format_duration(seconds):
    """Convert seconds to '1h 3m 42s' format."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    parts = []
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    if s or not parts:
        parts.append(f"{s}s")
    return " ".join(parts)
