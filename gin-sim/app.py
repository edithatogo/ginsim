"""
Deployment wrapper for the public gin-sim Streamlit app.

The dashboard source of truth lives under ``streamlit_app/`` in the main
repository. This wrapper exists so Streamlit Cloud can keep using ``gin-sim``
as the deployment entrypoint without maintaining a second divergent app.
"""

from __future__ import annotations

import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from _runner import run_source_path

SOURCE_APP = CURRENT_DIR.parent / "streamlit_app" / "app.py"


def main() -> None:
    """Execute the canonical dashboard app as the public deployment entrypoint."""
    run_source_path(SOURCE_APP)


if __name__ == "__main__":
    main()
