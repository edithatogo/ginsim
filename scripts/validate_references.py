#!/usr/bin/env python3
"""
Reference Validation Pipeline for Genetic Discrimination Policy Research

This script validates the bibliography (references.bib) against:
1. Completeness requirements
2. DOI format and resolution
3. Duplicate detection
4. Citation usage in project files
5. Orphaned entries (in bib but not cited)

Usage:
    python scripts/validate_references.py [--fix] [--report] [--doi-check]
"""

import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Optional imports
try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import BibTexWriter

    HAS_BIBTEXPARSER = True
except ImportError:
    HAS_BIBTEXPARSER = False
    print("Warning: bibtexparser not installed. Install with: pip install bibtexparser")

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: requests not installed. DOI validation disabled.")


@dataclass
class ValidationResult:
    """Holds validation results for a single entry."""

    entry_id: str
    entry_type: str
    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.is_valid = False

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def add_suggestion(self, msg: str):
        self.suggestions.append(msg)


@dataclass
class ValidationReport:
    """Holds the complete validation report."""

    total_entries: int = 0
    valid_entries: int = 0
    invalid_entries: int = 0
    warnings: int = 0
    results: list[ValidationResult] = field(default_factory=list)
    orphaned_entries: list[str] = field(default_factory=list)
    missing_citations: list[str] = field(default_factory=list)
    duplicates: list[tuple[str, str]] = field(default_factory=list)

    def summary(self) -> str:
        """Generate summary string."""
        lines = [
            "=" * 60,
            "REFERENCE VALIDATION REPORT",
            "=" * 60,
            f"Total entries: {self.total_entries}",
            f"Valid: {self.valid_entries} ({self.valid_entries / self.total_entries * 100:.1f}%)",
            f"Invalid: {self.invalid_entries}",
            f"Warnings: {self.warnings}",
            f"Orphaned (in bib but not cited): {len(self.orphaned_entries)}",
            f"Missing (cited but not in bib): {len(self.missing_citations)}",
            f"Duplicate pairs: {len(self.duplicates)}",
            "=" * 60,
        ]
        return "\n".join(lines)

    def detailed_report(self) -> str:
        """Generate detailed markdown report."""
        lines = [self.summary(), ""]

        if self.invalid_entries > 0:
            lines.append("## Invalid Entries")
            for result in self.results:
                if not result.is_valid:
                    lines.append(f"\n### {result.entry_id}")
                    lines.append(f"Type: {result.entry_type}")
                    if result.errors:
                        lines.append("**Errors:**")
                        for err in result.errors:
                            lines.append(f"- ❌ {err}")

        if self.warnings > 0:
            lines.append("\n## Warnings")
            for result in self.results:
                if result.warnings:
                    lines.append(f"\n### {result.entry_id}")
                    for warn in result.warnings:
                        lines.append(f"- ⚠️ {warn}")

        if self.orphaned_entries:
            lines.append("\n## Orphaned Entries (in bibliography but not cited)")
            for entry_id in self.orphaned_entries[:20]:  # Limit display
                lines.append(f"- `{entry_id}`")
            if len(self.orphaned_entries) > 20:
                lines.append(f"... and {len(self.orphaned_entries) - 20} more")

        if self.missing_citations:
            lines.append("\n## Missing Citations (cited but not in bibliography)")
            for citation in self.missing_citations[:20]:
                lines.append(f"- `{citation}`")
            if len(self.missing_citations) > 20:
                lines.append(f"... and {len(self.missing_citations) - 20} more")

        if self.duplicates:
            lines.append("\n## Potential Duplicates")
            for id1, id2 in self.duplicates:
                lines.append(f"- `{id1}` ↔ `{id2}`")

        return "\n".join(lines)


