from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import jax
import numpy as np
import pandas as pd

from src.model.dcba_ledger import LedgerSpec, compute_ledger
from src.model.glue_policy_eval import GlobalParams, simulate_policy
from src.model.module_a_behavior import BehaviorParams
from src.model.module_b_clinical import ClinicalParams
from src.model.module_c_insurance_eq import InsuranceParams
from src.model.module_e_passthrough import PassThroughParams
from src.model.module_f_data_quality import DataQualityParams
from src.model.policy_loader import load_policies_config
from src.utils.manifest import write_manifest
from src.utils.posterior import deterministic_subsample, load_draws_npy


def get_policies_path(jurisdiction: str) -> Path:
    mapping = {
        "australia": Path("configs/policies_australia.yaml"),
        "new_zealand": Path("configs/policies_new_zealand.yaml"),
        "nz": Path("configs/policies_new_zealand.yaml"),
        "au": Path("configs/policies_australia.yaml"),
    }
    if jurisdiction not in mapping:
        message = f"Unknown jurisdiction: {jurisdiction}. Use australia or new_zealand."
        raise ValueError(message)
    return mapping[jurisdiction]


def _read_seed(base_cfg_path: Path) -> int:
    seed = 20260302
    for ln in base_cfg_path.read_text(encoding="utf-8").splitlines():
        if ln.strip().startswith("seed:"):
            seed = int(ln.split(":", 1)[1].strip())
            break
    return seed


