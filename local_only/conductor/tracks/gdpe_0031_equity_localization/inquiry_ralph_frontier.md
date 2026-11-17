# Inquiry: The 'Fairness Frontier' Visualization

**Track:** gdpe_0031_equity_localization
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we implement a 'Fairness Frontier' visualization to complement the Global Efficiency Frontier?

## 1. The Concept
Currently, the "Global Efficiency Frontier" plots Testing Uptake vs. Utilitarian Welfare. A **Fairness Frontier** would plot:
- **X-Axis:** Utilitarian Social Welfare (Standard).
- **Y-Axis:** Equity-Weighted Social Welfare (Localized).

## 2. Decision Logic
Policies that fall on the upper-left are "Equity-Dominant" (better for protected groups but potentially less efficient overall). Policies on the lower-right are "Efficiency-Dominant."
- **Visual Impact:** A 45-degree line represents "Perfect Neutrality" (where equity weights have no effect). Points above the line indicate policies that specifically favor protected populations (e.g., Māori in NZ).

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is this redundant with Page 5?"
- **Answer:** Page 5 is tabular and audit-focused. A visualization in the Benchmarking tab would help high-level decision-makers see jurisdictional patterns at a glance.
- **Action:** I recommend adding a `plot_fairness_frontier` function to `dashboard_helpers.py` in the **Next Chained Track (gdpe_0044_adversarial_vertical)** to stress-test these weights under extreme scenarios.

## 4. Current Phase Conclusion
The mathematical infrastructure is now in place to support this visualization. The `DCBAResult` and `ScenarioResult` both carry the necessary dual-metrics.
