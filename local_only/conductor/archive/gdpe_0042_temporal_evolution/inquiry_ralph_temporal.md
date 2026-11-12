# Inquiry: 10-Year Temporal State Transitions

**Track:** gdpe_0042_temporal_evolution
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How do we structure the 10-year state-transition matrix to capture cumulative market drift?

## 1. The Dynamic State Vector
Currently, we evaluate "Single Equilibrium" points. To model evolution, we need a state vector $S_t$:
$$ S_t = [\text{Uptake}_t, \text{Premium}_t, \text{Compliance}_t, \text{Trust}_t, \text{Inflation}_t] $$

## 2. Transition Drivers

### Technological Drift (Module A/D)
- **Genetic Literacy Growth:** $\epsilon_{deterrence}$ likely declines as genetic testing becomes normalized.
- **Proxy Accuracy Growth:** $\delta_{redundancy}$ increases due to AI/ML underwriting improvements (from Track 0035 inquiry).

### Economic Drift (Module C/DCBA)
- **Sum-Insured Inflation:** Effective regulatory caps decline in real value unless indexed (from Track 0032 inquiry).
- **Cumulative Adverse Selection:** If high-risk individuals consistently enter the market at year $t$, the premium at $t+1$ must rise to restore actuarial fairness.

## 3. Implementation Action
1. **Create `src/model/temporal_engine.py`:** Implement a `simulate_evolution(initial_params, n_years=10)` function.
2. **The Temporal Loop:** Use `jax.lax.scan` to iterate through 10 years efficiently while maintaining differentiability.
3. **State Persistence:** The "Market Premium" from year $t$ becomes the "Baseline Premium" for year $t+1$.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "How do we handle policy changes mid-horizon?"
- **Answer:** We should allow a `reform_year` parameter. The transition logic switches from `PolicyConfig_A` to `PolicyConfig_B` at that time step.
- **Action:** Add `PolicySchedule` to the parameter schema.
