"""
Narrative Fairness Audit Logic.

Translates mathematical welfare outcomes into ethical/fairness categories.
"""

from __future__ import annotations


def audit_policy_fairness(
    uptake_delta: float,
    welfare_delta: float,
    premium_change: float,
) -> dict[str, str]:
    """
    Categorize a policy shift based on ethical frameworks.
    """
    verdict = "Neutral"
    rationale = "The policy maintains the status quo distribution of costs and benefits."

    # 1. Rawlsian Equity (Focus on high-risk/vulnerable)
    if uptake_delta > 0.05 and premium_change <= 0:
        verdict = "Rawlsian Equity"
        rationale = "Significantly increases participation for vulnerable groups without increasing financial barriers."

    # 2. Utilitarian Efficiency
    elif welfare_delta > 1000000:
        verdict = "Utilitarian Efficiency"
        rationale = "Maximizes total societal benefit, even if some individual costs increase."

    # 3. Precautionary Protection
    elif uptake_delta > 0 and premium_change > 0:
        verdict = "Precautionary Protection"
        rationale = (
            "Prioritizes information concealment and testing uptake over market pricing efficiency."
        )

    return {"ethical_category": verdict, "narrative_rationale": rationale}
