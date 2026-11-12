"""
Proof diagnostics for equilibrium and enforcement fixed points.
"""

from __future__ import annotations

from typing import Any

import jax
import jax.numpy as jnp

from . import module_c_insurance_eq as mod_c
from . import module_enforcement as mod_e
from .parameters import ModelParameters, PolicyConfig


def _pooling_profit_gap(
    premium: Any,
    params: ModelParameters,
    risk_high: Any = 0.3,
    risk_low: Any = 0.1,
    proportion_high: Any = 0.2,
) -> Any:
    """Return the zero-profit residual at a candidate premium."""
    takeup_h = mod_c.compute_demand(premium, price_elasticity=params.demand_elasticity_high_risk)
    takeup_l = mod_c.compute_demand(premium)
    total_insured = proportion_high * takeup_h + (1.0 - proportion_high) * takeup_l + 1e-10
    avg_risk = (
        proportion_high * takeup_h * jnp.asarray(risk_high)
        + (1.0 - proportion_high) * takeup_l * jnp.asarray(risk_low)
    ) / total_insured
    return premium - avg_risk * (1.0 + params.baseline_loading)


def summarize_proofs(
    params: ModelParameters,
    policy: PolicyConfig,
    risk_high: Any = 0.3,
    risk_low: Any = 0.1,
    proportion_high: Any = 0.2,
) -> dict[str, float | str]:
    """Compute lightweight proof diagnostics for the current policy evaluation."""
    equilibrium = mod_c.compute_equilibrium(
        params,
        policy,
        risk_high=risk_high,
        risk_low=risk_low,
        proportion_high=proportion_high,
    )
    premium = jnp.asarray(equilibrium.premium_high)
    profit_gap = _pooling_profit_gap(
        premium,
        params,
        risk_high=risk_high,
        risk_low=risk_low,
        proportion_high=proportion_high,
    )
    jacobian = mod_c.verify_equilibrium_stability(
        premium,
        params,
        risk_high=risk_high,
        risk_low=risk_low,
        proportion_high=proportion_high,
    )
    hessian = jax.hessian(
        lambda p: _pooling_profit_gap(
            p,
            params,
            risk_high=risk_high,
            risk_low=risk_low,
            proportion_high=proportion_high,
        )
    )(premium)

    enforcement = mod_e.compute_compliance_equilibrium(params, policy)
    compliance_target = mod_e.compute_compliance_decision(
        enforcement.expected_penalty,
        5000.0,
    )
    compliance_residual = jnp.asarray(compliance_target) - jnp.asarray(enforcement.compliance_rate)

    return {
        "equilibrium_type": equilibrium.equilibrium_type,
        "premium_stationarity": float(profit_gap),
        "premium_jacobian": float(jacobian),
        "premium_hessian": float(hessian),
        "compliance_fixed_point_residual": float(compliance_residual),
    }
