from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
from pathlib import Path

import pandas as pd


def run(cmd: list[str]) -> None:
    print("\n$ " + " ".join(cmd))
    subprocess.check_call(cmd)


def newest_subdir(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(path)
    subs = [p for p in path.iterdir() if p.is_dir()]
    if not subs:
        raise FileNotFoundError(f"No subdirectories under {path}")
    subs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return subs[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_draws", type=int, default=500)
    parser.add_argument("--out", default="outputs/runs/meta_pipeline")
    parser.add_argument(
        "--use_joint",
        action="store_true",
        help="Use joint_draws.npy with run_full_uncertainty_from_joint",
    )
    parser.add_argument("--joint_draws", default="outputs/posterior_samples/joint_draws.npy")
    # If not joint, these are passed to run_full_uncertainty
    parser.add_argument(
        "--mapping_posterior", default="outputs/posterior_samples/policy_mapping_posterior.npy"
    )
    parser.add_argument("--behavior_posterior", default="")
    parser.add_argument("--clinical_posterior", default="")
    parser.add_argument("--insurance_posterior", default="")
    parser.add_argument("--passthrough_posterior", default="")
    parser.add_argument("--data_quality_posterior", default="")
    parser.add_argument(
        "--sampling_mode", default="independent", choices=["independent", "common_index", "random"]
    )
    args = parser.parse_args()

    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    base_out = Path(args.out) / ts
    base_out.mkdir(parents=True, exist_ok=True)

    # Paths to stage outputs
    full_out = base_out / "full_uncertainty"
    s1_out = base_out / "decomp_s1"
    st_out = base_out / "decomp_total"
    evppi_out = base_out / "evppi_by_group"
    compare_out = base_out / "compare"

    full_out.mkdir(exist_ok=True)
    s1_out.mkdir(exist_ok=True)
    st_out.mkdir(exist_ok=True)
    evppi_out.mkdir(exist_ok=True)
    compare_out.mkdir(exist_ok=True)

    jurisdictions = ["australia", "new_zealand"]
    run_dirs: dict[str, Path] = {}

    for j in jurisdictions:
        if args.use_joint:
            run(
                [
                    sys.executable,
                    "-m",
                    "scripts.run_full_uncertainty_from_joint",
                    "--jurisdiction",
                    j,
                    "--joint_draws",
                    args.joint_draws,
                    "--n_draws",
                    str(args.n_draws),
                    "--out",
                    str(full_out),
                ]
            )
        else:
            cmd = [
                sys.executable,
                "-m",
                "scripts.run_full_uncertainty",
                "--jurisdiction",
                j,
                "--n_draws",
                str(args.n_draws),
                "--sampling_mode",
                args.sampling_mode,
                "--out",
                str(full_out),
                "--mapping_posterior",
                args.mapping_posterior,
                "--behavior_posterior",
                args.behavior_posterior,
                "--clinical_posterior",
                args.clinical_posterior,
                "--insurance_posterior",
                args.insurance_posterior,
                "--passthrough_posterior",
                args.passthrough_posterior,
                "--data_quality_posterior",
                args.data_quality_posterior,
            ]
            run(cmd)

        run_dir = newest_subdir(full_out)  # last run for this jurisdiction
        run_dirs[j] = run_dir

        # Decomposition S1
        run(
            [
                sys.executable,
                "-m",
                "scripts.run_uncertainty_decomposition",
                "--run_dir",
                str(run_dir),
                "--out",
                str(s1_out),
            ]
        )
        # Decomposition total order
        run(
            [
                sys.executable,
                "-m",
                "scripts.run_uncertainty_decomposition_total",
                "--run_dir",
                str(run_dir),
                "--out",
                str(st_out),
            ]
        )
        # EVPPI by group from theta matrices
        run(
            [
                sys.executable,
                "-m",
                "scripts.run_evppi_by_group_from_run_dir",
                "--run_dir",
                str(run_dir),
                "--out",
                str(evppi_out),
            ]
        )

    # Build comparison tables
    summaries = []
    for j, rd in run_dirs.items():
        summ = pd.read_csv(rd / "full_uncertainty_summary.csv")
        summ.insert(0, "jurisdiction", j)
        summaries.append(summ)
    df_summary = pd.concat(summaries, ignore_index=True)
    df_summary.to_csv(compare_out / "au_nz_policy_summary.csv", index=False)

    # Collect decomposition tables (most recent under each out folder corresponds to last run; load all)
    def collect_latest(folder: Path, pattern: str, label: str):
        subs = [p for p in folder.iterdir() if p.is_dir()]
        subs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        frames = []
        for p in subs[: len(jurisdictions) * 2]:  # just a small cap
            f = p / pattern
            if f.exists():
                d = pd.read_csv(f)
                d.insert(0, "source_run", str(p))
                d.insert(0, "kind", label)
                frames.append(d)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    s1_df = collect_latest(s1_out, "sobol_first_order_by_group.csv", "S1")
    st_df = collect_latest(st_out, "sobol_first_and_total_by_group.csv", "S1_ST")
    ev_df = collect_latest(evppi_out, "evppi_by_group.csv", "EVPPI")

    if not s1_df.empty:
        s1_df.to_csv(compare_out / "decomposition_s1_collected.csv", index=False)
    if not st_df.empty:
        st_df.to_csv(compare_out / "decomposition_total_collected.csv", index=False)
    if not ev_df.empty:
        ev_df.to_csv(compare_out / "evppi_by_group_collected.csv", index=False)

    # Write a simple markdown report
    top = (
        df_summary.sort_values(["jurisdiction", "nb_mean"], ascending=[True, False])
        .groupby("jurisdiction")
        .head(3)
    )
    report = []
    report.append(f"# Meta pipeline report ({ts})\n")
    report.append("## Top policies by mean net benefit (ledger)\n")
    report.append(top.to_markdown(index=False))
    report.append("\n\n## Outputs\n")
    report.append(f"- Full uncertainty runs: `{full_out}`")
    report.append(f"- S1 decomposition: `{s1_out}`")
    report.append(f"- Total-order decomposition: `{st_out}`")
    report.append(f"- EVPPI by group: `{evppi_out}`")
    report.append(f"- Comparison tables: `{compare_out}`\n")
    (compare_out / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print("\nWrote meta outputs to:", base_out)


if __name__ == "__main__":
    main()
