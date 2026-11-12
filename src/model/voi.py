"""
VOI (Value of Information) calculation engine.

Implements expected value of perfect information (EVPI) and partial information (EVPPI)
logic for genetic policy uncertainty.
"""

from __future__ import annotations

from functools import partial

import jax
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


@partial(jit, static_argnames=("n_bins",))
def compute_evppi(
    expected_welfare_matrix: Float[Array, "n_policies n_draws"],
    parameter_draws: Float[Array, "*"],
    n_bins: int = 20,
) -> Float[Array, ""]:
    """
    Calculate EVPPI for a specific parameter using a stratified mean approach.
    Efficient JAX implementation avoiding nested loops.
    """
    n_draws = expected_welfare_matrix.shape[1]

    # 1. Bin the parameter draws
    p_min, p_max = jnp.min(parameter_draws), jnp.max(parameter_draws)
    # Avoid zero range
    safe_p_max = jnp.maximum(p_max, p_min + 1e-7)

    # Calculate bin indices for each draw
    bins = jnp.floor((parameter_draws - p_min) / (safe_p_max - p_min) * n_bins).astype(jnp.int32)
    bins = jnp.clip(bins, 0, n_bins - 1)

    # 2. Compute conditional expected welfare for each policy in each bin
    # We use segments for efficient grouping
    def get_bin_means(policy_row):
        bin_sums = jnp.zeros(n_bins).at[bins].add(policy_row)
        bin_counts = jnp.zeros(n_bins).at[bins].add(1.0)
        return bin_sums / jnp.maximum(bin_counts, 1.0)

    # Map over all policies
    conditional_welfare = jax.vmap(get_bin_means)(expected_welfare_matrix)

    # 3. EVPPI Calculation
    # E [ max_j (E[W|p]) ]
    # We take the mean across bins, weighted by bin counts
    bin_counts = jnp.zeros(n_bins).at[bins].add(1.0)
    bin_probs = bin_counts / n_draws

    inner_expectations = jnp.max(conditional_welfare, axis=0)
    e_max_e_w_cond = jnp.sum(inner_expectations * bin_probs)

    # Max of overall means (same as in EVPI)
    max_e_w = jnp.max(jnp.mean(expected_welfare_matrix, axis=1))

    return jnp.maximum(0.0, e_max_e_w_cond - max_e_w)


# Aliases for backward compatibility
evpi = compute_evpi
evppi = compute_evppi
