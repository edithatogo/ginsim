"""
Module F: Data Quality Externality model.

Implements public goods game for research participation.

Strategic Game: Participation as Public Good
- Players: Individuals (participation decisions), Researchers, Health system
- Mechanism: Participation improves dataset representativeness and future tools
- Equilibrium: Participation rate as function of privacy protections
"""

from __future__ import annotations

from dataclasses import dataclass

import jax.numpy as jnp
from jax import jit
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig


def _to_float_scalar(value: Float[Array, ""] | float | int) -> Float[Array, ""]:
    """Normalize scalar-like inputs to float JAX arrays."""
    return jnp.asarray(value, dtype=jnp.float32)


@dataclass
class DataQualityMetrics:
    """
    Data quality metrics.
    """

    participation_rate: Float[Array, ""]
    representativeness: Float[Array, ""]
    predictive_performance: Float[Array, ""]
    selection_bias: Float[Array, ""]


@dataclass(frozen=True)
class DataQualityParams:
    """Compact data quality parameters used by glue scripts."""

    base_participation_logit: float
    fear_sensitivity: float
    base_auc: float
    auc_sensitivity: float


@jit
def compute_participation_probability(
    privacy_protections: Float[Array, ""] | float | int,
    social_benefit: Float[Array, ""] | float | int,
    privacy_concern: Float[Array, "..."] | float | int,
    elasticity: float = -0.10,
) -> Float[Array, "..."]:
    """
    Compute probability of research participation.
    """
    privacy_protections = _to_float_scalar(privacy_protections)
    social_benefit = _to_float_scalar(social_benefit)
    privacy_concern = jnp.asarray(privacy_concern, dtype=jnp.float32)
    # Base participation rate
    base_rate = 0.5

    # Effect of privacy protections
    protection_effect = elasticity * (1.0 - privacy_protections)

    # Effect of social benefit
    benefit_effect = 0.2 * social_benefit

    # Effect of privacy concerns
    concern_effect = -0.3 * privacy_concern

    # Final participation probability
    participation_prob = base_rate + protection_effect + benefit_effect + concern_effect

    # Bound [0, 1]
    participation_prob = jnp.clip(participation_prob, 0.0, 1.0)

    return participation_prob


def compute_participation_rate(
    params: ModelParameters,
    policy: PolicyConfig,
    n_individuals: int = 1000,
    rng_key: Array | None = None,
) -> Float[Array, ""]:
    """
    Compute aggregate research participation rate.
    """
    # Privacy protections from policy
    if not policy.allow_genetic_test_results:
        privacy_protections = policy.enforcement_strength
    else:
        privacy_protections = 0.2  # Low protections if information allowed

    # Social benefit (assumed constant)
    social_benefit = 0.6

    # Simulate heterogeneous privacy concerns
    if rng_key is not None:
        import jax.random as jr

        privacy_concerns = jr.uniform(rng_key, (n_individuals,))
    else:
        privacy_concerns = jnp.linspace(0, 1, n_individuals)

    # Compute participation probabilities
    participation_probs = compute_participation_probability(
        privacy_protections=jnp.array(privacy_protections),
        social_benefit=jnp.array(social_benefit),
        privacy_concern=privacy_concerns,
        elasticity=params.research_participation_elasticity,
    )

    # Aggregate participation rate
    participation_rate = jnp.mean(participation_probs)

    return participation_rate


@jit
def compute_representativeness(
    participation_rate: Float[Array, ""] | float | int,
    selection_bias_parameter: float = 0.5,
) -> Float[Array, ""]:
    """
    Compute sample representativeness as function of participation.
    """
    participation_rate = _to_float_scalar(participation_rate)
    representativeness = participation_rate ** (1.0 - selection_bias_parameter)
    return representativeness


