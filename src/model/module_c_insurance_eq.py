"""
Module C: Insurance Equilibrium model.

Implements Rothschild-Stiglitz screening model with policy constraints.

Strategic Game: Adverse Selection under Asymmetric Information
- Players: Applicants (informed about risk), Insurers (uninformed), Regulator
- Mechanism: Bayesian screening with policy information constraints
- Equilibrium: Separating/pooling equilibrium under different information regimes
"""

from __future__ import annotations

from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import jax.numpy as jnp
from jax import jit, lax
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig


@dataclass
class InsuranceEquilibrium:
    """
    Insurance market equilibrium outcomes.
    
    Attributes:
        premium_high_risk: Premium for high-risk individuals
        premium_low_risk: Premium for low-risk individuals  
        takeup_high_risk: Insurance take-up rate for high-risk
        takeup_low_risk: Insurance take-up rate for low-risk
        insurer_profits: Insurer expected profits (should be ~0 at equilibrium)
        converged: Whether equilibrium solver converged
        iterations: Number of iterations to converge
    """
    premium_high_risk: Float[Array, ""]
    premium_low_risk: Float[Array, ""]
    takeup_high_risk: Float[Array, ""]
    takeup_low_risk: Float[Array, ""]
    insurer_profits: Float[Array, ""]
    converged: bool
    iterations: int


@jit
def compute_risk_premium(
    risk_probability: Float[Array, ""],
    sum_insured: float = 1.0,
    loading: float = 0.0,
) -> Float[Array, ""]:
    """
    Compute actuarially fair premium with loading.
    
    Premium = risk_probability * sum_insured * (1 + loading)
    
    Args:
        risk_probability: Probability of claim (e.g., mortality)
        sum_insured: Coverage amount
        loading: Loading factor for administrative costs, profit
        
    Returns:
        Premium amount
    """
    return risk_probability * sum_insured * (1.0 + loading)


@jit
def compute_demand(
    premium: Float[Array, ""],
    income: float = 1.0,
    risk_aversion: float = 2.0,
    price_elasticity: float = -0.22,
) -> Float[Array, ""]:
    """
    Compute insurance demand given premium.
    
    Demand function:
        D(p) = base_demand * (p / p_ref)^elasticity
    
    Args:
        premium: Insurance premium
        income: Consumer income
        risk_aversion: Coefficient of relative risk aversion
        price_elasticity: Price elasticity of demand
        
    Returns:
        Demand (probability of purchase)
    """
    # Reference premium (actuarially fair for average risk)
    p_ref = 0.1  # Normalized reference
    
    # Demand with constant elasticity
    relative_price = premium / (p_ref + 1e-10)
    demand = jnp.power(relative_price, price_elasticity)
    
    # Bound demand [0, 1]
    demand = jnp.clip(demand, 0.0, 1.0)
    
    return demand


@jit
def compute_expected_profit(
    premium: Float[Array, ""],
    risk_probability: Float[Array, ""],
    sum_insured: float = 1.0,
    takeup: Float[Array, ""] = 1.0,
) -> Float[Array, ""]:
    """
    Compute insurer expected profit per policy.
    
    Profit = (premium - risk_probability * sum_insured) * takeup
    
    Args:
        premium: Premium charged
        risk_probability: Claim probability
        sum_insured: Coverage amount
        takeup: Take-up rate
        
    Returns:
        Expected profit
    """
    expected_claim = risk_probability * sum_insured
    profit_per_policy = premium - expected_claim
    total_profit = profit_per_policy * takeup
    
    return total_profit


@jit
def zero_profit_premium(
    risk_probability: Float[Array, ""],
    sum_insured: float = 1.0,
    loading: float = 0.0,
) -> Float[Array, ""]:
    """
    Compute zero-profit (actuarially fair) premium.
    
    At zero profit: premium = risk_probability * sum_insured * (1 + loading)
    
    Args:
        risk_probability: Claim probability
        sum_insured: Coverage amount
        loading: Loading factor
        
    Returns:
        Zero-profit premium
    """
    return compute_risk_premium(risk_probability, sum_insured, loading)


