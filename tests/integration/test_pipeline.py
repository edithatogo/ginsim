import pytest
from src.model.parameters import get_default_parameters, PolicyConfig
from src.model.pipeline import evaluate_single_policy, evaluate_policy_sweep, compare_policies, generate_policy_summary

class TestEvaluateSinglePolicy:
    def test_basic_evaluation(self):
        """Test that single policy evaluation runs."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="test",
            allow_genetic_test_results=True,
        )
        result = evaluate_single_policy(params, policy)
        assert result.policy_name == "test"
        assert result.testing_uptake is not None

    def test_premiums_positive(self):
        """Test that premiums are non-negative."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="test",
            allow_genetic_test_results=True,
        )
        result = evaluate_single_policy(params, policy)
        assert float(result.insurance_premiums["premium_high"]) >= 0
        assert float(result.insurance_premiums["premium_low"]) >= 0

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
        # Use net_welfare as exported by the pipeline
        assert "net_welfare" in result.all_metrics["welfare"]


class TestComparePolicies:
    def test_comparison_structure(self):
        """Test that comparison output has correct structure."""
        params = get_default_parameters()
        results = evaluate_policy_sweep(params)

        # Updated to expect dict from evaluate_policy_sweep results
        comparisons = compare_policies(results, baseline_name="status_quo")

        assert "moratorium" in comparisons
        assert "uptake_delta" in comparisons["moratorium"]
        assert "welfare_delta" in comparisons["moratorium"]

    def test_comparison_computes_changes(self):
        """Test that comparison correctly computes deltas."""
        params = get_default_parameters()
        results = evaluate_policy_sweep(params)

        comparisons = compare_policies(results, baseline_name="status_quo")
        
        # Welfare delta should be non-zero for ban vs sq
        assert abs(comparisons["ban"]["welfare_delta"]) > 0


class TestGeneratePolicySummary:
    def test_summary_contains_metrics(self):
        """Test that summary string includes key metrics."""
        params = get_default_parameters()
        results = evaluate_policy_sweep(params)

        summary = generate_policy_summary(results)

        assert "POLICY IMPACT SUMMARY" in summary
        assert "Testing Uptake" in summary


class TestRunFullEvaluation:
    def test_full_evaluation_with_custom_params(self):
        """Test evaluation with parameter overrides."""
        base_params = get_default_parameters()
        params = base_params.model_copy(update={"deterrence_elasticity": 0.5})
        results = evaluate_policy_sweep(params)
        assert len(results) >= 3
        assert "status_quo" in results
