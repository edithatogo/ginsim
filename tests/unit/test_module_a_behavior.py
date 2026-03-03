"""
Unit tests for Module A: Behavior / Deterrence.
"""

import pytest
import jax.numpy as jnp
from jax import random

from src.model.parameters import ModelParameters, PolicyConfig
from src.model.module_a_behavior import (
    compute_perceived_penalty,
    compute_testing_utility,
    compute_testing_probability,
    compute_testing_uptake,
    compute_policy_effect,
    get_standard_policies,
)


class TestPerceivedPenalty:
    """Tests for compute_perceived_penalty."""
    
    def test_penalty_positive(self):
        """Test that penalty is always positive."""
        params = ModelParameters()
        policy = PolicyConfig(
            name='test',
            description='Test policy',
            allow_genetic_test_results=True,
        )
        
        penalty = compute_perceived_penalty(params, policy)
        
        assert penalty >= 0.0
    
    def test_penalty_reduced_by_restrictions(self):
        """Test that information restrictions reduce penalty."""
        params = ModelParameters()
        
        # Permissive policy
        permissive = PolicyConfig(
            name='permissive',
            description='Permissive policy',
            allow_genetic_test_results=True,
            enforcement_strength=1.0,
        )
        
        # Restrictive policy
        restrictive = PolicyConfig(
            name='restrictive',
            description='Restrictive policy',
            allow_genetic_test_results=False,
            enforcement_strength=1.0,
        )
        
        penalty_permissive = compute_perceived_penalty(params, permissive)
        penalty_restrictive = compute_perceived_penalty(params, restrictive)
        
        # Restrictive policy should have lower penalty
        assert penalty_restrictive < penalty_permissive
    
    def test_penalty_reduced_by_enforcement(self):
        """Test that stronger enforcement reduces penalty."""
        params = ModelParameters()
        
        weak_enforcement = PolicyConfig(
            name='weak',
            description='Weak enforcement',
            allow_genetic_test_results=False,
            enforcement_strength=0.2,
        )
        
        strong_enforcement = PolicyConfig(
            name='strong',
            description='Strong enforcement',
            allow_genetic_test_results=False,
            enforcement_strength=1.0,
        )
        
        penalty_weak = compute_perceived_penalty(params, weak_enforcement)
        penalty_strong = compute_perceived_penalty(params, strong_enforcement)
        
        # Stronger enforcement should reduce penalty more
        assert penalty_strong <= penalty_weak


class TestTestingUtility:
    """Tests for compute_testing_utility."""
    
    def test_utility_increases_with_benefits(self):
        """Test that utility increases with benefits."""
        penalty = 0.1
        
        utility_low = compute_testing_utility(benefits=0.3, perceived_penalty=penalty)
        utility_high = compute_testing_utility(benefits=0.7, perceived_penalty=penalty)
        
        assert utility_high > utility_low
    
    def test_utility_decreases_with_penalty(self):
        """Test that utility decreases with penalty."""
        benefits = 0.5
        
        utility_low_penalty = compute_testing_utility(
            benefits=benefits, perceived_penalty=0.1
        )
        utility_high_penalty = compute_testing_utility(
            benefits=benefits, perceived_penalty=0.5
        )
        
        assert utility_high_penalty < utility_low_penalty


class TestTestingProbability:
    """Tests for compute_testing_probability."""
    
    def test_probability_bounded(self):
        """Test that probability is bounded [0, 1]."""
        for utility in [-10.0, -1.0, 0.0, 1.0, 10.0]:
            prob = compute_testing_probability(utility)
            assert 0.0 <= prob <= 1.0
    
    def test_probability_increases_with_utility(self):
        """Test that probability increases with utility."""
        prob_low = compute_testing_probability(-1.0)
        prob_high = compute_testing_probability(1.0)
        
        assert prob_high > prob_low
    
    def test_probability_at_zero_utility(self):
        """Test that probability is 0.5 at zero utility."""
        prob = compute_testing_probability(0.0)
        assert jnp.isclose(prob, 0.5, atol=1e-6)


class TestTestingUptake:
    """Tests for compute_testing_uptake."""
    
    def test_uptake_bounded(self):
        """Test that uptake is bounded [0, 1]."""
        params = ModelParameters()
        policy = PolicyConfig(
            name='test',
            description='Test policy',
            allow_genetic_test_results=True,
        )
        
        uptake = compute_testing_uptake(params, policy)
        
        assert 0.0 <= uptake <= 1.0
    
    def test_uptake_increases_with_benefits(self):
        """Test that uptake increases with perceived benefits."""
        params = ModelParameters()
        policy = PolicyConfig(
            name='test',
            description='Test policy',
            allow_genetic_test_results=True,
        )
        
        uptake_low_benefits = compute_testing_uptake(
            params, policy, benefits_mean=0.3
        )
        uptake_high_benefits = compute_testing_uptake(
            params, policy, benefits_mean=0.7
        )
        
        assert uptake_high_benefits > uptake_low_benefits
    
    def test_uptake_decreases_with_penalty(self):
        """Test that uptake decreases under restrictive policies."""
        params = ModelParameters()
        
        permissive = PolicyConfig(
            name='permissive',
            description='Permissive policy',
            allow_genetic_test_results=True,
        )
        
        restrictive = PolicyConfig(
            name='restrictive',
            description='Restrictive policy',
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
        params = ModelParameters()
        
        policies = get_standard_policies()
        baseline = policies['status_quo']
        reform = policies['moratorium']
        
        effect = compute_policy_effect(params, baseline, reform)
        
        assert 'baseline_uptake' in effect
        assert 'reform_uptake' in effect
        assert 'absolute_effect' in effect
        assert 'relative_effect' in effect
    
    def test_moratorium_increases_uptake(self):
        """Test that moratorium increases testing uptake vs status quo."""
        params = ModelParameters()
        
        policies = get_standard_policies()
        baseline = policies['status_quo']
        reform = policies['moratorium']
        
        effect = compute_policy_effect(params, baseline, reform)
        
        # Moratorium should increase uptake (less deterrence)
        assert effect['absolute_effect'] >= 0.0
        assert effect['relative_effect'] >= 0.0
    
    def test_ban_increases_uptake_more_than_moratorium(self):
        """Test that ban increases uptake more than moratorium."""
        params = ModelParameters()
        
        policies = get_standard_policies()
        baseline = policies['status_quo']
        moratorium = policies['moratorium']
        ban = policies['ban']
        
        effect_moratorium = compute_policy_effect(params, baseline, moratorium)
        effect_ban = compute_policy_effect(params, baseline, ban)
        
        # Ban should have larger effect than moratorium
        assert effect_ban['absolute_effect'] >= effect_moratorium['absolute_effect']


class TestGetStandardPolicies:
    """Tests for get_standard_policies."""
    
    def test_returns_all_policies(self):
        """Test that all standard policies are returned."""
        policies = get_standard_policies()
        
        assert 'status_quo' in policies
        assert 'moratorium' in policies
        assert 'ban' in policies
    
    def test_policies_are_valid(self):
        """Test that policies are valid PolicyConfig instances."""
        policies = get_standard_policies()
        
        for name, policy in policies.items():
            assert isinstance(policy, PolicyConfig)
            assert policy.name == name
