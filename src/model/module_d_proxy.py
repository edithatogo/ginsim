"""
Module D: Proxy Substitution model.

Implements constrained optimization for underwriting when genetic information
is restricted.
"""

from __future__ import annotations

from dataclasses import dataclass

import jax
import jax.numpy as jnp
from jax import grad, jit, lax
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig


@dataclass(frozen=True)
class UnderwritingAccuracy:
    """Compatibility metrics for proxy underwriting tests."""

    auc: float
    sensitivity: float
    specificity: float
    mispricing_error: float


@jit(static_argnames=["params", "policy", "max_iterations"])
def optimize_underwriting(
    params: ModelParameters,
    policy: PolicyConfig,
    training_data: dict[str, Array],
    max_iterations: int = 100,
    noise_level: float = 0.0,
) -> dict[str, Float[Array, ""]]:
    """
    Optimize underwriting model under policy constraints.
    Uses jax.lax.scan for high-performance iteration.
    """
    features = training_data["features"]
    outcomes = training_data["outcomes"]

    if noise_level > 0:
        noise_matrix = jnp.ones_like(features) * noise_level
        features = features + noise_matrix

    n_features = features.shape[1]
    weights = jnp.ones(n_features) * 0.1
    lr = 0.01

    def loss_fn(w: Array) -> Float[Array, ""]:
        preds = jnp.dot(features, w)
        return jnp.mean((preds - outcomes) ** 2)

    def step_fn(w, _):
        g = grad(loss_fn)(w)
        w_new = w - lr * g
        return w_new, None

    # Use scan for efficient JIT-compatible looping
    final_weights, _ = lax.scan(step_fn, weights, None, length=max_iterations)
    final_loss = loss_fn(final_weights)

    return {
        "weights": final_weights,
        "loss": final_loss,
        "accuracy": 1.0 - final_loss,
    }


@jit
def compute_auc_loss(
    weights: Array,
    features: Array,
    outcomes: Array,
) -> Float[Array, ""]:
    """Compute predictive error."""
    preds = jnp.dot(features, weights)
    return jnp.mean((preds - outcomes) ** 2)


def compute_risk_score(
    features: dict[str, float],
    weights: dict[str, float],
    *,
    include_genetic: bool = True,
) -> float:
    """Compute risk score."""
    score = 0.0
    for feature_name, feature_value in features.items():
        if not include_genetic and feature_name == "genetic_test_result":
            continue
        score += feature_value * weights.get(feature_name, 0.0)
    return score


def compute_claim_probability(
    risk_score: float,
    *,
    intercept: float = 0.0,
) -> float:
    """Logistic link function."""
    return float(jax.nn.sigmoid(risk_score + intercept))


def compute_underwriting_accuracy(
    predicted: Array,
    actual: Array,
    *,
    threshold: float = 0.5,
) -> UnderwritingAccuracy:
    """Compute basic underwriting accuracy metrics."""
    predicted_positive = predicted >= threshold
    actual_positive = actual >= threshold

    true_positive = float(jnp.sum(predicted_positive & actual_positive))
    true_negative = float(jnp.sum((~predicted_positive) & (~actual_positive)))
    false_positive = float(jnp.sum(predicted_positive & (~actual_positive)))
    false_negative = float(jnp.sum((~predicted_positive) & actual_positive))

    sensitivity = true_positive / max(true_positive + false_negative, 1.0)
    specificity = true_negative / max(true_negative + false_positive, 1.0)
    mispricing_error = float(jnp.mean(jnp.abs(predicted - actual)))
    auc = 0.5 * (sensitivity + specificity)

    return UnderwritingAccuracy(
        auc=auc,
        sensitivity=sensitivity,
        specificity=specificity,
        mispricing_error=mispricing_error,
    )


def compute_proxy_substitution_effect(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> dict[str, float]:
    """
    Compute effect of proxy substitution and the resulting 'Information Gap'.
    """
    baseline_accuracy = 0.8

    if reform_policy.allow_genetic_test_results:
        reform_accuracy = baseline_accuracy
    else:
        proxy_capture = params.proxy_substitution_rate
        family_history_capture = (
            params.family_history_sensitivity * 0.35 if reform_policy.allow_family_history else 0.0
        )
        enforcement_drag = 1.0 - (0.35 * reform_policy.enforcement_strength)

        # SOTA logic: criminal penalties reduce reconstruction power more than civil
        criminal_drag = 0.85 if reform_policy.penalty_type == "criminal" else 1.0

        residual_capture = jnp.clip(
            (proxy_capture + family_history_capture) * enforcement_drag * criminal_drag,
            0.0,
            1.0,
        )
        reform_accuracy = float(baseline_accuracy * residual_capture)

    accuracy_loss = baseline_accuracy - reform_accuracy
    # The Information Gap measures how much genetic info remains concealed
    residual_information_gap = max(0.0, 1.0 - (reform_accuracy / (baseline_accuracy + 1e-10)))

    return {
        "accuracy_baseline": baseline_accuracy,
        "accuracy_reform": reform_accuracy,
        "accuracy_loss": accuracy_loss,
        "residual_information_gap": residual_information_gap,
    }


def compute_family_history_accuracy(
    sensitivity_or_params: Float[Array, ""] | ModelParameters,
    family_history_or_specificity: Array | float = 0.9,
    mutation: Array | None = None,
) -> Float[Array, ""] | dict[str, float]:
    """Compute family history accuracy score."""
    if isinstance(sensitivity_or_params, ModelParameters):
        params = sensitivity_or_params
        if mutation is None:
            raise ValueError("mutation array is required when passing ModelParameters")

        family_history = jnp.asarray(family_history_or_specificity)
        mutation_arr = jnp.asarray(mutation)
        matches = family_history == mutation_arr
        accuracy = float(jnp.mean(matches))
        return {
            "sensitivity": float(params.family_history_sensitivity),
            "accuracy": accuracy,
        }

    sensitivity = sensitivity_or_params
    specificity = float(family_history_or_specificity)
    return (sensitivity + specificity) / 2


def get_standard_proxy_features() -> list[str]:
    """Get list of standard proxy features."""
    return [
        "age",
        "sex",
        "smoking_status",
        "bmi",
        "family_history",
        "genetic_test_result",
        "medical_history",
        "occupation",
    ]


def get_standard_features() -> list[str]:
    """Backward-compatible alias."""
    return get_standard_proxy_features()
