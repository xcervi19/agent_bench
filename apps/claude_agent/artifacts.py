"""Reproducible run artifacts for Claude Agent stages.

Layout under ``state_dir`` (a host-mounted directory):

    <state_dir>/news/<topic_id>/index.json
    <state_dir>/news/<topic_id>/runs/<run_id>/request.json
    <state_dir>/news/<topic_id>/runs/<run_id>/stream.ndjson
    <state_dir>/news/<topic_id>/runs/<run_id>/raw_result.json
    <state_dir>/news/<topic_id>/runs/<run_id>/parsed.json
    <state_dir>/news/<topic_id>/runs/<run_id>/meta.json

Caching works off the ``input_fingerprint`` recorded in ``index.json``: if a
successful run with the same fingerprint already exists, the orchestrator
returns the cached ``parsed.json`` instead of calling Claude again.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _normalize_args(args: str) -> str:
    return " ".join((args or "").lower().split())


def _sha1_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def _sha1_str(s: str) -> str:
    return _sha1_bytes(s.encode("utf-8"))


def _write_json_atomic(path: Path, obj: Any) -> None:
    """Write JSON to ``path`` atomically (tmp file + rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False, sort_keys=False)
            f.write("\n")
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def topic_id_from_args(args: str) -> str:
    """Deterministic topic_id derived from the (normalized) topic string.

    Used for filesystem layout / cache keys. The model may emit its own
    ``topic_id`` inside the parsed business JSON; that is preserved as-is and
    is independent of the filesystem id.
    """
    return _sha1_str(_normalize_args(args))


def file_sha1(path: Path) -> str:
    """SHA-1 of the file at ``path``, or empty string if it does not exist."""
    if not path.exists() or not path.is_file():
        return ""
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_input_fingerprint(
    *,
    command: str,
    args: str,
    command_file_hash: str,
    schema_hash: str,
    schema_version: str,
    env_version: str,
    model: str | None,
    permission_mode: str | None,
) -> str:
    """Stable hash of every input that should force a fresh Claude call."""
    payload = {
        "command": command,
        "args": _normalize_args(args),
        "command_file_hash": command_file_hash,
        "schema_hash": schema_hash,
        "schema_version": schema_version,
        "env_version": env_version,
        "model": model or "",
        "permission_mode": permission_mode or "",
    }
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha1_bytes(blob)


def output_fingerprint(parsed: dict[str, Any] | None) -> str | None:
    if parsed is None:
        return None
    blob = json.dumps(parsed, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha1_bytes(blob)


def parse_business_result(raw_result: dict[str, Any] | None) -> dict[str, Any] | None:
    """Extract the parsed business JSON from a CLI ``type=result`` wrapper.

    The Claude CLI puts the agent's final stdout (a JSON string) in
    ``raw["result"]``. We only treat ``subtype == "success"`` as parseable.
    """
    if not isinstance(raw_result, dict):
        return None
    if raw_result.get("type") != "result":
        return None
    if raw_result.get("subtype") != "success":
        return None
    result_str = raw_result.get("result")
    if not isinstance(result_str, str):
        return None
    try:
        loaded = json.loads(result_str)
    except json.JSONDecodeError:
        return None
    return loaded if isinstance(loaded, dict) else None


@dataclass(slots=True)
class CachedRun:
    run_id: str
    topic_id: str
    parsed_path: Path
    meta_path: Path
    parsed: dict[str, Any] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)


