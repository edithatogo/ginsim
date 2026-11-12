import sys
import zipfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging
from src.utils.path_resolver import resolve_path

setup_logging(level="INFO")


def create_final_pack():
    files = [
        "README.md",
        "pyproject.toml",
        "uv.lock",
        "docs/REPRODUCTION_REPORT.md",
        "docs/CITATION_GRAPH.json",
        "context/references.bib",
        "context/assumptions_registry.yaml",
        "scripts/quality_gate.py",
    ]
    with zipfile.ZipFile("diamond_submission_pack.zip", "w") as z:
        for f in files:
            resolved = resolve_path(f)
            if resolved.exists():
                # Store relative to root in zip
                z.write(resolved, arcname=f)
    logger.success("Final Diamond Pack Created.")


if __name__ == "__main__":
    create_final_pack()
