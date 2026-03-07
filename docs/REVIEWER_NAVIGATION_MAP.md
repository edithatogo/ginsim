# Reviewer Navigation Map

**Status:** Draft scaffold created in `gdpe_0021` Phase 1  
**Purpose:** Give a journal reviewer a direct path from major manuscript/repository claims to the supporting code, outputs, assumptions, and references.

---

## How to use this map

Start with the reviewer question or claim category in the first column. Each row points to the main document surface, the implemented code path, the supporting output artifact, the governing assumptions, and the canonical references that should be checked.

This map is intentionally conservative. If a surface is exploratory or adapted rather than fully calibrated, that should be stated explicitly in the caveat column.

## Claim-to-Evidence Map

| Reviewer question or claim | Primary document surface | Implemented code path | Supporting output artifact | Governing assumptions | Canonical references | Caveat / interpretation note |
|---|---|---|---|---|---|---|
| What policy comparators are actually implemented? | `README.md`, `docs/CURRENT_STATUS.md`, protocol/methods docs | `src/model/module_a_behavior.py`, `src/model/scenario_analysis.py`, `streamlit_app/app.py` | publish-pack policy summary tables and dashboard benchmark comparison | comparator canon in assumptions registry and jurisdiction profiles | `study/references/references.json` IDs used by configs/evidence registers | Active canonical set is `status_quo`, `moratorium`, `ban`; sandbox surfaces remain exploratory where stated. |
| How are welfare and policy outcomes computed on the active path? | `docs/METHODS_SECTION_DRAFT.md`, `docs/MODEL_CARD.md` | `src/model/pipeline.py`, `src/model/dcba_ledger.py`, `src/model/module_d_proxy.py` | policy summary tables, net benefit figures, uncertainty figures | assumptions registry entries for welfare mapping, transferability, proxy substitution | canonical reference IDs linked through evidence registers | The active path is implemented; some broader extensions remain outside the active manuscript-ready scope. |
| Which outputs are calibrated versus exploratory? | `docs/MODEL_CARD.md`, dashboard explanation copy, methods/protocol docs | `streamlit_app/app.py`, `streamlit_app/pages/*.py`, reporting scripts | dashboard pages, publish-pack outputs, caption files | assumptions registry and scenario disclosure notes | canonical reference IDs and scenario config citations | Scenario sandbox and extended-game surfaces must be read with their exploratory labels. |
| Where do key empirical assumptions come from? | `docs/METHODS_SECTION_DRAFT.md`, assumptions and traceability docs | `context/assumptions_registry.yaml`, `context/jurisdiction_profiles/*`, `scripts/validate_references.py` | traceability report and manuscript-facing assumption summaries | assumption IDs in registry | `study/references/references.json` plus alias reconciliation | Adapted NZ inputs must be read with transferability notes, not as direct NZ measurement unless stated. |
| What still blocks clean journal submission? | `docs/SUBMISSION_GAP_REGISTER.md` | n/a | submission-gap register and track completion notes | n/a | n/a | This is the authoritative current blocker list for manuscript packaging. |

## Notes

- This scaffold is expected to be expanded in `gdpe_0021` Phase 2.
- File paths and artifact names should stay aligned with the active implementation rather than archival milestone documents.
