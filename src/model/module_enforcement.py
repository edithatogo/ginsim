"""
Module E: Enforcement and Compliance.

Models the effectiveness of policy enforcement and the resulting expected
penalties for non-compliance.
"""

from __future__ import annotations

from typing import Any

import jax
import jax.numpy as jnp
from jax import jit
from jaxtyping import Array, Float

from .parameters import ModelParameters


class DictObject(dict):
    """Helper that allows both attribute and dictionary access."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name, value):
        self[name] = value


@jit
def _compute_expected_penalty_jit(
    penalty_max: float | Array,
    detection_prob: float | Array,
    enforcement_effectiveness: float | Array,
) -> Float[Array, ""]:
    return (
        jnp.asarray(penalty_max)
        * jnp.asarray(detection_prob)
        * jnp.asarray(enforcement_effectiveness)
    )


def compute_expected_penalty(
    penalty_max: Any,
    detection_prob: Any = 0.05,
    enforcement_effectiveness: Any = 0.5,
    **kwargs: Any,
) -> Any:
    """Public wrapper with alias support."""
    d_prob = kwargs.get("detection_probability", detection_prob)
    return _compute_expected_penalty_jit(penalty_max, d_prob, enforcement_effectiveness)


@jit
def _compute_compliance_decision_jit(
    expected_penalty: float | Array,
    compliance_cost: float | Array,
) -> Float[Array, ""]:
    diff = jnp.asarray(expected_penalty) - jnp.asarray(compliance_cost)
    return jax.nn.sigmoid(diff)


def compute_compliance_decision(
    expected_penalty: Any,
    compliance_cost: Any = 5000.0,
    **kwargs: Any,
) -> Any:
    """Public wrapper with alias support."""
    benefit = kwargs.get("violation_benefit", compliance_cost)
    return _compute_compliance_decision_jit(expected_penalty, benefit)


def compute_compliance_equilibrium(
    params: ModelParameters,
    policy: Any = None,
    compliance_cost: Any = None,
) -> Any:
    """Compute equilibrium compliance rate."""
    if policy is None:
        # Compatibility mode
        p_max = params
        d_prob = 0.05
        c_cost = 5000.0 if compliance_cost is None else compliance_cost
    else:
        p_max = getattr(policy, "penalty_max", 0.0)
        d_prob = (
            params.detection_prob_baseline if hasattr(params, "detection_prob_baseline") else 0.05
        )
        c_cost = params.compliance_cost_fixed

    expected_penalty = compute_expected_penalty(p_max, d_prob, 1.0)
    rate = compute_compliance_decision(expected_penalty, c_cost)
    return DictObject(
        {
            "compliance_rate": rate,
            "violation_rate": 1.0 - rate,
            "detection_rate": d_prob,
            "expected_penalty": expected_penalty,
        }
    )


def compute_enforcement_effect(
    params: ModelParameters,
    baseline_policy: Any = None,
    reform_policy: Any = None,
) -> Any:
    """Compute enforcement effect."""
    if reform_policy is not None:
        strength = getattr(reform_policy, "enforcement_strength", 1.0)
        effectiveness = params.enforcement_effectiveness
    else:
        # Compatibility mode
        strength = float(params)
        effectiveness = float(baseline_policy) if baseline_policy is not None else 0.5

    res = jnp.clip(jnp.asarray(strength) * jnp.asarray(effectiveness), 0.0, 1.0)
    return DictObject(
        {
            "compliance_baseline": res,
            "compliance_reform": res,
            "compliance_change": 0.0,
            "violation_baseline": 1.0 - res,
            "violation_reform": 1.0 - res,
            "enforcement_effect": res,
        }
    )


def compute_optimal_enforcement(
    params: ModelParameters,
    policy: Any = None,
) -> Any:
    """Compute optimal enforcement level."""
    if policy is not None:
        budget = params.enforcement_budget
        marginal_cost = params.marginal_cost_enforcement
    else:
        # Compatibility mode
        budget = float(params)
        marginal_cost = 0.1

    res = jnp.clip(budget / (marginal_cost + 1e-10), 0.0, 1.0)
    return DictObject(
        {
            "optimal_enforcement": res,
            "optimal_compliance": res,
            "optimal_violation_rate": 1.0 - res,
            "objective_value": 0.0,
        }
    )


def compute_violation_benefit(
    risk_reduction: Any,
    loading_savings: Any = 0.1,
) -> Any:
    """Compute benefit of policy violation."""
    r = 0.2 if hasattr(risk_reduction, "baseline_loading") else float(risk_reduction)
    ls = 0.1 if hasattr(loading_savings, "allow_genetic_test_results") else float(loading_savings)
    return jnp.asarray(r) + jnp.asarray(ls)


def compute_detection_probability(
    enforcement_strength: Any,
    base_detection_prob: Any = 0.05,
) -> Any:
    """Compute detection probability."""
    return jnp.clip(
        jnp.asarray(base_detection_prob) * (1.0 + jnp.asarray(enforcement_strength)), 0.0, 1.0
    )


def compute_compliance_decision_probability(
    expected_penalty: Any,
    compliance_cost: Any,
) -> Any:
    """Alias for compliance decision."""
    return compute_compliance_decision(expected_penalty, compliance_cost)


def get_standard_enforcement_parameters() -> dict[str, float]:
    """Get standard parameters."""
    return {
        "detection_prob_baseline": 0.05,
        "enforcement_budget": 1000000.0,
        "marginal_cost_enforcement": 0.5,
        "monitoring_intensity": 0.5,
        "target_compliance": 0.9,
        "enforcement_cost_parameter": 0.1,
        "max_detection_rate": 0.1,
    }


def get_standard_compliance_parameters() -> dict[str, float]:
    """Get standard compliance parameters."""
    return {"base_compliance_cost": 5000.0}
