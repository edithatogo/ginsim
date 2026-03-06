import pytest

from streamlit_app.dashboard_helpers import (
    build_sandbox_policy,
    evaluate_sandbox_policy,
    format_positive_share,
)


def test_build_sandbox_policy_uses_core_policy_shape():
    policy = build_sandbox_policy(enforcement_strength=0.8, penalty_rate=0.6)

    assert policy.name == "sandbox_policy"
    assert policy.allow_genetic_test_results is False
    assert policy.allow_family_history is True
    assert policy.sum_insured_caps is not None
    assert policy.enforcement_strength == pytest.approx(0.8)
    assert policy.penalty_max == pytest.approx(600000.0)


def test_evaluate_sandbox_policy_runs_through_core_pipeline():
    result = evaluate_sandbox_policy(
        baseline_testing_uptake=0.52,
        deterrence_elasticity=0.12,
        enforcement_effectiveness=0.7,
        penalty_rate=0.6,
    )

    assert result.policy_name == "sandbox_policy"
    assert 0.0 <= float(result.testing_uptake) <= 1.0
    assert 0.0 <= float(result.compliance_rate) <= 1.0
    assert "welfare" in result.all_metrics


@pytest.mark.parametrize(
    ("positive_count", "total_count", "expected"),
    [
        (0, 0, "0%"),
        (0, 5, "0%"),
        (2, 4, "50%"),
        (3, 4, "75%"),
    ],
)
def test_format_positive_share_handles_zero_and_non_zero_totals(
    positive_count,
    total_count,
    expected,
):
    assert format_positive_share(positive_count, total_count) == expected
