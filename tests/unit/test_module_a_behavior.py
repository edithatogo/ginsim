"""
Unit tests for Module A: Behavior / Deterrence.

Tests use wrapper functions that accept pydantic models.
"""

from src.model.module_a_behavior_wrappers import (
    compute_perceived_penalty,
    compute_policy_effect,
    compute_testing_uptake,
    get_standard_policies,
)
from src.model.parameters import PolicyConfig, get_default_parameters


class TestPerceivedPenalty:
    """Tests for compute_perceived_penalty."""

    def test_penalty_positive(self):
        """Test that penalty is always positive."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test policy",
            allow_genetic_test_results=True,
        )

        penalty = compute_perceived_penalty(params, policy)

        assert penalty >= 0.0

    def test_penalty_reduced_by_restrictions(self):
        """Test that information restrictions reduce penalty."""
        params = get_default_parameters()

        # Permissive policy
        permissive = PolicyConfig(
            name="permissive",
            description="Permissive policy",
            allow_genetic_test_results=True,
            enforcement_strength=1.0,
        )

        # Restrictive policy
        restrictive = PolicyConfig(
            name="restrictive",
            description="Restrictive policy",
            allow_genetic_test_results=False,
            enforcement_strength=1.0,
        )

        penalty_permissive = compute_perceived_penalty(params, permissive)
        penalty_restrictive = compute_perceived_penalty(params, restrictive)

        # Restrictive policy should have lower penalty
        assert penalty_restrictive < penalty_permissive

    def test_penalty_reduced_by_enforcement(self):
        """Test that stronger enforcement reduces penalty."""
        params = get_default_parameters()

        weak_enforcement = PolicyConfig(
            name="weak",
            description="Weak enforcement",
            allow_genetic_test_results=False,
            enforcement_strength=0.2,
        )

        strong_enforcement = PolicyConfig(
            name="strong",
            description="Strong enforcement",
            allow_genetic_test_results=False,
            enforcement_strength=1.0,
        )

        penalty_weak = compute_perceived_penalty(params, weak_enforcement)
        penalty_strong = compute_perceived_penalty(params, strong_enforcement)

        # Stronger enforcement should reduce penalty more
        assert penalty_strong <= penalty_weak


class TestTestingUtility:
    """Tests for testing utility (removed - internal function)."""

    # These tests removed as compute_testing_utility is internal


class TestTestingProbability:
    """Tests for testing probability (removed - internal function)."""

    # These tests removed as compute_testing_probability is internal


class TestTestingUptake:
    """Tests for compute_testing_uptake."""

    def test_uptake_bounded(self):
        """Test that uptake is bounded [0, 1]."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test policy",
            allow_genetic_test_results=True,
        )

        uptake = compute_testing_uptake(params, policy)

        assert 0.0 <= uptake <= 1.0

    def test_uptake_increases_with_benefits(self):
        """Test that uptake increases with perceived benefits."""
        params = get_default_parameters()
        policy = PolicyConfig(
            name="test",
            description="Test policy",
            allow_genetic_test_results=True,
        )

        uptake_low_benefits = compute_testing_uptake(
            params,
            policy,
            benefits_mean=0.3,
        )
        uptake_high_benefits = compute_testing_uptake(
            params,
            policy,
            benefits_mean=0.7,
        )

        assert uptake_high_benefits > uptake_low_benefits

    def test_uptake_decreases_with_penalty(self):
        """Test that uptake decreases under restrictive policies."""
        params = get_default_parameters()

        permissive = PolicyConfig(
            name="permissive",
            description="Permissive policy",
            allow_genetic_test_results=True,
        )

        restrictive = PolicyConfig(
            name="restrictive",
            description="Restrictive policy",
            allow_genetic_test_results=False,
        )

        uptake_permissive = compute_testing_uptake(params, permissive)
        uptake_restrictive = compute_testing_uptake(params, restrictive)

        # Restrictive policy should increase uptake (less deterrence)
        assert uptake_restrictive >= uptake_permissive


class TestPolicyEffect:
    """Tests for compute_policy_effect."""

    def test_effect_structure(self):
        """Test that effect dictionary has correct structure."""
        params = get_default_parameters()

        policies = get_standard_policies()
        baseline = policies["status_quo"]
        reform = policies["moratorium"]

        effect = compute_policy_effect(params, baseline, reform)

        assert "baseline_uptake" in effect
        assert "reform_uptake" in effect
        assert "absolute_effect" in effect
        assert "relative_effect" in effect

    def test_moratorium_increases_uptake(self):
        """Test that moratorium increases testing uptake vs status quo."""
        params = get_default_parameters()

        policies = get_standard_policies()
        baseline = policies["status_quo"]
        reform = policies["moratorium"]

        effect = compute_policy_effect(params, baseline, reform)

        # Moratorium should increase uptake (less deterrence)
        assert effect["absolute_effect"] >= 0.0
        assert effect["relative_effect"] >= 0.0

    def test_ban_increases_uptake_more_than_moratorium(self):
        """Test that ban increases uptake more than moratorium."""
        params = get_default_parameters()

        policies = get_standard_policies()
        baseline = policies["status_quo"]
        moratorium = policies["moratorium"]
        ban = policies["ban"]

        effect_moratorium = compute_policy_effect(params, baseline, moratorium)
        effect_ban = compute_policy_effect(params, baseline, ban)

        # Ban should have larger effect than moratorium
        assert effect_ban["absolute_effect"] >= effect_moratorium["absolute_effect"]


class TestGetStandardPolicies:
    """Tests for get_standard_policies."""

    def test_returns_all_policies(self):
        """Test that all standard policies are returned."""
        policies = get_standard_policies()

        assert "status_quo" in policies
        assert "moratorium" in policies
        assert "ban" in policies

    def test_policies_are_valid(self):
        """Test that policies are valid PolicyConfig instances."""
        policies = get_standard_policies()

        for name, policy in policies.items():
            assert isinstance(policy, PolicyConfig)
            assert policy.name == name
