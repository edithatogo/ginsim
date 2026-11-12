"""
Unit tests for Module F: Data Quality Externality.
"""

import jax.numpy as jnp

from src.model.module_f_data_quality import (
    compute_data_quality_externality,
    compute_participation_probability,
    compute_participation_rate,
    compute_predictive_performance,
    compute_representativeness,
    compute_research_value_loss,
    compute_selection_bias,
    get_standard_participation_parameters,
)
from src.model.parameters import PolicyConfig, get_default_parameters


class TestParticipationProbability:
    """Tests for compute_participation_probability."""

    def test_probability_bounded(self):
        """Test that probability is bounded [0, 1]."""
        for privacy_concern in [0.0, 0.5, 1.0]:
            prob = compute_participation_probability(
                privacy_protections=0.5,
                social_benefit=0.6,
                privacy_concern=privacy_concern,
            )
            assert 0.0 <= prob <= 1.0

    def test_probability_increases_with_protections(self):
        """Test that participation increases with privacy protections."""
        prob_low = compute_participation_probability(
            privacy_protections=0.2,
            social_benefit=0.6,
            privacy_concern=0.5,
        )
        prob_high = compute_participation_probability(
            privacy_protections=0.8,
            social_benefit=0.6,
            privacy_concern=0.5,
        )

        assert prob_high > prob_low

    def test_probability_decreases_with_concern(self):
        """Test that participation decreases with privacy concern."""
        prob_low_concern = compute_participation_probability(
            privacy_protections=0.5,
            social_benefit=0.6,
            privacy_concern=0.2,
        )
        prob_high_concern = compute_participation_probability(
            privacy_protections=0.5,
            social_benefit=0.6,
            privacy_concern=0.8,
        )

        assert prob_high_concern < prob_low_concern


class TestParticipationRate:
    """Tests for compute_participation_rate."""

    def test_rate_bounded(self):
        """Test that participation rate is bounded [0, 1]."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test policy",
            allow_genetic_test_results=False,
            enforcement_strength=0.5,
        )

        rate = compute_participation_rate(params, policy)

        assert 0.0 <= rate <= 1.0

    def test_rate_higher_with_protections(self):
        """Test that rate is higher with privacy protections."""
        params = get_default_parameters()

        # Policy with protections
        policy_with = PolicyConfig(
            name="with_protections",
            description="With protections",
            allow_genetic_test_results=False,
            enforcement_strength=1.0,
        )

        # Policy without protections
        policy_without = PolicyConfig(
            name="without",
            description="Without protections",
            allow_genetic_test_results=True,
        )

        rate_with = compute_participation_rate(params, policy_with)
        rate_without = compute_participation_rate(params, policy_without)

        # Protections should increase participation
        assert rate_with >= rate_without


class TestRepresentativeness:
    """Tests for compute_representativeness."""

    def test_representativeness_bounded(self):
        """Test that representativeness is bounded [0, 1]."""
        for participation in [0.0, 0.5, 1.0]:
            rep = compute_representativeness(participation)
            assert 0.0 <= rep <= 1.0

    def test_representativeness_increases_with_participation(self):
        """Test that representativeness increases with participation."""
        rep_low = compute_representativeness(0.3)
        rep_high = compute_representativeness(0.8)

        assert rep_high > rep_low


class TestPredictivePerformance:
    """Tests for compute_predictive_performance."""

    def test_performance_bounded(self):
        """Test that performance is bounded."""
        for rep in [0.0, 0.5, 1.0]:
            perf = compute_predictive_performance(rep)
            assert 0.0 <= perf <= 1.0

    def test_performance_increases_with_representativeness(self):
        """Test that performance increases with representativeness."""
        perf_low = compute_predictive_performance(0.3)
        perf_high = compute_predictive_performance(0.8)

        assert perf_high > perf_low


class TestSelectionBias:
    """Tests for compute_selection_bias."""

    def test_bias_bounded(self):
        """Test that selection bias is bounded [0, 1]."""
        for participation in [0.0, 0.5, 1.0]:
            bias = compute_selection_bias(participation)
            assert 0.0 <= bias <= 1.0

    def test_bias_decreases_with_participation(self):
        """Test that bias decreases with participation."""
        bias_low = compute_selection_bias(0.8)
        bias_high = compute_selection_bias(0.3)

        assert bias_high > bias_low


class TestDataQualityExternality:
    """Tests for compute_data_quality_externality."""

    def test_externality_structure(self):
        """Test that externality output has correct structure."""
        params = get_default_parameters()

        baseline = PolicyConfig(
            name="baseline",
            description="Baseline",
            allow_genetic_test_results=True,
        )

        reform = PolicyConfig(
            name="reform",
            description="Reform",
            allow_genetic_test_results=False,
            enforcement_strength=1.0,
        )

        externality = compute_data_quality_externality(params, baseline, reform)

        assert "participation_baseline" in externality
        assert "participation_reform" in externality
        assert "representativeness_baseline" in externality
        assert "representativeness_reform" in externality
        assert "performance_baseline" in externality
        assert "performance_reform" in externality

    def test_protections_increase_participation(self):
        """Test that privacy protections increase participation."""
        params = get_default_parameters()

        baseline = PolicyConfig(
            name="baseline",
            description="Baseline",
            allow_genetic_test_results=True,
        )

        reform = PolicyConfig(
            name="reform",
            description="Reform",
            allow_genetic_test_results=False,
            enforcement_strength=1.0,
        )

        externality = compute_data_quality_externality(params, baseline, reform)

        # Reform with protections should have higher participation
        assert externality["participation_reform"] >= externality["participation_baseline"]


class TestResearchValueLoss:
    """Tests for compute_research_value_loss."""

    def test_loss_positive_when_performance_decreases(self):
        """Test that value loss is positive when performance decreases."""
        loss = compute_research_value_loss(
            performance_baseline=0.8,
            performance_reform=0.6,
        )

        assert loss > 0.0

    def test_loss_zero_when_no_change(self):
        """Test that value loss is zero when no performance change."""
        loss = compute_research_value_loss(
            performance_baseline=0.8,
            performance_reform=0.8,
        )

        assert jnp.isclose(loss, 0.0, atol=1e-6)


class TestGetStandardParticipationParameters:
    """Tests for get_standard_participation_parameters."""

    def test_returns_all_parameters(self):
        """Test that all parameters are returned."""
        params = get_standard_participation_parameters()

        assert "base_participation" in params
        assert "privacy_elasticity" in params
        assert "social_benefit" in params
        assert "annual_research_value" in params
        assert "discount_rate" in params
        assert "time_horizon" in params

    def test_parameters_are_reasonable(self):
        """Test that parameters are reasonable values."""
        params = get_standard_participation_parameters()

        assert 0.0 < params["base_participation"] < 1.0
        assert params["privacy_elasticity"] < 0.0  # Negative elasticity
        assert 0.0 < params["social_benefit"] < 1.0
        assert params["annual_research_value"] > 0.0
        assert params["discount_rate"] >= 0.0
