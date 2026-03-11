import sys
import zipfile
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging
from src.utils.path_resolver import resolve_path

setup_logging(level="INFO")


def prepare_submission():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    zip_name = f"submission_package_{timestamp}.zip"

    files_to_include = [
        "README.md",
        "pyproject.toml",
        "uv.lock",
        "context/references.bib",
        "context/assumptions_registry.yaml",
        "docs/REVIEWER_NAVIGATION_MAP.md",
    ]

    logger.info(f"Creating submission package: {zip_name}...")
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for f in files_to_include:
            resolved = resolve_path(f)
            if resolved.exists():
                zipf.write(resolved, arcname=f)

    logger.success("RESULT: SUCCESS")


if __name__ == "__main__":
    prepare_submission()
