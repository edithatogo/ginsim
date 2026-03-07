"""
Unit tests for Sensitivity Analysis.
"""

from src.model.parameters import ModelParameters, PolicyConfig
from src.model.sensitivity import (
    one_way_sensitivity,
    scenario_analysis,
    tornado_analysis,
)


class TestOneWaySensitivity:
    """Tests for one_way_sensitivity."""

    def test_returns_sensitivity_result(self):
        """Test that analysis returns a SensitivityResult."""

        def model(p):
            return p.deterrence_elasticity * 10

        params = ModelParameters(deterrence_elasticity=0.5)
        result = one_way_sensitivity(model, params, "deterrence_elasticity")

        assert result.parameter_name == "deterrence_elasticity"
        assert result.base_outcome == 5.0

    def test_sensitivity_index_positive(self):
        """Test that sensitivity index is correctly calculated."""

        def model(p):
            return p.deterrence_elasticity

        params = ModelParameters(deterrence_elasticity=1.0)
        result = one_way_sensitivity(model, params, "deterrence_elasticity", variation=0.5)

        # Base=1.0, Low=0.5, High=1.5. Swing = 1.0. Index = 1.0/1.0 = 1.0
        assert result.sensitivity_index > 0


class TestTornadoAnalysis:
    """Tests for tornado_analysis."""

    def test_returns_sorted_results(self):
        """Test that results are sorted by impact."""

        def model(p):
            return p.deterrence_elasticity + 2 * p.moratorium_effect

        params = ModelParameters(deterrence_elasticity=1.0, moratorium_effect=1.0)
        results = tornado_analysis(model, params, ["deterrence_elasticity", "moratorium_effect"])

        assert len(results) == 2
        # Moratorium should have higher impact (coefficient 2 vs 1)
        assert results[0].parameter_name == "moratorium_effect"


class TestScenarioAnalysis:
    """Tests for scenario_analysis."""

    def test_returns_scenario_results(self):
        """Test that scenario analysis returns results."""

        def model(p, pol):
            return p.deterrence_elasticity * (2.0 if pol.allow_genetic_test_results else 1.0)

        params = ModelParameters(deterrence_elasticity=10.0)
        baseline = PolicyConfig(name="base", description="d", allow_genetic_test_results=True)
        reform = PolicyConfig(name="reform", description="d", allow_genetic_test_results=False)

        results = scenario_analysis(model, params, baseline, reform)

        assert results["baseline_outcome"] == 20.0
        assert results["reform_outcome"] == 10.0
        assert results["delta"] == -10.0
