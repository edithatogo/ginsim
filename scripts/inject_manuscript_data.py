#!/usr/bin/env python3
"""
Manuscript Data Injector (Diamond Standard).

Injects authoritative results from manifest.json into the manuscript template.
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging

setup_logging(level="INFO")


def main():
    project_root = Path(__file__).parent.parent
    manifest_path = project_root / "outputs" / "results_manifest.json"
    template_path = project_root / "local_only" / "docs" / "manuscript_template.md"
    output_path = project_root / "local_only" / "docs" / "manuscript_draft.md"

    if not manifest_path.exists():
        logger.error("Manifest not found. Run sync_manuscript_data.py first.")
        return

    # Load data
    with open(manifest_path, encoding="utf-8") as f:
        data = json.load(f)

    # Load template
    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    # Inject
    content = template
    for key, val in data.items():
        placeholder = "{{" + key + "}}"
        content = content.replace(placeholder, str(val))

    # Save draft
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    logger.success(f"Manuscript draft generated: {output_path}")


if __name__ == "__main__":
    main()
