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
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

FEEDS_DIRNAME = "feeds"
# Above this age a feed is exported and marked stale rather than withheld. The
# caller passes the configured value; this is the fallback for direct callers.
DEFAULT_MAX_AGE_DAYS = 45
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


def collected_at(meta: dict[str, Any], path: Path) -> datetime | None:
    """When this feed's content arrived in the slot.

    `publish` stamps `collected_at` on the sidecar it writes, and keeps the
    stamp while the content digest is unchanged — so the value is the age of the
    *numbers*, not of the last crawl that re-copied them. Feeds published before
    that stamp existed fall back to the file's mtime, which is when `publish`
    wrote it and therefore the same quantity, measured less precisely.
    """
    raw = meta.get("collected_at")
    if isinstance(raw, str) and raw.strip():
        try:
            when = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
        except ValueError:
            when = None
        if when is not None:
            return when if when.tzinfo else when.replace(tzinfo=UTC)
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
    except OSError:
        return None


def age_days(when: datetime | None, *, now: datetime | None = None) -> int | None:
    """Whole days since `when`, or None when the feed carries no usable date."""
    if when is None:
        return None
    delta = (now or datetime.now(UTC)) - when
    return max(0, int(delta.total_seconds() // 86_400))


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


def export_feeds(
    state_dir: str,
    destination: Path,
    facets: dict[str, Any],
    *,
    max_age_days: int = DEFAULT_MAX_AGE_DAYS,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Copy the feeds matching `facets` into `destination`. Returns the index.

    The index is written beside the files and mirrored into the run's input.json,
    so a later reader can tell "no feed applied to this topic" from "the feed
    directory was empty" — the same distinction #46 had to add to search.

    A feed past `max_age_days` is exported anyway and marked `stale`, in the index
    and in the file's own front matter. Withholding it would leave the analyst
    with nothing where it had an old-but-real number; marking it lets the figure
    be quoted with its period attached instead of as the current state (#51).
    """
    root = feeds_root(state_dir)
    index: dict[str, Any] = {
        "feed_count": 0,
        "feeds": [],
        "available": 0,
        "stale_count": 0,
        "max_age_days": max_age_days,
    }
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

        when = collected_at(meta, path)
        age = age_days(when, now=now)
        # An undated feed is not assumed fresh: we cannot say how old it is, and
        # the analyst has to know that before quoting a figure as current.
        stale = age is None or age > max_age_days

        destination.mkdir(parents=True, exist_ok=True)
        out = destination / path.name
        # Provenance in the file itself: the analyst cites the publisher and the
        # date, and must not have to trust that a filename means what it says.
        fields = [
            (key, meta.get(key))
            for key in ("title", "publisher", "url", "commodity", "region")
            if meta.get(key)
        ]
        fields.append(("collected_at", when.isoformat() if when else "unknown"))
        fields.append(("age_days", "unknown" if age is None else age))
        # Spelled out rather than left to arithmetic on `age_days`: the rule is
        # ours, and the reader of the file should not have to know the threshold.
        fields.append(("stale", "true" if stale else "false"))
        if stale:
            fields.append((
                "stale_note",
                f"older than {max_age_days} days — quote the figure with its period, "
                "not as the current state",
            ))
        header = "\n".join(f"{key}: {value}" for key, value in fields)
        out.write_text(f"---\n{header}\n---\n\n{text}", encoding="utf-8")
        selected.append({
            "source_id": meta.get("source_id") or path.stem,
            "title": meta.get("title"),
            "publisher": meta.get("publisher"),
            "url": meta.get("url"),
            "file": path.name,
            "chars": len(text),
            "collected_at": when.isoformat() if when else None,
            "age_days": age,
            "stale": stale,
        })

    index["feeds"] = selected
    index["feed_count"] = len(selected)
    index["stale_count"] = sum(1 for entry in selected if entry["stale"])
    if selected:
        (destination / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    elif candidates:
        # Feeds exist and none matched. That is either a correct "no feed applies"
        # or a topic whose facets went empty (#38 degradation), and the two are
        # indistinguishable from a feed_count of zero — so name the facets here.
        logger.warning(
            "feeds.none_matched available=%s commodity=%s geo=%s",
            len(candidates),
            sorted(_norm(facets.get("commodity"))),
            sorted(_norm(facets.get("geo"))),
        )
    return index


def publish(
    source_text_root: Path, state_dir: str, *, now: datetime | None = None
) -> list[str]:
    """Flatten `source_crawler`'s extracted output into the slot's feeds dir.

    `artifacts/collected_text/<id>/<id>.txt` is the crawler's layout, which
    carries QA packs and per-source directories the runtime has no use for.

    Only sources tagged `data_feed` are published. `document_type` is too broad a
    filter: OPEC's MOMR and BP's Energy Outlook are `official_data` too, but they
    are 170-300k-character reports that already live in RAG, where a topic
    retrieves the paragraph it needs. Copying them here would hand every matching
    run the whole document and duplicate the corpus. A feed is the other shape —
    a compact series whose value is that every row is present.

    The published sidecar gains `collected_at` (#51), which is what the run-time
    export ages a feed against. It is stamped when the *content* changes, not on
    every publish: the crawler re-downloads on its own cadence and an unchanged
    workbook is not fresher for having been fetched again. Keeping the stamp
    across a no-op re-publish is the difference between "we last saw new numbers
    in July" and "we asked again this morning".
    """
    published: list[str] = []
    target = feeds_root(state_dir)
    stamp = (now or datetime.now(UTC)).isoformat()
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
        meta["collected_at"] = _carried_stamp(target / sidecar.name, meta) or stamp
        shutil.copyfile(text_file, target / text_file.name)
        (target / sidecar.name).write_text(json.dumps(meta, indent=2), encoding="utf-8")
        published.append(text_file.stem)
    return published


def _carried_stamp(published_sidecar: Path, meta: dict[str, Any]) -> str | None:
    """The stamp already on the slot, when this publish changes nothing.

    `source_sha256` is the digest of the file the text was extracted from, so
    equality means the numbers are the ones already here. Anything unreadable or
    undecided returns None and the caller stamps `now`, which errs towards
    calling a feed fresher than it is — the alternative errs towards marking a
    genuinely current feed stale, and a stale mark the analyst must work around
    is the more expensive mistake to make wrongly.
    """
    try:
        existing = json.loads(published_sidecar.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(existing, dict):
        return None
    digest = meta.get("source_sha256")
    if not digest or existing.get("source_sha256") != digest:
        return None
    stamp = existing.get("collected_at")
    return stamp if isinstance(stamp, str) and stamp.strip() else None
