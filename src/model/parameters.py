"""
Model parameters with pydantic validation.

This module defines all model parameters with type safety and validation.
Parameters are separated into:
- ModelParameters: Calibrated parameters (from evidence)
- HyperParameters: MCMC settings, computation settings
- PolicyConfig: Policy regime encoding
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field, field_validator
import yaml
from pathlib import Path


class ModelParameters(BaseModel):
    """
    Calibrated model parameters with validation.
    
    All parameters are derived from evidence registers (gdpe_0002).
    """
    
    # =========================================================================
    # Module A: Behavior / Deterrence
    # =========================================================================
    
    baseline_testing_uptake: float = Field(
        default=0.52,
        ge=0.0,
        le=1.0,
        description="Baseline genetic testing uptake (no discrimination concerns)"
    )
    
    deterrence_elasticity: float = Field(
        default=0.18,
        ge=0.0,
        le=1.0,
        description="Proportion avoiding testing due to insurance concerns"
    )
    
    moratorium_effect: float = Field(
        default=0.15,
        ge=0.0,
        le=1.0,
        description="Reduction in deterrence under moratorium"
    )
    
    # =========================================================================
    # Module C: Insurance Equilibrium
    # =========================================================================
    
    adverse_selection_elasticity: float = Field(
        default=0.08,
        ge=0.0,
        description="Premium increase per 10% increase in informed high-risks"
    )
    
    demand_elasticity_high_risk: float = Field(
        default=-0.22,
        le=0.0,
        description="Demand change for high-risk individuals post-positive test"
    )
    
    baseline_loading: float = Field(
        default=0.15,
        ge=0.0,
        description="Baseline premium loading for genetic conditions"
    )
    
    # =========================================================================
    # Module D: Proxy Substitution
    # =========================================================================
    
    family_history_sensitivity: float = Field(
        default=0.68,
        ge=0.0,
        le=1.0,
        description="Sensitivity of family history for mutation detection"
    )
    
    proxy_substitution_rate: float = Field(
        default=0.40,
        ge=0.0,
        le=1.0,
        description="Proportion of genetic risk captured by proxies"
    )
    
    # =========================================================================
    # Module E: Pass-Through / Market Structure
    # =========================================================================
    
    pass_through_rate: float = Field(
        default=0.75,
        ge=0.0,
        le=1.0,
        description="Proportion of risk costs passed to consumers"
    )
    
    # =========================================================================
    # Module F: Data Quality Externality
    # =========================================================================
    
    research_participation_elasticity: float = Field(
        default=-0.10,
        le=0.0,
        description="Change in research participation with privacy concerns"
    )
    
    # =========================================================================
    # Enforcement
    # =========================================================================
    
    enforcement_effectiveness: float = Field(
        default=0.50,
        ge=0.0,
        le=1.0,
        description="Compliance rate with policy regime"
    )
    
    complaint_rate: float = Field(
        default=0.02,
        ge=0.0,
        le=1.0,
        description="Rate of discrimination complaints per 100 tests"
    )
    
    # =========================================================================
    # Metadata
    # =========================================================================
    
    jurisdiction: str = Field(
        default="australia",
        description="Jurisdiction (australia or new_zealand)"
    )
    
    calibration_date: str = Field(
        default="2026-03-03",
        description="Date of calibration"
    )
    
    @field_validator('jurisdiction')
    @classmethod
    def validate_jurisdiction(cls, v: str) -> str:
        if v not in ['australia', 'new_zealand']:
            raise ValueError("jurisdiction must be 'australia' or 'new_zealand'")
        return v
    
    class Config:
        extra = 'forbid'  # Catch typos in parameter names
        json_schema_extra = {
            'example': {
                'baseline_testing_uptake': 0.52,
                'deterrence_elasticity': 0.18,
                'jurisdiction': 'australia',
            }
        }


class HyperParameters(BaseModel):
    """
    Computational and MCMC hyperparameters.
    """
    
    # MCMC settings
    n_draws: int = Field(
        default=2000,
        ge=100,
        description="Number of posterior draws"
    )
    
    n_warmup: int = Field(
        default=1000,
        ge=100,
        description="Number of warmup iterations"
    )
    
    n_chains: int = Field(
        default=4,
        ge=1,
        description="Number of MCMC chains"
    )
    
    random_seed: int = Field(
        default=20260303,
        description="Random seed for reproducibility"
    )
    
    # Computation settings
    use_jit: bool = Field(
        default=True,
        description="Use JAX JIT compilation"
    )
    
    use_vmap: bool = Field(
        default=True,
        description="Use JAX vmap for vectorization"
    )
    
    # Convergence diagnostics
    rhat_threshold: float = Field(
        default=1.1,
        gt=1.0,
        description="R-hat convergence threshold"
    )
    
    class Config:
        extra = 'forbid'


class PolicyConfig(BaseModel):
    """
    Policy regime encoding.
    """
    
    name: str = Field(
        ...,
        description="Policy name (e.g., 'status_quo', 'moratorium', 'ban')"
    )
    
    description: str = Field(
        ...,
        description="Policy description"
    )
    
    # Information restrictions
    allow_genetic_test_results: bool = Field(
        default=True,
        description="Whether insurers can use genetic test results"
    )
    
    allow_family_history: bool = Field(
        default=True,
        description="Whether insurers can use family history"
    )
    
    # Financial caps
    sum_insured_caps: Optional[Dict[str, float]] = Field(
        default=None,
        description="Sum insured caps by product type"
    )
    
    # Enforcement
    enforcement_strength: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Enforcement strength (0=no enforcement, 1=full enforcement)"
    )
    
    # Penalties
    penalty_max: float = Field(
        default=0.0,
        ge=0.0,
        description="Maximum penalty for violations"
    )
    
    class Config:
        extra = 'forbid'


def load_parameters(config_path: str | Path) -> ModelParameters:
    """
    Load parameters from YAML config file.
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        ModelParameters instance
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValidationError: If parameters fail validation
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return ModelParameters(**config)


def load_hyper_parameters(config_path: str | Path) -> HyperParameters:
    """Load hyperparameters from YAML config."""
    config_path = Path(config_path)
    
    if not config_path.exists():
        # Return defaults if no config file
        return HyperParameters()
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return HyperParameters(**config)


def load_policy_config(config_path: str | Path) -> PolicyConfig:
    """Load policy configuration from YAML config."""
    config_path = Path(config_path)
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return PolicyConfig(**config)


# Default parameter instances
DEFAULT_PARAMETERS = ModelParameters()
DEFAULT_HYPER_PARAMETERS = HyperParameters()
