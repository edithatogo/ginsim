# Meta pipeline (AU + NZ end-to-end)

This repo includes an orchestrator that runs, for both Australia and Aotearoa New Zealand:

1) Full uncertainty propagation (saving net benefit matrix + theta matrices)
2) First-order decomposition (S1)
3) Total-order decomposition (ST approx)
4) EVPPI by group (from theta matrices)
5) Produces AU/NZ comparison tables and a short markdown report

## Run
### Option A: Use joint draws
```bash
python -m scripts.run_meta_pipeline --use_joint --joint_draws outputs/posterior_samples/joint_draws.npy --n_draws 500
```

### Option B: Use separate posterior files
```bash
python -m scripts.run_meta_pipeline --n_draws 500 \
  --mapping_posterior outputs/posterior_samples/policy_mapping_posterior.npy \
  --behavior_posterior outputs/posterior_samples/behavior_posterior.npy \
  --clinical_posterior outputs/posterior_samples/clinical_posterior.npy \
  --insurance_posterior outputs/posterior_samples/insurance_posterior.npy
```

Outputs go under `outputs/runs/meta_pipeline/<timestamp>/`.
Key comparison artefacts are in `.../compare/`.
