"""
Unit tests for policy encoder.
"""

import pytest

from src.model.policy_encoder import (
    encode_status_quo,
    encode_moratorium,
    encode_statutory_ban,
    get_standard_policies,
    encode_custom_policy,
)


class TestEncodeStatusQuo:
    """Tests for encode_status_quo."""
    
    def test_returns_encoded_policy(self):
        """Test that status quo is encoded correctly."""
        policy = encode_status_quo()
        
        assert policy.name == "status_quo"
        assert policy.allow_genetic_tests is True
        assert policy.allow_family_history is True
        assert policy.sum_insured_caps is None
        assert policy.enforcement_strength == 1.0
        assert policy.penalty_max == 0.0
        assert policy.information_index == 1.0
    
    def test_to_policy_config(self):
        """Test conversion to PolicyConfig."""
        policy = encode_status_quo()
        config = policy.to_policy_config()
        
        assert config.name == "status_quo"
        assert config.allow_genetic_test_results is True


class TestEncodeMoratorium:
    """Tests for encode_moratorium."""
    
    def test_returns_encoded_policy(self):
        """Test that moratorium is encoded correctly."""
        policy = encode_moratorium()
        
        assert policy.name == "moratorium"
        assert policy.allow_genetic_tests is False
        assert policy.allow_family_history is True
        assert policy.sum_insured_caps is not None
        assert policy.enforcement_strength == 0.5
        assert policy.penalty_max == 0.0
        assert policy.information_index == 0.3
    
    def test_custom_caps(self):
        """Test moratorium with custom caps."""
        policy = encode_moratorium(
            cap_death=600000,
            cap_tpd=300000,
            cap_trauma=300000,
        )
        
        assert policy.sum_insured_caps['death'] == 600000
        assert policy.sum_insured_caps['tpd'] == 300000


class TestEncodeStatutoryBan:
    """Tests for encode_statutory_ban."""
    
    def test_returns_encoded_policy(self):
        """Test that statutory ban is encoded correctly."""
        policy = encode_statutory_ban()
        
        assert policy.name == "statutory_ban"
        assert policy.allow_genetic_tests is False
        assert policy.allow_family_history is False
        assert policy.sum_insured_caps is None
        assert policy.enforcement_strength == 1.0
        assert policy.penalty_max == 1000000
        assert policy.information_index == 0.0
    
    def test_custom_penalty(self):
        """Test statutory ban with custom penalty."""
        policy = encode_statutory_ban(penalty_max=500000)
        
        assert policy.penalty_max == 500000


class TestGetStandardPolicies:
    """Tests for get_standard_policies."""
    
    def test_returns_all_policies(self):
        """Test that all standard policies are returned."""
        policies = get_standard_policies()
        
        assert 'status_quo' in policies
        assert 'moratorium' in policies
        assert 'statutory_ban' in policies
    
    def test_policies_are_encoded(self):
        """Test that policies are EncodedPolicy objects."""
        policies = get_standard_policies()
        
        for name, policy in policies.items():
            assert hasattr(policy, 'name')
            assert hasattr(policy, 'allow_genetic_tests')
            assert hasattr(policy, 'to_policy_config')


class TestEncodeCustomPolicy:
    """Tests for encode_custom_policy."""
    
    def test_returns_encoded_policy(self):
        """Test that custom policy is encoded correctly."""
        policy = encode_custom_policy(
            name="custom",
            allow_genetic_tests=False,
            allow_family_history=True,
            enforcement_strength=0.8,
        )
        
        assert policy.name == "custom"
        assert policy.allow_genetic_tests is False
        assert policy.allow_family_history is True
        assert policy.enforcement_strength == 0.8
    
    def test_information_index_computed(self):
        """Test that information index is computed correctly."""
        # Full information
        policy_full = encode_custom_policy(
            name="full",
            allow_genetic_tests=True,
            allow_family_history=True,
        )
        assert policy_full.information_index == 1.0
        
        # Partial information (family history only)
        policy_partial = encode_custom_policy(
            name="partial",
            allow_genetic_tests=False,
            allow_family_history=True,
        )
        assert policy_partial.information_index == 0.5
        
        # No information
        policy_none = encode_custom_policy(
            name="none",
            allow_genetic_tests=False,
            allow_family_history=False,
        )
        assert policy_none.information_index == 0.0
