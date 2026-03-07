import os
import re

EXCLUDE_DIRS = {".venv", "__pycache__", ".git", ".pytest_cache", ".ruff_cache", "external"}


def fix_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except:
        return

    # Move jaxtyping out
    if "if TYPE_CHECKING:" in content and "from jaxtyping" in content:
        pattern = r"if TYPE_CHECKING:\s+(?:.*\n\s+)*from jaxtyping import ([\w, ]+)"
        match = re.search(pattern, content)
        if match:
            imports = match.group(1)
            # Use simple replace for the specific block line
            block_line = f"    from jaxtyping import {imports}"
            content = content.replace(block_line, "")
            # Add to top
            if f"from jaxtyping import {imports}" not in content:
                content = (
                    f"from __future__ import annotations\nfrom jaxtyping import {imports}\n"
                    + content.replace("from __future__ import annotations", "")
                )

    # Fix int -> float
    content = re.sub(r"(penalty_max|cap_death|cap_tpd|cap_trauma)=(\d+)(?!\.)", r"\1=\2.0", content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


for target in ["src", "tests", "scripts"]:
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(".py"):
                fix_file(os.path.join(root, file))
