"""
Module D: Proxy substitution and underwriting re-optimisation

Scaffold module: replace placeholders with jurisdiction-specific, data-driven implementations.

Design goals:
- Pure functions compatible with JAX transforms (jit, vmap, scan).
- Deterministic randomness via explicit PRNG keys.
- Vectorized computations where possible.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    import jax
    import jax.numpy as jnp
except Exception as e:
    raise ImportError(
        "JAX (and jaxlib) must be installed to run this module. "
        "Install platform-appropriate jaxlib and rerun.",
    ) from e


@dataclass(frozen=True)
class ProxyParams:
    # Toy linear risk score parameters (weights learned/assumed).
    w: jnp.ndarray  # shape [K]
    b: float
    # Penalty for using prohibited features (set high to enforce constraint).
    prohibited_penalty: float = 50.0


def risk_score(x: jnp.ndarray, params: ProxyParams) -> jnp.ndarray:
    """Linear score -> probability of claim (toy)."""
    return jax.nn.sigmoid(jnp.dot(x, params.w) + params.b)


def reoptimize_weights(
    x: jnp.ndarray,
    y: jnp.ndarray,
    allowed_mask: jnp.ndarray,
    key: jax.Array,
    n_steps: int = 200,
    lr: float = 1e-2,
) -> ProxyParams:
    """
    Toy gradient descent re-optimisation with a soft constraint:
    - allowed_mask: 1 for allowed features, 0 for prohibited.
    Replace with a proper constrained optimiser / regularised GLM.
    """
    w = jnp.zeros(x.shape[1])
    b = jnp.array(0.0)

    def loss_fn(w: jnp.ndarray, b: jnp.ndarray) -> jnp.ndarray:
        p = jax.nn.sigmoid(x @ w + b)
        # Logistic loss
        ll = -jnp.mean(y * jnp.log(p + 1e-8) + (1 - y) * jnp.log(1 - p + 1e-8))
        # Penalty on prohibited weights
        penalty = jnp.sum((1.0 - allowed_mask) * (w**2)) * 50.0
        return ll + penalty

    grad_fn = jax.grad(loss_fn, argnums=(0, 1))

    for _ in range(n_steps):
        gw, gb = grad_fn(w, b)
        w = w - lr * gw
        b = b - lr * gb

    return ProxyParams(w=w, b=float(b))


def calibration_error(p: jnp.ndarray, y: jnp.ndarray, n_bins: int = 10) -> jnp.ndarray:
    """Simple ECE-like metric."""
    bins = jnp.linspace(0, 1, n_bins + 1)
    ece = jnp.array(0.0)
    for i in range(n_bins):
        lo, hi = bins[i], bins[i + 1]
        mask = (p >= lo) & (p < hi)
        frac = jnp.mean(mask.astype(jnp.float32))
        # avoid empty bin issues
        avg_p = jnp.where(frac > 0, jnp.sum(p * mask) / (jnp.sum(mask) + 1e-8), 0.0)
        avg_y = jnp.where(frac > 0, jnp.sum(y * mask) / (jnp.sum(mask) + 1e-8), 0.0)
        ece = ece + frac * jnp.abs(avg_p - avg_y)
    return ece


def run_module(
    key: jax.Array, policy: dict[str, Any], x: jnp.ndarray, y: jnp.ndarray, subgroup: jnp.ndarray
) -> dict[str, Any]:
    """
    Inputs:
    - x: underwriting features [N, K] (toy; include proxies such as family history, postcode)
    - y: observed claim indicator [N]
    - subgroup: subgroup labels [N] for fairness diagnostics (e.g., quantiles of SES; do NOT use protected class unless lawful/ethical)
    Output:
    - re-optimised weights for 'ban' policies and metrics for mispricing/fairness
    """
    allow_gen = policy.get("allow_genetic_test_results", True)
    # Convention: feature 0 represents genetic test result (toy). Real implementation will map feature schema.
    allowed_mask = jnp.ones(x.shape[1])
    if allow_gen is False:
        allowed_mask = allowed_mask.at[0].set(0.0)

    # Baseline fit (all allowed)
    base_params = reoptimize_weights(x, y, jnp.ones_like(allowed_mask), key)
    p_base = risk_score(x, base_params)
    ece_base = calibration_error(p_base, y)

    # Adapted fit (policy constraints)
    adapted_params = reoptimize_weights(x, y, allowed_mask, key)
    p_adapt = risk_score(x, adapted_params)
    ece_adapt = calibration_error(p_adapt, y)

    # Subgroup mispricing proxy: mean predicted - mean observed
    def subgroup_gap(p: jnp.ndarray) -> jnp.ndarray:
        gaps = []
        for g in jnp.unique(subgroup):
            m = subgroup == g
            gaps.append(jnp.mean(p[m]) - jnp.mean(y[m]))
        return jnp.stack(gaps)

    gaps_base = subgroup_gap(p_base)
    gaps_adapt = subgroup_gap(p_adapt)

    return {
        "ece_base": ece_base,
        "ece_adapt": ece_adapt,
        "subgroup_gaps_base": gaps_base,
        "subgroup_gaps_adapt": gaps_adapt,
        "params_base": {"w": base_params.w, "b": base_params.b},
        "params_adapt": {"w": adapted_params.w, "b": adapted_params.b},
        "allowed_mask": allowed_mask,
    }
