import bibtexparser
import yaml


def check_linkage():
    with open("context/assumptions_registry.yaml") as f:
        assumptions = yaml.safe_load(f)["assumptions"]

    with open("context/references.bib") as f:
        bib_db = bibtexparser.load(f)
        bib_keys = [entry["ID"] for entry in bib_db.entries]

    print(f"Loaded {len(bib_keys)} BibTeX keys.")

    errors = 0
    for aid, data in assumptions.items():
        for ref in data.get("evidence_basis", []):
            if not ref:
                continue
            if ref not in bib_keys:
                print(f"MISSING: Assumption {aid} references '{ref}' which is NOT in BibTeX.")
                errors += 1

    if errors == 0:
        print("RESULT: ALL REFERENCES VALIDATED.")
        return 0
    print(f"RESULT: {errors} DISCREPANCIES FOUND.")
    return 1


if __name__ == "__main__":
    import sys

    sys.exit(check_linkage())
