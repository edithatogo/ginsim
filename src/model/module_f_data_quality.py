"""
Module F: Data Quality Externality model.

Implements public goods game for research participation.

Strategic Game: Participation as Public Good
- Players: Individuals (participation decisions), Researchers, Health system
- Mechanism: Participation improves dataset representativeness and future tools
- Equilibrium: Participation rate as function of privacy protections
"""

from __future__ import annotations

from typing import Dict, Tuple
from dataclasses import dataclass
import jax.numpy as jnp
from jax import jit, vmap
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig


@dataclass
class DataQualityMetrics:
    """
    Data quality metrics.
    
    Attributes:
        participation_rate: Proportion participating in research
        representativeness: How representative the sample is
        predictive_performance: Performance of models trained on data
        selection_bias: Measure of selection bias
    """
    participation_rate: Float[Array, ""]
    representativeness: Float[Array, ""]
    predictive_performance: Float[Array, ""]
    selection_bias: Float[Array, ""]


@jit
def compute_participation_probability(
    privacy_protections: Float[Array, ""],
    social_benefit: Float[Array, ""],
    privacy_concern: Float[Array, ""],
    elasticity: float = -0.10,
) -> Float[Array, ""]:
    """
    Compute probability of research participation.
    
    Participation decision based on:
    - Privacy protections (positive effect)
    - Perceived social benefit (positive effect)
    - Privacy concerns (negative effect)
    
    Args:
        privacy_protections: Strength of privacy protections (0-1)
        social_benefit: Perceived social benefit (0-1)
        privacy_concern: Individual privacy concern (0-1)
        elasticity: Elasticity of participation w.r.t. protections
        
    Returns:
        Participation probability
    """
    # Base participation rate
    base_rate = 0.5
    
    # Effect of privacy protections
    protection_effect = elasticity * (1.0 - privacy_protections)
    
    # Effect of social benefit
    benefit_effect = 0.2 * social_benefit
    
    # Effect of privacy concerns
    concern_effect = -0.3 * privacy_concern
    
    # Final participation probability
    participation_prob = base_rate + protection_effect + benefit_effect + concern_effect
    
    # Bound [0, 1]
    participation_prob = jnp.clip(participation_prob, 0.0, 1.0)
    
    return participation_prob


# Don't use @jit - uses pydantic models
def compute_participation_rate(
    params: ModelParameters,
    policy: PolicyConfig,
    n_individuals: int = 1000,
    rng_key: Array | None = None,
) -> Float[Array, ""]:
    """
    Compute aggregate research participation rate.
    
    Args:
        params: Model parameters
        policy: Policy configuration
        n_individuals: Number of individuals to simulate
        rng_key: Optional RNG key
        
    Returns:
        Participation rate
    """
    # Privacy protections from policy
    if not policy.allow_genetic_test_results:
        privacy_protections = policy.enforcement_strength
    else:
        privacy_protections = 0.2  # Low protections if information allowed
    
    # Social benefit (assumed constant)
    social_benefit = 0.6
    
    # Simulate heterogeneous privacy concerns
    if rng_key is not None:
        privacy_concerns = jr.uniform(rng_key, (n_individuals,))
    else:
        privacy_concerns = jnp.linspace(0, 1, n_individuals)
    
    # Compute participation probabilities
    participation_probs = compute_participation_probability(
        privacy_protections=privacy_protections,
        social_benefit=social_benefit,
        privacy_concern=privacy_concerns,
        elasticity=params.research_participation_elasticity,
    )
    
    # Aggregate participation rate
    participation_rate = jnp.mean(participation_probs)
    
    return participation_rate


@jit
def compute_representativeness(
    participation_rate: Float[Array, ""],
    selection_bias_parameter: float = 0.5,
) -> Float[Array, ""]:
    """
    Compute sample representativeness as function of participation.
    
    Representativeness decreases with selection bias.
    
    Args:
        participation_rate: Participation rate
        selection_bias_parameter: Strength of selection bias
        
    Returns:
        Representativeness score (0-1)
    """
    # Representativeness increases with participation
    representativeness = participation_rate ** (1.0 - selection_bias_parameter)
    
    return representativeness


