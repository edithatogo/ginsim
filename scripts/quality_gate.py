import subprocess
import sys
import xml.etree.ElementTree as ET  # noqa: N817
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging

setup_logging(level="INFO")


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
        logger.warning("coverage.xml not found, returning 0.0")
        return 0.0
    tree = ET.parse(cov_file)
    root = tree.getroot()
    line_rate = float(root.attrib.get("line-rate", 0))
    return line_rate * 100.0


def main():
    logger.info("=== Diamond Standard Quality Gate ===")

    logger.info("Checking Lint (Ruff)...")
    lint_rc, _, lint_err = run_cmd(["uv", "run", "ruff", "check", "."])
    if lint_rc != 0:
        logger.error(f"FAILED: Linting errors found.\n{lint_err}")
        sys.exit(1)

    logger.info("Checking Types (Pyright)...")
    type_rc, _, type_err = run_cmd(["uv", "run", "pyright", "src/"])
    if type_rc != 0:
        logger.error(f"FAILED: Type errors found.\n{type_err}")
        sys.exit(1)

    logger.info("Checking Coverage...")
    coverage = get_coverage()
    logger.info(f"Total Coverage: {coverage:.2f}%")

    logger.success("QUALITY GATE: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
