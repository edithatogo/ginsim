"""
Module A: Behavior / Deterrence model - CORE JIT-compiled functions.

This module contains the core functions that work with JAX arrays.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
import jax.random as jr
from jaxtyping import Array, Float

from .parameters import PolicyConfig


@dataclass(frozen=True)
class BehaviorParams:
    """Compact behavior parameters used by glue scripts."""

    baseline_logit: float
    policy_shock: float
    trend: float


@jax.jit
def taper_function(x: Any, cap: Any, taper_range: Any) -> Array:
    """
    Compute a smooth tapering protection factor.
    """
    safe_range = jnp.maximum(jnp.asarray(taper_range), 1e-10)
    z = (jnp.asarray(x) - jnp.asarray(cap)) / safe_range
    z = jnp.clip(z, 0.0, 1.0)
    return 0.5 * (1.0 + jnp.cos(jnp.pi * z))


def compute_perceived_penalty(
    adverse_selection_elasticity: Any,
    baseline_loading: Any,
    allow_genetic_test_results: bool,
    enforcement_strength: Any,
    enforcement_effectiveness: Any,
    moratorium_effect: Any,
    sum_insured_caps: dict[str, float] | None = None,
    high_sum_insured_share: Any = 0.25,
    taper_range: Any = 0.0,
    acc_deterrence_offset: Any = 0.0,
    audit_intensity: Any = 0.50,
    audit_intensity_apra: Any = 0.50,
    audit_intensity_asic: Any = 0.50,
) -> Float[Array, ""]:
    """
    Compute perceived discrimination penalty under policy regime.
    """
    base_penalty = jnp.asarray(adverse_selection_elasticity) * jnp.asarray(baseline_loading)

    # AU-specific oversight modelling: combined APRA/ASIC intensity
    combined_audit = jnp.sqrt(jnp.asarray(audit_intensity_apra) * jnp.asarray(audit_intensity_asic))
    eff = jnp.maximum(jnp.asarray(enforcement_effectiveness), combined_audit)
    eff = jnp.maximum(eff, jnp.asarray(audit_intensity))

    enforcement_factor = jnp.asarray(enforcement_strength) * eff

    # JAX-compatible restriction strength logic
    # 1. No restriction if genetic results allowed
    # 2. Threshold protection if caps exist
    # 3. Full restriction otherwise
    avg_protection_high = taper_function(
        jnp.asarray(1.0),
        jnp.asarray(0.0),
        jnp.asarray(taper_range) / 1000000.0,
    )
    base_restriction = 1.0 - jnp.asarray(high_sum_insured_share)
    taper_bonus = jnp.asarray(high_sum_insured_share) * avg_protection_high
    threshold_restriction = (base_restriction + taper_bonus) * (
        0.7 + 0.3 * jnp.asarray(moratorium_effect)
    )

    restriction_strength = jnp.where(
        allow_genetic_test_results,
        0.0,
        jnp.where(sum_insured_caps is not None, threshold_restriction, 1.0),
    )

    penalty_reduction = restriction_strength * (0.5 + 0.5 * enforcement_factor)
    penalty_reduction = jnp.clip(penalty_reduction, 0.0, 0.95)
    effective_penalty_base = base_penalty * (1.0 - jnp.asarray(acc_deterrence_offset))
    perceived_penalty = effective_penalty_base * (1.0 - penalty_reduction)

    return jnp.asarray(perceived_penalty, dtype=jnp.float32)


def compute_perceived_penalty_wrapper(params: Any, policy: PolicyConfig) -> float:
    """Wrapper that accepts pydantic models."""
    penalty = compute_perceived_penalty(
        params.adverse_selection_elasticity,
        params.baseline_loading,
        policy.allow_genetic_test_results,
        policy.enforcement_strength,
        params.enforcement_effectiveness,
        params.moratorium_effect,
        policy.sum_insured_caps,
        getattr(params, "high_sum_insured_share", 0.25),
        policy.taper_range,
        getattr(params, "acc_deterrence_offset", 0.0),
        getattr(params, "audit_intensity", 0.50),
        getattr(params, "audit_intensity_apra", 0.50),
        getattr(params, "audit_intensity_asic", 0.50),
    )
    return float(penalty)


def compute_testing_utility(
    benefits: Any,
    perceived_penalty: Any,
    individual_characteristics: dict[str, Any] | None = None,
    medicare_cost_share: Any = 0.0,
    remoteness_index: Any = 0.0,
    remoteness_weight: Any = 0.20,
    year: Any = 0,
    tech_improvement_rate: Any = 0.15,
) -> Float[Array, "*"]:
    """
    Compute utility of genetic testing.
    Incorporates temporal cost curve (costs drop over time).
    """
    # Temporal cost curve: 15% annual drop
    cost_multiplier = (1.0 - tech_improvement_rate) ** float(year)
    base_test_cost = 0.1 * cost_multiplier * (1.0 - jnp.asarray(medicare_cost_share))
    spatial_test_cost = base_test_cost * (
        1.0 + jnp.asarray(remoteness_weight) * jnp.asarray(remoteness_index)
    )
    utility = jnp.asarray(benefits) - jnp.asarray(perceived_penalty) - spatial_test_cost

    if individual_characteristics is not None:
        for factor, val in individual_characteristics.items():
            # Add value directly (assuming they are pre-weighted shifts or utility components)
            utility = utility + jnp.asarray(val)

    return utility


def compute_testing_probability(utility: Any, scale: float = 1.0) -> Float[Array, "*"]:
    """
    Compute probability of testing using numerically stable sigmoid.
    """
    scaled_utility = jnp.asarray(utility) * scale
    return jax.nn.sigmoid(scaled_utility)


def compute_testing_uptake(
    params: Any,
    policy: PolicyConfig,
    benefits_mean: float = 0.5,
    benefits_sd: float = 0.1,
    n_individuals: int = 1000,
    rng_key: Array | None = None,
    remoteness_index: float = 0.0,
    year: int = 0,
    individual_characteristics: dict[str, Any] | None = None,
) -> Float[Array, ""]:
    """
    Compute aggregate testing uptake.
    """
    perceived_penalty = compute_perceived_penalty(
        params.adverse_selection_elasticity,
        params.baseline_loading,
        policy.allow_genetic_test_results,
        policy.enforcement_strength,
        params.enforcement_effectiveness,
        params.moratorium_effect,
        policy.sum_insured_caps,
        getattr(params, "high_sum_insured_share", 0.25),
        policy.taper_range,
        getattr(params, "acc_deterrence_offset", 0.0),
        getattr(params, "audit_intensity", 0.50),
        getattr(params, "audit_intensity_apra", 0.50),
        getattr(params, "audit_intensity_asic", 0.50),
    )

    if rng_key is not None:
        benefits = jr.normal(rng_key, (n_individuals,)) * benefits_sd + benefits_mean
    else:
        benefits = jnp.linspace(
            benefits_mean - 3 * benefits_sd,
            benefits_mean + 3 * benefits_sd,
            n_individuals,
        )

    utilities = compute_testing_utility(
        benefits,
        perceived_penalty,
        individual_characteristics=individual_characteristics,
        medicare_cost_share=getattr(params, "medicare_cost_share", 0.0),
        remoteness_index=remoteness_index,
        remoteness_weight=getattr(params, "remoteness_weight", 0.20),
        year=year,
        tech_improvement_rate=getattr(params, "tech_improvement_rate", 0.15),
    )

    probabilities = compute_testing_probability(utilities)
    return jnp.mean(probabilities)


def compute_policy_effect(
    params: Any,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> dict[str, Any]:
    """
    Compute effect of policy reform.
    """
    baseline_uptake = compute_testing_uptake(params, baseline_policy)
    reform_uptake = compute_testing_uptake(params, reform_policy)

    absolute_effect = reform_uptake - baseline_uptake
    relative_effect = absolute_effect / (baseline_uptake + 1e-10)

    return {
        "baseline_uptake": baseline_uptake,
        "reform_uptake": reform_uptake,
        "absolute_effect": absolute_effect,
        "relative_effect": relative_effect,
    }


def evaluate_multiple_policies(
    params: Any,
    policies: list[PolicyConfig],
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Evaluate testing uptake for multiple policies.
    """
    results = {}
    for policy in policies:
        results[policy.name] = compute_testing_uptake(params, policy, **kwargs)
    return results


def get_standard_policies() -> dict[str, PolicyConfig]:
    """
    Get standard policy configurations.
    """
    return {
        "status_quo": PolicyConfig(
            name="status_quo",
            description="Status Quo",
            allow_genetic_test_results=True,
            allow_family_history=True,
            enforcement_strength=1.0,
        ),
        "moratorium": PolicyConfig(
            name="moratorium",
            description="Moratorium (Self-Regulation)",
            allow_genetic_test_results=False,
            allow_family_history=True,
            sum_insured_caps={
                "life": 500000.0,
                "tpd": 500000.0,
                "trauma": 200000.0,
                "income_protection": 4000.0,
            },
            taper_range=100000.0,
            enforcement_strength=0.5,
        ),
        "ban": PolicyConfig(
            name="ban",
            description="Statutory Ban",
            allow_genetic_test_results=False,
            allow_family_history=False,
            enforcement_strength=1.0,
            penalty_max=500000.0,
        ),
    }
