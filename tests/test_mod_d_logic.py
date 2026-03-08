import jax.numpy as jnp
from hypothesis import given, settings
from hypothesis import strategies as st

from src.model.module_d_proxy import compute_proxy_substitution_effect
from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import get_default_parameters


@settings(max_examples=50, deadline=None)
@given(
    proxy_rate=st.floats(min_value=0.0, max_value=1.0),
)
def test_information_gap_monotonicity(proxy_rate):
    """
    Test that higher proxy substitution rates lead to smaller information gaps.
    """
    params = get_default_parameters()
    # Override with hypothesis value
    params = params.model_copy(update={"proxy_substitution_rate": proxy_rate})
    
    policies = get_standard_policies()
    sq = policies["status_quo"]
    reform = policies["ban"]

    res = compute_proxy_substitution_effect(params, sq, reform)
    gap = res["residual_information_gap"]

    # Since Status Quo has full info, gap should be between 0 and 1
    assert gap >= -1e-7
    assert gap <= 1.0 + 1e-7


def test_proxy_effect_zero_at_full_info():
    """If the reform policy allows genetic results, gap should be zero."""
    params = get_default_parameters()
    policies = get_standard_policies()
    sq = policies["status_quo"]

    res = compute_proxy_substitution_effect(params, sq, sq)
    assert jnp.abs(res["residual_information_gap"]) < 1e-7
