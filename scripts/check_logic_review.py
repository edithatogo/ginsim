import sys
from pathlib import Path


def check_summaries():
    summaries = list(Path("conductor").rglob("PHASE_*_SUMMARY.md"))
    if not summaries:
        return 0

    for summary in summaries:
        with open(summary) as f:
            content = f.read()
            if "# Red Team Critique" not in content and "## 1. Critique" not in content:
                print(f"Error: Summary {summary} is missing a Red Team Critique section.")
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(check_summaries())
