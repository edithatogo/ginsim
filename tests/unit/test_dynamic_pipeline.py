import jax.numpy as jnp

from src.model.parameters import get_default_parameters
from src.model.pipeline import get_standard_policies, simulate_evolution


def test_evolution_completes():
    """Verify that temporal evolution runs for the specified horizon."""
    params = get_default_parameters()
    # Shorter horizon for test
    params = params.model_copy(update={"time_horizon": 3})

    policy = get_standard_policies()["ban"]

    # Run evolution
    results_dict = simulate_evolution(params, policy)
    results = results_dict["annual"]

    # Should have results for years 0, 1, 2, 3
    assert len(results) == 4
    assert 0 in results
    assert 3 in results

    # Uptake should generally change (increase due to falling costs)
    assert results[3].testing_uptake != results[0].testing_uptake


def test_temporal_aggregation():
    """Verify that aggregate welfare is the sum of annual discounted welfare."""
    params = get_default_parameters()
    params = params.model_copy(update={"time_horizon": 2})
    policy = get_standard_policies()["status_quo"]

    results_dict = simulate_evolution(params, policy)
    aggregate = results_dict["aggregate"]
    annual = results_dict["annual"]

    expected_welfare = sum(res.welfare_impact for res in annual.values())
    assert jnp.isclose(aggregate.welfare_impact, expected_welfare)
