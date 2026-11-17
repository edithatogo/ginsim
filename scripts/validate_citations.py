#!/usr/bin/env python3
"""
Citation Audit Tool (Diamond Standard).

Verifies that every citation in the manuscript draft exists in the BibTeX library.
"""

import re
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
    manuscript_path = project_root / "local_only" / "docs" / "manuscript_draft.md"
    bib_path = project_root / "context" / "references.bib"

    if not manuscript_path.exists() or not bib_path.exists():
        logger.error("Missing manuscript or bib file.")
        return

    # 1. Load Manuscript and find @keys
    with open(manuscript_path, encoding="utf-8") as f:
        text = f.read()

    # Match patterns like [@key] or @key
    cite_keys = set(re.findall(r"@([a-zA-Z0-9_:-]+)", text))
    logger.info(f"Found {len(cite_keys)} unique citations in manuscript.")

    # 2. Load BibTeX and find keys
    with open(bib_path, encoding="utf-8") as f:
        bib_text = f.read()

    # Match patterns like @article{key,
    bib_keys = set(re.findall(r"@[a-zA-Z]+\{([a-zA-Z0-9_:-]+),", bib_text))
    logger.info(f"Found {len(bib_keys)} entries in references.bib.")

    # 3. Validate
    missing = [k for k in cite_keys if k not in bib_keys]
    unused = [k for k in bib_keys if k not in cite_keys]

    if missing:
        logger.warning(f"MISSING CITATIONS: {missing}")
    else:
        logger.success("All citations validated against BibTeX library.")

    if unused:
        logger.info(f"Unused BibTeX entries: {len(unused)}")


if __name__ == "__main__":
    main()
