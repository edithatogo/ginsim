"""
Property-based tests for Welfare & DCBA logic.
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from src.model.dcba_ledger import compute_dcba


@settings(deadline=None)
@given(
    uptake=st.floats(min_value=0.0, max_value=1.0),
    premium=st.floats(min_value=0.0, max_value=1.0),
    profits=st.floats(min_value=-1.0, max_value=1.0),
    externality=st.floats(min_value=0.0, max_value=1e6),
)
def test_welfare_conservation_identity(uptake, premium, profits, externality):
    """
    Property: Net Welfare MUST equal the sum of its stakeholder components.
    Identity: Net = CS + PS + Health + Fiscal - Research
    """
    res = compute_dcba(
        testing_uptake=uptake,
        baseline_uptake=0.5,
        insurance_premium=premium,
        baseline_premium=0.5,
        insurer_profits=profits,
        baseline_profits=0.0,
        research_value_loss=externality,
        time_horizon=20,
    )

    # Sum components
    component_sum = (
        res.consumer_surplus
        + res.producer_surplus
        + res.health_benefits
        + res.fiscal_impact
        - res.research_externalities
    )

    # Should be exactly equal (ignoring distributional weight)
    assert float(res.net_welfare) == pytest.approx(float(component_sum), abs=1e-5)


@settings(deadline=None)
@given(weight=st.floats(min_value=0.1, max_value=5.0))
def test_distributional_weight_linearity(weight):
    """
    Property: Welfare should scale linearly with distributional weight.
    """
    res_base = compute_dcba(0.6, 0.5, 0.5, 0.5, 0.0, 0.0, distributional_weight=1.0)
    res_weighted = compute_dcba(0.6, 0.5, 0.5, 0.5, 0.0, 0.0, distributional_weight=weight)

    assert float(res_weighted.net_welfare) == pytest.approx(
        float(res_base.net_welfare * weight), abs=1e-5
    )
