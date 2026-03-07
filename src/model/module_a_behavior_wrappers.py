"""
Module A: Behavior / Deterrence model - WRAPPERS for JAX compatibility.

This module provides user-facing wrapper functions that accept pydantic models
and call the JIT-compiled core functions with extracted primitives.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from jax import random as jr

from . import module_a_behavior as core

if TYPE_CHECKING:
    from jaxtyping import Array

    from .parameters import ModelParameters, PolicyConfig


def compute_perceived_penalty(
    params: ModelParameters,
    policy: PolicyConfig,
) -> float:
    """
    Compute perceived discrimination penalty under policy regime.

    Wrapper that accepts pydantic models and calls JIT-compiled core function.

    Args:
        params: Model parameters
        policy: Policy configuration

    Returns:
        Perceived penalty (higher = more deterrence)
    """
    penalty = core.compute_perceived_penalty(
        params.adverse_selection_elasticity,
        params.baseline_loading,
        policy.allow_genetic_test_results,
        policy.enforcement_strength,
        params.enforcement_effectiveness,
        params.moratorium_effect,
        policy.sum_insured_caps,
    )
    return float(penalty)


def compute_testing_uptake(
    params: ModelParameters,
    policy: PolicyConfig,
    benefits_mean: float = 0.5,
    benefits_sd: float = 0.1,
    n_individuals: int = 1000,
    rng_key: Array | None = None,
) -> float:
    """
    Compute aggregate testing uptake under policy regime.

    Wrapper that accepts pydantic models.

    Args:
        params: Model parameters
        policy: Policy configuration
        benefits_mean: Mean perceived benefits of testing
        benefits_sd: Standard deviation of benefits
        n_individuals: Number of individuals to simulate
        rng_key: Optional RNG key

    Returns:
        Aggregate testing uptake rate (0-1)
    """
    if rng_key is None:
        rng_key = jr.PRNGKey(20260303)

    uptake = core.compute_testing_uptake(
        params,
        policy,
        benefits_mean,
        benefits_sd,
        n_individuals,
        rng_key,
    )
    return float(uptake)


def compute_policy_effect(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> dict[str, float]:
    """
    Compute effect of policy reform on testing uptake.

    Wrapper that accepts pydantic models.

    Args:
        params: Model parameters
        baseline_policy: Baseline policy
        reform_policy: Reform policy

    Returns:
        Dictionary with baseline_uptake, reform_uptake, absolute_effect, relative_effect
    """
    result = core.compute_policy_effect(
        params,
        baseline_policy,
        reform_policy,
    )

    return {
        "baseline_uptake": float(result["baseline_uptake"]),
        "reform_uptake": float(result["reform_uptake"]),
        "absolute_effect": float(result["absolute_effect"]),
        "relative_effect": float(result["relative_effect"]),
    }


def get_standard_policies() -> dict[str, PolicyConfig]:
    """Get standard policy configurations."""
    return core.get_standard_policies()
