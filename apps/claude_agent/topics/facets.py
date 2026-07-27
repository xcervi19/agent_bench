"""Language-neutral topic facets (#38).

Source grounding is lexical: `source_discover` matches topic words against an
English whitelist and English playbooks. Folding diacritics and matching
inflected forms (see `sources.text`) rescues shared proper nouns, but nothing
lexical can turn `Estreito de Ormuz` into `Strait of Hormuz` or `ropa` into
`crude oil`. That last step needs someone who knows the vocabulary, so a small
agent leg restates the topic in English and names the facets discovery keys on.

This module owns the contract for that leg's output and, just as importantly,
the deterministic fallback: grounding is an optimization, so a parse leg that
is slow, missing or confused must degrade to pre-#38 behaviour rather than cost
the operator a report.

Facets are cached per topic hash, so refreshes and re-plans of the same topic
pay for the leg once.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

FACETS_FILENAME = "facets.json"
FACETS_SCHEMA_VERSION = "0.1.0"

LIST_FIELDS = ("commodity", "geo", "entities", "signals")

MAX_ITEMS = 12
MAX_ITEM_CHARS = 80
MAX_CANONICAL_CHARS = 300
MAX_LANGUAGES = 8

UNKNOWN_LANGUAGE = "und"


def _clean_items(value: object, *, limit: int = MAX_ITEMS) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for item in value:
        if not isinstance(item, str):
            continue
        text = " ".join(item.split())[:MAX_ITEM_CHARS]
        if text and text not in out:
            out.append(text)
    return out[:limit]


def _clean_language(value: object) -> str:
    """Keep ISO 639-1 codes, reject anything else.

    The agent occasionally answers `Czech` or `cs-CZ`; neither is worth
    guessing at, and no consumer branches on the value beyond display.
    """
    code = str(value or "").strip().lower()
    return code if len(code) == 2 and code.isalpha() else UNKNOWN_LANGUAGE


def _clean_source_languages(value: object) -> list[str]:
    """Search languages, English always included.

    English is the lingua franca of the whitelist and of most primary sources,
    so it belongs in every plan even when the topic is regional.
    """
    codes = [c for c in (_clean_language(v) for v in _clean_items(value)) if c != UNKNOWN_LANGUAGE]
    if "en" not in codes:
        codes.insert(0, "en")
    return codes[:MAX_LANGUAGES]


def normalize_facets(raw: object, topic: str) -> dict[str, Any]:
    """Coerce the parse leg's output into the facets contract.

    Raises ValueError when the output is unusable. That always means "fall back
    to `fallback_facets`", never "fail the topic".
    """
    if not isinstance(raw, dict):
        raise ValueError("facets must be a JSON object")
    canonical = " ".join(str(raw.get("canonical_topic_en") or "").split())
    if not canonical:
        raise ValueError("canonical_topic_en is empty")

    facets: dict[str, Any] = {
        "schema_version": FACETS_SCHEMA_VERSION,
        "topic": topic,
        "canonical_topic_en": canonical[:MAX_CANONICAL_CHARS],
        "input_language": _clean_language(raw.get("input_language")),
        "source_languages": _clean_source_languages(raw.get("source_languages")),
        "degraded": False,
        "degraded_reason": None,
    }
    for field in LIST_FIELDS:
        facets[field] = _clean_items(raw.get(field))
    return facets


def fallback_facets(topic: str, *, reason: str) -> dict[str, Any]:
    """Facets to use when the parse leg cannot be trusted.

    The raw topic becomes the canonical topic. For Latin-script input that
    still grounds through diacritics folding and inflection matching; for other
    scripts it grounds against nothing, which is what happened before this leg
    existed.
    """
    facets: dict[str, Any] = {
        "schema_version": FACETS_SCHEMA_VERSION,
        "topic": topic,
        "canonical_topic_en": " ".join(topic.split())[:MAX_CANONICAL_CHARS],
        "input_language": UNKNOWN_LANGUAGE,
        "source_languages": ["en"],
        "degraded": True,
        "degraded_reason": reason[:200],
    }
    for field in LIST_FIELDS:
        facets[field] = []
    return facets


def discovery_query(facets: dict[str, Any]) -> str:
    """The text handed to `source_discover`.

    Discovery is a bag-of-tokens match, so ordering is irrelevant and only
    coverage matters. The raw topic is appended as well: it costs nothing when
    it is redundant and preserves the inflection matches on proper nouns the
    agent may have dropped while translating.
    """
    parts = [str(facets.get("canonical_topic_en") or "")]
    for field in LIST_FIELDS:
        parts.extend(facets.get(field) or [])
    parts.append(str(facets.get("topic") or ""))
    return " ".join(p for p in parts if p).strip()


def facets_cache_path(state_dir: str, topic_hash: str) -> Path:
    """Per-topic, not per-run: refreshes reuse the same translation."""
    return Path(state_dir) / "news" / topic_hash / FACETS_FILENAME


def load_cached_facets(path: Path, topic: str) -> dict[str, Any] | None:
    """Return cached facets, or None if absent, unreadable or stale.

    A cache miss is always recoverable, so every failure mode here is silent.
    """
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict) or raw.get("schema_version") != FACETS_SCHEMA_VERSION:
        return None
    try:
        return normalize_facets(raw, topic)
    except ValueError:
        return None
