"""
Shared model parameters and policy configurations (Diamond Standard).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jax
import yaml


@dataclass(frozen=True, eq=False)
class PolicyConfig:
    """Configuration for a specific policy regime."""

    name: str
    description: str
    allow_genetic_test_results: bool
    allow_family_history: bool = True
    enforcement_strength: Any = 0.5
    penalty_max: Any = 0.0
    sum_insured_caps: dict[str, float] | None = None
    taper_range: Any = 0.0
    penalty_type: str = "civil"

    def __hash__(self):
        # Static metadata for JAX hashing
        return hash((self.name, self.allow_genetic_test_results, self.allow_family_history, self.penalty_type))

    def __eq__(self, other):
        if not isinstance(other, PolicyConfig):
            return False
        return (self.name == other.name and 
                self.allow_genetic_test_results == other.allow_genetic_test_results and
                self.allow_family_history == other.allow_family_history and
                self.penalty_type == other.penalty_type)

    def model_copy(self, update: dict[str, Any]) -> PolicyConfig:
        """Compatibility method."""
        from dataclasses import replace
        return replace(self, **update)


@dataclass(frozen=True, eq=False)
class ModelParameters:
    """
    Consolidated model parameters.
    Fields are Any to allow JAX tracers (BatchTracer) without validation issues.
    """

    jurisdiction: str
    calibration_date: str

    # Behavior (Module A)
    baseline_testing_uptake: Any
    deterrence_elasticity: Any
    moratorium_effect: Any

    # Insurance Market (Module C)
    adverse_selection_elasticity: Any
    demand_elasticity_high_risk: Any
    baseline_loading: Any

    # Proxy Mapping (Module D)
    family_history_sensitivity: Any
    proxy_substitution_rate: Any

    # Supply Chain (Module E)
    pass_through_rate: Any

    # Social Value (Module F)
    research_participation_elasticity: Any
    research_participation_value: Any

    # Welfare Normalization (DCBA)
    ppp_conversion_factor: Any
    equity_factor: Any = 1.0

    # Market Microstructure
    high_sum_insured_share: Any = 0.25
    taper_range: Any = 0.0

    # Enforcement
    enforcement_effectiveness: Any = 0.5
    complaint_rate: Any = 0.01
    enforcement_budget: Any = 1e6
    marginal_cost_enforcement: Any = 100.0
    compliance_cost_fixed: Any = 50000.0
    detection_prob_baseline: Any = 0.1

    # NZ System Specifics
    acc_deterrence_offset: Any = 0.0
    pharmac_qaly_threshold: Any = 50000.0

    # AU System Specifics
    medicare_cost_share: Any = 0.0
    audit_intensity: Any = 0.50
    remoteness_weight: Any = 0.20

    def __hash__(self):
        # We only hash static strings to ensure cache stability
        return hash((self.jurisdiction, self.calibration_date))

    def __eq__(self, other):
        if not isinstance(other, ModelParameters):
            return False
        # Only compare static fields to avoid TracerBoolConversionError
        return (self.jurisdiction == other.jurisdiction and 
                self.calibration_date == other.calibration_date)

    def model_copy(self, update: dict[str, Any]) -> ModelParameters:
        """Compatibility method."""
        from dataclasses import replace
        return replace(self, **update)


# =============================================================================
# JAX PyTree Registration
# =============================================================================
def _model_params_flatten(params: ModelParameters):
    children = (
        params.baseline_testing_uptake,
        params.deterrence_elasticity,
        params.moratorium_effect,
        params.adverse_selection_elasticity,
        params.demand_elasticity_high_risk,
        params.baseline_loading,
        params.family_history_sensitivity,
        params.proxy_substitution_rate,
        params.pass_through_rate,
        params.research_participation_elasticity,
        params.research_participation_value,
        params.ppp_conversion_factor,
        params.equity_factor,
        params.high_sum_insured_share,
        params.taper_range,
        params.enforcement_effectiveness,
        params.complaint_rate,
        params.enforcement_budget,
        params.marginal_cost_enforcement,
        params.compliance_cost_fixed,
        params.detection_prob_baseline,
        params.acc_deterrence_offset,
        params.pharmac_qaly_threshold,
        params.medicare_cost_share,
        params.audit_intensity,
        params.remoteness_weight,
    )
    aux_data = {
        "jurisdiction": params.jurisdiction,
        "calibration_date": params.calibration_date,
    }
    return (children, aux_data)


def _model_params_unflatten(aux_data: dict[str, Any], children: tuple[Any, ...]):
    return ModelParameters(
        baseline_testing_uptake=children[0],
        deterrence_elasticity=children[1],
        moratorium_effect=children[2],
        adverse_selection_elasticity=children[3],
        demand_elasticity_high_risk=children[4],
        baseline_loading=children[5],
        family_history_sensitivity=children[6],
        proxy_substitution_rate=children[7],
        pass_through_rate=children[8],
        research_participation_elasticity=children[9],
        research_participation_value=children[10],
        ppp_conversion_factor=children[11],
        equity_factor=children[12],
        high_sum_insured_share=children[13],
        taper_range=children[14],
        enforcement_effectiveness=children[15],
        complaint_rate=children[16],
        enforcement_budget=children[17],
        marginal_cost_enforcement=children[18],
        compliance_cost_fixed=children[19],
        detection_prob_baseline=children[20],
        acc_deterrence_offset=children[21],
        pharmac_qaly_threshold=children[22],
        medicare_cost_share=children[23],
        audit_intensity=children[24],
        remoteness_weight=children[25],
        **aux_data,
    )


jax.tree_util.register_pytree_node(
    ModelParameters,
    _model_params_flatten,
    _model_params_unflatten,
)


def load_jurisdiction_parameters(jurisdiction: str) -> ModelParameters:
    """Load parameters from YAML."""
    config_dir = Path(__file__).parent.parent.parent / "configs" / "jurisdictions"
    config_path = config_dir / f"{jurisdiction.lower()}.yaml"
    if not config_path.exists():
        config_path = Path("configs/jurisdictions") / f"{jurisdiction.lower()}.yaml"
    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return ModelParameters(**data)


def get_default_parameters() -> ModelParameters:
    """Default Australian parameters."""
    return load_jurisdiction_parameters("australia")


Params = ModelParameters


@dataclass(frozen=True)
class HyperParameters:
    """Global simulation hyperparameters."""
    n_samples: int = 1000
    seed: int = 20260303
    use_priors: bool = True
