"""Shared helpers for gin-sim deployment wrappers."""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_source_path(source_path: Path) -> None:
    """Execute a canonical Streamlit source file from an absolute path."""
    if not source_path.exists():
        message = f"Source dashboard not found at {source_path}"
        raise FileNotFoundError(message)

    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    os.chdir(REPO_ROOT)
    runpy.run_path(str(source_path), run_name="__main__")


def run_source(relative_source: str) -> None:
    """Execute a canonical Streamlit source file from the repository root."""
    run_source_path(REPO_ROOT / relative_source)
