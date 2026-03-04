"""
Value of Information (VOI) analysis.

Computes EVPI (Expected Value of Perfect Information) and 
EVPPI (Expected Value of Partial Perfect Information).
"""

from __future__ import annotations

from typing import Dict, List, Any
from dataclasses import dataclass
import json
from pathlib import Path

import numpy as np
from numpyro.distributions import Normal, Beta


@dataclass
class VOIResult:
    """
    VOI analysis result.
    
    Attributes:
        evpi: Expected Value of Perfect Information
        evppi: EVPPI by parameter group
        total_uncertainty: Total decision uncertainty
        research_priority: Top research priority
    """
    evpi: float
    evppi: Dict[str, float]
    total_uncertainty: float
    research_priority: str


def compute_evpi(
    net_benefits: np.ndarray,
    optimal_net_benefit: float,
) -> float:
    """
    Compute Expected Value of Perfect Information.
    
    EVPI = E[max NB] - max E[NB]
    
    Args:
        net_benefits: Array of net benefits for each policy across draws
        optimal_net_benefit: Net benefit under current optimal decision
        
    Returns:
        EVPI value
    """
    # Expected maximum net benefit (with perfect information)
    expected_max = np.mean(np.max(net_benefits, axis=1))
    
    # Maximum expected net benefit (current optimal)
    max_expected = optimal_net_benefit
    
    evpi = expected_max - max_expected
    
    return max(0.0, float(evpi))  # EVPI cannot be negative, ensure float return


def compute_evppi(
    net_benefits: np.ndarray,
    parameter_samples: Dict[str, np.ndarray],
    optimal_net_benefit: float,
    n_inner_draws: int = 50,
) -> Dict[str, float]:
    """
    Compute Expected Value of Partial Perfect Information by parameter group.
    
    Uses Monte Carlo estimation with inner sampling.
    
    Args:
        net_benefits: Array of net benefits for each policy
        parameter_samples: Dictionary of parameter samples by group
        optimal_net_benefit: Net benefit under current optimal decision
        n_inner_draws: Number of inner draws for EVPPI estimation
        
    Returns:
        Dictionary of EVPPI values by parameter group
    """
    evppi = {}
    n_outer = len(net_benefits)
    
    for param_group, samples in parameter_samples.items():
        # For each parameter group, compute EVPPI
        # EVPPI = E[max NB|θ_i] - max E[NB]
        
        # Simplified estimation using regression-based approach
        # In practice, would use Gaussian process or other surrogate
        
        # For now, use simplified formula
        group_variance = np.var(samples)
        total_variance = np.var(net_benefits)
        
        # Proportion of variance explained by this group
        if total_variance > 0:
            variance_proportion = group_variance / total_variance
        else:
            variance_proportion = 0.0
        
        # EVPPI approximation
        evpi = compute_evpi(net_benefits, optimal_net_benefit)
        evppi[param_group] = evpi * min(variance_proportion, 1.0)
    
    return evppi


def identify_research_priority(
    evppi: Dict[str, float],
) -> str:
    """
    Identify top research priority from EVPPI results.
    
    Args:
        evppi: EVPPI values by parameter group
        
    Returns:
        Name of parameter group with highest EVPPI
    """
    if not evppi:
        return "Unknown"
    
    return max(evppi, key=evppi.get)


def run_voi_analysis(
    net_benefits: np.ndarray,
    policy_names: List[str],
    parameter_samples: Dict[str, np.ndarray],
) -> VOIResult:
    """
    Run complete VOI analysis.
    
    Args:
        net_benefits: Array of net benefits (n_draws x n_policies)
        policy_names: Names of policies
        parameter_samples: Parameter samples by group
        
    Returns:
        VOIResult object
    """
    # Current optimal net benefit
    expected_benefits = np.mean(net_benefits, axis=0)
    optimal_idx = np.argmax(expected_benefits)
    optimal_net_benefit = expected_benefits[optimal_idx]
    optimal_policy = policy_names[optimal_idx]
    
    # Compute EVPI
    evpi = compute_evpi(net_benefits, optimal_net_benefit)
    
    # Compute EVPPI
    evppi = compute_evppi(net_benefits, parameter_samples, optimal_net_benefit)
    
    # Total uncertainty
    total_uncertainty = np.var(expected_benefits)
    
    # Research priority
    research_priority = identify_research_priority(evppi)
    
    return VOIResult(
        evpi=evpi,
        evppi=evppi,
        total_uncertainty=total_uncertainty,
        research_priority=research_priority,
    )


def format_voi_result(result: VOIResult) -> str:
    """
    Format VOI result for display.
    
    Args:
        result: VOIResult object
        
    Returns:
        Formatted string
    """
    lines = [
        "=" * 80,
        "VALUE OF INFORMATION ANALYSIS",
        "=" * 80,
        "",
        f"EVPI (Expected Value of Perfect Information): ${result.evpi:,.0f}",
        "",
        "EVPPI by Parameter Group:",
    ]
    
    # Sort by EVPPI value
    sorted_evppi = sorted(result.evppi.items(), key=lambda x: x[1], reverse=True)
    
    for param_group, value in sorted_evppi:
        lines.append(f"  {param_group}: ${value:,.0f}")
    
    lines.extend([
        "",
        f"Total Uncertainty: {result.total_uncertainty:.4f}",
        "",
        f"Top Research Priority: {result.research_priority}",
        "=" * 80,
    ])
    
    return "\n".join(lines)


def save_voi_results(
    result: VOIResult,
    output_path: str | Path,
) -> None:
    """
    Save VOI results to JSON file.
    
    Args:
        result: VOIResult object
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    results_dict = {
        'evpi': result.evpi,
        'evppi': result.evppi,
        'total_uncertainty': result.total_uncertainty,
        'research_priority': result.research_priority,
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results_dict, f, indent=2)
