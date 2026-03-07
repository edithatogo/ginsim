from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(
    out_dir: Path,
    *,
    repo_root: Path,
    jurisdiction: str,
    domain: str,
    policies_file: Path,
    base_config_file: Path,
    notes: str,
    extra: dict[str, Any] | None = None,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)

    policies_file = Path(policies_file)
    base_config_file = Path(base_config_file)
    repo_root = Path(repo_root)

    payload: dict[str, Any] = {
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "jurisdiction": jurisdiction,
        "domain": domain,
        "repo_root": str(repo_root),
        "repo_tree_hash": None,
        "policies_file": str(policies_file).replace("\\", "/"),
        "policies_file_sha256": _sha256(policies_file),
        "base_config_file": str(base_config_file).replace("\\", "/"),
        "base_config_file_sha256": _sha256(base_config_file),
        "notes": notes,
    }
    if extra:
        payload.update(extra)

    manifest_path = out_dir / "run_manifest.json"
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return manifest_path
