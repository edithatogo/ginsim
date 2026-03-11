import sys
from pathlib import Path

import bibtexparser

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging

setup_logging(level="INFO")


def validate_bibtex(file_path):
    path = Path(file_path)
    if not path.exists():
        logger.error(f"{file_path} not found.")
        return 1

    try:
        with open(path) as f:
            bib_db = bibtexparser.load(f)

        if not bib_db.entries:
            logger.warning(f"No entries found in {file_path}")
            return 0

        logger.success(f"Successfully validated {len(bib_db.entries)} entries in {file_path}")
        return 0
    except Exception as e:
        logger.error(f"BibTeX Validation Error in {file_path}: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python validate_bibtex.py <path_to_bib>")
        sys.exit(1)
    sys.exit(validate_bibtex(sys.argv[1]))