class ArtifactStore:
    """File-backed store of staged Claude runs.

    Parameters
    ----------
    root:
        Absolute or repo-relative path where ``news/<topic_id>/...`` lives.
    index_path_prefix:
        Prefix used inside ``index.json`` for ``parsed_path`` so consumers can
        resolve a path relative to the project root (e.g. ``"state"``).
    """

    def __init__(self, root: Path, index_path_prefix: str = "state") -> None:
        self.root = Path(root)
        self.index_path_prefix = index_path_prefix.strip("/")

    def topic_dir(self, topic_id: str) -> Path:
        return self.root / "news" / topic_id

    def run_dir(self, topic_id: str, run_id: str) -> Path:
        return self.topic_dir(topic_id) / "runs" / run_id

    def index_path(self, topic_id: str) -> Path:
        return self.topic_dir(topic_id) / "index.json"

    def parsed_index_path(self, topic_id: str, run_id: str) -> str:
        prefix = f"{self.index_path_prefix}/" if self.index_path_prefix else ""
        return f"{prefix}news/{topic_id}/runs/{run_id}/parsed.json"

    def find_cached(self, topic_id: str, input_fingerprint: str) -> CachedRun | None:
        """Return a cached run for ``input_fingerprint`` if one exists."""
        index_path = self.index_path(topic_id)
        if not index_path.exists():
            return None
        try:
            idx = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        runs = idx.get("runs") or []
        for run in reversed(runs):
            if (
                run.get("status") == "succeeded"
                and run.get("input_fingerprint") == input_fingerprint
            ):
                run_id = run.get("run_id")
                if not run_id:
                    continue
                parsed_path = self.run_dir(topic_id, run_id) / "parsed.json"
                meta_path = self.run_dir(topic_id, run_id) / "meta.json"
                if not (parsed_path.exists() and meta_path.exists()):
                    continue
                try:
                    parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
                    meta = json.loads(meta_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                return CachedRun(
                    run_id=run_id,
                    topic_id=topic_id,
                    parsed_path=parsed_path,
                    meta_path=meta_path,
                    parsed=parsed,
                    meta=meta,
                )
        return None


class RunRecorder:
    """Captures a single run's artifacts on disk.

    Lifecycle:
      1. ``write_request(...)``
      2. ``open_stream()`` → ``append_stream_line(...)`` per CLI event
      3. ``finalize(...)`` writes raw_result, parsed, meta and updates index
    """

    def __init__(
        self,
        store: ArtifactStore,
        *,
        topic: str,
        topic_id: str,
        run_id: str,
        stage: str = "newsfind_queries",
        created_at: datetime | None = None,
    ) -> None:
        self.store = store
        self.topic = topic
        self.topic_id = topic_id
        self.run_id = run_id
        self.stage = stage
        self.created_at = created_at or _now_utc()
        self.dir = store.run_dir(topic_id, run_id)
        self.dir.mkdir(parents=True, exist_ok=True)
        self._stream_fp: TextIO | None = None

    @property
    def request_path(self) -> Path:
        return self.dir / "request.json"

    @property
    def stream_path(self) -> Path:
        return self.dir / "stream.ndjson"

    @property
    def raw_result_path(self) -> Path:
        return self.dir / "raw_result.json"

    @property
    def parsed_path(self) -> Path:
        return self.dir / "parsed.json"

    @property
    def meta_path(self) -> Path:
        return self.dir / "meta.json"

    def write_request(self, request_payload: dict[str, Any]) -> None:
        payload = {
            **request_payload,
            "created_at": _iso(self.created_at),
        }
        _write_json_atomic(self.request_path, payload)

    def open_stream(self) -> None:
        self._stream_fp = self.stream_path.open("w", encoding="utf-8", buffering=1)

    def append_stream_line(self, line: str) -> None:
        if self._stream_fp is None:
            return
        line = line.rstrip("\n").rstrip("\r")
        if not line:
            return
        self._stream_fp.write(line + "\n")
        self._stream_fp.flush()

    def close_stream(self) -> None:
        if self._stream_fp is not None:
            try:
                self._stream_fp.flush()
            finally:
                self._stream_fp.close()
                self._stream_fp = None

    def finalize(
        self,
        *,
        status: str,
        raw_result: dict[str, Any] | None,
        parsed: dict[str, Any] | None,
        input_fingerprint: str,
        model: str | None,
        cached: bool = False,
        finished_at: datetime | None = None,
        duration_ms: int | None = None,
        total_cost_usd: float | None = None,
        error: str | None = None,
    ) -> dict[str, Any]:
        """Write raw_result/parsed/meta and update the topic's index.json."""
        finished_at = finished_at or _now_utc()
        if raw_result is not None:
            _write_json_atomic(self.raw_result_path, raw_result)
        if parsed is not None:
            _write_json_atomic(self.parsed_path, parsed)
        meta = {
            "run_id": self.run_id,
            "topic_id": self.topic_id,
            "stage": self.stage,
            "status": status,
            "created_at": _iso(self.created_at),
            "finished_at": _iso(finished_at),
            "duration_ms": duration_ms,
            "total_cost_usd": total_cost_usd,
            "input_fingerprint": input_fingerprint,
            "output_fingerprint": output_fingerprint(parsed),
            "model": model,
            "cached": cached,
            "error": error,
        }
        _write_json_atomic(self.meta_path, meta)
        self.close_stream()
        self._update_index(
            status=status,
            duration_ms=duration_ms,
            total_cost_usd=total_cost_usd,
            input_fingerprint=input_fingerprint,
            finished_at=finished_at,
        )
        return meta

    def _update_index(
        self,
        *,
        status: str,
        duration_ms: int | None,
        total_cost_usd: float | None,
        input_fingerprint: str,
        finished_at: datetime,
    ) -> None:
        index_path = self.store.index_path(self.topic_id)
        if index_path.exists():
            try:
                idx = json.loads(index_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                idx = {}
        else:
            idx = {}

        idx["topic_id"] = self.topic_id
        idx.setdefault("topic", self.topic)
        runs = idx.setdefault("runs", [])
        parsed_path_str = self.store.parsed_index_path(self.topic_id, self.run_id)

        runs.append(
            {
                "run_id": self.run_id,
                "stage": self.stage,
                "status": status,
                "input_fingerprint": input_fingerprint,
                "parsed_path": parsed_path_str,
                "created_at": _iso(self.created_at),
                "finished_at": _iso(finished_at),
                "duration_ms": duration_ms,
                "total_cost_usd": total_cost_usd,
            }
        )

        if status == "succeeded" and self.stage == "newsfind_queries":
            idx["latest_queries_run_id"] = self.run_id
            idx["latest_queries_parsed_path"] = parsed_path_str

        _write_json_atomic(index_path, idx)
