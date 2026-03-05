#!/usr/bin/env python3
"""
Extended strategic games for genetic discrimination policy analysis.

Implements advanced game-theoretic scenarios:
- Information Leakage Game (proxy bypass of genetic bans)
- Genetic Altruism Game (family-influenced testing decisions)
- Cascade Testing Game (sequential testing within families)
"""

from __future__ import annotations

from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
import jax.numpy as jnp
from jax import jit, vmap
from jaxtyping import Array, Float


@dataclass
class InformationLeakageResult:
    """Result from information leakage game."""
    reconstruction_accuracy: float  # How well insurers reconstruct risk
    bypass_rate: float  # Fraction of ban circumvented via proxies
    effective_uptake: float  # Actual testing uptake after leakage
    welfare_loss: float  # Welfare lost due to leakage


@dataclass
class GeneticAltruismResult:
    """Result from genetic altruism game."""
    family_testing_rate: float  # Testing rate influenced by family
    altruism_coefficient: float  # Strength of family influence
    spillover_effect: float  # Effect on non-tested family members
    welfare_impact: float  # Net welfare including altruism


@dataclass
class CascadeTestingResult:
    """Result from cascade testing game."""
    cascade_rate: float  # Rate of sequential family testing
    index_cases: int  # Number of initial testers
    secondary_cases: int  # Number of follow-up testers
    total_tests: int  # Total tests performed
    cost_effectiveness: float  # Cost per additional detection


def information_leakage_game(
    baseline_uptake: Float[Array, ""],
    ban_effectiveness: Float[Array, ""],
    proxy_accuracy: Float[Array, ""],
    insurer_inference_strength: Float[Array, ""],
) -> InformationLeakageResult:
    """
    Model information leakage through proxy variables.
    
    Even with genetic testing bans, insurers may reconstruct risk
    using family history, medical records, and other proxies.
    
    Args:
        baseline_uptake: Baseline testing uptake without discrimination
        ban_effectiveness: How effective the ban is (0-1)
        proxy_accuracy: How accurately proxies predict genetic risk (0-1)
        insurer_inference_strength: Insurer's ability to use proxies (0-1)
    
    Returns:
        InformationLeakageResult with leakage metrics
    """
    # Reconstruction accuracy = proxy accuracy × insurer inference strength
    reconstruction_accuracy = proxy_accuracy * insurer_inference_strength
    
    # Bypass rate = how much of the ban is circumvented
    # Higher reconstruction → higher bypass
    bypass_rate = reconstruction_accuracy * (1 - ban_effectiveness)
    
    # Effective uptake = baseline + (ban effect reduced by leakage)
    ban_boost = 0.20  # 20% increase from ban (example value)
    effective_uptake = baseline_uptake + ban_boost * (1 - bypass_rate)
    
    # Welfare loss from leakage
    # Leakage reduces the effectiveness of the ban
    welfare_loss = bypass_rate * 50000  # Example: $50k loss per bypass point
    
    return InformationLeakageResult(
        reconstruction_accuracy=float(reconstruction_accuracy),
        bypass_rate=float(bypass_rate),
        effective_uptake=float(effective_uptake),
        welfare_loss=float(welfare_loss),
    )


def genetic_altruism_game(
    baseline_uptake: Float[Array, ""],
    family_risk_level: Float[Array, ""],
    altruism_strength: Float[Array, ""],
    family_size: Float[Array, ""],
) -> GeneticAltruismResult:
    """
    Model genetic testing decisions influenced by family altruism.
    
    Individuals may get tested not just for themselves, but to help
    family members make informed decisions.
    
    Args:
        baseline_uptake: Baseline testing uptake for self-interest
        family_risk_level: Family's genetic risk level (0-1)
        altruism_strength: Strength of altruistic motivation (0-1)
        family_size: Number of family members who could benefit
    
    Returns:
        GeneticAltruismResult with altruism metrics
    """
    # Altruism coefficient = how much family influences decision
    altruism_coefficient = altruism_strength * jnp.minimum(family_size / 5, 1.0)
    
    # Family testing rate increases with risk and altruism
    family_testing_rate = baseline_uptake * (1 + altruism_coefficient * family_risk_level)
    
    # Spillover effect: non-tested family members benefit from information
    spillover_effect = altruism_coefficient * family_risk_level * 0.1
    
    # Welfare impact from altruism
    # Positive: better family decisions
    # Negative: potential anxiety from family risk knowledge
    welfare_impact = spillover_effect * 100000 - altruism_coefficient * 5000
    
    return GeneticAltruismResult(
        family_testing_rate=float(family_testing_rate),
        altruism_coefficient=float(altruism_coefficient),
        spillover_effect=float(spillover_effect),
        welfare_impact=float(welfare_impact),
    )


def cascade_testing_game(
    index_case_rate: Float[Array, ""],
    family_contact_rate: Float[Array, ""],
    uptake_after_contact: Float[Array, ""],
    average_family_size: Float[Array, ""],
    cost_per_test: Float[Array, ""],
    detection_yield: Float[Array, ""],
) -> CascadeTestingResult:
    """
    Model cascade testing within families.
    
    After an index case is identified, family members are contacted
    and offered testing, creating a cascade effect.
    
    Args:
        index_case_rate: Rate of initial (index) testers
        family_contact_rate: Fraction of families successfully contacted
        uptake_after_contact: Testing uptake after family contact
        average_family_size: Average number of testable family members
        cost_per_test: Cost per genetic test
        detection_yield: Probability of detecting mutation per test
    
    Returns:
        CascadeTestingResult with cascade metrics
    """
    # Assume 1000 population for calculation
    population = 1000
    index_cases = int(index_case_rate * population)
    
    # Secondary cases from cascade
    eligible_families = index_cases * family_contact_rate
    testable_relatives = eligible_families * (average_family_size - 1)  # Exclude index
    secondary_cases = int(testable_relatives * uptake_after_contact)
    
    # Total tests
    total_tests = index_cases + secondary_cases
    
    # Cost-effectiveness
    total_cost = total_tests * cost_per_test
    detections = index_cases * detection_yield + secondary_cases * detection_yield * 0.5  # Lower yield in cascade
    cost_effectiveness = total_cost / jnp.maximum(detections, 1)
    
    return CascadeTestingResult(
        cascade_rate=float(secondary_cases / jnp.maximum(index_cases, 1)),
        index_cases=index_cases,
        secondary_cases=secondary_cases,
        total_tests=total_tests,
        cost_effectiveness=float(cost_effectiveness),
    )


