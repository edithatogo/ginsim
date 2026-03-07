from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from scripts import generate_figures, publish_pack
from scripts.reporting_common import build_reporting_bundle, write_reporting_tables
from src.model.output_formatter import format_comparison_table, generate_policy_brief
from src.model.validation import run_ppc, save_ppc_results


def _write_run_fixture(parent: Path, jurisdiction: str) -> Path:
    run_dir = parent / f"{jurisdiction}_20260306T010203Z"
    run_dir.mkdir(parents=True, exist_ok=True)

    draws = pd.DataFrame(
        [
            {
                "policy": "status_quo",
                "nb": 100_000.0,
                "net_qalys": 10.0,
                "avg_premium": 1000.0,
            },
            {
                "policy": "status_quo",
                "nb": 110_000.0,
                "net_qalys": 11.0,
                "avg_premium": 1010.0,
            },
            {
                "policy": "moratorium",
                "nb": 150_000.0,
                "net_qalys": 13.0,
                "avg_premium": 1030.0,
            },
            {
                "policy": "moratorium",
                "nb": 160_000.0,
                "net_qalys": 14.0,
                "avg_premium": 1040.0,
            },
        ]
    )
    draws.to_csv(run_dir / "full_uncertainty_draws.csv", index=False)
    np.save(
        run_dir / "net_benefit_matrix.npy",
        np.array(
            [
                [100_000.0, 150_000.0],
                [110_000.0, 160_000.0],
            ]
        ),
    )
    np.save(
        run_dir / "theta_behavior.npy",
        np.array(
            [
                [0.1, 0.2, 0.3],
                [0.15, 0.25, 0.35],
            ]
        ),
    )
    np.save(
        run_dir / "theta_insurance.npy",
        np.array(
            [
                [0.4, 0.5],
                [0.45, 0.55],
            ]
        ),
    )
    (run_dir / "run_manifest.json").write_text(
        json.dumps(
            {
                "jurisdiction": jurisdiction,
                "created_utc": "2026-03-06T01:02:03Z",
                "repo_tree_hash": "abc123",
                "policies_file": f"configs/policies_{jurisdiction}.yaml",
                "policies_file_sha256": "policies-sha",
                "base_config_file_sha256": "base-sha",
            }
        ),
        encoding="utf-8",
    )
    return run_dir


def _write_meta_fixture(tmp_path: Path) -> Path:
    meta_dir = tmp_path / "meta_pipeline" / "20260306T010203Z"
    full_uncertainty = meta_dir / "full_uncertainty"
    _write_run_fixture(full_uncertainty, "australia")
    _write_run_fixture(full_uncertainty, "new_zealand")
    return meta_dir


def _synthetic_bundle(meta_dir: Path) -> dict[str, object]:
    return {
        "run_dirs": {
            "australia": meta_dir / "full_uncertainty" / "australia_20260306T010203Z",
            "new_zealand": meta_dir / "full_uncertainty" / "new_zealand_20260306T010203Z",
        },
        "manifests": {
            "australia": {"created_utc": "2026-03-06T01:02:03Z"},
            "new_zealand": {"created_utc": "2026-03-06T01:02:03Z"},
        },
        "policy_summary": pd.DataFrame(
            [
                {
                    "jurisdiction": "australia",
                    "policy": "moratorium",
                    "nb_mean": 155_000.0,
                    "nb_p05": 150_500.0,
                    "nb_p95": 159_500.0,
                    "qaly_mean": 13.5,
                    "qaly_p05": 13.05,
                    "qaly_p95": 13.95,
                    "prem_mean": 1035.0,
                    "prem_p05": 1030.5,
                    "prem_p95": 1039.5,
                },
                {
                    "jurisdiction": "new_zealand",
                    "policy": "moratorium",
                    "nb_mean": 155_000.0,
                    "nb_p05": 150_500.0,
                    "nb_p95": 159_500.0,
                    "qaly_mean": 13.5,
                    "qaly_p05": 13.05,
                    "qaly_p95": 13.95,
                    "prem_mean": 1035.0,
                    "prem_p05": 1030.5,
                    "prem_p95": 1039.5,
                },
            ]
        ),
        "evppi_by_group": pd.DataFrame(
            [
                {
                    "jurisdiction": "australia",
                    "group": "behavior",
                    "evppi": 12_345.0,
                    "evpi": 20_000.0,
                },
                {
                    "jurisdiction": "new_zealand",
                    "group": "behavior",
                    "evppi": 11_111.0,
                    "evpi": 19_000.0,
                },
            ]
        ),
        "uncertainty_decomposition": pd.DataFrame(
            [
                {
                    "jurisdiction": "australia",
                    "group": "behavior",
                    "S1_optimal_NB": 0.2,
                    "ST_optimal_NB": 0.4,
                    "S1_avg_policy_NB": 0.1,
                    "ST_avg_policy_NB": 0.3,
                },
                {
                    "jurisdiction": "new_zealand",
                    "group": "behavior",
                    "S1_optimal_NB": 0.25,
                    "ST_optimal_NB": 0.45,
                    "S1_avg_policy_NB": 0.15,
                    "ST_avg_policy_NB": 0.35,
                },
            ]
        ),
    }


