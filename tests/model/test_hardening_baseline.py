import jax.numpy as jnp
import pytest

from src.model.module_d_proxy import (
    compute_family_history_accuracy,
    compute_risk_score,
    optimize_underwriting,
)
from src.model.module_d_proxy_substitution import compute_proxy_potential
from src.model.parameters import PolicyConfig, get_default_parameters


def test_compute_proxy_potential_coverage():
    # Covers src/model/module_d_proxy_substitution.py
    res = compute_proxy_potential(jnp.asarray(0.5), jnp.asarray(0.7))
    assert res == 0.7
    res = compute_proxy_potential(jnp.asarray(0.8), jnp.asarray(0.4))
    assert res == 0.8


def test_optimize_underwriting_coverage():
    # Covers src/model/module_d_proxy.py lines 44-66
    params = get_default_parameters()
    policy = PolicyConfig(name="test", description="Test policy", allow_genetic_test_results=True)
    training_data = {
        "features": jnp.array([[1.0, 0.5], [0.5, 1.0]]),
        "outcomes": jnp.array([0.8, 0.2]),
    }

    # Test with noise_level > 0 to cover line 54-55
    res = optimize_underwriting(params, policy, training_data, max_iterations=10, noise_level=0.1)
    assert "weights" in res
    assert "loss" in res
    assert res["accuracy"] <= 1.0


def test_compute_risk_score_branch_coverage():
    # Covers src/model/module_d_proxy.py line 82 (the continue branch)
    features = {"genetic_test_result": 1.0, "age": 0.5}
    weights = {"genetic_test_result": 0.8, "age": 0.2}

    # include_genetic=False should skip genetic_test_result
    score = compute_risk_score(features, weights, include_genetic=False)
    assert score == pytest.approx(0.1)  # 0.5 * 0.2


def test_compute_family_history_accuracy_error_path():
    # Covers src/model/module_d_proxy.py lines 216-217 (mutation is None)
    params = get_default_parameters()
    with pytest.raises(ValueError, match="mutation array is required"):
        compute_family_history_accuracy(params, 0.9, mutation=None)


def test_compute_family_history_accuracy_success_path():
    # Covers src/model/module_d_proxy.py lines 210-215
    params = get_default_parameters().model_copy(update={"family_history_sensitivity": 0.7})
    mutation = jnp.array([1, 0, 1])
    family_history = jnp.array([1, 1, 1])
    # match at index 0 and 2. 2/3 = 0.666...
    res = compute_family_history_accuracy(params, family_history, mutation=mutation)
    assert isinstance(res, dict)
    assert res["sensitivity"] == 0.7
    assert res["accuracy"] == pytest.approx(2 / 3)


def test_evaluate_multiple_policies_coverage():
    from src.model.module_a_behavior import (
        compute_perceived_penalty,
        evaluate_multiple_policies,
        get_standard_policies,
    )

    params = get_default_parameters()
    policies = list(get_standard_policies().values())

    # Test individual_characteristics branch in compute_testing_utility (via compute_testing_uptake)
    char = {"risk_aversion": 0.1}
    res = evaluate_multiple_policies(
        params, policies, n_individuals=10, individual_characteristics=char
    )
    assert len(res) == len(policies)
    for p in policies:
        assert p.name in res

    # Test the "else" branch in compute_perceived_penalty (restriction_strength = 1.0)
    # This happens when allow_genetic_test_results=False AND sum_insured_caps is None
    p_no_caps = PolicyConfig(
        name="no_caps",
        description="No caps",
        allow_genetic_test_results=False,
        sum_insured_caps=None,
    )
    penalty = compute_perceived_penalty(
        params.adverse_selection_elasticity,
        params.baseline_loading,
        p_no_caps.allow_genetic_test_results,
        p_no_caps.enforcement_strength,
        params.enforcement_effectiveness,
        params.moratorium_effect,
        p_no_caps.sum_insured_caps,
    )
    assert penalty >= 0
