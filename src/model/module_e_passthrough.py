"""
Module E: Enforcement and Compliance (Passthrough Logic).

Provides a stable interface for integrating strategic enforcement games
into the primary policy evaluation pipeline.
"""

from __future__ import annotations

from jax import jit
from jaxtyping import Array, Float


@jit
def compute_expected_penalty(
    penalty_max: Float[Array, ""],
    detection_prob: Float[Array, ""],
) -> Float[Array, ""]:
    """
    Calculate the effective deterrence from expected penalties.
    """
    return penalty_max * detection_prob
