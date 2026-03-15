"""
Summarise downloaded Streamlit Cloud logs into distinct error signatures.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.utils.streamlit_cloud_logs import summarise_streamlit_cloud_log


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "log_path", type=Path, help="Path to a downloaded Streamlit log file or zip"
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Optional output path for the JSON summary",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    findings = summarise_streamlit_cloud_log(args.log_path)
    summary = [finding.to_dict() for finding in findings]

    if args.json_output is not None:
        args.json_output.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
