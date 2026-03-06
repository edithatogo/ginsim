from __future__ import annotations

import argparse
from contextlib import suppress
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np
import pandas as pd
from src.utils.manifest import write_manifest

from src.model.sensitivity import sobol_first_order_rff
from src.model.sensitivity_total import total_order_sobol_rff

GROUPS = ["mapping", "behavior", "clinical", "insurance", "passthrough", "data_quality"]


def load_theta(run_dir: Path, name: str):
    p = run_dir / f"theta_{name}.npy"
    if p.exists():
        return np.load(p)
    return None


def concat_complement(run_dir: Path, exclude: str) -> np.ndarray | None:
    mats = []
    for g in GROUPS:
        if g == exclude:
            continue
        m = load_theta(run_dir, g)
        if m is not None:
            mats.append(m)
    if not mats:
        return None
    # Ensure same number of rows
    n = mats[0].shape[0]
    mats = [m for m in mats if m.shape[0] == n]
    if not mats:
        return None
    return np.concatenate(mats, axis=1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_dir", required=True)
    parser.add_argument("--out", default="outputs/runs/uncertainty_decomposition_total")
    parser.add_argument("--seed", type=int, default=20260302)
    parser.add_argument("--n_features", type=int, default=256)
    parser.add_argument("--lengthscale", type=float, default=1.0)
    parser.add_argument("--l2", type=float, default=1e-2)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    nb = np.load(run_dir / "net_benefit_matrix.npy")  # [S,P]
    nb_j = jnp.array(nb)
    nb_opt = jnp.max(nb_j, axis=1)

    key = jax.random.PRNGKey(args.seed)

    rows = []
    for g in GROUPS:
        theta_g = load_theta(run_dir, g)
        if theta_g is None:
            continue
        theta_g_j = jnp.array(theta_g)

        comp = concat_complement(run_dir, g)
        if comp is None:
            continue
        comp_j = jnp.array(comp)

        # First-order and total-order for decision-focused output (optimal NB)
        k1 = jax.random.fold_in(key, hash(g) & 0xFFFFFFFF)
        s1_opt = float(
            sobol_first_order_rff(
                nb_opt,
                theta_g_j,
                k1,
                n_features=args.n_features,
                lengthscale=args.lengthscale,
                l2=args.l2,
            ),
        )
        k2 = jax.random.fold_in(key, (hash(g) + 1) & 0xFFFFFFFF)
        st_opt = float(
            total_order_sobol_rff(
                nb_opt,
                comp_j,
                k2,
                n_features=args.n_features,
                lengthscale=args.lengthscale,
                l2=args.l2,
            ),
        )

        # For per-policy NB (average)
        k3 = jax.random.fold_in(key, (hash(g) + 2) & 0xFFFFFFFF)
        s1_pol = sobol_first_order_rff(
            nb_j,
            theta_g_j,
            k3,
            n_features=args.n_features,
            lengthscale=args.lengthscale,
            l2=args.l2,
        )
        s1_avg = float(jnp.mean(s1_pol))

        k4 = jax.random.fold_in(key, (hash(g) + 3) & 0xFFFFFFFF)
        st_pol = total_order_sobol_rff(
            nb_j,
            comp_j,
            k4,
            n_features=args.n_features,
            lengthscale=args.lengthscale,
            l2=args.l2,
        )
        st_avg = float(jnp.mean(st_pol))

        rows.append(
            {
                "group": g,
                "S1_optimal_NB": s1_opt,
                "ST_optimal_NB": st_opt,
                "S1_avg_policy_NB": s1_avg,
                "ST_avg_policy_NB": st_avg,
            },
        )

    df = (
        pd.DataFrame(rows).sort_values("ST_optimal_NB", ascending=False)
        if rows
        else pd.DataFrame(
            columns=[
                "group",
                "S1_optimal_NB",
                "ST_optimal_NB",
                "S1_avg_policy_NB",
                "ST_avg_policy_NB",
            ],
        )
    )

    out_dir = Path(args.out) / pd.Timestamp.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_dir.mkdir(parents=True, exist_ok=True)
    with suppress(Exception):
        write_manifest(
            out_dir,
            repo_root=Path(),
            jurisdiction="n/a",
            domain="n/a",
            policies_file=Path("configs/base.yaml"),
            base_config_file=Path("configs/base.yaml"),
            notes="First-order + total-order uncertainty decomposition via RFF surrogate.",
            extra={"run_dir": str(run_dir)},
        )

    df.to_csv(out_dir / "sobol_first_and_total_by_group.csv", index=False)
    (out_dir / "report.txt").write_text(df.to_string(index=False) + "\n", encoding="utf-8")

    print("Wrote:", out_dir)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
