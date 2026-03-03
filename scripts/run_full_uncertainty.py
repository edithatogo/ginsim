from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd

import jax
import jax.numpy as jnp

from src.model.policy_loader import load_policies_config
from src.model.glue_policy_eval import GlobalParams, simulate_policy
from src.model.module_a_behavior import BehaviorParams
from src.model.module_b_clinical import ClinicalParams
from src.model.module_c_insurance_eq import InsuranceParams
from src.model.module_e_passthrough import PassThroughParams
from src.model.module_f_data_quality import DataQualityParams
from src.model.dcba_ledger import LedgerSpec, compute_ledger
from src.utils.manifest import write_manifest
from src.utils.posterior import load_draws_npy, deterministic_subsample
from src.utils.sampling import select_draw, SamplingMode

def get_policies_path(jurisdiction: str) -> Path:
    mapping = {
        "australia": Path("configs/policies_australia.yaml"),
        "new_zealand": Path("configs/policies_new_zealand.yaml"),
        "nz": Path("configs/policies_new_zealand.yaml"),
        "au": Path("configs/policies_australia.yaml"),
    }
    if jurisdiction not in mapping:
        raise ValueError(f"Unknown jurisdiction: {jurisdiction}. Use australia or new_zealand.")
    return mapping[jurisdiction]

def _read_seed(base_cfg_path: Path) -> int:
    seed = 20260302
    for ln in base_cfg_path.read_text(encoding="utf-8").splitlines():
        if ln.strip().startswith("seed:"):
            seed = int(ln.split(":", 1)[1].strip())
            break
    return seed

def maybe_load(path_str: str, n: int):
    if not path_str:
        return None
    p = Path(path_str)
    if p.exists():
        return deterministic_subsample(load_draws_npy(p), n)
    return None

