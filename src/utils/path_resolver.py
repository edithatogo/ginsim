"""
Central path resolver for genetic-discrimination-policy-econ.
Handles fallback between public and local_only directories.
"""
from __future__ import annotations

from pathlib import Path

from src.utils.logging_config import logger


def resolve_path(relative_path: str | Path) -> Path:
    """
    Resolve a path, checking for existence in the root directory
    and falling back to local_only/ if not found.
    """
    path = Path(relative_path)

    # 1. Check if path already exists relative to current working directory
    if path.exists():
        logger.debug(f"Resolved path directly: {path}")
        return path.absolute()

    # 2. Check in local_only/
    local_path = Path("local_only") / path
    if local_path.exists():
        logger.debug(f"Resolved path via local_only: {local_path}")
        return local_path.absolute()

    # 3. Handle cases where the script might be running from a subdirectory (like scripts/)
    current = Path.cwd()
    for _ in range(3):
        if (current / path).exists():
            resolved = (current / path).absolute()
            logger.debug(f"Resolved path by climbing: {resolved}")
            return resolved
        if (current / "local_only" / path).exists():
            resolved = (current / "local_only" / path).absolute()
            logger.debug(f"Resolved path by climbing (local_only): {resolved}")
            return resolved
        current = current.parent

    logger.warning(f"Could not resolve path: {relative_path}")
    return path.absolute()
