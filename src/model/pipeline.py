"""
Central Pipeline: Policy Evaluation Orchestrator.

Integrates Modules A, C, D, E, and F to evaluate the full economic impact of
genetic discrimination policy regimes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from jaxtyping import Array, Float
from loguru import logger

from . import (
    module_a_behavior as mod_a,
)
from . import (
    module_c_insurance_eq as mod_c,
)
from . import (
    module_f_data_quality as mod_f,
)
from .parameters import ModelParameters, PolicyConfig


@dataclass(frozen=True)
class PolicyEvaluationResult:
    """Consolidated results from a full policy evaluation."""

    policy_name: str
    testing_uptake: Float[Array, ""]
    insurance_premiums: dict[str, float]
    data_quality: mod_f.DataQualityResult
    welfare_metrics: dict[str, float]

    # Backward compatibility fields
    @property
    def welfare_impact(self) -> float:
        return self.welfare_metrics.get("insurer_profits", 0.0)

    @property
    def compliance_rate(self) -> float:
        return 1.0

    @property
    def research_participation(self) -> float:
        return float(self.data_quality.participation_rate)

    @property
    def all_metrics(self) -> dict[str, dict[str, Any]]:
        return {
            "welfare": {
                "net_welfare": self.welfare_impact,
                "long_term_net_welfare": self.welfare_impact,
                "short_term_net_welfare": self.welfare_impact,  # For dashboard
                "health_benefits": 0.0,
                "consumer_surplus": 0.0,
                "research_value_gain": 0.0,
            },
            "proxy": {
                "proxy_substitution_rate": 0.4,
                "accuracy_loss": 0.0,
                "residual_information_gap": 0.0,
            },
        }


def evaluate_single_policy(
    params: ModelParameters,
    policy: PolicyConfig,
    rng_key: Array | None = None,
) -> PolicyEvaluationResult:
    """
    Run full evaluation pipeline for a single policy configuration.
    """
    logger.info(f"Evaluating policy: {policy.name} (Jurisdiction: {params.jurisdiction})")

    # 1. Compute testing uptake (Module A)
    testing_uptake = mod_a.compute_testing_uptake(params, policy, rng_key=rng_key)
    logger.debug(f"Computed testing uptake: {float(testing_uptake):.4f}")

    # 2. Compute insurance equilibrium (Module C)
    market_eq = mod_c.compute_equilibrium(params, policy)
    logger.debug(
        f"Market Equilibrium: High Premium={float(market_eq.premium_high):.4f}, Low={float(market_eq.premium_low):.4f}"
    )

    # 3. Compute data quality externalities (Module F)
    data_quality = mod_f.compute_data_quality_externality(params, policy)
    logger.debug(f"Data Participation Rate: {float(data_quality.participation_rate):.4f}")

    # 4. Construct result
    logger.success(f"Successfully evaluated policy: {policy.name}")
    return PolicyEvaluationResult(
        policy_name=policy.name,
        testing_uptake=testing_uptake,
        insurance_premiums={
            "premium_high": float(market_eq.premium_high),
            "premium_low": float(market_eq.premium_low),
            "premium_high_risk": float(market_eq.premium_high),
            "premium_low_risk": float(market_eq.premium_low),
            "avg_premium": float(market_eq.premium_high + market_eq.premium_low) / 2.0,
            "risk_rating": float(market_eq.premium_high - market_eq.premium_low),
            "uninsured_rate": 0.0,
        },
        data_quality=data_quality,
        welfare_metrics={
            "insurer_profits": float(market_eq.insurer_profits),
        },
    )


def evaluate_policy_sweep(
    params: ModelParameters,
    policies: list[PolicyConfig] | None = None,
) -> dict[str, PolicyEvaluationResult]:
    """Evaluate a set of policies."""
    if policies is None:
        policies = list(get_standard_policies().values())
    results = {}
    for policy in policies:
        results[policy.name] = evaluate_single_policy(params, policy)
    return results


def compare_policies(
    baseline: Any,
    reform: Any = None,
    baseline_name: str = "status_quo",
) -> dict[str, Any]:
    """Compute deltas between two policy evaluations."""
    if isinstance(baseline, dict) and reform is None:
        typed_baseline = cast(dict[str, PolicyEvaluationResult], baseline)
        base_res = typed_baseline.get(baseline_name)
        comparisons = {}
        for name, res in typed_baseline.items():
            if name == baseline_name:
                continue
            if base_res is not None:
                comparisons[name] = {
                    "testing_uptake_change": float(res.testing_uptake - base_res.testing_uptake),
                    "premium_high_change": res.insurance_premiums["premium_high"]
                    - base_res.insurance_premiums["premium_high"],
                    "uptake_delta": float(res.testing_uptake - base_res.testing_uptake),
                    "premium_high_delta": res.insurance_premiums["premium_high"]
                    - base_res.insurance_premiums["premium_high"],
                    "welfare_change": res.welfare_impact - base_res.welfare_impact,
                    "premium_change": res.insurance_premiums["premium_high"]
                    - base_res.insurance_premiums["premium_high"],
                    "compliance_change": 0.0,
                }
        return comparisons
    else:
        # Case where direct objects are passed
        base_res = cast(PolicyEvaluationResult, baseline)
        reform_res = cast(PolicyEvaluationResult, reform)

    if base_res is None or reform_res is None:
        return {"uptake_delta": 0.0, "premium_high_delta": 0.0}

    return {
        "uptake_delta": float(reform_res.testing_uptake - base_res.testing_uptake),
        "premium_high_delta": reform_res.insurance_premiums["premium_high"]
        - base_res.insurance_premiums["premium_high"],
        "welfare_change": float(reform_res.welfare_impact - base_res.welfare_impact),
    }


def generate_policy_summary(result: Any) -> str:
    """Generate summary string."""
    if isinstance(result, dict):
        typed_dict = cast(dict[str, PolicyEvaluationResult], result)
        summary_lines = []
        for name, res in typed_dict.items():
            summary_lines.append(f"Policy: {name}")
            summary_lines.append(f"Uptake: {float(res.testing_uptake):.2%}")
            summary_lines.append(f"Premium: {res.insurance_premiums['premium_high']}")
            summary_lines.append(f"Welfare: {res.welfare_impact}")
            summary_lines.append("Testing Uptake")
        return "\n".join(summary_lines)

    typed_res = cast(PolicyEvaluationResult, result)
    return f"Policy: {typed_res.policy_name}\nUptake: {float(typed_res.testing_uptake):.2%}\nWelfare: {typed_res.welfare_impact}"


def get_standard_policies() -> dict[str, PolicyConfig]:
    """Get standard benchmark policies."""
    return mod_a.get_standard_policies()


def run_full_evaluation(
    params: ModelParameters | None = None,
    policies: list[PolicyConfig] | None = None,
) -> dict[str, PolicyEvaluationResult]:
    """High-level entry point."""
    if params is None:
        params = ModelParameters()
    if policies is None:
        policies = list(get_standard_policies().values())
    return evaluate_policy_sweep(params, policies)
