#!/usr/bin/env python3
"""
Sync Manuscript Data (Diamond Standard).

Runs the full policy sweep and updates the authoritative results manifest
for automated manuscript injection.
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.model.parameters import load_jurisdiction_parameters
from src.model.pipeline import run_full_pipeline
from src.utils.logging_config import setup_logging

setup_logging(level="INFO")

OUTPUT_FILE = project_root / "outputs" / "results_manifest.json"

def main():
    logger.info("Starting Manuscript Data Sync...")

    jurisdictions = ["australia", "new_zealand", "uk", "canada", "us"]
    manifest = {}

    for j in jurisdictions:
        logger.info(f"Processing {j}...")
        params = load_jurisdiction_parameters(j)
        results = run_full_pipeline(params=params)

        for p_name, res in results.items():
            prefix = f"{j.upper()}_{p_name.upper()}"
            manifest[f"{prefix}_UPTAKE"] = f"{float(res.testing_uptake):.4f}"
            manifest[f"{prefix}_WELFARE"] = f"{float(res.welfare_impact):.2f}"
            manifest[f"{prefix}_COMPLIANCE"] = f"{float(res.compliance_rate):.4f}"

    # Save manifest
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    logger.success(f"Manifest updated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
