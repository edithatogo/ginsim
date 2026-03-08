import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.path_resolver import resolve_path


def sync_registry():
    tracks_dir = resolve_path("conductor/tracks")
    registry_path = resolve_path("conductor/tracks.md")

    print(f"Syncing registry from {tracks_dir} to {registry_path}...")

    tracks = []
    if not tracks_dir.exists():
        print(f"Error: tracks_dir {tracks_dir} does not exist.")
        return

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
