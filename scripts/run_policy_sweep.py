import argparse
import sys
from pathlib import Path

import jax
import yaml
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.model.glue_policy_eval import GlobalParams, simulate_policy
from src.model.module_a_behavior import BehaviorParams
from src.model.module_b_clinical import ClinicalParams
from src.model.module_c_insurance_eq import InsuranceParams
from src.model.module_e_passthrough import PassThroughParams
from src.model.module_f_data_quality import DataQualityParams
from src.utils.logging_config import setup_logging

setup_logging(level="INFO")


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
        msg = f"Unknown jurisdiction: {jurisdiction}. Use australia or new_zealand."
        raise ValueError(msg)
    return mapping[jurisdiction]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jurisdiction", default="australia", help="australia | new_zealand")
    args = parser.parse_args()

    logger.info(f"Starting policy sweep for jurisdiction: {args.jurisdiction}")

    try:
        cfg = load_yaml(Path("configs/base.yaml"))
        pol_cfg = load_yaml(get_policies_path(args.jurisdiction))
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return

    seed = int(cfg["seed"])
    key = jax.random.PRNGKey(seed)
    logger.debug(f"Initialized PRNGKey with seed: {seed}")

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

    logger.info(f"Evaluating {len(policies)} policies...")

    results = []
    # Common random numbers across policies
    base_key = key

    for pol in policies:
        logger.debug(f"Simulating policy: {pol['name']}")
        res = simulate_policy(base_key, pol, params)
        results.append(res)

    logger.info("Simulation complete. Results:")
    logger.info("-" * 100)
    logger.info(
        f"JURISDICTION: {pol_cfg.get('jurisdiction', 'n/a').upper()} | DOMAIN: {pol_cfg.get('domain', 'n/a').upper()}"
    )
    logger.info("-" * 100)

    for r in results:
        logger.success(
            f"Policy: {r['policy']:<15} | "
            f"Net QALYs: {float(r['net_qalys']):>8.4f} | "
            f"Avg Prem: {float(r['avg_premium']):>10.2f} | "
            f"AUC: {float(r.get('data_auc', 0.0)):>6.3f}",
        )
    logger.info("-" * 100)


if __name__ == "__main__":
    main()
