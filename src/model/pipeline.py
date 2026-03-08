"""
Central Pipeline: Policy Evaluation Orchestrator (Diamond Standard).

Integrates Modules A, B, C, D, E, and F + DCBA Ledger to evaluate
the 100% full economic impact of genetic discrimination policy regimes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from jaxtyping import Array, Float
from loguru import logger

from . import dcba_ledger as dcba

# Import the FULL logic suite
from . import module_a_behavior as mod_a
from . import module_b_clinical as mod_b
from . import module_c_insurance_eq as mod_c
from . import module_d_proxy as mod_d
from . import module_enforcement as mod_e
from . import module_f_data_quality as mod_f
from .parameters import ModelParameters, PolicyConfig, get_default_parameters


@dataclass(frozen=True)
class PolicyEvaluationResult:
    """Consolidated results from a 100% full policy evaluation."""

    policy_name: str
    testing_uptake: Float[Array, ""]
    insurance_premiums: dict[str, float]
    data_quality: mod_f.DataQualityResult
    enforcement: Any
    proxy_effects: dict[str, float]
    dcba_result: dcba.DCBAResult
    clinical_outcomes: dict[str, Any]

    @property
    def welfare_impact(self) -> float:
        """The rigorous net welfare from the DCBA ledger."""
        return float(self.dcba_result.net_welfare)

    @property
    def compliance_rate(self) -> float:
        """Dynamic compliance rate from Module E."""
        return float(self.enforcement.compliance_rate)

    @property
    def research_participation(self) -> float:
        """Data quality from Module F."""
        return float(self.data_quality.participation_rate)

    @property
    def all_metrics(self) -> dict[str, Any]:
        """Full audit-ready metrics dictionary."""
        return {
            "welfare": {
                "net_welfare": float(self.dcba_result.net_welfare),
                "consumer_surplus": float(self.dcba_result.consumer_surplus),
                "producer_surplus": float(self.dcba_result.producer_surplus),
                "health_benefits": float(self.dcba_result.health_benefits),
                "fiscal_impact": float(self.dcba_result.fiscal_impact),
                "research_externalities": float(self.dcba_result.research_externalities),
            },
            "market": self.insurance_premiums,
            "compliance": {
                "rate": float(self.enforcement.compliance_rate),
                "expected_penalty": float(self.enforcement.expected_penalty),
            },
            "proxy": self.proxy_effects,
        }


def evaluate_single_policy(
    params: ModelParameters,
    policy: PolicyConfig,
    rng_key: Array | None = None,
) -> PolicyEvaluationResult:
    """
    Run the COMPLETE evaluation pipeline using the entire codebase.
    """
    logger.info(f"FULL EVALUATION: {policy.name} ({params.jurisdiction})")

    # Ensure float types for beartype/JAX
    p_params = params
    p_policy = policy

    # 1. Enforcement (Module E)
    enforcement = mod_e.compute_compliance_equilibrium(p_params, p_policy)

    # 2. Testing Uptake (Module A)
    testing_uptake = mod_a.compute_testing_uptake(p_params, p_policy, rng_key=rng_key)

    # 3. Insurance Equilibrium (Module C)
    market_eq = mod_c.compute_equilibrium(p_params, p_policy)

    # 4. Proxy Substitution (Module D)
    sq_policy = mod_a.get_standard_policies()["status_quo"]
    proxy_effects = mod_d.compute_proxy_substitution_effect(p_params, sq_policy, p_policy)

    # 5. Data Quality (Module F)
    data_quality = mod_f.compute_data_quality_externality(p_params, p_policy)

    # 6. Clinical Depth (Module B Restoration)
    clinical = mod_b.compute_clinical_outcomes(testing_uptake)

    # 7. DCBA Ledger
    dcba_res = dcba.compute_dcba(
        testing_uptake=testing_uptake,
        baseline_uptake=float(p_params.baseline_testing_uptake),
        insurance_premium=market_eq.premium_high,
        baseline_premium=0.2,
        insurer_profits=market_eq.insurer_profits,
        baseline_profits=0.05,
        research_value_loss=float(1.0 - data_quality.participation_rate) * p_params.research_participation_value,
        ppp_conversion_factor=float(p_params.ppp_conversion_factor),
        equity_factor=float(getattr(p_params, "equity_factor", 1.0)),
        value_per_qaly=float(getattr(p_params, "pharmac_qaly_threshold", 50000.0)),
    )

    logger.success(f"Full logic integration complete for {p_policy.name}")

    return PolicyEvaluationResult(
        policy_name=p_policy.name,
        testing_uptake=testing_uptake,
        insurance_premiums={
            "premium_high": float(market_eq.premium_high),
            "premium_low": float(market_eq.premium_low),
            "avg_premium": float(market_eq.premium_high + market_eq.premium_low) / 2.0,
            "risk_rating": float(market_eq.premium_high - market_eq.premium_low),
        },
        data_quality=data_quality,
        enforcement=enforcement,
        proxy_effects=proxy_effects,
        dcba_result=dcba_res,
        clinical_outcomes=clinical,
    )


def evaluate_policy_sweep(
    params: ModelParameters,
    policies: list[PolicyConfig] | None = None,
) -> dict[str, PolicyEvaluationResult]:
    """Evaluate a set of policies."""
    if policies is None:
        policies = list(get_standard_policies().values())
    return {p.name: evaluate_single_policy(params, p) for p in policies}


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
                    "uptake_delta": float(res.testing_uptake - base_res.testing_uptake),
                    "welfare_change": res.welfare_impact - base_res.welfare_impact,
                    "compliance_change": float(res.compliance_rate - base_res.compliance_rate),
                }
        return comparisons

    base_res = cast(PolicyEvaluationResult, baseline)
    reform_res = cast(PolicyEvaluationResult, reform)
    return {
        "uptake_delta": float(reform_res.testing_uptake - base_res.testing_uptake),
        "welfare_change": float(reform_res.welfare_impact - base_res.welfare_impact),
    }


def generate_policy_summary(result: Any) -> str:
    """Generate summary string for a policy evaluation."""
    if isinstance(result, dict):
        typed_dict = cast(dict[str, PolicyEvaluationResult], result)
        summary_lines = []
        for name, res in typed_dict.items():
            summary_lines.append(f"Policy: {name}")
            summary_lines.append(f"Uptake: {float(res.testing_uptake):.2%}")
            summary_lines.append(f"Welfare: {res.welfare_impact}")
        return "\n".join(summary_lines)

    typed_res = cast(PolicyEvaluationResult, result)
    return f"Policy: {typed_res.policy_name}\nUptake: {float(typed_res.testing_uptake):.2%}\nWelfare: {typed_res.welfare_impact}"


def get_standard_policies() -> dict[str, PolicyConfig]:
    return mod_a.get_standard_policies()


def run_full_evaluation(
    params: ModelParameters | None = None,
    policies: list[PolicyConfig] | None = None,
) -> dict[str, PolicyEvaluationResult]:
    if params is None:
        params = get_default_parameters()
    return evaluate_policy_sweep(params, policies)
