#!/usr/bin/env python3
"""
Submission Pack Publisher (Diamond Standard v2.0).

Consolidates all public artifacts, result manifests, and supplementary
documentation into a single reviewer-ready ZIP archive.
"""

import sys
import zipfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging

setup_logging(level="INFO")


def main():
    project_root = Path(__file__).parent.parent
    dist_dir = project_root / "outputs" / "submission_pack"
    dist_dir.mkdir(parents=True, exist_ok=True)

    zip_path = project_root / "outputs" / "diamond_submission_pack_v2.0.zip"

    # 1. Gather Public Artifacts
    manifest_path = project_root / "outputs" / "results_manifest.json"
    manuscript_path = project_root / "local_only" / "docs" / "manuscript_draft.md"
    supp_path = project_root / "local_only" / "docs" / "SUPPLEMENTARY_DOCS.md"

    logger.info("Consolidating artifacts...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Source Code (Core only)
        for folder in ["src", "scripts", "configs", "context"]:
            for file in (project_root / folder).rglob("*"):
                if "__pycache__" not in str(file) and file.is_file():
                    zipf.write(file, arcname=file.relative_to(project_root))

        # Root Meta
        for meta in ["pyproject.toml", "uv.lock", "README.md", "LICENSE"]:
            p = project_root / meta
            if p.exists():
                zipf.write(p, arcname=meta)

        # Autoritative Data
        if manifest_path.exists():
            zipf.write(manifest_path, arcname="manifest.json")

        # Manuscript & Supplementary (Publicized)
        if manuscript_path.exists():
            zipf.write(manuscript_path, arcname="MANUSCRIPT_DRAFT.md")
        if supp_path.exists():
            zipf.write(supp_path, arcname="SUPPLEMENTARY_DOCS.md")

    logger.success(f"Archival package generated: {zip_path}")


if __name__ == "__main__":
    main()
