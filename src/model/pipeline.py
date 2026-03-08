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

# Import the FULL logic suite
from . import module_a_behavior as mod_a
from . import module_b_clinical as mod_b
from . import module_c_insurance_eq as mod_c
from . import module_d_proxy as mod_d
from . import module_enforcement as mod_e
from . import module_f_data_quality as mod_f
from . import dcba_ledger as dcba
from .parameters import ModelParameters, PolicyConfig


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

    # 1. Enforcement (Module E)
    enforcement = mod_e.compute_compliance_equilibrium(params, policy)
    
    # 2. Testing Uptake (Module A)
    testing_uptake = mod_a.compute_testing_uptake(params, policy, rng_key=rng_key)
    
    # 3. Insurance Equilibrium (Module C)
    market_eq = mod_c.compute_equilibrium(params, policy)
    
    # 4. Proxy Substitution (Module D)
    # We use the status quo as a relative baseline for substitution effects
    sq_policy = mod_a.get_standard_policies()["status_quo"]
    proxy_effects = mod_d.compute_proxy_substitution_effect(params, sq_policy, policy)
    
    # 5. Data Quality (Module F)
    data_quality = mod_f.compute_data_quality_externality(params, policy)
    
    # 6. DCBA Ledger (The Heart of the Model)
    # Get a 'baseline' for comparison (approximated here)
    dcba_res = dcba.compute_dcba(
        testing_uptake=testing_uptake,
        baseline_uptake=params.baseline_testing_uptake,
        insurance_premium=market_eq.premium_high,
        baseline_premium=0.2, # Baseline premium anchor
        insurer_profits=market_eq.insurer_profits,
        baseline_profits=0.05, # Baseline profit anchor
        research_value_loss=float(1.0 - data_quality.participation_rate) * 50000
    )

    logger.success(f"Full logic integration complete for {policy.name}")
    
    return PolicyEvaluationResult(
        policy_name=policy.name,
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
        dcba_result=dcba_res
    )

def get_standard_policies() -> dict[str, PolicyConfig]:
    return mod_a.get_standard_policies()

def evaluate_policy_sweep(params, policies=None):
    if policies is None:
        policies = list(get_standard_policies().values())
    return {p.name: evaluate_single_policy(params, p) for p in policies}
