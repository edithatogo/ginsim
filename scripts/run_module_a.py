#!/usr/bin/env python3
"""
Run individual module A: Behavior/Deterrence.

Usage:
    python -m scripts.run_module_a --policy status_quo
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.model.module_a_behavior_wrappers import (
    compute_testing_uptake,
    get_standard_policies,
)
from src.model.parameters import get_default_parameters
from src.utils.logging_config import setup_logging

setup_logging(level="INFO")


def main():
    parser = argparse.ArgumentParser(description="Run Module A: Behavior/Deterrence")
    parser.add_argument(
        "--policy",
        type=str,
        default="status_quo",
        choices=["status_quo", "moratorium", "ban"],
        help="Policy regime to evaluate",
    )
    parser.add_argument(
        "--output", type=str, default="outputs/runs/module_a", help="Output directory"
    )

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("MODULE A: BEHAVIOR/DETERRENCE")
    logger.info("=" * 60)

    # Load parameters
    params = get_default_parameters()
    logger.info(f"Loaded parameters for {params.jurisdiction}")

    # Get policy
    policies = get_standard_policies()
    policy = policies[args.policy]
    logger.info(f"Policy: {policy.name}")

    # Compute testing uptake
    uptake = compute_testing_uptake(params, policy)
    logger.info(f"Testing Uptake: {uptake:.4f}")

    # Save results
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "module": "A",
        "policy": args.policy,
        "testing_uptake": float(uptake),
        "parameters": {
            "baseline_testing_uptake": params.baseline_testing_uptake,
            "deterrence_elasticity": params.deterrence_elasticity,
            "moratorium_effect": params.moratorium_effect,
        },
    }

    output_file = output_dir / f"module_a_{args.policy}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    logger.success(f"Results saved to {output_file}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
