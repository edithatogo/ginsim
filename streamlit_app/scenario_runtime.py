"""
Resilient scenario helpers for Streamlit pages.

These pages only need a narrow slice of the full scenario-analysis surface.
Keeping that slice here avoids breaking public routes when non-UI scenario
helpers change or become fragile at import time in hosted runtimes.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

from src.utils.yaml_compat import load_yaml_path


@dataclass
class ScenarioRuntimeResult:
    """Minimal scenario result surface used by the Streamlit pages."""

    scenario_name: str
    jurisdiction: str
    testing_uptake: Any
    welfare_impact: Any
    equity_weighted_welfare: Any
    compliance_rate: Any
    insurance_premiums: dict[str, Any]
    all_metrics: dict[str, Any]


def load_scenarios(config_path: Path | str) -> dict[str, dict[str, Any]]:
    """Load scenario definitions from a YAML config file."""
    resolved_path = Path(config_path)
    if not resolved_path.exists():
        msg = f"Scenario config not found: {resolved_path}"
        raise FileNotFoundError(msg)

    config = load_yaml_path(resolved_path) or {}
    scenarios = config.get("scenarios", {})
    return scenarios if isinstance(scenarios, dict) else {}


def get_scenario_display_name(scenario_name: str, scenario_config: dict[str, Any]) -> str:
    """Return a stable user-facing scenario label."""
    explicit_name = scenario_config.get("name")
    if isinstance(explicit_name, str) and explicit_name.strip():
        return explicit_name
    return scenario_name.replace("_", " ").title()


def filter_scenarios_by_jurisdiction(
    scenarios: dict[str, dict[str, Any]],
    jurisdiction_code: str,
) -> dict[str, dict[str, Any]]:
    """Return only scenarios for the requested jurisdiction."""
    normalized_code = jurisdiction_code.strip().upper()
    return {
        name: config
        for name, config in scenarios.items()
        if str(config.get("jurisdiction", "")).strip().upper() == normalized_code
    }


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


def _build_model_parameters(scenario_config: dict[str, Any]) -> Any:
    from src.model.parameters import ModelParameters, PolicyConfig, load_jurisdiction_parameters

    params_dict = dict(scenario_config.get("parameters", {}))

    jurisdiction_code = str(scenario_config.get("jurisdiction", "AU")).strip().upper()
    jurisdiction_map = {
        "AU": "australia",
        "NZ": "new_zealand",
        "UK": "uk",
        "CA": "canada",
        "US": "us",
    }
    jurisdiction_id = jurisdiction_map.get(jurisdiction_code, "australia")
    base_params = load_jurisdiction_parameters(jurisdiction_id)

    model_field_names = {field.name for field in fields(ModelParameters)}
    policy_field_names = {field.name for field in fields(PolicyConfig)}
    invalid_fields = sorted(
        key for key in params_dict if key not in model_field_names and key not in policy_field_names
    )
    if invalid_fields:
        message = (
            "Scenario contains unsupported parameter field(s): "
            + ", ".join(invalid_fields)
            + ". Move policy controls into `policy_overrides` or remove illustrative-only fields."
        )
        raise ValueError(message)

    model_updates = {key: value for key, value in params_dict.items() if key in model_field_names}
    return base_params.model_copy(update=model_updates)


def _build_policy_config(scenario_name: str, scenario_config: dict[str, Any]) -> Any:
    from src.model.module_a_behavior import get_standard_policies
    from src.model.parameters import PolicyConfig

    policies = get_standard_policies()
    policy_id = _infer_policy_id(scenario_name, scenario_config)
    if policy_id not in policies:
        available = ", ".join(sorted(policies))
        msg = f"Unknown policy_id '{policy_id}'. Available policies: {available}"
        raise ValueError(msg)

    policy = policies[policy_id]
    policy_updates = dict(scenario_config.get("policy_overrides", {}))
    parameter_values = scenario_config.get("parameters", {})
    valid_policy_fields = {field.name for field in fields(PolicyConfig)}

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


def evaluate_scenario(
    scenario_name: str,
    scenario_config: dict[str, Any],
    model_func,
) -> ScenarioRuntimeResult:
    """Evaluate a single scenario for Streamlit comparison surfaces."""
    model_params = _build_model_parameters(scenario_config)
    policy = _build_policy_config(scenario_name, scenario_config)
    result = model_func(model_params, policy)

    testing_uptake = result.testing_uptake if hasattr(result, "testing_uptake") else 0.0
    welfare_impact = result.welfare_impact if hasattr(result, "welfare_impact") else 0.0
    equity_weighted_welfare = (
        result.equity_weighted_welfare if hasattr(result, "equity_weighted_welfare") else 0.0
    )
    compliance_rate = result.compliance_rate if hasattr(result, "compliance_rate") else 0.0
    insurance_premiums = (
        result.insurance_premiums
        if hasattr(result, "insurance_premiums")
        else {"premium_high": 0.0, "premium_low": 0.0}
    )

    info_gap = 0.0
    if hasattr(result, "proxy_effects"):
        info_gap = float(result.proxy_effects.get("residual_information_gap", 0.0))
    elif hasattr(result, "all_metrics"):
        info_gap = float(result.all_metrics.get("proxy", {}).get("residual_information_gap", 0.0))

    return ScenarioRuntimeResult(
        scenario_name=scenario_name,
        jurisdiction=str(scenario_config.get("jurisdiction", "Unknown")),
        testing_uptake=testing_uptake,
        welfare_impact=welfare_impact,
        equity_weighted_welfare=equity_weighted_welfare,
        compliance_rate=compliance_rate,
        insurance_premiums=insurance_premiums,
        all_metrics={
            "testing_uptake": testing_uptake,
            "welfare_impact": welfare_impact,
            "equity_weighted_welfare": equity_weighted_welfare,
            "compliance_rate": compliance_rate,
            "insurance_premiums": insurance_premiums,
            "info_gap": info_gap,
            "policy_name": policy.name,
            "policy_description": policy.description,
        },
    )
