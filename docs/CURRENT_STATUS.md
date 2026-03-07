# Current Status

**Last updated:** 2026-03-07  
**Current track:** none  
**Most recently completed track:** `gdpe_0021_manuscript_harmonization_and_submission_pack`  
**Next planned track:** none

---

## Repository state

- The archived milestone baseline remains historically complete, but it is no longer the authoritative readiness signal.
- The active submission-facing orientation surfaces are:
  - `docs/CURRENT_STATUS.md`
  - `docs/REVIEWER_NAVIGATION_MAP.md`
  - `docs/MANUSCRIPT_ASSET_INVENTORY.md`
  - `docs/SUBMISSION_GAP_REGISTER.md`
- The current repository state now includes a fresh generated package rooted at `outputs/runs/meta_pipeline/20260307T064546Z`.

## Current generated package

- Meta run root: `outputs/runs/meta_pipeline/20260307T064546Z`
- Publish pack root: `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack`
- Generated brief artifacts:
  - `POLICY_BRIEF.md`
  - `POLICY_BRIEF.docx`
  - `POLICY_BRIEF.pdf`
- Generated structured outputs:
  - `policy_summary.csv`
  - `australia_policy_summary.csv`
  - `new_zealand_policy_summary.csv`
  - `reporting_manifest.json`
- Generated figures:
  - `figures/australia_net_benefit.png`
  - `figures/new_zealand_net_benefit.png`
  - paired caption files for both figures

## Verified checks in this pass

- `pytest -p no:cacheprovider tests/unit/test_reporting_pipeline.py -q` passed with `5 passed`.
- `python -m scripts.run_meta_pipeline --n_draws 30` completed and produced the current meta run.
- `python -m scripts.publish_pack --meta_dir outputs/runs/meta_pipeline/20260307T064546Z` completed and produced the current publish pack.

## Current interpretation state

- The active packaging path is now functional and reproducible from the current codebase.
- The current package is adequate as a reviewer-facing policy brief and reporting bundle.
- The current package should not yet be described as a complete manuscript submission package.

## Remaining blockers

- Legacy uncertainty decomposition scripts still depend on removed `sobol_first_order_rff` APIs.
- Legacy EVPPI generation still depends on removed `src.model.evppi_rff`.
- The current package does not yet provide rebuilt decomposition or EVPPI sidecars.
- The current package also has not yet been lifted into a final manuscript-grade asset set with final numbering, journal-specific tables, and discussion framing.

## Reviewer-facing reading order

1. Start with `docs/REVIEWER_NAVIGATION_MAP.md`.
2. Check `docs/MANUSCRIPT_ASSET_INVENTORY.md` for the exact generated asset set.
3. Check `docs/SUBMISSION_GAP_REGISTER.md` for what is still missing or not yet defensible to claim.
