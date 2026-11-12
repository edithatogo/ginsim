"""Deployment wrapper for the game diagrams dashboard page."""

from __future__ import annotations

import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
GIN_SIM_DIR = CURRENT_DIR.parent
if str(GIN_SIM_DIR) not in sys.path:
    sys.path.insert(0, str(GIN_SIM_DIR))

from _runner import run_source_path

SOURCE_PAGE = GIN_SIM_DIR.parent / "streamlit_app" / "pages" / "1_Game_Diagrams.py"


def main() -> None:
    """Execute the canonical game diagrams page."""
    run_source_path(SOURCE_PAGE)


if __name__ == "__main__":
    main()
