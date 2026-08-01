"""Read-side helpers shared by the owner API and the public share API (#40).

Both routers serve the same files off the same run directories; only the
authorization in front of them differs. Keeping the path resolution here means a
change to the artifact layout cannot make the two views disagree — and, more to
the point, cannot leave the public view reading from somewhere the owner view
does not.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse

from ..config import ClaudeAgentSettings

MEDIA_TYPES = {
    ".json": "application/json",
    ".md": "text/markdown; charset=utf-8",
}


def artifact_path(
    settings: ClaudeAgentSettings, topic_hash: str, run_id: str | None, filename: str
) -> Path:
    """Locate one artifact of one run. 404 when the stage has not written it yet."""
    if not run_id:
        raise HTTPException(status_code=404, detail=f"{filename} not produced yet")
    path = Path(settings.state_dir) / "news" / topic_hash / "runs" / run_id / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"{filename} not produced yet")
    return path


def artifact_response(
    settings: ClaudeAgentSettings, topic_hash: str, run_id: str | None, filename: str
) -> FileResponse:
    path = artifact_path(settings, topic_hash, run_id, filename)
    return FileResponse(str(path), media_type=MEDIA_TYPES.get(path.suffix, "application/json"))
