#!/usr/bin/env python3
"""
Run individual module A: Behavior/Deterrence.

Usage:
    python -m scripts.run_module_a --policy status_quo
"""

import argparse
import json
from pathlib import Path

from src.model.module_a_behavior_wrappers import (
    compute_testing_uptake,
    get_standard_policies,
)
from src.model.parameters import get_default_parameters


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

    print("=" * 60)
    print("MODULE A: BEHAVIOR/DETERRENCE")
    print("=" * 60)

    # Load parameters
    params = get_default_parameters()
    print(f"Loaded parameters for {params.jurisdiction}")

    # Get policy
    policies = get_standard_policies()
    policy = policies[args.policy]
    print(f"Policy: {policy.name}")

    # Compute testing uptake
    uptake = compute_testing_uptake(params, policy)
    print(f"\nTesting Uptake: {uptake:.4f}")

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

    print(f"\n✓ Results saved to {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
