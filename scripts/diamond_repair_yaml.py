import yaml


def repair_file(path):
    print(f"Repairing {path}...")
    with open(path) as f:
        # Load all documents (handling the --- separators)
        docs = list(yaml.safe_load_all(f))

    # Fix the EVPPI groupings in each module that has them
    for doc in docs:
        if not doc:
            continue
        for key in doc:
            if "calibration" in key:
                module = doc[key]
                if "evppi_groupings" in module:
                    old_groups = module["evppi_groupings"]
                    new_groups = {}
                    for priority, data in old_groups.items():
                        if priority == "rationale":
                            continue
                        # Ensure it's a dict with params and rationale
                        if isinstance(data, list):
                            new_groups[priority] = {
                                "params": data,
                                "rationale": "Key drivers for this module",
                            }
                        else:
                            new_groups[priority] = data
                    module["evppi_groupings"] = new_groups

    with open(path, "w") as f:
        yaml.dump_all(docs, f, sort_keys=False)


# First, checkout the clean versions again
import subprocess

subprocess.run(["git", "checkout", "configs/calibration_australia.yaml"], check=True)
subprocess.run(["git", "checkout", "configs/calibration_new_zealand.yaml"], check=True)

repair_file("configs/calibration_australia.yaml")
repair_file("configs/calibration_new_zealand.yaml")
