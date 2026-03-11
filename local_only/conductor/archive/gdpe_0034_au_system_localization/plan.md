# Implementation Plan: AU System Localization (Medicare & Oversight)

**Track ID:** gdpe_0034_au_system_localization
**Execution mode:** Autonomous Phase Loop

## Phase 1: Parameter & Baseline Verification
- [x] Task: Verify `medicare_cost_share` and `audit_intensity` in `ModelParameters`.
- [x] Task: Verify baseline cost reduction in `module_a_behavior.py`.
- [x] Task: Conductor - Autonomous Review & Remediation 'Baseline'

## Phase 2: Oversight Modeling Refinement
- [x] Task: Update `compute_perceived_penalty` to use `audit_intensity` more explicitly for AU.
- [x] Task: Implement APRA vs ASIC distinction if beneficial (or clarify logic).
- [x] Task: Conductor - Autonomous Review & Remediation 'Oversight'

## Phase 3: Evidence Anchoring
- [x] Task: Add `AU_medicare_001` and `AU_enf_003` (Audit Intensity) to `australia_evidence_register.yaml`.
- [x] Task: Update `configs/jurisdictions/australia.yaml` to match synthesis.
- [x] Task: Conductor - Autonomous Review & Remediation 'Evidence'

## Phase 4: Verification & Closure
- [x] Task: Run AU-specific smoke tests.
- [x] Task: Verify "Medicare Rebate" impact on testing utility.
- [x] Task: Final track closure and registry sync.

## Phase 5: Review Fixes
- [x] Task: Apply review suggestions 3bfeb18
