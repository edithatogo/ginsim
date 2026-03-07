import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def run_cmd(cmd_list):
    """Securely run a command and return output using UTF-8."""
    # Use capture_output=True and manual decode to ensure UTF-8 handling on Windows
    result = subprocess.run(cmd_list, capture_output=True)
    stdout = result.stdout.decode("utf-8", errors="replace")
    stderr = result.stderr.decode("utf-8", errors="replace")
    return result.returncode, stdout, stderr


def get_coverage():
    cov_file = Path("coverage.xml")
    if not cov_file.exists():
        return 0.0
    tree = ET.parse(cov_file)
    root = tree.getroot()
    line_rate = float(root.attrib.get("line-rate", 0))
    return line_rate * 100.0


def main():
    print("=== Diamond Standard Conductor Gate ===")

    print("Checking Lint (Ruff)...")
    lint_rc, _, lint_err = run_cmd(["uv", "run", "ruff", "check", "."])
    if lint_rc != 0:
        print(f"FAILED: Linting errors found.\n{lint_err}")
        sys.exit(1)

    print("Checking Types (Pyright)...")
    type_rc, _, type_err = run_cmd(["uv", "run", "pyright", "src/"])
    if type_rc != 0:
        print(f"FAILED: Type errors found.\n{type_err}")
        sys.exit(1)

    print("Checking Coverage...")
    coverage = get_coverage()
    print(f"Total Coverage: {coverage:.2f}%")

    print("RESULT: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
