"""
Formal fixed-point diagnostics for the proof engine.
"""

from __future__ import annotations

import math

from src.model.module_a_behavior import get_standard_policies
from src.model.parameters import get_default_parameters
from src.model.proof_engine import summarize_proofs


def test_proof_bundle_has_expected_fields() -> None:
    params = get_default_parameters()
    policy = get_standard_policies()["moratorium"]

    proofs = summarize_proofs(params, policy)

    assert proofs["equilibrium_type"] in {"separating", "pooling"}
    assert math.isfinite(float(proofs["premium_stationarity"]))
    assert math.isfinite(float(proofs["premium_jacobian"]))
    assert math.isfinite(float(proofs["premium_hessian"]))
    assert math.isfinite(float(proofs["compliance_fixed_point_residual"]))


def test_compliance_fixed_point_residual_is_zero() -> None:
    params = get_default_parameters()
    policy = get_standard_policies()["ban"]

    proofs = summarize_proofs(params, policy)

    assert abs(float(proofs["compliance_fixed_point_residual"])) < 1e-8
