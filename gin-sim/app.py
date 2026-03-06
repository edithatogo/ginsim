#!/usr/bin/env python3
"""
Deployment wrapper for the public gin-sim Streamlit app.

The dashboard source of truth lives under ``streamlit_app/`` in the main
repository. This wrapper exists so Streamlit Cloud can keep using ``gin-sim``
as the deployment entrypoint without maintaining a second divergent app.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_APP = REPO_ROOT / "streamlit_app" / "app.py"


def main() -> None:
    """Execute the canonical dashboard app as the public deployment entrypoint."""
    if not SOURCE_APP.exists():
        message = f"Source dashboard not found at {SOURCE_APP}"
        raise FileNotFoundError(message)

    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    runpy.run_path(str(SOURCE_APP), run_name="__main__")


if __name__ == "__main__":
    main()
