from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PIPELINE_SCHEMA_VERSION = 1


def append_pipeline_step(
    text_root: Path,
    *,
    command: str,
    payload: dict,
) -> Path:
    text_root.mkdir(parents=True, exist_ok=True)
    path = text_root / "pipeline_run.json"
    if path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = {"schema_version": PIPELINE_SCHEMA_VERSION, "steps": []}
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    step = {"command": command, "at": data["updated_at"], **payload}
    data.setdefault("steps", []).append(step)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path
