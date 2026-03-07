"""
Unit tests for Policy Encoder.
"""

from src.model.policy_encoder import (
    EncodedPolicy,
    encode_moratorium,
    encode_statutory_ban,
)


class TestEncodedPolicy:
    """Tests for EncodedPolicy dataclass."""

    def test_creation(self):
        """Test that EncodedPolicy can be instantiated."""
        policy = EncodedPolicy(
            name="test",
            allow_genetic_tests=True,
            allow_family_history=True,
            sum_insured_caps=None,
            enforcement_strength=1.0,
            penalty_max=0.0,
            information_index=1.0,
        )
        assert policy.name == "test"


class TestEncodeMoratorium:
    """Tests for encode_moratorium."""

    def test_default_moratorium(self):
        """Test moratorium with default values."""
        policy = encode_moratorium()
        assert isinstance(policy, EncodedPolicy)
        assert not policy.allow_genetic_tests
        assert policy.allow_family_history
        assert policy.sum_insured_caps["death"] == 500000.0

    def test_custom_caps(self):
        """Test moratorium with custom caps."""
        policy = encode_moratorium(
            cap_death=600000.0,
            cap_tpd=300000.0,
            cap_trauma=300000.0,
        )
        assert policy.sum_insured_caps["death"] == 600000.0
        assert policy.sum_insured_caps["tpd"] == 300000.0


class TestEncodeStatutoryBan:
    """Tests for encode_statutory_ban."""

    def test_default_ban(self):
        """Test statutory ban with default values."""
        policy = encode_statutory_ban()
        assert not policy.allow_genetic_tests
        assert not policy.allow_family_history
        assert policy.penalty_max == 1000000.0

    def test_custom_penalty(self):
        """Test statutory ban with custom penalty."""
        policy = encode_statutory_ban(penalty_max=500000.0)
        assert policy.penalty_max == 500000.0
