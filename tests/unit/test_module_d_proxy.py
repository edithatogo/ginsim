"""
Unit tests for Module D: Proxy Substitution.
"""

import jax.numpy as jnp

from src.model.module_d_proxy import (
    compute_claim_probability,
    compute_family_history_accuracy,
    compute_risk_score,
    compute_underwriting_accuracy,
    get_standard_features,
)
from src.model.parameters import get_default_parameters


class TestRiskScore:
    """Tests for compute_risk_score."""

    def test_risk_score_positive(self):
        """Test that risk score is computed correctly."""
        features = {
            "age": 0.5,
            "bmi": 0.3,
        }
        weights = {
            "age": 0.6,
            "bmi": 0.4,
        }

        score = compute_risk_score(features, weights)

        assert jnp.isclose(score, 0.42, atol=1e-6)

    def test_risk_score_excludes_genetic_when_not_allowed(self):
        """Test that genetic features are excluded when not allowed."""
        features = {
            "age": 0.5,
            "genetic_test_result": 1.0,  # Should be excluded
        }
        weights = {
            "age": 0.6,
            "genetic_test_result": 0.8,
        }

        # With genetic
        score_with = compute_risk_score(features, weights, include_genetic=True)

        # Without genetic
        score_without = compute_risk_score(features, weights, include_genetic=False)

        # Score without genetic should be lower (excludes genetic contribution)
        assert score_without < score_with


class TestClaimProbability:
    """Tests for compute_claim_probability."""

    def test_probability_bounded(self):
        """Test that probability is bounded [0, 1]."""
        for risk_score in [-10.0, -1.0, 0.0, 1.0, 10.0]:
            prob = compute_claim_probability(risk_score)
            assert 0.0 <= prob <= 1.0

    def test_probability_increases_with_risk_score(self):
        """Test that probability increases with risk score."""
        prob_low = compute_claim_probability(risk_score=-1.0)
        prob_high = compute_claim_probability(risk_score=1.0)

        assert prob_high > prob_low

    def test_probability_at_zero_risk(self):
        """Test probability at zero risk score."""
        prob = compute_claim_probability(0.0, intercept=0.0)
        assert jnp.isclose(prob, 0.5, atol=1e-6)


class TestUnderwritingAccuracy:
    """Tests for compute_underwriting_accuracy."""

    def test_accuracy_metrics_bounded(self):
        """Test that accuracy metrics are bounded [0, 1]."""
        n = 100
        predicted = jnp.linspace(0, 1, n)
        actual = jnp.zeros(n).at[:50].set(1)  # 50% positive

        accuracy = compute_underwriting_accuracy(predicted, actual)

        assert 0.0 <= accuracy.auc <= 1.0
        assert 0.0 <= accuracy.sensitivity <= 1.0
        assert 0.0 <= accuracy.specificity <= 1.0
        assert 0.0 <= accuracy.mispricing_error <= 1.0

    def test_perfect_prediction(self):
        """Test accuracy with perfect predictions."""
        n = 100
        predicted = jnp.zeros(n).at[:50].set(1)
        actual = predicted.copy()

        accuracy = compute_underwriting_accuracy(predicted, actual)

        assert jnp.isclose(accuracy.sensitivity, 1.0, atol=1e-6)
        assert jnp.isclose(accuracy.specificity, 1.0, atol=1e-6)
        assert jnp.isclose(accuracy.mispricing_error, 0.0, atol=1e-6)


class TestFamilyHistoryAccuracy:
    """Tests for compute_family_history_accuracy."""

    def test_sensitivity_from_params(self):
        """Test that sensitivity matches parameter value."""
        params = get_default_parameters()

        # Create test data
        n = 100
        family_history = jnp.zeros(n).at[:20].set(1)  # 20 positive
        mutation = jnp.zeros(n).at[:15].set(1)  # 15 with mutation

        result = compute_family_history_accuracy(params, family_history, mutation)

        # Sensitivity should match parameter
        assert jnp.isclose(result["sensitivity"], params.family_history_sensitivity, atol=1e-6)

    def test_accuracy_computed_correctly(self):
        """Test that empirical accuracy is computed correctly."""
        params = get_default_parameters()

        # Perfect prediction case
        n = 100
        family_history = jnp.zeros(n).at[:20].set(1)
        mutation = family_history.copy()

        result = compute_family_history_accuracy(params, family_history, mutation)

        assert jnp.isclose(result["accuracy"], 1.0, atol=1e-6)


class TestGetStandardFeatures:
    """Tests for get_standard_features."""

    def test_returns_all_features(self):
        """Test that all standard features are returned."""
        features = get_standard_features()

        assert "age" in features
        assert "sex" in features
        assert "smoking_status" in features
        assert "bmi" in features
        assert "family_history" in features
        assert "genetic_test_result" in features
        assert "medical_history" in features
        assert "occupation" in features

    def test_feature_count(self):
        """Test correct number of features."""
        features = get_standard_features()

        assert len(features) == 8
