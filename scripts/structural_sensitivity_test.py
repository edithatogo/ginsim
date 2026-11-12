import sys
from pathlib import Path

import jax.numpy as jnp

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging

setup_logging(level="INFO")


def linear_deterrence(perceived_penalty, elasticity=0.18):
    """Original linear model."""
    return 1.0 - (elasticity * perceived_penalty)


def step_deterrence(perceived_penalty, threshold=0.3, base_deterrence=0.2):
    """Step-function model (Threshold effect)."""
    return jnp.where(perceived_penalty > threshold, 1.0 - base_deterrence, 1.0)


# Simulate range of perceived penalties
penalties = jnp.linspace(0, 1, 100)

# Calculate responses
linear_res = linear_deterrence(penalties)
step_res = step_deterrence(penalties)

# Compare outcomes for Canada GNDA (High penalty/protection) vs US GINA (No protection)
# Canada: perceived penalty is low (0.1) due to strong protection
# US: perceived penalty is high (0.8) due to no protection

results = {
    "Scenario": ["Canada (Low Penalty)", "USA (High Penalty)"],
    "Linear Result (Uptake Multiplier)": [
        float(linear_deterrence(0.1)),
        float(linear_deterrence(0.8)),
    ],
    "Step Result (Uptake Multiplier)": [float(step_deterrence(0.1)), float(step_deterrence(0.8))],
}

logger.info("Structural Sensitivity Results:")
logger.info("-" * 60)
for i in range(2):
    logger.info(f"{results['Scenario'][i]}:")
    logger.info(f"  Linear: {results['Linear Result (Uptake Multiplier)'][i]:.2f}")
    logger.info(f"  Step:   {results['Step Result (Uptake Multiplier)'][i]:.2f}")
logger.info("-" * 60)

# Finding: In the US scenario, the linear model predicts a 14.4% drop (0.18*0.8)
# but the step model predicts a 20% drop (fixed base deterrence).
# In Canada, the linear model predicts a small drop, while step predicts zero drop.
