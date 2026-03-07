from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


def _normalize_policy_name(raw_name: str) -> str:
    lowered = raw_name.lower()
    if lowered == "status_quo":
        return "status_quo"
    if "moratorium" in lowered:
        return "moratorium"
    if "ban" in lowered:
        return "ban"
    return raw_name


def _normalize_bool(value: bool | str | None, *, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default

    lowered = str(value).strip().lower()
    if lowered in {"true", "yes", "1"}:
        return True
    if lowered in {"false", "no", "0", "none", "null"}:
        return False
    if lowered == "limited":
        return False
    return default


def _normalize_caps(raw_caps: dict[str, Any] | None) -> dict[str, float] | None:
    if raw_caps is None:
        return None
    return {str(key): float(value) for key, value in raw_caps.items()}


def _normalize_enforcement(value: float | int | str | None) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return 0.5

    mapping = {
        "baseline": 0.0,
        "industry": 0.5,
        "industry_or_statutory": 0.75,
        "statutory": 1.0,
    }
    return mapping.get(str(value).strip().lower(), 0.5)


@dataclass(frozen=True)
class LoadedPolicy:
    name: str
    description: str
    allow_genetic_test_results: bool
    allow_family_history: bool
    predictive_only: bool
    sum_insured_caps: dict[str, float] | None
    enforcement_strength: float

    def model_dump(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "allow_genetic_test_results": self.allow_genetic_test_results,
            "allow_family_history": self.allow_family_history,
            "predictive_only": self.predictive_only,
            "sum_insured_caps": self.sum_insured_caps,
            "enforcement_strength": self.enforcement_strength,
        }


@dataclass(frozen=True)
class LoadedPoliciesConfig:
    jurisdiction: str
    domain: str
    policies: dict[str, LoadedPolicy]


def load_policies_config(config_path: str | Path) -> LoadedPoliciesConfig:
    config_path = Path(config_path)
    with config_path.open(encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}

    policies_payload = payload.get("policies", {})
    policies: dict[str, LoadedPolicy] = {}

    for raw_name, raw_policy in policies_payload.items():
        raw_policy = raw_policy or {}
        normalized_name = _normalize_policy_name(str(raw_name))
        policies[normalized_name] = LoadedPolicy(
            name=normalized_name,
            description=str(raw_policy.get("description", normalized_name)),
            allow_genetic_test_results=_normalize_bool(
                raw_policy.get("allow_genetic_test_results"),
                default=True,
            ),
            allow_family_history=_normalize_bool(
                raw_policy.get("allow_family_history"),
                default=True,
            ),
            predictive_only=_normalize_bool(raw_policy.get("predictive_only"), default=False),
            sum_insured_caps=_normalize_caps(raw_policy.get("sum_insured_caps")),
            enforcement_strength=_normalize_enforcement(raw_policy.get("enforcement_strength")),
        )

    return LoadedPoliciesConfig(
        jurisdiction=str(payload.get("jurisdiction", "")),
        domain=str(payload.get("domain", "")),
        policies=policies,
    )
