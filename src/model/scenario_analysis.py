#!/usr/bin/env python3
"""
Scenario analysis module.

Compare policy outcomes across predefined scenarios and custom configurations.
"""

from __future__ import annotations

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import yaml

import jax.numpy as jnp
from jaxtyping import Array, Float


@dataclass
class ScenarioResult:
    """Result from evaluating a single scenario."""
    scenario_name: str
    jurisdiction: str
    testing_uptake: float
    welfare_impact: float
    qalys_gained: float
    compliance_rate: float
    all_metrics: Dict[str, Any]


@dataclass
class ScenarioComparison:
    """Comparison of multiple scenarios."""
    baseline_scenario: str
    scenarios: List[ScenarioResult]
    delta_from_baseline: Dict[str, Dict[str, float]]


def load_scenarios(config_path: Path | str) -> Dict[str, Any]:
    """
    Load scenario definitions from YAML config.
    
    Args:
        config_path: Path to scenarios.yaml
        
    Returns:
        Dictionary of scenario definitions
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Scenario config not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config.get('scenarios', {})


def evaluate_scenario(
    scenario_name: str,
    scenario_config: Dict[str, Any],
    model_func,
) -> ScenarioResult:
    """
    Evaluate a single scenario using the core model.
    
    Args:
        scenario_name: Name of the scenario
        scenario_config: Scenario configuration dictionary
        model_func: Model evaluation function
        
    Returns:
        ScenarioResult with outcomes
    """
    from src.model.parameters import ModelParameters, PolicyConfig
    
    # Extract parameters
    params_dict = scenario_config.get('parameters', {})
    
    # Create model parameters
    try:
        model_params = ModelParameters(**params_dict)
    except Exception as e:
        # Handle missing parameters with defaults
        model_params = ModelParameters()
        for key, value in params_dict.items():
            if hasattr(model_params, key):
                setattr(model_params, key, value)
    
    # Get policy config (simplified - use default policy)
    from src.model.module_a_behavior import get_standard_policies
    policies = get_standard_policies()
    policy = policies.get('status_quo', list(policies.values())[0])
    
    # Evaluate
    result = model_func(model_params, policy)
    
    # Extract metrics
    testing_uptake = float(result.testing_uptake) if hasattr(result, 'testing_uptake') else 0.0
    welfare_impact = float(result.welfare_impact) if hasattr(result, 'welfare_impact') else 0.0
    qalys_gained = float(result.qalys_gained) if hasattr(result, 'qalys_gained') else 0.0
    compliance_rate = float(result.compliance_rate) if hasattr(result, 'compliance_rate') else 0.0
    
    return ScenarioResult(
        scenario_name=scenario_name,
        jurisdiction=scenario_config.get('jurisdiction', 'Unknown'),
        testing_uptake=testing_uptake,
        welfare_impact=welfare_impact,
        qalys_gained=qalys_gained,
        compliance_rate=compliance_rate,
        all_metrics={
            'testing_uptake': testing_uptake,
            'welfare_impact': welfare_impact,
            'qalys_gained': qalys_gained,
            'compliance_rate': compliance_rate,
        }
    )


def compare_scenarios(
    scenarios: Dict[str, Dict[str, Any]],
    model_func,
    baseline_name: str = 'au_status_quo',
) -> ScenarioComparison:
    """
    Compare multiple scenarios against a baseline.
    
    Args:
        scenarios: Dictionary of scenario configurations
        model_func: Model evaluation function
        baseline_name: Name of baseline scenario for comparison
        
    Returns:
        ScenarioComparison with delta calculations
    """
    # Evaluate all scenarios
    results = []
    for name, config in scenarios.items():
        result = evaluate_scenario(name, config, model_func)
        results.append(result)
    
    # Find baseline
    baseline = None
    for r in results:
        if r.scenario_name == baseline_name:
            baseline = r
            break
    
    # Calculate deltas
    deltas = {}
    if baseline:
        for r in results:
            if r.scenario_name != baseline_name:
                deltas[r.scenario_name] = {
                    'testing_uptake_delta': r.testing_uptake - baseline.testing_uptake,
                    'welfare_delta': r.welfare_impact - baseline.welfare_impact,
                    'qalys_delta': r.qalys_gained - baseline.qalys_gained,
                    'compliance_delta': r.compliance_rate - baseline.compliance_rate,
                }
    
    return ScenarioComparison(
        baseline_scenario=baseline_name,
        scenarios=results,
        delta_from_baseline=deltas,
    )


def format_comparison_table(comparison: ScenarioComparison) -> str:
    """
    Format scenario comparison as markdown table.
    
    Args:
        comparison: ScenarioComparison object
        
    Returns:
        Markdown table string
    """
    lines = []
    
    # Header
    lines.append("| Scenario | Jurisdiction | Testing Uptake | Δ vs Baseline | Welfare Impact | Compliance |")
    lines.append("|----------|--------------|----------------|---------------|----------------|------------|")
    
    # Rows
    for result in comparison.scenarios:
        delta_str = ""
        if result.scenario_name in comparison.delta_from_baseline:
            delta = comparison.delta_from_baseline[result.scenario_name]['testing_uptake_delta']
            delta_str = f"{delta:+.1%}"
        
        lines.append(
            f"| {result.scenario_name} | {result.jurisdiction} | "
            f"{result.testing_uptake:.1%} | {delta_str} | "
            f"${result.welfare_impact:,.0f} | {result.compliance_rate:.1%} |"
        )
    
    return "\n".join(lines)


def run_scenario_analysis(
    config_path: Optional[Path | str] = None,
    model_func=None,
    output_dir: Optional[Path] = None,
) -> ScenarioComparison:
    """
    Run complete scenario analysis.
    
    Args:
        config_path: Path to scenarios.yaml (default: configs/scenarios.yaml)
        model_func: Model evaluation function
        output_dir: Optional output directory for results
        
    Returns:
        ScenarioComparison object
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / "configs" / "scenarios.yaml"
    
    # Load scenarios
    print(f"Loading scenarios from {config_path}...")
    scenarios = load_scenarios(config_path)
    print(f"  Loaded {len(scenarios)} scenarios")
    
    # Run comparison
    print("\nRunning scenario comparison...")
    comparison = compare_scenarios(scenarios, model_func)
    
    # Print results
    print("\n" + "=" * 80)
    print("SCENARIO COMPARISON RESULTS")
    print("=" * 80)
    print(f"\nBaseline: {comparison.baseline_scenario}\n")
    print(format_comparison_table(comparison))
    
    # Save results
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "scenario_comparison.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Scenario Comparison Results\n\n")
            f.write(f"**Baseline:** {comparison.baseline_scenario}\n\n")
            f.write(format_comparison_table(comparison))
            f.write("\n\n## Detailed Results\n\n")
            
            for result in comparison.scenarios:
                f.write(f"\n### {result.scenario_name}\n\n")
                f.write(f"- **Jurisdiction:** {result.jurisdiction}\n")
                f.write(f"- **Testing Uptake:** {result.testing_uptake:.1%}\n")
                f.write(f"- **Welfare Impact:** ${result.welfare_impact:,.0f}\n")
                f.write(f"- **QALYs Gained:** {result.qalys_gained:.2f}\n")
                f.write(f"- **Compliance Rate:** {result.compliance_rate:.1%}\n")
        
        print(f"\nResults saved to {output_path}")
    
    return comparison
