#!/usr/bin/env python3
"""
Tests for scenario analysis module.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import yaml

from src.model.scenario_analysis import (
    ScenarioComparison,
    ScenarioResult,
    compare_scenarios,
    format_comparison_table,
    load_scenarios,
)


class TestLoadScenarios:
    """Test scenario loading functionality."""

    def test_load_scenarios_valid_config(self):
        """Test loading scenarios from valid config file."""
        config_path = Path(__file__).parent.parent.parent / "configs" / "scenarios.yaml"
        if config_path.exists():
            scenarios = load_scenarios(config_path)
            assert len(scenarios) > 0
            assert "au_status_quo" in scenarios or len(scenarios) > 0

    def test_load_scenarios_file_not_found(self):
        """Test error handling for missing config file."""
        with pytest.raises(FileNotFoundError):
            load_scenarios("/nonexistent/path/scenarios.yaml")

    def test_load_scenarios_empty_file(self):
        """Test loading from empty config file."""
        with TemporaryDirectory() as tmpdir:
            empty_config = Path(tmpdir) / "empty.yaml"
            empty_config.write_text("{}")  # Empty dict, not completely empty
            scenarios = load_scenarios(empty_config)
            assert scenarios == {}

    def test_load_scenarios_minimal_config(self):
        """Test loading from minimal valid config."""
        with TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "minimal.yaml"
            config_data = {
                "scenarios": {
                    "test_scenario": {
                        "name": "Test Scenario",
                        "jurisdiction": "AU",
                        "parameters": {
                            "baseline_testing_uptake": 0.5,
                        },
                    },
                },
            }
            with config_path.open("w", encoding="utf-8") as config_file:
                yaml.dump(config_data, config_file)

            scenarios = load_scenarios(config_path)
            assert "test_scenario" in scenarios
            assert scenarios["test_scenario"]["name"] == "Test Scenario"


class TestScenarioResult:
    """Test ScenarioResult dataclass."""

    def test_scenario_result_creation(self):
        """Test creating a ScenarioResult object."""
        result = ScenarioResult(
            scenario_name="test",
            jurisdiction="AU",
            testing_uptake=0.55,
            welfare_impact=100000.0,
            qalys_gained=10.5,
            compliance_rate=0.8,
            all_metrics={"testing_uptake": 0.55},
        )
        assert result.scenario_name == "test"
        assert result.jurisdiction == "AU"
        assert result.testing_uptake == 0.55
        assert result.welfare_impact == 100000.0
        assert result.qalys_gained == 10.5
        assert result.compliance_rate == 0.8


class TestFormatComparisonTable:
    """Test scenario comparison table formatting."""

    def test_format_comparison_table_basic(self):
        """Test formatting a basic comparison table."""
        results = [
            ScenarioResult(
                scenario_name="baseline",
                jurisdiction="AU",
                testing_uptake=0.50,
                welfare_impact=50000.0,
                qalys_gained=5.0,
                compliance_rate=0.7,
                all_metrics={},
            ),
            ScenarioResult(
                scenario_name="treatment",
                jurisdiction="AU",
                testing_uptake=0.60,
                welfare_impact=75000.0,
                qalys_gained=7.5,
                compliance_rate=0.85,
                all_metrics={},
            ),
        ]

        comparison = ScenarioComparison(
            baseline_scenario="baseline",
            scenarios=results,
            delta_from_baseline={
                "treatment": {
                    "testing_uptake_delta": 0.10,
                    "welfare_delta": 25000.0,
                    "qalys_delta": 2.5,
                    "compliance_delta": 0.15,
                },
            },
        )

        table = format_comparison_table(comparison)

        # Check table structure
        assert "| Scenario |" in table
        assert "|----------|" in table
        assert "baseline" in table
        assert "treatment" in table


class TestCompareScenarios:
    """Test scenario comparison functionality."""

    def test_compare_scenarios_empty(self):
        """Test comparison with no scenarios."""
        comparison = compare_scenarios({}, lambda p, pol: None)
        assert comparison.baseline_scenario == "au_status_quo"
        assert comparison.scenarios == []
        assert comparison.delta_from_baseline == {}

    def test_compare_scenarios_single(self):
        """Test comparison with single scenario."""

        def mock_model(params, policy):
            class MockResult:
                testing_uptake = 0.55
                welfare_impact = 60000.0
                qalys_gained = 6.0
                compliance_rate = 0.75

            return MockResult()

        scenarios = {
            "test": {
                "jurisdiction": "AU",
                "parameters": {"baseline_testing_uptake": 0.55},
            },
        }

        comparison = compare_scenarios(scenarios, mock_model, baseline_name="test")
        assert len(comparison.scenarios) == 1
        assert comparison.scenarios[0].scenario_name == "test"
        assert comparison.delta_from_baseline == {}  # No delta for baseline itself
