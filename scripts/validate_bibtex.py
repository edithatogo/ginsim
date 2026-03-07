import sys
from pathlib import Path

import bibtexparser


def validate_bibtex(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: {file_path} not found.")
        return 1

    try:
        with open(path) as f:
            bib_db = bibtexparser.load(f)

        if not bib_db.entries:
            print(f"Warning: No entries found in {file_path}")
            return 0

        print(f"Successfully validated {len(bib_db.entries)} entries in {file_path}")
        return 0
    except Exception as e:
        print(f"BibTeX Validation Error in {file_path}: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_bibtex.py <path_to_bib>")
        sys.exit(1)
    sys.exit(validate_bibtex(sys.argv[1]))
