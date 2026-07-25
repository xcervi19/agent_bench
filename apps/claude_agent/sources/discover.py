from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from .playbooks import (
    PlaybookHit,
    find_playbooks,
    playbooks_dir_or_raise,
    playbooks_for_topic,
    resolve_playbook_entries,
)
from .whitelist import (
    WhitelistEntry,
    entities_named_in,
    is_whitelisted_domain,
    load_whitelist,
    match_entries,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_WHITELIST = REPO_ROOT / "source_whitelist.json"
DEFAULT_PLAYBOOKS = REPO_ROOT / "local_knowledge_sources" / "playbooks"


def _signals_from_watch(watch: str) -> list[str]:
    if not watch or watch == "—":
        return []
    parts = re.split(r"[,;/]| and ", watch)
    out: list[str] = []
    for part in parts:
        token = re.sub(r"\s+", " ", part).strip(" .")
        if token and token not in out:
            out.append(token)
    return out[:6]


def _known_source(
    entry: WhitelistEntry,
    playbook_refs: list[str],
) -> dict[str, Any]:
    return {
        "entity": entry.entity,
        "domain": entry.domain,
        "type": entry.type,
        "category": entry.category,
        "notes": entry.notes,
        "playbook_refs": playbook_refs,
    }


def _source_target(
    entry: WhitelistEntry,
    playbook_refs: list[str],
    signals: list[str],
) -> dict[str, Any]:
    return {
        "entity": entry.entity,
        "known_domains": [entry.domain],
        "playbook_refs": playbook_refs,
        "signals": signals,
        "type": entry.type,
    }


def _assemble(
    query: str,
    direct: list[WhitelistEntry],
    playbook_hits: list[PlaybookHit],
    from_playbooks: list[tuple[WhitelistEntry, list[str], str]],
) -> dict[str, Any]:
    refs_by_domain: dict[str, list[str]] = {}
    watch_by_domain: dict[str, str] = {}
    for entry, refs, watch in from_playbooks:
        refs_by_domain[entry.domain] = refs
        watch_by_domain[entry.domain] = watch

    merged: dict[str, WhitelistEntry] = {}
    for entry in direct:
        merged[entry.domain] = entry
    for entry, refs, _watch in from_playbooks:
        merged.setdefault(entry.domain, entry)
        refs_by_domain.setdefault(entry.domain, refs)

    for entry in direct:
        if entry.domain not in refs_by_domain:
            refs_by_domain[entry.domain] = sorted({h.name for h in playbook_hits})

    known_sources = [
        _known_source(entry, refs_by_domain.get(entry.domain, []))
        for entry in sorted(
            merged.values(),
            key=lambda e: (-e.agreement_count, e.entity.casefold(), e.domain),
        )
    ]

    source_targets = {
        "entities": [
            _source_target(
                entry,
                refs_by_domain.get(entry.domain, []),
                _signals_from_watch(watch_by_domain.get(entry.domain, "")),
            )
            for entry in sorted(
                merged.values(),
                key=lambda e: (-e.agreement_count, e.entity.casefold(), e.domain),
            )
        ]
    }

    return {
        "query": query,
        "known_sources": known_sources,
        "discovered_candidates": [],
        "playbook_refs": sorted({h.name for h in playbook_hits}),
        "source_targets": source_targets,
    }


def discover_sources(
    query: str,
    *,
    whitelist_path: Path | None = None,
    playbooks_dir: Path | None = None,
) -> dict[str, Any]:
    q = query.strip()
    if not q:
        raise ValueError("query must be non-empty")

    whitelist = load_whitelist(whitelist_path or DEFAULT_WHITELIST)
    playbooks_root = playbooks_dir_or_raise(playbooks_dir or DEFAULT_PLAYBOOKS)

    playbook_hits = find_playbooks(playbooks_root, q)
    return _assemble(
        q,
        match_entries(whitelist, q),
        playbook_hits,
        resolve_playbook_entries(playbook_hits, whitelist, q),
    )


def discover_sources_for_topic(
    topic: str,
    *,
    whitelist_path: Path | None = None,
    playbooks_dir: Path | None = None,
) -> dict[str, Any]:
    t = topic.strip()
    if not t:
        raise ValueError("topic must be non-empty")

    whitelist = load_whitelist(whitelist_path or DEFAULT_WHITELIST)
    playbooks_root = playbooks_dir_or_raise(playbooks_dir or DEFAULT_PLAYBOOKS)

    named = entities_named_in(whitelist, t)
    playbook_hits = playbooks_for_topic(playbooks_root, t, {e.domain for e in named})
    return _assemble(
        t,
        named,
        playbook_hits,
        resolve_playbook_entries(playbook_hits, whitelist, t),
    )


def filter_candidates_to_whitelist(
    candidates: list[dict[str, Any]],
    *,
    whitelist_path: Path | None = None,
) -> list[dict[str, Any]]:
    whitelist = load_whitelist(whitelist_path or DEFAULT_WHITELIST)
    by_domain = {e.domain: e for e in whitelist}
    kept: list[dict[str, Any]] = []
    for raw in candidates:
        domain = str(raw.get("domain") or "").strip().lower().removeprefix("www.")
        if not domain or not is_whitelisted_domain(domain, by_domain):
            continue
        entry = by_domain.get(domain)
        kept.append(
            {
                "entity": str(raw.get("entity") or (entry.entity if entry else domain)),
                "domain": domain,
                "url": raw.get("url"),
                "reason": raw.get("reason"),
                "whitelisted": True,
            }
        )
    return kept


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Discover whitelist + playbook sources for an entity or topic (#32).",
    )
    ap.add_argument("query", help='Entity or topic, e.g. "NIOC"')
    ap.add_argument(
        "--whitelist",
        type=Path,
        default=DEFAULT_WHITELIST,
        help="Path to source_whitelist.json",
    )
    ap.add_argument(
        "--playbooks",
        type=Path,
        default=DEFAULT_PLAYBOOKS,
        help="Path to local_knowledge_sources/playbooks",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional path to write JSON (also printed to stdout)",
    )
    args = ap.parse_args(argv)

    result = discover_sources(
        args.query,
        whitelist_path=args.whitelist,
        playbooks_dir=args.playbooks,
    )
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    sys.stdout.write(text)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
