"""Stage 2 — intro (pure Python).

Reads ``parsed.json`` (Stage 1) and emits ``intro.json`` + ``intro.md``.
NEVER invents facts; only restructures fields from Stage 1 output.

Output schema_version: 0.1.0
"""

from __future__ import annotations

import json
import time
import traceback
import uuid
from pathlib import Path
from typing import Any

from ...artifacts import ArtifactStore, _write_json_atomic  # type: ignore[attr-defined]
from ...config import ClaudeAgentSettings
from .types import StageResult

INTRO_SCHEMA_VERSION = "0.1.0"

_STYLES = {"raw", "trader", "executive", "analyst"}


def _short(text: str | None, max_chars: int = 480) -> str:
    if not text:
        return ""
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:") + "…"


def _truncate_sentences(text: str | None, max_sentences: int) -> str:
    if not text:
        return ""
    pieces: list[str] = []
    cur = ""
    for ch in text.strip():
        cur += ch
        if ch in ".?!":
            pieces.append(cur.strip())
            cur = ""
            if len(pieces) >= max_sentences:
                break
    if cur.strip() and len(pieces) < max_sentences:
        pieces.append(cur.strip())
    return " ".join(pieces).strip()


def _build_intro(parsed: dict[str, Any], style: str) -> dict[str, Any]:
    style = style if style in _STYLES else "raw"
    entities = parsed.get("entities") or {}
    actors = entities.get("actors") or []
    languages = entities.get("primary_languages") or []
    regions = entities.get("regions") or []
    queries = parsed.get("queries") or []

    monitoring = parsed.get("monitoring_plan") or {}
    trigger_terms = monitoring.get("trigger_terms") or []

    headline = parsed.get("topic") or parsed.get("topic_restated") or ""
    understanding = _short(parsed.get("topic_restated"), 320)
    current_state_short = _truncate_sentences(parsed.get("current_state"), 3)
    working_thesis_short = _truncate_sentences(parsed.get("working_thesis"), 2)

    highlights: list[str] = []
    if queries:
        langs_present = sorted({q.get("language", "") for q in queries if q.get("language")})
        highlights.append(
            f"Will search {len(queries)} angles in {len(langs_present)} languages "
            f"({', '.join(langs_present) or '—'})."
        )
    if working_thesis_short:
        highlights.append(f"Working thesis: {_short(working_thesis_short, 220)}")
    if trigger_terms:
        terms_preview = ", ".join(trigger_terms[:6])
        highlights.append(f"Will watch trigger terms: {terms_preview}.")
    if not highlights:
        highlights.append("Stage 1 completed; awaiting your go-ahead to begin Stage 3 search.")

    return {
        "schema_version": INTRO_SCHEMA_VERSION,
        "topic_id": parsed.get("topic_id") or "",
        "style": style,
        "headline": headline,
        "understanding": understanding,
        "current_state_short": current_state_short,
        "working_thesis_short": working_thesis_short,
        "approach": {
            "queries_count": len(queries),
            "languages": languages,
            "regions": regions,
            "key_actors_top5": actors[:5],
        },
        "highlights": highlights,
        "next_step": "Press Proceed to begin web search and source collection.",
    }


def _render_md(intro: dict[str, Any]) -> str:
    actors = intro["approach"]["key_actors_top5"]
    actors_chip = (
        f'<EntityChips entities="{", ".join(actors)}"/>'
        if actors
        else ""
    )
    highlights_md = "\n".join(f"- {h}" for h in intro["highlights"])
    languages = intro["approach"]["languages"]
    regions = intro["approach"]["regions"]

    parts = [
        f"# {intro['headline']}",
        "",
        f"**Understanding.** {intro['understanding']}",
    ]
    if intro["current_state_short"]:
        parts += ["", f"**Current state.** {intro['current_state_short']}"]
    if intro["working_thesis_short"]:
        parts += ["", f"**Working thesis.** {intro['working_thesis_short']}"]
    parts += [
        "",
        "## Approach",
        f"- Queries planned: **{intro['approach']['queries_count']}**",
        f"- Languages: {', '.join(languages) if languages else '—'}",
        f"- Regions: {', '.join(regions) if regions else '—'}",
    ]
    if actors_chip:
        parts += ["", "## Key actors", actors_chip]
    parts += [
        "",
        "## What happens next",
        f'<Highlights items="{len(intro["highlights"])}"/>',
        highlights_md,
        "",
        f"_{intro['next_step']}_",
        "",
    ]
    return "\n".join(parts)


async def run_intro_stage(
    *,
    topic_id_hash: str,
    queries_run_id: str,
    style: str,
    settings: ClaudeAgentSettings,
) -> StageResult:
    """Read Stage 1's ``parsed.json`` and write ``intro.json`` + ``intro.md``."""
    started = time.monotonic()
    try:
        store = ArtifactStore(
            Path(settings.state_dir),
            index_path_prefix=settings.state_index_prefix,
        )
        run_dir = store.run_dir(topic_id_hash, queries_run_id)
        parsed_path = run_dir / "parsed.json"
        if not parsed_path.exists():
            return StageResult(
                status="failed",
                run_id=queries_run_id,
                topic_id_hash=topic_id_hash,
                error=f"parsed.json missing at {parsed_path}",
                error_type="FileNotFoundError",
            )
        parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
        intro = _build_intro(parsed, style)
        intro_md = _render_md(intro)

        # Stage 2 reuses the Stage 1 run_id by design (assembly, not generation):
        # the artifact bundle for a topic stays cohesive in one folder.
        intro_json_path = run_dir / "intro.json"
        intro_md_path = run_dir / "intro.md"
        _write_json_atomic(intro_json_path, intro)
        intro_md_path.write_text(intro_md, encoding="utf-8")

        # Update the topic's index.json with cross-stage pointers.
        _update_index(store, topic_id_hash, intro_json_path, intro_md_path)

        duration_ms = int((time.monotonic() - started) * 1000)
        return StageResult(
            status="succeeded",
            run_id=queries_run_id,
            topic_id_hash=topic_id_hash,
            artifact_paths={
                "intro_json": str(intro_json_path),
                "intro_md": str(intro_md_path),
            },
            parsed=intro,
            duration_ms=duration_ms,
            total_cost_usd=0.0,
        )
    except Exception as exc:  # noqa: BLE001
        return StageResult(
            status="failed",
            run_id=queries_run_id,
            topic_id_hash=topic_id_hash,
            error=f"{type(exc).__name__}: {exc}",
            error_type=type(exc).__name__,
            traceback=traceback.format_exc(),
        )


def _update_index(
    store: ArtifactStore,
    topic_id_hash: str,
    intro_json_path: Path,
    intro_md_path: Path,
) -> None:
    index_path = store.index_path(topic_id_hash)
    if not index_path.exists():
        return
    try:
        idx = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    prefix = f"{store.index_path_prefix}/" if store.index_path_prefix else ""
    rel_intro = (
        f"{prefix}news/{topic_id_hash}/runs/{intro_json_path.parent.name}/intro.json"
    )
    rel_intro_md = (
        f"{prefix}news/{topic_id_hash}/runs/{intro_md_path.parent.name}/intro.md"
    )
    idx["latest_intro_path"] = rel_intro
    idx["latest_intro_md_path"] = rel_intro_md
    _write_json_atomic(index_path, idx)
