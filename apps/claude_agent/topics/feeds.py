"""Official data feeds handed to the analyst alongside the web evidence (#45).

A statistical agency is a source we do not have to search for. We know PPAC's
URL, and the India run proved that asking for it beats searching for it: a
domain-filtered search reached ppac.gov.in but the index served a monthly report
two years stale, while one direct request returned the current workbook. That is
the third channel argued for in #49 — known sources polled off the search budget.

`source_crawler` does the polling and the conversion; this module is the other
half, deciding which of the resulting feeds belong in *this* topic's run and
copying them where the analyst reads.

Selection is deterministic — commodity and region matched against the topic's
facets — for the same reason the evidence store records outcomes rather than
verdicts: a model asked "is PPAC relevant to Indian gas?" would usually be right,
and the times it was wrong would be invisible. A set comparison is auditable.

Feeds live under `<state_dir>/feeds`, not in the image. Playbooks and the
whitelist are baked in because they change with a release; a monthly balance
changes on the publisher's schedule, and an image rebuild is the wrong unit of
freshness for it.
"""

from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

FEEDS_DIRNAME = "feeds"
# Enough of a monthly series for the recent months to survive; the workbooks that
# matter here run ~50k characters, most of it empty future columns.
MAX_CHARS_PER_FEED = 60_000
TRUNCATION_NOTE = "\n\n[... truncated]"


def feeds_root(state_dir: str) -> Path:
    """Where `source_crawler` publishes extracted feeds for this slot."""
    return Path(state_dir) / FEEDS_DIRNAME


def _norm(value: object) -> set[str]:
    """Lowercased tokens, with `_` and `-` treated alike.

    Facets say `natural gas` where a seed says `natural_gas`, and neither is
    wrong; normalising here beats making one of them wrong.
    """
    items: list[str] = []
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = [str(v) for v in value]
    out: set[str] = set()
    for item in items:
        text = item.strip().lower().replace("-", "_").replace(" ", "_")
        if text:
            out.add(text)
    return out


def matches(meta: dict[str, Any], facets: dict[str, Any]) -> bool:
    """Does this feed belong to this topic?

    Both axes must agree when the feed declares them. A feed with no region is
    global (JODI world data), and a feed with no commodity is unfiltered — in
    both cases the missing axis cannot disqualify it. A topic with no facets at
    all gets nothing, which is deliberate: handing every feed to every topic is
    how a run ends up reading Indian gas tables for a Hormuz shipping question.
    """
    topic_commodity = _norm(facets.get("commodity"))
    topic_geo = _norm(facets.get("geo"))
    if not topic_commodity and not topic_geo:
        return False

    feed_commodity = _norm(meta.get("commodity"))
    if feed_commodity and topic_commodity and not (feed_commodity & topic_commodity):
        return False

    feed_region = _norm(meta.get("region"))
    if feed_region and topic_geo and not (feed_region & topic_geo):
        return False

    # A feed that declares nothing we can check is not evidence of a match.
    return bool((feed_commodity & topic_commodity) or (feed_region & topic_geo))


def _load(path: Path) -> tuple[dict[str, Any], str] | None:
    sidecar = path.with_suffix(path.suffix + ".meta.json")
    if not sidecar.is_file():
        return None
    try:
        meta = json.loads(sidecar.read_text(encoding="utf-8"))
        text = path.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError):
        return None
    return (meta, text) if isinstance(meta, dict) else None


def export_feeds(state_dir: str, destination: Path, facets: dict[str, Any]) -> dict[str, Any]:
    """Copy the feeds matching `facets` into `destination`. Returns the index.

    The index is written beside the files and mirrored into the run's input.json,
    so a later reader can tell "no feed applied to this topic" from "the feed
    directory was empty" — the same distinction #46 had to add to search.
    """
    root = feeds_root(state_dir)
    index: dict[str, Any] = {"feed_count": 0, "feeds": [], "available": 0}
    if not root.is_dir():
        return index

    candidates = sorted(root.glob("*.txt"))
    index["available"] = len(candidates)
    selected: list[dict[str, Any]] = []

    for path in candidates:
        loaded = _load(path)
        if loaded is None:
            logger.warning("feeds.unreadable path=%s", path)
            continue
        meta, text = loaded
        if not matches(meta, facets):
            continue
        if len(text) > MAX_CHARS_PER_FEED:
            text = text[:MAX_CHARS_PER_FEED] + TRUNCATION_NOTE

        destination.mkdir(parents=True, exist_ok=True)
        out = destination / path.name
        # Provenance in the file itself: the analyst cites the publisher and the
        # date, and must not have to trust that a filename means what it says.
        header = "\n".join(
            f"{key}: {meta.get(key)}"
            for key in ("title", "publisher", "url", "collected_at", "commodity", "region")
            if meta.get(key)
        )
        out.write_text(f"---\n{header}\n---\n\n{text}", encoding="utf-8")
        selected.append({
            "source_id": meta.get("source_id") or path.stem,
            "title": meta.get("title"),
            "publisher": meta.get("publisher"),
            "url": meta.get("url"),
            "file": path.name,
            "chars": len(text),
        })

    index["feeds"] = selected
    index["feed_count"] = len(selected)
    if selected:
        (destination / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index


def publish(source_text_root: Path, state_dir: str) -> list[str]:
    """Flatten `source_crawler`'s extracted output into the slot's feeds dir.

    `artifacts/collected_text/<id>/<id>.txt` is the crawler's layout, which
    carries QA packs and per-source directories the runtime has no use for.

    Only sources tagged `data_feed` are published. `document_type` is too broad a
    filter: OPEC's MOMR and BP's Energy Outlook are `official_data` too, but they
    are 170-300k-character reports that already live in RAG, where a topic
    retrieves the paragraph it needs. Copying them here would hand every matching
    run the whole document and duplicate the corpus. A feed is the other shape —
    a compact series whose value is that every row is present.
    """
    published: list[str] = []
    target = feeds_root(state_dir)
    for sidecar in sorted(source_text_root.glob("*/*.txt.meta.json")):
        try:
            meta = json.loads(sidecar.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if "data_feed" not in (meta.get("tags") or []):
            continue
        # The sidecar is `<name>.txt.meta.json`; `with_suffix` would give
        # `<name>.txt.txt`, because the stem already ends in `.txt`.
        text_file = sidecar.parent / sidecar.name[: -len(".meta.json")]
        if not text_file.is_file():
            continue
        target.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(text_file, target / text_file.name)
        shutil.copyfile(sidecar, target / sidecar.name)
        published.append(text_file.stem)
    return published
