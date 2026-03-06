"""
Module C: Insurance Equilibrium model.

Implements Rothschild-Stiglitz screening model with policy constraints.

Strategic Game: Adverse Selection under Asymmetric Information
- Players: Applicants (informed about risk), Insurers (uninformed), Regulator
- Mechanism: Bayesian screening with policy information constraints
- Equilibrium: Separating/pooling equilibrium under different information regimes
"""

from __future__ import annotations

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
        uninsured_rate: Overall proportion uninsured
        insurer_profits: Insurer expected profits (should be ~0 at equilibrium)
        converged: Whether equilibrium solver converged
        iterations: Number of iterations to converge
    """

    premium_high_risk: Float[Array, ""]
    premium_low_risk: Float[Array, ""]
    takeup_high_risk: Float[Array, ""]
    takeup_low_risk: Float[Array, ""]
    uninsured_rate: Float[Array, ""]
    insurer_profits: Float[Array, ""]
    converged: bool
    iterations: int


@dataclass(frozen=True)
class InsuranceParams:
    """Compact insurance parameters used by glue scripts."""

    base_premium: float
    loss_cost: float
    expense_load: float
    markup: float
    adverse_selection_sensitivity: float
    price_elasticity: float


def compute_risk_premium(
    risk_probability: Float[Array, ""],
    sum_insured: float = 1.0,
    loading: float = 0.0,
) -> Float[Array, ""]:
    """
    Compute actuarially fair premium with loading.
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
    """
    p_ref = 0.1
    relative_price = premium / (p_ref + 1e-10)
    demand = jnp.power(relative_price, price_elasticity)
    demand = jnp.clip(demand, 0.0, 1.0)
    return demand


@jit
def compute_expected_profit(
    premium: Float[Array, ""],
    risk_probability: Float[Array, ""],
    sum_insured: float = 1.0,
    takeup: Float[Array, ""] = jnp.array(1.0),
) -> Float[Array, ""]:
    """
    Compute insurer expected profit per policy.
    """
    expected_claim = risk_probability * sum_insured
    profit_per_policy = premium - expected_claim
    total_profit = profit_per_policy * takeup
    return total_profit


def zero_profit_premium(
    risk_probability: Float[Array, ""],
    sum_insured: float = 1.0,
    loading: float = 0.0,
) -> Float[Array, ""]:
    """
    Compute zero-profit (actuarially fair) premium.
    """
    return compute_risk_premium(risk_probability, sum_insured, loading)


def separating_equilibrium(
    params: ModelParameters,
    risk_high: float = 0.3,
    risk_low: float = 0.1,
    proportion_high: float = 0.2,
) -> InsuranceEquilibrium:
    """
    Compute separating equilibrium (full information).
    """
    # Zero-profit premiums
    premium_high = zero_profit_premium(
        jnp.array(risk_high),
        sum_insured=1.0,
        loading=params.baseline_loading,
    )
    premium_low = zero_profit_premium(
        jnp.array(risk_low),
        sum_insured=1.0,
        loading=params.baseline_loading,
    )

    # Demand
    takeup_high = compute_demand(premium_high, price_elasticity=params.demand_elasticity_high_risk)
    takeup_low = compute_demand(premium_low)

    # Profits
    profit_high = compute_expected_profit(premium_high, jnp.array(risk_high), takeup=takeup_high)
    profit_low = compute_expected_profit(premium_low, jnp.array(risk_low), takeup=takeup_low)
    total_profit = profit_high * proportion_high + profit_low * (1 - proportion_high)

    # Takeup and uninsured rate
    overall_takeup = takeup_high * proportion_high + takeup_low * (1 - proportion_high)
    uninsured_rate = 1.0 - overall_takeup

    return InsuranceEquilibrium(
        premium_high_risk=premium_high,
        premium_low_risk=premium_low,
        takeup_high_risk=takeup_high,
        takeup_low_risk=takeup_low,
        uninsured_rate=uninsured_rate,
        insurer_profits=total_profit,
        converged=True,
        iterations=1,
    )


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
    """
    # Initial pool risk (average)
    avg_risk = proportion_high * risk_high + (1 - proportion_high) * risk_low

    def iteration_step(
        carry_converged: tuple[
            tuple[Float[Array, ""], Float[Array, ""], float, int],
            Array,
        ],
    ) -> tuple[tuple[Float[Array, ""], Float[Array, ""], float, int], Array]:
        premium, _pool_risk, prop_high, i = carry_converged[0]

        takeup_high = compute_demand(premium, price_elasticity=params.demand_elasticity_high_risk)
        takeup_low = compute_demand(premium)

        high_risk_insured = prop_high * takeup_high
        low_risk_insured = (1 - prop_high) * takeup_low
        total_insured = high_risk_insured + low_risk_insured + 1e-10

        new_prop_high = high_risk_insured / total_insured
        new_pool_risk = new_prop_high * risk_high + (1 - new_prop_high) * risk_low

        new_premium = zero_profit_premium(
            jnp.array(new_pool_risk),
            sum_insured=1.0,
            loading=params.baseline_loading,
        )

        converged = jnp.abs(new_premium - premium) < tolerance
        return (new_premium, jnp.array(new_pool_risk), new_prop_high, i + 1), converged

    initial_premium = zero_profit_premium(
        jnp.array(avg_risk), sum_insured=1.0, loading=params.baseline_loading
    )
    init_carry = (initial_premium, jnp.array(avg_risk), proportion_high, 0)

    def continue_condition(
        carry_converged: tuple[
            tuple[Float[Array, ""], Float[Array, ""], float, int],
            Array,
        ],
    ) -> Array:
        return jnp.logical_and(jnp.logical_not(carry_converged[1]), carry_converged[0][3] < max_iterations)

    (premium, pool_risk, _prop_high, n_iter), _ = lax.while_loop(
        continue_condition,
        iteration_step,
        (init_carry, jnp.array(False)),
    )

    takeup_high = compute_demand(premium, price_elasticity=params.demand_elasticity_high_risk)
    takeup_low = compute_demand(premium)
    profit = compute_expected_profit(
        premium, jnp.array(pool_risk), takeup=(takeup_high + takeup_low) / 2
    )

    overall_takeup = takeup_high * proportion_high + takeup_low * (1 - proportion_high)
    uninsured_rate = 1.0 - overall_takeup

    return InsuranceEquilibrium(
        premium_high_risk=premium,
        premium_low_risk=premium,  # Same in pooling
        takeup_high_risk=takeup_high,
        takeup_low_risk=takeup_low,
        uninsured_rate=uninsured_rate,
        insurer_profits=profit,
        converged=(n_iter < max_iterations),
        iterations=int(n_iter),
    )


