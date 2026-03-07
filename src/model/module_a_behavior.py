"""
Module A: Behavior / Deterrence model - CORE JIT-compiled functions.

This module contains the core functions that work with JAX arrays.
Use module_a_behavior_wrappers.py for user-facing functions that accept pydantic models.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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


# Don't use @jit here - boolean arguments don't work with JIT
def compute_perceived_penalty(
    adverse_selection_elasticity: float,
    baseline_loading: float,
    allow_genetic_test_results: bool,
    enforcement_strength: float,
    enforcement_effectiveness: float,
    moratorium_effect: float,
    sum_insured_caps: dict[str, float] | None = None,
) -> Float[Array, ""]:
    """
    Compute perceived discrimination penalty under policy regime.
    """
    # Base penalty from adverse selection
    base_penalty = adverse_selection_elasticity * baseline_loading

    # Policy reduces penalty
    enforcement_factor = enforcement_strength * enforcement_effectiveness

    if allow_genetic_test_results:
        restriction_strength = 0.0
    elif sum_insured_caps is not None:
        restriction_strength = 0.5 + moratorium_effect
    else:
        restriction_strength = 1.0

    penalty_reduction = restriction_strength * (0.5 + 0.5 * enforcement_factor)
    penalty_reduction = min(penalty_reduction, 0.95)

    # Final perceived penalty
    perceived_penalty = base_penalty * (1.0 - penalty_reduction)

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
    Compute probability of testing.
    """
    scaled_utility = utility * scale
    return jnp.exp(scaled_utility) / (1.0 + jnp.exp(scaled_utility))


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
    # Compute perceived penalty
    perceived_penalty = compute_perceived_penalty(
        params.adverse_selection_elasticity,
        params.baseline_loading,
        policy.allow_genetic_test_results,
        policy.enforcement_strength,
        params.enforcement_effectiveness,
        params.moratorium_effect,
        policy.sum_insured_caps,
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
    Get standard policy configurations with scales matching existing tests.
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
            description="Moratorium",
            allow_genetic_test_results=False,
            allow_family_history=True,
            sum_insured_caps={"death": 600000.0, "tpd": 200000.0, "trauma": 200000.0},
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
