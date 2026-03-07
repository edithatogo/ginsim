import os
import re


def fix_content(content):
    # Fix jaxtyping imports in TYPE_CHECKING blocks
    # We find blocks that contain ONLY jaxtyping imports and remove the whole block
    # Match: if TYPE_CHECKING:\n    from jaxtyping import ...
    pattern = r"if TYPE_CHECKING:\s+from jaxtyping import ([\w, ]+)\n"
    match = re.search(pattern, content)
    if match:
        imports = match.group(1)
        # Remove the block
        content = re.sub(pattern, "", content)
        # Add to top (after __future__)
        if "from jaxtyping import" not in content:
            content = content.replace(
                "from __future__ import annotations",
                f"from __future__ import annotations\nfrom jaxtyping import {imports}",
            )

    # Fix int -> float assignments safely
    # We only target specific keywords and ensured they don't already have a dot
    # Matches: penalty_max=1000000.0 -> penalty_max=100000.00.0
    # Does NOT match: penalty_max=100000.00.0
    keys = ["penalty_max", "cap_death", "cap_tpd", "cap_trauma"]
    for key in keys:
        content = re.sub(rf"({key})=(\d+)(?!\.)", r"\1=\2.0", content)

    return content


def process_dir(target):
    for root, dirs, files in os.walk(target):
        if any(ex in root for ex in [".venv", "__pycache__", ".git"]):
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()

                    new_content = fix_content(content)

                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing {path}: {e}")


if __name__ == "__main__":
    process_dir("src")
    process_dir("tests")
    process_dir("scripts")