def test_reporting_bundle_and_tables(tmp_path: Path) -> None:
    meta_dir = _write_meta_fixture(tmp_path)
    output_dir = tmp_path / "tables"

    bundle = build_reporting_bundle(meta_dir=meta_dir)
    generated = write_reporting_tables(output_dir, bundle)

    assert set(bundle["run_dirs"]) == {"australia", "new_zealand"}
    assert (output_dir / "policy_summary.csv").exists()
    assert (output_dir / "australia_policy_summary.csv").exists()
    assert (output_dir / "new_zealand_policy_summary.csv").exists()
    assert generated["reporting_manifest"].exists()

    summary = pd.read_csv(output_dir / "policy_summary.csv")
    assert set(summary["jurisdiction"]) == {"australia", "new_zealand"}
    assert "moratorium" in set(summary["policy"])


def test_reporting_tables_write_uncertainty_outputs(tmp_path: Path) -> None:
    meta_dir = _write_meta_fixture(tmp_path)
    bundle = _synthetic_bundle(meta_dir)
    output_dir = tmp_path / "tables_with_uncertainty"

    write_reporting_tables(output_dir, bundle)

    assert (output_dir / "australia_evppi_by_group.csv").exists()
    assert (output_dir / "new_zealand_evppi_by_group.csv").exists()
    assert (output_dir / "australia_uncertainty_decomposition.csv").exists()
    assert (output_dir / "new_zealand_uncertainty_decomposition.csv").exists()


def test_generate_figures_and_publish_pack(tmp_path: Path, monkeypatch) -> None:
    meta_dir = _write_meta_fixture(tmp_path)
    figures_dir = tmp_path / "figures"

    monkeypatch.setattr(
        "sys.argv",
        [
            "generate_figures",
            "--meta_dir",
            str(meta_dir),
            "--output",
            str(figures_dir),
            "--formats",
            "png",
        ],
    )
    generate_figures.main()

    assert (figures_dir / "australia_net_benefit.png").exists()
    assert (figures_dir / "new_zealand_net_benefit.png").exists()
    assert (figures_dir / "australia_net_benefit_caption.md").exists()

    publish_dir = tmp_path / "publish_pack"
    monkeypatch.setattr(
        "sys.argv",
        [
            "publish_pack",
            "--meta_dir",
            str(meta_dir),
            "--out",
            str(publish_dir),
        ],
    )
    publish_pack.main()

    assert (publish_dir / "POLICY_BRIEF.md").exists()
    assert (publish_dir / "POLICY_BRIEF.docx").exists()
    assert (publish_dir / "POLICY_BRIEF.pdf").exists()
    assert (publish_dir / "policy_summary.csv").exists()
    assert (publish_dir / "reporting_manifest.json").exists()
    assert (publish_dir / "figures" / "australia_net_benefit.png").exists()

    brief = (publish_dir / "POLICY_BRIEF.md").read_text(encoding="utf-8")
    assert "Source:" not in brief
    assert "Moratorium leads on mean net benefit" in brief
    assert "premium indices from the insurance model" in brief

    manifest = json.loads((publish_dir / "reporting_manifest.json").read_text(encoding="utf-8"))
    assert "source_runs" in manifest
    assert "source_run_dirs" not in manifest
    assert manifest["source_runs"]["australia"]["run_id"] == "australia_20260306T010203Z"


def test_publish_pack_writes_uncertainty_outputs_from_bundle(tmp_path: Path, monkeypatch) -> None:
    meta_dir = _write_meta_fixture(tmp_path)
    publish_dir = tmp_path / "publish_pack_with_uncertainty"

    def stub_build_reporting_bundle(meta_dir: Path) -> dict[str, object]:
        return _synthetic_bundle(meta_dir)

    monkeypatch.setattr(publish_pack, "build_reporting_bundle", stub_build_reporting_bundle)
    monkeypatch.setattr(
        "sys.argv",
        [
            "publish_pack",
            "--meta_dir",
            str(meta_dir),
            "--out",
            str(publish_dir),
        ],
    )
    publish_pack.main()

    assert (publish_dir / "australia_evppi_by_group.csv").exists()
    assert (publish_dir / "new_zealand_uncertainty_decomposition.csv").exists()
    assert (publish_dir / "figures" / "new_zealand_uncertainty_decomposition.png").exists()
    assert (publish_dir / "figures" / "new_zealand_uncertainty_decomposition_caption.md").exists()


def test_validation_and_output_formatting(tmp_path: Path) -> None:
    comparisons = {
        "moratorium": {
            "testing_uptake_change": 0.05,
            "premium_change": 0.02,
            "welfare_change": 50_000.0,
            "compliance_change": 0.10,
        },
        "ban": {
            "testing_uptake_change": 0.08,
            "premium_change": 0.03,
            "welfare_change": 75_000.0,
            "compliance_change": 0.15,
        },
    }
    table = format_comparison_table(comparisons)
    assert "+75,000" in table

    brief_path = tmp_path / "brief.md"
    generate_policy_brief(
        results={
            "status_quo": {
                "testing_uptake": 0.5,
                "avg_premium": 1_000.0,
                "welfare_impact": 0.0,
                "compliance_rate": 0.7,
            }
        },
        comparisons=comparisons,
        output_path=brief_path,
    )
    brief = brief_path.read_text(encoding="utf-8")
    assert "Ban" in brief

    checks = run_ppc(
        simulated_data={"uptake": [0.48, 0.5, 0.52, 0.54, 0.56]},
        empirical_targets={"uptake": {"value": 0.52, "ci_lower": 0.5, "ci_upper": 0.54}},
    )
    assert len(checks) == 1
    assert checks[0].simulated_ci[0] != min([0.48, 0.5, 0.52, 0.54, 0.56])

    results_path = tmp_path / "ppc_results.json"
    save_ppc_results(checks, results_path)
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    assert "summary" in payload
    assert "checks" in payload
