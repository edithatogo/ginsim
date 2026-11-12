import re
import sys
from pathlib import Path

ENTRY_PATTERN = re.compile(r"@\w+\s*\{\s*[^,\s]+\s*,", re.MULTILINE)


def _has_balanced_braces(text: str) -> bool:
    depth = 0
    for char in text:
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def validate_bibtex(file_path: str) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: {file_path} not found.")
        return 1

    text = path.read_text(encoding="utf-8")
    entries = ENTRY_PATTERN.findall(text)

    if not entries:
        print(f"Warning: No BibTeX entries found in {file_path}")
        return 0

    if not _has_balanced_braces(text):
        print(f"BibTeX Validation Error in {file_path}: unbalanced braces detected")
        return 1

    print(f"Successfully validated {len(entries)} entries in {file_path}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_bibtex.py <path_to_bib>")
        sys.exit(1)
    sys.exit(validate_bibtex(sys.argv[1]))
