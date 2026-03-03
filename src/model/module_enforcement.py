"""
Enforcement and Compliance module.

Implements compliance game between insurers and regulators.

Strategic Game: Enforcement/Compliance
- Players: Insurers, Regulator, Applicants
- Mechanism: Compliance game with monitoring and penalties
- Equilibrium: Mixed strategy Nash equilibrium
"""

from __future__ import annotations

from typing import Dict, Tuple
from dataclasses import dataclass
import jax.numpy as jnp
from jax import jit
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig


@dataclass
class ComplianceOutcome:
    """
    Compliance outcome metrics.
    
    Attributes:
        compliance_rate: Proportion of insurers complying
        violation_rate: Proportion violating policy
        detection_rate: Proportion of violations detected
        expected_penalty: Expected penalty for violation
    """
    compliance_rate: Float[Array, ""]
    violation_rate: Float[Array, ""]
    detection_rate: Float[Array, ""]
    expected_penalty: Float[Array, ""]


@jit
def compute_detection_probability(
    enforcement_strength: Float[Array, ""],
    monitoring_intensity: Float[Array, ""],
    max_detection: float = 0.9,
) -> Float[Array, ""]:
    """
    Compute probability of detecting violations.
    
    Args:
        enforcement_strength: Overall enforcement strength (0-1)
        monitoring_intensity: Intensity of monitoring (0-1)
        max_detection: Maximum achievable detection rate
        
    Returns:
        Detection probability
    """
    # Detection increases with enforcement and monitoring
    detection = max_detection * enforcement_strength * monitoring_intensity
    
    return detection


@jit
def compute_expected_penalty(
    penalty_max: float,
    detection_probability: Float[Array, ""],
    enforcement_effectiveness: Float[Array, ""],
) -> Float[Array, ""]:
    """
    Compute expected penalty for violation.
    
    Expected penalty = penalty_max * detection_probability * enforcement_effectiveness
    
    Args:
        penalty_max: Maximum statutory penalty
        detection_probability: Probability of detection
        enforcement_effectiveness: Effectiveness of enforcement
        
    Returns:
        Expected penalty
    """
    expected_penalty = penalty_max * detection_probability * enforcement_effectiveness
    
    return expected_penalty


# Don't use @jit - uses pydantic models
def compute_violation_benefit(
    params: ModelParameters,
    policy: PolicyConfig,
) -> Float[Array, ""]:
    """
    Compute benefit from violating policy.
    
    Benefit comes from:
    - Using genetic information for better risk selection
    - Avoiding high-risk individuals
    
    Args:
        params: Model parameters
        policy: Policy configuration
        
    Returns:
        Benefit from violation
    """
    # Base benefit from using genetic information
    base_benefit = params.adverse_selection_elasticity * params.baseline_loading
    
    # Reduce benefit if policy allows some information use
    if policy.allow_genetic_test_results:
        benefit_multiplier = 0.2  # Low benefit if already allowed
    elif policy.sum_insured_caps is not None:
        benefit_multiplier = 0.5  # Medium benefit if caps exist
    else:
        benefit_multiplier = 1.0  # Full benefit if completely banned
    
    benefit = base_benefit * benefit_multiplier
    
    return benefit


@jit
def compute_compliance_decision(
    violation_benefit: Float[Array, ""],
    expected_penalty: Float[Array, ""],
) -> Float[Array, ""]:
    """
    Compute probability of compliance (vs violation).
    
    Insurer complies if expected penalty > violation benefit.
    Uses smooth decision function (logit).
    
    Args:
        violation_benefit: Benefit from violating
        expected_penalty: Expected penalty if caught
        
    Returns:
        Compliance probability
    """
    # Net benefit of violation
    net_benefit = violation_benefit - expected_penalty
    
    # Logit decision function
    scale = 5.0  # Decision sharpness
    compliance_prob = 1.0 / (1.0 + jnp.exp(scale * net_benefit))
    
    return compliance_prob


# Don't use @jit - uses pydantic models
def compute_compliance_equilibrium(
    params: ModelParameters,
    policy: PolicyConfig,
    monitoring_intensity: float = 0.5,
) -> ComplianceOutcome:
    """
    Compute compliance equilibrium.
    
    Args:
        params: Model parameters
        policy: Policy configuration
        monitoring_intensity: Intensity of regulatory monitoring
        
    Returns:
        ComplianceOutcome object
    """
    # Detection probability
    detection_prob = compute_detection_probability(
        policy.enforcement_strength,
        monitoring_intensity,
    )
    
    # Expected penalty
    expected_pen = compute_expected_penalty(
        policy.penalty_max,
        detection_prob,
        params.enforcement_effectiveness,
    )
    
    # Violation benefit
    violation_ben = compute_violation_benefit(params, policy)
    
    # Compliance decision
    compliance_prob = compute_compliance_decision(violation_ben, expected_pen)
    
    # Violation rate
    violation_rate = 1.0 - compliance_prob
    
    # Detection rate (of actual violations)
    detection_rate = detection_prob * violation_rate
    
    return ComplianceOutcome(
        compliance_rate=compliance_prob,
        violation_rate=violation_rate,
        detection_rate=detection_rate,
        expected_penalty=expected_pen,
    )


