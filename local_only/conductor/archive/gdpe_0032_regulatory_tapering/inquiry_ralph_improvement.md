# Inquiry: Temporal Scaling of Regulatory Thresholds

**Track:** gdpe_0032_regulatory_tapering
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Could tapering be used to model 'Sum-Insured Inflation' over time?

## 1. The Dynamic Threshold Hypothesis
Currently, we model static thresholds (e.g., $500k). However, the real economic value of these thresholds declines due to inflation. If the cap is not indexed, more people effectively fall into the "unprotected" zone over time.

## 2. Tapering as a Dynamic Model
The `taper_function(x, cap, range)` we implemented can easily support temporal scaling:
$$ \text{Cap}(t) = \text{Cap}_0 \cdot (1 + \pi)^{-t} $$
where $\pi$ is the inflation rate.

- **Interaction:** By widening the `taper_range` as $t$ increases, we can model the "Regulatory Friction" where the transition between protected and unprotected states becomes noisier as the real value of the cap drifts.

## 3. Implementation for Future Tracks
This logic should be integrated into **Track `gdpe_0042_temporal_evolution`**.
- We can define a `ThresholdScaler` class that updates the `PolicyConfig` thresholds for each time step in the 10-year horizon.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is there a simpler way to surface this in the dashboard now?"
- **Answer:** We could add an "Inflation Indexing" toggle. If disabled, the model automatically shifts the effective cap leftward.
- **Action:** I will not implement this now to avoid scope creep, but I will document it as a high-priority follow-on for the Temporal Evolution track.
