import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from os import environ
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging

setup_logging(level="INFO")

RUFF_TARGETS = ["src", "streamlit_app", "tests", "gin-sim", "scripts", "noxfile.py"]
PYRIGHT_TARGETS = ["src"]
PYTEST_ARGS = [
    "tests/e2e/test_dashboard.py",
    "tests/e2e/test_dashboard_pages.py",
    "tests/unit/test_gin_sim_wrapper.py",
]
MIN_COVERAGE = float(environ.get("GDPE_MIN_COVERAGE", "45"))


@dataclass(frozen=True)
class Check:
    name: str
    command: list[str]


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


def require_success(check: Check) -> None:
    """Run a check and exit immediately on failure."""
    logger.info(f"Running {check.name}: {' '.join(check.command)}")
    rc, stdout, stderr = run_cmd(check.command)
    if rc != 0:
        logger.error(f"FAILED: {check.name}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        sys.exit(1)


def main():
    logger.info("=== Diamond Standard Quality Gate ===")
    checks = [
        Check("Ruff format", ["uv", "run", "ruff", "format", "--check", *RUFF_TARGETS]),
        Check("Ruff lint", ["uv", "run", "ruff", "check", *RUFF_TARGETS]),
        Check("Pyright", ["uv", "run", "pyright", *PYRIGHT_TARGETS]),
        Check(
            "Pytest fast suite",
            [
                "uv",
                "run",
                "pytest",
                "--cov=src",
                "--cov-report=xml",
                "--cov-report=term-missing:skip-covered",
                *PYTEST_ARGS,
            ],
        ),
    ]

    for check in checks:
        require_success(check)

    logger.info("Checking Coverage...")
    coverage = get_coverage()
    logger.info(f"Total Coverage: {coverage:.2f}%")
    if coverage < MIN_COVERAGE:
        logger.error(f"FAILED: Coverage {coverage:.2f}% is below required {MIN_COVERAGE:.2f}%")
        sys.exit(1)

    logger.success("QUALITY GATE: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
