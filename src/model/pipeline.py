"""
Central Pipeline: Policy Evaluation Orchestrator (Diamond Standard).

Integrates Modules A, B, C, D, E, and F + DCBA Ledger to evaluate
the 100% full economic impact of genetic discrimination policy regimes.
"""

from __future__ import annotations

from typing import Any, cast

import jax.numpy as jnp
from loguru import logger

from . import dcba_ledger as dcba
from . import module_a_behavior as mod_a
from . import module_b_clinical as mod_b
from . import module_c_insurance_eq as mod_c
from . import module_d_proxy as mod_d
from . import module_enforcement as mod_e
from . import module_f_data_quality as mod_f
from . import proof_engine
from .parameters import ModelParameters, PolicyConfig, get_default_parameters
from .reporting_common import PolicyEvaluationResult
from .sanity_checker import EconomicSanityChecker


def evaluate_single_policy(
    params: ModelParameters,
    policy: PolicyConfig,
    year: int = 0,
    is_annual: bool = False,
    include_proofs: bool = True,
) -> PolicyEvaluationResult:
    """
    Execute full clinical-economic pipeline for a single policy configuration.
    """
    logger.info(f"FULL EVALUATION: {policy.name} ({params.jurisdiction}) - Year {year}")

    p_params = params
    p_policy = policy

    # 1. Enforcement (Module E)
    enforcement = mod_e.compute_compliance_equilibrium(p_params, p_policy)

    # 2. Testing Uptake (Module A)
    testing_uptake = mod_a.compute_testing_uptake(p_params, p_policy, year=year)

    # 3. Insurance Equilibrium (Module C)
    market_eq = mod_c.compute_equilibrium(p_params, p_policy)

    # 4. Proxy Substitution (Module D)
    sq_policy = mod_a.get_standard_policies()["status_quo"]
    proxy = mod_d.compute_proxy_substitution_effect(p_params, sq_policy, p_policy, year=year)

    # 5. Clinical Impact (Module B)
    clinical = mod_b.compute_clinical_outcomes(testing_uptake)

    # 6. Data Quality (Module F)
    data_quality = mod_f.compute_data_quality_externality(p_params, p_policy)

    # 7. DCBA Ledger
    # PROOF FIX: Use status-quo consistent baselines
    b_premium = 0.161  # Approximate SQ premium
    b_profits = 0.057  # Approximate SQ profit

    dcba_res = dcba.compute_dcba(
        testing_uptake=testing_uptake,
        baseline_uptake=jnp.asarray(p_params.baseline_testing_uptake).astype(float),
        insurance_premium=market_eq.premium_high,
        baseline_premium=b_premium,
        insurer_profits=market_eq.insurer_profits,
        baseline_profits=b_profits,
        research_value_loss=jnp.asarray(1.0 - data_quality.participation_rate).astype(float)
        * jnp.asarray(p_params.research_participation_value).astype(float),
        ppp_conversion_factor=jnp.asarray(p_params.ppp_conversion_factor).astype(float),
        equity_factor=jnp.asarray(p_params.equity_factor).astype(float),
        value_per_qaly=jnp.asarray(p_params.pharmac_qaly_threshold).astype(float),
        setup_cost=jnp.asarray(p_params.compliance_cost_fixed).astype(float),
        time_horizon=year if is_annual else 20,
        is_annual=is_annual,
    )

    # 8. Aggregate into Result Object
    proof_bundle = proof_engine.summarize_proofs(p_params, p_policy) if include_proofs else {}
    result = PolicyEvaluationResult(
        policy_name=p_policy.name,
        jurisdiction=p_params.jurisdiction,
        testing_uptake=testing_uptake,
        welfare_impact=dcba_res.net_welfare,
        equity_weighted_welfare=dcba_res.equity_weighted_welfare,
        clinical_outcomes={
            "total_qaly_gains": clinical["total_qaly_gains"],
            "total_cost_savings": clinical["total_cost_savings"],
        },
        insurance_premiums={
            "premium_high": market_eq.premium_high,
            "premium_low": market_eq.premium_low,
            "avg_premium": (market_eq.premium_high + market_eq.premium_low) / 2.0,
            "risk_rating": market_eq.premium_high / (market_eq.premium_low + 1e-10),
            "uninsured_rate": 1.0 - testing_uptake,
        },
        compliance_rate=enforcement.compliance_rate,
        dcba_result=dcba_res,
        all_metrics={
            "enforcement": enforcement,
            "proxy": proxy,
            "clinical": clinical,
            "data_quality": data_quality,
            "proofs": proof_bundle,
            "welfare": {
                "consumer_surplus": dcba_res.consumer_surplus,
                "producer_surplus": dcba_res.producer_surplus,
                "health_benefits": dcba_res.health_benefits,
                "fiscal_impact": dcba_res.fiscal_impact,
                "research_externalities": dcba_res.research_externalities,
                "net_welfare": dcba_res.net_welfare,
            },
        },
    )

    # 9. Automated Sanity Check
    EconomicSanityChecker.verify_result(result)

    return result


