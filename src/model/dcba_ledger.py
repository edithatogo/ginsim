"""
DCBA (Distributional Cost-Benefit Analysis) Ledger.

Aggregates welfare impacts across stakeholders with time dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import jax.numpy as jnp
from jax import jit

if TYPE_CHECKING:
    from jaxtyping import Array, Float


def _to_float_scalar(value: Array | float) -> Float[Array, ""]:
    """Normalize scalar-like inputs to float JAX arrays."""
    return jnp.asarray(value, dtype=jnp.float32)


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
        time_horizon: Time horizon in years
    """

    net_welfare: Array
    consumer_surplus: Array
    producer_surplus: Array
    health_benefits: Array
    fiscal_impact: Array
    distributional_weight: Array
    time_horizon: int = 20


@jit
def compute_consumer_surplus(
    testing_uptake: Array | float,
    insurance_premium: Array | float,
    baseline_premium: Array | float,
    value_of_testing: float = 100.0,
) -> Float[Array, ""]:
    """Compute consumer surplus change."""
    testing_uptake = _to_float_scalar(testing_uptake)
    insurance_premium = _to_float_scalar(insurance_premium)
    baseline_premium = _to_float_scalar(baseline_premium)
    premium_change = insurance_premium - baseline_premium
    return testing_uptake * value_of_testing - premium_change


@jit
def compute_producer_surplus(
    insurer_profits: Array | float,
    baseline_profits: Array | float,
) -> Float[Array, ""]:
    """Compute producer surplus change."""
    insurer_profits = _to_float_scalar(insurer_profits)
    baseline_profits = _to_float_scalar(baseline_profits)
    return insurer_profits - baseline_profits


@jit
def compute_health_benefits(
    testing_uptake: Array | float,
    baseline_uptake: Array | float,
    qaly_per_test: float = 0.01,
    value_per_qaly: float = 50000.0,
    time_horizon: int = 20,
    discount_rate: float = 0.03,
) -> Float[Array, ""]:
    """
    Compute health benefits with time discounting.

    In the short term (e.g. Year 3), health benefits are lower as
    screening/prevention takes time to manifest as QALY gains.
    """
    testing_uptake = _to_float_scalar(testing_uptake)
    baseline_uptake = _to_float_scalar(baseline_uptake)
    uptake_change = testing_uptake - baseline_uptake

    # Time-dependent manifestation factor (Scientific Power logic)
    # Year 3: 20% of lifetime benefits manifested
    # Year 20: 100% of lifetime benefits manifested
    manifestation_factor = jnp.minimum(time_horizon / 20.0, 1.0)

    qaly_gain = uptake_change * qaly_per_test * manifestation_factor
    health_benefit = qaly_gain * value_per_qaly

    # Discount back to present
    discount_factor = (1 + discount_rate) ** (-time_horizon / 2)  # Mid-point discount

    return health_benefit * discount_factor


@jit
def compute_fiscal_impact(
    testing_uptake: Array | float,
    baseline_uptake: Array | float,
    cost_per_test: float = 500.0,
    health_savings_per_test: float = 200.0,
    setup_cost: float = 1e6,
    time_horizon: int = 20,
) -> Float[Array, ""]:
    """
    Compute fiscal impact with setup costs.

    Short-term (Year 3) is dominated by setup costs.
    Long-term (Year 20) is dominated by cumulative savings.
    """
    testing_uptake = _to_float_scalar(testing_uptake)
    baseline_uptake = _to_float_scalar(baseline_uptake)
    uptake_change = testing_uptake - baseline_uptake

    # Recurring costs/savings
    annual_testing_cost = uptake_change * cost_per_test
    annual_health_savings = uptake_change * health_savings_per_test * (time_horizon / 20.0)

    total_recurring = (annual_health_savings - annual_testing_cost) * time_horizon

    # Front-loaded setup costs (only in year 1-3)
    effective_setup = jnp.where(time_horizon >= 1, setup_cost, 0.0)

    return total_recurring - effective_setup


def compute_dcba(
    testing_uptake: Array | float,
    baseline_uptake: Array | float,
    insurance_premium: Array | float,
    baseline_premium: Array | float,
    insurer_profits: Array | float,
    baseline_profits: Array | float,
    distributional_weight: float = 1.0,
    time_horizon: int = 20,
) -> DCBAResult:
    """Compute full DCBA ledger for a specific time horizon."""
    testing_uptake = _to_float_scalar(testing_uptake)
    baseline_uptake = _to_float_scalar(baseline_uptake)
    insurance_premium = _to_float_scalar(insurance_premium)
    baseline_premium = _to_float_scalar(baseline_premium)
    insurer_profits = _to_float_scalar(insurer_profits)
    baseline_profits = _to_float_scalar(baseline_profits)

    consumer_surplus = compute_consumer_surplus(testing_uptake, insurance_premium, baseline_premium)
    producer_surplus = compute_producer_surplus(insurer_profits, baseline_profits)
    health_benefits = compute_health_benefits(
        testing_uptake, baseline_uptake, time_horizon=time_horizon
    )
    fiscal_impact = compute_fiscal_impact(
        testing_uptake, baseline_uptake, time_horizon=time_horizon
    )

    net_welfare = (
        (consumer_surplus * time_horizon) + producer_surplus + health_benefits + fiscal_impact
    )
    weighted_welfare = net_welfare * distributional_weight

    return DCBAResult(
        net_welfare=weighted_welfare,
        consumer_surplus=consumer_surplus * time_horizon,
        producer_surplus=producer_surplus,
        health_benefits=health_benefits,
        fiscal_impact=fiscal_impact,
        distributional_weight=_to_float_scalar(distributional_weight),
        time_horizon=time_horizon,
    )


def compute_dual_horizon_dcba(
    **kwargs: Any,
) -> dict[str, DCBAResult]:
    """Compute DCBA for both short-term (Year 3) and long-term (Year 20)."""
    res_3 = compute_dcba(**kwargs, time_horizon=3)
    res_20 = compute_dcba(**kwargs, time_horizon=20)

    return {
        "short_term": res_3,
        "long_term": res_20,
    }


def format_dcba_result(result: DCBAResult) -> str:
    """Format DCBA result for display."""
    lines = [
        "=" * 60,
        f"DCBA Ledger (Horizon: {result.time_horizon} years)",
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
