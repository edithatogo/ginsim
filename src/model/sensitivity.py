"""
Sensitivity analysis.

One-way sensitivity and scenario analysis.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from operator import attrgetter
from pathlib import Path
from collections.abc import Callable
from typing import Any

import numpy as np


@dataclass
class SensitivityResult:
    """
    Sensitivity analysis result.

    Attributes:
        parameter: Parameter name
        base_value: Base case value
        range: Tested range (low, high)
        impact: Impact on outcome (low_outcome, high_outcome)
        sensitivity_index: Normalized sensitivity index
    """

    parameter: str
    base_value: float
    range: tuple[float, float]
    impact: tuple[float, float]
    sensitivity_index: float


def one_way_sensitivity(
    model_func: Callable[[dict[str, float]], float],
    base_params: dict[str, float],
    parameter_name: str,
    range_pct: float = 0.25,
    n_points: int = 10,
) -> SensitivityResult:
    """
    Run one-way sensitivity analysis.

    Args:
        model_func: Model function that takes parameters and returns outcome
        base_params: Base case parameters
        parameter_name: Parameter to vary
        range_pct: Percentage variation (e.g., 0.25 = ±25%)
        n_points: Number of points to evaluate

    Returns:
        SensitivityResult object
    """
    base_value = base_params[parameter_name]
    low = base_value * (1 - range_pct)
    high = base_value * (1 + range_pct)

    # Evaluate at multiple points
    test_values = np.linspace(low, high, n_points)
    outcomes = []

    for value in test_values:
        params = base_params.copy()
        params[parameter_name] = value
        outcome = model_func(params)
        outcomes.append(outcome)

    outcomes = np.array(outcomes)

    # Sensitivity index (normalized)
    outcome_range = np.max(outcomes) - np.min(outcomes)
    base_outcome = model_func(base_params)

    if base_outcome != 0:
        sensitivity_index = outcome_range / abs(base_outcome)
    else:
        sensitivity_index = outcome_range

    return SensitivityResult(
        parameter=parameter_name,
        base_value=base_value,
        range=(low, high),
        impact=(float(np.min(outcomes)), float(np.max(outcomes))),
        sensitivity_index=float(sensitivity_index),
    )


def tornado_analysis(
    model_func: Callable[[dict[str, float]], float],
    base_params: dict[str, float],
    parameters: list[str],
    range_pct: float = 0.25,
) -> list[SensitivityResult]:
    """
    Run tornado (multi-parameter one-way) sensitivity analysis.

    Args:
        model_func: Model function
        base_params: Base case parameters
        parameters: List of parameters to analyze
        range_pct: Percentage variation

    Returns:
        List of SensitivityResult objects, sorted by sensitivity
    """
    results = []

    for param in parameters:
        result = one_way_sensitivity(
            model_func,
            base_params,
            param,
            range_pct,
        )
        results.append(result)

    # Sort by sensitivity index (descending)
    results.sort(key=attrgetter("sensitivity_index"), reverse=True)

    return results


def scenario_analysis(
    model_func: Callable[[dict[str, float]], float],
    base_params: dict[str, float],
    scenarios: dict[str, dict[str, float]],
) -> dict[str, Any]:
    """
    Run scenario analysis.

    Args:
        model_func: Model function
        base_params: Base case parameters
        scenarios: Dictionary of scenario names to parameter overrides

    Returns:
        Dictionary of scenario results
    """
    results = {}

    # Base case
    base_outcome = model_func(base_params)
    results["base"] = {
        "outcome": base_outcome,
        "params": base_params,
    }

    # Scenarios
    for scenario_name, overrides in scenarios.items():
        scenario_params = base_params.copy()
        scenario_params.update(overrides)

        outcome = model_func(scenario_params)
        change = (outcome - base_outcome) / abs(base_outcome) if base_outcome != 0 else 0

        results[scenario_name] = {
            "outcome": outcome,
            "change_from_base": change,
            "params": scenario_params,
        }

    return results


def format_sensitivity_results(
    results: list[SensitivityResult],
) -> str:
    """
    Format sensitivity results as table.

    Args:
        results: List of SensitivityResult objects

    Returns:
        Formatted table string
    """
    from tabulate import tabulate

    headers = ["Parameter", "Base", "Range", "Impact", "Sensitivity"]

    rows = []
    for result in results:
        rows.append(
            [
                result.parameter,
                f"{result.base_value:.3f}",
                f"{result.range[0]:.3f} - {result.range[1]:.3f}",
                f"{result.impact[0]:.2f} - {result.impact[1]:.2f}",
                f"{result.sensitivity_index:.3f}",
            ]
        )

    return tabulate(rows, headers=headers, tablefmt="grid")


def save_sensitivity_results(
    results: list[SensitivityResult],
    output_path: str | Path,
) -> None:
    """
    Save sensitivity results to JSON file.

    Args:
        results: List of SensitivityResult objects
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results_dict = []
    for result in results:
        results_dict.append(
            {
                "parameter": result.parameter,
                "base_value": result.base_value,
                "range": result.range,
                "impact": result.impact,
                "sensitivity_index": result.sensitivity_index,
            }
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_dict, f, indent=2)
