# Reviewer Navigation Map

**Status:** Updated against the current generated package on 2026-03-07  
**Primary package root:** `outputs/runs/meta_pipeline/20260307T064546Z`  
**Purpose:** Give a reviewer a direct path from major claims to the implemented code, generated outputs, assumptions, and remaining caveats.

---

## How to use this map

Start with the reviewer question in the first column. Each row points to the main narrative surface, the implemented code path, the current generated artifact, and the main caveat that should shape interpretation.

## Claim-to-evidence map

| Reviewer question or claim | Primary document surface | Implemented code path | Current generated artifact | Governing assumptions / references | Caveat / interpretation note |
|---|---|---|---|---|---|
| What policy comparators are actually implemented? | `README.md`, `docs/CURRENT_STATUS.md`, methods/protocol docs | `src/model/module_a_behavior.py`, `src/model/scenario_analysis.py`, `streamlit_app/app.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/policy_summary.csv` | `context/assumptions_registry.yaml`, `study/references/references.json` | The active comparator canon is `status_quo`, `moratorium`, `ban`. |
| How are policy outcomes computed on the active path? | `docs/METHODS_SECTION_DRAFT.md`, `docs/MODEL_CARD.md` | `src/model/pipeline.py`, `src/model/dcba_ledger.py`, `src/model/module_d_proxy.py` | `outputs/runs/meta_pipeline/20260307T064546Z/compare/REPORT.md` and publish-pack summary tables | assumptions registry plus evidence-register citations | The active output surface is implemented, but the package still lacks rebuilt decomposition and EVPPI sidecars. |
| What concrete reviewer package exists right now? | `docs/MANUSCRIPT_ASSET_INVENTORY.md`, `docs/SUBMISSION_GAP_REGISTER.md` | `scripts/run_meta_pipeline.py`, `scripts/publish_pack.py`, `scripts/generate_figures.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/` | reporting manifest and run manifests | The current package is real and reproducible, but it is still a policy-brief package rather than a final manuscript submission bundle. |
| Which figures and tables are currently available? | `docs/MANUSCRIPT_ASSET_INVENTORY.md` | `scripts/generate_figures.py`, `scripts/reporting_common.py` | Net-benefit figures and summary CSVs under `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/` | reporting manifest | EVPPI and decomposition figures are not currently generated because the legacy runners are broken against removed APIs. |
| What still blocks a cleaner journal submission package? | `docs/SUBMISSION_GAP_REGISTER.md` | n/a | `outputs/runs/meta_pipeline/20260307T064546Z/compare/REPORT.md` plus the gap register | n/a | The authoritative current blockers are decomposition/EVPPI rebuild, manuscript-grade asset lift, and substantive interpretation review. |

## Reading note

- Treat the generated package as the authoritative current output surface.
- Treat older milestone or scaffold wording elsewhere in the repository as historical unless it matches the current package path above.
