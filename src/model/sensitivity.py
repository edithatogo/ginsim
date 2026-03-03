from __future__ import annotations

import jax
import jax.numpy as jnp

from .evppi_rff import rff_features, ridge_fit

def sobol_first_order_rff(y: jnp.ndarray,
                          theta: jnp.ndarray,
                          key: jax.Array,
                          n_features: int = 256,
                          lengthscale: float = 1.0,
                          l2: float = 1e-2) -> jnp.ndarray:
    """Approximate first-order Sobol index S1 = Var(E[y|theta]) / Var(y) using an RFF ridge surrogate."""
    y = jnp.asarray(y)
    if y.ndim == 1:
        y2 = y[:, None]
    else:
        y2 = y

    Phi = rff_features(key, theta, n_features=n_features, lengthscale=lengthscale)
    W = ridge_fit(Phi, y2, l2=l2)
    cond = Phi @ W

    var_total = jnp.var(y2, axis=0) + 1e-12
    var_cond = jnp.var(cond, axis=0)
    s1 = jnp.clip(var_cond / var_total, 0.0, 1.0)
    return s1[0] if y.ndim == 1 else s1
