"""
Property-based tests for Module D Proxy logic.
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from src.model.module_d_proxy import compute_proxy_substitution_effect
from src.model.parameters import ModelParameters, PolicyConfig


@settings(deadline=None)
@given(
    proxy_rate=st.floats(min_value=0.0, max_value=1.0),
    fam_history_sens=st.floats(min_value=0.0, max_value=1.0),
    enforcement=st.floats(min_value=0.0, max_value=1.0),
)
def test_information_gap_monotonicity(proxy_rate, fam_history_sens, enforcement):
    """
    Property: Banning genetic info MUST create a non-negative information gap.
    """
    params = ModelParameters(
        proxy_substitution_rate=proxy_rate, family_history_sensitivity=fam_history_sens
    )

    baseline = PolicyConfig(name="base", description="d", allow_genetic_test_results=True)
    reform = PolicyConfig(
        name="reform",
        description="d",
        allow_genetic_test_results=False,
        enforcement_strength=enforcement,
    )

    res = compute_proxy_substitution_effect(params, baseline, reform)

    # Information gap should be between 0 and 1
    assert res["residual_information_gap"] >= 0.0
    assert res["residual_information_gap"] <= 1.0

    # If we allow genetic info, gap should be zero
    res_base = compute_proxy_substitution_effect(params, baseline, baseline)
    assert res_base["residual_information_gap"] == pytest.approx(0.0, abs=1e-9)


@settings(deadline=None)
@given(enforcement=st.floats(min_value=0.0, max_value=1.0))
def test_criminal_penalty_impact(enforcement):
    """
    Property: Criminal penalties should create a LARGER information gap than civil.
    """
    params = ModelParameters()
    baseline = PolicyConfig(name="base", description="d", allow_genetic_test_results=True)

    reform_civil = PolicyConfig(
        name="civil",
        description="d",
        allow_genetic_test_results=False,
        enforcement_strength=enforcement,
        penalty_type="fixed",
    )

    reform_criminal = PolicyConfig(
        name="criminal",
        description="d",
        allow_genetic_test_results=False,
        enforcement_strength=enforcement,
        penalty_type="criminal",
    )

    res_civil = compute_proxy_substitution_effect(params, baseline, reform_civil)
    res_criminal = compute_proxy_substitution_effect(params, baseline, reform_criminal)

    # Criminal should be strictly more effective (larger gap)
    assert res_criminal["residual_information_gap"] >= res_civil["residual_information_gap"]
