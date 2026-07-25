from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .text import significant_tokens, tokens


@dataclass(frozen=True, slots=True)
class WhitelistEntry:
    entity: str
    domain: str
    type: str
    category: str
    notes: str
    agreement_count: int


def load_whitelist(path: Path) -> list[WhitelistEntry]:
    if not path.is_file():
        raise FileNotFoundError(f"whitelist not found: {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"whitelist must be a JSON array: {path}")
    entries: list[WhitelistEntry] = []
    for i, row in enumerate(raw):
        if not isinstance(row, dict):
            raise ValueError(f"whitelist[{i}] must be an object")
        domain = str(row.get("domain") or "").strip().lower()
        entity = str(row.get("entity") or "").strip()
        if not domain or not entity:
            raise ValueError(f"whitelist[{i}] missing entity or domain")
        entries.append(
            WhitelistEntry(
                entity=entity,
                domain=domain,
                type=str(row.get("type") or "official"),
                category=str(row.get("category") or ""),
                notes=str(row.get("notes") or ""),
                agreement_count=int(row.get("agreement_count") or 0),
            )
        )
    return entries


def index_by_domain(entries: list[WhitelistEntry]) -> dict[str, WhitelistEntry]:
    by_domain: dict[str, WhitelistEntry] = {}
    for entry in entries:
        by_domain.setdefault(entry.domain, entry)
    return by_domain


def entity_matches(entity: str, query: str) -> bool:
    q = query.strip()
    if not q:
        return False
    e = entity.strip()
    if e.casefold() == q.casefold():
        return True
    q_tokens = tokens(q)
    if not q_tokens:
        return False
    e_tokens = tokens(e)
    if q_tokens <= e_tokens:
        return True
    return len(q) >= 3 and q.casefold() in e.casefold()


def _name_variants(entity: str) -> list[str]:
    head = re.split(r"[(\u2014\u2013,]", entity)[0]
    return [entity, head] if head.strip() != entity.strip() else [entity]


def entities_named_in(entries: list[WhitelistEntry], topic: str) -> list[WhitelistEntry]:
    topic_tokens = significant_tokens(topic)
    if not topic_tokens:
        return []
    hits = [
        entry
        for entry in entries
        if any(
            (name_tokens := significant_tokens(variant)) and name_tokens <= topic_tokens
            for variant in _name_variants(entry.entity)
        )
    ]
    hits.sort(key=lambda e: (-e.agreement_count, e.entity.casefold(), e.domain))
    return hits


def match_entries(entries: list[WhitelistEntry], query: str) -> list[WhitelistEntry]:
    q = query.strip().casefold()
    if not q:
        return []
    hits = [e for e in entries if entity_matches(e.entity, query) or e.domain == q]
    hits.sort(key=lambda e: (-e.agreement_count, e.entity.casefold(), e.domain))
    return hits


def is_whitelisted_domain(domain: str, by_domain: dict[str, WhitelistEntry]) -> bool:
    d = domain.strip().lower().removeprefix("www.")
    if d in by_domain:
        return True
    return any(d == known or d.endswith("." + known) for known in by_domain)
