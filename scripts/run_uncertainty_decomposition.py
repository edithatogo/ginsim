import argparse
import sys
from contextlib import suppress
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

try:
    from src.model.sensitivity import sobol_first_order_rff
except ImportError:
    logger.warning("src.model.sensitivity.sobol_first_order_rff not found. Using None.")
    sobol_first_order_rff = None

from src.utils.logging_config import setup_logging
from src.utils.manifest import write_manifest

setup_logging(level="INFO")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_dir", required=True)
    parser.add_argument("--out", default="outputs/runs/uncertainty_decomposition")
    parser.add_argument("--seed", type=int, default=20260302)
    parser.add_argument("--n_features", type=int, default=256)
    parser.add_argument("--lengthscale", type=float, default=1.0)
    parser.add_argument("--l2", type=float, default=1e-2)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    nb_path = run_dir / "net_benefit_matrix.npy"
    nb = np.load(nb_path)
    nb_j = jnp.array(nb)
    nb_opt = jnp.max(nb_j, axis=1)

    key = jax.random.PRNGKey(args.seed)

    groups = []
    for name in ["mapping", "behavior", "clinical", "insurance", "passthrough", "data_quality"]:
        p = run_dir / f"theta_{name}.npy"
        if p.exists():
            groups.append((name, jnp.array(np.load(p))))

    rows = []
    if sobol_first_order_rff is None:
        logger.error("sobol_first_order_rff is missing. Skipping decomposition calculation.")
    else:
        for name, theta in groups:
            k1 = jax.random.fold_in(key, hash(name) & 0xFFFFFFFF)
            s1_opt = float(
                sobol_first_order_rff(
                    nb_opt,
                    theta,
                    k1,
                    n_features=args.n_features,
                    lengthscale=args.lengthscale,
                    l2=args.l2,
                ),
            )

            k2 = jax.random.fold_in(key, (hash(name) + 1) & 0xFFFFFFFF)
            s1_per_policy = sobol_first_order_rff(
                nb_j,
                theta,
                k2,
                n_features=args.n_features,
                lengthscale=args.lengthscale,
                l2=args.l2,
            )
            s1_avg = float(jnp.mean(s1_per_policy))

            rows.append({"group": name, "S1_optimal_NB": s1_opt, "S1_avg_policy_NB": s1_avg})

    df = (
        pd.DataFrame(rows).sort_values("S1_optimal_NB", ascending=False)
        if rows
        else pd.DataFrame(columns=["group", "S1_optimal_NB", "S1_avg_policy_NB"])
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
            notes="Uncertainty decomposition: first-order Sobol indices via RFF surrogate.",
            extra={"run_dir": str(run_dir)},
        )

    df.to_csv(out_dir / "sobol_first_order_by_group.csv", index=False)
    (out_dir / "report.txt").write_text(df.to_string(index=False) + "\n", encoding="utf-8")

    logger.info(f"Wrote uncertainty results to: {out_dir}")
    logger.info(f"\n{df.to_string(index=False)}")


if __name__ == "__main__":
    main()
