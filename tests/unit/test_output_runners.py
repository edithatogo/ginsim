import pytest
from scripts import run_posterior_predictive, run_stress_tests

def test_simulate_model_outputs_uses_active_pipeline() -> None:
    draws = {
        name: run_posterior_predictive.draw_from_prior(name, 3, seed=20260303)
        for name in run_posterior_predictive.PRIORS
    }

    simulations = run_posterior_predictive.simulate_model_outputs(draws, 3)
    
    # Check one of the output arrays
    assert len(simulations["testing_uptake"]) == 3
    assert float(simulations["testing_uptake"][0]) > 0


def test_run_stress_test_returns_real_metrics() -> None:
    # Stress tests now build params internally using build_base_params
    result = run_stress_tests.run_stress_test(
        "C_100pct_enforcement",
        run_stress_tests.SCENARIOS["C_100pct_enforcement"],
        "australia",
    )

    assert result["scenario"] == "C_100pct_enforcement"
    assert float(result["testing_uptake"]) > 0
    assert float(result["welfare_impact"]) != 0
    assert "research_participation" in result
    assert float(result["research_participation"]) >= 0
