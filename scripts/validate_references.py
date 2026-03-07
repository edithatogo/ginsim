#!/usr/bin/env python3
"""
Reference validation pipeline for the genetic discrimination policy repo.

This validator treats `study/references/references.json` as the canonical
reference store. It scans manuscript-adjacent text plus YAML/config evidence
surfaces, resolves long-form evidence keys through an alias map, and reports:
1. unresolved reference keys;
2. canonical references not cited anywhere in scanned surfaces;
3. alias targets that point to missing canonical IDs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCAN_PATTERNS = ("*.md", "*.tex", "*.py", "*.yaml", "*.yml", "*.json")
SKIP_PARTS = {".git", ".venv", "outputs", "__pycache__", ".pytest_cache", ".mypy_cache"}

LATEX_PATTERNS = (
    r"\\cite\{([^}]+)\}",
    r"\\citep\{([^}]+)\}",
    r"\\citet\{([^}]+)\}",
    r"\\citeauthor\{([^}]+)\}",
    r"\\parencite\{([^}]+)\}",
)
MARKDOWN_PATTERNS = (r"\[@([A-Za-z0-9_:\-]+)\]",)
YAML_PATTERNS = (
    r'citation_key:\s*"([^"]+)"',
    r"citation_key:\s*'([^']+)'",
    r"citation_key:\s*([A-Za-z0-9_:\-]+)",
    r'source:\s*"([^"]+)"',
    r"source:\s*'([^']+)'",
)


@dataclass
class ValidationReport:
    references_count: int = 0
    files_scanned: int = 0
    raw_keys_count: int = 0
    resolved_keys: set[str] = field(default_factory=set)
    internal_only_keys: set[str] = field(default_factory=set)
    unresolved_keys: set[str] = field(default_factory=set)
    unused_reference_ids: set[str] = field(default_factory=set)
    missing_alias_targets: dict[str, str] = field(default_factory=dict)

    def summary(self) -> str:
        lines = [
            "=" * 60,
            "REFERENCE VALIDATION REPORT",
            "=" * 60,
            f"Canonical references: {self.references_count}",
            f"Files scanned: {self.files_scanned}",
            f"Raw keys found: {self.raw_keys_count}",
            f"Resolved canonical keys: {len(self.resolved_keys)}",
            f"Internal-only keys allowed: {len(self.internal_only_keys)}",
            f"Unresolved keys: {len(self.unresolved_keys)}",
            f"Unused canonical references: {len(self.unused_reference_ids)}",
            f"Broken alias targets: {len(self.missing_alias_targets)}",
            "=" * 60,
        ]
        return "\n".join(lines)

    def detailed_report(self) -> str:
        lines = [self.summary(), ""]

        if self.unresolved_keys:
            lines.append("## Unresolved keys")
            for key in sorted(self.unresolved_keys):
                lines.append(f"- `{key}`")
            lines.append("")

        if self.missing_alias_targets:
            lines.append("## Broken alias targets")
            for alias, target in sorted(self.missing_alias_targets.items()):
                lines.append(f"- `{alias}` -> `{target}` (missing canonical ID)")
            lines.append("")

        if self.internal_only_keys:
            lines.append("## Internal-only allowed keys")
            for key in sorted(self.internal_only_keys):
                lines.append(f"- `{key}`")
            lines.append("")

        if self.unused_reference_ids:
            lines.append("## Unused canonical references")
            for ref_id in sorted(self.unused_reference_ids):
                lines.append(f"- `{ref_id}`")
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"


class ReferenceValidator:
    def __init__(self, references_file: Path, alias_file: Path, project_root: Path):
        self.references_file = references_file
        self.alias_file = alias_file
        self.project_root = project_root
        self.reference_ids: set[str] = set()
        self.alias_map: dict[str, str | None] = {}
        self.files_scanned = 0

    def load_references(self) -> None:
        payload = json.loads(self.references_file.read_text(encoding="utf-8"))
        references = payload.get("references", [])
        self.reference_ids = {entry["id"] for entry in references}

    def load_alias_map(self) -> None:
        if not self.alias_file.exists():
            self.alias_map = {}
            return
        payload = json.loads(self.alias_file.read_text(encoding="utf-8"))
        self.alias_map = {str(key): value for key, value in payload.items()}

    def should_skip(self, path: Path) -> bool:
        return any(part in SKIP_PARTS for part in path.parts)

    def iter_scan_files(self) -> list[Path]:
        files: list[Path] = []
        for pattern in SCAN_PATTERNS:
            for path in self.project_root.rglob(pattern):
                if self.should_skip(path):
                    continue
                files.append(path)
        return sorted(set(files))

    def extract_raw_keys(self, text: str, suffix: str) -> set[str]:
        keys: set[str] = set()

        for pattern in LATEX_PATTERNS:
            for match in re.findall(pattern, text):
                for key in match.split(","):
                    cleaned = key.strip()
                    if cleaned:
                        keys.add(cleaned)

        for pattern in MARKDOWN_PATTERNS:
            for match in re.findall(pattern, text):
                cleaned = match.strip().rstrip(".,;:")
                if cleaned:
                    keys.add(cleaned)

        if suffix in {".yaml", ".yml", ".json"}:
            for pattern in YAML_PATTERNS:
                for match in re.findall(pattern, text):
                    cleaned = match.strip()
                    if cleaned:
                        keys.add(cleaned)

        return keys

    def normalize_source_value(self, key: str) -> list[str]:
        normalized = re.sub(r"\s*\([^)]*\)", "", key).strip()
        if not normalized:
            return []
        return [part.strip() for part in re.split(r"\s+\+\s+", normalized) if part.strip()]

    def resolve_key(self, key: str, report: ValidationReport) -> None:
        if key in self.reference_ids:
            report.resolved_keys.add(key)
            return

        alias_target = self.alias_map.get(key)
        if alias_target is None and key in self.alias_map:
            report.internal_only_keys.add(key)
            return

        if alias_target is not None:
            if alias_target in self.reference_ids:
                report.resolved_keys.add(alias_target)
                return
            report.missing_alias_targets[key] = alias_target
            report.unresolved_keys.add(key)
            return

        report.unresolved_keys.add(key)

    def run(self) -> ValidationReport:
        self.load_references()
        self.load_alias_map()

        report = ValidationReport(references_count=len(self.reference_ids))
        files = self.iter_scan_files()
        report.files_scanned = len(files)

        raw_keys: set[str] = set()
        for file_path in files:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            raw_keys.update(self.extract_raw_keys(text, file_path.suffix.lower()))

        report.raw_keys_count = len(raw_keys)

        normalized_keys: set[str] = set()
        for key in raw_keys:
            if key.startswith("10."):
                continue
            normalized_keys.update(self.normalize_source_value(key))

        for key in sorted(normalized_keys):
            self.resolve_key(key, report)

        report.unused_reference_ids = self.reference_ids - report.resolved_keys
        return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate canonical reference traceability")
    parser.add_argument(
        "--references-file",
        default="study/references/references.json",
        help="Path to canonical CSL-JSON reference file",
    )
    parser.add_argument(
        "--alias-file",
        default="study/references/reference_key_aliases.json",
        help="Path to JSON alias map from evidence/config keys to canonical CSL IDs",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Write a detailed markdown report",
    )
    parser.add_argument(
        "--output",
        default="docs/REFERENCE_VALIDATION_REPORT.md",
        help="Output path for detailed markdown report",
    )
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    references_file = project_root / args.references_file
    alias_file = project_root / args.alias_file

    if not references_file.exists():
        print(f"ERROR: canonical references file not found: {references_file}")
        sys.exit(1)

    validator = ReferenceValidator(references_file, alias_file, project_root)
    report = validator.run()

    print(report.summary())

    if args.report:
        output_path = project_root / args.output
        output_path.write_text(report.detailed_report(), encoding="utf-8")
        print(f"Detailed report saved to: {output_path}")

    if report.unresolved_keys or report.missing_alias_targets:
        print("Validation failed: unresolved or broken reference mappings remain.")
        sys.exit(1)

    print("Validation passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
