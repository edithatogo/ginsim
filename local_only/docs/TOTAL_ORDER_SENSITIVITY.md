# Total-order sensitivity (interaction-aware)

This repo includes a pragmatic total-order sensitivity measure, estimated via a surrogate:

- First-order index: S1_g = Var(E[Y|Θ_g]) / Var(Y)
- Total-order index: ST_g = 1 - Var(E[Y|X_-g]) / Var(Y)

where X_-g is the complement of group g (all other parameter groups concatenated).

## Why this approach
A classical pick–freeze Sobol design requires generating hybrid samples.
In many policy models, we have posterior draws rather than a generative sampler for Θ, so we use a surrogate
to estimate conditional expectations directly.

## Run
1) Run `run_full_uncertainty` to generate `net_benefit_matrix.npy` and `theta_*.npy`.
2) Then:
```bash
python -m scripts.run_uncertainty_decomposition_total --run_dir <run_dir>
```

Outputs:
- `sobol_first_and_total_by_group.csv`
- `report.txt`

## Interpretation
- S1 captures main effects (group alone).
- ST captures total effect (main + interactions), approximated by the complement surrogate.
