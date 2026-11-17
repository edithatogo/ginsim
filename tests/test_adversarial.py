from src.model.adversarial_engine import AdversarialEngine
from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import get_default_parameters


def test_adversarial_engine_optimization():
    """Verify that the adversarial engine can find a worst-case scenario."""
    params = get_default_parameters()
    policies = get_standard_policies()

    status_quo = policies["status_quo"]
    ban = policies["ban"]

    # Use small number of steps for fast test
    engine = AdversarialEngine(learning_rate=0.05, steps=20, n_individuals=100)
    result = engine.find_worst_case(ban, status_quo, params)

    assert result.success
    assert result.min_welfare_delta is not None
    assert len(result.loss_history) == 20
    assert "final_proportion_high" in result.worst_case_theta


def test_policy_comparison():
    """Verify the multi-policy comparison method."""
    params = get_default_parameters()
    policies = get_standard_policies()

    engine = AdversarialEngine(learning_rate=0.05, steps=5, n_individuals=50)
    # Only test a subset for speed
    test_policies = [policies["moratorium"], policies["ban"]]

    results = engine.run_policy_comparison(test_policies, policies["status_quo"], params)

    assert len(results) == 2
    assert "moratorium" in results
    assert "ban" in results
