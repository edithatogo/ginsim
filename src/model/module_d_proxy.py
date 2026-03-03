"""
Module D: Proxy Substitution model.

Implements constrained optimization for underwriting when genetic information
is restricted.

Strategic Game: Constrained Optimization under Regulatory Constraints
- Players: Insurers (constrained optimization), Applicants
- Mechanism: Insurer re-optimization using allowed proxies
- Equilibrium: New underwriting rules using correlated features
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import jax.numpy as jnp
from jax import jit, vmap, grad
from jaxtyping import Array, Float

from .parameters import ModelParameters, PolicyConfig


@dataclass
class UnderwritingAccuracy:
    """
    Underwriting accuracy metrics.
    
    Attributes:
        auc: Area under ROC curve
        sensitivity: True positive rate
        specificity: True negative rate
        mispricing_error: Mean absolute pricing error
    """
    auc: Float[Array, ""]
    sensitivity: Float[Array, ""]
    specificity: Float[Array, ""]
    mispricing_error: Float[Array, ""]


# Don't use @jit - has boolean conditional on traced value
def compute_risk_score(
    features: Dict[str, Float[Array, ""]],
    weights: Dict[str, Float[Array, ""]],
    include_genetic: bool = False,
) -> Float[Array, ""]:
    """
    Compute risk score from features.
    
    Risk score = sum(feature_i * weight_i)
    
    Args:
        features: Dictionary of feature values
        weights: Dictionary of feature weights
        include_genetic: Whether to include genetic test results
        
    Returns:
        Risk score
    """
    risk_score = jnp.zeros(())
    
    for feature_name, feature_value in features.items():
        # Skip genetic features if not allowed
        if 'genetic' in feature_name.lower() and not include_genetic:
            continue
        
        if feature_name in weights:
            risk_score = risk_score + feature_value * weights[feature_name]
    
    return risk_score


@jit
def sigmoid(x: Float[Array, ""]) -> Float[Array, ""]:
    """Sigmoid activation function."""
    return 1.0 / (1.0 + jnp.exp(-x))


@jit
def compute_claim_probability(
    risk_score: Float[Array, ""],
    intercept: float = -2.0,
    slope: float = 1.0,
) -> Float[Array, ""]:
    """
    Compute claim probability from risk score (logistic model).
    
    P(claim) = sigmoid(intercept + slope * risk_score)
    
    Args:
        risk_score: Risk score from features
        intercept: Model intercept
        slope: Model slope
        
    Returns:
        Claim probability
    """
    linear_predictor = intercept + slope * risk_score
    return sigmoid(linear_predictor)


@jit
def compute_underwriting_accuracy(
    predicted_probabilities: Float[Array, "n"],
    actual_outcomes: Float[Array, "n"],
    threshold: float = 0.5,
) -> UnderwritingAccuracy:
    """
    Compute underwriting accuracy metrics.
    
    Args:
        predicted_probabilities: Predicted claim probabilities
        actual_outcomes: Actual claim outcomes (0 or 1)
        threshold: Classification threshold
        
    Returns:
        UnderwritingAccuracy object
    """
    # Binary predictions
    predictions = (predicted_probabilities > threshold).astype(jnp.float32)
    
    # Confusion matrix elements
    true_positives = jnp.sum((predictions == 1) & (actual_outcomes == 1))
    true_negatives = jnp.sum((predictions == 0) & (actual_outcomes == 0))
    false_positives = jnp.sum((predictions == 1) & (actual_outcomes == 0))
    false_negatives = jnp.sum((predictions == 0) & (actual_outcomes == 1))
    
    # Metrics
    sensitivity = true_positives / (true_positives + false_negatives + 1e-10)
    specificity = true_negatives / (true_negatives + false_positives + 1e-10)
    
    # Mispricing error (mean absolute error)
    mispricing_error = jnp.mean(jnp.abs(predicted_probabilities - actual_outcomes))
    
    # AUC approximation (using trapezoidal rule)
    # Simplified: use sensitivity at different thresholds
    thresholds = jnp.linspace(0, 1, 100)
    
    def compute_tpr_fpr(thresh):
        preds = (predicted_probabilities > thresh).astype(jnp.float32)
        tp = jnp.sum((preds == 1) & (actual_outcomes == 1))
        fp = jnp.sum((preds == 1) & (actual_outcomes == 0))
        tpr = tp / (tp + jnp.sum(actual_outcomes == 0) + 1e-10)
        fpr = fp / (fp + jnp.sum(actual_outcomes == 1) + 1e-10)
        return tpr, fpr
    
    tpr_values, fpr_values = vmap(compute_tpr_fpr)(thresholds)
    
    # AUC via trapezoidal integration (jnp.trapz deprecated, use manual)
    auc = 0.0
    for i in range(len(fpr_values) - 1):
        auc += 0.5 * (fpr_values[i + 1] - fpr_values[i]) * (tpr_values[i + 1] + tpr_values[i])
    
    return UnderwritingAccuracy(
        auc=auc,
        sensitivity=sensitivity,
        specificity=specificity,
        mispricing_error=mispricing_error,
    )


@jit
def optimize_underwriting(
    params: ModelParameters,
    policy: PolicyConfig,
    training_data: Dict[str, Array],
    max_iterations: int = 100,
) -> Dict[str, Float[Array, ""]]:
    """
    Optimize underwriting model under policy constraints.
    
    When genetic information is restricted, insurer re-optimizes
    using allowed proxies (family history, demographics, etc.).
    
    Uses gradient descent to find optimal weights.
    
    Args:
        params: Model parameters
        policy: Policy configuration
        training_data: Dictionary with 'features', 'outcomes'
        max_iterations: Maximum optimization iterations
        
    Returns:
        Dictionary with optimized weights and accuracy metrics
    """
    features = training_data['features']
    outcomes = training_data['outcomes']
    n_features = features.shape[1]
    
    # Initialize weights
    weights = jnp.ones(n_features) * 0.1
    
    # Loss function: negative log-likelihood
    def loss_fn(w):
        risk_scores = jnp.dot(features, w)
        probabilities = compute_claim_probability(risk_scores)
        
        # Binary cross-entropy loss
        epsilon = 1e-10
        loss = -jnp.mean(
            outcomes * jnp.log(probabilities + epsilon) +
            (1 - outcomes) * jnp.log(1 - probabilities + epsilon)
        )
        
        return loss
    
    # Gradient descent
    learning_rate = 0.01
    
    def step(carry):
        weights, i = carry
        
        # Compute gradient
        grad_loss = grad(loss_fn)(weights)
        
        # Update weights
        new_weights = weights - learning_rate * grad_loss
        
        return (new_weights, i + 1), jnp.linalg.norm(grad_loss) < 1e-6
    
    # Initialize
    init_carry = (weights, 0)
    
    # Optimize
    (optimized_weights, n_iter), converged = lax.while_loop(
        lambda carry_converged: (carry_converged[0][1] < max_iterations) & (~carry_converged[1]),
        step,
        (init_carry, False)
    )
    
    # Compute predictions with optimized weights
    risk_scores = jnp.dot(features, optimized_weights)
    probabilities = compute_claim_probability(risk_scores)
    
    # Compute accuracy
    accuracy = compute_underwriting_accuracy(probabilities, outcomes)
    
    return {
        'weights': optimized_weights,
        'converged': converged,
        'iterations': n_iter,
        'auc': accuracy.auc,
        'mispricing_error': accuracy.mispricing_error,
    }


@jit
def compute_proxy_substitution_effect(
    params: ModelParameters,
    baseline_policy: PolicyConfig,
    reform_policy: PolicyConfig,
    training_data_with_genetic: Dict[str, Array],
    training_data_without_genetic: Dict[str, Array],
) -> Dict[str, Float[Array, ""]]:
    """
    Compute effect of proxy substitution.
    
    When genetic information is banned, insurers substitute
    with correlated proxies (family history, etc.).
    
    Args:
        params: Model parameters
        baseline_policy: Baseline policy (with genetic info)
        reform_policy: Reform policy (without genetic info)
        training_data_with_genetic: Training data including genetic features
        training_data_without_genetic: Training data excluding genetic features
        
    Returns:
        Dictionary with substitution effect metrics
    """
    # Optimize with genetic information
    result_with_genetic = optimize_underwriting(
        params,
        baseline_policy,
        training_data_with_genetic,
    )
    
    # Optimize without genetic information (proxy substitution)
    result_without_genetic = optimize_underwriting(
        params,
        reform_policy,
        training_data_without_genetic,
    )
    
    # Compute substitution effect
    auc_loss = result_with_genetic['auc'] - result_without_genetic['auc']
    error_increase = result_without_genetic['mispricing_error'] - result_with_genetic['mispricing_error']
    
    # Proxy substitution rate (from parameters)
    proxy_substitution_rate = params.proxy_substitution_rate
    
    return {
        'auc_with_genetic': result_with_genetic['auc'],
        'auc_without_genetic': result_without_genetic['auc'],
        'auc_loss': auc_loss,
        'error_with_genetic': result_with_genetic['mispricing_error'],
        'error_without_genetic': result_without_genetic['mispricing_error'],
        'error_increase': error_increase,
        'proxy_substitution_rate': proxy_substitution_rate,
    }


# Don't use @jit - uses pydantic models
def compute_family_history_accuracy(
    params: ModelParameters,
    family_history_positive: Float[Array, "n"],
    mutation_status: Float[Array, "n"],
) -> Dict[str, Float[Array, ""]]:
    """
    Compute accuracy of family history as proxy for mutation status.
    
    Args:
        params: Model parameters
        family_history_positive: Whether family history is positive
        mutation_status: Actual mutation status (0 or 1)
        
    Returns:
        Dictionary with accuracy metrics
    """
    # Sensitivity (from parameters)
    sensitivity = params.family_history_sensitivity
    
    # Specificity (complement of false positive rate)
    # Assume specificity is similar to sensitivity for simplicity
    specificity = sensitivity
    
    # Predictions based on family history
    predictions = family_history_positive.astype(jnp.float32)
    
    # Accuracy metrics
    true_positives = jnp.sum((predictions == 1) & (mutation_status == 1))
    true_negatives = jnp.sum((predictions == 0) & (mutation_status == 0))
    total_positives = jnp.sum(mutation_status == 1)
    total_negatives = jnp.sum(mutation_status == 0)
    
    empirical_sensitivity = true_positives / (total_positives + 1e-10)
    empirical_specificity = true_negatives / (total_negatives + 1e-10)
    
    # Overall accuracy
    accuracy = (true_positives + true_negatives) / (len(mutation_status) + 1e-10)
    
    return {
        'sensitivity': sensitivity,
        'specificity': specificity,
        'empirical_sensitivity': empirical_sensitivity,
        'empirical_specificity': empirical_specificity,
        'accuracy': accuracy,
    }


# Convenience function
def get_standard_features() -> List[str]:
    """
    Get standard underwriting feature names.
    
    Returns:
        List of feature names
    """
    return [
        'age',
        'sex',
        'smoking_status',
        'bmi',
        'family_history',
        'genetic_test_result',  # May be restricted by policy
        'medical_history',
        'occupation',
    ]
