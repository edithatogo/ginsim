import json
from pathlib import Path


def sync_registry():
    tracks_dir = Path("conductor/tracks")
    registry_path = Path("conductor/tracks.md")

    print(f"Syncing registry from {tracks_dir} to {registry_path}...")

    tracks = []
    for track_folder in tracks_dir.iterdir():
        if track_folder.is_dir():
            metadata_file = track_folder / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    tracks.append(json.load(f))

    # Sort tracks by ID or Date if available
    # For now, just a basic list update
    print(f"Found {len(tracks)} tracks in metadata.")
    # In a full implementation, we would rewrite the Markdown table in tracks.md


if __name__ == "__main__":
    sync_registry()
