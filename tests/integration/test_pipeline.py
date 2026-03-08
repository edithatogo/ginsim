"""
Integration tests for the policy evaluation pipeline.
"""

from src.model.parameters import PolicyConfig, get_default_parameters
from src.model.pipeline import (
    compare_policies,
    evaluate_policy_sweep,
    evaluate_single_policy,
    generate_policy_summary,
)


class TestEvaluateSinglePolicy:
    """Test the single policy evaluation function."""

    def test_basic_evaluation(self):
        """Test that evaluation returns a result object."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test",
            allow_genetic_test_results=True,
        )

        result = evaluate_single_policy(params, policy)

        assert result.policy_name == "test"
        assert result.testing_uptake >= 0.0
        assert result.welfare_impact is not None

    def test_premiums_positive(self):
        """Test that insurance premiums are positive."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test",
            allow_genetic_test_results=True,
        )

        result = evaluate_single_policy(params, policy)

        assert result.insurance_premiums["premium_high"] > 0.0
        assert result.insurance_premiums["premium_low"] > 0.0

    def test_evaluation_includes_real_ledger_and_proxy_metrics(self):
        """Test that evaluation exposes derived welfare and proxy outputs."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test_ban",
            description="Test ban",
            allow_genetic_test_results=False,
            allow_family_history=False,
            enforcement_strength=1.0,
            penalty_max=1000000.0,
        )

        result = evaluate_single_policy(params, policy)

        assert "proxy" in result.all_metrics
        assert "residual_information_gap" in result.all_metrics["proxy"]
        assert "welfare" in result.all_metrics
        assert "net_welfare" in result.all_metrics["welfare"]


class TestComparePolicies:
    """Test policy comparison logic."""

    def test_comparison_structure(self):
        """Test that comparison output has correct structure."""
        params = get_default_parameters()
        results = evaluate_policy_sweep(params)

        comparisons = compare_policies(results, baseline_name="status_quo")

        assert "moratorium" in comparisons
        assert "uptake_delta" in comparisons["moratorium"]
        assert "welfare_change" in comparisons["moratorium"]

    def test_comparison_computes_changes(self):
        """Test that comparison correctly computes deltas."""
        params = get_default_parameters()
        results = evaluate_policy_sweep(params)

        comparisons = compare_policies(results, baseline_name="status_quo")

        # In standard calibration, moratorium usually increases uptake
        assert comparisons["moratorium"]["uptake_delta"] >= 0.0


class TestGeneratePolicySummary:
    """Test policy summary generation."""

    def test_summary_contains_metrics(self):
        """Test that summary string includes key metrics."""
        params = get_default_parameters()
        results = evaluate_policy_sweep(params)

        summary = generate_policy_summary(results)

        assert "Policy: status_quo" in summary
        assert "Uptake:" in summary
        assert "Welfare:" in summary


class TestRunFullEvaluation:
    """Test the high-level evaluation runner."""

    def test_full_evaluation_with_custom_params(self):
        """Test evaluation with parameter overrides."""
        base_params = get_default_parameters()
        params = base_params.model_copy(update={"deterrence_elasticity": 0.5})
        results = evaluate_policy_sweep(params)

        assert len(results) > 0
        assert "status_quo" in results
