"""
VOI: Value of Information utilities

Scaffold module: replace placeholders with jurisdiction-specific, data-driven implementations.

Design goals:
- Pure functions compatible with JAX transforms (jit, vmap, scan).
- Deterministic randomness via explicit PRNG keys.
- Vectorized computations where possible.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

try:
    import jax
    import jax.numpy as jnp
except Exception as e:
    raise ImportError(
        "JAX (and jaxlib) must be installed to run this module. "
        "Install platform-appropriate jaxlib and rerun."
    ) from e

from typing import Sequence

def evpi(net_benefit: jnp.ndarray) -> jnp.ndarray:
    """
    Expected Value of Perfect Information.
    net_benefit: array [S, P] where S draws, P policies. Higher is better.
    EVPI = E[max_p NB] - max_p E[NB]
    """
    term1 = jnp.mean(jnp.max(net_benefit, axis=1))
    term2 = jnp.max(jnp.mean(net_benefit, axis=0))
    return term1 - term2

def evppi(net_benefit: jnp.ndarray,
          param_samples: jnp.ndarray,
          n_bins: int = 20) -> jnp.ndarray:
    """
    Very lightweight EVPPI estimator by binning a scalar parameter.
    For production, replace with regression-based EVPPI (e.g., GAM/GP) or
    nested Monte Carlo with smoothing.

    net_benefit: [S, P]
    param_samples: [S]
    """
    # sort by parameter
    idx = jnp.argsort(param_samples)
    nb = net_benefit[idx]
    ps = param_samples[idx]

    # bin edges by quantiles
    qs = jnp.linspace(0.0, 1.0, n_bins + 1)
    edges = jnp.quantile(ps, qs)

    def bin_value(i):
        lo, hi = edges[i], edges[i+1]
        m = (ps >= lo) & (ps <= hi) if i == n_bins - 1 else (ps >= lo) & (ps < hi)
        # If empty, ignore
        nb_m = nb[m]
        w = jnp.mean(m.astype(jnp.float32))
        val = jnp.where(nb_m.shape[0] > 0, jnp.max(jnp.mean(nb_m, axis=0)), 0.0)
        return w * val

    term1 = jnp.sum(jax.vmap(bin_value)(jnp.arange(n_bins)))
    term2 = jnp.max(jnp.mean(net_benefit, axis=0))
    return term1 - term2
