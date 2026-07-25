from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from .text import significant_tokens
from .whitelist import WhitelistEntry, entity_matches, index_by_domain

MAX_TOPIC_PLAYBOOKS = 3

_SECTION_RE = re.compile(
    r"^##\s+Primary Official Sources\s*$",
    re.MULTILINE | re.IGNORECASE,
)
_NEXT_SECTION_RE = re.compile(r"^##\s+", re.MULTILINE)
_ROW_RE = re.compile(
    r"^\|\s*(?P<entity>[^|]+?)\s*\|\s*(?P<domain>[^|]+?)\s*\|\s*(?P<watch>[^|]*?)\s*\|",
    re.MULTILINE,
)


@dataclass(frozen=True, slots=True)
class PlaybookSourceRow:
    entity: str
    domain: str
    what_to_watch: str
    playbook: str


@dataclass(slots=True)
class PlaybookHit:
    path: Path
    name: str
    rows: list[PlaybookSourceRow] = field(default_factory=list)
    entity_row_match: bool = False


def playbooks_dir_or_raise(path: Path) -> Path:
    if not path.is_dir():
        raise FileNotFoundError(f"playbooks directory not found: {path}")
    return path


def list_playbook_files(directory: Path) -> list[Path]:
    return sorted(p for p in directory.glob("*.md") if p.name != "CHECKLIST.md")


def _primary_sources_section(text: str) -> str:
    match = _SECTION_RE.search(text)
    if not match:
        return ""
    rest = text[match.end() :]
    next_sec = _NEXT_SECTION_RE.search(rest)
    return rest[: next_sec.start()] if next_sec else rest


def parse_primary_official_sources(text: str, playbook_name: str) -> list[PlaybookSourceRow]:
    section = _primary_sources_section(text)
    if not section:
        return []
    rows: list[PlaybookSourceRow] = []
    for match in _ROW_RE.finditer(section):
        entity = match.group("entity").strip()
        domain = match.group("domain").strip().lower()
        watch = match.group("watch").strip()
        if not entity or not domain or entity.lower() == "entity" or domain == "domain":
            continue
        if domain.startswith("---") or set(domain) <= {"-"}:
            continue
        rows.append(
            PlaybookSourceRow(
                entity=entity,
                domain=domain.removeprefix("www."),
                what_to_watch=watch,
                playbook=playbook_name,
            )
        )
    return rows


def find_playbooks(directory: Path, query: str) -> list[PlaybookHit]:
    q = query.strip()
    if not q:
        return []
    hits: list[PlaybookHit] = []
    for path in list_playbook_files(directory):
        text = path.read_text(encoding="utf-8")
        rows = parse_primary_official_sources(text, path.name)
        entity_row_match = any(
            entity_matches(r.entity, q) or q.casefold() in r.domain for r in rows
        )
        topic_hit = entity_matches(path.stem.replace("_", " "), q) or (
            len(q) >= 3 and q.casefold() in text.casefold()
        )
        if not (entity_row_match or topic_hit):
            continue
        hits.append(
            PlaybookHit(
                path=path,
                name=path.name,
                rows=rows,
                entity_row_match=entity_row_match,
            )
        )
    return hits


def _read_hit(path: Path) -> PlaybookHit:
    rows = parse_primary_official_sources(path.read_text(encoding="utf-8"), path.name)
    return PlaybookHit(path=path, name=path.name, rows=rows)


def _stem_relevance(hits: list[PlaybookHit], topic: str) -> dict[str, float]:
    stem_tokens = {h.name: significant_tokens(h.path.stem.replace("_", " ")) for h in hits}
    frequency = Counter(t for toks in stem_tokens.values() for t in toks)
    topic_tokens = significant_tokens(topic)
    return {
        name: sum(1 / frequency[t] for t in toks & topic_tokens)
        for name, toks in stem_tokens.items()
    }


def playbooks_for_topic(
    directory: Path,
    topic: str,
    entity_domains: set[str],
) -> list[PlaybookHit]:
    hits = [_read_hit(path) for path in list_playbook_files(directory)]
    relevance = _stem_relevance(hits, topic)

    def entity_rows(hit: PlaybookHit) -> int:
        return sum(1 for row in hit.rows if row.domain in entity_domains)

    by_entity = sorted(
        (h for h in hits if entity_rows(h)),
        key=lambda h: (-entity_rows(h), h.name),
    )[:MAX_TOPIC_PLAYBOOKS]
    by_topic = sorted(
        (h for h in hits if relevance[h.name]),
        key=lambda h: (-relevance[h.name], h.name),
    )[:MAX_TOPIC_PLAYBOOKS]

    selected: dict[str, PlaybookHit] = {}
    for hit in by_entity + by_topic:
        selected.setdefault(hit.name, hit)
    return list(selected.values())


def selected_rows_for_query(hit: PlaybookHit, query: str) -> list[PlaybookSourceRow]:
    if hit.entity_row_match:
        return [
            r
            for r in hit.rows
            if entity_matches(r.entity, query) or query.casefold() in r.domain
        ]
    return list(hit.rows)


def resolve_playbook_entries(
    hits: list[PlaybookHit],
    whitelist: list[WhitelistEntry],
    query: str,
) -> list[tuple[WhitelistEntry, list[str], str]]:
    by_domain = index_by_domain(whitelist)
    merged: dict[str, tuple[WhitelistEntry, set[str], str]] = {}
    for hit in hits:
        for row in selected_rows_for_query(hit, query):
            entry = by_domain.get(row.domain)
            if entry is None:
                continue
            existing = merged.get(entry.domain)
            if existing is None:
                merged[entry.domain] = (entry, {hit.name}, row.what_to_watch)
            else:
                existing[1].add(hit.name)
    out = [(entry, sorted(refs), watch) for entry, refs, watch in merged.values()]
    out.sort(key=lambda t: (-t[0].agreement_count, t[0].entity.casefold(), t[0].domain))
    return out
