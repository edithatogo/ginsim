"""
DCBA (Distributional Cost-Benefit Analysis) Ledger.

Aggregates welfare impacts across stakeholders with consistent temporal discounting.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
from jax import jit
from jaxtyping import Array, Float


def _to_float_scalar(value: Array | float) -> Float[Array, ""]:
    """Normalize scalar-like inputs to float JAX arrays."""
    return jnp.asarray(value, dtype=jnp.float32)


@dataclass(frozen=True)
class DCBAResult:
    """
    DCBA ledger results. Fields are Any to allow JAX tracers.
    """

    net_welfare: Any
    consumer_surplus: Any
    producer_surplus: Any
    health_benefits: Any
    fiscal_impact: Any
    research_externalities: Any
    distributional_weight: Any
    time_horizon: int = 20


# Register PyTree for JAX JIT compatibility
jax.tree_util.register_pytree_node(
    DCBAResult,
    lambda x: (
        (
            x.net_welfare,
            x.consumer_surplus,
            x.producer_surplus,
            x.health_benefits,
            x.fiscal_impact,
            x.research_externalities,
            x.distributional_weight,
        ),
        (x.time_horizon,),
    ),
    lambda aux, children: DCBAResult(*children, time_horizon=aux[0]),
)


@jit(static_argnames=["time_horizon", "discount_rate"])
def compute_discount_factor(
    time_horizon: float | int | Array,
    discount_rate: float | int | Array = 0.03,
) -> Float[Array, ""]:
    """Compute cumulative discount factor."""
    th = jnp.asarray(float(time_horizon))
    dr = jnp.asarray(float(discount_rate))
    return (1.0 - (1.0 + dr) ** (-th)) / (dr + 1e-10)


@jit(static_argnames=["time_horizon", "discount_rate"])
def compute_consumer_surplus(
    testing_uptake: Array | float,
    insurance_premium: Array | float,
    baseline_premium: Array | float,
    value_of_testing: float = 100.0,
    time_horizon: float | int | Array = 20.0,
    discount_rate: float | int | Array = 0.03,
) -> Float[Array, ""]:
    """Compute discounted consumer surplus change."""
    testing_uptake = _to_float_scalar(testing_uptake)
    insurance_premium = _to_float_scalar(insurance_premium)
    baseline_premium = _to_float_scalar(baseline_premium)

    annual_surplus = testing_uptake * value_of_testing - (insurance_premium - baseline_premium)
    cum_discount = compute_discount_factor(time_horizon, discount_rate)

    return annual_surplus * cum_discount


@jit(static_argnames=["time_horizon", "discount_rate"])
def compute_producer_surplus(
    insurer_profits: Array | float,
    baseline_profits: Array | float,
    time_horizon: float | int | Array = 20.0,
    discount_rate: float | int | Array = 0.03,
) -> Float[Array, ""]:
    """Compute discounted producer surplus."""
    annual_surplus = _to_float_scalar(insurer_profits) - _to_float_scalar(baseline_profits)
    cum_discount = compute_discount_factor(time_horizon, discount_rate)
    return annual_surplus * cum_discount


@jit(static_argnames=["time_horizon", "discount_rate"])
def compute_health_benefits(
    testing_uptake: Array | float,
    baseline_uptake: Array | float,
    qaly_per_test: float = 0.01,
    value_per_qaly: float = 50000.0,
    time_horizon: float | int | Array = 20.0,
    discount_rate: float | int | Array = 0.03,
) -> Float[Array, ""]:
    """Compute discounted health benefits."""
    uptake_change = _to_float_scalar(testing_uptake) - _to_float_scalar(baseline_uptake)
    annual_qaly_gain = uptake_change * qaly_per_test
    avg_manifestation = jnp.minimum(jnp.asarray(float(time_horizon)) / 40.0, 0.5)
    annual_benefit = annual_qaly_gain * value_per_qaly * avg_manifestation
    cum_discount = compute_discount_factor(time_horizon, discount_rate)
    return annual_benefit * cum_discount


@jit(static_argnames=["time_horizon", "discount_rate"])
def compute_fiscal_impact(
    testing_uptake: Array | float,
    baseline_uptake: Array | float,
    cost_per_test: float = 500.0,
    health_savings_per_test: float = 200.0,
    setup_cost: float = 1e6,
    time_horizon: float | int | Array = 20.0,
    discount_rate: float | int | Array = 0.03,
) -> Float[Array, ""]:
    """Compute discounted fiscal impact."""
    uptake_change = _to_float_scalar(testing_uptake) - _to_float_scalar(baseline_uptake)

    annual_testing_cost = uptake_change * cost_per_test
    annual_health_savings = (
        uptake_change
        * health_savings_per_test
        * jnp.minimum(jnp.asarray(float(time_horizon)) / 20.0, 1.0)
    )

    net_annual_impact = annual_health_savings - annual_testing_cost
    cum_discount = compute_discount_factor(time_horizon, discount_rate)
    return net_annual_impact * cum_discount - setup_cost


@jit(static_argnames=["time_horizon", "discount_rate"])
def compute_dcba(
    testing_uptake: Array | float,
    baseline_uptake: Array | float,
    insurance_premium: Array | float,
    baseline_premium: Array | float,
    insurer_profits: Array | float,
    baseline_profits: Array | float,
    research_value_loss: Array | float = 0.0,
    distributional_weight: float = 1.0,
    time_horizon: int = 20,
    discount_rate: float = 0.03,
    ppp_conversion_factor: float = 1.0,
) -> DCBAResult:
    """
    Compute full DCBA ledger with PPP normalization.
    """
    cs = compute_consumer_surplus(
        testing_uptake,
        insurance_premium,
        baseline_premium,
        time_horizon=time_horizon,
        discount_rate=discount_rate,
    )
    ps = compute_producer_surplus(
        insurer_profits, baseline_profits, time_horizon=time_horizon, discount_rate=discount_rate
    )
    hb = compute_health_benefits(
        testing_uptake, baseline_uptake, time_horizon=time_horizon, discount_rate=discount_rate
    )
    fi = compute_fiscal_impact(
        testing_uptake, baseline_uptake, time_horizon=time_horizon, discount_rate=discount_rate
    )
    re = _to_float_scalar(research_value_loss)
    
    # 1. Compute net local welfare
    net_welfare_local = cs + ps + hb + fi - re
    weighted_welfare_local = net_welfare_local * distributional_weight
    
    # 2. Apply PPP normalization to all components
    ppp = jnp.asarray(float(ppp_conversion_factor))
    
    return DCBAResult(
        net_welfare=weighted_welfare_local * ppp,
        consumer_surplus=cs * ppp,
        producer_surplus=ps * ppp,
        health_benefits=hb * ppp,
        fiscal_impact=fi * ppp,
        research_externalities=re * ppp,
        distributional_weight=_to_float_scalar(distributional_weight),
        time_horizon=time_horizon
    )


def compute_dual_horizon_dcba(**kwargs):
    """Compatibility wrapper."""
    return {
        "short_term": compute_dcba(**kwargs, time_horizon=3),
        "long_term": compute_dcba(**kwargs, time_horizon=20),
    }


def format_dcba_result(result: DCBAResult) -> str:
    """Format DCBA result for display."""
    lines = [
        "=" * 60,
        f"DCBA Ledger (Horizon: {result.time_horizon} years)",
        "=" * 60,
        f"Consumer Surplus:    ${float(result.consumer_surplus):>15,.2f}",
        f"Producer Surplus:    ${float(result.producer_surplus):>15,.2f}",
        f"Health Benefits:     ${float(result.health_benefits):>15,.2f}",
        f"Fiscal Impact:       ${float(result.fiscal_impact):>15,.2f}",
        f"Research Ext:       -${float(result.research_externalities):>15,.2f}",
        "-" * 60,
        f"Net Welfare:         ${float(result.net_welfare):>15,.2f}",
        f"Distributional Weight: {float(result.distributional_weight):.2f}x",
        "=" * 60,
    ]
    return "\n".join(lines)
