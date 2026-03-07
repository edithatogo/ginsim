from __future__ import annotations

import json

from scripts import create_nature_depth_track


def test_instantiate_track_creates_seeded_artifacts_and_updates_registry(
    tmp_path, monkeypatch
) -> None:
    conductor_dir = tmp_path / "conductor"
    templates_dir = conductor_dir / "templates" / "nature_depth_cycle"
    tracks_dir = conductor_dir / "tracks"
    registry_path = conductor_dir / "tracks.md"

    templates_dir.mkdir(parents=True)
    tracks_dir.mkdir(parents=True)

    template_files = {
        "spec.template.md": "# Track Specification: <title>\n**Track ID:** <track_id>\n**Aspect:** <repo_aspect>\n",
        "plan.template.md": "# Plan for <track_id>\n**Estimated duration:** <estimate>\n",
        "metadata.template.json": json.dumps(
            {
                "track_id": "<track_id>",
                "title": "<title>",
                "aspect": "<repo_aspect>",
                "status": "planned",
            }
        ),
        "AUTONOMOUS_CYCLE.md": "# Cycle\n",
        "HANDOFF.template.md": "# Handoff for <track_id>\nStatus: <status>\n",
        "TRACK_CLOSEOUT.template.md": "# Closeout for <track_id>\n",
        "TEMPLATE_REFLECTION_LOG.md": "# Reflection log\n",
    }

    for filename, content in template_files.items():
        (templates_dir / filename).write_text(content, encoding="utf-8")

    registry_path.write_text(
        "# Tracks registry\n\n## Active Tracks\n\n| Track ID | Title | Status | Link |\n|---|---|---|---|\n| _None_ | | | |\n\n## Planned Tracks\n\n| Track ID | Title | Status | Link |\n|---|---|---|---|\n| _None_ | | | |\n\n## Completed Follow-up Tracks"
        "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(create_nature_depth_track, "TEMPLATE_DIR", templates_dir)
    monkeypatch.setattr(create_nature_depth_track, "TRACKS_DIR", tracks_dir)
    monkeypatch.setattr(create_nature_depth_track, "TRACKS_REGISTRY", registry_path)

    track_dir = create_nature_depth_track.instantiate_track(
        track_id="gdpe_1234_test_track",
        title="Test Track",
        aspect="generator coverage",
        estimate="1 day",
        status="active",
    )

    assert track_dir.exists()
    assert (track_dir / "spec.md").read_text(encoding="utf-8").find("Test Track") != -1
    assert (track_dir / "plan.md").read_text(encoding="utf-8").find("1 day") != -1
    assert (track_dir / "AUTONOMOUS_CYCLE.md").exists()
    assert (track_dir / "HANDOFF.md").exists()
    assert (track_dir / "TRACK_COMPLETE.md").exists()
    assert (track_dir / "TEMPLATE_REFLECTION_LOG.seed.md").exists()

    for round_number in range(1, 6):
        assert (track_dir / f"track_refinement_round_{round_number}.md").exists()

    for phase_number in range(5):
        assert (track_dir / f"phase_{phase_number}_review.md").exists()

    metadata = json.loads((track_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["track_id"] == "gdpe_1234_test_track"
    assert metadata["title"] == "Test Track"
    assert metadata["aspect"] == "generator coverage"
    assert metadata["status"] == "active"

    registry_text = registry_path.read_text(encoding="utf-8")
    assert "| gdpe_1234_test_track | Test Track | Active |" in registry_text
    active_section = registry_text.split("## Active Tracks", maxsplit=1)[1].split(
        "## Planned Tracks", maxsplit=1
    )[0]
    assert "| _None_ | | | |" not in active_section


def test_conductor_tracking_files_are_not_ignored() -> None:
    tracked_paths = [
        "conductor/index.md",
        "conductor/workflow.md",
        "conductor/templates/README.md",
        "conductor/templates/nature_depth_cycle/README.md",
    ]
    gitignore_text = (create_nature_depth_track.REPO_ROOT / ".gitignore").read_text(
        encoding="utf-8"
    )

    for tracked_path in tracked_paths:
        assert f"!{tracked_path}" in gitignore_text or tracked_path.startswith(
            "conductor/templates/"
        )
