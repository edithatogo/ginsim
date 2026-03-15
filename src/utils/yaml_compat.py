"""
Compatibility helpers for loading YAML in constrained runtimes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load_yaml_path(path: Path) -> Any:
    """Load YAML from disk with a narrow fallback chain."""
    raw_bytes = path.read_bytes()

    try:
        import yaml  # type: ignore[import-not-found]
    except Exception:
        yaml = None

    if yaml is not None:
        return yaml.safe_load(raw_bytes.decode("utf-8"))

    try:
        from msgspec import yaml as msgspec_yaml
    except Exception as exc:
        msg = (
            "No YAML loader is available. Install PyYAML or msgspec to read "
            f"configuration from {path}."
        )
        raise RuntimeError(msg) from exc

    return msgspec_yaml.decode(raw_bytes)
