# Track Specification: Publication-Grade Model Closure, Traceability, Dashboard Alignment, and Submission-Surface Sync

**Track ID:** gdpe_0020_dashboard_policy_alignment_and_publication_sync
**Type:** Feature / Publication Readiness Hardening
**Date:** 2026-03-07

---

## 1. Objective

Implement the review findings from `gdpe_0019` and subsequent publication-readiness exploration so that the active model path, dashboard, evidence/assumption traceability layer, reporting outputs, and manuscript-adjacent documents are aligned with one canonical system and defensible at a top-tier journal standard.

For this track, "publication standard" means the repository can survive both:
- expert review of model alignment, evidence traceability, transferability, and output integrity; and
- non-specialist policy-reader review of dashboard clarity, page flow, and interpretation support.

## 2. Scope

### 2.1 Active-Path Model Closure
- Replace publication-breaking placeholder aggregation on the active evaluation path with documented, empirically grounded implementations or explicitly quarantined exploratory outputs.
- Integrate proxy-substitution outputs into the pipeline rather than echoing placeholder values in `evaluate_single_policy`.
- Replace constant-based welfare placeholders with a documented welfare/DCBA ledger and explicit mapping from model outputs to policy-facing metrics.
- Retire or clearly demote scaffold-only modules and run surfaces that should not be interpreted as validated analysis paths.

### 2.2 Empirical Grounding and Reference Traceability
- Audit all active empirical inputs, priors, scenario values, and output-facing claims against the evidence registers in `context/jurisdiction_profiles/`.
- Reconcile evidence-register/config citation keys with the canonical CSL-JSON file at `study/references/references.json` so every active citation resolves to one authoritative ID scheme.
- Replace or rewrite the current reference validator so it targets the canonical CSL-JSON store, scans YAML/Markdown/code evidence surfaces, and runs cleanly cross-platform.
- Where assumptions remain necessary, document their justification, uncertainty treatment, transferability logic, and supporting references in `context/assumptions_registry.yaml` and related output-facing documents.

### 2.3 Jurisdiction and Comparator Canon
- Standardize one authoritative comparator vocabulary across the model layer, dashboard UI, scenario configs, reporting outputs, protocol, SAP, and methods text.
- Repair scenario and comparative-delta logic so scenarios bind both `ModelParameters` and `PolicyConfig`, and so active-looking scenario fields are never silently ignored.
- Ensure dashboard jurisdiction controls affect actual model evaluation, explanatory text, and any evidence-context summaries.
- Define and document which policy/config files are canonical, jurisdiction-specific, exploratory, or deprecated.

### 2.4 Transferability and Assumption Discipline
- Produce an explicit New Zealand transferability audit for any adapted non-NZ inputs and record the justification, evidence basis, and sensitivity treatment.
- Expand the assumptions registry from a minimal placeholder list to a complete active-path assumption inventory.
- Distinguish empirically calibrated, adapted, illustrative, and scaffolded surfaces in a single disclosure matrix consumable by code, docs, and dashboard copy.

### 2.5 Dashboard Usability and Explanation
- Add plain-language explanation blocks, glossary/help text, and recommended user-flow guidance across the dashboard.
- Rework any pages whose current presentation is too methodological or ambiguous for a non-specialist audience.
- Distinguish calibrated outputs from illustrative/exploratory surfaces everywhere they coexist.
- Raise the dashboard to a level where a smart non-specialist reader can understand what each page answers, what is uncertain, and which outputs are safe to cite.

### 2.6 Reporting and Output Quality
- Improve publish-pack parity across Markdown, DOCX, and PDF.
- Improve output labels, units, interpretive prose, figure/table completeness, and figure resolution/format handling.
- Replace static narrative boilerplate with data-driven summaries that identify the leading policy, interval width, and dominant uncertainty drivers.
- Remove any public-facing leakage of local file paths, placeholder metadata, or generic boilerplate from publication surfaces.
- Add stronger tests for output content quality and page-level dashboard behavior.

### 2.7 Protocol, Documents, and Manuscript Sync
- Update protocol- and manuscript-facing documents so they match the implemented dashboard, scenario engine, reporting outputs, and current model scope.
- Identify and close any stale claims in docs that overstate current functionality.
- Ensure protocol/manuscript-facing claims about evidence, assumptions, calibration, and data governance are traceable back to the evidence registers and canonical references.
- Reconcile all repo-facing claims about publication readiness, validation status, and repository topology so they are true under current implementation.
- Remove stale links, dead paths, `TODO` publication metadata, and submodule-era documentation that would mislead an external reviewer.

## 3. Acceptance Criteria

- [ ] Dashboard policy options and scenario pages use the canonical model/policy layer without known key mismatches.
- [ ] Remaining known placeholder logic on the active model/dashboard/output path is either replaced with grounded implementations or explicitly documented as justified assumptions.
- [ ] Active empirical inputs and assumptions are traceable to the evidence registers and canonical CSL-JSON references through one validated key scheme.
- [ ] The repository has a working cross-platform reference/traceability validator for evidence registers, configs, and manuscript-adjacent surfaces.
- [ ] New Zealand transfer/adaptation decisions are explicitly justified and sensitivity-linked rather than silently borrowed.
- [ ] Jurisdiction selection and page text align with actual model behavior.
- [ ] Active-looking scenario fields are either implemented, blocked, or clearly marked illustrative; they are not silently ignored.
- [ ] Dashboard pages include enough plain-language guidance that a non-specialist reader can follow what each page shows, how to interpret it, and what remains exploratory.
- [ ] Publish-pack artifacts are materially aligned and more publication-ready in labeling, narrative, and completeness.
- [ ] Public-facing repository/docs no longer contain stale paths, `Zenodo.TODO`, or unsupported claims of publication/SOTA readiness.
- [ ] Protocol/doc/manuscript-facing materials reflect the actual implemented system rather than the pre-review or placeholder state.

---

**Version:** 1.2
**Status:** Complete
