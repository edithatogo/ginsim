import pytest

from src.model.parameters import load_jurisdiction_parameters
from src.model.pipeline import evaluate_single_policy, get_standard_policies


@pytest.mark.parametrize("jurisdiction", ["australia", "new_zealand", "uk", "canada", "us"])
def test_pipeline_execution_matrix(jurisdiction):
    """
    Verify that the full evaluation pipeline runs without errors for every jurisdiction.
    """
    params = load_jurisdiction_parameters(jurisdiction)
    policies = get_standard_policies()

    for name, policy in policies.items():
        result = evaluate_single_policy(params, policy)

        # Invariants (Cast to float for JAX compatibility)
        assert float(result.testing_uptake) >= 0.0
        assert float(result.testing_uptake) <= 1.0
        assert result.welfare_impact is not None
        assert float(result.compliance_rate) >= 0.0
        assert float(result.compliance_rate) <= 1.0


@pytest.mark.parametrize("jurisdiction", ["australia", "uk"])
def test_threshold_blending_impact(jurisdiction):
    """
    Verify that the threshold logic (blended equilibrium) is active for moratoriums.
    """
    params = load_jurisdiction_parameters(jurisdiction)
    policies = get_standard_policies()

    # Moratorium has thresholds
    moratorium = policies["moratorium"]
    res_moratorium = evaluate_single_policy(params, moratorium)

    # Status Quo has no thresholds
    sq = policies["status_quo"]
    _ = evaluate_single_policy(params, sq)

    # Check that premiums are populated and contain high/low
    assert "premium_high" in res_moratorium.insurance_premiums
    assert "premium_low" in res_moratorium.insurance_premiums

    # Premium high should be >= premium low
    ph = float(res_moratorium.insurance_premiums["premium_high"])
    pl = float(res_moratorium.insurance_premiums["premium_low"])
    assert ph >= pl
