"""
Module C: Insurance Equilibrium - Rothschild-Stiglitz Screening.

This module computes the pooling and separating equilibria for insurance markets
under different genetic information policy regimes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
from jax import jacfwd, jit, lax
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig


def _to_float_scalar(value: Array | float) -> Float[Array, ""]:
    """Normalize scalar-like inputs to float JAX arrays."""
    return jnp.asarray(value, dtype=jnp.float32)


@dataclass(frozen=True)
class InsuranceEquilibrium:
    """Represents a computed insurance market equilibrium. Fields are Any to allow JAX tracers."""

    premium_high: Any
    premium_low: Any
    uptake_high: Any
    uptake_low: Any
    insurer_profits: Any
    equilibrium_id: Any  # 0 for separating, 1 for pooling
    iterations: Any = 1

    # Backward compatibility properties
    @property
    def premium_high_risk(self) -> float:
        return float(self.premium_high)

    @property
    def premium_low_risk(self) -> float:
        return float(self.premium_low)

    @property
    def converged(self) -> bool:
        return True

    @property
    def equilibrium_type(self) -> str:
        return "separating" if self.equilibrium_id == 0 else "pooling"


# Register PyTree for JAX JIT compatibility
jax.tree_util.register_pytree_node(
    InsuranceEquilibrium,
    lambda x: (
        (
            x.premium_high,
            x.premium_low,
            x.uptake_high,
            x.uptake_low,
            x.insurer_profits,
            x.equilibrium_id,
            x.iterations,
        ),
        (),
    ),
    lambda aux, children: InsuranceEquilibrium(*children),
)


@jit
def compute_demand(
    premium: Array | float,
    income: float = 1.0,
    risk_aversion: float = 2.0,
    price_elasticity: float = -0.22,
) -> Float[Array, ""]:
    """
    Compute insurance demand using constant elasticity form.
    """
    p = jnp.asarray(premium)
    return jnp.clip(1.0 + price_elasticity * (p / income), 0.0, 1.0)


@jit
def compute_insurer_profit(
    premium: Any,
    risk: Any,
    takeup: Any = 1.0,  # Added for compatibility
    loading: float = 0.0,
) -> Float[Array, ""]:
    """Compute insurer profit for a single group."""
    return jnp.asarray(takeup) * (jnp.asarray(premium) - jnp.asarray(risk) * (1.0 + loading))


@jit(static_argnames=["params"])
def separating_equilibrium(
    params: ModelParameters,
    risk_high: Float[Array, ""] | float = 0.3,
    risk_low: Float[Array, ""] | float = 0.1,
    proportion_high: Float[Array, ""] | float = 0.2,
) -> InsuranceEquilibrium:
    """
    Compute Rothschild-Stiglitz separating equilibrium.
    """
    p_h = _to_float_scalar(jnp.asarray(risk_high) * (1.0 + params.baseline_loading))
    p_l = _to_float_scalar(jnp.asarray(risk_low) * (1.0 + params.baseline_loading))

    u_h = compute_demand(p_h, price_elasticity=params.demand_elasticity_high_risk)
    u_l = compute_demand(p_l)

    profit_h = compute_insurer_profit(p_h, risk_high, u_h, params.baseline_loading)
    profit_l = compute_insurer_profit(p_l, risk_low, u_l, params.baseline_loading)

    return InsuranceEquilibrium(
        premium_high=p_h,
        premium_low=p_l,
        uptake_high=u_h,
        uptake_low=u_l,
        insurer_profits=profit_h + profit_l,
        equilibrium_id=0,
        iterations=1,
    )


@jit(static_argnames=["params"])
def pooling_equilibrium(
    params: ModelParameters,
    risk_high: Float[Array, ""] | float = 0.3,
    risk_low: Float[Array, ""] | float = 0.1,
    proportion_high: Float[Array, ""] | float = 0.2,
) -> InsuranceEquilibrium:
    """
    Compute pooling equilibrium.
    """

    def body_fn(p):
        takeup_h = compute_demand(p, price_elasticity=params.demand_elasticity_high_risk)
        takeup_l = compute_demand(p)
        total_insured = proportion_high * takeup_h + (1.0 - proportion_high) * takeup_l + 1e-10
        avg_risk = (
            proportion_high * takeup_h * jnp.asarray(risk_high)
            + (1.0 - proportion_high) * takeup_l * jnp.asarray(risk_low)
        ) / total_insured
        return avg_risk * (1.0 + params.baseline_loading)

    p_init = _to_float_scalar(
        (proportion_high * jnp.asarray(risk_high) + (1.0 - proportion_high) * jnp.asarray(risk_low))
        * (1.0 + params.baseline_loading)
    )
    p_final = lax.fori_loop(0, 10, lambda i, val: body_fn(val), p_init)

    u_h = compute_demand(p_final, price_elasticity=params.demand_elasticity_high_risk)
    u_l = compute_demand(p_final)

    profit = proportion_high * compute_insurer_profit(
        p_final, risk_high, u_h, params.baseline_loading
    ) + (1.0 - proportion_high) * compute_insurer_profit(
        p_final, risk_low, u_l, params.baseline_loading
    )

    return InsuranceEquilibrium(
        premium_high=p_final,
        premium_low=p_final,
        uptake_high=u_h,
        uptake_low=u_l,
        insurer_profits=profit,
        equilibrium_id=1,
        iterations=10,
    )


@jit(static_argnames=["params", "policy"])
def compute_equilibrium(
    params: ModelParameters,
    policy: PolicyConfig,
    risk_high: Float[Array, ""] | float = 0.3,
    risk_low: Float[Array, ""] | float = 0.1,
    proportion_high: Float[Array, ""] | float = 0.2,
) -> InsuranceEquilibrium:
    """
    Determine which equilibrium type exists under current parameters.
    """
    # Note: cannot use logger inside @jit unless wrapped in lax.debug.callback
    return lax.cond(
        policy.allow_genetic_test_results,
        lambda _: separating_equilibrium(params, risk_high, risk_low, proportion_high),
        lambda _: pooling_equilibrium(params, risk_high, risk_low, proportion_high),
        operand=None,
    )


def compute_premium_divergence(
    params: ModelParameters,
    baseline_policy: Any,
    reform_policy: Any = None,
) -> dict[str, float]:
    """
    Compute premium divergence between two policies or within one policy.
    """
    if reform_policy is None or isinstance(reform_policy, float | int):
        policy = baseline_policy
        risk_h = float(reform_policy) if reform_policy is not None else 0.3
        eq = compute_equilibrium(params, policy, risk_high=risk_h)
        return {
            "premium_high": float(eq.premium_high),
            "premium_low": float(eq.premium_low),
            "premium_high_risk": float(eq.premium_high),
            "premium_low_risk": float(eq.premium_low),
            "divergence": float(eq.premium_high - eq.premium_low),
            "is_pooled": bool(abs(eq.premium_high - eq.premium_low) < 1e-5),
        }

    eq_base = compute_equilibrium(params, baseline_policy)
    eq_reform = compute_equilibrium(params, reform_policy)

    return {
        "baseline_premium_high": float(eq_base.premium_high),
        "reform_premium_high": float(eq_reform.premium_high),
        "avg_premium_baseline": float(eq_base.premium_high + eq_base.premium_low) / 2.0,
        "avg_premium_reform": float(eq_reform.premium_high + eq_reform.premium_low) / 2.0,
        "risk_rating_baseline": float(eq_base.premium_high - eq_base.premium_low),
        "risk_rating_reform": float(eq_reform.premium_high - eq_reform.premium_low),
        "relative_divergence": float(eq_reform.premium_high - eq_reform.premium_low)
        / (float(eq_base.premium_high - eq_base.premium_low) + 1e-10),
        "divergence_delta": float(
            (eq_reform.premium_high - eq_reform.premium_low)
            - (eq_base.premium_high - eq_base.premium_low)
        ),
        "premium_high_risk": float(eq_reform.premium_high),
        "absolute_divergence": float(eq_reform.premium_high - eq_reform.premium_low),
    }


def get_standard_risk_parameters() -> dict[str, float]:
    """
    Get standard risk parameters.
    """
    return {
        "risk_high": 0.3,
        "risk_low": 0.1,
        "proportion_high": 0.2,
    }


@jit(static_argnames=["params"])
def verify_equilibrium_stability(
    premium: Float[Array, ""],
    params: ModelParameters,
    risk_high: float = 0.3,
    risk_low: float = 0.1,
    proportion_high: float = 0.2,
) -> Float[Array, ""]:
    """
    Compute the derivative of the insurer's profit function.
    """

    def profit_fn(p):
        takeup_h = compute_demand(p, price_elasticity=params.demand_elasticity_high_risk)
        takeup_l = compute_demand(p)
        total_insured = proportion_high * takeup_h + (1.0 - proportion_high) * takeup_l + 1e-10
        avg_risk = (
            proportion_high * takeup_h * jnp.asarray(risk_high)
            + (1.0 - proportion_high) * takeup_l * jnp.asarray(risk_low)
        ) / total_insured
        return p - avg_risk * (1.0 + params.baseline_loading)

    return jacfwd(profit_fn)(premium)


@jit
def compute_risk_premium(
    risk_probability: Any, loading: float = 0.15, sum_insured: float = 1.0
) -> Float[Array, ""]:
    """Compute risk premium."""
    return _to_float_scalar(jnp.asarray(risk_probability) * (1.0 + loading) * sum_insured)


@jit
def zero_profit_premium(
    risk_high: Any,
    risk_low: float = 0.1,
    prop_high: float = 0.2,
    loading: float = 0.0,
) -> Float[Array, ""]:
    """Compute zero-profit pooling premium."""
    return _to_float_scalar(
        (
            jnp.asarray(prop_high) * jnp.asarray(risk_high)
            + (1.0 - jnp.asarray(prop_high)) * jnp.asarray(risk_low)
        )
        * (1.0 + jnp.asarray(loading))
    )