@jit
def compute_predictive_performance(
    representativeness: Float[Array, ""],
    baseline_performance: float = 0.8,
    max_performance: float = 0.95,
) -> Float[Array, ""]:
    """
    Compute predictive performance as function of data quality.
    
    Args:
        representativeness: Sample representativeness
        baseline_performance: Performance with minimal data
        max_performance: Maximum achievable performance
        
    Returns:
        Predictive performance metric
    """
    # Performance increases with representativeness
    performance = baseline_performance + (max_performance - baseline_performance) * representativeness
    
    return performance


@jit
def compute_selection_bias(
    participation_rate: Float[Array, ""],
    high_risk_participation_ratio: float = 0.8,
) -> Float[Array, ""]:
    """
    Compute selection bias metric.
    
    Selection bias occurs when high-risk individuals participate
    at different rates than low-risk individuals.
    
    Args:
        participation_rate: Overall participation rate
        high_risk_participation_ratio: Ratio of high-risk to low-risk participation
        
    Returns:
        Selection bias metric (0 = no bias, 1 = maximum bias)
    """
    # Selection bias increases as ratio deviates from 1
    bias = jnp.abs(1.0 - high_risk_participation_ratio)
    
    # Scale by participation rate (low participation → more bias)
    bias = bias * (1.0 - participation_rate)
    
    return bias


# Don't use @jit - uses pydantic models
def compute_data_quality_externality(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> Dict[str, Float[Array, ""]]:
    """
    Compute data quality externality of policy change.
    
    Policy changes affect participation, which affects data quality,
    which affects future predictive tools (externality).
    
    Args:
        params: Model parameters
        baseline_policy: Baseline policy
        reform_policy: Reform policy
        
    Returns:
        Dictionary with data quality metrics for both policies
    """
    # Compute participation rates
    participation_baseline = compute_participation_rate(params, baseline_policy)
    participation_reform = compute_participation_rate(params, reform_policy)
    
    # Compute representativeness
    representativeness_baseline = compute_representativeness(participation_baseline)
    representativeness_reform = compute_representativeness(participation_reform)
    
    # Compute predictive performance
    performance_baseline = compute_predictive_performance(representativeness_baseline)
    performance_reform = compute_predictive_performance(representativeness_reform)
    
    # Compute selection bias
    bias_baseline = compute_selection_bias(participation_baseline)
    bias_reform = compute_selection_bias(participation_reform)
    
    return {
        'participation_baseline': participation_baseline,
        'participation_reform': participation_reform,
        'representativeness_baseline': representativeness_baseline,
        'representativeness_reform': representativeness_reform,
        'performance_baseline': performance_baseline,
        'performance_reform': performance_reform,
        'selection_bias_baseline': bias_baseline,
        'selection_bias_reform': bias_reform,
    }


@jit
def compute_research_value_loss(
    performance_baseline: Float[Array, ""],
    performance_reform: Float[Array, ""],
    annual_research_value: float = 1e6,  # $1M annual value
    discount_rate: float = 0.03,
    time_horizon: int = 10,
) -> Float[Array, ""]:
    """
    Compute present value of research value loss.
    
    Args:
        performance_baseline: Performance under baseline
        performance_reform: Performance under reform
        annual_research_value: Annual value of research
        discount_rate: Discount rate
        time_horizon: Time horizon in years
        
    Returns:
        Present value of research value loss
    """
    # Performance loss
    performance_loss = performance_baseline - performance_reform
    
    # Annual value loss
    annual_loss = performance_loss * annual_research_value
    
    # Present value (geometric series)
    if discount_rate > 0:
        pv_factor = (1 - (1 + discount_rate) ** (-time_horizon)) / discount_rate
    else:
        pv_factor = time_horizon
    
    present_value_loss = annual_loss * pv_factor
    
    return present_value_loss


# Convenience function
def get_standard_participation_parameters() -> Dict[str, float]:
    """
    Get standard parameters for participation model.
    
    Returns:
        Dictionary with standard parameter values
    """
    return {
        'base_participation': 0.5,
        'privacy_elasticity': -0.10,
        'social_benefit': 0.6,
        'annual_research_value': 1e6,
        'discount_rate': 0.03,
        'time_horizon': 10,
    }
