"""
Fairness and distributional equity analysis module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FairnessResult:
    """Metrics for policy fairness audit."""

    is_fair: bool
    score: float
    verdict: str
    reasons: list[str]


def audit_policy_fairness(
    uptake_delta: Any,
    welfare_delta: Any,
    premium_delta: Any,
) -> FairnessResult:
    """
    Audit a policy reform for distributional fairness.
    Uses Any to allow JAX tracers.
    """
    reasons = []

    # 1. Equity of Access (Uptake)
    # If uptake increases, it's generally fairer (less deterrence)
    u_fair = float(uptake_delta) >= -0.01
    if not u_fair:
        reasons.append("Significant decrease in testing uptake suggests increased deterrents.")

    # 2. Economic Efficiency (Welfare)
    w_fair = float(welfare_delta) >= 0.0
    if not w_fair:
        reasons.append("Net social welfare loss detected.")

    # 3. Consumer Protection (Premiums)
    p_fair = float(premium_delta) <= 0.05
    if not p_fair:
        reasons.append("Excessive premium loading for high-risk individuals.")

    # Aggregate
    is_fair = u_fair and w_fair and p_fair
    score = (float(u_fair) + float(w_fair) + float(p_fair)) / 3.0

    if is_fair:
        verdict = "FAIR: Policy enhances or maintains social equity."
    elif score >= 0.6:
        verdict = "MARGINAL: Policy has trade-offs but overall acceptable."
    else:
        verdict = "UNFAIR: Policy introduces significant inequities."

    return FairnessResult(is_fair=is_fair, score=score, verdict=verdict, reasons=reasons)
