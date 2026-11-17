#!/usr/bin/env python3
"""
Extract and catalogue all mathematical formulae from the model source code.

Usage:
    python -m scripts.extract_formulae --output docs/FORMULAE_INVENTORY.md
"""

import argparse
import re
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging

setup_logging(level="INFO")


def extract_formulae_from_file(file_path: Path) -> list[dict]:
    """Extract formulae from a Python file."""
    formulae = []

    with file_path.open(encoding="utf-8") as f:
        content = f.read()
        lines = content.split("\n")

    # Pattern to match mathematical expressions in comments and docstrings
    latex_pattern = r"\$([^$]+)\$"
    r_pattern = r'r[\'"]([^\'"]+)[\'"]'

    for i, line in enumerate(lines, 1):
        # Look for LaTeX-style math in comments
        matches = re.findall(latex_pattern, line)
        formulae.extend(
            {
                "file": str(file_path),
                "line": i,
                "formula": match,
                "context": line.strip(),
            }
            for match in matches
        )

        # Look for r-strings with math (common in JAX code)
        if 'r"' in line or "r'" in line:
            matches = re.findall(r_pattern, line)
            formulae.extend(
                {
                    "file": str(file_path),
                    "line": i,
                    "formula": match,
                    "context": line.strip(),
                }
                for match in matches
                if any(
                    op in match
                    for op in ["=", "+", "-", "*", "/", "^", "sum", "prod", "exp", "log"]
                )
            )

    return formulae


def categorize_formulae(formulae: list[dict]) -> dict[str, list[dict]]:
    """Categorize formulae by module."""
    categories = {
        "Module A (Behavior)": [],
        "Module C (Insurance)": [],
        "Module D (Proxy)": [],
        "Module E (Pass-Through)": [],
        "Module F (Data Quality)": [],
        "Enforcement": [],
        "VOI/Sensitivity": [],
        "Other": [],
    }

    for formula in formulae:
        file_path = formula["file"]
        if "module_a" in file_path:
            categories["Module A (Behavior)"].append(formula)
        elif "module_c" in file_path or "insurance" in file_path:
            categories["Module C (Insurance)"].append(formula)
        elif "module_d" in file_path or "proxy" in file_path:
            categories["Module D (Proxy)"].append(formula)
        elif "module_e" in file_path or "passthrough" in file_path:
            categories["Module E (Pass-Through)"].append(formula)
        elif "module_f" in file_path or "data_quality" in file_path:
            categories["Module F (Data Quality)"].append(formula)
        elif "enforcement" in file_path:
            categories["Enforcement"].append(formula)
        elif "voi" in file_path or "sensitivity" in file_path:
            categories["VOI/Sensitivity"].append(formula)
        else:
            categories["Other"].append(formula)

    return categories


def generate_inventory(categorized: dict[str, list[dict]], output_path: Path) -> None:
    """Generate formula inventory markdown file."""
    with output_path.open("w", encoding="utf-8") as f:
        f.write("# Formulae Inventory\n\n")
        f.write("**Track:** gdpe_0006_formulae_verification  \n")
        f.write("**Date:** 2026-03-03  \n")
        f.write("**Version:** 1.0\n\n")
        f.write("---\n\n")

        total = 0
        for category, formulae in categorized.items():
            if not formulae:
                continue

            f.write(f"## {category}\n\n")
            f.write(f"**Count:** {len(formulae)} formulae\n\n")

            for i, formula in enumerate(formulae, 1):
                formula_id = f"{category.split()[0]}-{i:03d}"
                f.write(f"### {formula_id}\n\n")
                f.write(f"**Location:** `{formula['file']}` (line {formula['line']})\n\n")
                f.write(f"**Formula:** `{formula['formula']}`\n\n")
                f.write(f"**Context:** `{formula['context']}`\n\n")
                f.write("**Verification:** ⏳ Pending\n\n")
                f.write("**Reference:** Not yet assigned\n\n")
                f.write("---\n\n")

            total += len(formulae)

        f.write("## Summary\n\n")
        f.write(f"**Total Formulae:** {total}\n\n")
        f.write("| Category | Count |\n")
        f.write("|----------|-------|\n")
        for category, formulae in categorized.items():
            f.write(f"| {category} | {len(formulae)} |\n")
        f.write(f"| **Total** | **{total}** |\n\n")


def main():
    parser = argparse.ArgumentParser(description="Extract formulae from source code")
    parser.add_argument("--src", type=str, default="src/model", help="Source directory to scan")
    parser.add_argument(
        "--output",
        type=str,
        default="docs/FORMULAE_INVENTORY.md",
        help="Output file for formula inventory",
    )

    args = parser.parse_args()

    src_dir = Path(args.src)
    output_path = Path(args.output)

    logger.info("=" * 60)
    logger.info("FORMULAE EXTRACTION")
    logger.info("=" * 60)

    # Extract formulae from all Python files
    all_formulae = []
    for py_file in src_dir.glob("**/*.py"):
        logger.info(f"Scanning {py_file}...")
        formulae = extract_formulae_from_file(py_file)
        all_formulae.extend(formulae)

    logger.info(f"Found {len(all_formulae)} formulae")

    # Categorize formulae
    categorized = categorize_formulae(all_formulae)

    # Generate inventory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_inventory(categorized, output_path)

    logger.success(f"Formula inventory saved to {output_path}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
