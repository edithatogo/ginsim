# ruff: noqa: I001,TC003
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    import jax
    import jax.numpy as jnp
    from src.model.evppi_rff import evppi_rff
    from src.model.sensitivity import sobol_first_order_rff
    from src.model.sensitivity_total import total_order_sobol_rff
    from src.model.voi import evpi
except ModuleNotFoundError as exc:  # pragma: no cover - optional dependency surface
    allowed_missing = {
        "jax",
        "jax.numpy",
        "src.model.evppi_rff",
        "src.model.sensitivity",
        "src.model.sensitivity_total",
        "src.model.voi",
    }
    if exc.name not in allowed_missing:
        raise
    jax = None
    jnp = None
    evppi_rff = None
    sobol_first_order_rff = None
    total_order_sobol_rff = None
    evpi = None

GROUPS = ["mapping", "behavior", "clinical", "insurance", "passthrough", "data_quality"]


def latest_run_dir(full_uncertainty_dir: Path, prefix: str) -> Path | None:
    """Return the newest run directory matching a jurisdiction prefix."""
    if not full_uncertainty_dir.exists():
        return None

    candidates = [
        path
        for path in full_uncertainty_dir.iterdir()
        if path.is_dir() and path.name.startswith(prefix)
    ]
    if not candidates:
        return None

    candidates.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return candidates[0]


def maybe_load_manifest(run_dir: Path) -> dict[str, Any]:
    """Load a run manifest when one exists."""
    manifest_path = run_dir / "run_manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {}


def describe_run_source(run_dir: Path) -> dict[str, Any]:
    """Build a path-safe public description of a source run."""
    manifest = maybe_load_manifest(run_dir)
    return {
        "run_id": run_dir.name,
        "created_utc": manifest.get("created_utc"),
        "repo_tree_hash": manifest.get("repo_tree_hash"),
        "policies_file": manifest.get("policies_file"),
        "policies_file_sha256": manifest.get("policies_file_sha256"),
        "base_config_file_sha256": manifest.get("base_config_file_sha256"),
    }


def infer_jurisdiction(run_dir: Path) -> str:
    """Infer jurisdiction from the manifest or directory name."""
    manifest = maybe_load_manifest(run_dir)
    jurisdiction = manifest.get("jurisdiction")
    if isinstance(jurisdiction, str) and jurisdiction:
        return jurisdiction

    name = run_dir.name.lower()
    if name.startswith("australia_"):
        return "australia"
    if name.startswith("new_zealand_"):
        return "new_zealand"
    if name.startswith("nz_"):
        return "new_zealand"
    if name.startswith("au_"):
        return "australia"
    return name


def resolve_run_dirs(
    *,
    meta_dir: Path | None = None,
    run_dir: Path | None = None,
) -> dict[str, Path]:
    """Resolve reporting inputs to a jurisdiction-keyed run directory mapping."""
    if meta_dir is not None:
        full_uncertainty_dir = meta_dir / "full_uncertainty"
        run_dirs = {
            "australia": latest_run_dir(full_uncertainty_dir, "australia_"),
            "new_zealand": latest_run_dir(full_uncertainty_dir, "new_zealand_"),
        }
        resolved = {
            jurisdiction: path for jurisdiction, path in run_dirs.items() if path is not None
        }
        if not resolved:
            message = f"Could not locate jurisdiction run directories under {full_uncertainty_dir}"
            raise FileNotFoundError(message)
        return resolved

    if run_dir is not None:
        return {infer_jurisdiction(run_dir): run_dir}

    message = "Either meta_dir or run_dir must be provided"
    raise ValueError(message)


def load_draws_summary(run_dir: Path) -> pd.DataFrame:
    """Summarize per-policy uncertainty draws from a run directory."""
    draws_path = run_dir / "full_uncertainty_draws.csv"
    if not draws_path.exists():
        raise FileNotFoundError(draws_path)

    df = pd.read_csv(draws_path)
    for column in ["policy", "nb"]:
        if column not in df.columns:
            message = f"Expected column '{column}' in {draws_path}"
            raise ValueError(message)

    if "net_qalys" not in df.columns:
        df["net_qalys"] = np.nan
    if "avg_premium" not in df.columns:
        df["avg_premium"] = np.nan

    def quantile(series: pd.Series, probability: float) -> float:
        cleaned = series.dropna()
        if cleaned.empty:
            return float("nan")
        return float(np.quantile(cleaned, probability))

    return (
        df.groupby("policy")
        .agg(
            nb_mean=("nb", "mean"),
            nb_p05=("nb", lambda series: quantile(series, 0.05)),
            nb_p95=("nb", lambda series: quantile(series, 0.95)),
            qaly_mean=("net_qalys", "mean"),
            qaly_p05=("net_qalys", lambda series: quantile(series, 0.05)),
            qaly_p95=("net_qalys", lambda series: quantile(series, 0.95)),
            prem_mean=("avg_premium", "mean"),
            prem_p05=("avg_premium", lambda series: quantile(series, 0.05)),
            prem_p95=("avg_premium", lambda series: quantile(series, 0.95)),
        )
        .reset_index()
        .sort_values("nb_mean", ascending=False)
    )


