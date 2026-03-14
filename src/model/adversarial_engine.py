"""
Adversarial Engine: Economic Red-Teaming (Diamond Standard).

Uses JAX and Optax to find the "Worst-Case Scenario" parameter combinations
that collapse a given policy's economic performance.
"""

from __future__ import annotations

from functools import partial
from typing import Any, NamedTuple

import jax
import jax.numpy as jnp
import optax
from loguru import logger

from . import dcba_ledger as dcba
from . import module_a_behavior as mod_a
from . import module_c_insurance_eq as mod_c
from .parameters import ModelParameters, PolicyConfig


class AdversarialResult(NamedTuple):
    """Result of an adversarial optimization run.

    Attributes:
        worst_case_theta: dict of raw optimizer variables and mapped outcomes.
        worst_case_params: ModelParameters object with optimized values.
        min_welfare_delta: The minimum welfare difference found ($M).
        optimization_steps: Number of steps performed.
        success: Whether the optimization converged without NaNs.
        loss_history: List of welfare deltas across steps.
        reform_welfare_result: DCBAResult for the reform policy.
        baseline_welfare_result: DCBAResult for the baseline policy.
    """

    worst_case_theta: dict[str, float]
    worst_case_params: ModelParameters
    min_welfare_delta: float
    optimization_steps: int
    success: bool
    loss_history: list[float] | None = None
    reform_welfare_result: Any = None
    baseline_welfare_result: Any = None


def parameter_mapping(
    theta: dict[str, Any], base_params: ModelParameters
) -> tuple[ModelParameters, dict[str, Any]]:
    """
    Map unbounded optimizer variables (theta) to bounded model parameters.

    Args:
        theta: Dictionary of optimizer tracers/variables.
        base_params: Base ModelParameters to copy from.

    Returns:
        tuple of (Updated ModelParameters, Dictionary of risk-specific parameters).
    """
    prop_high = jax.nn.sigmoid(theta.get("proportion_high", 0.0)) * 0.5
    risk_low = jax.nn.sigmoid(theta.get("risk_low", -1.0)) * 0.4
    risk_high = risk_low + jax.nn.softplus(theta.get("risk_high_delta", 0.0))
    risk_high = jnp.minimum(risk_high, 0.8)

    elasticity_high = -jax.nn.softplus(theta.get("demand_elasticity_high_risk", 0.0))
    as_elasticity = -jax.nn.softplus(theta.get("adverse_selection_elasticity", 0.0))

    loading = jax.nn.sigmoid(theta.get("baseline_loading", 0.0)) * 1.0
    mor_effect = jax.nn.sigmoid(theta.get("moratorium_effect", 0.0))

    new_params = base_params.model_copy(
        {
            "demand_elasticity_high_risk": elasticity_high,
            "adverse_selection_elasticity": as_elasticity,
            "baseline_loading": loading,
            "moratorium_effect": mor_effect,
        }
    )

    risk_params = {"risk_high": risk_high, "risk_low": risk_low, "proportion_high": prop_high}

    return new_params, risk_params


def evaluate_welfare_pure(
    params: ModelParameters,
    policy: PolicyConfig,
    risk_params: dict[str, Any],
    n_individuals: int = 500,
    baseline_policy: PolicyConfig | None = None,
) -> Any:
    """
    Differentiable welfare calculation (Pure JAX).

    Args:
        params: ModelParameters to use.
        policy: PolicyConfig to evaluate.
        risk_params: Risk profile (prevalence, costs).
        n_individuals: Population size for Monte Carlo.
        baseline_policy: Optional baseline for relative calculation.

    Returns:
        DCBAResult or scalar welfare.
    """
    uptake = mod_a.compute_testing_uptake(params, policy, n_individuals=n_individuals)
    market_eq = mod_c.compute_equilibrium(
        params,
        policy,
        risk_high=risk_params["risk_high"],
        risk_low=risk_params["risk_low"],
        proportion_high=risk_params["proportion_high"],
    )

    if baseline_policy is not None:
        b_uptake = mod_a.compute_testing_uptake(
            params, baseline_policy, n_individuals=n_individuals
        )
        b_eq = mod_c.compute_equilibrium(
            params,
            baseline_policy,
            risk_high=risk_params["risk_high"],
            risk_low=risk_params["risk_low"],
            proportion_high=risk_params["proportion_high"],
        )
        base_uptake, base_premium, base_profits = b_uptake, b_eq.premium_high, b_eq.insurer_profits
    else:
        base_uptake, base_premium, base_profits = (
            jnp.asarray(params.baseline_testing_uptake),
            0.161,
            0.057,
        )

    return dcba.compute_dcba(
        testing_uptake=uptake,
        baseline_uptake=base_uptake,
        insurance_premium=market_eq.premium_high,
        baseline_premium=base_premium,
        insurer_profits=market_eq.insurer_profits,
        baseline_profits=base_profits,
        research_value_loss=0.0,
        ppp_conversion_factor=params.ppp_conversion_factor,
        equity_factor=params.equity_factor,
        value_per_qaly=params.pharmac_qaly_threshold,
        setup_cost=params.compliance_cost_fixed,
        time_horizon=20,
        is_annual=False,
    )


