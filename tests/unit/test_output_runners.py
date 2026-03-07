from __future__ import annotations

from scripts import run_posterior_predictive, run_stress_tests


def test_simulate_model_outputs_uses_active_pipeline() -> None:
    draws = {
        name: run_posterior_predictive.draw_from_prior(name, 3, seed=20260303)
        for name in run_posterior_predictive.PRIORS
    }

    simulations = run_posterior_predictive.simulate_model_outputs(draws, 3)

    assert set(simulations) == {
        "testing_uptake",
        "premium_divergence",
        "welfare_impact",
        "deterrence_rate",
    }
    assert len(simulations["testing_uptake"]) == 3
    assert all(0.0 <= value <= 1.0 for value in simulations["testing_uptake"])
    assert all(value >= 0.0 for value in simulations["premium_divergence"])


def test_run_stress_test_returns_real_metrics() -> None:
    result = run_stress_tests.run_stress_test(
        "C_100pct_enforcement",
        run_stress_tests.SCENARIOS["C_100pct_enforcement"],
        "australia",
    )

    assert result["policy"] == "ban"
    assert 0.0 <= result["testing_uptake"] <= 1.0
    assert 0.0 <= result["enforcement_compliance"] <= 1.0
    assert "validation_issues" not in result
