"""
Helpers for working with downloaded Streamlit Cloud logs.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from zipfile import ZipFile

ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")
TIMESTAMP_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[ T]")
EXCEPTION_SUMMARY_RE = re.compile(
    r"^[A-Za-z_][\w.]+(?:Error|Exception|Warning|Exit|Fault|Failure):"
)
ERROR_LINE_RE = re.compile(
    r"\b(?:Error installing requirements|Error running app|Traceback|[A-Za-z_][\w.]+(?:Error|Exception|Warning|Exit|Fault|Failure):)"
)
FRAME_RE = re.compile(r'File "([^"]+)", line \d+')


@dataclass(frozen=True)
class StreamlitLogFinding:
    signature: str
    count: int
    sources: tuple[str, ...]
    example: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _strip_ansi(text: str) -> str:
    return ANSI_ESCAPE_RE.sub("", text)


def _iter_text_payloads(path: Path) -> list[tuple[str, str]]:
    if path.suffix.lower() != ".zip":
        return [(path.name, path.read_text(encoding="utf-8", errors="replace"))]

    payloads: list[tuple[str, str]] = []
    with ZipFile(path) as archive:
        for member in archive.namelist():
            if member.endswith("/"):
                continue
            payloads.append((member, archive.read(member).decode("utf-8", errors="replace")))
    return payloads


def _looks_like_exception_summary(line: str) -> bool:
    return bool(EXCEPTION_SUMMARY_RE.match(line.strip()))


def _looks_like_error_line(line: str) -> bool:
    return bool(ERROR_LINE_RE.search(line.strip()))


def _looks_like_new_record(line: str) -> bool:
    cleaned = line.strip()
    return bool(cleaned and TIMESTAMP_PREFIX_RE.match(cleaned))


def _normalise_signature(block: str) -> str:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
        return "unknown-log-error"

    exception_line = next(
        (line for line in reversed(lines) if _looks_like_exception_summary(line)),
        lines[-1],
    )
    frame_line = next(
        (
            FRAME_RE.search(line).group(1)
            for line in lines
            if FRAME_RE.search(line) and ("streamlit_app/" in line or "src/" in line)
        ),
        "",
    )
    if frame_line:
        return f"{frame_line} -> {exception_line}"
    return exception_line


def _extract_blocks(text: str) -> list[str]:
    lines = [_strip_ansi(line.rstrip()) for line in text.splitlines()]
    blocks: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue

        if "Traceback (most recent call last):" in line:
            block_lines = [line]
            index += 1
            while index < len(lines):
                current = lines[index].rstrip()
                current_stripped = current.strip()
                if (
                    block_lines
                    and _looks_like_new_record(current_stripped)
                    and _looks_like_exception_summary(block_lines[-1])
                ):
                    break
                if (
                    current_stripped == ""
                    and block_lines
                    and _looks_like_exception_summary(block_lines[-1])
                ):
                    break
                if current_stripped:
                    block_lines.append(current_stripped)
                index += 1
            blocks.append("\n".join(block_lines))
            continue

        if _looks_like_error_line(line):
            blocks.append(line)

        index += 1

    return blocks


def summarise_streamlit_cloud_log(path: Path | str) -> list[StreamlitLogFinding]:
    resolved_path = Path(path)
    payloads = _iter_text_payloads(resolved_path)
    grouped_examples: dict[str, str] = {}
    grouped_sources: dict[str, set[str]] = defaultdict(set)
    counts: dict[str, int] = defaultdict(int)

    for source_name, text in payloads:
        for block in _extract_blocks(text):
            signature = _normalise_signature(block)
            counts[signature] += 1
            grouped_sources[signature].add(source_name)
            grouped_examples.setdefault(signature, block)

    findings = [
        StreamlitLogFinding(
            signature=signature,
            count=counts[signature],
            sources=tuple(sorted(grouped_sources[signature])),
            example=grouped_examples[signature],
        )
        for signature in counts
    ]
    return sorted(findings, key=lambda finding: (-finding.count, finding.signature))
