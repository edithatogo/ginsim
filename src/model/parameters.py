"""
Parameter schemas and loading logic for the economic model.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict


class PolicyConfig(BaseModel):
    """Configuration for a specific policy regime."""

    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    allow_genetic_test_results: bool = True
    allow_family_history: bool = True
    enforcement_strength: float = 1.0
    penalty_max: float = 0.0
    penalty_type: str = "fixed"
    sum_insured_caps: dict[str, float] | None = None

    def __hash__(self):
        return hash((self.name, self.allow_genetic_test_results, self.enforcement_strength))


class ModelParameters(BaseModel):
    """Calibrated parameters for the model (Diamond Standard)."""

    model_config = ConfigDict(frozen=True)

    # Behavior
    baseline_testing_uptake: float
    deterrence_elasticity: float
    moratorium_effect: float

    # Insurance
    adverse_selection_elasticity: float
    demand_elasticity_high_risk: float
    baseline_loading: float

    # Proxy
    family_history_sensitivity: float
    proxy_substitution_rate: float

    # Economics
    pass_through_rate: float
    research_participation_elasticity: float
    research_participation_value: float
    ppp_conversion_factor: float = 1.0
    high_sum_insured_share: float = 0.25  # Share of market above typical caps
    equity_factor: float = 1.0
    taper_range: float = 0.0

    # Enforcement
    enforcement_effectiveness: float
    complaint_rate: float
    enforcement_budget: float
    marginal_cost_enforcement: float
    compliance_cost_fixed: float
    detection_prob_baseline: float
    acc_deterrence_offset: float = 0.0
    pharmac_qaly_threshold: float = 50000.0
    medicare_cost_share: float = 0.0
    audit_intensity: float = 0.5
    audit_intensity_apra: float = 0.5
    audit_intensity_asic: float = 0.5
    remoteness_weight: float = 0.2
    time_horizon: int = 10
    tech_improvement_rate: float = 0.15

    # Metadata
    jurisdiction: str
    calibration_date: str

    def __hash__(self):
        return hash((self.jurisdiction, self.calibration_date, self.baseline_loading))


def load_jurisdiction_parameters(jurisdiction: str) -> ModelParameters:
    """
    Load parameters for a specific jurisdiction from YAML.
    """
    # Look for config relative to project root
    # Try multiple common locations for reliability
    roots = [Path.cwd(), Path(__file__).parent.parent.parent]

    config_path = None
    for root in roots:
        target = root / "configs" / "jurisdictions" / f"{jurisdiction}.yaml"
        if target.exists():
            config_path = target
            break

    if not config_path:
        raise FileNotFoundError(f"Config for jurisdiction '{jurisdiction}' not found.")

    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return ModelParameters(**data)


def get_default_parameters() -> ModelParameters:
    """
    Backward compatibility helper: returns Australian defaults.
    """
    try:
        return load_jurisdiction_parameters("australia")
    except Exception:
        # Emergency hardcoded fallback if file system access fails during tests
        return ModelParameters(
            baseline_testing_uptake=0.52,
            deterrence_elasticity=0.18,
            moratorium_effect=0.15,
            adverse_selection_elasticity=0.08,
            demand_elasticity_high_risk=-0.22,
            baseline_loading=0.15,
            family_history_sensitivity=0.68,
            proxy_substitution_rate=0.40,
            pass_through_rate=0.75,
            research_participation_elasticity=-0.1,
            research_participation_value=50000.0,
            ppp_conversion_factor=1.0,
            enforcement_effectiveness=0.50,
            complaint_rate=0.02,
            enforcement_budget=1000000.0,
            marginal_cost_enforcement=0.1,
            compliance_cost_fixed=5000.0,
            detection_prob_baseline=0.05,
            jurisdiction="australia",
            calibration_date="2026-03-03",
        )


# Use direct assignment instead of TypeAlias for older tools/compatibility
InsuranceParams = ModelParameters
DataQualityParams = ModelParameters


class HyperParameters(BaseModel):
    """Global simulation hyperparameters."""

    model_config = ConfigDict(frozen=True)

    n_samples: int = 1000
    seed: int = 20260303
    use_priors: bool = True
