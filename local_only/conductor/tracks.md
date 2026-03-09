# Tracks registry

This registry is the index of Conductor tracks for this repository.

## Active Tracks

| Track ID | Title | Status | Link |
|---|---|---|---|
| gdpe_0022_empirical_traceability_and_legacy_closure | Empirical traceability and legacy analysis closure | Completed | [track](./tracks/gdpe_0022_empirical_traceability_and_legacy_closure/index.md) |

## Planned Tracks

| Track ID | Title | Status | Link |
|---|---|---|---|
| _None_ | | | |

## Completed Follow-up Tracks

| repo_scrub_audit_20260308 | Repository Scrub and Audit | Completed | [track](./tracks/repo_scrub_audit_20260308/index.md) |

| Track ID | Title | Status | Link |
|---|---|---|---|
| gdpe_0021_manuscript_harmonization_and_submission_pack | Manuscript harmonization, archival cleanup, and submission-pack refinement | ✅ Complete | [track](./tracks/gdpe_0021_manuscript_harmonization_and_submission_pack/index.md) |
| gdpe_0034_au_system_localization | AU System Localization (Medicare & Oversight) | ✅ Complete | [archived](./archive/gdpe_0034_au_system_localization/index.md) |
| gdpe_0043_interop_vertical | Interoperability & Standardized HTA Export | ✅ Complete | [archived](./archive/gdpe_0043_interop_vertical/index.md) |
| gdpe_0036_spatial_equity | Spatial Equity & 'Diagnostic Deserts' | ✅ Complete | [archived](./archive/gdpe_0036_spatial_equity/index.md) |
| gdpe_0020_dashboard_policy_alignment_and_publication_sync | Publication-grade model closure, traceability, dashboard alignment, and submission-surface sync | ✅ Complete | [track](./tracks/gdpe_0020_dashboard_policy_alignment_and_publication_sync/index.md) |
| gdpe_0019_review_and_author_metadata | Comprehensive codebase review and author-metadata alignment | ✅ Complete | [track](./tracks/gdpe_0019_review_and_author_metadata/index.md) |
| gdpe_0018_dashboard_alignment | Dashboard, validation, and gin-sim alignment | ✅ Complete | [track](./tracks/gdpe_0018_dashboard_alignment/index.md) |
| gdpe_0017_reporting_pipeline | Reporting and publish-pack pipeline refinement | ✅ Complete | [track](./tracks/gdpe_0017_reporting_pipeline/index.md) |
| gdpe_0016_repo_hardening | Repository-wide lint, typing, and automation hardening | ✅ Complete | [track](./tracks/gdpe_0016_repo_hardening/index.md) |
| gdpe_0015_reconciliation | Conductor reconciliation and working tree classification | ✅ Complete | [track](./tracks/gdpe_0015_reconciliation/index.md) |

## Archived Tracks

| Track ID | Title | Status | Link |
|---|---|---|---|
| gdpe_0014_repo_professionalization | Repository Professionalization & Remote Monitoring | ✅ Complete | [archived](./archive/gdpe_0014_repo_professionalization/index.md) |
| gdpe_0013_external_validation | External Validation & Historical Concordance | ✅ Complete | [archived](./archive/gdpe_0013_external_validation/index.md) |
| gdpe_0012_dashboard_enhancements | Dashboard enhancements (diagrams, sensitivity, JAX verification) | ✅ Complete | [archived](./archive/gdpe_0012_dashboard_enhancements/index.md) |
| gdpe_0011_streamlit_e2e | Streamlit dashboard E2E testing + gin-sim repo | ✅ Complete | [archived](./archive/gdpe_0011_streamlit_e2e/index.md) |
| gdpe_0010_final_repo_check | Final repository check | ✅ Complete | [archived](./archive/gdpe_0010_final_repo_check/index.md) |
| gdpe_0009_streamlit_dashboard | Streamlit dashboard with GitHub sync | ✅ Complete | [archived](./archive/gdpe_0009_streamlit_dashboard/index.md) |
| gdpe_0008_testing_strategy | Comprehensive testing (>95% coverage) | ✅ Complete | [archived](./archive/gdpe_0008_testing_strategy/index.md) |
| gdpe_0007_game_execution | Game execution (individual + hybrid) | ✅ Complete | [archived](./archive/gdpe_0007_game_execution/index.md) |
| gdpe_0006_formulae_verification | Formulae verification and documentation | ✅ Complete | [archived](./archive/gdpe_0006_formulae_verification/index.md) |
| gdpe_0005_game_validation | Game validation and documentation | ✅ Complete | [archived](./archive/gdpe_0005_game_validation/index.md) |
| gdpe_0004_quality_assurance | Quality assurance and publication readiness | ✅ Complete | [archived](./archive/gdpe_0004_quality_assurance/index.md) |
| gdpe_0003_model_implementation | Model implementation and policy analysis | ✅ Complete | [archived](./archive/gdpe_0003_model_implementation/index.md) |
| gdpe_0002_evidence_anchoring | Evidence register + calibration plan for AU/NZ | ✅ Complete | [archived](./archive/gdpe_0002_evidence_anchoring/index.md) |
| gdpe_0001_bootstrap | Bootstrap the AU/NZ genetic discrimination policy-econ modelling repo | ✅ Completed | [archived](./archive/gdpe_0001_bootstrap/index.md) |

