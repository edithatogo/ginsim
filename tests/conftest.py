#!/usr/bin/env python3
"""
Pytest configuration for tests.
"""

import sys
from pathlib import Path

# Set non-interactive matplotlib backend before importing pyplot
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