def _theta(draws: list[dict[str, Any]], keys: list[str], n: int) -> np.ndarray:
    cols = []
    for k in keys:
        col = []
        for i in range(n):
            v = draws[i].get(k, 0.0)
            if isinstance(v, (int, float)):
                col.append(float(v))
            else:
                try:
                    col.append(float(np.mean(np.array(v, dtype=float))))
                except Exception:
                    col.append(0.0)
        cols.append(col)
    return np.column_stack(cols).astype(float)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jurisdiction", default="australia")
    parser.add_argument(
        "--joint_draws",
        required=True,
        help="Path to joint_draws.npy (dict draws with nested groups)",
    )
    parser.add_argument("--n_draws", type=int, default=500)
    parser.add_argument("--out", default="outputs/runs/full_uncertainty_joint")
    args = parser.parse_args()

    base_cfg_path = Path("configs/base.yaml")
    pol_cfg_path = get_policies_path(args.jurisdiction)
    pol_cfg = load_policies_config(pol_cfg_path)

    seed = _read_seed(base_cfg_path)
    key = jax.random.PRNGKey(seed)

    # Load and subsample joint draws
    joint = deterministic_subsample(load_draws_npy(Path(args.joint_draws)), args.n_draws)
    n = len(joint)

    # Defaults if a group missing in a draw
    defaults = {
        "behavior": {"baseline_logit": -2.0, "policy_shock": 1.0, "trend": 0.01},
        "clinical": {
            "baseline_event_rate": 0.02,
            "uptake_to_prevention": 0.5,
            "prevention_effect": 0.6,
            "cost_per_event": 20000.0,
            "qaly_loss_per_event": 0.3,
        },
        "insurance": {
            "base_premium": 1000.0,
            "loss_cost": 700.0,
            "expense_load": 0.2,
            "markup": 0.1,
            "adverse_selection_sensitivity": 0.3,
            "price_elasticity": 1.2,
        },
        "passthrough": {
            "base_pass_through": 0.7,
            "concentration_slope": -0.3,
            "noise_sd": 0.05,
        },
        "data_quality": {
            "base_participation_logit": 0.0,
            "fear_sensitivity": 2.0,
            "base_auc": 0.75,
            "auc_sensitivity": 0.08,
            "noise_sd": 0.01,
        },
    }

    policies = [r.model_dump() for r in pol_cfg.policies.values()]
    n_policies = len(policies)
    spec = LedgerSpec()

    rows = []
    nb = np.zeros((n, n_policies), dtype=float)

    # Capture theta matrices for decomposition
    theta_store: dict[str, list[dict[str, Any]]] = {
        g: []
        for g in ["mapping", "behavior", "clinical", "insurance", "passthrough", "data_quality"]
    }

    for i in range(n):
        draw_key = jax.random.fold_in(key, i)
        d = joint[i]

        mp = d.get("mapping", None)
        beh = d.get("behavior", defaults["behavior"])
        clin = d.get("clinical", defaults["clinical"])
        ins = d.get("insurance", defaults["insurance"])
        pt = d.get("passthrough", defaults["passthrough"])
        dq = d.get("data_quality", defaults["data_quality"])

        params = GlobalParams(
            behavior=BehaviorParams(**beh),
            clinical=ClinicalParams(**clin),
            insurance=InsuranceParams(**ins),
            passthrough=PassThroughParams(**pt),
            data_quality=DataQualityParams(**dq),
        )

        for g, values in theta_store.items():
            if g in d:
                values.append(d[g])

        for j, pol in enumerate(policies):
            pol2 = dict(pol)
            if mp is not None:
                pol2["_mapping_params"] = mp
            out = simulate_policy(draw_key, pol2, params)
            led = compute_ledger(out, spec)

            nb[i, j] = float(led["net_benefit"])
            rows.append(
                {
                    "jurisdiction": pol_cfg.jurisdiction,
                    "domain": pol_cfg.domain,
                    "draw": i,
                    "policy": out["policy"],
                    "net_qalys": float(out.get("net_qalys", 0.0)),
                    "avg_premium": float(out.get("avg_premium", 0.0)),
                    "nb": float(led["net_benefit"]),
                },
            )

    df = pd.DataFrame(rows)
    out_dir = (
        Path(args.out)
        / f"{pol_cfg.jurisdiction}_{pd.Timestamp.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    write_manifest(
        out_dir,
        repo_root=Path(),
        jurisdiction=pol_cfg.jurisdiction,
        domain=pol_cfg.domain,
        policies_file=pol_cfg_path,
        base_config_file=base_cfg_path,
        notes="Full uncertainty run from joint draws (nested parameter groups).",
        extra={"joint_draws": args.joint_draws, "n_draws": n},
    )

    df.to_csv(out_dir / "full_uncertainty_draws.csv", index=False)
    np.save(out_dir / "net_benefit_matrix.npy", nb)

    # Save theta matrices if present and consistent length
    # (Only save for groups provided; decomposition scripts will ignore missing)
    if len(theta_store["mapping"]) == n:
        np.save(
            out_dir / "theta_mapping.npy",
            _theta(
                theta_store["mapping"],
                ["intercept", "beta_allow", "beta_caps", "beta_enforcement"],
                n,
            ),
        )
    if len(theta_store["behavior"]) == n:
        np.save(
            out_dir / "theta_behavior.npy",
            _theta(theta_store["behavior"], ["baseline_logit", "policy_shock", "trend"], n),
        )
    if len(theta_store["clinical"]) == n:
        np.save(
            out_dir / "theta_clinical.npy",
            _theta(
                theta_store["clinical"],
                [
                    "baseline_event_rate",
                    "uptake_to_prevention",
                    "prevention_effect",
                    "cost_per_event",
                    "qaly_loss_per_event",
                ],
                n,
            ),
        )
    if len(theta_store["insurance"]) == n:
        np.save(
            out_dir / "theta_insurance.npy",
            _theta(
                theta_store["insurance"],
                [
                    "base_premium",
                    "loss_cost",
                    "expense_load",
                    "markup",
                    "adverse_selection_sensitivity",
                    "price_elasticity",
                ],
                n,
            ),
        )
    if len(theta_store["passthrough"]) == n:
        np.save(
            out_dir / "theta_passthrough.npy",
            _theta(
                theta_store["passthrough"],
                ["base_pass_through", "concentration_slope", "noise_sd"],
                n,
            ),
        )
    if len(theta_store["data_quality"]) == n:
        np.save(
            out_dir / "theta_data_quality.npy",
            _theta(
                theta_store["data_quality"],
                [
                    "base_participation_logit",
                    "fear_sensitivity",
                    "base_auc",
                    "auc_sensitivity",
                    "noise_sd",
                ],
                n,
            ),
        )

    summary = (
        df.groupby(["policy"])
        .agg(
            nb_mean=("nb", "mean"),
            nb_p05=("nb", lambda x: float(np.quantile(x, 0.05))),
            nb_p95=("nb", lambda x: float(np.quantile(x, 0.95))),
        )
        .reset_index()
        .sort_values("nb_mean", ascending=False)
    )
    summary.to_csv(out_dir / "full_uncertainty_summary.csv", index=False)

    print("Wrote:", out_dir)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
