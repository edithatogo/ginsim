import jax.numpy as jnp

from src.model.module_a_behavior import compute_perceived_penalty, compute_testing_utility
from src.model.parameters import load_jurisdiction_parameters


def test_medicare_toggle_impact():
    """Verify that medicare_cost_share reduces testing costs."""
    # Base utility with no medicare support
    u_no_medicare = compute_testing_utility(
        benefits=1.0, perceived_penalty=0.1, medicare_cost_share=0.0
    )

    # Utility with full medicare support
    u_full_medicare = compute_testing_utility(
        benefits=1.0, perceived_penalty=0.1, medicare_cost_share=1.0
    )

    # Full medicare should have higher utility (zero cost)
    assert u_full_medicare > u_no_medicare
    # Cost with 1.0 medicare should be 0, so utility = benefits - penalty
    assert jnp.isclose(u_full_medicare, 0.9)


def test_audit_intensity_impact():
    """Verify that audit_intensity (ASIC/APRA) increases perceived penalty reduction (lower perceived penalty)."""
    # Low audit intensity
    penalty_low = compute_perceived_penalty(
        adverse_selection_elasticity=0.1,
        baseline_loading=0.2,
        allow_genetic_test_results=False,
        enforcement_strength=1.0,
        enforcement_effectiveness=0.1,
        moratorium_effect=0.0,
        audit_intensity=0.1,
        audit_intensity_apra=0.1,
        audit_intensity_asic=0.1,
    )

    # High audit intensity
    penalty_high = compute_perceived_penalty(
        adverse_selection_elasticity=0.1,
        baseline_loading=0.2,
        allow_genetic_test_results=False,
        enforcement_strength=1.0,
        enforcement_effectiveness=0.1,
        moratorium_effect=0.0,
        audit_intensity=0.1,
        audit_intensity_apra=0.9,
        audit_intensity_asic=0.9,
    )

    # High audit intensity should result in a LOWER perceived penalty
    assert penalty_high < penalty_low


def test_australia_parameter_loading():
    """Verify that Australia parameters load correctly with new fields."""
    params = load_jurisdiction_parameters("australia")
    assert params.jurisdiction == "australia"
    assert hasattr(params, "medicare_cost_share")
    assert hasattr(params, "audit_intensity_apra")
    assert hasattr(params, "audit_intensity_asic")
    assert params.medicare_cost_share == 0.75
