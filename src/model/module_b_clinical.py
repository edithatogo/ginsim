"""
Module B: Clinical prevention and outcomes (Diamond Standard Upgrade).

Implements disease-specific microsimulation logic to ground QALY gains in
empirical clinical cohorts (e.g., BRCA, Lynch Syndrome).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
from jax import jit
from jaxtyping import Array, Float


@dataclass(frozen=True)
class DiseaseCohort:
    """Represents a specific genetic condition cohort."""
    name: str
    prevalence: Any
    baseline_risk: Any
    prevention_efficacy: Any
    qaly_loss_per_event: Any
    cost_per_event: Any

# Register PyTree for JAX compatibility
jax.tree_util.register_pytree_node(
    DiseaseCohort,
    lambda x: ((x.prevalence, x.baseline_risk, x.prevention_efficacy, x.qaly_loss_per_event, x.cost_per_event), (x.name,)),
    lambda aux, children: DiseaseCohort(aux[0], *children)
)

@jit
def simulate_cohort_outcomes(
    uptake: Float[Array, ""],
    cohort: DiseaseCohort,
) -> dict[str, Float[Array, ""]]:
    """
    Simulate outcomes for a specific disease cohort.
    """
    # Effective prevention: uptake * efficacy in the prevalent population
    events_prevented = uptake * cohort.prevalence * cohort.baseline_risk * cohort.prevention_efficacy
    
    qaly_gains = events_prevented * cohort.qaly_loss_per_event
    cost_savings = events_prevented * cohort.cost_per_event
    
    return {
        "events_prevented": events_prevented,
        "qaly_gains": qaly_gains,
        "cost_savings": cost_savings
    }

def get_standard_cohorts() -> list[DiseaseCohort]:
    """Get high-impact clinical cohorts for simulation."""
    return [
        DiseaseCohort("BRCA1/2 (HBOC)", float(0.0025), float(0.60), float(0.50), float(5.0), float(80000.0)),
        DiseaseCohort("Lynch Syndrome (CRC)", float(0.0035), float(0.40), float(0.60), float(4.0), float(65000.0)),
        DiseaseCohort("FH (Cardiovascular)", float(0.0050), float(0.30), float(0.70), float(3.0), float(45000.0))
    ]

def compute_clinical_outcomes(uptake: Float[Array, ""]) -> dict[str, Any]:
    """
    Aggregate clinical outcomes across all standard cohorts.
    """
    cohorts = get_standard_cohorts()
    results = [simulate_cohort_outcomes(uptake, c) for c in cohorts]
    
    total_qaly = sum(r["qaly_gains"] for r in results)
    total_savings = sum(r["cost_savings"] for r in results)
    
    return {
        "total_qaly_gains": total_qaly,
        "total_cost_savings": total_savings,
        "cohort_breakdown": {c.name: r for c, r in zip(cohorts, results)}
    }
