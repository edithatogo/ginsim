"""
Unified Sensitivity Engine (Diamond Standard).

Consolidates JAX-vectorized DSA, PSA, and Sobol analysis for
high-performance uncertainty quantification.
Now integrated with Bayesian Prior Grounding (Track 0039).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
from jax import jit, vmap
from jaxtyping import Array

from src.inference.priors import sample_parameter_matrix

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
        "samples": results[:n_subsamples],
    }


def evaluate_core_numerical(params: ModelParameters, policy: PolicyConfig) -> dict[str, Array]:
    """
    JIT-compatible numerical kernel that returns only arrays.
    """
    # Use global evaluate_single_policy but extract only numbers
    res = evaluate_single_policy(params, policy)
    return {
        "uptake": res.testing_uptake,
        "welfare": res.welfare_impact,
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
        "raw_welfare": results["welfare"],
    }


def run_psa(
    base_params: ModelParameters,
    policy: PolicyConfig,
    n_draws: int = 1000,
    seed: int = 20260303,
) -> dict[str, UncertaintyResult]:
    """
    Run Probabilistic Sensitivity Analysis (PSA) using Bayesian Priors.
    """
    key = jax.random.PRNGKey(seed)

    # 1. Generate parameter matrix from GROUNDED PRIORS (No more uniform jitter)
    prior_draws = sample_parameter_matrix(key, n_draws, base_params.jurisdiction)

    def _to_batch(val):
        return jnp.full((n_draws,), float(val))

    # 2. Build the vectorized parameter tree
    batch_params = ModelParameters(
        jurisdiction=base_params.jurisdiction,
        calibration_date=base_params.calibration_date,
        baseline_testing_uptake=_to_batch(base_params.baseline_testing_uptake),
        # Bayesian Varied Fields
        deterrence_elasticity=prior_draws["deterrence_elasticity"],
        adverse_selection_elasticity=-prior_draws[
            "adverse_selection_elasticity"
        ],  # Negative by convention
        equity_factor=prior_draws["equity_factor"],
        # Constants
        moratorium_effect=_to_batch(base_params.moratorium_effect),
        demand_elasticity_high_risk=_to_batch(base_params.demand_elasticity_high_risk),
        baseline_loading=_to_batch(base_params.baseline_loading),
        family_history_sensitivity=_to_batch(base_params.family_history_sensitivity),
        proxy_substitution_rate=_to_batch(base_params.proxy_substitution_rate),
        pass_through_rate=_to_batch(base_params.pass_through_rate),
        research_participation_elasticity=_to_batch(base_params.research_participation_elasticity),
        research_participation_value=_to_batch(base_params.research_participation_value),
        ppp_conversion_factor=_to_batch(base_params.ppp_conversion_factor),
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
        audit_intensity_apra=_to_batch(getattr(base_params, "audit_intensity_apra", 0.50)),
        audit_intensity_asic=_to_batch(getattr(base_params, "audit_intensity_asic", 0.50)),
        remoteness_weight=_to_batch(base_params.remoteness_weight),
    )

    raw_results = evaluate_batch(batch_params, policy)

    return {
        "uptake": UncertaintyResult(**raw_results["uptake"]),
        "welfare": UncertaintyResult(**raw_results["welfare"]),
    }


def run_full_voi_analysis(
    base_params: ModelParameters,
    n_draws: int = 1000,
    seed: int = 20260303,
) -> dict[str, Any]:
    """
    Run comprehensive VOI analysis using Bayesian Priors.
    """
    policies = get_standard_policies()
    policy_list = list(policies.values())

    key = jax.random.PRNGKey(seed)
    prior_draws = sample_parameter_matrix(key, n_draws, base_params.jurisdiction)

    def _to_batch(val):
        return jnp.full((n_draws,), float(val))

    batch_params = ModelParameters(
        jurisdiction=base_params.jurisdiction,
        calibration_date=base_params.calibration_date,
        baseline_testing_uptake=_to_batch(base_params.baseline_testing_uptake),
        deterrence_elasticity=prior_draws["deterrence_elasticity"],
        adverse_selection_elasticity=-prior_draws["adverse_selection_elasticity"],
        equity_factor=prior_draws["equity_factor"],
        moratorium_effect=_to_batch(base_params.moratorium_effect),
        demand_elasticity_high_risk=_to_batch(base_params.demand_elasticity_high_risk),
        baseline_loading=_to_batch(base_params.baseline_loading),
        family_history_sensitivity=_to_batch(base_params.family_history_sensitivity),
        proxy_substitution_rate=_to_batch(base_params.proxy_substitution_rate),
        pass_through_rate=_to_batch(base_params.pass_through_rate),
        research_participation_elasticity=_to_batch(base_params.research_participation_elasticity),
        research_participation_value=_to_batch(base_params.research_participation_value),
        ppp_conversion_factor=_to_batch(base_params.ppp_conversion_factor),
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
        audit_intensity_apra=_to_batch(getattr(base_params, "audit_intensity_apra", 0.50)),
        audit_intensity_asic=_to_batch(getattr(base_params, "audit_intensity_asic", 0.50)),
        remoteness_weight=_to_batch(base_params.remoteness_weight),
    )

    welfare_matrix = []
    for p in policy_list:
        res = evaluate_batch(batch_params, p)
        welfare_matrix.append(res["raw_welfare"])

    w_matrix = jnp.stack(welfare_matrix)

    evpi = compute_evpi(w_matrix)
    evppi_deterrence = compute_evppi(w_matrix, prior_draws["deterrence_elasticity"])
    evppi_as = compute_evppi(w_matrix, prior_draws["adverse_selection_elasticity"])

    return {
        "evpi": float(evpi),
        "evppi": {
            "Deterrence Elasticity": float(evppi_deterrence),
            "Adverse Selection": float(evppi_as),
        },
        "w_matrix": w_matrix,
    }
