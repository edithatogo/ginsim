# Implementation Plan: Implement Dashboard/Policy Alignment, Plain-Language UX, and Document Sync

**Track ID:** gdpe_0020_dashboard_policy_alignment_and_publication_sync  
**Estimated duration:** 5-7 days

---

## Phase 1 - Empirical Audit and Placeholder Closure

### Tasks
- [x] Audit active parameters, scenario inputs, and dashboard-facing metrics against the evidence registers.
- [x] Identify which active code paths still use placeholder/scaffold values rather than grounded inputs.
- [x] Add missing supporting citations to `study/references/references.json` and missing assumption entries/justifications to `context/assumptions_registry.yaml`.
- [x] Reconcile evidence, assumption, and reference keys so evidence-register citations, canonical CSL-JSON IDs, and output-facing references use a single consistent identifier set.
- [x] Replace or explicitly quarantine any public-facing outputs that still depend on scaffold-only model components.

---

## Phase 2 - Model and Scenario Alignment

### Tasks
- [x] Unify dashboard policy keys with the canonical registry in the model layer.
- [x] Repair `scenario_analysis` so scenario YAML binds real policy regimes and valid parameter subsets.
- [x] Wire jurisdiction selection into both evaluation and explanatory text.
- [x] Replace or explicitly quarantine remaining placeholder logic on the active model/dashboard path.
- [x] Distinguish calibrated benchmark scenarios from sandbox/custom-policy scenarios in both computation and presentation.

---

## Phase 3 - Dashboard Usability and Coverage

### Tasks
- [x] Add page-level plain-language explanation blocks and glossary/help support.
- [x] Review page layout and information density for non-specialist comprehension.
- [x] Add page-level tests for Scenarios, Sensitivity, Delta View, and Extended Games.
- [x] Add calibrated/exploratory badges and provenance notes to all non-landing pages.
- [x] Standardize metric units, horizons, and decision-facing definitions across the dashboard.
- [x] Add a guided user flow on the landing page for first-time and non-technical readers.

---

## Phase 4 - Reporting and Publication Sync

### Tasks
- [x] Improve publish-pack parity and output labeling/units/narrative quality.
- [x] Update protocol/doc/manuscript-facing artifacts to match the implemented functionality, empirical grounding, and current claims.
- [x] Verify the final aligned behavior with targeted tests and artifact checks.
- [x] Remove or qualify "publication-ready" and "ready-to-share" claims in docs until the outputs satisfy the strengthened acceptance criteria.
- [x] Add richer policy-brief figures, including uncertainty decomposition and manuscript-ready captioning.
- [x] Make the brief narrative data-driven rather than template-driven, and prevent public outputs from exposing local filesystem paths.

---

**Version:** 1.2  
**Status:** Complete
