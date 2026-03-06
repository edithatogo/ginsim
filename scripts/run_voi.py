from __future__ import annotations

import argparse
from pathlib import Path

import jax
import jax.numpy as jnp
import yaml

from src.model.glue_policy_eval import GlobalParams, simulate_policy
from src.model.module_a_behavior import BehaviorParams
from src.model.module_b_clinical import ClinicalParams
from src.model.module_c_insurance_eq import InsuranceParams
from src.model.module_e_passthrough import PassThroughParams
from src.model.module_f_data_quality import DataQualityParams
from src.model.voi import evpi, evppi


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
        message = f"Unknown jurisdiction: {jurisdiction}. Use australia or new_zealand."
        raise ValueError(message)
    return mapping[jurisdiction]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jurisdiction", default="australia", help="australia | new_zealand")
    args = parser.parse_args()

    cfg = load_yaml(Path("configs/base.yaml"))
    pol_cfg = load_yaml(get_policies_path(args.jurisdiction))

    seed = int(cfg["seed"])
    key = jax.random.PRNGKey(seed)

    # Placeholder: in real usage, these would come from posterior draws.
    base_params = GlobalParams(
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

    # Monte Carlo over one uncertain parameter to demo EVPPI
    n_draws = 2000
    keys = jax.random.split(key, n_draws)

    shock = jax.random.normal(keys[0], (n_draws,)) * 0.3 + 1.0
    shock = jnp.clip(shock, 0.0, 2.0)

    def one_draw(i):
        p = GlobalParams(
            behavior=BehaviorParams(
                baseline_logit=base_params.behavior.baseline_logit,
                policy_shock=float(shock[i]),
                trend=base_params.behavior.trend,
            ),
            clinical=base_params.clinical,
            insurance=base_params.insurance,
            passthrough=base_params.passthrough,
            data_quality=base_params.data_quality,
        )
        base_k = keys[i]
        outs = [simulate_policy(base_k, pol, p) for pol in policies]

        nb = [100000.0 * o["net_qalys"] - o["net_health_cost"] - 0.1 * o["avg_premium"] for o in outs]
        return jnp.stack(nb)

    net_benefit = jax.vmap(one_draw)(jnp.arange(n_draws))

    print(f"Jurisdiction: {pol_cfg.get('jurisdiction')} | Domain: {pol_cfg.get('domain')}")
    print("EVPI:", float(evpi(net_benefit)))
    print("EVPPI (policy_shock):", float(evppi(net_benefit, shock, n_bins=20)))


if __name__ == "__main__":
    main()
