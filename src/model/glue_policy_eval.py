"""
Policy glue: integrate modules and compute decision metrics

This is a scaffold. Replace placeholder models with jurisdiction-specific and data-driven implementations.

Design goals:
- Pure functions compatible with JAX transforms (jit, vmap, scan).
- Deterministic randomness via explicit PRNG keys.
- Shape-safe arrays (use jaxtyping/chex in real implementations).
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

from .module_a_behavior import BehaviorParams
from .module_b_clinical import ClinicalParams, simulate_outcomes
from .module_c_insurance_eq import InsuranceParams
from .module_e_passthrough import PassThroughParams
from .module_e_passthrough import run_module as run_passthrough
from .module_f_data_quality import DataQualityParams


@dataclass(frozen=True)
class GlobalParams:
    behavior: BehaviorParams
    clinical: ClinicalParams
    insurance: InsuranceParams
    passthrough: PassThroughParams
    data_quality: DataQualityParams


def simulate_policy(key: jax.Array, policy: dict[str, Any], params: GlobalParams) -> dict[str, Any]:
    """
    One policy simulation pass (deterministic given key and params).
    Common random numbers should be implemented by splitting keys consistently across policies.
    """
    # Module A: placeholder uptake mapping driven by policy restrictions.
    policy_shock = params.behavior.policy_shock
    if not policy.get("allow_genetic_test_results", True):
        policy_shock += 0.15
    uptake = jnp.clip(jax.nn.sigmoid(params.behavior.baseline_logit + policy_shock), 0.0, 1.0)

    # Module B
    out_b = simulate_outcomes(uptake, params.clinical)

    # Module C: simple premium/takeup placeholder for glue scripts.
    avg_premium = jnp.array(
        params.insurance.base_premium
        + params.insurance.loss_cost
        * params.insurance.adverse_selection_sensitivity
        * (1.0 - uptake)
    )
    takeup = jnp.clip(1.0 - params.insurance.price_elasticity * (avg_premium / 10000.0), 0.0, 1.0)
    out_c = {"premium": avg_premium, "takeup": takeup}

    # Module E (pass-through; requires market concentration input in real implementation)
    out_e = run_passthrough(jax.random.fold_in(key, 17), policy, hhi=0.2, params=params.passthrough)

    # Module F (data quality; fear should come from Module A / survey latent variable)
    fear = jnp.clip(1.0 - uptake, 0.0, 1.0)  # placeholder mapping
    participation = jnp.clip(
        jax.nn.sigmoid(
            params.data_quality.base_participation_logit
            - params.data_quality.fear_sensitivity * fear
        ),
        0.0,
        1.0,
    )
    auc = jnp.clip(
        params.data_quality.base_auc - params.data_quality.auc_sensitivity * fear, 0.5, 0.99
    )
    out_f = {"repr_score": participation, "auc": auc, "mean_participation": participation}

    # Minimal DCBA-style metric placeholders
    # Replace with full accounting: healthcare costs, premiums, fiscal spillovers, equity weights, etc.
    net_health_cost = -jnp.sum(out_b["cost_savings"])  # negative means savings
    net_qalys = jnp.sum(out_b["qaly_gains"])
    avg_premium = out_c["premium"]
    takeup = out_c["takeup"]

    return {
        "policy": policy["name"],
        "net_health_cost": net_health_cost,
        "net_qalys": net_qalys,
        "avg_premium": avg_premium,
        "insurance_takeup": takeup,
        "pass_through": out_e["pass_through"],
        "data_repr_score": out_f["repr_score"],
        "data_auc": out_f["auc"],
        "series": {
            "uptake": uptake,
            "prevented_events": out_b["prevented_events"],
            "mean_participation": out_f["mean_participation"],
        },
    }
