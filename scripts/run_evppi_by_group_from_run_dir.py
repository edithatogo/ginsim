from __future__ import annotations

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
    from src.model.evppi_rff import evppi_rff
except ImportError:
    logger.warning("src.model.evppi_rff.evppi_rff not found. Using None.")
    evppi_rff = None

from src.model.voi import evpi
from src.utils.logging_config import setup_logging
from src.utils.manifest import write_manifest

setup_logging(level="INFO")

GROUPS = ["mapping", "behavior", "clinical", "insurance", "passthrough", "data_quality"]


def load_theta(run_dir: Path, name: str):
    p = run_dir / f"theta_{name}.npy"
    if p.exists():
        return np.load(p)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run_dir",
        required=True,
        help="Directory containing net_benefit_matrix.npy and theta_*.npy",
    )
    parser.add_argument("--out", default="outputs/runs/evppi_groups_from_run")
    parser.add_argument("--seed", type=int, default=20260302)
    parser.add_argument("--n_features", type=int, default=256)
    parser.add_argument("--lengthscale", type=float, default=1.0)
    parser.add_argument("--l2", type=float, default=1e-2)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    nb_path = run_dir / "net_benefit_matrix.npy"
    if not nb_path.exists():
        message = f"Missing {nb_path}"
        raise FileNotFoundError(message)

    nb = np.load(nb_path)  # [S,P]
    nb_j = jnp.array(nb)

    key = jax.random.PRNGKey(args.seed)
    evpi_val = float(evpi(nb_j))

    rows = []
    if evppi_rff is None:
        logger.error("evppi_rff is missing. Skipping EVPPI calculation.")
    else:
        for g in GROUPS:
            theta = load_theta(run_dir, g)
            if theta is None:
                continue
            theta_j = jnp.array(theta)
            k = jax.random.fold_in(key, hash(g) & 0xFFFFFFFF)
            val = float(
                evppi_rff(
                    nb_j,
                    theta_j,
                    k,
                    n_features=args.n_features,
                    lengthscale=args.lengthscale,
                    l2=args.l2,
                ),
            )
            rows.append({"group": g, "evppi": val})

    df = (
        pd.DataFrame(rows).sort_values("evppi", ascending=False)
        if rows
        else pd.DataFrame(columns=["group", "evppi"])
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
            notes="EVPPI by group computed from run_dir theta matrices via RFF surrogate.",
            extra={"run_dir": str(run_dir), "evpi": evpi_val},
        )

    df.to_csv(out_dir / "evppi_by_group.csv", index=False)
    (out_dir / "report.txt").write_text(
        f"EVPI: {evpi_val:.6f}\n"
        + "\n".join([f"{r['group']}: {r['evppi']:.6f}" for r in rows])
        + "\n",
        encoding="utf-8",
    )

    logger.info(f"Wrote evppi results to: {out_dir}")
    logger.info(f"\n{df.to_string(index=False)}")


if __name__ == "__main__":
    main()
