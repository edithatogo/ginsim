"""
Integration tests for the full policy evaluation pipeline.
"""

from src.model.parameters import ModelParameters, PolicyConfig
from src.model.pipeline import (
    compare_policies,
    evaluate_policy_sweep,
    evaluate_single_policy,
    generate_policy_summary,
    get_standard_policies,
    run_full_evaluation,
)


class TestEvaluateSinglePolicy:
    """Tests for evaluate_single_policy."""

    def test_evaluation_returns_result(self):
        """Test that evaluation returns a result object."""
        params = ModelParameters()
        policy = PolicyConfig(
            name="test",
            description="Test policy",
            allow_genetic_test_results=True,
        )

        result = evaluate_single_policy(params, policy)

        assert result is not None
        assert hasattr(result, "policy_name")
        assert hasattr(result, "testing_uptake")
        assert hasattr(result, "insurance_premiums")
        assert hasattr(result, "welfare_impact")

    def test_testing_uptake_bounded(self):
        """Test that testing uptake is bounded [0, 1]."""
        params = ModelParameters()
        policy = PolicyConfig(
            name="test",
            description="Test",
            allow_genetic_test_results=True,
        )

        result = evaluate_single_policy(params, policy)

        assert 0.0 <= result.testing_uptake <= 1.0

    def test_premiums_positive(self):
        """Test that insurance premiums are positive."""
        params = ModelParameters()
        policy = PolicyConfig(
            name="test",
            description="Test",
            allow_genetic_test_results=True,
        )

        result = evaluate_single_policy(params, policy)

        assert result.insurance_premiums["premium_high_risk"] > 0.0
        assert result.insurance_premiums["premium_low_risk"] > 0.0

    def test_compliance_rate_bounded(self):
        """Test that compliance rate is bounded [0, 1]."""
        params = ModelParameters()
        policy = PolicyConfig(
            name="test",
            description="Test",
            allow_genetic_test_results=False,
        )

        result = evaluate_single_policy(params, policy)

        assert 0.0 <= result.compliance_rate <= 1.0


class TestEvaluatePolicySweep:
    """Tests for evaluate_policy_sweep."""

    def test_sweep_returns_all_policies(self):
        """Test that sweep returns results for all standard policies."""
        params = ModelParameters()

        results = evaluate_policy_sweep(params)

        assert "status_quo" in results
        assert "moratorium" in results
        assert "ban" in results

    def test_sweep_results_are_valid(self):
        """Test that all sweep results are valid."""
        params = ModelParameters()

        results = evaluate_policy_sweep(params)

        for result in results.values():
            assert 0.0 <= result.testing_uptake <= 1.0
            assert 0.0 <= result.compliance_rate <= 1.0
            assert 0.0 <= result.research_participation <= 1.0


class TestComparePolicies:
    """Tests for compare_policies."""

    def test_comparison_structure(self):
        """Test that comparison output has correct structure."""
        params = ModelParameters()
        results = evaluate_policy_sweep(params)

        comparisons = compare_policies(results, baseline_name="status_quo")

        assert "moratorium" in comparisons
        assert "ban" in comparisons

        for metrics in comparisons.values():
            assert "testing_uptake_change" in metrics
            assert "welfare_change" in metrics
            assert "premium_change" in metrics
            assert "compliance_change" in metrics

    def test_comparison_computes_changes(self):
        """Test that comparison computes changes correctly."""
        params = ModelParameters()
        results = evaluate_policy_sweep(params)

        comparisons = compare_policies(results, baseline_name="status_quo")

        # Changes should be computed (not None)
        for metrics in comparisons.values():
            assert metrics["testing_uptake_change"] is not None
            assert metrics["welfare_change"] is not None


class TestGeneratePolicySummary:
    """Tests for generate_policy_summary."""

    def test_summary_is_string(self):
        """Test that summary is a string."""
        params = ModelParameters()
        results = evaluate_policy_sweep(params)

        summary = generate_policy_summary(results)

        assert isinstance(summary, str)

    def test_summary_contains_policy_names(self):
        """Test that summary contains policy names."""
        params = ModelParameters()
        results = evaluate_policy_sweep(params)

        summary = generate_policy_summary(results)

        assert "status_quo" in summary or "Status Quo" in summary
        assert "moratorium" in summary or "Moratorium" in summary
        assert "ban" in summary or "Ban" in summary

    def test_summary_contains_metrics(self):
        """Test that summary contains key metrics."""
        params = ModelParameters()
        results = evaluate_policy_sweep(params)

        summary = generate_policy_summary(results)

        assert "Testing Uptake" in summary
        assert "Premium" in summary or "premium" in summary
        assert "Welfare" in summary or "welfare" in summary


class TestRunFullEvaluation:
    """Tests for run_full_evaluation."""

    def test_full_evaluation_returns_results(self):
        """Test that full evaluation returns results."""
        results = run_full_evaluation()

        assert results is not None
        assert len(results) > 0

    def test_full_evaluation_with_custom_params(self):
        """Test full evaluation with custom parameters."""
        params = ModelParameters(
            baseline_testing_uptake=0.60,
            deterrence_elasticity=0.15,
        )

        results = run_full_evaluation(params=params)

        assert results is not None
        assert len(results) > 0


class TestGetStandardPolicies:
    """Tests for get_standard_policies."""

    def test_returns_all_policies(self):
        """Test that all standard policies are returned."""
        policies = get_standard_policies()

        assert "status_quo" in policies
        assert "moratorium" in policies
        assert "ban" in policies

    def test_policies_are_valid(self):
        """Test that all policies are valid PolicyConfig instances."""
        policies = get_standard_policies()

        for name, policy in policies.items():
            assert isinstance(policy, PolicyConfig)
            assert policy.name == name
