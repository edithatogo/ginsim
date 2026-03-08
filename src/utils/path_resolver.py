"""
Central path resolver for genetic-discrimination-policy-econ.
Handles fallback between public and local_only directories.
"""

from __future__ import annotations

from pathlib import Path

def resolve_path(relative_path: str | Path) -> Path:
    """
    Resolve a path, checking for existence in the root directory 
    and falling back to local_only/ if not found.
    """
    path = Path(relative_path)
    
    # 1. Check if path already exists relative to current working directory
    if path.exists():
        return path.absolute()
    
    # 2. Check in local_only/
    local_path = Path("local_only") / path
    if local_path.exists():
        return local_path.absolute()
    
    # 3. Handle cases where the script might be running from a subdirectory (like scripts/)
    # Look for root by climbing up
    current = Path.cwd()
    for _ in range(3):
        if (current / path).exists():
            return (current / path).absolute()
        if (current / "local_only" / path).exists():
            return (current / "local_only" / path).absolute()
        current = current.parent
        
    # Return original path if not found (let the caller handle FileNotFoundError)
    return path.absolute()