class ReferenceValidator:
    """Validates BibTeX references."""

    REQUIRED_FIELDS = {
        "article": ["author", "title", "year"],
        "book": ["author", "title", "year", "publisher"],
        "inbook": ["author", "title", "booktitle", "year"],
        "incollection": ["author", "title", "booktitle", "year"],
        "inproceedings": ["author", "title", "booktitle", "year"],
        "manual": ["author", "title", "year"],
        "mastersthesis": ["author", "title", "year", "school"],
        "phdthesis": ["author", "title", "year", "school"],
        "techreport": ["author", "title", "year", "institution"],
        "unpublished": ["author", "title", "year", "note"],
        "misc": ["author", "title", "year"],
        "report": ["author", "title", "year", "institution"],
    }

    def __init__(self, bib_file: Path, project_root: Path):
        self.bib_file = bib_file
        self.project_root = project_root
        self.bib_database = None
        self.cited_keys = set()

    def load_bibliography(self) -> bool:
        """Load the BibTeX file."""
        if not HAS_BIBTEXPARSER:
            print("Error: bibtexparser not installed")
            return False

        if not self.bib_file.exists():
            print(f"Error: Bibliography file not found: {self.bib_file}")
            return False

        with open(self.bib_file, encoding="utf-8") as f:
            parser = BibTexParser()
            parser.ignore_nonstandard_types = False
            self.bib_database = bibtexparser.load(f, parser)

        print(f"Loaded {len(self.bib_database.entries)} entries from {self.bib_file.name}")
        return True

    def find_citations_in_project(self) -> set:
        """Find all citation keys used in project files."""
        cited = set()

        # Patterns for LaTeX citations
        latex_patterns = [
            r"\\cite\{([^}]+)\}",
            r"\\citep\{([^}]+)\}",
            r"\\citet\{([^}]+)\}",
            r"\\citeauthor\{([^}]+)\}",
            r"\\parencite\{([^}]+)\}",
        ]

        # Patterns for markdown citations (Pandoc style)
        md_patterns = [
            r"\[@([a-zA-Z0-9_:]+)\]",
        ]

        # Search these file types
        file_patterns = ["*.md", "*.tex", "*.py", "*.yaml", "*.yml", "*.bib"]

        for pattern in file_patterns:
            for file_path in self.project_root.rglob(pattern):
                # Skip outputs and .git
                if "outputs" in str(file_path) or ".git" in str(file_path):
                    continue

                try:
                    with open(file_path, encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                        # Check LaTeX patterns
                        for latex_pattern in latex_patterns:
                            matches = re.findall(latex_pattern, content)
                            for match in matches:
                                # Handle multiple citations in one \cite{}
                                keys = [k.strip() for k in match.split(",")]
                                cited.update(keys)

                        # Check markdown patterns
                        for md_pattern in md_patterns:
                            matches = re.findall(md_pattern, content)
                            cited.update(matches)

                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")

        self.cited_keys = cited
        print(f"Found {len(cited)} unique citations in project files")
        return cited

    def validate_entry(self, entry: dict) -> ValidationResult:
        """Validate a single bibliography entry."""
        result = ValidationResult(
            entry_id=entry.get("ID", "UNKNOWN"),
            entry_type=entry.get("ENTRYTYPE", "unknown"),
        )

        entry_type = entry.get("ENTRYTYPE", "misc").lower()
        required = self.REQUIRED_FIELDS.get(entry_type, ["author", "title", "year"])

        # Check required fields
        for field in required:
            if field not in entry or not entry[field].strip():
                result.add_error(f"Missing required field: {field}")

        # Check for at least one identifier
        has_identifier = any(f in entry for f in ["doi", "url", "isbn", "issn"])
        if not has_identifier and entry_type in ["article", "book", "inproceedings"]:
            result.add_warning("No DOI, URL, ISBN, or ISSN provided")

        # Validate DOI format
        if "doi" in entry:
            doi = entry["doi"]
            if not doi.startswith("10."):
                result.add_error(f"Invalid DOI format: {doi}")
            elif not re.match(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", doi, re.IGNORECASE):
                result.add_warning(f"DOI may be malformed: {doi}")

        # Check author format
        if "author" in entry:
            author = entry["author"]
            if " and " in author:
                authors = [a.strip() for a in author.split(" and ")]
                if len(authors) > 10:
                    result.add_suggestion("Consider using 'and others' for >10 authors")
            elif "," not in author and len(author.split()) < 3:
                result.add_warning(f"Author name may be incomplete: {author}")

        # Check year
        if "year" in entry:
            year = entry["year"]
            if not year.isdigit() and not year.startswith("-"):
                result.add_warning(f"Year may be invalid: {year}")
            elif year.isdigit() and (int(year) < 1900 or int(year) > 2100):
                result.add_warning(f"Year seems unusual: {year}")

        # Check title capitalization (optional suggestion)
        if "title" in entry:
            title = entry["title"]
            if title.isupper():
                result.add_suggestion("Title is all caps; consider sentence case")

        return result

    def detect_duplicates(self) -> list[tuple[str, str]]:
        """Detect potential duplicate entries."""
        duplicates = []
        entries = self.bib_database.entries if self.bib_database else []

        # Group by DOI
        by_doi = {}
        for entry in entries:
            if "doi" in entry:
                doi = entry["doi"].lower()
                if doi in by_doi:
                    duplicates.append((by_doi[doi], entry.get("ID", "UNKNOWN")))
                else:
                    by_doi[doi] = entry.get("ID", "UNKNOWN")

        # Group by title similarity (simple hash)
        by_title_hash = {}
        for entry in entries:
            if "title" in entry:
                # Normalize title: lowercase, remove punctuation
                title = entry["title"].lower()
                title = re.sub(r"[^\w\s]", "", title)
                title_hash = hashlib.md5(title.encode()).hexdigest()

                if title_hash in by_title_hash:
                    duplicates.append((by_title_hash[title_hash], entry.get("ID", "UNKNOWN")))
                else:
                    by_title_hash[title_hash] = entry.get("ID", "UNKNOWN")

        return duplicates

    def validate_doi_resolution(self, entry: dict, timeout: float = 2.0) -> bool:
        """Validate DOI by resolving it via doi.org."""
        if not HAS_REQUESTS:
            return False

        if "doi" not in entry:
            return False

        doi = entry["doi"]
        url = f"https://doi.org/{doi}"

        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            return response.status_code == 200
        except Exception:
            return False

    def run_full_validation(self, check_doi: bool = False) -> ValidationReport:
        """Run complete validation."""
        report = ValidationReport()

        if not self.bib_database:
            if not self.load_bibliography():
                report.add_error("Could not load bibliography")
                return report

        # Find citations in project
        self.find_citations_in_project()

        # Validate each entry
        for entry in self.bib_database.entries:
            result = self.validate_entry(entry)

            # Optional DOI resolution check
            if check_doi and "doi" in entry:
                if not self.validate_doi_resolution(entry):
                    result.add_warning(f"DOI resolution failed: {entry['doi']}")

            report.results.append(result)
            report.total_entries += 1

            if result.is_valid:
                report.valid_entries += 1
            else:
                report.invalid_entries += 1

            report.warnings += len(result.warnings)

        # Find orphaned entries
        entry_ids = {e.get("ID", "") for e in self.bib_database.entries}
        report.orphaned_entries = list(entry_ids - self.cited_keys)

        # Find missing citations
        report.missing_citations = list(self.cited_keys - entry_ids)

        # Detect duplicates
        report.duplicates = self.detect_duplicates()

        return report

    def fix_common_issues(self) -> dict:
        """Auto-fix common issues and return fixed entries."""
        fixed_count = 0

        for entry in self.bib_database.entries:
            # Fix DOI: remove https://doi.org/ prefix if present
            if "doi" in entry:
                doi = entry["doi"]
                if doi.startswith("https://doi.org/"):
                    entry["doi"] = doi.replace("https://doi.org/", "")
                    fixed_count += 1
                elif doi.startswith("http://dx.doi.org/"):
                    entry["doi"] = doi.replace("http://dx.doi.org/", "")
                    fixed_count += 1

            # Fix year: remove brackets if present
            if "year" in entry:
                year = entry["year"].strip()
                if year.startswith("{") and year.endswith("}"):
                    entry["year"] = year[1:-1]
                    fixed_count += 1

            # Standardize entry type
            if "ENTRYTYPE" in entry:
                entry["ENTRYTYPE"] = entry["ENTRYTYPE"].lower()
                fixed_count += 1

        print(f"Auto-fixed {fixed_count} common issues")
        return {"fixed_count": fixed_count}

    def write_fixed_bibliography(self, output_file: Path):
        """Write the (possibly fixed) bibliography to a new file."""
        if not self.bib_database:
            return False

        writer = BibTexWriter()
        writer.indent = "  "
        writer.order_entries_by = "ID"

        with open(output_file, "w", encoding="utf-8") as f:
            bibtexparser.dump(self.bib_database, f)

        print(f"Wrote fixed bibliography to {output_file}")
        return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate research bibliography")
    parser.add_argument("--bib-file", default="context/references.bib", help="Path to BibTeX file")
    parser.add_argument("--fix", action="store_true", help="Auto-fix common issues")
    parser.add_argument(
        "--doi-check", action="store_true", help="Validate DOIs by resolving them (slow)"
    )
    parser.add_argument("--report", action="store_true", help="Generate detailed markdown report")
    parser.add_argument(
        "--output", default="docs/REFERENCE_VALIDATION_REPORT.md", help="Output path for report"
    )

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    bib_file = project_root / args.bib_file

    print("=" * 60)
    print("REFERENCE VALIDATION PIPELINE")
    print("=" * 60)

    validator = ReferenceValidator(bib_file, project_root)

    if not validator.load_bibliography():
        sys.exit(1)

    # Run validation
    print("\nRunning validation...")
    report = validator.run_full_validation(check_doi=args.doi_check)

    print("\n" + report.summary())

    # Auto-fix if requested
    if args.fix:
        print("\nAuto-fixing common issues...")
        fix_result = validator.fix_common_issues()
        validator.write_fixed_bibliography(bib_file)
        print(f"Fixed {fix_result['fixed_count']} issues in {bib_file}")

    # Generate report if requested
    if args.report:
        output_path = project_root / args.output
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report.detailed_report())
        print(f"\nDetailed report saved to: {output_path}")

    # Exit with error if critical issues found
    if report.invalid_entries > 0:
        print(f"\n❌ Validation failed: {report.invalid_entries} invalid entries")
        sys.exit(1)
    elif report.warnings > 0:
        print(f"\n⚠️ Validation passed with warnings: {report.warnings} warnings")
        sys.exit(0)
    else:
        print("\n✅ Validation passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