# Don't use @jit - uses pydantic models
def separating_equilibrium(
    params: ModelParameters,
    risk_high: float = 0.3,
    risk_low: float = 0.1,
    proportion_high: float = 0.2,
) -> InsuranceEquilibrium:
    """
    Compute separating equilibrium (full information).
    
    In separating equilibrium:
    - High-risk pay premium based on their risk
    - Low-risk pay premium based on their risk
    - No cross-subsidization
    
    Args:
        params: Model parameters
        risk_high: Claim probability for high-risk
        risk_low: Claim probability for low-risk
        proportion_high: Proportion of high-risk individuals
        
    Returns:
        InsuranceEquilibrium object
    """
    # Zero-profit premiums for each risk type
    premium_high = zero_profit_premium(
        risk_high,
        sum_insured=1.0,
        loading=params.baseline_loading
    )
    
    premium_low = zero_profit_premium(
        risk_low,
        sum_insured=1.0,
        loading=params.baseline_loading
    )
    
    # Demand at these premiums
    takeup_high = compute_demand(
        premium_high,
        price_elasticity=params.demand_elasticity_high_risk
    )
    
    takeup_low = compute_demand(premium_low)
    
    # Profits (should be ~0)
    profit_high = compute_expected_profit(premium_high, risk_high, takeup=takeup_high)
    profit_low = compute_expected_profit(premium_low, risk_low, takeup=takeup_low)
    total_profit = profit_high * proportion_high + profit_low * (1 - proportion_high)
    
    return InsuranceEquilibrium(
        premium_high_risk=premium_high,
        premium_low_risk=premium_low,
        takeup_high_risk=takeup_high,
        takeup_low_risk=takeup_low,
        insurer_profits=total_profit,
        converged=True,
        iterations=1,
    )


# Don't use @jit - uses pydantic models
def pooling_equilibrium(
    params: ModelParameters,
    risk_high: float = 0.3,
    risk_low: float = 0.1,
    proportion_high: float = 0.2,
    max_iterations: int = 100,
    tolerance: float = 1e-6,
) -> InsuranceEquilibrium:
    """
    Compute pooling equilibrium (no information).
    
    In pooling equilibrium:
    - All individuals pay same premium
    - Premium based on average risk in pool
    - May have adverse selection (low-risk drop out)
    
    Uses iterative algorithm:
    1. Start with average risk premium
    2. Compute demand for each type
    3. Update pool composition
    4. Recompute premium based on new pool
    5. Repeat until convergence
    
    Args:
        params: Model parameters
        risk_high: Claim probability for high-risk
        risk_low: Claim probability for low-risk
        proportion_high: Initial proportion of high-risk
        max_iterations: Maximum iterations
        tolerance: Convergence tolerance
        
    Returns:
        InsuranceEquilibrium object
    """
    # Initial pool risk (average)
    avg_risk = proportion_high * risk_high + (1 - proportion_high) * risk_low
    
    def iteration_step(carry):
        premium, pool_risk, prop_high, i = carry
        
        # Compute demand for each type
        takeup_high = compute_demand(
            premium,
            price_elasticity=params.demand_elasticity_high_risk
        )
        takeup_low = compute_demand(premium)
        
        # Update pool composition (who remains insured)
        high_risk_insured = prop_high * takeup_high
        low_risk_insured = (1 - prop_high) * takeup_low
        total_insured = high_risk_insured + low_risk_insured + 1e-10
        
        new_prop_high = high_risk_insured / total_insured
        
        # Compute new pool risk
        new_pool_risk = new_prop_high * risk_high + (1 - new_prop_high) * risk_low
        
        # Compute zero-profit premium for new pool
        new_premium = zero_profit_premium(
            new_pool_risk,
            sum_insured=1.0,
            loading=params.baseline_loading
        )
        
        # Check convergence
        converged = jnp.abs(new_premium - premium) < tolerance
        
        return (new_premium, new_pool_risk, new_prop_high, i + 1), converged
    
    # Initial premium
    initial_premium = zero_profit_premium(avg_risk, sum_insured=1.0, loading=params.baseline_loading)
    
    # Iterate
    init_carry = (initial_premium, avg_risk, proportion_high, 0)
    
    (premium, pool_risk, prop_high, n_iter), _ = lax.while_loop(
        lambda carry_converged: carry_converged[1] == False,
        iteration_step,
        (init_carry, False)
    )
    
    # Final takeup
    takeup_high = compute_demand(
        premium,
        price_elasticity=params.demand_elasticity_high_risk
    )
    takeup_low = compute_demand(premium)
    
    # Profits
    profit = compute_expected_profit(premium, pool_risk, takeup=(takeup_high + takeup_low) / 2)
    
    return InsuranceEquilibrium(
        premium_high_risk=premium,
        premium_low_risk=premium,  # Same in pooling
        takeup_high_risk=takeup_high,
        takeup_low_risk=takeup_low,
        insurer_profits=profit,
        converged=(n_iter < max_iterations),
        iterations=n_iter.astype(int),
    )


