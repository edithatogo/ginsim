"""
Unit tests for high-level output runner scripts.
"""

import numpy as np
from scripts import run_posterior_predictive, run_stress_tests
from src.model.parameters import get_default_parameters


def test_simulate_model_outputs_uses_active_pipeline() -> None:
    draws = {
        name: run_posterior_predictive.draw_from_prior(name, 3, seed=20260303)
        for name in run_posterior_predictive.PRIORS
    }

    simulations = run_posterior_predictive.simulate_model_outputs(draws, 3)

    assert "testing_uptake" in simulations
    assert "premium_divergence" in simulations
    assert simulations["testing_uptake"].shape == (3,)


def test_run_stress_test_returns_real_metrics() -> None:
    # Stress tests now build params internally using build_base_params
    # We can test that function directly if needed, or the wrapper
    result = run_stress_tests.run_stress_test(
        "C_100pct_enforcement",
        run_stress_tests.SCENARIOS["C_100pct_enforcement"],
        "australia",
    )

    assert result["policy"] == "ban"  # C_100pct_enforcement uses 'ban' policy
    assert result["testing_uptake"] is not None
    assert "policy_effect" in result
