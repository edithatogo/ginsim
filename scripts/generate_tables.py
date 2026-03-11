#!/usr/bin/env python3
"""
Generate publication-ready reporting tables from run outputs.

Usage:
    python -m scripts.generate_tables --meta_dir outputs/runs/meta_pipeline/20260306T010203Z
    python -m scripts.generate_tables --run_dir outputs/runs/full_uncertainty/australia_20260306T010203Z
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging
from scripts.reporting_common import build_reporting_bundle, write_reporting_tables

setup_logging(level="INFO")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reporting tables from model outputs")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--meta_dir",
        type=str,
        help="Meta-pipeline directory containing full_uncertainty jurisdiction run directories",
    )
    input_group.add_argument(
        "--run_dir",
        type=str,
        help="Single-jurisdiction full uncertainty run directory",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Output directory for generated tables (default: <meta_dir>/tables or <run_dir>/tables)",
    )
    args = parser.parse_args()

    meta_dir = Path(args.meta_dir) if args.meta_dir else None
    run_dir = Path(args.run_dir) if args.run_dir else None
    output_dir = (
        Path(args.output)
        if args.output
        else (meta_dir / "tables" if meta_dir is not None else run_dir / "tables")
    )

    logger.info("=" * 60)
    logger.info("TABLE GENERATION")
    logger.info("=" * 60)

    bundle = build_reporting_bundle(meta_dir=meta_dir, run_dir=run_dir)
    generated = write_reporting_tables(output_dir, bundle)

    logger.info(f"Source runs: {', '.join(sorted(bundle['run_dirs']))}")
    for name, path in generated.items():
        logger.success(f"  {name}: {path.name}")

    logger.info("=" * 60)
    logger.success(f"Reporting tables generated in {output_dir}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