def compute_uncertainty_tables(
    run_dir: Path, seed: int = 20260302
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute EVPPI and uncertainty decomposition tables when theta matrices exist."""
    if (
        jax is None
        or jnp is None
        or evppi_rff is None
        or sobol_first_order_rff is None
        or total_order_sobol_rff is None
        or evpi is None
    ):
        return (
            pd.DataFrame(columns=["group", "evppi", "evpi"]),
            pd.DataFrame(
                columns=[
                    "group",
                    "S1_optimal_NB",
                    "ST_optimal_NB",
                    "S1_avg_policy_NB",
                    "ST_avg_policy_NB",
                ]
            ),
        )

    nb_path = run_dir / "net_benefit_matrix.npy"
    if not nb_path.exists():
        return (
            pd.DataFrame(columns=["group", "evppi", "evpi"]),
            pd.DataFrame(
                columns=[
                    "group",
                    "S1_optimal_NB",
                    "ST_optimal_NB",
                    "S1_avg_policy_NB",
                    "ST_avg_policy_NB",
                ]
            ),
        )

    theta = {}
    for group in GROUPS:
        theta_path = run_dir / f"theta_{group}.npy"
        if theta_path.exists():
            theta[group] = theta_path

    if not theta:
        return (
            pd.DataFrame(columns=["group", "evppi", "evpi"]),
            pd.DataFrame(
                columns=[
                    "group",
                    "S1_optimal_NB",
                    "ST_optimal_NB",
                    "S1_avg_policy_NB",
                    "ST_avg_policy_NB",
                ]
            ),
        )

    nb = np.load(nb_path)
    nb_j = jnp.array(nb)
    nb_opt = jnp.max(nb_j, axis=1)
    key = jax.random.PRNGKey(seed)
    evpi_value = float(evpi(nb_j))

    evppi_rows: list[dict[str, float | str]] = []
    decomposition_rows: list[dict[str, float | str]] = []

    def concat_complement(exclude: str):
        complements = [
            jnp.array(np.load(path)) for group, path in theta.items() if group != exclude
        ]
        if not complements:
            return None
        return jnp.concatenate(complements, axis=1)

    for group, theta_path in theta.items():
        theta_matrix = jnp.array(np.load(theta_path))
        evppi_key = jax.random.fold_in(key, hash(group) & 0xFFFFFFFF)
        evppi_rows.append(
            {
                "group": group,
                "evppi": float(
                    evppi_rff(
                        nb_j,
                        theta_matrix,
                        evppi_key,
                        n_features=256,
                        lengthscale=1.0,
                        l2=1e-2,
                    )
                ),
                "evpi": evpi_value,
            }
        )

        complement = concat_complement(group)
        if complement is None:
            continue

        s1_opt_key = jax.random.fold_in(key, (hash(group) + 1) & 0xFFFFFFFF)
        st_opt_key = jax.random.fold_in(key, (hash(group) + 2) & 0xFFFFFFFF)
        s1_avg_key = jax.random.fold_in(key, (hash(group) + 3) & 0xFFFFFFFF)
        st_avg_key = jax.random.fold_in(key, (hash(group) + 4) & 0xFFFFFFFF)

        s1_average = sobol_first_order_rff(nb_j, theta_matrix, s1_avg_key)
        st_average = total_order_sobol_rff(nb_j, complement, st_avg_key)

        decomposition_rows.append(
            {
                "group": group,
                "S1_optimal_NB": float(sobol_first_order_rff(nb_opt, theta_matrix, s1_opt_key)),
                "ST_optimal_NB": float(total_order_sobol_rff(nb_opt, complement, st_opt_key)),
                "S1_avg_policy_NB": float(jnp.mean(s1_average)),
                "ST_avg_policy_NB": float(jnp.mean(st_average)),
            }
        )

    evppi_df = (
        pd.DataFrame(evppi_rows).sort_values("evppi", ascending=False)
        if evppi_rows
        else pd.DataFrame(columns=["group", "evppi", "evpi"])
    )
    decomposition_df = (
        pd.DataFrame(decomposition_rows).sort_values("ST_optimal_NB", ascending=False)
        if decomposition_rows
        else pd.DataFrame(
            columns=[
                "group",
                "S1_optimal_NB",
                "ST_optimal_NB",
                "S1_avg_policy_NB",
                "ST_avg_policy_NB",
            ]
        )
    )
    return evppi_df, decomposition_df


def build_reporting_bundle(
    *,
    meta_dir: Path | None = None,
    run_dir: Path | None = None,
) -> dict[str, Any]:
    """Build a coherent reporting bundle from one meta run or one jurisdiction run."""
    run_dirs = resolve_run_dirs(meta_dir=meta_dir, run_dir=run_dir)

    summaries: list[pd.DataFrame] = []
    evppi_tables: list[pd.DataFrame] = []
    decomposition_tables: list[pd.DataFrame] = []
    manifests: dict[str, dict[str, Any]] = {}

    for jurisdiction, jurisdiction_run_dir in run_dirs.items():
        manifest = maybe_load_manifest(jurisdiction_run_dir)
        manifests[jurisdiction] = manifest

        summary = load_draws_summary(jurisdiction_run_dir).copy()
        summary.insert(0, "jurisdiction", jurisdiction)
        summaries.append(summary)

        evppi_df, decomposition_df = compute_uncertainty_tables(jurisdiction_run_dir)
        if not evppi_df.empty:
            evppi_df = evppi_df.copy()
            evppi_df.insert(0, "jurisdiction", jurisdiction)
            evppi_tables.append(evppi_df)
        if not decomposition_df.empty:
            decomposition_df = decomposition_df.copy()
            decomposition_df.insert(0, "jurisdiction", jurisdiction)
            decomposition_tables.append(decomposition_df)

    policy_summary = pd.concat(summaries, ignore_index=True).sort_values(
        ["jurisdiction", "nb_mean"],
        ascending=[True, False],
    )
    evppi_by_group = (
        pd.concat(evppi_tables, ignore_index=True).sort_values(
            ["jurisdiction", "evppi"],
            ascending=[True, False],
        )
        if evppi_tables
        else pd.DataFrame(columns=["jurisdiction", "group", "evppi", "evpi"])
    )
    uncertainty_decomposition = (
        pd.concat(decomposition_tables, ignore_index=True).sort_values(
            ["jurisdiction", "ST_optimal_NB"],
            ascending=[True, False],
        )
        if decomposition_tables
        else pd.DataFrame(
            columns=[
                "jurisdiction",
                "group",
                "S1_optimal_NB",
                "ST_optimal_NB",
                "S1_avg_policy_NB",
                "ST_avg_policy_NB",
            ]
        )
    )

    return {
        "run_dirs": run_dirs,
        "manifests": manifests,
        "policy_summary": policy_summary,
        "evppi_by_group": evppi_by_group,
        "uncertainty_decomposition": uncertainty_decomposition,
    }


def write_reporting_tables(output_dir: Path, bundle: dict[str, Any]) -> dict[str, Path]:
    """Write reporting tables and a compact manifest to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)

    generated: dict[str, Path] = {}
    policy_summary = bundle["policy_summary"]
    evppi_by_group = bundle["evppi_by_group"]
    uncertainty_decomposition = bundle["uncertainty_decomposition"]

    policy_summary_path = output_dir / "policy_summary.csv"
    policy_summary.to_csv(policy_summary_path, index=False)
    generated["policy_summary"] = policy_summary_path

    if not evppi_by_group.empty:
        evppi_path = output_dir / "evppi_by_group.csv"
        evppi_by_group.to_csv(evppi_path, index=False)
        generated["evppi_by_group"] = evppi_path

    if not uncertainty_decomposition.empty:
        decomposition_path = output_dir / "uncertainty_decomposition.csv"
        uncertainty_decomposition.to_csv(decomposition_path, index=False)
        generated["uncertainty_decomposition"] = decomposition_path

    for jurisdiction in policy_summary["jurisdiction"].unique():
        jurisdiction_policy = policy_summary.loc[
            policy_summary["jurisdiction"] == jurisdiction
        ].drop(columns=["jurisdiction"])
        jurisdiction_policy_path = output_dir / f"{jurisdiction}_policy_summary.csv"
        jurisdiction_policy.to_csv(jurisdiction_policy_path, index=False)
        generated[f"{jurisdiction}_policy_summary"] = jurisdiction_policy_path

        if not evppi_by_group.empty:
            jurisdiction_evppi = evppi_by_group.loc[
                evppi_by_group["jurisdiction"] == jurisdiction
            ].drop(columns=["jurisdiction"])
            if not jurisdiction_evppi.empty:
                jurisdiction_evppi_path = output_dir / f"{jurisdiction}_evppi_by_group.csv"
                jurisdiction_evppi.to_csv(jurisdiction_evppi_path, index=False)
                generated[f"{jurisdiction}_evppi_by_group"] = jurisdiction_evppi_path

        if not uncertainty_decomposition.empty:
            jurisdiction_decomposition = uncertainty_decomposition.loc[
                uncertainty_decomposition["jurisdiction"] == jurisdiction
            ].drop(columns=["jurisdiction"])
            if not jurisdiction_decomposition.empty:
                jurisdiction_decomposition_path = (
                    output_dir / f"{jurisdiction}_uncertainty_decomposition.csv"
                )
                jurisdiction_decomposition.to_csv(
                    jurisdiction_decomposition_path,
                    index=False,
                )
                generated[f"{jurisdiction}_uncertainty_decomposition"] = (
                    jurisdiction_decomposition_path
                )

    reporting_manifest = {
        "source_runs": {
            jurisdiction: describe_run_source(path)
            for jurisdiction, path in bundle["run_dirs"].items()
        },
        "generated_files": {name: path.name for name, path in generated.items()},
    }
    manifest_path = output_dir / "reporting_manifest.json"
    manifest_path.write_text(
        json.dumps(reporting_manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    generated["reporting_manifest"] = manifest_path
    return generated
