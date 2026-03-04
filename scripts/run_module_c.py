#!/usr/bin/env python3
"""
Run individual module C: Insurance Equilibrium.

Usage:
    python -m scripts.run_module_c --policy status_quo
"""

import argparse
import json
from pathlib import Path
from src.model.parameters import ModelParameters, PolicyConfig
from src.model.module_c_insurance_eq import (
    separating_equilibrium,
    pooling_equilibrium,
    compute_equilibrium,
)


def main():
    parser = argparse.ArgumentParser(description='Run Module C: Insurance Equilibrium')
    parser.add_argument('--policy', type=str, default='status_quo',
                       choices=['status_quo', 'moratorium', 'ban'],
                       help='Policy regime to evaluate')
    parser.add_argument('--output', type=str, default='outputs/runs/module_c',
                       help='Output directory')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("MODULE C: INSURANCE EQUILIBRIUM")
    print("=" * 60)
    
    # Load parameters
    params = ModelParameters()
    print(f"Loaded parameters for {params.jurisdiction}")
    
    # Get policy
    policy = PolicyConfig(
        name=args.policy,
        description=f'{args.policy} policy',
        allow_genetic_test_results=(args.policy == 'status_quo'),
    )
    print(f"Policy: {policy.name}")
    
    # Compute equilibrium
    print("\nComputing equilibrium...")
    
    if args.policy == 'status_quo':
        eq = separating_equilibrium(params)
        eq_type = 'Separating'
    else:
        eq = pooling_equilibrium(params)
        eq_type = 'Pooling'
    
    print(f"Equilibrium Type: {eq_type}")
    print(f"High-risk premium: {eq.premium_high:.4f}")
    print(f"Low-risk premium: {eq.premium_low:.4f}")
    
    # Save results
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {
        'module': 'C',
        'policy': args.policy,
        'equilibrium_type': eq_type,
        'premium_high': float(eq.premium_high),
        'premium_low': float(eq.premium_low),
        'parameters': {
            'adverse_selection_elasticity': params.adverse_selection_elasticity,
            'demand_elasticity_high_risk': params.demand_elasticity_high_risk,
            'baseline_loading': params.baseline_loading,
        }
    }
    
    output_file = output_dir / f'module_c_{args.policy}.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
