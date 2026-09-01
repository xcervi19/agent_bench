"""Read-side helpers shared by the owner API and the public share API (#40).

Both routers serve the same files off the same run directories; only the
authorization in front of them differs. Keeping the path resolution here means a
change to the artifact layout cannot make the two views disagree — and, more to
the point, cannot leave the public view reading from somewhere the owner view
does not.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse

from ..config import ClaudeAgentSettings
from .db import session_scope
from .models import Topic

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


async def advance_public_view(
    topic_id: uuid.UUID, *, deliver_run_id: str | None = None
) -> None:
    """Move the public view forward — called only after work has finished (#50).

    A live shared topic keeps running, so a reader has to be shown *some*
    consistent state while the next cycle is in flight. That state is whatever
    completed last, and this is the single place it advances:

      * `run_deliver` succeeded  -> point the public view at the new report;
      * a refresh cycle completed -> the report is the same file, but the topic
        now says something newer, so only the stamp moves.

    Nothing calls this on failure. A deliver that crashes leaves the previous
    report shared and readable rather than replacing it with 404s, which is the
    behaviour you want on a link that is already in somebody's inbox.
    """
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        if row is None:
            return
        if deliver_run_id is not None:
            row.public_deliver_run_id = deliver_run_id
        row.public_updated_at = datetime.now(timezone.utc)
