"""
Integrated policy evaluation pipeline.

Integrates all modules (A, C, D, E, F, Enforcement) into unified pipeline
for policy evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax.random as jr
from jaxtyping import Array, Float
from loguru import logger

from .module_a_behavior import (
    compute_testing_uptake,
    get_standard_policies,
)
from .module_c_insurance_eq import (
    compute_equilibrium as insurance_equilibrium,
)
from .module_c_insurance_eq import (
    get_standard_risk_parameters,
)
from .module_enforcement import (
    compute_compliance_equilibrium,
)
from .module_f_data_quality import (
    compute_participation_rate,
)
from .parameters import HyperParameters, ModelParameters, PolicyConfig
from .rng import RNGManager


@dataclass
class PolicyEvaluationResult:
    """
    Comprehensive policy evaluation results.

    Attributes:
        policy_name: Name of policy evaluated
        testing_uptake: Testing uptake rate
        insurance_premiums: Dictionary with premium metrics
        welfare_impact: Net welfare impact
        compliance_rate: Insurer compliance rate
        research_participation: Research participation rate
        all_metrics: Dictionary with all computed metrics
    """

    policy_name: str
    testing_uptake: Float[Array, ""]
    insurance_premiums: dict[str, Float[Array, ""]]
    welfare_impact: Float[Array, ""]
    compliance_rate: Float[Array, ""]
    research_participation: Float[Array, ""]
    all_metrics: dict[str, Any]


def evaluate_single_policy(
    params: ModelParameters,
    policy: PolicyConfig,
    rng_key: Array | None = None,
) -> PolicyEvaluationResult:
    """
    Evaluate single policy across all modules.

    Args:
        params: Model parameters
        policy: Policy configuration
        rng_key: Optional RNG key

    Returns:
        PolicyEvaluationResult object
    """
    logger.info(f"Evaluating policy: {policy.name}")

    # =========================================================================
    # Module A: Behavior / Deterrence
    # =========================================================================
    testing_uptake = compute_testing_uptake(params, policy, rng_key=rng_key)
    logger.debug(f"Testing uptake: {float(testing_uptake):.1%}")

    # =========================================================================
    # Module C: Insurance Equilibrium
    # =========================================================================
    risk_params = get_standard_risk_parameters()
    insurance_eq = insurance_equilibrium(
        params,
        policy,
        risk_high=risk_params["risk_high"],
        risk_low=risk_params["risk_low"],
        proportion_high=risk_params["proportion_high"],
    )

    insurance_premiums = {
        "premium_high_risk": insurance_eq.premium_high_risk,
        "premium_low_risk": insurance_eq.premium_low_risk,
        "avg_premium": (insurance_eq.premium_high_risk + insurance_eq.premium_low_risk) / 2,
        "risk_rating": insurance_eq.premium_high_risk - insurance_eq.premium_low_risk,
        "uninsured_rate": insurance_eq.uninsured_rate,
    }
    logger.debug(f"Average premium: {float(insurance_premiums['avg_premium']):.3f}")

    # =========================================================================
    # Module D: Proxy Substitution (simplified)
    # =========================================================================
    # Full implementation would require training data
    proxy_metrics = {
        "substitution_rate": params.proxy_substitution_rate,
        "family_history_sensitivity": params.family_history_sensitivity,
    }

    # =========================================================================
    # Enforcement
    # =========================================================================
    compliance_outcome = compute_compliance_equilibrium(params, policy)
    logger.debug(f"Compliance rate: {float(compliance_outcome.compliance_rate):.1%}")

    # =========================================================================
    # Module F: Data Quality
    # =========================================================================
    research_participation = compute_participation_rate(params, policy, rng_key=rng_key)

    # =========================================================================
    # Welfare Aggregation (simplified DCBA ledger)
    # =========================================================================
    # Welfare = Testing benefits + Insurance consumer surplus - Costs

    # Testing benefits (more testing → more health benefits)
    testing_benefit = testing_uptake * 100  # Simplified: 100 QALYs per tester

    # Insurance consumer surplus (lower premiums → higher surplus)
    avg_premium = insurance_premiums["avg_premium"]
    consumer_surplus = (1.0 - avg_premium) * 50  # Simplified

    # Compliance costs (higher compliance → higher administrative costs)
    compliance_cost = compliance_outcome.compliance_rate * 10

    # Net welfare
    welfare_impact = testing_benefit + consumer_surplus - compliance_cost
    logger.info(f"Net welfare impact for {policy.name}: {float(welfare_impact):.2f}")

    # =========================================================================
    # Aggregate all metrics
    # =========================================================================
    all_metrics = {
        "testing_uptake": testing_uptake,
        "insurance": insurance_premiums,
        "proxy": proxy_metrics,
        "enforcement": {
            "compliance_rate": compliance_outcome.compliance_rate,
            "violation_rate": compliance_outcome.violation_rate,
            "detection_rate": compliance_outcome.detection_rate,
        },
        "data_quality": {
            "research_participation": research_participation,
        },
        "welfare": {
            "testing_benefit": testing_benefit,
            "consumer_surplus": consumer_surplus,
            "compliance_cost": compliance_cost,
            "net_welfare": welfare_impact,
        },
    }

    return PolicyEvaluationResult(
        policy_name=policy.name,
        testing_uptake=testing_uptake,
        insurance_premiums=insurance_premiums,
        welfare_impact=welfare_impact,
        compliance_rate=compliance_outcome.compliance_rate,
        research_participation=research_participation,
        all_metrics=all_metrics,
    )


def evaluate_policy_sweep(
    params: ModelParameters,
    policies: list[PolicyConfig] | None = None,
    hyper_params: HyperParameters | None = None,
) -> dict[str, PolicyEvaluationResult]:
    """
    Evaluate multiple policies (policy sweep).

    Args:
        params: Model parameters
        policies: List of policies to evaluate (uses standard policies if None)
        hyper_params: Hyperparameters

    Returns:
        Dictionary mapping policy name to evaluation result
    """
    if policies is None:
        policies_dict = get_standard_policies()
        policies = list(policies_dict.values())

    if hyper_params is None:
        hyper_params = HyperParameters()

    # Initialize RNG
    rng = RNGManager(base_key=jr.PRNGKey(hyper_params.random_seed))

    # Evaluate each policy
    results = {}
    for policy in policies:
        policy_key = rng.get_key(f"policy_{policy.name}")
        result = evaluate_single_policy(params, policy, rng_key=policy_key)
        results[policy.name] = result

    return results


def compare_policies(
    results: dict[str, PolicyEvaluationResult],
    baseline_name: str = "status_quo",
) -> dict[str, dict[str, Float[Array, ""]]]:
    """
    Compare policies against baseline.

    Args:
        results: Dictionary of evaluation results
        baseline_name: Name of baseline policy

    Returns:
        Dictionary with comparative metrics
    """
    if baseline_name not in results:
        raise ValueError(f"Baseline policy '{baseline_name}' not found in results")

    baseline = results[baseline_name]
    comparisons = {}

    for policy_name, result in results.items():
        if policy_name == baseline_name:
            continue

        comparisons[policy_name] = {
            "testing_uptake_change": result.testing_uptake - baseline.testing_uptake,
            "welfare_change": result.welfare_impact - baseline.welfare_impact,
            "premium_change": (
                result.insurance_premiums["avg_premium"]
                - baseline.insurance_premiums["avg_premium"]
            ),
            "compliance_change": (result.compliance_rate - baseline.compliance_rate),
        }

    return comparisons


def generate_policy_summary(
    results: dict[str, PolicyEvaluationResult],
) -> str:
    """
    Generate human-readable policy summary.

    Args:
        results: Dictionary of evaluation results

    Returns:
        Formatted summary string
    """
    lines = []
    lines.append("=" * 80)
    lines.append("POLICY EVALUATION SUMMARY")
    lines.append("=" * 80)
    lines.append("")

    for policy_name, result in results.items():
        lines.append(f"Policy: {policy_name}")
        lines.append("-" * 40)
        lines.append(f"Testing Uptake: {result.testing_uptake:.1%}")
        lines.append(f"Average Premium: {result.insurance_premiums['avg_premium']:.3f}")
        lines.append(f"Risk Rating: {result.insurance_premiums['risk_rating']:.3f}")
        lines.append(f"Compliance Rate: {result.compliance_rate:.1%}")
        lines.append(f"Research Participation: {result.research_participation:.1%}")
        lines.append(f"Net Welfare Impact: {result.welfare_impact:.2f}")
        lines.append("")

    # Compare policies
    if len(results) > 1:
        lines.append("=" * 80)
        lines.append("POLICY COMPARISONS")
        lines.append("=" * 80)
        lines.append("")

        comparisons = compare_policies(results)

        for policy_name, metrics in comparisons.items():
            lines.append(f"{policy_name} vs Status Quo:")
            lines.append(f"  Testing Uptake Change: {metrics['testing_uptake_change']:+.1%}")
            lines.append(f"  Welfare Change: {metrics['welfare_change']:+.2f}")
            lines.append(f"  Premium Change: {metrics['premium_change']:+.3f}")
            lines.append("")

    return "\n".join(lines)


# Convenience function
def run_full_evaluation(
    params: ModelParameters | None = None,
    hyper_params: HyperParameters | None = None,
) -> dict[str, PolicyEvaluationResult]:
    """
    Run full policy evaluation with default parameters.

    Args:
        params: Model parameters (uses defaults if None)
        hyper_params: Hyperparameters (uses defaults if None)

    Returns:
        Dictionary of evaluation results
    """
    if params is None:
        params = ModelParameters()

    if hyper_params is None:
        hyper_params = HyperParameters()

    # Evaluate all standard policies
    results = evaluate_policy_sweep(params, hyper_params=hyper_params)

    # Print summary
    generate_policy_summary(results)
    logger.info("Policy evaluation summary generated")

    return results
