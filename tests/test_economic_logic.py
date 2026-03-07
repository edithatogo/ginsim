import jax.numpy as jnp
from hypothesis import given, settings
from hypothesis import strategies as st

from src.model.module_c_insurance_eq import pooling_equilibrium, separating_equilibrium
from src.model.parameters import ModelParameters


@settings(deadline=None)
@given(
    loading=st.floats(min_value=0.0, max_value=0.5),
    demand_elasticity=st.floats(min_value=-1.0, max_value=-0.01),
    prop_high=st.floats(min_value=0.01, max_value=0.99),
)
def test_insurer_zero_profit_identity(loading, demand_elasticity, prop_high):
    """
    Property: In a competitive equilibrium, insurer expected profits must be approximately zero.
    """
    params = ModelParameters(
        baseline_loading=loading,
        demand_elasticity_high_risk=demand_elasticity,
        deterrence_elasticity=0.1,
        moratorium_effect=0.1,
        adverse_selection_elasticity=0.1,
        pass_through_rate=0.7,
        research_participation_elasticity=-0.1,
        enforcement_effectiveness=0.5,
        complaint_rate=0.01,
        baseline_testing_uptake=0.5,
        family_history_sensitivity=0.7,
        proxy_substitution_rate=0.4,
    )

    eq_sep = separating_equilibrium(params, proportion_high=prop_high)
    assert jnp.abs(eq_sep.insurer_profits) < 1e-5

    eq_pool = pooling_equilibrium(params, proportion_high=prop_high)
    assert jnp.abs(eq_pool.insurer_profits) < 1e-3
