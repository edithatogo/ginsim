# Implementation plan: Bootstrap AU/NZ policy-econ repo

## Phase 1 — Core repo structure and policy schema
- [x] Create repo structure (src/, scripts/, configs/, docs/, context/) (retrospective)
- [x] Implement policy schema + loader (Pydantic + YAML) (retrospective)
- [x] Add baseline AU/NZ policy configs (retrospective)

## Phase 2 — Policy effect mapping and uncertainty
- [x] Implement heuristic policy→intensity mapping (retrospective)
- [x] Add parametric mapping and NumPyro fit scaffold (retrospective)
- [x] Add propagation hook `_mapping_params` into modules (retrospective)

## Phase 3 — Modules + DCBA ledger + VOI
- [x] Implement/extend modules A–F scaffolds (retrospective)
- [x] Add DCBA ledger scaffold and integrate into VOI script (retrospective)
- [x] Add EVPPI surrogates and decomposition scaffolds (retrospective)

## Phase 4 — Posterior propagation and AU/NZ comparisons
- [x] Add posterior propagation runner(s) (retrospective)
- [x] Add AU vs NZ comparison runner (retrospective)
- [x] Add meta pipeline runner orchestrating AU+NZ (retrospective)

## Phase 5 — Publish artifacts + documentation
- [x] Add publish pack generator (MD/DOCX/PDF/figures) (retrospective)
- [x] Add context engineering improvements + evidence templates (retrospective)
- [x] Add game-theoretic framing doc (retrospective)

## Notes
This track is recorded retrospectively to reflect work already completed in this repository build.
