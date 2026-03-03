from __future__ import annotations

import argparse
import yaml
from pathlib import Path

import jax

from src.model.glue_policy_eval import GlobalParams, simulate_policy
from src.model.module_a_behavior import BehaviorParams
from src.model.module_b_clinical import ClinicalParams
from src.model.module_c_insurance_eq import InsuranceParams
from src.model.module_e_passthrough import PassThroughParams
from src.model.module_f_data_quality import DataQualityParams

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text())

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jurisdiction", default="australia", help="australia | new_zealand")
    args = parser.parse_args()

    cfg = load_yaml(Path("configs/base.yaml"))
    pol_cfg = load_yaml(get_policies_path(args.jurisdiction))

    seed = int(cfg["seed"])
    key = jax.random.PRNGKey(seed)

    # Placeholder parameters. Replace with inference outputs.
    params = GlobalParams(
        behavior=BehaviorParams(baseline_logit=-2.0, policy_shock=1.0, trend=0.01),
        clinical=ClinicalParams(
            baseline_event_rate=0.02,
            uptake_to_prevention=0.5,
            prevention_effect=0.6,
            cost_per_event=20000.0,
            qaly_loss_per_event=0.3,
        ),
        insurance=InsuranceParams(
            base_premium=1000.0,
            loss_cost=700.0,
            expense_load=0.2,
            markup=0.1,
            adverse_selection_sensitivity=0.3,
            price_elasticity=1.2,
        ),
        passthrough=PassThroughParams(),
        data_quality=DataQualityParams(
            base_participation_logit=0.0,
            fear_sensitivity=2.0,
            base_auc=0.75,
            auc_sensitivity=0.08,
        ),
    )

    policies = []
    for name, rule in pol_cfg["policies"].items():
        policies.append({"name": name, **rule})

    results = []
    # Common random numbers across policies
    base_key = key

    for pol in policies:
        res = simulate_policy(base_key, pol, params)
        results.append(res)

    print(f"Jurisdiction: {pol_cfg.get('jurisdiction')} | Domain: {pol_cfg.get('domain')}")
    for r in results:
        print(
            r["policy"],
            "net_qalys=", float(r["net_qalys"]),
            "avg_premium=", float(r["avg_premium"]),
            "pass_through=", float(r.get("pass_through", 0.0)),
            "data_auc=", float(r.get("data_auc", 0.0)),
        )

if __name__ == "__main__":
    main()