@jit
def run_extended_games_batch(
    params_batch: Dict[str, Float[Array, "batch"]],
) -> Dict[str, Float[Array, "batch"]]:
    """
    Run all extended games in batch for efficiency.
    
    Args:
        params_batch: Dictionary of parameter arrays for batch processing
        
    Returns:
        Dictionary of result arrays for all games
    """
    # Information Leakage
    leakage_result = vmap(lambda **kwargs: information_leakage_game(**kwargs))(
        baseline_uptake=params_batch.get("baseline_uptake", jnp.array([0.5])),
        ban_effectiveness=params_batch.get("ban_effectiveness", jnp.array([0.8])),
        proxy_accuracy=params_batch.get("proxy_accuracy", jnp.array([0.6])),
        insurer_inference_strength=params_batch.get("insurer_inference", jnp.array([0.7])),
    )
    
    # Genetic Altruism
    altruism_result = vmap(lambda **kwargs: genetic_altruism_game(**kwargs))(
        baseline_uptake=params_batch.get("baseline_uptake", jnp.array([0.5])),
        family_risk_level=params_batch.get("family_risk", jnp.array([0.3])),
        altruism_strength=params_batch.get("altruism_strength", jnp.array([0.5])),
        family_size=params_batch.get("family_size", jnp.array([4.0])),
    )
    
    # Cascade Testing
    cascade_result = vmap(lambda **kwargs: cascade_testing_game(**kwargs))(
        index_case_rate=params_batch.get("index_rate", jnp.array([0.05])),
        family_contact_rate=params_batch.get("contact_rate", jnp.array([0.7])),
        uptake_after_contact=params_batch.get("cascade_uptake", jnp.array([0.4])),
        average_family_size=params_batch.get("family_size", jnp.array([4.0])),
        cost_per_test=params_batch.get("test_cost", jnp.array([500.0])),
        detection_yield=params_batch.get("detection_yield", jnp.array([0.1])),
    )
    
    return {
        "leakage": {
            "reconstruction_accuracy": leakage_result.reconstruction_accuracy,
            "bypass_rate": leakage_result.bypass_rate,
            "effective_uptake": leakage_result.effective_uptake,
            "welfare_loss": leakage_result.welfare_loss,
        },
        "altruism": {
            "family_testing_rate": altruism_result.family_testing_rate,
            "altruism_coefficient": altruism_result.altruism_coefficient,
            "spillover_effect": altruism_result.spillover_effect,
            "welfare_impact": altruism_result.welfare_impact,
        },
        "cascade": {
            "cascade_rate": cascade_result.cascade_rate,
            "index_cases": cascade_result.index_cases,
            "secondary_cases": cascade_result.secondary_cases,
            "total_tests": cascade_result.total_tests,
            "cost_effectiveness": cascade_result.cost_effectiveness,
        },
    }


def format_extended_games_results(
    leakage: InformationLeakageResult,
    altruism: GeneticAltruismResult,
    cascade: CascadeTestingResult,
) -> str:
    """
    Format extended games results as markdown table.
    
    Args:
        leakage: Information leakage result
        altruism: Genetic altruism result
        cascade: Cascade testing result
        
    Returns:
        Formatted markdown string
    """
    lines = []
    lines.append("## Extended Strategic Games Results\n")
    
    # Information Leakage
    lines.append("### Information Leakage Game")
    lines.append(f"- **Reconstruction Accuracy:** {leakage.reconstruction_accuracy:.1%}")
    lines.append(f"- **Bypass Rate:** {leakage.bypass_rate:.1%}")
    lines.append(f"- **Effective Testing Uptake:** {leakage.effective_uptake:.1%}")
    lines.append(f"- **Welfare Loss from Leakage:** ${leakage.welfare_loss:,.0f}\n")
    
    # Genetic Altruism
    lines.append("### Genetic Altruism Game")
    lines.append(f"- **Altruism Coefficient:** {altruism.altruism_coefficient:.2f}")
    lines.append(f"- **Family Testing Rate:** {altruism.family_testing_rate:.1%}")
    lines.append(f"- **Spillover Effect:** {altruism.spillover_effect:.3f}")
    lines.append(f"- **Net Welfare Impact:** ${altruism.welfare_impact:,.0f}\n")
    
    # Cascade Testing
    lines.append("### Cascade Testing Game")
    lines.append(f"- **Cascade Rate:** {cascade.cascade_rate:.1f}x")
    lines.append(f"- **Index Cases:** {cascade.index_cases}")
    lines.append(f"- **Secondary Cases:** {cascade.secondary_cases}")
    lines.append(f"- **Total Tests:** {cascade.total_tests}")
    lines.append(f"- **Cost per Detection:** ${cascade.cost_effectiveness:,.0f}\n")
    
    return "\n".join(lines)
