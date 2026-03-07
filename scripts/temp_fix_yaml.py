import yaml

with open("configs/calibration_australia.yaml") as f:
    data = yaml.safe_load(f)

# Add sensitivity_bounds to deterrence_elasticity
params = data["module_a_calibration"]["parameters"]
params["deterrence_elasticity"]["sensitivity_bounds"] = {
    "lower": 0.02,
    "upper": 0.60,
    "rationale": "Bounds cover the full range of international survey evidence (McGuire 2019, Taylor 2021).",
}

with open("configs/calibration_australia.yaml", "w") as f:
    yaml.dump(data, f, sort_keys=False)