---

## Milestone Summary

**Completed milestone tracks:** 14/14
**Repository baseline:** Historical milestone marked Publication Ready (SOTA); superseded by follow-up review findings
**Current active follow-up track:** none
**Next planned follow-up track:** none

---

## Notes

- Historical Conductor files from completed tracks are intentionally retained in `conductor/tracks/` and `conductor/archive/` for traceability.
- `gdpe_0015_reconciliation` captures the classification step that promoted the dirty working tree into explicit follow-on tracks.
- `gdpe_0016_repo_hardening` is now complete; remaining lint debt is intentionally separated between deferred follow-on work (`gdpe_0017`, `gdpe_0018`) and a smaller set of non-blocking structural refactor candidates.
- `gdpe_0017_reporting_pipeline` and `gdpe_0018_dashboard_alignment` are now complete.
- `gdpe_0019_review_and_author_metadata` is complete and records the next implementation priorities: canonical policy-ID unification, scenario-engine repair, and broader page-level dashboard coverage.
- `gdpe_0020_dashboard_policy_alignment_and_publication_sync` is complete and records the closure of active-path placeholder debt, traceability reconciliation, dashboard plain-language usability, reporting hardening, and primary protocol/document synchronization.
- `gdpe_0021_manuscript_harmonization_and_submission_pack` is complete and records the reviewer-facing harmonization, manuscript asset inventory, submission-gap register, and archival qualification pass.

---

- [x] **Track: Cleanse remote repo of AI artifacts/context, relocate to local_only, and perform high-rigor audit.**
*Link: [./tracks/repo_scrub_audit_20260308/](./tracks/repo_scrub_audit_20260308/)*

---

- [x] **Track: Simulate multi-persona peer review from high-impact journals and government departments.**
*Link: [./tracks/peer_review_simulation_20260308/](./tracks/peer_review_simulation_20260308/)*


---

- [x] **Track: Expand to Global Benchmarking (UK, CAN, US) with Threshold Architecture and PPP normalization.**
*Link: [./tracks/gdpe_0030_global_benchmarking/](./tracks/gdpe_0030_global_benchmarking/)*


---

- [x] **Track: Equity Localization (Maori & Quintile Weights)**
*Link: [./tracks/gdpe_0031_equity_localization/](./tracks/gdpe_0031_equity_localization/)*

---

- [x] **Track: Regulatory Tapering & Nuance (Glide Paths)**
*Link: [./tracks/gdpe_0032_regulatory_tapering/](./tracks/gdpe_0032_regulatory_tapering/)*

---

- [x] **Track: NZ System Localization (ACC & PHARMAC)**
*Link: [./tracks/gdpe_0033_nz_system_localization/](./tracks/gdpe_0033_nz_system_localization/)*

---



---

- [x] **Track: Empirical 'Information Gap' Mapping**
*Link: [./tracks/gdpe_0035_empirical_information_gap/](./tracks/gdpe_0035_empirical_information_gap/)*

---



---

- [x] **Track: End-to-End Visualization Audit**
*Link: [./tracks/gdpe_0037_viz_audit_e2e/](./tracks/gdpe_0037_viz_audit_e2e/)*

---

- [x] **Track: Comprehensive Sensitivity Suite Overhaul**
*Link: [./tracks/gdpe_0038_sensitivity_overhaul/](./tracks/gdpe_0038_sensitivity_overhaul/)*

---

- [x] **Track: Bayesian Calibration Vertical (NumPyro/BlackJAX)**
*Link: [./tracks/gdpe_0039_calibration_vertical/](./tracks/gdpe_0039_calibration_vertical/)*

---

- [~] **Track: Automated Manuscript & Artifact Lifecycle**
*Link: [./tracks/gdpe_0040_manuscript_vertical/](./tracks/gdpe_0040_manuscript_vertical/)*

---

- [x] **Track: Formal Mathematical Anchoring Vertical (Proof Engine)**
*Link: [./tracks/gdpe_0041_math_verification_vertical/](./tracks/gdpe_0041_math_verification_vertical/)*

---

- [~] **Track: Temporal Evolution & Market Dynamics (10-Year Horizon)**
*Link: [./tracks/gdpe_0042_temporal_evolution/](./tracks/gdpe_0042_temporal_evolution/)*

---



---

- [ ] **Track: Adversarial Economic Red-Teaming Vertical**
*Link: [./tracks/gdpe_0044_adversarial_vertical/](./tracks/gdpe_0044_adversarial_vertical/)*

---

- [ ] **Track: Agentic Delphi Protocol Vertical (Permanent Audit)**
*Link: [./tracks/gdpe_0045_agentic_delphi_vertical/](./tracks/gdpe_0045_agentic_delphi_vertical/)*
