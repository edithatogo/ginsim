"""
Module D: Proxy Substitution model (Advanced Edition).

Implements constrained optimization for underwriting when genetic information
is restricted. Models the degree to which non-genetic features act as
correlated proxies for genetic risk.
"""

from __future__ import annotations

import jax.numpy as jnp
from jax import jit
from jaxtyping import Array, Float


@jit
def compute_proxy_potential(
    family_history_sensitivity: Float[Array, ""],
    other_medical_history_sensitivity: Float[Array, ""],
) -> Float[Array, ""]:
    """
    Estimate the informational redundancy between proxies and genetic data.
    """
    return jnp.maximum(family_history_sensitivity, other_medical_history_sensitivity)
