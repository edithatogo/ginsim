# Australian Policy Investigation Report: Fiscal & Regulatory Audit

**Personas:** Department of Health, Treasury  
**Date:** 2026-03-08

## 1. Summary of Findings
The model provides a high-utility framework for comparing the 2019 FSC Moratorium against the proposed 2025 Statutory Ban. The JAX-powered sensitivity analysis (EVPPI) is particularly valuable for Australian Treasury analysts evaluating policy robustness under uncertainty.

## 2. Answers to User Questions

### Is this model useful for informing Australian genetic discrimination policy?
Highly relevant. It explicitly models the shift from self-regulation (Moratorium) to legislation (Ban). The comparative framing aligns with current parliamentary discussions.

### How robust is the fiscal impact modeling and market stability analysis?
Market stability is robustly modeled using Rothschild-Stiglitz equilibria in Module C. Fiscal impacts are tracked via the DCBA ledger (Module Ledger), though specific parameters like `cost_per_test` and `health_savings_per_test` require more frequent AU-specific calibration to move beyond 'toy' status.

### What are the specific implementation hurdles identified in the code?
- **JIT Constraints:** The requirement for stateless logic in JAX complicates the implementation of complex, branching AU regulatory rules (e.g., specific sum-insured thresholds).
- **Compliance Modeling:** `module_enforcement.py` uses simplified detection probabilities which may not reflect the actual oversight capabilities of Australian regulators (ASIC/APRA).

### What additional features would be useful?
- **Medicare Toggle:** Explicit modeling of Medicare-funded vs. out-of-pocket testing costs.
- **Tapering Logic:** Implementation of phased 'glide paths' for moratorium caps.
- **Oversight Agencies:** Modeling specific enforcement behaviors linked to ASIC/APRA.

### Is expansion beyond the current scope justified?
- **Employment:** Justified. The proxy discrimination logic (Module D) is naturally extensible to HR data.
- **Health Insurance:** Not justified with current architecture. AU Private Health Insurance is community-rated (no risk-rating), which breaks the fundamental logic of Module C.

## 3. Regulatory Toggles Audit
The code currently relies on generic `enforcement_strength` and `penalty_max`. To elevate this for AU policy, these should be linked to specific legislative clauses from the *Insurance Act 1973* or the proposed 2025 amendments.
