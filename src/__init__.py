"""
Genetic Discrimination Policy Economic Evaluation Model.

This package provides a modular Bayesian decision analysis model
for quantifying the economic and welfare impacts of policies
that restrict genetic discrimination in life insurance.
"""

# Package-wide runtime type checking with beartype
from beartype.claw import beartype_this_package

# Enable runtime type checking for entire package
beartype_this_package()

# Core imports
from .model.parameters import HyperParameters, ModelParameters, PolicyConfig
from .model.pipeline import (
    compare_policies,
    evaluate_policy_sweep,
    evaluate_single_policy,
    generate_policy_summary,
    run_full_evaluation,
)
from .model.rng import RNGManager, get_global_rng, reset_global_rng

__version__ = "0.2.0"
__author__ = "Dylan A. Mordaunt"
__all__ = [
    # Version
    "__version__",
    "__author__",
    # Parameters
    "ModelParameters",
    "PolicyConfig",
    "HyperParameters",
    # RNG
    "RNGManager",
    "get_global_rng",
    "reset_global_rng",
    # Pipeline
    "evaluate_single_policy",
    "evaluate_policy_sweep",
    "compare_policies",
    "generate_policy_summary",
    "run_full_evaluation",
]
