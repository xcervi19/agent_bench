from __future__ import annotations

import json
from collections.abc import Collection, Iterable, Mapping
from dataclasses import asdict, dataclass
from json import JSONDecodeError
from pathlib import Path
from urllib.parse import urlparse

from ..sources.discover import DEFAULT_WHITELIST
from ..sources.whitelist import load_whitelist

AUTHORITATIVE_CLASSES = frozenset({"primary_official", "data_feed"})


@dataclass(frozen=True, slots=True)
class SourceMix:
    total: int
    authoritative: int
    whitelisted: int

    @property
    def authoritative_ratio(self) -> float:
        return self.authoritative / self.total if self.total else 0.0

    @property
    def is_entirely_secondary(self) -> bool:
        return self.total > 0 and self.authoritative == 0

    def as_payload(self) -> dict[str, object]:
        return {
            **asdict(self),
            "authoritative_ratio": round(self.authoritative_ratio, 3),
            "entirely_secondary": self.is_entirely_secondary,
        }


def load_whitelisted_domains(path: Path | None = None) -> frozenset[str]:
    return frozenset(entry.domain for entry in load_whitelist(path or DEFAULT_WHITELIST))


def host_of(url: str) -> str:
    try:
        return (urlparse(url).hostname or "").lower()
    except ValueError:
        return ""


def is_whitelisted(url: str, domains: Collection[str]) -> bool:
    host = host_of(url)
    return any(host == domain or host.endswith(f".{domain}") for domain in domains)


def is_authoritative(source: Mapping[str, object], domains: Collection[str]) -> bool:
    if source.get("source_class") in AUTHORITATIVE_CLASSES:
        return True
    return is_whitelisted(str(source.get("url") or ""), domains)


def summarize(sources: Iterable[Mapping[str, object]], domains: Collection[str]) -> SourceMix:
    rows = list(sources)
    return SourceMix(
        total=len(rows),
        authoritative=sum(1 for row in rows if is_authoritative(row, domains)),
        whitelisted=sum(1 for row in rows if is_whitelisted(str(row.get("url") or ""), domains)),
    )


def read_sources(news_path: Path) -> list[Mapping[str, object]]:
    try:
        document = json.loads(news_path.read_text(encoding="utf-8"))
    except (OSError, JSONDecodeError):
        return []
    sources = document.get("sources") if isinstance(document, dict) else None
    return [row for row in sources or [] if isinstance(row, Mapping)]


def summarize_run(run_directory: Path, domains: Collection[str]) -> SourceMix:
    return summarize(read_sources(run_directory / "news.json"), domains)
