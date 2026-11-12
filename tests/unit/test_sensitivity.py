"""
Unit tests for sensitivity analysis functions.
"""

from src.model.parameters import PolicyConfig, get_default_parameters
from src.model.sensitivity import (
    SensitivityResult,
    run_scenario_analysis,
    tornado_analysis,
)


class TestOneWaySensitivity:
    """Tests for one-way sensitivity analysis."""

    def test_returns_sensitivity_result(self):
        """Test that analysis returns a SensitivityResult."""

        def model(p):
            return p.deterrence_elasticity * 10

        params = get_default_parameters()
        params = params.model_copy(update={"deterrence_elasticity": 0.5})

        results = tornado_analysis(
            model_fn=model,
            params=params,
            param_names=["deterrence_elasticity"],
        )

        assert len(results) == 1
        assert isinstance(results[0], SensitivityResult)

    def test_sensitivity_index_positive(self):
        """Test that sensitivity index is correctly calculated."""

        def model(p):
            return p.deterrence_elasticity

        params = get_default_parameters()
        params = params.model_copy(update={"deterrence_elasticity": 1.0})

        results = tornado_analysis(
            model_fn=model,
            params=params,
            param_names=["deterrence_elasticity"],
            variation=0.1,
        )

        # Index should be positive for increasing function
        assert results[0].sensitivity_index > 0


class TestTornadoAnalysis:
    """Tests for tornado analysis aggregation."""

    def test_returns_sorted_results(self):
        """Test that results are sorted by impact."""

        def model(p):
            return p.deterrence_elasticity + 2 * p.moratorium_effect

        params = get_default_parameters()
        params = params.model_copy(update={"deterrence_elasticity": 1.0, "moratorium_effect": 1.0})

        results = tornado_analysis(
            model_fn=model,
            params=params,
            param_names=["deterrence_elasticity", "moratorium_effect"],
        )

        assert len(results) == 2
        # moratorium_effect has larger weight (2 vs 1)
        assert results[0].parameter_name == "moratorium_effect"


class TestScenarioAnalysis:
    """Tests for scenario analysis."""

    def test_returns_scenario_results(self):
        """Test that scenario analysis returns results."""

        def model(p, pol):
            return p.deterrence_elasticity * (2.0 if pol.allow_genetic_test_results else 1.0)

        params = get_default_parameters()
        params = params.model_copy(update={"deterrence_elasticity": 10.0})

        policies = [
            PolicyConfig(name="sq", description="SQ", allow_genetic_test_results=True),
            PolicyConfig(name="ban", description="Ban", allow_genetic_test_results=False),
        ]

        results = run_scenario_analysis(
            model_fn=model,
            base_params=params,
            policies=policies,
        )

        assert len(results) == 2
        assert results["sq"] == 20.0
        assert results["ban"] == 10.0
