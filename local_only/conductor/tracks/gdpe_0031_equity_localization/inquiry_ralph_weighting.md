# Inquiry: Mathematical Representation of Māori Health Sovereignty

**Track:** gdpe_0031_equity_localization
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How can we mathematically represent Treaty of Waitangi obligations (Aotearoa NZ) and socio-economic equity (AU) without over-simplifying Māori health sovereignty?

## 1. The Treaty Context (NZ)
In Aotearoa New Zealand, the **Te Tiriti o Waitangi** (Treaty of Waitangi) provides a mandate for equitable Māori health outcomes. 
- **Health Sovereignty:** Māori must have agency over their data and health journeys.
- **Equity Gap:** Māori face systemic barriers leading to lower genetic testing uptake and higher disease burden.

## 2. Mathematical Proposal: Distributional Weights
We can represent these obligations as **Distributional Weights** in the social welfare function.
Instead of a simple sum of welfare:
$$ W = \sum_{i} U_i $$
We move to:
$$ W = \sum_{g \in \text{Groups}} \omega_g \cdot \Delta Surplus_g $$

- **For NZ:** $\omega_{Maori} > 1.0$ represents the "Sovereignty Multiplier" required to reach equity targets.
- **For AU:** $\omega_{Q1} > 1.0$ (Bottom Quintile) represents the "Vertical Equity" priority for those most deterred by costs.

## 3. Implementation Plan for `dcba_ledger.py`
We need to refactor the `compute_dcba` function to:
1. Accept a `distributional_weight` parameter (float).
2. Calculate a "Standard Welfare" (Utilitarian) and an "Equity-Weighted Welfare" (Social Benefit).
3. Ensure the `equity_factor` is explicitly logged in the `PolicyEvaluationResult`.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "Should the weight be fixed or dynamic based on the uptake gap?"
- **Answer:** For this phase, we use a fixed jurisdictional weight anchored in the evidence register. In future tracks (Temporal Evolution), we could model "Trust Recovery" where weights decline as equity gaps close.
- **Action:** Add `equity_factor: float = 1.0` to `ModelParameters`.
