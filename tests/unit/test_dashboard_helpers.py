"""
Unit tests for dashboard helper functions.
"""

from streamlit_app.dashboard_helpers import evaluate_sandbox_policy


def test_evaluate_sandbox_policy_runs_through_core_pipeline():
    """Test that sandbox evaluation returns expected result structure."""
    # Signature: baseline_testing_uptake, deterrence_elasticity, enforcement_effectiveness, penalty_rate
    result = evaluate_sandbox_policy(
        baseline_testing_uptake=0.52,
        deterrence_elasticity=0.18,
        enforcement_effectiveness=0.5,
        penalty_rate=0.05,
    )

    # Result is a PolicyEvaluationResult dataclass
    assert result.testing_uptake is not None
    assert result.welfare_impact is not None
    assert result.compliance_rate is not None
    assert result.policy_name == "sandbox_policy"
