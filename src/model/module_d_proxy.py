"""
Module D: Proxy Substitution model.

Implements constrained optimization for underwriting when genetic information
is restricted.

Strategic Game: Constrained Optimization under Regulatory Constraints
- Players: Insurers (choosing underwriting weights), Regulator (constraints)
- Mechanism: Re-optimization using proxy variables
- Equilibrium: Optimal underwriting model given restricted information set
"""

from __future__ import annotations

from dataclasses import dataclass

import jax.numpy as jnp
import jax
from jax import grad, jit
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig


@dataclass(frozen=True)
class UnderwritingAccuracy:
    """Compatibility metrics for proxy underwriting tests."""

    auc: float
    sensitivity: float
    specificity: float
    mispricing_error: float


@jit
def optimize_underwriting(
    params: ModelParameters,
    policy: PolicyConfig,
    training_data: dict[str, Array],
    max_iterations: int = 100,
    noise_level: float = 0.0,
) -> dict[str, Float[Array, ""]]:
    """
    Optimize underwriting model under policy constraints.

    Args:
        params: Model parameters
        policy: Policy configuration
        training_data: Dictionary with 'features', 'outcomes'
        max_iterations: Maximum optimization iterations
        noise_level: Level of adversarial noise in proxy features (0-1)

    Returns:
        Dictionary with optimized weights and accuracy metrics
    """
    features = training_data["features"]
    outcomes = training_data["outcomes"]

    # Inject adversarial noise if level > 0 (AL_1.2.1)
    if noise_level > 0:
        noise_matrix = jnp.ones_like(features) * noise_level
        features = features + noise_matrix

    n_features = features.shape[1]

    # Initialize weights
    weights = jnp.ones(n_features) * 0.1

    # Loss function: negative log-likelihood (MSE proxy)
    def loss_fn(w: Array) -> Float[Array, ""]:
        preds = jnp.dot(features, w)
        return jnp.mean((preds - outcomes) ** 2)

    # Simple gradient descent
    lr = 0.01
    for _ in range(max_iterations):
        g = grad(loss_fn)(weights)
        weights = weights - lr * g

    final_loss = loss_fn(weights)

    return {
        "weights": weights,
        "loss": final_loss,
        "accuracy": 1.0 - final_loss,
    }


@jit
def compute_auc_loss(
    weights: Array,
    features: Array,
    outcomes: Array,
) -> Float[Array, ""]:
    """Compute AUC-like loss (predictive error)."""
    preds = jnp.dot(features, weights)
    return jnp.mean((preds - outcomes) ** 2)


def compute_risk_score(
    features: dict[str, float],
    weights: dict[str, float],
    *,
    include_genetic: bool = True,
) -> float:
    """Compute a simple linear risk score from named features."""
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
    """Map a scalar risk score to claim probability via logistic link."""
    return float(jax.nn.sigmoid(risk_score + intercept))


def compute_underwriting_accuracy(
    predicted: Array,
    actual: Array,
    *,
    threshold: float = 0.5,
) -> UnderwritingAccuracy:
    """Compute basic underwriting accuracy metrics for compatibility tests."""
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


def compute_equity_metrics(
    weights: Array,
    features: Array,
    outcomes: Array,
    n_quintiles: int = 5,
) -> dict[str, list[float]]:
    """
    Compute predictive loss broken down by equity quintiles.

    AL_1.4.2: SOTA Algorithmic Fairness requirement.
    """
    # Sort by outcome (risk level)
    idx = jnp.argsort(outcomes)
    features_sorted = features[idx]
    outcomes_sorted = outcomes[idx]

    # Split into quintiles
    chunk_size = len(outcomes) // n_quintiles
    quintile_losses = []

    for i in range(n_quintiles):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < n_quintiles - 1 else len(outcomes)

        q_feat = features_sorted[start:end]
        q_out = outcomes_sorted[start:end]

        loss = compute_auc_loss(weights, q_feat, q_out)
        quintile_losses.append(float(loss))

    return {
        "quintile_losses": quintile_losses,
        "max_disparity": max(quintile_losses) / (min(quintile_losses) + 1e-10),
    }


def compute_proxy_substitution_effect(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
) -> dict[str, float]:
    """Compute effect of proxy substitution."""
    baseline_accuracy = 0.8

    if reform_policy.allow_genetic_test_results:
        reform_accuracy = baseline_accuracy
    else:
        proxy_capture = params.proxy_substitution_rate
        family_history_capture = (
            params.family_history_sensitivity * 0.35 if reform_policy.allow_family_history else 0.0
        )
        enforcement_drag = 1.0 - (0.35 * reform_policy.enforcement_strength)
        criminal_drag = 0.85 if reform_policy.penalty_type == "criminal" else 1.0

        residual_capture = jnp.clip(
            (proxy_capture + family_history_capture) * enforcement_drag * criminal_drag,
            0.0,
            1.0,
        )
        reform_accuracy = float(baseline_accuracy * residual_capture)

    accuracy_loss = baseline_accuracy - reform_accuracy
    residual_information_gap = max(0.0, 1.0 - (reform_accuracy / baseline_accuracy))

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
    """Compute family history accuracy score or legacy test metrics."""
    if isinstance(sensitivity_or_params, ModelParameters):
        params = sensitivity_or_params
        if mutation is None:
            msg = "mutation array is required when passing ModelParameters"
            raise ValueError(msg)

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
    """Get list of standard proxy features used in underwriting."""
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
    """Backward-compatible alias for the proxy feature list."""
    return get_standard_proxy_features()
