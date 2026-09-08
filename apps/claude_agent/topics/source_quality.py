"""One definition of how authoritative a run's sources are (#39, #51).

A source counts as authoritative when the analyst classed it `primary_official`
or `data_feed`, **or** when its host is on the register. Both halves are needed
and neither is redundant: the class is the analyst's judgement about what the
document is, and the register is our own standing decision about who publishes
it — a ministry page the analyst classed `unknown` is still a ministry page.

That definition lives here and nowhere else. The frontend used to carry a second
one that counted only the class, so the ratio a customer read was narrower than
the ratio the system measured and no one could say which was "the" number. The
run now writes `source_mix.json` beside its other artifacts and the UI renders
it; local computation there survives only as a fallback for runs written before
this file did.
"""

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

SOURCE_MIX_FILENAME = "source_mix.json"


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


def write_source_mix(run_directory: Path, mix: SourceMix) -> Path | None:
    """Record the mix beside the run's other artifacts, for the owner and public views.

    The same number is also emitted on `report.ready` / `refresh.completed`, but an
    event is a moment and a reader arrives later — and a public reader gets no event
    stream at all (see `public_routes`). A file is what both views can read.

    Best effort: a report that exists must not be withheld because a derived
    summary of it could not be written.
    """
    path = run_directory / SOURCE_MIX_FILENAME
    try:
        path.write_text(json.dumps(mix.as_payload(), indent=2), encoding="utf-8")
    except OSError:
        return None
    return path
