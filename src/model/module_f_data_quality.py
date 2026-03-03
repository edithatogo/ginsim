"""
Module F: Data-quality externality (selection bias and tool performance)

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

@dataclass(frozen=True)
class DataQualityParams:
    # Toy selection model parameters
    base_participation_logit: float
    fear_sensitivity: float
    # Toy prediction performance parameters
    base_auc: float
    auc_sensitivity: float  # how representativeness affects AUC
    noise_sd: float = 0.01

def participation_prob(fear: jnp.ndarray, params: DataQualityParams) -> jnp.ndarray:
    logits = params.base_participation_logit - params.fear_sensitivity * fear
    return jax.nn.sigmoid(logits)

def effective_representativeness(p_participate: jnp.ndarray, weights: jnp.ndarray | None = None) -> jnp.ndarray:
    """
    Proxy for representativeness: mean participation probability, optionally weighted.
    Replace with proper selection-bias diagnostics (e.g., covariate balance metrics).
    """
    if weights is None:
        return jnp.mean(p_participate)
    return jnp.sum(weights * p_participate) / (jnp.sum(weights) + 1e-8)

def simulate_auc(key: jax.Array, repr_score: jnp.ndarray, params: DataQualityParams) -> jnp.ndarray:
    """
    Toy mapping: better representativeness improves AUC.
    """
    auc = params.base_auc + params.auc_sensitivity * (repr_score - 0.5)
    auc = jnp.clip(auc, 0.5, 0.99)
    auc = auc + params.noise_sd * jax.random.normal(key)
    return jnp.clip(auc, 0.5, 0.99)

def run_module(key: jax.Array, policy: Dict[str, Any], fear: jnp.ndarray, params: DataQualityParams) -> Dict[str, Any]:
    """
    fear: array capturing perceived discrimination risk (latent or measured).
    Policy changes fear via a simple policy-intensity mapping (placeholder).
    """
    policy_name = policy.get("name", "status_quo")
    policy_intensity = jnp.array(
        0.0 if policy_name == "status_quo" else
        0.5 if policy_name == "moratorium" else
        0.8 if policy_name == "partial_ban" else
        1.0
    )
    # Policy reduces fear (toy); real implementation uses Module A estimates.
    fear_cf = jnp.clip(fear * (1.0 - 0.4 * policy_intensity), 0.0, 1.0)
    p_part = participation_prob(fear_cf, params)
    repr_score = effective_representativeness(p_part)
    auc = simulate_auc(key, repr_score, params)
    return {"repr_score": repr_score, "auc": auc, "mean_participation": jnp.mean(p_part)}
