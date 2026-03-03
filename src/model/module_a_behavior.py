"""
Module A: Behavior / Deterrence model.

Implements discrete choice model for genetic testing behavior under
perceived discrimination risk.

Strategic Game: Testing Participation under Penalty Risk
- Players: Individuals, Insurers (downstream penalty), Policymakers
- Mechanism: Participation under perceived penalty risk
- Equilibrium: Testing uptake as function of policy regime
"""

from __future__ import annotations

from typing import Dict, Tuple
import jax.numpy as jnp
from jax import jit, vmap
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig


@jit
def compute_perceived_penalty(
    adverse_selection_elasticity: float,
    baseline_loading: float,
    allow_genetic_test_results: bool,
    enforcement_strength: float,
    enforcement_effectiveness: float,
    moratorium_effect: float,
    sum_insured_caps: dict | None = None,
) -> Float[Array, ""]:
    """
    Compute perceived discrimination penalty under policy regime.
    
    The perceived penalty captures the expected cost of genetic testing
    from the individual's perspective, considering:
    - Probability of discrimination
    - Severity of discrimination (premium loading, denial)
    - Policy protections
    
    Args:
        adverse_selection_elasticity: Adverse selection elasticity
        baseline_loading: Baseline premium loading
        allow_genetic_test_results: Whether genetic tests are allowed
        enforcement_strength: Enforcement strength (0-1)
        enforcement_effectiveness: Enforcement effectiveness
        moratorium_effect: Moratorium effect size
        sum_insured_caps: Sum insured caps by product type
        
    Returns:
        Perceived penalty (higher = more deterrence)
    """
    # Base penalty from adverse selection
    base_penalty = adverse_selection_elasticity * baseline_loading
    
    # Policy reduces penalty based on:
    # 1. Information restrictions
    # 2. Enforcement effectiveness
    
    info_restriction = 1.0 if allow_genetic_test_results else 0.0
    enforcement_factor = enforcement_strength * enforcement_effectiveness
    
    # Penalty reduction from policy
    penalty_reduction = info_restriction * enforcement_factor
    
    # Apply moratorium effect if applicable
    if not allow_genetic_test_results and sum_insured_caps is not None:
        penalty_reduction += moratorium_effect
    
    # Final perceived penalty
    perceived_penalty = base_penalty * (1.0 - penalty_reduction)
    
    return perceived_penalty


# Convenience wrapper that accepts ModelParameters and PolicyConfig
def compute_perceived_penalty_wrapper(
    params: ModelParameters,
    policy: PolicyConfig,
) -> float:
    """Wrapper that accepts pydantic models."""
    penalty = compute_perceived_penalty(
        params.adverse_selection_elasticity,
        params.baseline_loading,
        policy.allow_genetic_test_results,
        policy.enforcement_strength,
        params.enforcement_effectiveness,
        params.moratorium_effect,
        policy.sum_insured_caps,
    )
    return float(penalty)
    benefits: Float[Array, ""],
    perceived_penalty: Float[Array, ""],
    individual_characteristics: Dict[str, Float[Array, ""]] | None = None,
) -> Float[Array, ""]:
    """
    Compute utility of genetic testing.
    
    Utility function:
        U(test) = benefits - perceived_penalty + individual_factors
    
    Args:
        benefits: Perceived benefits of testing (health, information)
        perceived_penalty: Perceived discrimination penalty
        individual_characteristics: Optional individual-level factors
        
    Returns:
        Utility of testing
    """
    # Base utility
    utility = benefits - perceived_penalty
    
    # Add individual characteristics if provided
    if individual_characteristics is not None:
        for factor, weight in individual_characteristics.items():
            utility = utility + weight * individual_characteristics.get(factor, 0.0)
    
    return utility


@jit
def compute_testing_probability(
    utility: Float[Array, ""],
    scale: float = 1.0,
) -> Float[Array, ""]:
    """
    Compute probability of testing given utility (logit model).
    
    P(test) = exp(scale * utility) / (1 + exp(scale * utility))
    
    Args:
        utility: Utility of testing
        scale: Scale parameter (higher = more deterministic choice)
        
    Returns:
        Probability of testing
    """
    scaled_utility = utility * scale
    probability = jnp.exp(scaled_utility) / (1.0 + jnp.exp(scaled_utility))
    return probability


