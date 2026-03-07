"""
Module A: Behavior / Deterrence model - User-facing wrappers.

This module provides high-level wrappers for the core JAX functions in
module_a_behavior.py that accept pydantic models and handle conversion.
"""

from __future__ import annotations

from typing import Any

from jaxtyping import Array, Float

from . import module_a_behavior as core
from .parameters import ModelParameters, PolicyConfig


def compute_perceived_penalty(
    params: ModelParameters,
    policy: PolicyConfig,
) -> float:
    """Wrapper for perceived penalty calculation."""
    return core.compute_perceived_penalty_wrapper(params, policy)


def compute_testing_uptake(
    params: ModelParameters,
    policy: PolicyConfig,
    **kwargs: Any,
) -> Float[Array, ""]:
    """Wrapper for aggregate uptake simulation."""
    return core.compute_testing_uptake(params, policy, **kwargs)


def evaluate_multiple_policies(
    params: ModelParameters,
    policies: list[PolicyConfig],
    **kwargs: Any,
) -> dict[str, Float[Array, ""]]:
    """Evaluate uptake for a list of policies."""
    return core.evaluate_multiple_policies(params, policies, **kwargs)


def get_standard_policies() -> dict[str, PolicyConfig]:
    """Get standard benchmark policies."""
    return core.get_standard_policies()


def compute_policy_effect(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> dict[str, Float[Array, ""]]:
    """Wrapper for policy effect calculation."""
    return core.compute_policy_effect(params, baseline_policy, reform_policy)
