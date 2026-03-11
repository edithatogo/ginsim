# New Zealand Policy Investigation Report: Health System & Equity Audit

**Personas:** Ministry of Health, NZ Treasury  
**Date:** 2026-03-08

## 1. Summary of Findings
The NZ model is currently in a 'transplanted' state from the Australian framework. While it provides a useful heuristic for comparing policy directions, it requires significant localization—specifically regarding ACC integration and Māori health equity—to be considered for Cabinet-level advice.

## 2. Answers to User Questions

### Is this model useful for informing New Zealand policy?
Useful as a strategic exploration tool, but currently lacks the 'high-rigor' required for formal regulatory impact statements due to reliance on US/AU evidence proxies.

### How effectively does the model handle NZ-specific constraints?
- **ACC:** Mentioned in evidence registers but not functionally integrated. ACC's no-fault cover reduces the private insurance burden, which should theoretically lower testing deterrence—this effect is not yet quantified.
- **PHARMAC:** Cost-effectiveness thresholds are not explicitly linked to the QALY valuations in the DCBA ledger.

### What are the key gaps regarding Māori health equity and Treaty of Waitangi obligations?
Significant gap. While 'Te Mana Raraunga' principles are noted, the model lacks specific distributional weights or outcome metrics for Māori health. Distributional analysis by ethnicity is entirely absent from the core logic.

### What additional features or visualizations would be useful for NZ cabinet-level decisions?
- **Cross-Tasman Divergence Map:** Visualizing the risks of NZ becoming a 'regulatory outlier' compared to Australia.
- **Rural Access Heatmaps:** Mapping the 'Diagnostic Desert' effect in rural DHB (Te Whatu Ora) regions.
- **IDI Linkage Strategy:** A roadmap for anchoring model priors in New Zealand's Integrated Data Infrastructure.

### Should we prioritize adding specific international jurisdictions?
Yes. Prioritize **UK** (voluntary moratorium) and **Canada** (statutory ban). These jurisdictions provide the most relevant 'natural experiments' for the policy paths NZ is currently debating.

## 3. Equity Audit
The implementation of 'Fairness' in `src/model/fairness.py` must be expanded to include a **Treaty of Waitangi Framework**, moving beyond generic Rawlsian/Utilitarian views to reflect NZ's unique constitutional and health equity obligations.
