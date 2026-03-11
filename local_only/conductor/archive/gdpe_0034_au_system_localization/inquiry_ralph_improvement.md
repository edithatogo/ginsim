# Inquiry: Commonwealth Budget Impact Visualization

**Track:** gdpe_0034_au_system_localization
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we add a visualization for the 'Commonwealth Budget Impact' specifically for Medicare testing rebates?

## 1. The Fiscal Transparency Rationale
The Commonwealth Treasury persona requested a clear view of how Medicare funding shifts costs from individuals to the government. 
- **Current View:** The DCBA Ledger has a single "Fiscal Impact" bar. 
- **Improvement:** Splitting "Fiscal Impact" into "Direct Testing Costs (Medicare)" and "Downstream Health Savings" would provide a much clearer ROI story for Australian policymakers.

## 2. Mathematical Impact
This would require expanding the `DCBAResult` object further or providing a more granular dictionary in `PolicyEvaluationResult.all_metrics`.
- **New Metric:** `medicare_outlay = testing_uptake * cost_per_test * medicare_cost_share`.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is there a simpler way to do this without changing the core DCBA schema again?"
- **Answer:** We can implement a "Fiscal Drill-Down" chart in the dashboard that simply unpacks the existing `fiscal_impact` using the `medicare_cost_share` parameter as a multiplier.
- **Action:** This should be implemented in **Track `gdpe_0037_viz_audit_e2e`**. I will add a requirement to that track to ensure the Fiscal Impact is decomposed visually for AU/NZ runs.
