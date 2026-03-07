import zipfile
import os
from pathlib import Path

def create_final_pack():
    files = [
        "README.md", "pyproject.toml", "uv.lock",
        "docs/REPRODUCTION_REPORT.md", "docs/CITATION_GRAPH.json",
        "context/references.bib", "context/assumptions_registry.yaml",
        "scripts/conductor_gate.py"
    ]
    with zipfile.ZipFile("diamond_submission_pack.zip", "w") as z:
        for f in files:
            if os.path.exists(f): z.write(f)
    print("Final Diamond Pack Created.")

if __name__ == "__main__": create_final_pack()
