from __future__ import annotations

import json
from typing import TYPE_CHECKING

from scripts.validate_references import ReferenceValidator

if TYPE_CHECKING:
    from pathlib import Path


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_reference_validator_resolves_aliases_and_internal_sources(tmp_path: Path) -> None:
    references_file = tmp_path / "study" / "references" / "references.json"
    alias_file = tmp_path / "study" / "references" / "reference_key_aliases.json"

    references_payload = {
        "references": [
            {"id": "mcguire2019"},
            {"id": "fsc2019"},
        ]
    }
    references_file.parent.mkdir(parents=True, exist_ok=True)
    references_file.write_text(json.dumps(references_payload), encoding="utf-8")
    alias_file.write_text(
        json.dumps(
            {
                "mcguire_perceived_discrimination_testing_2019": "mcguire2019",
                "Authors' analysis based on policy documents": None,
            }
        ),
        encoding="utf-8",
    )

    write_text(
        tmp_path / "context" / "evidence.yaml",
        'source: "mcguire_perceived_discrimination_testing_2019"\nsource: "Authors\' analysis based on policy documents"',
    )
    write_text(tmp_path / "docs" / "paper.md", "Policy summary [@fsc2019].\n")

    validator = ReferenceValidator(references_file, alias_file, tmp_path)
    report = validator.run()

    assert report.unresolved_keys == set()
    assert report.missing_alias_targets == {}
    assert report.resolved_keys == {"mcguire2019", "fsc2019"}
    assert report.internal_only_keys == {"Authors' analysis based on policy documents"}
    assert report.unused_reference_ids == set()


def test_reference_validator_reports_unresolved_keys(tmp_path: Path) -> None:
    references_file = tmp_path / "study" / "references" / "references.json"
    alias_file = tmp_path / "study" / "references" / "reference_key_aliases.json"
    references_file.parent.mkdir(parents=True, exist_ok=True)
    references_file.write_text(
        json.dumps({"references": [{"id": "mcguire2019"}]}), encoding="utf-8"
    )
    alias_file.write_text("{}", encoding="utf-8")

    write_text(
        tmp_path / "configs" / "calibration.yaml",
        'source: "unknown_reference_key_2026"\n',
    )

    validator = ReferenceValidator(references_file, alias_file, tmp_path)
    report = validator.run()

    assert report.unresolved_keys == {"unknown_reference_key_2026"}
    assert report.resolved_keys == set()
    assert report.unused_reference_ids == {"mcguire2019"}
