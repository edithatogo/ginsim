#!/usr/bin/env python3
"""
Comprehensive sensitivity analysis with JAX acceleration.

Includes:
- Tornado diagrams (one-way sensitivity)
- Heat maps (two-way sensitivity)
- Sobol indices (global sensitivity)
- CEAC (cost-effectiveness acceptability curves)
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jax
import jax.numpy as jnp
from jax import jit, vmap
from jaxtyping import Array, Float, Int


ModelFunc = Callable[[Float[Array, ...]], Any]
CostEffectModelFunc = Callable[[Float[Array, ...], Float[Array, ...]], tuple[Any, Any]]


@dataclass
class TornadoResult:
    """Tornado diagram result for single parameter."""

    parameter: str
    base_value: float
    low_value: float
    high_value: float
    low_outcome: float
    high_outcome: float
    sensitivity_magnitude: float


@dataclass
class HeatMapResult:
    """Two-way sensitivity heat map result."""

    param1_name: str
    param2_name: str
    param1_values: Array
    param2_values: Array
    outcomes: Array  # 2D array [param1, param2]
    min_outcome: float
    max_outcome: float


@dataclass
class SobolResult:
    """Sobol sensitivity indices."""

    parameter: str
    first_order: float  # S_i: Main effect
    total_order: float  # S_Ti: Total effect (including interactions)
    second_order: dict[str, float] | None = None  # S_ij: Second-order interactions


@dataclass
class CEACResult:
    """Cost-effectiveness acceptability curve result."""

    thresholds: Array  # Willingness-to-pay thresholds
    probabilities: Array  # Probability of cost-effectiveness at each threshold
    optimal_policy: str  # Optimal policy name


@jit
def _evaluate_model_jax(
    model_func: ModelFunc,
    params_batch: Float[Array, ...],
    param_indices: Int[Array, ...],
    param_values: Float[Array, ...],
) -> Float[Array, ...]:
    """
    Evaluate model with JAX for sensitivity analysis.

    Args:
        model_func: Model function to evaluate
        params_batch: Base parameter values
        param_indices: Which parameter to vary (integer indices)
        param_values: Values to set for varied parameters

    Returns:
        Model outcomes for each evaluation
    """

    def single_eval(idx_val: Array) -> Any:
        idx, val = idx_val
        params = params_batch.at[idx].set(val)
        return model_func(params)

    return vmap(single_eval)(jnp.stack([param_indices, param_values], axis=1))


def tornado_sensitivity(
    model_func: ModelFunc,
    base_params: Float[Array, ...],
    param_names: list[str],
    param_indices: list[int],
    range_pct: float = 0.25,
    n_points: int = 5,
) -> list[TornadoResult]:
    """
    Run tornado (one-way) sensitivity analysis with JAX.

    Args:
        model_func: JAX-compatible model function
        base_params: Base parameter values as JAX array
        param_names: Names of parameters to vary
        param_indices: Indices of parameters to vary
        range_pct: Percentage variation (e.g., 0.25 = ±25%)
        n_points: Number of points to evaluate per parameter

    Returns:
        List of TornadoResult objects, sorted by sensitivity magnitude
    """
    results = []

    # Get base outcome
    _ = float(model_func(base_params))

    for name, idx in zip(param_names, param_indices):
        base_value = float(base_params[idx])
        low = base_value * (1 - range_pct)
        high = base_value * (1 + range_pct)

        # Evaluate at extremes
        test_values = jnp.linspace(low, high, n_points)
        test_indices = jnp.full(n_points, idx, dtype=jnp.int32)

        # Vectorized evaluation
        outcomes = _evaluate_model_jax(
            model_func,
            base_params,
            test_indices,
            test_values,
        )

        low_outcome = float(jnp.min(outcomes))
        high_outcome = float(jnp.max(outcomes))
        sensitivity_magnitude = high_outcome - low_outcome

        results.append(
            TornadoResult(
                parameter=name,
                base_value=base_value,
                low_value=low,
                high_value=high,
                low_outcome=low_outcome,
                high_outcome=high_outcome,
                sensitivity_magnitude=sensitivity_magnitude,
            ),
        )

    def sensitivity_key(result: TornadoResult) -> float:
        return result.sensitivity_magnitude

    # Sort by sensitivity magnitude (descending)
    results.sort(key=sensitivity_key, reverse=True)

    return results


def twoway_sensitivity(
    model_func: ModelFunc,
    base_params: Float[Array, ...],
    param1_idx: int,
    param2_idx: int,
    param1_range: tuple[float, float],
    param2_range: tuple[float, float],
    n_points: int = 20,
) -> HeatMapResult:
    """
    Run two-way sensitivity analysis with JAX.

    Args:
        model_func: JAX-compatible model function
        base_params: Base parameter values
        param1_idx: Index of first parameter
        param2_idx: Index of second parameter
        param1_range: Range for first parameter (low, high)
        param2_range: Range for second parameter (low, high)
        n_points: Number of points per dimension

    Returns:
        HeatMapResult with 2D outcome grid
    """
    # Create parameter grids
    param1_values = jnp.linspace(*param1_range, n_points)
    param2_values = jnp.linspace(*param2_range, n_points)

    # Create meshgrid
    p1_grid, p2_grid = jnp.meshgrid(param1_values, param2_values, indexing="ij")

    # Flatten for batch evaluation
    p1_flat = p1_grid.ravel()
    p2_flat = p2_grid.ravel()

    # Create parameter batches
    def evaluate_pair(p1_val: Any, p2_val: Any) -> Any:
        params = base_params.at[param1_idx].set(p1_val).at[param2_idx].set(p2_val)
        return model_func(params)

    # Vectorized evaluation
    outcomes = vmap(evaluate_pair)(p1_flat, p2_flat)
    outcomes_grid = outcomes.reshape(n_points, n_points)

    return HeatMapResult(
        param1_name=f"param_{param1_idx}",
        param2_name=f"param_{param2_idx}",
        param1_values=param1_values,
        param2_values=param2_values,
        outcomes=outcomes_grid,
        min_outcome=float(jnp.min(outcomes_grid)),
        max_outcome=float(jnp.max(outcomes_grid)),
    )


def sobol_sensitivity(
    model_func: ModelFunc,
    base_params: Float[Array, ...],
    param_names: list[str],
    param_indices: list[int],
    n_samples: int = 1000,
    seed: int = 42,
) -> list[SobolResult]:
    """
    Estimate Sobol sensitivity indices using JAX.

    Uses Saltelli's sampling scheme for efficient estimation.

    Args:
        model_func: JAX-compatible model function
        base_params: Base parameter values
        param_names: Names of parameters
        param_indices: Indices of parameters to analyze
        n_samples: Number of Monte Carlo samples
        seed: Random seed

    Returns:
        List of SobolResult with first and total order indices
    """
    key = jax.random.PRNGKey(seed)
    n_params = len(param_indices)

    # Generate samples from uniform distribution [0, 1]
    # For proper Sobol analysis, you'd use Sobol sequences
    # Here we use pseudo-random for simplicity
    key, subkey = jax.random.split(key)
    A = jax.random.uniform(subkey, (n_samples, n_params))

    key, subkey = jax.random.split(key)
    B = jax.random.uniform(subkey, (n_samples, n_params))

    # Build parameter matrices
    # A and B are the base sample matrices
    # A_B^i is matrix A with column i replaced by column i from B

    # Evaluate model at A and B
    def params_from_scaled(scaled: Float[Array, n_params]) -> Float[Array, n_params]:
        """Convert [0,1] scaled params to actual values (assuming ±25% range)."""
        result = base_params.copy()
        for i, idx in enumerate(param_indices):
            base_val = float(base_params[idx])
            result = result.at[idx].set(base_val * (0.75 + 0.5 * scaled[i]))
        return result

    A_params = jax.vmap(params_from_scaled)(A)
    B_params = jax.vmap(params_from_scaled)(B)

    f_A = jax.vmap(model_func)(A_params)
    f_B = jax.vmap(model_func)(B_params)

    # Build A_B matrices and evaluate using JAX-friendly operations
    f_A_B = []
    for i in range(n_params):
        # Use JAX-friendly column replacement with where
        mask = jnp.arange(n_params)[None, :] == i
        A_B = jnp.where(mask, B, A)
        A_B_params = jax.vmap(params_from_scaled)(A_B)
        f_A_B.append(jax.vmap(model_func)(A_B_params))

    f_A_B = jnp.stack(f_A_B, axis=1)  # [n_samples, n_params]

    # Calculate Sobol indices using Saltelli's estimator
    # Total variance (pooled)
    var_total = jnp.var(jnp.concatenate([f_A, f_B]))

    results = []
    for i in range(n_params):
        # First-order index using Saltelli's estimator:
        # S_i = Var[E(Y|X_i)] / Var(Y)
        # Approximated as: (1/N) * sum(f_B * (f_A_B_i - f_A)) / var_total
        numerator = jnp.mean(f_B * (f_A_B[:, i] - f_A))
        first_order = float(numerator / var_total) if var_total > 0 else 0.0

        # Total-order index: S_Ti = (1/2N) * sum((f_A - f_A_B_i)^2) / var_total
        numerator_total = 0.5 * jnp.mean((f_A - f_A_B[:, i]) ** 2)
        total_order = float(numerator_total / var_total) if var_total > 0 else 0.0

        # Clip to valid range [0, 1] to handle numerical errors
        results.append(
            SobolResult(
                parameter=param_names[i],
                first_order=float(jnp.clip(first_order, 0.0, 1.0)),
                total_order=float(jnp.clip(total_order, 0.0, 1.0)),
            ),
        )

    return results


def ceac_analysis(
    model_func: CostEffectModelFunc,
    base_params: Float[Array, ...],
    policies: list[str],
    policy_params: list[Float[Array, ...]],
    thresholds: Float[Array, ...],
    n_draws: int = 1000,
    seed: int = 42,
) -> CEACResult:
    """
    Generate cost-effectiveness acceptability curve with JAX.

    Args:
        model_func: JAX-compatible model function returning (costs, effects)
        base_params: Base parameter values
        policies: Names of policies to compare
        policy_params: Parameter sets for each policy
        thresholds: Willingness-to-pay thresholds to evaluate
        n_draws: Number of Monte Carlo draws
        seed: Random seed

    Returns:
        CEACResult with probabilities and optimal policies
    """
    key = jax.random.PRNGKey(seed)
    n_policies = len(policies)

    # Generate parameter draws (probabilistic sensitivity analysis)
    key, subkey = jax.random.split(key)

    # Assume ±20% uncertainty on parameters (adjust as needed)
    uncertainty_scale = 0.20
    draws = jax.random.normal(subkey, (n_draws, len(base_params)))
    param_draws = base_params * (1 + uncertainty_scale * draws)

    # Evaluate all policies for all draws
    costs_all = []
    effects_all = []

    for policy_params_set in policy_params:
        # Create a closure that binds the current policy_params_set
        def make_eval_single(
            pps: Float[Array, ...],
        ) -> Callable[[Float[Array, ...]], tuple[Any, Any]]:
            def eval_single(params: Float[Array, ...]) -> tuple[Any, Any]:
                cost, effect = model_func(params, pps)
                return cost, effect

            return eval_single

        eval_fn = make_eval_single(policy_params_set)
        costs, effects = jax.vmap(eval_fn)(param_draws)
        costs_all.append(costs)
        effects_all.append(effects)

    costs_all = jnp.stack(costs_all, axis=1)  # [n_draws, n_policies]
    effects_all = jnp.stack(effects_all, axis=1)  # [n_draws, n_policies]

    # Calculate net benefit for first threshold (simplified for single threshold)
    if len(thresholds) > 0:
        threshold = thresholds[0]
        # Net benefit = effect * threshold - cost
        net_benefit = effects_all * threshold - costs_all  # [n_draws, n_policies]

        # Find optimal policy for each draw
        optimal = jnp.argmax(net_benefit, axis=1)  # [n_draws]

        # Count probability each policy is optimal using bincount
        optimal_counts = jnp.bincount(optimal, length=n_policies)
        probs = optimal_counts / n_draws

        # Find policy with highest expected net benefit
        expected_net_benefit = jnp.mean(net_benefit, axis=0)
        optimal_policy_idx = int(jnp.argmax(expected_net_benefit))
        optimal_policy = policies[optimal_policy_idx]
    else:
        probs = jnp.zeros(n_policies)
        optimal_policy = policies[0]

    return CEACResult(
        thresholds=thresholds,
        probabilities=probs,
        optimal_policy=optimal_policy,
    )


def save_sensitivity_results(
    tornado_results: list[TornadoResult] | None = None,
    sobol_results: list[SobolResult] | None = None,
    output_path: Path | str | None = None,
) -> None:
    """
    Save sensitivity analysis results to JSON.

    Args:
        tornado_results: Tornado analysis results
        sobol_results: Sobol index results
        output_path: Output file path
    """
    if output_path is None:
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results_dict = {}

    if tornado_results:
        results_dict["tornado"] = [
            {
                "parameter": r.parameter,
                "base_value": r.base_value,
                "low_value": r.low_value,
                "high_value": r.high_value,
                "low_outcome": r.low_outcome,
                "high_outcome": r.high_outcome,
                "sensitivity_magnitude": r.sensitivity_magnitude,
            }
            for r in tornado_results
        ]

    if sobol_results:
        results_dict["sobol"] = [
            {
                "parameter": r.parameter,
                "first_order": float(r.first_order),
                "total_order": float(r.total_order),
            }
            for r in sobol_results
        ]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_dict, f, indent=2)


# Convenience function for complete sensitivity analysis
def run_comprehensive_sensitivity(
    model_func: ModelFunc,
    base_params: Float[Array, ...],
    param_names: list[str],
    param_indices: list[int],
    output_dir: Path | None = None,
    n_sobol_samples: int = 500,
) -> dict[str, Any]:
    """
    Run comprehensive sensitivity analysis.

    Args:
        model_func: JAX-compatible model function
        base_params: Base parameter values
        param_names: Names of parameters to analyze
        param_indices: Indices of parameters
        output_dir: Optional output directory for results
        n_sobol_samples: Number of samples for Sobol analysis

    Returns:
        Dictionary with 'tornado' and 'sobol' keys containing result lists
    """
    results = {}

    print("Running tornado sensitivity analysis...")
    tornado = tornado_sensitivity(model_func, base_params, param_names, param_indices)
    results["tornado"] = tornado
    print("  Top 3 most sensitive parameters:")
    for i, r in enumerate(tornado[:3]):
        print(f"    {i + 1}. {r.parameter}: {r.sensitivity_magnitude:.4f}")

    print("\nRunning Sobol global sensitivity analysis...")
    sobol = sobol_sensitivity(
        model_func,
        base_params,
        param_names,
        param_indices,
        n_samples=n_sobol_samples,
    )
    results["sobol"] = sobol
    print("  Top 3 by first-order index:")
    for i, r in enumerate(sorted(sobol, key=lambda x: x.first_order, reverse=True)[:3]):
        print(f"    {i + 1}. {r.parameter}: S={r.first_order:.3f}, S_T={r.total_order:.3f}")

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        save_sensitivity_results(
            tornado_results=tornado,
            sobol_results=sobol,
            output_path=output_dir / "sensitivity_results.json",
        )
        print(f"\nResults saved to {output_dir / 'sensitivity_results.json'}")

    return results