@jit
def compute_testing_uptake(
    params: ModelParameters,
    policy: PolicyConfig,
    benefits_mean: float = 0.5,
    benefits_sd: float = 0.1,
    n_individuals: int = 1000,
    rng_key: Array | None = None,
) -> Float[Array, ""]:
    """
    Compute aggregate testing uptake under policy regime.
    
    This function:
    1. Computes perceived penalty for policy regime
    2. Simulates heterogeneous benefits across individuals
    3. Computes testing probability for each individual
    4. Aggregates to population-level uptake
    
    Args:
        params: Model parameters
        policy: Policy configuration
        benefits_mean: Mean perceived benefits of testing
        benefits_sd: Standard deviation of benefits (heterogeneity)
        n_individuals: Number of individuals to simulate
        rng_key: Optional RNG key for benefit simulation
        
    Returns:
        Aggregate testing uptake rate (0-1)
    """
    # Compute perceived penalty
    perceived_penalty = compute_perceived_penalty(params, policy)
    
    # Simulate heterogeneous benefits
    if rng_key is not None:
        benefits = jr.normal(rng_key, (n_individuals,)) * benefits_sd + benefits_mean
    else:
        # Deterministic grid for reproducibility
        benefits = jnp.linspace(
            benefits_mean - 3 * benefits_sd,
            benefits_mean + 3 * benefits_sd,
            n_individuals
        )
    
    # Compute utility for each individual
    utilities = compute_testing_utility(benefits, perceived_penalty)
    
    # Compute testing probabilities
    probabilities = compute_testing_probability(utilities)
    
    # Aggregate uptake
    uptake = jnp.mean(probabilities)
    
    return uptake


@jit
def compute_policy_effect(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> Dict[str, Float[Array, ""]]:
    """
    Compute effect of policy reform on testing uptake.
    
    Args:
        params: Model parameters
        baseline_policy: Baseline policy (e.g., status quo)
        reform_policy: Reform policy (e.g., moratorium, ban)
        
    Returns:
        Dictionary with:
        - baseline_uptake: Testing uptake under baseline
        - reform_uptake: Testing uptake under reform
        - absolute_effect: Absolute change in uptake
        - relative_effect: Relative change in uptake
    """
    # Compute uptake under both policies
    baseline_uptake = compute_testing_uptake(params, baseline_policy)
    reform_uptake = compute_testing_uptake(params, reform_policy)
    
    # Compute effects
    absolute_effect = reform_uptake - baseline_uptake
    relative_effect = absolute_effect / (baseline_uptake + 1e-10)
    
    return {
        'baseline_uptake': baseline_uptake,
        'reform_uptake': reform_uptake,
        'absolute_effect': absolute_effect,
        'relative_effect': relative_effect,
    }


# Vectorized version for batch evaluation
_compute_testing_uptake_batch = vmap(
    compute_testing_uptake,
    in_axes=(None, 0, None, None, None, None),
    out_axes=0,
)


@jit
def evaluate_multiple_policies(
    params: ModelParameters,
    policies: list[PolicyConfig],
    **kwargs,
) -> Float[Array, "n_policies"]:
    """
    Evaluate testing uptake for multiple policies (vectorized).
    
    Uses vmap for efficient batch evaluation.
    
    Args:
        params: Model parameters
        policies: List of policy configurations
        **kwargs: Additional arguments for compute_testing_uptake
        
    Returns:
        Array of uptake rates for each policy
    """
    return _compute_testing_uptake_batch(params, policies, **kwargs)


# Convenience function for common scenarios
def get_standard_policies() -> Dict[str, PolicyConfig]:
    """
    Get standard policy configurations.
    
    Returns:
        Dictionary with 'status_quo', 'moratorium', 'ban' policies
    """
    return {
        'status_quo': PolicyConfig(
            name='status_quo',
            description='No restrictions on genetic information use',
            allow_genetic_test_results=True,
            allow_family_history=True,
            enforcement_strength=1.0,
        ),
        'moratorium': PolicyConfig(
            name='moratorium',
            description='Industry moratorium with caps',
            allow_genetic_test_results=False,
            allow_family_history=True,
            sum_insured_caps={'death': 500000, 'tpd': 200000, 'trauma': 200000},
            enforcement_strength=0.5,
        ),
        'ban': PolicyConfig(
            name='ban',
            description='Statutory ban on genetic information use',
            allow_genetic_test_results=False,
            allow_family_history=False,
            enforcement_strength=1.0,
            penalty_max=1000000,
        ),
    }
