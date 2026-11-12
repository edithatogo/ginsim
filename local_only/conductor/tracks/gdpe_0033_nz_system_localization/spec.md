# Track Specification: NZ System Localization (ACC & PHARMAC)

**Track ID:** gdpe_0033_nz_system_localization
**Type:** Feature / Jurisdictional Rigor
**Goal:** functionally integrate New Zealand's ACC (no-fault cover) and PHARMAC (cost-effectiveness) logic into the policy evaluation pipeline.

## 1. Overview
The current NZ model is an Australian transplant. This track localizes the health economic logic to account for ACC's impact on insurance demand and PHARMAC's specific QALY valuation thresholds.

## 2. Functional Requirements
- **ACC Integration:** Update `module_a_behavior.py` to reduce deterrence if ACC covers the primary genetic condition (e.g., specific cancers/injuries).
- **PHARMAC Linkage:** Synchronize the DCBA ledger's `value_per_qaly` with PHARMAC's internal thresholds for NZ runs.
- **NZ-Specific Evidence:** Anchor all new parameters in the `nz_evidence_register.yaml`.

## 3. Acceptance Criteria
- [ ] NZ outputs show distinct clinical-economic behavior compared to AU when ACC is enabled.
- [ ] PHARMAC thresholds implemented as a sidebar advanced control.
