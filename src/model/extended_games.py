"""
Extended strategic games for genetic discrimination policy analysis.

Implements advanced game-theoretic scenarios:
- Information Leakage Game (proxy bypass of genetic bans)
- Genetic Altruism Game (family-influenced testing decisions)
- Cascade Testing Game (sequential testing within families)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
from jax import jit
from jaxtyping import Array, Float


@dataclass(frozen=True)
class InformationLeakageResult:
    """Result from information leakage game."""

    reconstruction_accuracy: Any
    bypass_rate: Any
    effective_uptake: Any
    welfare_loss: Any


jax.tree_util.register_pytree_node(
    InformationLeakageResult,
    lambda x: ((x.reconstruction_accuracy, x.bypass_rate, x.effective_uptake, x.welfare_loss), ()),
    lambda aux, children: InformationLeakageResult(*children),
)


@dataclass(frozen=True)
class GeneticAltruismResult:
    """Result from genetic altruism game."""

    family_testing_rate: Any
    altruism_coefficient: Any
    spillover_effect: Any
    welfare_impact: Any


jax.tree_util.register_pytree_node(
    GeneticAltruismResult,
    lambda x: (
        (x.family_testing_rate, x.altruism_coefficient, x.spillover_effect, x.welfare_impact),
        (),
    ),
    lambda aux, children: GeneticAltruismResult(*children),
)


@dataclass(frozen=True)
class CascadeTestingResult:
    """Result from cascade testing game."""

    cascade_rate: Any
    index_cases: Any
    secondary_cases: Any
    total_tests: Any
    cost_effectiveness: Any


jax.tree_util.register_pytree_node(
    CascadeTestingResult,
    lambda x: (
        (x.cascade_rate, x.index_cases, x.secondary_cases, x.total_tests, x.cost_effectiveness),
        (),
    ),
    lambda aux, children: CascadeTestingResult(*children),
)


@jit
def _information_leakage_core(
    baseline_uptake: Float[Array, ""],
    ban_effectiveness: Float[Array, ""],
    proxy_accuracy: Float[Array, ""],
    insurer_inference_strength: Float[Array, ""],
) -> InformationLeakageResult:
    # Reconstruction accuracy = proxy accuracy × insurer inference strength
    reconstruction_accuracy = proxy_accuracy * insurer_inference_strength

    # Bypass rate = how much of the ban is circumvented
    threshold = 0.7
    base_bypass = reconstruction_accuracy * (1 - ban_effectiveness)
    acceleration = jnp.where(reconstruction_accuracy > threshold, 1.5, 1.0)
    bypass_rate = jnp.clip(base_bypass * acceleration, 0.0, 1.0)

    # Effective uptake = baseline + (ban effect reduced by leakage)
    ban_boost = 0.20
    effective_uptake = baseline_uptake + ban_boost * (1 - bypass_rate)

    # Welfare loss from leakage
    welfare_loss = bypass_rate * 50000

    return InformationLeakageResult(
        reconstruction_accuracy=reconstruction_accuracy,
        bypass_rate=bypass_rate,
        effective_uptake=effective_uptake,
        welfare_loss=welfare_loss,
    )


def information_leakage_game(
    baseline_uptake: Array | float,
    ban_effectiveness: Array | float,
    proxy_accuracy: Array | float,
    insurer_inference_strength: Array | float,
) -> InformationLeakageResult:
    """Public wrapper."""
    return _information_leakage_core(
        jnp.asarray(baseline_uptake),
        jnp.asarray(ban_effectiveness),
        jnp.asarray(proxy_accuracy),
        jnp.asarray(insurer_inference_strength),
    )


@jit
def _genetic_altruism_core(
    baseline_uptake: Float[Array, ""],
    family_risk_level: Float[Array, ""],
    altruism_strength: Float[Array, ""],
    family_size: Float[Array, ""],
    kinship_multiplier: Float[Array, ""] = 1.0,
) -> GeneticAltruismResult:
    # Altruism coefficient increases with family size and kinship
    altruism_coefficient = altruism_strength * (family_size / 4.0) * kinship_multiplier

    # Spillover effect: information benefits non-testers
    spillover_effect = family_risk_level * altruism_coefficient * 0.5

    # Effective testing rate
    family_testing_rate = jnp.clip(baseline_uptake + spillover_effect, 0.0, 1.0)

    # Welfare impact
    welfare_impact = family_testing_rate * 100000 * altruism_coefficient

    return GeneticAltruismResult(
        family_testing_rate=family_testing_rate,
        altruism_coefficient=altruism_coefficient,
        spillover_effect=spillover_effect,
        welfare_impact=welfare_impact,
    )


def genetic_altruism_game(
    baseline_uptake: Array | float,
    family_risk_level: Array | float,
    altruism_strength: Array | float,
    family_size: Array | float,
) -> GeneticAltruismResult:
    """Public wrapper."""
    return _genetic_altruism_core(
        jnp.asarray(baseline_uptake),
        jnp.asarray(family_risk_level),
        jnp.asarray(altruism_strength),
        jnp.asarray(family_size),
    )


@jit
def _cascade_testing_core(
    index_case_rate: Float[Array, ""],
    family_contact_rate: Float[Array, ""],
    uptake_after_contact: Float[Array, ""],
    average_family_size: Float[Array, ""],
    cost_per_test: Float[Array, ""],
    detection_yield: Float[Array, ""],
) -> CascadeTestingResult:
    # Cascade rate: additional tests per index case
    cascade_rate = family_contact_rate * uptake_after_contact * (average_family_size - 1)

    # Calculate cases
    n_individuals = 10000
    index_cases = index_case_rate * n_individuals
    secondary_cases = index_cases * cascade_rate
    total_tests = index_cases + secondary_cases

    # Cost effectiveness: cost per detection
    total_cost = total_tests * cost_per_test
    total_detections = (index_cases * detection_yield) + (secondary_cases * (detection_yield / 2.0))
    cost_effectiveness = total_cost / (total_detections + 1e-10)

    return CascadeTestingResult(
        cascade_rate=cascade_rate,
        index_cases=index_cases,
        secondary_cases=secondary_cases,
        total_tests=total_tests,
        cost_effectiveness=cost_effectiveness,
    )


def cascade_testing_game(
    index_case_rate: Array | float,
    family_contact_rate: Array | float,
    uptake_after_contact: Array | float,
    average_family_size: Array | float,
    cost_per_test: Array | float,
    detection_yield: Array | float,
) -> CascadeTestingResult:
    """Public wrapper."""
    return _cascade_testing_core(
        jnp.asarray(index_case_rate),
        jnp.asarray(family_contact_rate),
        jnp.asarray(uptake_after_contact),
        jnp.asarray(average_family_size),
        jnp.asarray(cost_per_test),
        jnp.asarray(detection_yield),
    )