def objective_function(theta, base_params, policy, baseline_policy, n_individuals=500):
    """Objective: Minimize (Welfare_Reform - Welfare_Baseline)."""
    params, risk_params = parameter_mapping(theta, base_params)
    res_reform = evaluate_welfare_pure(
        params, policy, risk_params, n_individuals=n_individuals, baseline_policy=None
    )
    res_base = evaluate_welfare_pure(
        params, baseline_policy, risk_params, n_individuals=n_individuals, baseline_policy=None
    )

    diff = res_reform.net_welfare - res_base.net_welfare
    return jnp.where(jnp.isnan(diff), 1e9, diff)


class AdversarialEngine:
    """Production wrapper for economic red-teaming."""

    def __init__(self, learning_rate: float = 0.05, steps: int = 150, n_individuals: int = 500):
        self.learning_rate = learning_rate
        self.steps = steps
        self.n_individuals = n_individuals

    def find_worst_case(
        self, policy: PolicyConfig, baseline_policy: PolicyConfig, base_params: ModelParameters
    ) -> AdversarialResult:
        """Find the parameter set that makes policy perform worst relative to baseline."""
        logger.info(f"ADVERSARIAL: Stress testing '{policy.name}' vs '{baseline_policy.name}'")

        initial_theta = {
            "proportion_high": 0.0,
            "risk_low": -1.0,
            "risk_high_delta": 0.0,
            "demand_elasticity_high_risk": 0.0,
            "adverse_selection_elasticity": 0.0,
            "baseline_loading": 0.0,
            "moratorium_effect": 0.0,
        }

        optimizer = optax.adam(self.learning_rate)
        opt_state = optimizer.init(initial_theta)

        obj_fn = partial(
            objective_function,
            base_params=base_params,
            policy=policy,
            baseline_policy=baseline_policy,
            n_individuals=self.n_individuals,
        )

        def step_fn_with_history(state, _):
            theta, opt_state = state
            loss, grads = jax.value_and_grad(obj_fn)(theta)
            updates, opt_state = optimizer.update(grads, opt_state)
            theta = optax.apply_updates(theta, updates)
            return (theta, opt_state), (theta, loss)

        init_state = (initial_theta, opt_state)

        (_final_theta, _final_opt_state), (theta_history, losses) = jax.jit(
            lambda s: jax.lax.scan(step_fn_with_history, s, None, length=self.steps)
        )(init_state)

        min_idx = int(jnp.argmin(losses))
        best_theta_pytree = jax.tree_util.tree_map(lambda x: x[min_idx], theta_history)
        min_loss = float(losses[min_idx])

        worst_params, risk_params = parameter_mapping(best_theta_pytree, base_params)

        # Calculate full results for the best theta
        best_res_reform = evaluate_welfare_pure(
            worst_params, policy, risk_params, n_individuals=self.n_individuals
        )
        best_res_base = evaluate_welfare_pure(
            worst_params, baseline_policy, risk_params, n_individuals=self.n_individuals
        )

        best_results = {k: float(v) for k, v in best_theta_pytree.items()}
        mapped_results = {
            "final_proportion_high": float(risk_params["proportion_high"]),
            "final_risk_high": float(risk_params["risk_high"]),
            "final_risk_low": float(risk_params["risk_low"]),
            "final_loading": float(worst_params.baseline_loading),
            "final_demand_elasticity_high": float(worst_params.demand_elasticity_high_risk),
            "final_as_elasticity": float(worst_params.adverse_selection_elasticity),
        }
        best_results.update(mapped_results)

        return AdversarialResult(
            worst_case_theta=best_results,
            worst_case_params=worst_params,
            min_welfare_delta=min_loss,
            optimization_steps=self.steps,
            success=not jnp.isnan(min_loss),
            loss_history=[float(x) for x in losses],
            reform_welfare_result=best_res_reform,
            baseline_welfare_result=best_res_base,
        )

    def run_policy_comparison(
        self,
        policies: list[PolicyConfig],
        baseline_policy: PolicyConfig,
        base_params: ModelParameters,
    ) -> dict[str, AdversarialResult]:
        """Run stress tests for multiple policies."""
        results = {}
        for policy in policies:
            if policy.name == baseline_policy.name:
                continue
            results[policy.name] = self.find_worst_case(policy, baseline_policy, base_params)
        return results
