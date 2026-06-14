"""Offline tests for the topic refresh scheduler (#22).

No DB and no network: the pure scheduling helpers are tested directly, and the
dispatch loop is exercised with stubbed claim/run functions.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
