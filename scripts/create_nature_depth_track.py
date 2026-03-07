#!/usr/bin/env python3
"""
Instantiate a Conductor nature-depth-cycle track from the repo template.

Usage:
    python -m scripts.create_nature_depth_track \
        --track-id gdpe_0022_example \
        --title "Example title" \
        --aspect "example repo aspect"
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO_ROOT / "conductor" / "templates" / "nature_depth_cycle"
TRACKS_DIR = REPO_ROOT / "conductor" / "tracks"
TRACKS_REGISTRY = REPO_ROOT / "conductor" / "tracks.md"


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
    return "\n".join(
        [
            f"# Track index: {track_id}",
            "",
            f"## {title}",
            "",
            "- [Specification](./spec.md)",
            "- [Plan](./plan.md)",
            "- [Metadata](./metadata.json)",
            "- [Autonomous Cycle](./AUTONOMOUS_CYCLE.md)",
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
            "- Created from the `nature_depth_cycle` template.",
        ]
    ) + "\n"


def build_placeholder_artifact(title: str) -> str:
    """Create a simple placeholder markdown artifact."""
    return "\n".join(
        [
            f"# {title}",
            "",
            "Status: pending",
            "",
            "Populate this file during track execution.",
        ]
    ) + "\n"


def update_tracks_registry(track_id: str, title: str) -> None:
    """Insert the generated track into the Planned Tracks table."""
    registry_text = TRACKS_REGISTRY.read_text(encoding="utf-8")
    planned_none_row = "| _None_ | | | |"
    new_row = (
        f"| {track_id} | {title} | Planned | "
        f"[track](./tracks/{track_id}/index.md) |"
    )

    if new_row in registry_text:
        return

    if planned_none_row in registry_text:
        registry_text = registry_text.replace(planned_none_row, new_row)
    else:
        marker = "## Completed Follow-up Tracks"
        insertion = f"{new_row}\n\n{marker}"
        registry_text = registry_text.replace(marker, insertion)

    TRACKS_REGISTRY.write_text(registry_text, encoding="utf-8")


def instantiate_track(
    track_id: str,
    title: str,
    aspect: str,
    estimate: str,
) -> Path:
    """Create a new track directory from the template."""
    track_dir = TRACKS_DIR / track_id
    if track_dir.exists():
        raise FileExistsError(f"Track directory already exists: {track_dir}")

    track_dir.mkdir(parents=True, exist_ok=False)

    replacements = {
        "track_id": track_id,
        "title": title,
        "repo_aspect": aspect,
        "yyyy-mm-dd": date.today().isoformat(),
        "estimate": estimate,
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
        "TRACK_CLOSEOUT.template.md": "TRACK_COMPLETE.md",
    }

    for source_name, dest_name in template_map.items():
        source_path = TEMPLATE_DIR / source_name
        dest_path = track_dir / dest_name
        content = source_path.read_text(encoding="utf-8")
        dest_path.write_text(render_template(content, replacements), encoding="utf-8")

    reflection_template = TEMPLATE_DIR / "TEMPLATE_REFLECTION_LOG.md"
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
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["track_id"] = track_id
    metadata["title"] = title
    metadata["aspect"] = aspect
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    update_tracks_registry(track_id, title)

    return track_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a Conductor nature-depth-cycle track from the repository template."
    )
    parser.add_argument("--track-id", required=True, help="Track identifier, e.g. gdpe_0022_example")
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
    args = parser.parse_args()

    track_dir = instantiate_track(
        track_id=args.track_id,
        title=args.title,
        aspect=args.aspect,
        estimate=args.estimate,
    )

    print(f"Created track template at: {track_dir}")
    print("Next steps:")
    print("1. Run 3-5 track refinement rounds before implementation")
    print("2. Update spec.md and plan.md with aspect-specific findings")
    print("3. Start the autonomous phase loop")


if __name__ == "__main__":
    main()
