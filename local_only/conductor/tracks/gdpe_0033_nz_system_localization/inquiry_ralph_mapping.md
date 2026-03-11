# Inquiry: NZ Institutional Mapping (ACC & PHARMAC)

**Track:** gdpe_0033_nz_system_localization
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How exactly does ACC's existence shift the price elasticity of life insurance for individuals with genetic risks?

## 1. The ACC Displacement Effect
In Australia, a genetic diagnosis (e.g., increased risk of stroke) creates a pure private insurance burden. If the individual is deterred from testing, they lose prevention value.

In New Zealand, the **Accident Compensation Corporation (ACC)** provides no-fault cover for "Treatment Injury" and "Personal Injury." 
- **Mechanism:** If a genetic condition leads to an event that ACC covers (e.g., a medical misadventure during preventative surgery or a stroke classified as an injury), the financial downside is partially socialized.
- **Economic Hypothesis:** This social safety net should *decrease* the price elasticity of demand for private life insurance. Individuals are less "deterred" by private insurance discrimination if they know ACC covers the catastrophic medical/disability costs.

## 2. PHARMAC Threshold Linkage
PHARMAC uses a cost-effectiveness threshold (often cited around $20k-$40k per QALY, though not officially public).
- **Integration:** The DCBA ledger's `value_per_qaly` should be strictly linked to this NZ-specific threshold to provide "Cabinet-Ready" advice.

## 3. Implementation Action
1. **Update `new_zealand.yaml`:** Add `acc_deterrence_offset: 0.15` and `pharmac_qaly_threshold: 35000.0`.
2. **Refactor Module A:** Multiply the `perceived_penalty` by `(1.0 - acc_deterrence_offset)` for NZ runs.
3. **Refactor DCBA:** Use `pharmac_qaly_threshold` for the health benefit valuation.