def compute_equilibrium(
    params: ModelParameters,
    policy: PolicyConfig,
    risk_high: float = 0.3,
    risk_low: float = 0.1,
    proportion_high: float = 0.2,
) -> InsuranceEquilibrium:
    """
    Compute insurance equilibrium under policy regime.
    """
    if policy.allow_genetic_test_results:
        return separating_equilibrium(params, risk_high, risk_low, proportion_high)
    return pooling_equilibrium(params, risk_high, risk_low, proportion_high)


def compute_premium_divergence(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> dict[str, Float[Array, ""]]:
    """
    Compute premium divergence between policy regimes.
    """
    eq_baseline = compute_equilibrium(params, baseline_policy)
    eq_reform = compute_equilibrium(params, reform_policy)

    avg_premium_baseline = (eq_baseline.premium_high_risk + eq_baseline.premium_low_risk) / 2
    avg_premium_reform = (eq_reform.premium_high_risk + eq_reform.premium_low_risk) / 2

    absolute_divergence = avg_premium_reform - avg_premium_baseline
    relative_divergence = absolute_divergence / (avg_premium_baseline + 1e-10)

    risk_rating_baseline = eq_baseline.premium_high_risk - eq_baseline.premium_low_risk
    risk_rating_reform = eq_reform.premium_high_risk - eq_reform.premium_low_risk

    return {
        "avg_premium_baseline": avg_premium_baseline,
        "avg_premium_reform": avg_premium_reform,
        "absolute_divergence": absolute_divergence,
        "relative_divergence": relative_divergence,
        "risk_rating_baseline": risk_rating_baseline,
        "risk_rating_reform": risk_rating_reform,
    }


def get_standard_risk_parameters() -> dict[str, float]:
    """
    Get standard risk parameters for equilibrium computation.
    """
    return {
        "risk_high": 0.3,
        "risk_low": 0.1,
        "proportion_high": 0.2,
    }
