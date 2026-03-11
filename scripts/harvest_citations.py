import json
import sys
from pathlib import Path

import bibtexparser

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.utils.logging_config import setup_logging
from src.utils.path_resolver import resolve_path

setup_logging(level="INFO")


def harvest_citations():
    bib_path = resolve_path("context/references.bib")
    with open(bib_path, encoding="utf-8") as f:
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

    out_path = resolve_path("docs/CITATION_GRAPH.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)
    logger.success("Citation Graph Generated.")


if __name__ == "__main__":
    harvest_citations()