# Don't use @jit - uses pydantic models
def compute_enforcement_effect(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> Dict[str, Float[Array, ""]]:
    """
    Compute effect of enforcement changes.
    
    Args:
        params: Model parameters
        baseline_policy: Baseline policy
        reform_policy: Reform policy
        
    Returns:
        Dictionary with enforcement effect metrics
    """
    # Compute compliance for both policies
    outcome_baseline = compute_compliance_equilibrium(params, baseline_policy)
    outcome_reform = compute_compliance_equilibrium(params, reform_policy)
    
    # Effects
    compliance_change = outcome_reform.compliance_rate - outcome_baseline.compliance_rate
    violation_change = outcome_reform.violation_rate - outcome_baseline.violation_rate
    
    return {
        'compliance_baseline': outcome_baseline.compliance_rate,
        'compliance_reform': outcome_reform.compliance_rate,
        'compliance_change': compliance_change,
        'violation_baseline': outcome_baseline.violation_rate,
        'violation_reform': outcome_reform.violation_rate,
        'violation_change': violation_change,
        'detection_baseline': outcome_baseline.detection_rate,
        'detection_reform': outcome_reform.detection_rate,
    }


# Don't use @jit - uses pydantic models and has optimization loop
def compute_optimal_enforcement(
    params: ModelParameters,
    policy: PolicyConfig,
    target_compliance: float = 0.9,
    enforcement_cost_parameter: float = 0.1,
) -> Dict[str, Float[Array, ""]]:
    """
    Compute optimal enforcement level.
    
    Balances:
    - Benefit of higher compliance
    - Cost of enforcement
    
    Args:
        params: Model parameters
        policy: Policy configuration
        target_compliance: Target compliance rate
        enforcement_cost_parameter: Cost parameter for enforcement
        
    Returns:
        Dictionary with optimal enforcement metrics
    """
    # Grid search for optimal enforcement
    enforcement_levels = jnp.linspace(0, 1, 50)
    
    def compute_objective(enf_strength):
        # Create policy with this enforcement level
        enf_policy = PolicyConfig(
            name=policy.name,
            description=policy.description,
            allow_genetic_test_results=policy.allow_genetic_test_results,
            allow_family_history=policy.allow_family_history,
            sum_insured_caps=policy.sum_insured_caps,
            enforcement_strength=enf_strength,
            penalty_max=policy.penalty_max,
        )
        
        # Compute compliance
        outcome = compute_compliance_equilibrium(params, enf_policy, monitoring_intensity=0.5)
        
        # Objective: minimize distance from target + enforcement cost
        compliance_gap = (target_compliance - outcome.compliance_rate) ** 2
        enforcement_cost = enforcement_cost_parameter * enf_strength ** 2
        
        objective = compliance_gap + enforcement_cost
        
        return objective
    
    # Evaluate objective at all enforcement levels
    objectives = jnp.array([compute_objective(e) for e in enforcement_levels])
    
    # Find optimal
    optimal_idx = jnp.argmin(objectives)
    optimal_enforcement = enforcement_levels[optimal_idx]
    
    # Compute outcome at optimal
    optimal_policy = PolicyConfig(
        name=policy.name,
        description=policy.description,
        allow_genetic_test_results=policy.allow_genetic_test_results,
        allow_family_history=policy.allow_family_history,
        sum_insured_caps=policy.sum_insured_caps,
        enforcement_strength=optimal_enforcement,
        penalty_max=policy.penalty_max,
    )
    
    optimal_outcome = compute_compliance_equilibrium(params, optimal_policy)
    
    return {
        'optimal_enforcement': optimal_enforcement,
        'optimal_compliance': optimal_outcome.compliance_rate,
        'optimal_violation_rate': optimal_outcome.violation_rate,
        'objective_value': objectives[optimal_idx],
    }


# Convenience function
def get_standard_enforcement_parameters() -> Dict[str, float]:
    """
    Get standard enforcement parameters.
    
    Returns:
        Dictionary with standard parameter values
    """
    return {
        'monitoring_intensity': 0.5,
        'target_compliance': 0.9,
        'enforcement_cost_parameter': 0.1,
        'max_detection_rate': 0.9,
    }
