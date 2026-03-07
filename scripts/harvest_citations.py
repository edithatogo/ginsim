import json

import bibtexparser


def harvest_citations():
    with open("context/references.bib", encoding="utf-8") as f:
        bib_db = bibtexparser.load(f)

    graph = {"total_references": len(bib_db.entries), "references": []}

    for entry in bib_db.entries:
        graph["references"].append(
            {
                "key": entry["ID"],
                "title": entry.get("title", "N/A"),
                "author": entry.get("author", "N/A"),
                "year": entry.get("year", "N/A"),
                "doi": entry.get("doi", "N/A"),
            }
        )

    with open("docs/CITATION_GRAPH.json", "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)
    print("Citation Graph Generated.")


if __name__ == "__main__":
    harvest_citations()
