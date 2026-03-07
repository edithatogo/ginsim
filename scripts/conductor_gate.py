import sys
import subprocess
from pathlib import Path


def run_cmd(cmd_list):
    """Securely run a command."""
    result = subprocess.run(cmd_list, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def check_lint():
    print("Running ruff check...")
    rc, out, err = run_cmd(["ruff", "check", "."])
    return rc == 0


def main():
    print("=== Conductor Phase Gate ===")
    lint_pass = check_lint()
    if lint_pass:
        print("RESULT: PASS")
        sys.exit(0)
    else:
        print("RESULT: FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
