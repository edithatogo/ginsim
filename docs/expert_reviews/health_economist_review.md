# Expert Face-Validity Review: Health Economics

**Expert Persona:** Dr. Elena Vance  
**Field:** Health Economics & Technology Assessment (HTA)  
**Date:** 2026-03-05  
**Model Version:** 2d371e2 (Track gdpe_0012 archived)

---

## 1. Executive Summary
The model provides a robust framework for aggregating welfare impacts across stakeholders using a JAX-accelerated pipeline. The inclusion of research externalities (Module F) and family altruism (Extended Games) is commendable and aligns with contemporary literature. However, the current implementation of time dynamics and QALY-equivalence for scientific loss requires significant refinement to be "policy-convincing."

## 2. Technical Audit: Welfare Aggregation & QALYs

### 2.1 Logic Audit: Linear QALY-Equivalence
The "Scientific Loss" and "Altruism Gain" in the Extended Games use a simple multiplicative factor to estimate welfare impacts. 
- **Critique:** The assumption that research value loss scales linearly with "reconstruction accuracy" is likely an oversimplification. Scientific progress often follows a threshold or "step-function" behavior—losing 10% of a cohort might have negligible impact, but losing 40% might prevent a study from reaching statistical power entirely.
- **Recommendation:** Implement a non-linear "Scientific Power" function in `src/model/extended_games.py`.

### 2.2 Time Dynamics Audit (SOTA Requirement)
The model correctly identifies health benefits in QALY terms but fails to explicitly separate the **Fiscal Time-Horizon**.
- **Critique:** As a Health Economist, I see no differentiation between Year 1 implementation costs (high) and Year 15 health savings (discounted). Policymakers need to see the "Fiscal Breakeven Point."
- **Logic Check:** `dcba_ledger.py` aggregates all values into a single point-estimate. This hides the "political valley" where costs are high before any health gains materialize.
- **Recommendation:** Add a multi-period output to the DCBA ledger to show Year 1, Year 5, and Year 20 outcomes.

## 3. Specific Inquiries

| Inquiry | Response/Critique |
|---------|-------------------|
| **Distributional Equity (DCEA)** | The `apply_distributional_weight` function is present but currently uses a static weight (1.0). This needs to be calibrated against actual equity priorities (e.g., Māori/Indigenous health gaps). |
| **Scientific Opportunity Cost** | The `compute_research_value_loss` logic in Module F is a good start, but the `annual_research_value` parameter ($1M) lacks a clear evidence anchor in the Australian context. |
| **Discounting Consistency** | The model uses a 3% discount rate in Module F, but other modules appear to use undiscounted aggregate values. Discounting must be consistent across all welfare components. |

## 4. Final Verdict: Conditional Face-Validity
The model logic is mathematically sound but structurally "flat." It captures the **What** but not the **When**. To be persuasive to a Treasury official, the model must demonstrate the temporal delay between regulatory spending and population health gains.

---
**Signed:**  
*Dr. Elena Vance*  
Senior Health Economist