@jit
def compute_scientific_power(
    representativeness: Float[Array, ""] | float | int,
    threshold: float = 0.4,
    steepness: float = 10.0,
) -> Float[Array, ""]:
    """
    Compute scientific power as non-linear function of representativeness.
    """
    representativeness = _to_float_scalar(representativeness)
    return 1.0 / (1.0 + jnp.exp(-steepness * (representativeness - threshold)))


@jit
def compute_predictive_performance(
    representativeness: Float[Array, ""] | float | int,
    baseline_performance: float = 0.8,
    max_performance: float = 0.95,
) -> Float[Array, ""]:
    """
    Compute predictive performance as function of data quality.
    """
    representativeness = _to_float_scalar(representativeness)
    performance = (
        baseline_performance + (max_performance - baseline_performance) * representativeness
    )
    return performance


@jit
def compute_selection_bias(
    participation_rate: Float[Array, ""] | float | int,
    high_risk_participation_ratio: float = 0.8,
) -> Float[Array, ""]:
    """
    Compute selection bias metric.
    """
    participation_rate = _to_float_scalar(participation_rate)
    bias = jnp.abs(1.0 - high_risk_participation_ratio)
    bias = bias * (1.0 - participation_rate)
    return bias


def compute_data_quality_externality(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> dict[str, Float[Array, ""]]:
    """
    Compute data quality externality of policy change.
    """
    participation_baseline = compute_participation_rate(params, baseline_policy)
    participation_reform = compute_participation_rate(params, reform_policy)

    representativeness_baseline = compute_representativeness(participation_baseline)
    representativeness_reform = compute_representativeness(participation_reform)

    performance_baseline = compute_predictive_performance(representativeness_baseline)
    performance_reform = compute_predictive_performance(representativeness_reform)

    bias_baseline = compute_selection_bias(participation_baseline)
    bias_reform = compute_selection_bias(participation_reform)

    return {
        "participation_baseline": participation_baseline,
        "participation_reform": participation_reform,
        "representativeness_baseline": representativeness_baseline,
        "representativeness_reform": representativeness_reform,
        "performance_baseline": performance_baseline,
        "performance_reform": performance_reform,
        "selection_bias_baseline": bias_baseline,
        "selection_bias_reform": bias_reform,
    }


@jit
def compute_research_value_loss(
    representativeness_baseline: Float[Array, ""] | float | int | None = None,
    representativeness_reform: Float[Array, ""] | float | int | None = None,
    *,
    performance_baseline: Float[Array, ""] | float | int | None = None,
    performance_reform: Float[Array, ""] | float | int | None = None,
    annual_research_value: float = 1e6,
    discount_rate: float = 0.03,
    time_horizon: int = 10,
) -> Float[Array, ""]:
    """
    Compute present value of research value loss using non-linear power.
    """
    if performance_baseline is not None and performance_reform is not None:
        baseline_metric = _to_float_scalar(performance_baseline)
        reform_metric = _to_float_scalar(performance_reform)
        metric_loss = jnp.maximum(baseline_metric - reform_metric, 0.0)
        annual_loss = metric_loss * annual_research_value
    else:
        if representativeness_baseline is None or representativeness_reform is None:
            raise ValueError(
                "Either representativeness_* or performance_* inputs must be provided."
            )
        power_baseline = compute_scientific_power(representativeness_baseline)
        power_reform = compute_scientific_power(representativeness_reform)
        power_loss = jnp.maximum(power_baseline - power_reform, 0.0)
        annual_loss = power_loss * annual_research_value

    if discount_rate > 0:
        pv_factor = (1 - (1 + discount_rate) ** (-time_horizon)) / discount_rate
    else:
        pv_factor = time_horizon

    present_value_loss = annual_loss * pv_factor
    return present_value_loss


def get_standard_participation_parameters() -> dict[str, float]:
    """
    Get standard parameters for participation model.
    """
    return {
        "base_participation": 0.5,
        "privacy_elasticity": -0.10,
        "social_benefit": 0.6,
        "annual_research_value": 1e6,
        "discount_rate": 0.03,
        "time_horizon": 10,
    }
