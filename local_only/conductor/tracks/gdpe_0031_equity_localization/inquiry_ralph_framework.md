# Inquiry: Mathematical Representation of Māori Health Sovereignty & Treaty Obligations

**Track:** gdpe_0031_equity_localization
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How can we mathematically represent Treaty of Waitangi obligations without over-simplifying Māori health sovereignty?

## 1. The Philosophical Constraint
Māori health sovereignty (Tino Rangatiratanga) implies that outcomes for Māori should not merely be "weighted" in a Western utilitarian calculus, but rather evaluated against specific constitutional obligations of equity and partnership. A simple scalar multiplier (e.g., $W_{Māori} = 1.2 \times B_{Māori}$) risks being reductionist and tokenistic.

## 2. Mathematical Alternatives

### Option A: The "Gap-Closing" Weight
Define the weight as a dynamic function of the current disparity.
$$w_m = 1 + \alpha \cdot (Outcome_{non-Māori} - Outcome_{Māori})$$
- **Pros:** Directly targets inequity.
- **Cons:** Weight becomes zero if parity is reached, which may ignore ongoing sovereignty obligations.

### Option B: Lexicographic Priority (Rawlsian-Treaty Hybrid)
A policy is only considered "Socially Beneficial" if it first satisfies a non-negative impact constraint for Māori.
- **Pros:** Strongest protection of sovereignty.
- **Cons:** Hard to implement in a continuous JAX optimization environment (non-differentiable).

### Option C: The "Dual-Ledger" Approach (Consensus Recommendation)
Maintain two distinct welfare tallies in the DCBA ledger:
1. **Utilitarian Net Welfare ($W_U$):** The standard aggregate.
2. **Equity-Adjusted Welfare ($W_E$):** Where $W_E = \sum w_i \cdot B_i$.
   - For NZ: $w_{Māori}$ is anchored in the "Proportional Universalism" principle.
   - For AU: $w_{Quintile1}$ is anchored in "Vertical Equity."

## 3. Implementation Logic for JAX
We will implement Option C. The `DCBAResult` will be expanded to include `weighted_net_welfare`. The `distributional_weight` will move from a single scalar to a vector or a dictionary of weights applied during the summation in `dcba_ledger.py`.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "What if the user provides weights that lead to a market collapse?"
- **Answer:** We must link the Adversarial Red-Teaming (Track 0044) to the Equity weights to find the 'Fairness-Stability Frontier'.
- **Action:** Add a `weighted_welfare` field to `DCBAResult` and update `compute_dcba` to accept an `equity_factor` array.
