"""
Common reporting types and data structures.
"""

from __future__ import annotations

import jax
from dataclasses import dataclass
from typing import Any

from .dcba_ledger import DCBAResult


@dataclass(frozen=True)
class PolicyEvaluationResult:
    """
    Result from evaluating a single policy.
    Fields are Any to allow JAX tracers (BatchTracer) without Beartype violations.
    """

    policy_name: str
    jurisdiction: str
    testing_uptake: Any
    welfare_impact: Any
    equity_weighted_welfare: Any
    clinical_outcomes: dict[str, Any]
    insurance_premiums: dict[str, Any]
    compliance_rate: Any
    dcba_result: DCBAResult
    all_metrics: dict[str, Any]

    @property
    def research_participation(self) -> Any:
        """Helper for stress tests."""
        return self.all_metrics.get("data_quality", {}).get("participation_rate", 0.0)

    @property
    def proxy_effects(self) -> dict[str, Any]:
        """Backward compatibility alias for tests."""
        return self.all_metrics.get("proxy", {})


# Register PolicyEvaluationResult as a PyTree for JAX compatibility
jax.tree_util.register_pytree_node(
    PolicyEvaluationResult,
    lambda x: (
        (
            x.testing_uptake,
            x.welfare_impact,
            x.equity_weighted_welfare,
            x.compliance_rate,
            x.dcba_result,
            x.clinical_outcomes,
            x.insurance_premiums,
            x.all_metrics,
        ),
        (x.policy_name, x.jurisdiction),
    ),
    lambda aux, children: PolicyEvaluationResult(
        policy_name=aux[0],
        jurisdiction=aux[1],
        testing_uptake=children[0],
        welfare_impact=children[1],
        equity_weighted_welfare=children[2],
        compliance_rate=children[3],
        dcba_result=children[4],
        clinical_outcomes=children[5],
        insurance_premiums=children[6],
        all_metrics=children[7],
    ),
)
