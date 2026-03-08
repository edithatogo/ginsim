#!/usr/bin/env python3
"""
Initialize a research-grade development track from the repository template.

Usage:
    python -m scripts.create_research_track \
        --track-id gdpe_0022_example \
        --title "Example title" \
        --aspect "example repo aspect"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.path_resolver import resolve_path

TEMPLATE_DIR = resolve_path("conductor/templates/nature_depth_cycle")
TRACKS_DIR = resolve_path("conductor/tracks")
TRACKS_REGISTRY = resolve_path("conductor/tracks.md")


def slugify_title(title: str) -> str:
    """Create a filesystem-safe slug from a title."""
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return slug or "untitled_track"


def render_template(template_text: str, replacements: dict[str, str]) -> str:
    """Replace template placeholders in text content."""
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace(f"<{key}>", value)
    return rendered


def build_index(track_id: str, title: str) -> str:
    """Build a default track index file."""
    return (
        "\n".join(
            [
                f"# Track index: {track_id}",
                "",
                f"## {title}",
                "",
                "- [Specification](./spec.md)",
                "- [Plan](./plan.md)",
                "- [Metadata](./metadata.json)",
                "- [Development Cycle](./AUTONOMOUS_CYCLE.md)",
                "- [Handoff](./HANDOFF.md)",
                "- [Track Complete](./TRACK_COMPLETE.md)",
                "",
                "## Expected phase artifacts",
                "",
                "- `track_refinement_round_1.md` through `track_refinement_round_5.md` as needed",
                "- `phase_0_review.md`",
                "- `phase_1_review.md`",
                "- `phase_2_review.md`",
                "- `phase_3_review.md`",
                "- `phase_4_review.md`",
                "",
                "## Current status",
                "",
                "- Planned.",
                "- Created from the standard research template.",
            ]
        )
        + "\n"
    )


def build_placeholder_artifact(title: str) -> str:
    """Create a simple placeholder markdown artifact."""
    return (
        "\n".join(
            [
                f"# {title}",
                "",
                "Status: pending",
                "",
                "Populate this file during track execution.",
            ]
        )
        + "\n"
    )


def update_tracks_registry(track_id: str, title: str, status: str) -> None:
    """Insert the generated track into the requested registry section."""
    if not TRACKS_REGISTRY.exists():
        return

    registry_text = TRACKS_REGISTRY.read_text(encoding="utf-8")
    normalized_status = status.strip().lower()
    if normalized_status not in {"planned", "active"}:
        msg = f"Unsupported track status: {status}"
        raise ValueError(msg)

    section_title = "## Planned Tracks" if normalized_status == "planned" else "## Active Tracks"
    replacement_status = "Planned" if normalized_status == "planned" else "Active"
    empty_row = "| _None_ | | | |"
    new_row = (
        f"| {track_id} | {title} | {replacement_status} | [track](./tracks/{track_id}/index.md) |"
    )

    if new_row in registry_text:
        return

    section_start = registry_text.find(section_title)
    if section_start == -1:
        msg = f"Could not find registry section: {section_title}"
        raise ValueError(msg)

    next_section = registry_text.find("\n## ", section_start + len(section_title))
    section_end = len(registry_text) if next_section == -1 else next_section
    section_block = registry_text[section_start:section_end]

    if empty_row in section_block:
        section_block = section_block.replace(empty_row, new_row, 1)
    else:
        section_block = section_block.rstrip() + "\n" + new_row + "\n"

    registry_text = registry_text[:section_start] + section_block + registry_text[section_end:]

    TRACKS_REGISTRY.write_text(registry_text, encoding="utf-8")


def instantiate_track(
    track_id: str,
    title: str,
    aspect: str,
    estimate: str,
    status: str,
) -> Path:
    """Create a new track directory from the template."""
    track_dir = TRACKS_DIR / track_id
    if track_dir.exists():
        msg = f"Track directory already exists: {track_dir}"
        raise FileExistsError(msg)

    track_dir.mkdir(parents=True, exist_ok=False)

    replacements = {
        "track_id": track_id,
        "title": title,
        "repo_aspect": aspect,
        "yyyy-mm-dd": date.today().isoformat(),
        "estimate": estimate,
        "status": status.lower(),
        "phase": "phase_0",
        "artifact": "spec.md / plan.md",
        "change_1": "<change_1>",
        "change_2": "<change_2>",
        "next_action_1": "Run track refinement round 1",
        "next_action_2": "Incorporate refinements into spec.md and plan.md",
        "next_action_3": "Begin Phase 0 review",
        "local_verification": "not yet run",
        "remote_verification": "not yet run",
        "streamlit_verification": "not yet run",
        "next_track_id": "<next_track_id>",
        "sha": "<sha>",
        "why": "<why>",
        "risk_1": "<risk_1>",
        "risk_2": "<risk_2>",
        "effect_1": "<effect_1>",
        "effect_2": "<effect_2>",
        "closed_item_1": "<closed_item_1>",
        "closed_item_2": "<closed_item_2>",
    }

    template_map = {
        "spec.template.md": "spec.md",
        "plan.template.md": "plan.md",
        "metadata.template.json": "metadata.json",
        "AUTONOMOUS_CYCLE.md": "AUTONOMOUS_CYCLE.md",
        "HANDOFF.template.md": "HANDOFF.md",
        "TRACK_CLOSEOUT.template.md": "TRACK_COMPLETE.md",
    }

    for source_name, dest_name in template_map.items():
        source_path = TEMPLATE_DIR / source_name
        dest_path = track_dir / dest_name
        if not source_path.exists():
            continue
        content = source_path.read_text(encoding="utf-8")
        dest_path.write_text(render_template(content, replacements), encoding="utf-8")

    reflection_template = TEMPLATE_DIR / "TEMPLATE_REFLECTION_LOG.md"
    if reflection_template.exists():
        (track_dir / "TEMPLATE_REFLECTION_LOG.seed.md").write_text(
            reflection_template.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    (track_dir / "index.md").write_text(build_index(track_id, title), encoding="utf-8")

    for round_number in range(1, 6):
        (track_dir / f"track_refinement_round_{round_number}.md").write_text(
            build_placeholder_artifact(f"Track Refinement Round {round_number}"),
            encoding="utf-8",
        )

    for phase_number in range(5):
        (track_dir / f"phase_{phase_number}_review.md").write_text(
            build_placeholder_artifact(f"Phase {phase_number} Review"),
            encoding="utf-8",
        )

    metadata_path = track_dir / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["track_id"] = track_id
        metadata["title"] = title
        metadata["aspect"] = aspect
        metadata["status"] = status.lower()
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    update_tracks_registry(track_id, title, status)

    return track_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a research development track from the repository template."
    )
    parser.add_argument(
        "--track-id", required=True, help="Track identifier, e.g. gdpe_0022_example"
    )
    parser.add_argument("--title", required=True, help="Human-readable track title")
    parser.add_argument(
        "--aspect",
        required=True,
        help="Single repository aspect this track will cover in depth",
    )
    parser.add_argument(
        "--estimate",
        default="2-5 days",
        help="Estimated duration to write into the plan template",
    )
    parser.add_argument(
        "--status",
        default="planned",
        choices=["planned", "active"],
        help="Registry section to insert the track into",
    )
    args = parser.parse_args()

    track_dir = instantiate_track(
        track_id=args.track_id,
        title=args.title,
        aspect=args.aspect,
        estimate=args.estimate,
        status=args.status,
    )

    print(f"Created development track at: {track_dir}")
    print("Next steps:")
    print("1. Run 3-5 refinement rounds before implementation")
    print("2. Update spec.md and plan.md with aspect-specific findings")
    print("3. Start the implementation cycle")


if __name__ == "__main__":
    main()
