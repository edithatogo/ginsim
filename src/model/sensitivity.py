"""
Sensitivity Analysis: One-way and Tornado Analysis.

This module provides tools for quantifying the impact of parameter uncertainty
on model outcomes using one-way sensitivity and tornado analysis.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .parameters import ModelParameters, PolicyConfig


@dataclass(frozen=True)
class SensitivityResult:
    """Represents the result of a sensitivity analysis for one parameter."""

    parameter_name: str
    base_value: float
    lower_value: float
    upper_value: float
    base_outcome: float
    lower_outcome: float
    upper_outcome: float
    sensitivity_index: float


def run_one_way_sensitivity(model_fn, params, name, variation=0.2):
    """Legacy alias for one_way_sensitivity."""
    return one_way_sensitivity(model_fn, params, name, variation=variation)


def one_way_sensitivity(
    model_fn: Callable[[ModelParameters], float],
    params: ModelParameters,
    param_name: str,
    variation: float = 0.2,
) -> SensitivityResult:
    """
    Run one-way sensitivity analysis for a single parameter.
    """
    base_val = getattr(params, param_name)
    lower_val = base_val * (1.0 - variation)
    upper_val = base_val * (1.0 + variation)

    # Base outcome
    base_outcome = model_fn(params)

    # Lower bound outcome
    params_low = params.model_copy(update={param_name: lower_val})
    lower_outcome = model_fn(params_low)

    # Upper bound outcome
    params_high = params.model_copy(update={param_name: upper_val})
    upper_outcome = model_fn(params_high)

    # Sensitivity index (normalized delta)
    total_swing = abs(upper_outcome - lower_outcome)
    sensitivity_index = total_swing / (abs(base_outcome) + 1e-10)

    return SensitivityResult(
        parameter_name=param_name,
        base_value=float(base_val),
        lower_value=float(lower_val),
        upper_value=float(upper_val),
        base_outcome=float(base_outcome),
        lower_outcome=float(lower_outcome),
        upper_outcome=float(upper_outcome),
        sensitivity_index=float(sensitivity_index),
    )


def tornado_analysis(
    model_fn: Callable[[ModelParameters], float],
    params: ModelParameters,
    param_names: list[str],
    variation: float = 0.2,
) -> list[SensitivityResult]:
    """
    Run sensitivity analysis across multiple parameters and sort by impact.
    """
    results = []
    for name in param_names:
        results.append(one_way_sensitivity(model_fn, params, name, variation))

    # Sort by sensitivity index descending
    return sorted(results, key=lambda x: x.sensitivity_index, reverse=True)


def scenario_analysis(
    model_fn: Callable[[ModelParameters, PolicyConfig], float],
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> dict[str, float]:
    """
    Evaluate outcomes under two different policy scenarios.
    """
    baseline_outcome = model_fn(params, baseline_policy)
    reform_outcome = model_fn(params, reform_policy)

    return {
        "baseline_outcome": float(baseline_outcome),
        "reform_outcome": float(reform_outcome),
        "delta": float(reform_outcome - baseline_outcome),
        "percentage_change": float(
            (reform_outcome / baseline_outcome - 1.0) if baseline_outcome != 0 else 0
        ),
    }