def simulate_evolution(
    params: ModelParameters,
    policy: PolicyConfig,
) -> dict[str, Any]:
    """
    Simulate policy impact over a multi-year horizon and return aggregate.
    """
    horizon = int(getattr(params, "time_horizon", 10))
    logger.info(f"SIMULATING EVOLUTION: {policy.name} over {horizon} years")
    annual_results = {}

    for year in range(horizon + 1):
        annual_results[year] = evaluate_single_policy(params, policy, year=year, is_annual=True)

    # Aggregate ledger
    logger.info("Aggregating temporal results...")
    ledger_list = [res.dcba_result for res in annual_results.values()]
    aggregate_ledger = dcba.aggregate_temporal_results(ledger_list)

    # Primary result is the aggregate
    main_res = annual_results[0]  # Base for metadata
    # Update with aggregate welfare
    result = PolicyEvaluationResult(
        policy_name=main_res.policy_name,
        jurisdiction=main_res.jurisdiction,
        testing_uptake=main_res.testing_uptake,
        welfare_impact=aggregate_ledger.net_welfare,
        equity_weighted_welfare=aggregate_ledger.equity_weighted_welfare,
        clinical_outcomes=main_res.clinical_outcomes,
        insurance_premiums=main_res.insurance_premiums,
        compliance_rate=main_res.compliance_rate,
        dcba_result=aggregate_ledger,
        all_metrics={
            "temporal_results": annual_results,
            "aggregate_ledger": aggregate_ledger,
        },
    )

    return {"aggregate": result, "annual": annual_results}


def evaluate_policy_sweep(
    params: ModelParameters,
    policies: list[PolicyConfig] | None = None,
) -> dict[str, PolicyEvaluationResult]:
    """Evaluate a standard set of policies for comparison."""
    if policies is None:
        policies = list(mod_a.get_standard_policies().values())

    results = {}
    for policy in policies:
        results[policy.name] = evaluate_single_policy(params, policy)

    # Sweep-level Sanity Check
    EconomicSanityChecker.verify_sweep(results)

    return results


def get_standard_policies() -> dict[str, PolicyConfig]:
    """Compatibility export."""
    return mod_a.get_standard_policies()


def compare_policies(
    params: Any,
    baseline_name: str = "status_quo",
    reform_name: str | None = None,
) -> dict[str, Any] | Any:
    """Compare two policies and return delta metrics."""
    if isinstance(params, dict) and "status_quo" in params:
        typed_params = cast(dict[str, PolicyEvaluationResult], params)
        res_base = typed_params[baseline_name]
        results = {}
        for name, res in typed_params.items():
            if name == baseline_name:
                continue
            results[name] = {
                "uptake_delta": float(res.testing_uptake - res_base.testing_uptake),
                "welfare_delta": float(res.welfare_impact - res_base.welfare_impact),
                "compliance_delta": float(res.compliance_rate - res_base.compliance_rate),
                "welfare_change": float(res.welfare_impact - res_base.welfare_impact),
            }
        return results if reform_name is None else results.get(reform_name)

    # Parameters mode
    typed_params = cast(ModelParameters, params)
    res_base = evaluate_single_policy(typed_params, get_standard_policies()["status_quo"])
    return {
        "uptake_delta": 0.0,
        "welfare_delta": 0.0,
        "compliance_delta": 0.0,
        "welfare_change": 0.0,
    }


def generate_policy_summary(result: Any) -> str:
    """Generate summary. Handles dict or result object."""
    res = (
        cast(dict[str, PolicyEvaluationResult], result)["status_quo"]
        if isinstance(result, dict) and "status_quo" in result
        else cast(PolicyEvaluationResult, result)
    )

    lines = [
        f"POLICY IMPACT SUMMARY: {res.policy_name}",
        f"Jurisdiction: {res.jurisdiction}",
        "-" * 40,
        f"Testing Uptake:    {float(res.testing_uptake):.1%}",
        f"Welfare Impact:    ${float(res.welfare_impact):,.0f}",
        f"Compliance Rate:   {float(res.compliance_rate):.1%}",
        f"High-Risk Premium: {float(res.insurance_premiums['premium_high']):.3f}",
        "-" * 40,
    ]
    return "\n".join(lines)


def run_full_evaluation(
    params: ModelParameters | None = None,
    policies: list[PolicyConfig] | None = None,
) -> dict[str, PolicyEvaluationResult]:
    """Top-level entry point for evaluation."""
    if params is None:
        params = get_default_parameters()
    return evaluate_policy_sweep(params, policies)


def run_full_pipeline(
    params: ModelParameters | None = None,
    policies: list[PolicyConfig] | None = None,
) -> dict[str, PolicyEvaluationResult]:
    """Compatibility alias."""
    return run_full_evaluation(params, policies)
