import asyncio
import hashlib
import json
import uuid
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from sqlalchemy import update

from ..config import ClaudeAgentSettings
from ..runner import stream_claude
from ..schemas import RunRequest
from ..sources.discover import discover_sources_for_topic
from .db import session_scope
from .facets import (
    FACETS_FILENAME,
    discovery_query,
    facets_cache_path,
    fallback_facets,
    load_cached_facets,
    normalize_facets,
)
from .models import Topic, TopicEvent
from .webhooks import deliver_event

STATE_PLANNING = "planning"
STATE_PLANNED = "planned_awaiting_review"
STATE_DELIVERING = "delivering"
STATE_REPORTED = "reported"
STATE_FAILED = "failed"
STATE_CANCELLED = "cancelled"

TOPIC_PARSE_COMMAND = "/newsfind-topic-parse"
PLAN_COMMAND = "/newsfind-plan"
DELIVER_COMMAND = "/newsfind-deliver"

PIPELINE_COMMANDS = (TOPIC_PARSE_COMMAND, PLAN_COMMAND, DELIVER_COMMAND)
"""Slash commands the topic lifecycle drives.

Deployments override `allowed_commands` in their own `.env`, so adding a leg to
this module is not enough to make it run in production. `app.py` warns at
startup when one of these is missing rather than letting the stage silently
no-op, which is how #36 shipped a disabled grounding stage unnoticed.
"""


def topic_id_hash(topic: str) -> str:
    normalized = " ".join(topic.lower().split())
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()


def run_dir(state_dir: str, hash_: str, run_id: str) -> Path:
    return Path(state_dir) / "news" / hash_ / "runs" / run_id


async def emit(topic_id: uuid.UUID, event_type: str, payload: dict[str, Any]) -> int:
    async with session_scope() as s:
        seq = (
            await s.execute(
                update(Topic)
                .where(Topic.id == topic_id)
                .values(last_event_seq=Topic.last_event_seq + 1)
                .returning(Topic.last_event_seq)
            )
        ).scalar_one()
        s.add(TopicEvent(topic_id=topic_id, seq=seq, event_type=event_type, payload=payload))
    await deliver_event(topic_id, int(seq), event_type, payload)
    return int(seq)


async def set_state(topic_id: uuid.UUID, new_state: str, *, error: str | None = None) -> None:
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        old = row.state
        row.state = new_state
        if error is not None:
            row.error = error
    await emit(topic_id, "state.changed", {"from": old, "to": new_state, "error": error})


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


async def _run_parse_leg(run_dir: Path, settings: ClaudeAgentSettings) -> None:
    """Drive the topic_parse command, raising on anything short of success.

    Deliberately quieter than `_run_slash`: this leg makes no tool calls worth
    showing an operator, and it reports failure by raising so the caller can
    degrade instead of moving the topic to `failed`.
    """
    req = RunRequest(
        command=TOPIC_PARSE_COMMAND,
        args=str(run_dir),
        output_format="stream-json",
        timeout_sec=settings.topic_parse_timeout_sec,
    )
    success = False
    async for line in stream_claude(req, settings):
        event = _try_loads(line)
        if not isinstance(event, dict):
            continue
        kind = event.get("type")
        if kind == "result":
            if event.get("subtype") != "success":
                raise RuntimeError(f"result subtype={event.get('subtype')}")
            success = True
        elif kind == "error":
            raise RuntimeError(str(event.get("error") or "stream error"))
    if not success:
        raise RuntimeError("agent produced no result event")


async def run_topic_parse(
    topic_id: uuid.UUID,
    topic: str,
    out_dir: Path,
    settings: ClaudeAgentSettings,
) -> dict[str, Any]:
    """Restate the topic in English so lexical source discovery can key on it.

    Never fails the topic. Grounding is an optimization over an agent that can
    still search the open web, so every failure mode here degrades to the
    untranslated topic and lets the run continue.
    """
    await emit(topic_id, "stage.started", {"stage": "topic_parse"})
    cache = facets_cache_path(settings.state_dir, topic_id_hash(topic))
    facets = load_cached_facets(cache, topic)
    cached = facets is not None

    if facets is None:
        parse_dir = out_dir / "topic_parse"
        _write_json(parse_dir / "input.json", {"topic": topic})
        try:
            await _run_parse_leg(parse_dir, settings)
            raw = json.loads((parse_dir / FACETS_FILENAME).read_text(encoding="utf-8"))
            facets = normalize_facets(raw, topic)
        except Exception as exc:  # noqa: BLE001 - degrade on anything, incl. a missing CLI
            facets = fallback_facets(topic, reason=f"{type(exc).__name__}: {exc}")
        else:
            _write_json(cache, facets)

    _write_json(out_dir / FACETS_FILENAME, facets)
    await emit(topic_id, "stage.finished", {
        "stage": "topic_parse",
        "cached": cached,
        "degraded": facets["degraded"],
        "degraded_reason": facets["degraded_reason"],
        "input_language": facets["input_language"],
        "canonical_topic_en": facets["canonical_topic_en"],
        "source_languages": facets["source_languages"],
    })
    return facets


async def run_source_discover(topic_id: uuid.UUID, query: str, out_dir: Path) -> None:
    await emit(topic_id, "stage.started", {"stage": "source_discover"})
    warning: str | None = None
    try:
        result = await asyncio.to_thread(discover_sources_for_topic, query)
    except OSError as exc:
        # Whitelist or playbooks missing from the image is a packaging fault,
        # not a reason to deny the operator a report: the plan agent can still
        # search unscoped. #36 shipped exactly this bug and failed every topic.
        warning = f"source grounding unavailable: {exc}"
        result = {"source_targets": {"entities": []}, "playbook_refs": []}

    targets = result["source_targets"]
    _write_json(out_dir / "source_targets.json", targets)
    await emit(topic_id, "stage.finished", {
        "stage": "source_discover",
        "entities": len(targets["entities"]),
        "playbook_refs": result["playbook_refs"],
        "warning": warning,
    })


