from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

import httpx

from .fetch import fetch_http
from .models import FetchOutcome, SourceSpec


def discover_urls(seed_url: str, html: str, pattern: str, base_url: str) -> list[str]:
    rx = re.compile(pattern, re.IGNORECASE)
    found: list[str] = []
    seen: set[str] = set()
    for match in rx.finditer(html):
        raw = match.group(1)
        full = urljoin(base_url, raw)
        if full in seen:
            continue
        seen.add(full)
        found.append(full)
    return found


def run_discovery(
    client: httpx.Client,
    spec: SourceSpec,
    root: Path,
) -> list[FetchOutcome]:
    if not spec.discover_seed_url or not spec.discover_link_pattern:
        raise ValueError(f"discovery misconfigured for {spec.id}")

    resp = client.get(spec.discover_seed_url)
    resp.raise_for_status()
    links = discover_urls(
        spec.discover_seed_url,
        resp.text,
        spec.discover_link_pattern,
        spec.discover_seed_url,
    )[: spec.max_discover]

    outcomes: list[FetchOutcome] = []
    for idx, link in enumerate(links):
        child_id = f"{spec.id}__{idx:03d}"
        child = SourceSpec(
            id=child_id,
            title=f"{spec.title} [{idx}]",
            url=link,
            publisher=spec.publisher,
            tier=spec.tier,
            domain=spec.domain,
            format=spec.format,
            commodity=spec.commodity,
            region=spec.region,
            tags=spec.tags,
        )
        outcome = fetch_http(
            client,
            child,
            root,
            url=link,
            discovered_from=spec.discover_seed_url,
            suffix=f"__d{idx:03d}",
        )
        outcomes.append(outcome)
    return outcomes
