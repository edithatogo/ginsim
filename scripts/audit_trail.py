import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging
from src.utils.path_resolver import resolve_path

setup_logging(level="INFO")


def get_git_logs():
    """Extract conventional commits from history."""
    try:
        res = subprocess.check_output(
            ["git", "log", "--pretty=format:%as|%s", "--since=1.day"], text=True
        )
        return res.split("\n")
    except Exception:
        return []


def update_log(track_id):
    log_path = resolve_path(f"conductor/tracks/{track_id}/LOG_OBSERVABILITY.md")
    if not log_path.exists():
        logger.error(f"Log not found at {log_path}")
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
