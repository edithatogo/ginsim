# Uncertainty decomposition

This repo supports a decision-focused sensitivity analysis using first-order Sobol indices:

S1 = Var(E[Y | Θ_g]) / Var(Y)

where Θ_g is a group of uncertain parameters (e.g., mapping, behaviour, clinical).

We approximate E[Y|Θ_g] using a Random Fourier Features (RFF) ridge surrogate (fast and scalable).

## Workflow
1) Run full uncertainty (saves `net_benefit_matrix.npy` and `theta_*.npy`):
```bash
python -m scripts.run_full_uncertainty --jurisdiction australia --n_draws 500
```

2) Run decomposition:
```bash
python -m scripts.run_uncertainty_decomposition --run_dir <run_output_dir>
```

Outputs:
- `sobol_first_order_by_group.csv`
- `report.txt`
