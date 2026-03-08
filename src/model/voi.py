"""
VOI (Value of Information) calculation engine.

Implements expected value of perfect information (EVPI) and partial information (EVPPI)
logic for genetic policy uncertainty.
"""

from __future__ import annotations

import jax.numpy as jnp
from jax import jit
from jaxtyping import Array, Float


@jit
def compute_evpi(
    expected_welfare_matrix: Float[Array, "n_policies n_draws"],
) -> Float[Array, ""]:
    """
    Calculate EVPI as the difference between information-first and baseline-first expectations.
    """
    # Mean of max vs max of means
    e_max_w = jnp.mean(jnp.max(expected_welfare_matrix, axis=0))
    max_e_w = jnp.max(jnp.mean(expected_welfare_matrix, axis=1))
    return jnp.maximum(0.0, e_max_w - max_e_w)
