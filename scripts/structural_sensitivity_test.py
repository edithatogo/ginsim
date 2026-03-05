import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as np

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
    "Linear Result (Uptake Multiplier)": [float(linear_deterrence(0.1)), float(linear_deterrence(0.8))],
    "Step Result (Uptake Multiplier)": [float(step_deterrence(0.1)), float(step_deterrence(0.8))]
}

print("Structural Sensitivity Results:")
print("-" * 60)
for i in range(2):
    print(f"{results['Scenario'][i]}:")
    print(f"  Linear: {results['Linear Result (Uptake Multiplier)'][i]:.2f}")
    print(f"  Step:   {results['Step Result (Uptake Multiplier)'][i]:.2f}")
print("-" * 60)

# Finding: In the US scenario, the linear model predicts a 14.4% drop (0.18*0.8)
# but the step model predicts a 20% drop (fixed base deterrence).
# In Canada, the linear model predicts a small drop, while step predicts zero drop.
