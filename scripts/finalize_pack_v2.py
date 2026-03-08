import sys
import zipfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.path_resolver import resolve_path


def create_v2_pack():
    files = [
        "README.md",
        "pyproject.toml",
        "uv.lock",
        "protocols/Protocol_GeneticDiscriminationPolicy_v2.0.md",
        "docs/METHODS_SECTION_DRAFT.md",
        "docs/EVIDENCE_TO_PRIORS_APPENDIX.md",
        "docs/REPRODUCTION_REPORT.md",
        "docs/CITATION_GRAPH.json",
        "docs/ARTEFACT_AUDIT.md",
        "docs/REVIEWER_NAVIGATION_MAP.md",
        "context/references.bib",
        "context/assumptions_registry.yaml",
        "scripts/quality_gate.py",
    ]
    with zipfile.ZipFile("diamond_submission_pack_v2.0.zip", "w") as z:
        for f in files:
            resolved = resolve_path(f)
            if resolved.exists():
                z.write(resolved, arcname=f)
    print("Final Diamond Pack v2.0 Created.")


if __name__ == "__main__":
    create_v2_pack()
