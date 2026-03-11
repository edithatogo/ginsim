# Inquiry: Spatial Interactions & 'Diagnostic Deserts'

**Track:** gdpe_0036_spatial_equity
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Does a statutory ban close the testing gap in rural areas, or does geographic distance remain the dominant deterrent regardless of insurance policy?

## 1. The Multi-Factor Deterrence Model
Currently, our model assumes testing uptake is a function of:
$$ \text{Uptake} = \sigma(\text{Clinical Benefit} - \text{Insurance Penalty} - \text{Test Cost}) $$

In rural areas, "Test Cost" includes significant travel and time costs (The "Diagnostic Desert" effect).
- **Hypothesis:** For a rural individual, the "Test Cost" is so high that even if the "Insurance Penalty" is reduced to zero by a statutory ban, the uptake will remain lower than urban baselines. 

## 2. Spatial Parameters
We need to introduce a `remoteness_index` (0.0 to 1.0) where:
- **0.0:** Urban (Tertiary Hospital adjacent).
- **1.0:** Remote (Long-distance travel required).

$$ \text{Effective Test Cost} = \text{Cost}_{base} \cdot (1 + \beta \cdot \text{remoteness_index}) $$

## 3. Implementation Action
1. **Update `ModelParameters`:** Add `remoteness_weight: float`.
2. **Refactor Module A:** In `compute_testing_utility`, add the `remoteness_index` interaction.
3. **Pipeline Refinement:** Allow the pipeline to run a "Spatial Sweep" where it iterates across different remoteness levels to generate a geographic profile.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "How do we visualize this without real GIS data?"
- **Answer:** We can create a **"Synthetic Geography"** visualization—a scatter plot of Uptake vs. Remoteness—to show the "Equity Decay" curve.
- **Action:** Add a "Remoteness Impact" chart to the new "Spatial Equity" tab.
