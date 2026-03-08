"""
Logging configuration for genetic-discrimination-policy-econ.
Standardizes loguru sinks and formatting across CLI and dashboard.
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger


def setup_logging(level: str = "INFO", log_to_file: bool = True):
    """
    Configure loguru with research-grade formatting and optional file sink.
    """
    # Remove default handler
    logger.remove()

    # 1. Standard Console Sink (Colorized)
    format_str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    logger.add(sys.stderr, format=format_str, level=level)

    # 2. File Sink (Rotated, for auditability)
    if log_to_file:
        log_dir = Path("outputs/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        logger.add(
            log_dir / "pipeline_{time:YYYYMMDD}.log",
            rotation="10 MB",
            retention="1 month",
            compression="zip",
            format=format_str,
            level="DEBUG",
        )

    logger.info(f"Logging initialized at level: {level}")
    return logger
