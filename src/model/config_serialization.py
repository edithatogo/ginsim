"""
Config serialization with msgspec.

Provides fast serialization/deserialization for model configurations.
10-80x faster than pydantic for JSON encoding/decoding.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import msgspec


class MsgSpecConfig(msgspec.Struct):
    """
    Fast config with validation using msgspec.

    Benefits:
    - 10-80x faster than pydantic
    - Zero-cost validation during deserialization
    - Supports JSON, YAML, MessagePack, TOML
    """

    jurisdiction: str
    n_draws: int = 2000
    random_seed: int = 20260303

    # Module A parameters
    baseline_testing_uptake: float = 0.52
    deterrence_elasticity: float = 0.18
    moratorium_effect: float = 0.15

    # Module C parameters
    adverse_selection_elasticity: float = 0.08
    demand_elasticity_high_risk: float = -0.22
    baseline_loading: float = 0.15

    # Module D parameters
    family_history_sensitivity: float = 0.68
    proxy_substitution_rate: float = 0.40

    # Module E parameters
    pass_through_rate: float = 0.75

    # Module F parameters
    research_participation_elasticity: float = -0.10

    # Enforcement parameters
    enforcement_effectiveness: float = 0.50
    complaint_rate: float = 0.02


def save_config(config: MsgSpecConfig, path: str | Path) -> None:
    """
    Save config to JSON file.

    Args:
        config: Config object
        path: Output file path
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    json_bytes = msgspec.json.encode(config)
    path.write_bytes(json_bytes)


def load_config(path: str | Path) -> MsgSpecConfig:
    """
    Load config from JSON file with validation.

    Args:
        path: Input file path

    Returns:
        Validated config object
    """
    path = Path(path)
    json_bytes = path.read_bytes()

    return msgspec.json.decode(json_bytes, type=MsgSpecConfig)


def config_to_yaml(config: MsgSpecConfig, path: str | Path) -> None:
    """
    Save config to YAML file.

    Args:
        config: Config object
        path: Output file path
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    yaml_bytes = msgspec.yaml.encode(config)
    path.write_bytes(yaml_bytes)


def config_from_yaml(path: str | Path) -> MsgSpecConfig:
    """
    Load config from YAML file with validation.

    Args:
        path: Input file path

    Returns:
        Validated config object
    """
    path = Path(path)
    yaml_bytes = path.read_bytes()

    return msgspec.yaml.decode(yaml_bytes, type=MsgSpecConfig)


def config_to_dict(config: MsgSpecConfig) -> dict[str, Any]:
    """
    Convert config to dictionary.

    Args:
        config: Config object

    Returns:
        Dictionary representation
    """
    return msgspec.structs.asdict(config)


def config_from_dict(data: dict[str, Any]) -> MsgSpecConfig:
    """
    Create config from dictionary.

    Args:
        data: Dictionary with config values

    Returns:
        Validated config object
    """
    return msgspec.convert(data, MsgSpecConfig)


# Example usage
if __name__ == "__main__":
    # Create config
    config = MsgSpecConfig(
        jurisdiction="australia",
        n_draws=2000,
    )

    # Save/load JSON
    save_config(config, "outputs/config_test.json")
    config2 = load_config("outputs/config_test.json")

    # Save/load YAML
    config_to_yaml(config, "outputs/config_test.yaml")
    config3 = config_from_yaml("outputs/config_test.yaml")

    # Convert to/from dict
    config_dict = config_to_dict(config)
    config4 = config_from_dict(config_dict)