# Don't use @jit - uses pydantic models
def compute_equilibrium(
    params: ModelParameters,
    policy: PolicyConfig,
    risk_high: float = 0.3,
    risk_low: float = 0.1,
    proportion_high: float = 0.2,
) -> InsuranceEquilibrium:
    """
    Compute insurance equilibrium under policy regime.
    
    Automatically selects separating vs pooling based on information availability.
    
    Args:
        params: Model parameters
        policy: Policy configuration
        risk_high: Claim probability for high-risk
        risk_low: Claim probability for low-risk
        proportion_high: Proportion of high-risk individuals
        
    Returns:
        InsuranceEquilibrium object
    """
    # Check if genetic information can be used
    if policy.allow_genetic_test_results:
        # Full information → separating equilibrium
        equilibrium = separating_equilibrium(
            params,
            risk_high=risk_high,
            risk_low=risk_low,
            proportion_high=proportion_high,
        )
    else:
        # No information → pooling equilibrium
        equilibrium = pooling_equilibrium(
            params,
            risk_high=risk_high,
            risk_low=risk_low,
            proportion_high=proportion_high,
        )
    
    return equilibrium


# Don't use @jit - uses pydantic models
def compute_premium_divergence(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> Dict[str, Float[Array, ""]]:
    """
    Compute premium divergence between policy regimes.
    
    Premium divergence measures the change in premium structure
    when moving from one policy regime to another.
    
    Args:
        params: Model parameters
        baseline_policy: Baseline policy
        reform_policy: Reform policy
        
    Returns:
        Dictionary with premium divergence metrics
    """
    # Compute equilibria
    eq_baseline = compute_equilibrium(params, baseline_policy)
    eq_reform = compute_equilibrium(params, reform_policy)
    
    # Premium divergence
    avg_premium_baseline = (eq_baseline.premium_high_risk + eq_baseline.premium_low_risk) / 2
    avg_premium_reform = (eq_reform.premium_high_risk + eq_reform.premium_low_risk) / 2
    
    absolute_divergence = avg_premium_reform - avg_premium_baseline
    relative_divergence = absolute_divergence / (avg_premium_baseline + 1e-10)
    
    # Risk rating (difference between high and low risk premiums)
    risk_rating_baseline = eq_baseline.premium_high_risk - eq_baseline.premium_low_risk
    risk_rating_reform = eq_reform.premium_high_risk - eq_reform.premium_low_risk
    
    return {
        'avg_premium_baseline': avg_premium_baseline,
        'avg_premium_reform': avg_premium_reform,
        'absolute_divergence': absolute_divergence,
        'relative_divergence': relative_divergence,
        'risk_rating_baseline': risk_rating_baseline,
        'risk_rating_reform': risk_rating_reform,
    }


# Convenience function
def get_standard_risk_parameters() -> Dict[str, float]:
    """
    Get standard risk parameters for equilibrium computation.
    
    Returns:
        Dictionary with risk_high, risk_low, proportion_high
    """
    return {
        'risk_high': 0.3,  # 30% claim probability for high-risk
        'risk_low': 0.1,   # 10% claim probability for low-risk
        'proportion_high': 0.2,  # 20% of population is high-risk
    }
