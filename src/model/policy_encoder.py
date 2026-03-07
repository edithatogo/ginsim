"""
Policy scenario encoder.

Encodes policy regimes into model-ready parameters.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .parameters import PolicyConfig


def _float_caps(sum_insured_caps: dict[str, float | int] | None) -> dict[str, float] | None:
    """Normalize legacy integer caps to float-valued policy caps."""
    if sum_insured_caps is None:
        return None
    return {key: float(value) for key, value in sum_insured_caps.items()}


class PolicyRegime(Enum):
    """Standard policy regimes."""

    STATUS_QUO = "status_quo"
    MORATORIUM = "moratorium"
    STATUTORY_BAN = "statutory_ban"


@dataclass
class EncodedPolicy:
    """
    Encoded policy parameters for model evaluation.

    Attributes:
        name: Policy name
        allow_genetic_tests: Whether genetic test results can be used
        allow_family_history: Whether family history can be used
        sum_insured_caps: Caps by product type (None = no caps)
        enforcement_strength: Enforcement strength (0-1)
        penalty_max: Maximum penalty for violations
        information_index: Information availability index (0-1)
    """

    name: str
    allow_genetic_tests: bool
    allow_family_history: bool
    sum_insured_caps: dict[str, float] | None
    enforcement_strength: float
    penalty_max: float
    information_index: float  # 0 = no information, 1 = full information

    def to_policy_config(self) -> PolicyConfig:
        """Convert to PolicyConfig."""
        return PolicyConfig(
            name=self.name,
            description=f"Encoded policy: {self.name}",
            allow_genetic_test_results=self.allow_genetic_tests,
            allow_family_history=self.allow_family_history,
            sum_insured_caps=_float_caps(self.sum_insured_caps),
            enforcement_strength=self.enforcement_strength,
            penalty_max=self.penalty_max,
        )


def encode_status_quo() -> EncodedPolicy:
    """
    Encode status quo policy (no restrictions).

    Returns:
        EncodedPolicy object
    """
    return EncodedPolicy(
        name="status_quo",
        allow_genetic_tests=True,
        allow_family_history=True,
        sum_insured_caps=None,
        enforcement_strength=1.0,
        penalty_max=0.0,
        information_index=1.0,  # Full information
    )


def encode_moratorium(
    cap_death: float = 500000,
    cap_tpd: float = 200000,
    cap_trauma: float = 200000,
    enforcement_strength: float = 0.5,
) -> EncodedPolicy:
    """
    Encode industry moratorium policy.

    Args:
        cap_death: Cap for life insurance
        cap_tpd: Cap for TPD insurance
        cap_trauma: Cap for trauma insurance
        enforcement_strength: Industry self-enforcement strength

    Returns:
        EncodedPolicy object
    """
    return EncodedPolicy(
        name="moratorium",
        allow_genetic_tests=False,
        allow_family_history=True,
        sum_insured_caps=_float_caps(
            {
                "death": cap_death,
                "tpd": cap_tpd,
                "trauma": cap_trauma,
            }
        ),
        enforcement_strength=enforcement_strength,
        penalty_max=0.0,  # Industry self-regulation
        information_index=0.3,  # Partial information (below caps)
    )


def encode_statutory_ban(
    enforcement_strength: float = 1.0,
    penalty_max: float = 1000000,
) -> EncodedPolicy:
    """
    Encode statutory ban policy.

    Args:
        enforcement_strength: Regulatory enforcement strength
        penalty_max: Maximum statutory penalty

    Returns:
        EncodedPolicy object
    """
    return EncodedPolicy(
        name="statutory_ban",
        allow_genetic_tests=False,
        allow_family_history=False,
        sum_insured_caps=None,
        enforcement_strength=enforcement_strength,
        penalty_max=float(penalty_max),
        information_index=0.0,  # No genetic information
    )


def get_standard_policies() -> dict[str, EncodedPolicy]:
    """
    Get all standard encoded policies.

    Returns:
        Dictionary mapping policy name to EncodedPolicy
    """
    return {
        "status_quo": encode_status_quo(),
        "moratorium": encode_moratorium(),
        "statutory_ban": encode_statutory_ban(),
    }


def encode_custom_policy(
    name: str,
    allow_genetic_tests: bool,
    allow_family_history: bool,
    sum_insured_caps: dict[str, float] | None = None,
    enforcement_strength: float = 0.5,
    penalty_max: float = 0.0,
) -> EncodedPolicy:
    """
    Encode custom policy.

    Args:
        name: Policy name
        allow_genetic_tests: Whether genetic tests allowed
        allow_family_history: Whether family history allowed
        sum_insured_caps: Sum insured caps
        enforcement_strength: Enforcement strength
        penalty_max: Maximum penalty

    Returns:
        EncodedPolicy object
    """
    # Compute information index
    info_index = 0.0
    if allow_genetic_tests:
        info_index = 1.0
    elif allow_family_history:
        info_index = 0.5
    if sum_insured_caps is not None:
        # Partial information below caps
        info_index = max(info_index, 0.3)

    return EncodedPolicy(
        name=name,
        allow_genetic_tests=allow_genetic_tests,
        allow_family_history=allow_family_history,
        sum_insured_caps=_float_caps(sum_insured_caps),
        enforcement_strength=enforcement_strength,
        penalty_max=penalty_max,
        information_index=info_index,
    )
