with open("configs/calibration_australia.yaml") as f:
    # Use a safer loading strategy for broken YAML: read as lines and fix
    lines = f.readlines()

fixed_lines = []
for line in lines:
    # Fix the invalid 'rationale' sibling to a list
    if "rationale:" in line and "Key policy drivers" in line:
        fixed_lines.append(
            '      group_rationale: "Key policy drivers; high uncertainty; direct impact on outcomes"\n'
        )
    elif "rationale:" in line and "Well-estimated but important" in line:
        fixed_lines.append(
            '      group_rationale: "Well-estimated but important for absolute levels"\n'
        )
    else:
        fixed_lines.append(line)

with open("configs/calibration_australia.yaml", "w") as f:
    f.writelines(fixed_lines)
