import re

with open("configs/calibration_australia.yaml") as f:
    content = f.read()

# Pattern to find the broken EVPPI block
pattern = (
    r"  # EVPPI groupings[\s\S]+?rationale: \"Well-estimated but important for absolute levels\""
)
replacement = """  # EVPPI groupings
  evppi_groupings:
    high_priority:
      params:
        - deterrence_elasticity
        - moratorium_effect
      rationale: "Key policy drivers; high uncertainty; direct impact on outcomes"

    medium_priority:
      params:
        - baseline_testing_uptake
      rationale: "Well-estimated but important for absolute levels\""""

new_content = re.sub(pattern, replacement, content)

with open("configs/calibration_australia.yaml", "w") as f:
    f.write(new_content)
