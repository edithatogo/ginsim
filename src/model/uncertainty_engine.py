"""
Unified Sensitivity Engine (Diamond Standard).

Consolidates JAX-vectorized DSA, PSA, and Sobol analysis for 
high-performance uncertainty quantification.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
from jax import vmap, jit
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig
from .pipeline import evaluate_single_policy, get_standard_policies
from .voi import compute_evpi, compute_evppi


@dataclass(frozen=True)
class UncertaintyResult:
    """Consolidated summary of a Monte Carlo run."""
    mean: Any
    median: Any
    lower_95: Any
    upper_95: Any
    std: Any
    samples: Any


@jit
def calculate_summary_stats(results: Array, n_subsamples: int = 100) -> dict[str, Any]:
    """Compute summary statistics for a batch of results."""
    return {
        "mean": jnp.mean(results),
        "median": jnp.median(results),
        "lower_95": jnp.percentile(results, 2.5),
        "upper_95": jnp.percentile(results, 97.5),
        "std": jnp.std(results),
        "samples": results[:n_subsamples] # Match UncertaintyResult field name
    }


def evaluate_core_numerical(params: ModelParameters, policy: PolicyConfig) -> dict[str, Array]:
    """
    JIT-compatible numerical kernel that returns only arrays.
    """
    # 1. Enforcement
    from . import module_enforcement as mod_e
    enforcement = mod_e.compute_compliance_equilibrium(params, policy)
    
    # 2. Behavior
    from . import module_a_behavior as mod_a
    uptake = mod_a.compute_testing_uptake(params, policy)
    
    # 3. Insurance
    from . import module_c_insurance_eq as mod_c
    market = mod_c.compute_equilibrium(params, policy)
    
    # 4. Ledger
    from . import dcba_ledger as dcba
    from . import module_f_data_quality as mod_f
    dq = mod_f.compute_data_quality_externality(params, policy)
    
    ledger = dcba.compute_dcba(
        testing_uptake=uptake,
        baseline_uptake=jnp.asarray(params.baseline_testing_uptake).astype(float),
        insurance_premium=market.premium_high,
        baseline_premium=0.2,
        insurer_profits=market.insurer_profits,
        baseline_profits=0.05,
        research_value_loss=jnp.asarray(1.0 - dq.participation_rate).astype(float) * jnp.asarray(params.research_participation_value).astype(float),
        ppp_conversion_factor=jnp.asarray(params.ppp_conversion_factor).astype(float),
        equity_factor=jnp.asarray(params.equity_factor).astype(float),
        value_per_qaly=jnp.asarray(params.pharmac_qaly_threshold).astype(float),
    )
    
    return {
        "uptake": uptake,
        "welfare": ledger.net_welfare,
    }


def evaluate_batch(
    params_matrix: ModelParameters,
    policy: PolicyConfig,
) -> dict[str, Any]:
    """
    Vectorized evaluation of a policy over a matrix of parameters.
    """
    vmap_eval = vmap(evaluate_core_numerical, in_axes=(0, None))
    results = vmap_eval(params_matrix, policy)
    
    return {
        "uptake": calculate_summary_stats(results["uptake"]),
        "welfare": calculate_summary_stats(results["welfare"]),
        "raw_welfare": results["welfare"]
    }


def run_psa(
    base_params: ModelParameters,
    policy: PolicyConfig,
    n_draws: int = 1000,
    seed: int = 20260303,
) -> dict[str, UncertaintyResult]:
    """
    Run Probabilistic Sensitivity Analysis (PSA).
    """
    key = jax.random.PRNGKey(seed)
    keys = jax.random.split(key, 3)
    
    d_elasticities = jax.random.uniform(keys[0], (n_draws,), minval=0.8, maxval=1.2) * float(base_params.deterrence_elasticity)
    m_effects = jax.random.uniform(keys[1], (n_draws,), minval=0.8, maxval=1.2) * float(base_params.moratorium_effect)
    
    def _to_batch(val):
        return jnp.full((n_draws,), float(val))

    batch_params = ModelParameters(
        jurisdiction=base_params.jurisdiction,
        calibration_date=base_params.calibration_date,
        baseline_testing_uptake=_to_batch(base_params.baseline_testing_uptake),
        deterrence_elasticity=d_elasticities,
        moratorium_effect=m_effects,
        adverse_selection_elasticity=_to_batch(base_params.adverse_selection_elasticity),
        demand_elasticity_high_risk=_to_batch(base_params.demand_elasticity_high_risk),
        baseline_loading=_to_batch(base_params.baseline_loading),
        family_history_sensitivity=_to_batch(base_params.family_history_sensitivity),
        proxy_substitution_rate=_to_batch(base_params.proxy_substitution_rate),
        pass_through_rate=_to_batch(base_params.pass_through_rate),
        research_participation_elasticity=_to_batch(base_params.research_participation_elasticity),
        research_participation_value=_to_batch(base_params.research_participation_value),
        ppp_conversion_factor=_to_batch(base_params.ppp_conversion_factor),
        equity_factor=_to_batch(base_params.equity_factor),
        high_sum_insured_share=_to_batch(base_params.high_sum_insured_share),
        taper_range=_to_batch(getattr(base_params, "taper_range", 0.0)),
        enforcement_effectiveness=_to_batch(base_params.enforcement_effectiveness),
        complaint_rate=_to_batch(base_params.complaint_rate),
        enforcement_budget=_to_batch(base_params.enforcement_budget),
        marginal_cost_enforcement=_to_batch(base_params.marginal_cost_enforcement),
        compliance_cost_fixed=_to_batch(base_params.compliance_cost_fixed),
        detection_prob_baseline=_to_batch(base_params.detection_prob_baseline),
        acc_deterrence_offset=_to_batch(base_params.acc_deterrence_offset),
        pharmac_qaly_threshold=_to_batch(base_params.pharmac_qaly_threshold),
        medicare_cost_share=_to_batch(base_params.medicare_cost_share),
        audit_intensity=_to_batch(base_params.audit_intensity),
        remoteness_weight=_to_batch(base_params.remoteness_weight),
    )
    
    raw_results = evaluate_batch(batch_params, policy)
    
    return {
        "uptake": UncertaintyResult(**raw_results["uptake"]),
        "welfare": UncertaintyResult(**raw_results["welfare"])
    }


def run_full_voi_analysis(
    base_params: ModelParameters,
    n_draws: int = 1000,
    seed: int = 20260303,
) -> dict[str, Any]:
    """
    Run comprehensive VOI analysis across all standard policies.
    """
    policies = get_standard_policies()
    policy_list = list(policies.values())
    
    key = jax.random.PRNGKey(seed)
    keys = jax.random.split(key, 3)
    
    d_elasticities = jax.random.uniform(keys[0], (n_draws,), minval=0.8, maxval=1.2) * float(base_params.deterrence_elasticity)
    m_effects = jax.random.uniform(keys[1], (n_draws,), minval=0.8, maxval=1.2) * float(base_params.moratorium_effect)
    
    def _to_batch(val):
        return jnp.full((n_draws,), float(val))

    batch_params = ModelParameters(
        jurisdiction=base_params.jurisdiction,
        calibration_date=base_params.calibration_date,
        baseline_testing_uptake=_to_batch(base_params.baseline_testing_uptake),
        deterrence_elasticity=d_elasticities,
        moratorium_effect=m_effects,
        adverse_selection_elasticity=_to_batch(base_params.adverse_selection_elasticity),
        demand_elasticity_high_risk=_to_batch(base_params.demand_elasticity_high_risk),
        baseline_loading=_to_batch(base_params.baseline_loading),
        family_history_sensitivity=_to_batch(base_params.family_history_sensitivity),
        proxy_substitution_rate=_to_batch(base_params.proxy_substitution_rate),
        pass_through_rate=_to_batch(base_params.pass_through_rate),
        research_participation_elasticity=_to_batch(base_params.research_participation_elasticity),
        research_participation_value=_to_batch(base_params.research_participation_value),
        ppp_conversion_factor=_to_batch(base_params.ppp_conversion_factor),
        equity_factor=_to_batch(base_params.equity_factor),
        high_sum_insured_share=_to_batch(base_params.high_sum_insured_share),
        taper_range=_to_batch(getattr(base_params, "taper_range", 0.0)),
        enforcement_effectiveness=_to_batch(base_params.enforcement_effectiveness),
        complaint_rate=_to_batch(base_params.complaint_rate),
        enforcement_budget=_to_batch(base_params.enforcement_budget),
        marginal_cost_enforcement=_to_batch(base_params.marginal_cost_enforcement),
        compliance_cost_fixed=_to_batch(base_params.compliance_cost_fixed),
        detection_prob_baseline=_to_batch(base_params.detection_prob_baseline),
        acc_deterrence_offset=_to_batch(base_params.acc_deterrence_offset),
        pharmac_qaly_threshold=_to_batch(base_params.pharmac_qaly_threshold),
        medicare_cost_share=_to_batch(base_params.medicare_cost_share),
        audit_intensity=_to_batch(base_params.audit_intensity),
        remoteness_weight=_to_batch(base_params.remoteness_weight),
    )
    
    welfare_matrix = []
    for p in policy_list:
        res = evaluate_batch(batch_params, p)
        welfare_matrix.append(res["raw_welfare"])
    
    w_matrix = jnp.stack(welfare_matrix)
    
    evpi = compute_evpi(w_matrix)
    evppi_deterrence = compute_evppi(w_matrix, d_elasticities)
    evppi_moratorium = compute_evppi(w_matrix, m_effects)
    
    return {
        "evpi": float(evpi),
        "evppi": {
            "Deterrence Elasticity": float(evppi_deterrence),
            "Moratorium Effect": float(evppi_moratorium)
        },
        "w_matrix": w_matrix
    }
