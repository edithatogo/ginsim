# Joint posterior draws

If you have posterior draws for multiple parameter groups (mapping, behaviour, clinical, insurance, etc.),
you can package them into a single file for portability and explicit correlation control.

## Build joint draws
```bash
python -m scripts.build_joint_draws   --out outputs/posterior_samples/joint_draws.npy   --n_draws 1000   --mapping outputs/posterior_samples/policy_mapping_posterior.npy   --behavior outputs/posterior_samples/behavior_posterior.npy   --clinical outputs/posterior_samples/clinical_posterior.npy   --insurance outputs/posterior_samples/insurance_posterior.npy   --mode common_index
```

## Run full uncertainty from joint draws
```bash
python -m scripts.run_full_uncertainty_from_joint   --jurisdiction australia   --joint_draws outputs/posterior_samples/joint_draws.npy   --n_draws 500
```

Outputs include the usual run folder with:
- `full_uncertainty_draws.csv`
- `net_benefit_matrix.npy`
- `theta_*.npy` (where the joint file includes that group)