async def run_plan(topic_id: uuid.UUID, topic: str, settings: ClaudeAgentSettings) -> None:
    plan_run_id = str(uuid.uuid4())
    hash_ = topic_id_hash(topic)
    out_dir = run_dir(settings.state_dir, hash_, plan_run_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_json(out_dir / "input.json", {"topic": topic, "run_id": plan_run_id})

    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        row.plan_run_id = plan_run_id
        row.topic_id_hash = hash_

    await set_state(topic_id, STATE_PLANNING)
    facets = await run_topic_parse(topic_id, topic, out_dir, settings)
    try:
        await run_source_discover(topic_id, discovery_query(facets), out_dir)
    except ValueError as exc:
        error = f"source_discover failed: {exc}"
        await emit(topic_id, "error", {"stage": "source_discover", "error": error})
        await set_state(topic_id, STATE_FAILED, error=error)
        return

    summary = await _run_slash(topic_id, leg="plan", command=PLAN_COMMAND, args=str(out_dir), settings=settings)
    if summary is None:
        return
    await emit(topic_id, "intro.ready", summary)
    await emit(topic_id, "needs_input", {"gate": "planned_awaiting_review"})
    await set_state(topic_id, STATE_PLANNED)


async def run_deliver(topic_id: uuid.UUID, settings: ClaudeAgentSettings) -> None:
    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        plan_run_id = row.plan_run_id
        hash_ = row.topic_id_hash

    deliver_run_id = str(uuid.uuid4())
    plan_dir = run_dir(settings.state_dir, hash_, plan_run_id)
    out_dir = run_dir(settings.state_dir, hash_, deliver_run_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "input.json").write_text(
        json.dumps({
            "plan_run_dir": str(plan_dir),
            "deliver_run_dir": str(out_dir),
            "run_id": deliver_run_id,
        }),
        encoding="utf-8",
    )

    async with session_scope() as s:
        row = await s.get(Topic, topic_id)
        row.deliver_run_id = deliver_run_id

    await set_state(topic_id, STATE_DELIVERING)
    summary = await _run_slash(
        topic_id, leg="deliver", command=DELIVER_COMMAND, args=str(out_dir), settings=settings
    )
    if summary is None:
        return
    await emit(topic_id, "report.ready", summary)
    await set_state(topic_id, STATE_REPORTED)


async def _run_slash(
    topic_id: uuid.UUID,
    *,
    leg: str,
    command: str,
    args: str,
    settings: ClaudeAgentSettings,
) -> dict[str, Any] | None:
    await emit(topic_id, "stage.started", {"stage": leg})
    req = RunRequest(
        command=command,
        args=args,
        output_format="stream-json",
        timeout_sec=settings.max_timeout_sec,
    )
    error: str | None = None
    cost: float | None = None
    duration_ms: int | None = None
    success = False

    try:
        async for line in stream_claude(req, settings):
            event = _try_loads(line)
            if not isinstance(event, dict):
                continue
            kind = event.get("type")
            if kind == "assistant":
                for block in event.get("message", {}).get("content", []) or []:
                    if block.get("type") == "tool_use":
                        await emit(topic_id, "tool_use", {
                            "tool": block.get("name"),
                            "tool_use_id": block.get("id"),
                            "input_preview": str(block.get("input"))[:400],
                        })
            elif kind == "user":
                for block in event.get("message", {}).get("content", []) or []:
                    if block.get("type") == "tool_result":
                        await emit(topic_id, "tool_result", {
                            "tool_use_id": block.get("tool_use_id"),
                            "is_error": bool(block.get("is_error")),
                            "output_preview": _result_preview(block.get("content")),
                        })
            elif kind == "result":
                if event.get("subtype") == "success":
                    cost = event.get("total_cost_usd")
                    duration_ms = event.get("duration_ms")
                    success = True
                else:
                    error = f"result subtype={event.get('subtype')}"
            elif kind == "error":
                error = str(event.get("error") or "stream error")
    except Exception as exc:  # pragma: no cover - must not leave topic stuck mid-stage
        error = f"pipeline error: {exc}"
        await emit(topic_id, "error", {"stage": leg, "error": error})
        await set_state(topic_id, STATE_FAILED, error=error)
        return None

    if error is None and not success:
        error = "agent produced no result event"

    summary: dict[str, Any] | None = None
    if error is None:
        try:
            summary = _read_summary(Path(args))
        except (FileNotFoundError, ValueError, JSONDecodeError, OSError) as exc:
            error = f"summary.json invalid: {exc}"

    if error is not None:
        await emit(topic_id, "error", {"stage": leg, "error": error})
        await set_state(topic_id, STATE_FAILED, error=error)
        return None

    await emit(topic_id, "stage.finished", {
        "stage": leg,
        "duration_ms": duration_ms,
        "total_cost_usd": cost,
    })
    return summary


def _read_summary(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "summary.json"
    if not path.exists():
        raise FileNotFoundError(f"{path} not written")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def _try_loads(s: str | None) -> Any:
    if not s:
        return None
    try:
        return json.loads(s)
    except (JSONDecodeError, TypeError):
        return None


def _result_preview(content: Any) -> str:
    if isinstance(content, str):
        return content[:600]
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
            else:
                parts.append(str(block))
        return " ".join(parts)[:600]
    return str(content)[:600]
