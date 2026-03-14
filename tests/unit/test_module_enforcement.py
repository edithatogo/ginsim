"""
Unit tests for Enforcement module.
"""

import jax.numpy as jnp

from src.model.module_enforcement import (
    compute_compliance_decision,
    compute_compliance_equilibrium,
    compute_detection_probability,
    compute_enforcement_effect,
    compute_expected_penalty,
    compute_optimal_enforcement,
    compute_violation_benefit,
    get_standard_enforcement_parameters,
)
from src.model.parameters import PolicyConfig, get_default_parameters


class TestDetectionProbability:
    """Tests for compute_detection_probability."""

    def test_probability_bounded(self):
        """Test that detection probability is bounded [0, 1]."""
        for enf_strength in [0.0, 0.5, 1.0]:
            for monitoring in [0.0, 0.5, 1.0]:
                prob = compute_detection_probability(enf_strength, monitoring)
                assert 0.0 <= prob <= 1.0

    def test_probability_increases_with_enforcement(self):
        """Test that detection increases with enforcement strength."""
        prob_low = compute_detection_probability(0.2, 0.5)
        prob_high = compute_detection_probability(0.8, 0.5)

        assert prob_high > prob_low

    def test_probability_increases_with_monitoring(self):
        """Test that detection increases with monitoring intensity."""
        prob_low = compute_detection_probability(0.5, 0.2)
        prob_high = compute_detection_probability(0.5, 0.8)

        assert prob_high > prob_low


class TestExpectedPenalty:
    """Tests for compute_expected_penalty."""

    def test_penalty_positive(self):
        """Test that expected penalty is positive."""
        penalty = compute_expected_penalty(
            penalty_max=10000.0,
            detection_probability=0.5,
            enforcement_effectiveness=0.5,
        )
        assert penalty > 0.0

    def test_penalty_increases_with_penalty_max(self):
        """Test that penalty increases with maximum penalty."""
        penalty_low = compute_expected_penalty(100000.0, 0.5, 0.5)
        penalty_high = compute_expected_penalty(200000.0, 0.5, 0.5)

        assert penalty_high > penalty_low

    def test_penalty_increases_with_detection(self):
        """Test that penalty increases with detection probability."""
        penalty_low = compute_expected_penalty(100000.00, 0.2, 0.5)
        penalty_high = compute_expected_penalty(100000.00, 0.8, 0.5)

        assert penalty_high > penalty_low


class TestViolationBenefit:
    """Tests for compute_violation_benefit."""

    def test_benefit_positive(self):
        """Test that violation benefit is positive."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test",
            allow_genetic_test_results=True,
        )

        benefit = compute_violation_benefit(params, policy)

        assert benefit >= 0.0

    def test_benefit_higher_when_banned(self):
        """Test that benefit is higher when completely banned."""
        params = get_default_parameters()

        # Allowed
        policy_allowed = PolicyConfig(
            name="allowed",
            description="Allowed",
            allow_genetic_test_results=True,
        )

        # Banned
        policy_banned = PolicyConfig(
            name="banned",
            description="Banned",
            allow_genetic_test_results=False,
        )

        benefit_allowed = compute_violation_benefit(params, policy_allowed)
        benefit_banned = compute_violation_benefit(params, policy_banned)

        # Benefit should be higher when banned (more incentive to violate)
        assert benefit_banned >= benefit_allowed


class TestComplianceDecision:
    """Tests for compute_compliance_decision."""

    def test_compliance_bounded(self):
        """Test that compliance probability is bounded [0, 1]."""
        for benefit in [0.0, 0.5, 1.0]:
            for penalty in [0.0, 0.5, 1.0]:
                compliance = compute_compliance_decision(benefit, penalty)
                assert 0.0 <= compliance <= 1.0

    def test_compliance_increases_with_penalty(self):
        """Test that compliance increases with expected penalty."""
        compliance_low = compute_compliance_decision(violation_benefit=0.5, expected_penalty=0.2)
        compliance_high = compute_compliance_decision(violation_benefit=0.5, expected_penalty=0.8)

        assert compliance_high > compliance_low

    def test_compliance_decreases_with_benefit(self):
        """Test that compliance decreases with violation benefit."""
        compliance_low_benefit = compute_compliance_decision(
            violation_benefit=0.2,
            expected_penalty=0.5,
        )
        compliance_high_benefit = compute_compliance_decision(
            violation_benefit=0.8,
            expected_penalty=0.5,
        )

        assert compliance_high_benefit < compliance_low_benefit


class TestComplianceEquilibrium:
    """Tests for compute_compliance_equilibrium."""

    def test_equilibrium_structure(self):
        """Test that equilibrium output has correct structure."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test policy",
            allow_genetic_test_results=False,
            enforcement_strength=0.5,
            penalty_max=10000.0,
        )

        outcome = compute_compliance_equilibrium(params, policy)

        assert hasattr(outcome, "compliance_rate")
        assert hasattr(outcome, "violation_rate")
        assert hasattr(outcome, "detection_rate")
        assert hasattr(outcome, "expected_penalty")

    def test_rates_sum_to_one(self):
        """Test that compliance and violation rates sum to 1."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test",
            allow_genetic_test_results=False,
            enforcement_strength=0.5,
        )

        outcome = compute_compliance_equilibrium(params, policy)

        assert jnp.isclose(outcome.compliance_rate + outcome.violation_rate, 1.0, atol=1e-6)


class TestEnforcementEffect:
    """Tests for compute_enforcement_effect."""

    def test_effect_structure(self):
        """Test that effect output has correct structure."""
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

        effect = compute_enforcement_effect(params, baseline, reform)

        assert "compliance_baseline" in effect
        assert "compliance_reform" in effect
        assert "compliance_change" in effect
        assert "violation_baseline" in effect
        assert "violation_reform" in effect


class TestOptimalEnforcement:
    """Tests for compute_optimal_enforcement."""

    def test_optimal_structure(self):
        """Test that optimal enforcement output has correct structure."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test",
            allow_genetic_test_results=False,
            penalty_max=10000.0,
        )

        result = compute_optimal_enforcement(params, policy)

        assert "optimal_enforcement" in result
        assert "optimal_compliance" in result
        assert "optimal_violation_rate" in result
        assert "objective_value" in result

    def test_optimal_enforcement_bounded(self):
        """Test that optimal enforcement is bounded [0, 1]."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test",
            allow_genetic_test_results=False,
        )

        result = compute_optimal_enforcement(params, policy)

        assert 0.0 <= result["optimal_enforcement"] <= 1.0


class TestGetStandardEnforcementParameters:
    """Tests for get_standard_enforcement_parameters."""

    def test_returns_all_parameters(self):
        """Test that all parameters are returned."""
        params = get_standard_enforcement_parameters()

        assert "monitoring_intensity" in params
        assert "target_compliance" in params
        assert "enforcement_cost_parameter" in params
        assert "max_detection_rate" in params

    def test_parameters_are_reasonable(self):
        """Test that parameters are reasonable values."""
        params = get_standard_enforcement_parameters()

        assert 0.0 < params["monitoring_intensity"] < 1.0
        assert 0.0 < params["target_compliance"] < 1.0
        assert params["enforcement_cost_parameter"] > 0.0
        assert 0.0 < params["max_detection_rate"] < 1.0
