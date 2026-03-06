"""
Unit tests for config serialization with msgspec.
"""

import tempfile

from src.model.config_serialization import (
    MsgSpecConfig,
    config_from_dict,
    config_from_yaml,
    config_to_dict,
    config_to_yaml,
    load_config,
    save_config,
)


class TestMsgSpecConfig:
    """Tests for MsgSpecConfig."""

    def test_create_config(self):
        """Test config creation with defaults."""
        config = MsgSpecConfig(jurisdiction="australia")

        assert config.jurisdiction == "australia"
        assert config.n_draws == 2000
        assert config.random_seed == 20260303

    def test_create_config_with_values(self):
        """Test config creation with custom values."""
        config = MsgSpecConfig(
            jurisdiction="new_zealand",
            n_draws=1000,
            baseline_testing_uptake=0.60,
        )

        assert config.jurisdiction == "new_zealand"
        assert config.n_draws == 1000
        assert config.baseline_testing_uptake == 0.60


class TestSaveLoadConfig:
    """Tests for save_config and load_config."""

    def test_save_load_json(self):
        """Test save and load JSON config."""
        config = MsgSpecConfig(jurisdiction="australia", n_draws=1500)

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            save_config(config, f.name)
            config2 = load_config(f.name)

        assert config2.jurisdiction == config.jurisdiction
        assert config2.n_draws == config.n_draws

    def test_save_load_yaml(self):
        """Test save and load YAML config."""
        config = MsgSpecConfig(jurisdiction="new_zealand", n_draws=2500)

        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            config_to_yaml(config, f.name)
            config2 = config_from_yaml(f.name)

        assert config2.jurisdiction == config.jurisdiction
        assert config2.n_draws == config.n_draws


class TestConfigConversion:
    """Tests for config conversion."""

    def test_config_to_dict(self):
        """Test config to dictionary conversion."""
        config = MsgSpecConfig(jurisdiction="australia")
        config_dict = config_to_dict(config)

        assert isinstance(config_dict, dict)
        assert config_dict["jurisdiction"] == "australia"
        assert config_dict["n_draws"] == 2000

    def test_config_from_dict(self):
        """Test config from dictionary conversion."""
        config_dict = {
            "jurisdiction": "new_zealand",
            "n_draws": 3000,
        }
        config = config_from_dict(config_dict)

        assert config.jurisdiction == "new_zealand"
        assert config.n_draws == 3000

    def test_roundtrip_dict(self):
        """Test roundtrip dictionary conversion."""
        config1 = MsgSpecConfig(jurisdiction="australia", n_draws=1500)
        config_dict = config_to_dict(config1)
        config2 = config_from_dict(config_dict)

        assert config2.jurisdiction == config1.jurisdiction
        assert config2.n_draws == config1.n_draws
