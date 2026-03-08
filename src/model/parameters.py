"""
Parameter schemas and loading logic for the economic model.
"""

from __future__ import annotations

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
    """Calibrated parameters for the model."""

    model_config = ConfigDict(frozen=True)

    # Behavior
    baseline_testing_uptake: float = 0.52
    deterrence_elasticity: float = 0.18
    moratorium_effect: float = 0.15

    # Insurance
    adverse_selection_elasticity: float = 0.08
    demand_elasticity_high_risk: float = -0.22
    baseline_loading: float = 0.15

    # Proxy
    family_history_sensitivity: float = 0.68
    proxy_substitution_rate: float = 0.40

    # Economics
    pass_through_rate: float = 0.75
    research_participation_elasticity: float = -0.1
    research_participation_value: float = 50000.0

    # Enforcement
    enforcement_effectiveness: float = 0.50
    complaint_rate: float = 0.02
    enforcement_budget: float = 1000000.0
    marginal_cost_enforcement: float = 0.1
    compliance_cost_fixed: float = 5000.0
    detection_prob_baseline: float = 0.05

    # Metadata
    jurisdiction: str = "australia"
    calibration_date: str = "2026-03-03"

    def __hash__(self):
        return hash((self.jurisdiction, self.calibration_date, self.baseline_loading))


# Use direct assignment instead of TypeAlias for older tools/compatibility
InsuranceParams = ModelParameters
DataQualityParams = ModelParameters


class HyperParameters(BaseModel):
    """Global simulation hyperparameters."""

    model_config = ConfigDict(frozen=True)

    n_samples: int = 1000
    seed: int = 20260303
    use_priors: bool = True
