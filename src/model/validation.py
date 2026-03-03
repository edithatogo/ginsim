"""
Posterior predictive check protocol.

Protocol for validating model outputs against empirical targets.
"""

from __future__ import annotations

from typing import Dict, List, Any
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class PPCCheck:
    """
    Posterior predictive check result.
    
    Attributes:
        parameter: Parameter name
        target_value: Empirical target value
        target_ci: Empirical 95% CI
        simulated_mean: Mean of simulated values
        simulated_ci: Simulated 95% CI
        coverage: Whether target is within simulated CI
        bias: Relative bias
    """
    parameter: str
    target_value: float
    target_ci: tuple[float, float]
    simulated_mean: float
    simulated_ci: tuple[float, float]
    coverage: bool
    bias: float


def compute_coverage(
    simulated_values: List[float],
    target_value: float,
) -> bool:
    """
    Compute whether target is within simulated credible interval.
    
    Args:
        simulated_values: Simulated values from model
        target_value: Empirical target value
        
    Returns:
        True if target is within 95% CI of simulated values
    """
    import numpy as np
    
    simulated_array = np.array(simulated_values)
    ci_lower = np.percentile(simulated_array, 2.5)
    ci_upper = np.percentile(simulated_array, 97.5)
    
    return ci_lower <= target_value <= ci_upper


def compute_bias(
    simulated_mean: float,
    target_value: float,
) -> float:
    """
    Compute relative bias.
    
    Args:
        simulated_mean: Mean of simulated values
        target_value: Empirical target value
        
    Returns:
        Relative bias (simulated - target) / target
    """
    if target_value == 0:
        return float('inf') if simulated_mean != 0 else 0.0
    
    return (simulated_mean - target_value) / target_value


def run_ppc(
    simulated_data: Dict[str, List[float]],
    empirical_targets: Dict[str, Dict[str, Any]],
) -> List[PPCCheck]:
    """
    Run posterior predictive checks.
    
    Args:
        simulated_data: Dictionary of parameter names to simulated values
        empirical_targets: Dictionary of parameter names to target info
                          (value, ci_lower, ci_upper)
        
    Returns:
        List of PPCCheck objects
    """
    checks = []
    
    for parameter, targets in empirical_targets.items():
        if parameter not in simulated_data:
            continue
        
        simulated = simulated_data[parameter]
        simulated_mean = sum(simulated) / len(simulated)
        simulated_ci = (
            min(simulated),  # Simplified - use min/max
            max(simulated),
        )
        
        coverage = compute_coverage(simulated, targets['value'])
        bias = compute_bias(simulated_mean, targets['value'])
        
        check = PPCCheck(
            parameter=parameter,
            target_value=targets['value'],
            target_ci=(targets['ci_lower'], targets['ci_upper']),
            simulated_mean=simulated_mean,
            simulated_ci=simulated_ci,
            coverage=coverage,
            bias=bias,
        )
        
        checks.append(check)
    
    return checks


def summarize_ppc(checks: List[PPCCheck]) -> Dict[str, Any]:
    """
    Summarize PPC results.
    
    Args:
        checks: List of PPCCheck objects
        
    Returns:
        Summary dictionary
    """
    total = len(checks)
    passed = sum(1 for c in checks if c.coverage)
    
    return {
        'total_checks': total,
        'passed': passed,
        'failed': total - passed,
        'pass_rate': passed / total if total > 0 else 0.0,
        'mean_bias': sum(abs(c.bias) for c in checks) / total if total > 0 else 0.0,
    }


def format_ppc_report(checks: List[PPCCheck]) -> str:
    """
    Format PPC results as report.
    
    Args:
        checks: List of PPCCheck objects
        
    Returns:
        Formatted report string
    """
    lines = [
        "=" * 80,
        "POSTERIOR PREDICTIVE CHECK REPORT",
        "=" * 80,
        "",
    ]
    
    for check in checks:
        status = "✅ PASS" if check.coverage else "❌ FAIL"
        lines.append(f"Parameter: {check.parameter}")
        lines.append(f"  Status: {status}")
        lines.append(f"  Target: {check.target_value:.3f} (95% CI: {check.target_ci[0]:.3f}-{check.target_ci[1]:.3f})")
        lines.append(f"  Simulated: {check.simulated_mean:.3f} (95% CI: {check.simulated_ci[0]:.3f}-{check.simulated_ci[1]:.3f})")
        lines.append(f"  Bias: {check.bias:+.1%}")
        lines.append("")
    
    # Summary
    summary = summarize_ppc(checks)
    lines.append("=" * 80)
    lines.append("SUMMARY")
    lines.append("=" * 80)
    lines.append(f"Total Checks: {summary['total_checks']}")
    lines.append(f"Passed: {summary['passed']} ({summary['pass_rate']:.1%})")
    lines.append(f"Failed: {summary['failed']}")
    lines.append(f"Mean Absolute Bias: {summary['mean_bias']:.1%}")
    lines.append("=" * 80)
    
    return "\n".join(lines)


def save_ppc_results(
    checks: List[PPCCheck],
    output_path: str | Path,
) -> None:
    """
    Save PPC results to JSON file.
    
    Args:
        checks: List of PPCCheck objects
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    results = []
    for check in checks:
        results.append({
            'parameter': check.parameter,
            'target_value': check.target_value,
            'target_ci': check.target_ci,
            'simulated_mean': check.simulated_mean,
            'simulated_ci': check.simulated_ci,
            'coverage': check.coverage,
            'bias': check.bias,
        })
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
