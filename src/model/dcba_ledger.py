"""
DCBA (Distributional Cost-Benefit Analysis) Ledger.

Aggregates welfare impacts across stakeholders.
"""

from __future__ import annotations

from typing import Dict, Optional
from dataclasses import dataclass
import jax.numpy as jnp
from jax import jit
from jaxtyping import Array, Float


@dataclass
class DCBAResult:
    """
    DCBA ledger results.
    
    Attributes:
        net_welfare: Net welfare impact
        consumer_surplus: Consumer surplus change
        producer_surplus: Producer (insurer) surplus change
        health_benefits: Health benefits (QALYs)
        fiscal_impact: Fiscal impact (government)
        distributional_weight: Distributional weight applied
    """
    net_welfare: Float[Array, ""]
    consumer_surplus: Float[Array, ""]
    producer_surplus: Float[Array, ""]
    health_benefits: Float[Array, ""]
    fiscal_impact: Float[Array, ""]
    distributional_weight: Float[Array, ""]


@jit
def compute_consumer_surplus(
    testing_uptake: Float[Array, ""],
    insurance_premium: Float[Array, ""],
    baseline_premium: Float[Array, ""],
    value_of_testing: float = 100.0,
) -> Float[Array, ""]:
    """
    Compute consumer surplus change.
    
    Consumer surplus = value_of_testing * uptake - premium_change
    
    Args:
        testing_uptake: Testing uptake rate
        insurance_premium: Premium under policy
        baseline_premium: Premium under baseline
        value_of_testing: Per-person value of testing
        
    Returns:
        Consumer surplus change
    """
    premium_change = insurance_premium - baseline_premium
    surplus = testing_uptake * value_of_testing - premium_change
    
    return surplus


@jit
def compute_producer_surplus(
    insurer_profits: Float[Array, ""],
    baseline_profits: Float[Array, ""],
) -> Float[Array, ""]:
    """
    Compute producer (insurer) surplus change.
    
    Args:
        insurer_profits: Insurer profits under policy
        baseline_profits: Insurer profits under baseline
        
    Returns:
        Producer surplus change
    """
    return insurer_profits - baseline_profits


@jit
def compute_health_benefits(
    testing_uptake: Float[Array, ""],
    baseline_uptake: Float[Array, ""],
    qaly_per_test: float = 0.01,
    value_per_qaly: float = 50000.0,
) -> Float[Array, ""]:
    """
    Compute health benefits from testing.
    
    Health benefits = (uptake - baseline) * qaly_per_test * value_per_qaly
    
    Args:
        testing_uptake: Testing uptake under policy
        baseline_uptake: Testing uptake under baseline
        qaly_per_test: QALYs gained per test
        value_per_qaly: Monetary value per QALY
        
    Returns:
        Health benefits (monetized)
    """
    uptake_change = testing_uptake - baseline_uptake
    qaly_gain = uptake_change * qaly_per_test
    health_benefit = qaly_gain * value_per_qaly
    
    return health_benefit


@jit
def compute_fiscal_impact(
    testing_uptake: Float[Array, ""],
    baseline_uptake: Float[Array, ""],
    cost_per_test: float = 500.0,
    health_savings_per_test: float = 200.0,
) -> Float[Array, ""]:
    """
    Compute fiscal impact (government).
    
    Fiscal impact = cost_of_testing - health_savings
    
    Args:
        testing_uptake: Testing uptake under policy
        baseline_uptake: Testing uptake under baseline
        cost_per_test: Government cost per test
        health_savings_per_test: Health system savings per test
        
    Returns:
        Fiscal impact (negative = cost, positive = savings)
    """
    uptake_change = testing_uptake - baseline_uptake
    testing_cost = uptake_change * cost_per_test
    health_savings = uptake_change * health_savings_per_test
    
    fiscal_impact = health_savings - testing_cost
    
    return fiscal_impact


@jit
def apply_distributional_weight(
    welfare_impact: Float[Array, ""],
    weight: float = 1.0,
) -> Float[Array, ""]:
    """
    Apply distributional weight to welfare impact.
    
    Args:
        welfare_impact: Unweighted welfare impact
        weight: Distributional weight (>1 favors disadvantaged)
        
    Returns:
        Weighted welfare impact
    """
    return welfare_impact * weight


@jit
def compute_dcba(
    testing_uptake: Float[Array, ""],
    baseline_uptake: Float[Array, ""],
    insurance_premium: Float[Array, ""],
    baseline_premium: Float[Array, ""],
    insurer_profits: Float[Array, ""],
    baseline_profits: Float[Array, ""],
    distributional_weight: float = 1.0,
) -> DCBAResult:
    """
    Compute full DCBA ledger.
    
    Args:
        testing_uptake: Testing uptake under policy
        baseline_uptake: Testing uptake under baseline
        insurance_premium: Premium under policy
        baseline_premium: Premium under baseline
        insurer_profits: Insurer profits under policy
        baseline_profits: Insurer profits under baseline
        distributional_weight: Distributional weight
        
    Returns:
        DCBAResult object
    """
    # Compute components
    consumer_surplus = compute_consumer_surplus(
        testing_uptake,
        insurance_premium,
        baseline_premium,
    )
    
    producer_surplus = compute_producer_surplus(
        insurer_profits,
        baseline_profits,
    )
    
    health_benefits = compute_health_benefits(
        testing_uptake,
        baseline_uptake,
    )
    
    fiscal_impact = compute_fiscal_impact(
        testing_uptake,
        baseline_uptake,
    )
    
    # Net welfare
    net_welfare = consumer_surplus + producer_surplus + health_benefits + fiscal_impact
    
    # Apply distributional weight
    weighted_welfare = apply_distributional_weight(net_welfare, distributional_weight)
    
    return DCBAResult(
        net_welfare=weighted_welfare,
        consumer_surplus=consumer_surplus,
        producer_surplus=producer_surplus,
        health_benefits=health_benefits,
        fiscal_impact=fiscal_impact,
        distributional_weight=jnp.array(distributional_weight),
    )


def format_dcba_result(result: DCBAResult) -> str:
    """
    Format DCBA result for display.
    
    Args:
        result: DCBAResult object
        
    Returns:
        Formatted string
    """
    lines = [
        "=" * 60,
        "DCBA (Distributional Cost-Benefit Analysis) Ledger",
        "=" * 60,
        f"Consumer Surplus:    ${float(result.consumer_surplus):>12,.2f}",
        f"Producer Surplus:    ${float(result.producer_surplus):>12,.2f}",
        f"Health Benefits:     ${float(result.health_benefits):>12,.2f}",
        f"Fiscal Impact:       ${float(result.fiscal_impact):>12,.2f}",
        "-" * 60,
        f"Net Welfare:         ${float(result.net_welfare):>12,.2f}",
        f"Distributional Weight: {float(result.distributional_weight):.2f}x",
        "=" * 60,
    ]
    
    return "\n".join(lines)
