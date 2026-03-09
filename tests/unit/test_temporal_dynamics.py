from src.model.module_a_behavior import compute_testing_uptake, get_standard_policies
from src.model.module_d_proxy import compute_proxy_substitution_effect
from src.model.parameters import get_default_parameters


def test_temporal_proxy_improvement():
    """Verify that proxy substitution improves over time."""
    params = get_default_parameters()
    # Mocking tech improvement rate
    params = params.model_copy(update={"tech_improvement_rate": 0.15})

    policies = get_standard_policies()
    baseline = policies["status_quo"]
    reform = policies["ban"]

    # Year 0 effect
    effect_y0 = compute_proxy_substitution_effect(params, baseline, reform, year=0)
    # Year 10 effect
    effect_y10 = compute_proxy_substitution_effect(params, baseline, reform, year=10)

    # Informational redundancy should be higher in year 10
    assert effect_y10["informational_redundancy"] > effect_y0["informational_redundancy"]
    # Accuracy should be higher in year 10
    assert effect_y10["accuracy_reform"] > effect_y0["accuracy_reform"]
    # Information gap should be lower in year 10
    assert effect_y10["residual_information_gap"] < effect_y0["residual_information_gap"]


def test_temporal_cost_reduction():
    """Verify that testing uptake increases over time as costs drop."""
    params = get_default_parameters()
    # Use standard tech improvement rate
    params = params.model_copy(update={"tech_improvement_rate": 0.15})

    policies = get_standard_policies()
    policy = policies["status_quo"]

    # Year 0 uptake
    uptake_y0 = compute_testing_uptake(params, policy, year=0)
    # Year 10 uptake
    uptake_y10 = compute_testing_uptake(params, policy, year=10)

    # Uptake should be higher in year 10 because costs are lower (15% drop/year)
    assert uptake_y10 > uptake_y0
