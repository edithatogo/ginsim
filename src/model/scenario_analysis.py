#!/usr/bin/env python3
"""
Scenario analysis module.

Compare policy outcomes across predefined scenarios and custom configurations.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ModelFunc = Callable[[Any, Any], Any]


@dataclass
class ScenarioResult:
    """Result from evaluating a single scenario."""

    scenario_name: str
    jurisdiction: str
    testing_uptake: float
    welfare_impact: float
    qalys_gained: float
    compliance_rate: float
    insurance_premiums: dict[str, float]
    all_metrics: dict[str, Any]


@dataclass
class ScenarioComparison:
    """Comparison of multiple scenarios."""

    baseline_scenario: str
    scenarios: list[ScenarioResult]
    delta_from_baseline: dict[str, dict[str, float]]


def _build_model_parameters(scenario_config: dict[str, Any]) -> Any:
    """Build validated ModelParameters from a scenario config."""
    from src.model.parameters import ModelParameters, PolicyConfig

    params_dict = dict(scenario_config.get("parameters", {}))
    model_fields = set(ModelParameters.model_fields)
    policy_fields = set(PolicyConfig.model_fields)

    invalid_fields = sorted(
        key for key in params_dict if key not in model_fields and key not in policy_fields
    )
    if invalid_fields:
        message = (
            "Scenario contains unsupported parameter field(s): "
            + ", ".join(invalid_fields)
            + ". Move policy controls into `policy_overrides` or remove illustrative-only fields."
        )
        raise ValueError(message)

    model_updates = {key: value for key, value in params_dict.items() if key in model_fields}
    jurisdiction = scenario_config.get("jurisdiction", "").strip().upper()
    if jurisdiction == "AU":
        model_updates.setdefault("jurisdiction", "australia")
    elif jurisdiction == "NZ":
        model_updates.setdefault("jurisdiction", "new_zealand")

    return ModelParameters(**model_updates)


def _infer_policy_id(scenario_name: str, scenario_config: dict[str, Any]) -> str:
    explicit_policy_id = scenario_config.get("policy_id")
    if explicit_policy_id:
        return str(explicit_policy_id)

    normalized_name = f"{scenario_name} {scenario_config.get('name', '')}".lower()
    if "moratorium" in normalized_name or "code" in normalized_name:
        return "moratorium"
    if "ban" in normalized_name or "gnda" in normalized_name:
        return "ban"
    return "status_quo"


def _build_policy_config(scenario_name: str, scenario_config: dict[str, Any]) -> Any:
    """Build validated PolicyConfig from scenario config."""
    from src.model.module_a_behavior import get_standard_policies

    policies = get_standard_policies()
    policy_id = _infer_policy_id(scenario_name, scenario_config)
    if policy_id not in policies:
        available = ", ".join(sorted(policies))
        msg = f"Unknown policy_id '{policy_id}'. Available policies: {available}"
        raise ValueError(msg)

    policy = policies[policy_id]
    policy_updates = dict(scenario_config.get("policy_overrides", {}))

    # Backward compatibility: allow policy fields in parameters, but only if valid.
    parameter_values = scenario_config.get("parameters", {})
    valid_policy_fields = set(type(policy).model_fields)
    for key, value in parameter_values.items():
        if key in valid_policy_fields and key not in policy_updates:
            policy_updates[key] = value

    invalid_policy_fields = sorted(key for key in policy_updates if key not in valid_policy_fields)
    if invalid_policy_fields:
        message = "Scenario contains unsupported policy override field(s): " + ", ".join(
            invalid_policy_fields
        )
        raise ValueError(message)

    return policy.model_copy(update=policy_updates)


def load_scenarios(config_path: Path | str) -> dict[str, Any]:
    """
    Load scenario definitions from YAML config.

    Args:
        config_path: Path to scenarios.yaml

    Returns:
        Dictionary of scenario definitions
    """
    config_path = Path(config_path)
    if not config_path.exists():
        msg = f"Scenario config not found: {config_path}"
        raise FileNotFoundError(msg)

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config.get("scenarios", {})


def evaluate_scenario(
    scenario_name: str,
    scenario_config: dict[str, Any],
    model_func: ModelFunc,
) -> ScenarioResult:
    """
    Evaluate a single scenario using the core model.

    Args:
        scenario_name: Name of the scenario
        scenario_config: Scenario configuration dictionary
        model_func: Model evaluation function

    Returns:
        ScenarioResult with outcomes
    """
    model_params = _build_model_parameters(scenario_config)
    policy = _build_policy_config(scenario_name, scenario_config)

    # Evaluate
    result = model_func(model_params, policy)

    # Extract metrics
    testing_uptake = float(result.testing_uptake) if hasattr(result, "testing_uptake") else 0.0
    welfare_impact = float(result.welfare_impact) if hasattr(result, "welfare_impact") else 0.0
    qalys_gained = float(result.qalys_gained) if hasattr(result, "qalys_gained") else 0.0
    compliance_rate = float(result.compliance_rate) if hasattr(result, "compliance_rate") else 0.0
    insurance_premiums = result.insurance_premiums if hasattr(result, "insurance_premiums") else {"premium_high": 0.0, "premium_low": 0.0}

    return ScenarioResult(
        scenario_name=scenario_name,
        jurisdiction=scenario_config.get("jurisdiction", "Unknown"),
        testing_uptake=testing_uptake,
        welfare_impact=welfare_impact,
        qalys_gained=qalys_gained,
        compliance_rate=compliance_rate,
        insurance_premiums=insurance_premiums,
        all_metrics={
            "testing_uptake": testing_uptake,
            "welfare_impact": welfare_impact,
            "qalys_gained": qalys_gained,
            "compliance_rate": compliance_rate,
            "insurance_premiums": insurance_premiums,
            "policy_name": policy.name,
            "policy_description": policy.description,
        },
    )


def compare_scenarios(
    scenarios: dict[str, dict[str, Any]],
    model_func: ModelFunc,
    baseline_name: str = "au_status_quo",
) -> ScenarioComparison:
    """
    Compare multiple scenarios against a baseline.

    Args:
        scenarios: Dictionary of scenario configurations
        model_func: Model evaluation function
        baseline_name: Name of baseline scenario for comparison

    Returns:
        ScenarioComparison with delta calculations
    """
    # Evaluate all scenarios
    results = []
    for name, config in scenarios.items():
        result = evaluate_scenario(name, config, model_func)
        results.append(result)

    # Find baseline
    baseline = None
    for r in results:
        if r.scenario_name == baseline_name:
            baseline = r
            break

    # Calculate deltas
    deltas = {}
    if baseline:
        for r in results:
            if r.scenario_name != baseline_name:
                deltas[r.scenario_name] = {
                    "testing_uptake_delta": r.testing_uptake - baseline.testing_uptake,
                    "welfare_delta": r.welfare_impact - baseline.welfare_impact,
                    "qalys_delta": r.qalys_gained - baseline.qalys_gained,
                    "compliance_delta": r.compliance_rate - baseline.compliance_rate,
                }

    return ScenarioComparison(
        baseline_scenario=baseline_name,
        scenarios=results,
        delta_from_baseline=deltas,
    )


def format_comparison_table(comparison: ScenarioComparison) -> str:
    """
    Format scenario comparison as markdown table.

    Args:
        comparison: ScenarioComparison object

    Returns:
        Markdown table string
    """
    lines = []

    # Header
    lines.append(
        "| Scenario | Jurisdiction | Testing Uptake | Δ vs Baseline | Welfare Impact | Compliance |",
    )
    lines.append(
        "|----------|--------------|----------------|---------------|----------------|------------|",
    )

    # Rows
    for result in comparison.scenarios:
        delta_str = ""
        if result.scenario_name in comparison.delta_from_baseline:
            delta = comparison.delta_from_baseline[result.scenario_name]["testing_uptake_delta"]
            delta_str = f"{delta:+.1%}"

        lines.append(
            f"| {result.scenario_name} | {result.jurisdiction} | "
            f"{result.testing_uptake:.1%} | {delta_str} | "
            f"${result.welfare_impact:,.0f} | {result.compliance_rate:.1%} |",
        )

    return "\n".join(lines)


def run_scenario_analysis(
    config_path: Path | str | None = None,
    model_func: ModelFunc | None = None,
    output_dir: Path | None = None,
) -> ScenarioComparison:
    """
    Run complete scenario analysis.

    Args:
        config_path: Path to scenarios.yaml (default: configs/scenarios.yaml)
        model_func: Model evaluation function
        output_dir: Optional output directory for results

    Returns:
        ScenarioComparison object
    """
    if config_path is None:
        config_path = Path(__file__).resolve().parents[2] / "configs" / "scenarios.yaml"

    if model_func is None:
        from src.model.pipeline import evaluate_single_policy as default_model_func

        model_func = default_model_func

    # Load scenarios
    scenarios = load_scenarios(config_path)

    # Run comparison
    comparison = compare_scenarios(scenarios, model_func)

    # Print results

    # Save results
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "scenario_comparison.md"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Scenario Comparison Results\n\n")
            f.write(f"**Baseline:** {comparison.baseline_scenario}\n\n")
            f.write(format_comparison_table(comparison))
            f.write("\n\n## Detailed Results\n\n")

            for result in comparison.scenarios:
                f.write(f"\n### {result.scenario_name}\n\n")
                f.write(f"- **Jurisdiction:** {result.jurisdiction}\n")
                f.write(f"- **Testing Uptake:** {result.testing_uptake:.1%}\n")
                f.write(f"- **Welfare Impact:** ${result.welfare_impact:,.0f}\n")
                f.write(f"- **QALYs Gained:** {result.qalys_gained:.2f}\n")
                f.write(f"- **Compliance Rate:** {result.compliance_rate:.1%}\n")

    return comparison
