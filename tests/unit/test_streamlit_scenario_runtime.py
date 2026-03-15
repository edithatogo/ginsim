from pathlib import Path

import pytest

from streamlit_app.scenario_runtime import (
    evaluate_scenario,
    filter_scenarios_by_jurisdiction,
    get_scenario_display_name,
    load_scenarios,
)


def test_load_scenarios_reads_real_config() -> None:
    config_path = Path(__file__).resolve().parents[2] / "configs" / "scenarios.yaml"
    scenarios = load_scenarios(config_path)

    assert "au_2025_ban" in scenarios
    assert scenarios["canada_gnda"]["jurisdiction"] == "CA"


def test_runtime_helpers_present_human_labels_and_subset_scope() -> None:
    scenarios = {
        "au_status_quo": {"jurisdiction": "AU"},
        "au_2025_ban": {"name": "Australia 2025 Genetic Ban", "jurisdiction": "AU"},
        "uk_code": {"jurisdiction": "UK"},
    }

    assert get_scenario_display_name("au_2025_ban", scenarios["au_2025_ban"]) == (
        "Australia 2025 Genetic Ban"
    )
    assert get_scenario_display_name("sandbox_strong_enforcement", {}) == (
        "Sandbox Strong Enforcement"
    )
    assert filter_scenarios_by_jurisdiction(scenarios, "AU") == {
        "au_status_quo": {"jurisdiction": "AU"},
        "au_2025_ban": {"name": "Australia 2025 Genetic Ban", "jurisdiction": "AU"},
    }


def test_runtime_evaluate_scenario_uses_policy_id_and_overrides() -> None:
    seen: dict[str, object] = {}

    def mock_model(params, policy):
        seen["jurisdiction"] = params.jurisdiction
        seen["policy_name"] = policy.name
        seen["enforcement_strength"] = policy.enforcement_strength
        seen["penalty_type"] = policy.penalty_type

        class MockResult:
            testing_uptake = 0.61
            welfare_impact = 12345.0
            equity_weighted_welfare = 15000.0
            compliance_rate = 0.91

            def __init__(self) -> None:
                self.insurance_premiums = {"premium_high": 0.5, "premium_low": 0.1}

        return MockResult()

    scenario = {
        "jurisdiction": "NZ",
        "policy_id": "ban",
        "parameters": {
            "baseline_testing_uptake": 0.48,
            "deterrence_elasticity": 0.10,
        },
        "policy_overrides": {
            "enforcement_strength": 0.95,
        },
    }

    result = evaluate_scenario("nz_ban", scenario, mock_model)

    assert result.scenario_name == "nz_ban"
    assert result.testing_uptake == 0.61
    assert result.all_metrics["policy_name"] == "ban"
    assert seen == {
        "jurisdiction": "new_zealand",
        "policy_name": "ban",
        "enforcement_strength": 0.95,
        "penalty_type": "civil",
    }


def test_runtime_evaluate_scenario_rejects_unsupported_active_fields() -> None:
    def mock_model(params, policy):  # pragma: no cover - should not run
        msg = "Scenario should fail before model evaluation"
        raise AssertionError(msg)

    scenario = {
        "jurisdiction": "AU",
        "policy_id": "status_quo",
        "parameters": {
            "baseline_testing_uptake": 0.52,
            "penalty_rate": 0.8,
        },
    }

    with pytest.raises(ValueError, match="unsupported parameter field"):
        evaluate_scenario("bad_scenario", scenario, mock_model)
