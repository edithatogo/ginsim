from __future__ import annotations

import jax
import jax.numpy as jnp

from .evppi_rff import rff_features, ridge_fit

def total_order_sobol_rff(y: jnp.ndarray,
                          theta_complement: jnp.ndarray,
                          key: jax.Array,
                          n_features: int = 256,
                          lengthscale: float = 1.0,
                          l2: float = 1e-2) -> jnp.ndarray:
    """
    Approximate total-order Sobol index for a group g using the complement features (-g):

      ST_g = 1 - Var(E[Y | X_-g]) / Var(Y)

    We estimate E[Y | X_-g] with an RFF ridge surrogate.
    This captures all variance *not* explained by the complement, which is interpreted as total effect of g
    (main + interactions), under the assumption the complement feature set is rich enough.

    y: [S] or [S,K]
    theta_complement: [S,Dc] features representing all other uncertain parameter groups
    """
    y = jnp.asarray(y)
    if y.ndim == 1:
        y2 = y[:, None]
    else:
        y2 = y

    Phi = rff_features(key, theta_complement, n_features=n_features, lengthscale=lengthscale)
    W = ridge_fit(Phi, y2, l2=l2)
    cond = Phi @ W

    var_total = jnp.var(y2, axis=0) + 1e-12
    var_explained_by_complement = jnp.var(cond, axis=0)

    st = jnp.clip(1.0 - (var_explained_by_complement / var_total), 0.0, 1.0)
    return st[0] if y.ndim == 1 else st
