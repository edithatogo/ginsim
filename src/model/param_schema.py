from __future__ import annotations

from pydantic import BaseModel


class BehaviorParamsDraw(BaseModel):
    baseline_logit: float
    policy_shock: float
    trend: float


class ClinicalParamsDraw(BaseModel):
    baseline_event_rate: float
    uptake_to_prevention: float
    prevention_effect: float
    cost_per_event: float
    qaly_loss_per_event: float


class InsuranceParamsDraw(BaseModel):
    base_premium: float
    loss_cost: float
    expense_load: float
    markup: float
    adverse_selection_sensitivity: float
    price_elasticity: float


class PassThroughParamsDraw(BaseModel):
    base_pass_through: float = 0.7
    concentration_slope: float = -0.3
    noise_sd: float = 0.05


class DataQualityParamsDraw(BaseModel):
    base_participation_logit: float
    fear_sensitivity: float
    base_auc: float
    auc_sensitivity: float
    noise_sd: float = 0.01


class PolicyMappingParamsDraw(BaseModel):
    beta_allow: float
    beta_predictive_only: float
    beta_caps: float
    beta_enforcement: float
    intercept: float
