# Inquiry: AU Fiscal & Regulatory Mapping (Medicare & Oversight)

**Track:** gdpe_0034_au_system_localization
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How do we distinguish between the credibility of a statutory ban vs. the voluntarism of the FSC moratorium in terms of ASIC oversight?

## 1. The Medicare Cost-Sharing Logic
In Australia, the cost of genetic testing is split between the individual (out-of-pocket) and the Commonwealth (Medicare).
- **Mechanism:** A high `medicare_cost_share` (e.g., 0.85) reduces the direct utility cost of testing for the individual in Module A.
- **Fiscal Shift:** This must be reflected in the DCBA ledger as an increased fiscal burden on the government but a higher consumer surplus.

## 2. Regulatory Oversight: ASIC vs. APRA
The current model uses a generic `enforcement_effectiveness`. We need to move to **"Audit Intensity."**
- **Statutory Ban (ASIC Oversight):** Regulated by law. Audit intensity is high because non-compliance is a legal violation with public reporting.
- **Voluntary Moratorium (FSC Self-Regulation):** Regulated by industry agreement. Audit intensity is lower as it relies on industry self-reporting and voluntary audits.

## 3. Implementation Action
1. **Update `australia.yaml`:** Add `medicare_cost_share: 0.75` and `audit_intensity: 0.60`.
2. **Refactor Module A:** In `compute_testing_uptake`, reduce the test cost component by `(1.0 - medicare_cost_share)`.
3. **Refactor Pipeline:** Map `expected_penalty` to `penalty_max * audit_intensity`.
