# Genetic discrimination policy: integrated economic evaluation (JAX/XLA)

This repository is a reproducible scaffold for a linked, modular economic evaluation of policy options restricting genetic discrimination, implemented with a JAX-first stack.

**License:** MIT (code) | CC-BY 4.0 (documentation/outputs)

**Citation:** See [CITATION.cff](CITATION.cff)

---

## Contents

### Research infrastructure
- `protocols/` — OSF presubmission, validation protocols, governance
- `context/` — Evidence registers, assumptions, decision log, data provenance, bibliography
- `conductor/` — Conductor extension tracks for project management
- `docs/` — Documentation, runbooks, quality checklists

### Code and configuration
- `src/` — Modelling modules and glue code
- `scripts/` — Runnable entry points
- `configs/` — YAML configuration for policies, priors, and run settings
- `tests/` — Unit and integration tests

### Outputs (not committed by default)
- `outputs/` — Versioned run outputs, posterior samples, publish packs

---

## Quick start (local)

1. **Create an environment** (recommended: uv, conda, or venv)
2. **Install dependencies** listed in `pyproject.toml`
3. **Run** `python -m scripts.run_policy_sweep`

Notes:
- This scaffold assumes CPU execution by default. GPU is optional.
- JAX requires `jaxlib` appropriate to your platform.

---

## Reproducibility

- Deterministic seeds mandatory
- Policy contrasts use common random numbers for variance reduction
- Each run writes immutable manifest (config + git hash + timestamp)
- Data provenance tracked (`context/data_provenance_template.md`)
- Evidence quality graded (`context/evidence_grading_rubric.md`)

---

## Research quality

Before releasing outputs, see:
- **Quality checklist:** `docs/RESEARCH_QUALITY_CHECKLIST.md`
- **Validation protocol:** `protocols/model_validation_protocol.md`
- **Decision log:** `context/decision_log.md`

---

## Jurisdictions

- **Australia:** `configs/policies_australia.yaml` (run with `--jurisdiction australia`)
- **New Zealand:** `configs/policies_new_zealand.yaml` (run with `--jurisdiction new_zealand`)

Evidence registers: `context/jurisdiction_profiles/`

---

## Key scripts

| Script | Purpose |
|--------|---------|
| `run_meta_pipeline.py` | Orchestrate AU + NZ comparison |
| `run_full_uncertainty.py` | Full probabilistic sensitivity analysis |
| `run_voi.py` | Compute EVPI/EVPPI |
| `run_policy_sweep.py` | Compare policy scenarios |
| `publish_pack.py` | Generate publication-ready outputs |

See `docs/RUNBOOK.md` for full documentation.

---

## Conductor workflow

This repo uses the Conductor extension for Gemini CLI to manage tracks.

- **Install:** `gemini extensions install https://github.com/gemini-cli-extensions/conductor --auto-update`
- **Project index:** `conductor/index.md`
- **Tracks registry:** `conductor/tracks.md`
- **Current track:** `gdpe_0002_evidence_anchoring`

---

## Related documentation

- `docs/CONTEXT_ENGINEERING.md` — Assumption tracking and experiment cards
- `docs/GAME_THEORETIC_FRAMING.md` — Strategic interaction modelling
- `docs/META_PIPELINE.md` — Multi-jurisdiction comparison workflow
- `docs/PUBLISH_PACK.md` — Output generation for policy briefs
- `docs/RESEARCH_QUALITY_CHECKLIST.md` — Pre-release checklist


## VOI
Run `python -m scripts.run_voi` to compute EVPI/EVPPI on a toy net benefit definition (replace with DCBA/welfare net benefit).


## Jurisdictions
- Australia: `configs/policies_australia.yaml` (run with `--jurisdiction australia`)
- New Zealand: `configs/policies_new_zealand.yaml` (run with `--jurisdiction new_zealand`)


## Posterior conversion
- `python -m scripts.convert_posterior_csv_to_npy --csv <file.csv> --kind behavior --out outputs/posterior_samples/behavior_posterior.npy`

## Joint sampling control
`run_full_uncertainty` supports `--sampling_mode independent|common_index|random`.

## Uncertainty decomposition
- `python -m scripts.run_uncertainty_decomposition --run_dir <full_uncertainty_run_dir>`

## Build joint draws (optional)
- `python -m scripts.build_joint_draws --out outputs/posterior_samples/joint_draws.npy --n_draws 1000 --mapping ... --behavior ... --mode common_index`


## Full uncertainty from joint draws
- `python -m scripts.run_full_uncertainty_from_joint --jurisdiction australia --joint_draws outputs/posterior_samples/joint_draws.npy --n_draws 500`
See `docs/JOINT_DRAWS.md`.


## Total-order sensitivity (approx)
- `python -m scripts.run_uncertainty_decomposition_total --run_dir <full_uncertainty_run_dir>`
See `docs/TOTAL_ORDER_SENSITIVITY.md`.


## Meta pipeline (AU + NZ)
- `python -m scripts.run_meta_pipeline --n_draws 500` (see `docs/META_PIPELINE.md`)


## Publish pack
- `python -m scripts.publish_pack --meta_dir outputs/runs/meta_pipeline/<timestamp>` (see `docs/PUBLISH_PACK.md`)


## Game-theoretic framing
See `docs/GAME_THEORETIC_FRAMING.md` for the strategic interaction mapping and modelling rationale.


## Conductor workflow
This repo includes a `conductor/` directory compatible with the Conductor extension for Gemini CLI.
- Install: `gemini extensions install https://github.com/gemini-cli-extensions/conductor --auto-update`
- Project index: `conductor/index.md`
- Tracks registry: `conductor/tracks.md`
