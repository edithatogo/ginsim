import os
import zipfile


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
        "scripts/conductor_gate.py",
    ]
    with zipfile.ZipFile("diamond_submission_pack_v2.0.zip", "w") as z:
        for f in files:
            if os.path.exists(f):
                z.write(f)
    print("Final Diamond Pack v2.0 Created.")


if __name__ == "__main__":
    create_v2_pack()
