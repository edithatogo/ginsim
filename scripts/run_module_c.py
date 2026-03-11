#!/usr/bin/env python3
"""
Run individual module C: Insurance Equilibrium.

Usage:
    python -m scripts.run_module_c --policy status_quo
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.model.module_c_insurance_eq import (
    pooling_equilibrium,
    separating_equilibrium,
)
from src.model.parameters import PolicyConfig, get_default_parameters
from src.utils.logging_config import setup_logging

setup_logging(level="INFO")


def main():
    parser = argparse.ArgumentParser(description="Run Module C: Insurance Equilibrium")
    parser.add_argument(
        "--policy",
        type=str,
        default="status_quo",
        choices=["status_quo", "moratorium", "ban"],
        help="Policy regime to evaluate",
    )
    parser.add_argument(
        "--output", type=str, default="outputs/runs/module_c", help="Output directory"
    )

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("MODULE C: INSURANCE EQUILIBRIUM")
    logger.info("=" * 60)

    # Load parameters
    params = get_default_parameters()
    logger.info(f"Loaded parameters for {params.jurisdiction}")

    # Get policy
    policy = PolicyConfig(
        name=args.policy,
        description=f"{args.policy} policy",
        allow_genetic_test_results=(args.policy == "status_quo"),
    )
    logger.info(f"Policy: {policy.name}")

    # Compute equilibrium
    logger.info("Computing equilibrium...")

    if args.policy == "status_quo":
        eq = separating_equilibrium(params)
        eq_type = "Separating"
    else:
        eq = pooling_equilibrium(params)
        eq_type = "Pooling"

    logger.info(f"Equilibrium Type: {eq_type}")
    logger.info(f"High-risk premium: {eq.premium_high:.4f}")
    logger.info(f"Low-risk premium: {eq.premium_low:.4f}")

    # Save results
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "module": "C",
        "policy": args.policy,
        "equilibrium_type": eq_type,
        "premium_high": float(eq.premium_high),
        "premium_low": float(eq.premium_low),
        "parameters": {
            "adverse_selection_elasticity": params.adverse_selection_elasticity,
            "demand_elasticity_high_risk": params.demand_elasticity_high_risk,
            "baseline_loading": params.baseline_loading,
        },
    }

    output_file = output_dir / f"module_c_{args.policy}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    logger.success(f"Results saved to {output_file}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
