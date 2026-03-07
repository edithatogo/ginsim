"""
Glue code for policy evaluation.

Coordinates between the high-level pipeline and specific module logic.
"""

from __future__ import annotations

from typing import Any

from . import (
    module_a_behavior as mod_a,
)
from . import (
    module_c_insurance_eq as mod_c,
)
from . import (
    module_f_data_quality as mod_f,
)
from .parameters import ModelParameters, PolicyConfig

# Type aliases for internal use
InsuranceParams = ModelParameters
DataQualityParams = ModelParameters


def run_simple_evaluation(
    params: ModelParameters,
    policy: PolicyConfig,
) -> dict[str, Any]:
    """
    Run a simplified evaluation for quick feedback loops.
    """
    # 1. Behavior
    uptake = mod_a.compute_testing_uptake(params, policy)

    # 2. Market
    market_eq = mod_c.compute_equilibrium(params, policy)

    # 3. Data Quality
    dq = mod_f.compute_data_quality_externality(params, policy)

    return {
        "uptake": float(uptake),
        "premium_high": float(market_eq.premium_high),
        "premium_low": float(market_eq.premium_low),
        "participation_rate": float(dq.participation_rate),
        "net_profit": float(market_eq.insurer_profits),
    }
