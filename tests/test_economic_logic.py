import jax.numpy as jnp
from hypothesis import given, settings
from hypothesis import strategies as st

from src.model.module_c_insurance_eq import pooling_equilibrium, separating_equilibrium
from src.model.parameters import get_default_parameters


@settings(max_examples=50, deadline=None)
@given(prop_high=st.floats(min_value=0.01, max_value=0.99))
def test_insurer_zero_profit_identity(prop_high):
    """
    Fundamental Identity: In a competitive screening equilibrium with
    actuarially fair pricing, insurer profits must be zero.
    """
    params = get_default_parameters()

    eq_sep = separating_equilibrium(params, proportion_high=prop_high)
    assert jnp.abs(eq_sep.insurer_profits) < 1e-5

    eq_pool = pooling_equilibrium(params, proportion_high=prop_high)
    assert jnp.abs(eq_pool.insurer_profits) < 1e-3