def theta_matrix(draws, keys: list[str], n: int) -> np.ndarray | None:
    if draws is None:
        return None
    cols = []
    for k in keys:
        col = []
        for i in range(n):
            d = draws[i % len(draws)]
            v = d.get(k, 0.0)
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
    parser.add_argument("--n_draws", type=int, default=500)
    parser.add_argument("--sampling_mode", default="independent", choices=["independent", "common_index", "random"])
    parser.add_argument("--out", default="outputs/runs/full_uncertainty")

    parser.add_argument("--mapping_posterior", default="outputs/posterior_samples/policy_mapping_posterior.npy")
    parser.add_argument("--behavior_posterior", default="")
    parser.add_argument("--clinical_posterior", default="")
    parser.add_argument("--insurance_posterior", default="")
    parser.add_argument("--passthrough_posterior", default="")
    parser.add_argument("--data_quality_posterior", default="")
    args = parser.parse_args()

    base_cfg_path = Path("configs/base.yaml")
    pol_cfg_path = get_policies_path(args.jurisdiction)
    pol_cfg = load_policies_config(pol_cfg_path)

    seed = _read_seed(base_cfg_path)
    key = jax.random.PRNGKey(seed)
    rng = np.random.default_rng(seed)

    n = int(args.n_draws)
    mode: SamplingMode = args.sampling_mode  # type: ignore

    mapping_draws = maybe_load(args.mapping_posterior, n) if args.mapping_posterior else None
    behavior_draws = maybe_load(args.behavior_posterior, n)
    clinical_draws = maybe_load(args.clinical_posterior, n)
    insurance_draws = maybe_load(args.insurance_posterior, n)
    passthrough_draws = maybe_load(args.passthrough_posterior, n)
    dq_draws = maybe_load(args.data_quality_posterior, n)

    # Defaults
    default_behavior = dict(baseline_logit=-2.0, policy_shock=1.0, trend=0.01)
    default_clinical = dict(baseline_event_rate=0.02, uptake_to_prevention=0.5, prevention_effect=0.6,
                            cost_per_event=20000.0, qaly_loss_per_event=0.3)
    default_insurance = dict(base_premium=1000.0, loss_cost=700.0, expense_load=0.2, markup=0.1,
                             adverse_selection_sensitivity=0.3, price_elasticity=1.2)
    default_passthrough = dict(base_pass_through=0.7, concentration_slope=-0.3, noise_sd=0.05)
    default_dq = dict(base_participation_logit=0.0, fear_sensitivity=2.0, base_auc=0.75, auc_sensitivity=0.08, noise_sd=0.01)

    policies = [r.model_dump() for r in pol_cfg.policies.values()]
    P = len(policies)

    spec = LedgerSpec()

    rows = []
    nb = np.zeros((n, P), dtype=float)

    for i in range(n):
        draw_key = jax.random.fold_in(key, i)

        mp = select_draw(mapping_draws, i, n, mode, rng) if mapping_draws is not None else None
        b = select_draw(behavior_draws, i, n, mode, rng) or default_behavior
        c = select_draw(clinical_draws, i, n, mode, rng) or default_clinical
        ins = select_draw(insurance_draws, i, n, mode, rng) or default_insurance
        pt = select_draw(passthrough_draws, i, n, mode, rng) or default_passthrough
        dq = select_draw(dq_draws, i, n, mode, rng) or default_dq

        params = GlobalParams(
            behavior=BehaviorParams(**b),
            clinical=ClinicalParams(**c),
            insurance=InsuranceParams(**ins),
            passthrough=PassThroughParams(**pt),
            data_quality=DataQualityParams(**dq),
        )

        for j, pol in enumerate(policies):
            pol2 = dict(pol)
            if mp is not None:
                pol2["_mapping_params"] = mp

            out = simulate_policy(draw_key, pol2, params)
            led = compute_ledger(out, spec)
            nb[i, j] = float(led["net_benefit"])

            rows.append({
                "jurisdiction": pol_cfg.jurisdiction,
                "domain": pol_cfg.domain,
                "draw": i,
                "policy": out["policy"],
                "net_qalys": float(out.get("net_qalys", 0.0)),
                "avg_premium": float(out.get("avg_premium", 0.0)),
                "nb": float(led["net_benefit"]),
            })

    df = pd.DataFrame(rows)
    out_dir = Path(args.out) / f"{pol_cfg.jurisdiction}_{pd.Timestamp.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    out_dir.mkdir(parents=True, exist_ok=True)

    write_manifest(
        out_dir,
        repo_root=Path("."),
        jurisdiction=pol_cfg.jurisdiction,
        domain=pol_cfg.domain,
        policies_file=pol_cfg_path,
        base_config_file=base_cfg_path,
        notes="Full uncertainty run with sampling modes; writes NB matrix and theta matrices for decomposition.",
        extra={"n_draws": n, "sampling_mode": mode},
    )

    df.to_csv(out_dir / "full_uncertainty_draws.csv", index=False)
    np.save(out_dir / "net_benefit_matrix.npy", nb)

    theta_map = theta_matrix(mapping_draws, ["intercept","beta_allow","beta_caps","beta_enforcement"], n)
    theta_beh = theta_matrix(behavior_draws, ["baseline_logit","policy_shock","trend"], n)
    theta_clin = theta_matrix(clinical_draws, ["baseline_event_rate","uptake_to_prevention","prevention_effect","cost_per_event","qaly_loss_per_event"], n)
    theta_ins = theta_matrix(insurance_draws, ["base_premium","loss_cost","expense_load","markup","adverse_selection_sensitivity","price_elasticity"], n)
    theta_pt = theta_matrix(passthrough_draws, ["base_pass_through","concentration_slope","noise_sd"], n)
    theta_dq = theta_matrix(dq_draws, ["base_participation_logit","fear_sensitivity","base_auc","auc_sensitivity","noise_sd"], n)

    if theta_map is not None: np.save(out_dir / "theta_mapping.npy", theta_map)
    if theta_beh is not None: np.save(out_dir / "theta_behavior.npy", theta_beh)
    if theta_clin is not None: np.save(out_dir / "theta_clinical.npy", theta_clin)
    if theta_ins is not None: np.save(out_dir / "theta_insurance.npy", theta_ins)
    if theta_pt is not None: np.save(out_dir / "theta_passthrough.npy", theta_pt)
    if theta_dq is not None: np.save(out_dir / "theta_data_quality.npy", theta_dq)

    summary = (
        df.groupby(["policy"])
          .agg(
              nb_mean=("nb","mean"),
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
