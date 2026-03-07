import subprocess
from pathlib import Path


def get_git_logs():
    """Extract conventional commits from history."""
    try:
        res = subprocess.check_output(
            ["git", "log", "--pretty=format:%as|%s", "--since=1.day"], text=True
        )
        return res.split("\n")
    except:
        return []


def update_log(track_id):
    log_path = Path(f"conductor/tracks/{track_id}/LOG_OBSERVABILITY.md")
    if not log_path.exists():
        print(f"Error: Log not found at {log_path}")
        return

    logs = get_git_logs()

    with open(log_path, "a") as f:
        f.write("\n## Automated Audit Trail (Git Sync)\n\n")
        f.write("| Date | Action | Description |\n")
        f.write("|---|---|---|\n")
        for log in logs:
            if "|" in log:
                date, msg = log.split("|", 1)
                f.write(f"| {date} | Commit | {msg} |\n")


if __name__ == "__main__":
    update_log("gdpe_0023_unattended_loop_automation")
