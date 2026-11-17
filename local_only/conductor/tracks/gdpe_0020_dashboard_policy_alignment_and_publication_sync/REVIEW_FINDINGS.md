# Review Findings: gdpe_0020_dashboard_policy_alignment_and_publication_sync

**Date:** 2026-03-07
**Purpose:** Consolidate the post-`gdpe_0019` exploration findings that define the publication-readiness hardening work for `gdpe_0020`.

---

## Priority Findings

### 1. High: The active model/output path still contains placeholder aggregation.
- `src/model/pipeline.py` still computes key policy-facing outputs using placeholder proxy values and fixed welfare constants.
- `src/model/module_d_proxy.py` exposes an optimizer surface that does not yet materially use `params` and `policy`.
- This means the current headline outputs are not yet fully empirically grounded, even where the dashboard and docs imply they are.

### 2. High: Citation traceability is not internally coherent.
- Evidence registers use long-form citation keys while `study/references/references.json` uses short-form CSL IDs.
- The current reference validator targets `context/references.bib` instead of the CSL-JSON store and is not a reliable publication QA surface.
- The repo therefore lacks a functioning canonical evidence-to-reference resolver.

### 3. High: The assumptions layer is placeholder-grade.
- `context/assumptions_registry.yaml` still contains only three high-level placeholder entries.
- This is not enough for a multi-jurisdiction, partially adapted policy-evaluation model intended for external peer review.

### 4. High: New Zealand calibration relies heavily on transferred/adapted evidence without a full justification layer.
- Several NZ calibration entries explicitly import non-NZ evidence or qualitative-to-quantitative mappings.
- Those transfers need a dedicated audit and manuscript-grade disclosure, not just inline notes in configs.

### 5. High: Comparator and scenario canon are still fragmented.
- The canonical model registry exposes `status_quo`, `moratorium`, and `ban`.
- The dashboard and some documentation still use `statutory_ban`.
- Scenario configs continue to expose fields that look active, but some are currently ignored by the evaluation path.

### 6. High: Repo-facing documents still overclaim readiness and validation.
- `docs/PUBLICATION_READINESS.md`, `docs/CURRENT_STATUS.md`, and `docs/MODEL_VALIDATION_REPORT.md` still claim publication/SOTA readiness that is not supported by the current active-path state.
- `docs/MODEL_CARD.md` simultaneously discloses scaffold limitations, which creates visible contradiction.

### 7. High: Study/documentation topology is stale.
- `study/README.md` still references non-existent submodule-era paths and a placeholder external GitHub URL.
- Public-facing metadata still includes `Zenodo.TODO`.
- These are immediate credibility failures for an external reviewer.

### 8. Medium: Dashboard UX remains too method-heavy for non-specialists.
- The current dashboard still expects readers to infer what the page is for, which metrics matter, and which pages are exploratory.
- It does not yet provide the level of plain-language scaffolding needed for a policy audience or an intelligent lay reader.

### 9. Medium: Reporting outputs are reproducible but not yet manuscript-grade.
- Publish-pack outputs still use generic prose, incomplete parity across formats, and public-artifact hygiene that is not yet submission-safe.
- The current figure surface is narrow relative to the uncertainty outputs already computed in the reporting bundle.

---

## Required Workstreams

1. **Model closure:** remove or quarantine active-path placeholder logic.
2. **Citation reconciliation:** unify evidence keys and CSL-JSON IDs, then validate them automatically.
3. **Assumption discipline:** expand assumptions and transferability disclosure to publication standard.
4. **Comparator canon:** make one policy/scenario taxonomy authoritative across code, UI, configs, and docs.
5. **Dashboard comprehension:** add plain-language framing, guidance, and calibrated/exploratory labeling.
6. **Reporting integrity:** make publication artifacts data-driven, complete, and externally safe.
7. **Claims reconciliation:** remove unsupported readiness/validation claims until the implementation truly supports them.

---

## Nature-Bar Interpretation

For this repository to be defensible at a Nature Human Behaviour level, it is not enough for the code to run and the dashboard to render. The project needs:
- an active analysis path that is not visibly scaffolded;
- a fully auditable evidence/assumption/reference chain;
- one coherent comparator vocabulary across all surfaces;
- dashboard and output surfaces that are understandable, honest about uncertainty, and safe to cite;
- documentation and protocol text that describe the implemented system rather than the intended one.
