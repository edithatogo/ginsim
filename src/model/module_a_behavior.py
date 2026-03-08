"""
Module A: Behavior / Deterrence model - CORE JIT-compiled functions.

This module contains the core functions that work with JAX arrays.
Use module_a_behavior_wrappers.py for user-facing functions that accept pydantic models.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
import jax.random as jr
from jaxtyping import Array, Float
from loguru import logger

from .parameters import PolicyConfig


@dataclass(frozen=True)
class BehaviorParams:
    """Compact behavior parameters used by glue scripts."""

    baseline_logit: float
    policy_shock: float
    trend: float


@jax.jit
def taper_function(x: Array, cap: Array, taper_range: Array) -> Array:
    """
    Compute a smooth tapering protection factor.
    Returns 1.0 if x <= cap, 0.0 if x >= cap + taper_range.
    Interpolates smoothly in between.
    """
    # Normalized position in taper: 0 at cap, 1 at cap + range
    # Avoid division by zero for hard caps
    safe_range = jnp.maximum(taper_range, 1e-10)
    z = (x - cap) / safe_range
    z = jnp.clip(z, 0.0, 1.0)

    # Cosine smoothing (SmoothStep)
    # 0.5 * (1 + cos(pi * z)) gives 1 at z=0, 0 at z=1
    return 0.5 * (1.0 + jnp.cos(jnp.pi * z))


# Don't use @jit here - boolean arguments don't work with JIT
def compute_perceived_penalty(
    adverse_selection_elasticity: float,
    baseline_loading: float,
    allow_genetic_test_results: bool,
    enforcement_strength: float,
    enforcement_effectiveness: float,
    moratorium_effect: float,
    sum_insured_caps: dict[str, float] | None = None,
    high_sum_insured_share: float = 0.25,
    taper_range: float = 0.0,
    acc_deterrence_offset: float = 0.0,
) -> Float[Array, ""]:
    """
    Compute perceived discrimination penalty under policy regime.
    Now supports smooth regulatory tapering and NZ ACC offsets.
    """
    # Base penalty from adverse selection
    base_penalty = adverse_selection_elasticity * baseline_loading

    # Policy reduces penalty
    enforcement_factor = enforcement_strength * enforcement_effectiveness

    if allow_genetic_test_results:
        restriction_strength = 0.0
    elif sum_insured_caps is not None:
        avg_protection_high = taper_function(
            jnp.asarray(1.0), # Normalized proxy for high buyers
            jnp.asarray(0.0),
            jnp.asarray(taper_range / 1000000.0) # Scaled range
        )

        base_restriction = (1.0 - high_sum_insured_share)
        taper_bonus = high_sum_insured_share * avg_protection_high

        restriction_strength = (base_restriction + taper_bonus) * (0.7 + 0.3 * moratorium_effect)
    else:
        restriction_strength = 1.0

    penalty_reduction = restriction_strength * (0.5 + 0.5 * enforcement_factor)
    penalty_reduction = jnp.clip(penalty_reduction, 0.0, 0.95)

    # ACC Offset: Reduces the perceived 'pain' of insurance discrimination
    # because of the no-fault safety net for injury/treatment injury.
    effective_penalty_base = base_penalty * (1.0 - acc_deterrence_offset)

    # Final perceived penalty
    perceived_penalty = effective_penalty_base * (1.0 - penalty_reduction)

    return jnp.asarray(perceived_penalty, dtype=jnp.float32)


# Convenience wrapper
def compute_perceived_penalty_wrapper(
    params: Any,
    policy: PolicyConfig,
) -> float:
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
    )
    return float(penalty)

def compute_testing_utility(
    benefits: Float[Array, "*"],
    perceived_penalty: Float[Array, ""],
    individual_characteristics: dict[str, Float[Array, "*"]] | None = None,
) -> Float[Array, "*"]:
    """
    Compute utility of genetic testing.
    """
    # Base utility
    utility = benefits - perceived_penalty

    # Add individual characteristics
    if individual_characteristics is not None:
        for factor, weight in individual_characteristics.items():
            utility = utility + weight * individual_characteristics.get(factor, 0.0)

    return utility


def compute_testing_probability(
    utility: Float[Array, "*"],
    scale: float = 1.0,
) -> Float[Array, "*"]:
    """
    Compute probability of testing using numerically stable sigmoid.
    """
    scaled_utility = utility * scale
    # jax.nn.sigmoid is numerically stabilized for large values
    return jax.nn.sigmoid(scaled_utility)


def compute_testing_uptake(
    params: Any,
    policy: PolicyConfig,
    benefits_mean: float = 0.5,
    benefits_sd: float = 0.1,
    n_individuals: int = 1000,
    rng_key: Array | None = None,
) -> Float[Array, ""]:
    """
    Compute aggregate testing uptake.
    """
    logger.debug(f"Computing testing uptake for policy: {policy.name}")
    # Compute perceived penalty
    perceived_penalty = compute_perceived_penalty(
        params.adverse_selection_elasticity,
        params.baseline_loading,
        policy.allow_genetic_test_results,
        policy.enforcement_strength,
        params.enforcement_effectiveness,
        params.moratorium_effect,
        policy.sum_insured_caps,
        getattr(params, "high_sum_insured_share", 0.25),
        policy.taper_range
    )

    # Simulate heterogeneous benefits
    if rng_key is not None:
        benefits = jr.normal(rng_key, (n_individuals,)) * benefits_sd + benefits_mean
    else:
        # Deterministic grid
        benefits = jnp.linspace(
            benefits_mean - 3 * benefits_sd,
            benefits_mean + 3 * benefits_sd,
            n_individuals,
        )

    # Compute utility
    utilities = compute_testing_utility(benefits, perceived_penalty)

    # Compute testing probabilities
    probabilities = compute_testing_probability(utilities)

    # Aggregate uptake
    return jnp.mean(probabilities)


def compute_policy_effect(
    params: Any,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> dict[str, Float[Array, ""]]:
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
) -> dict[str, Float[Array, ""]]:
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
            # Exact FSC Moratorium thresholds (AUD)
            sum_insured_caps={"life": 500000.0, "tpd": 500000.0, "trauma": 200000.0, "income_protection": 4000.0},
            taper_range=100000.0, # 100k AUD taper zone
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
