import os
import zipfile
from datetime import datetime


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

    print(f"Creating submission package: {zip_name}...")
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for f in files_to_include:
            if os.path.exists(f):
                zipf.write(f)

    print("RESULT: SUCCESS")


if __name__ == "__main__":
    prepare_submission()
