from __future__ import annotations

import httpx

from .eia_countries import eia_country_overview_urls
from .fetch import fetch_http
from .models import FetchOutcome, SourceSpec


def run_static_batch(
    client: httpx.Client,
    spec: SourceSpec,
    root: Path,
) -> list[FetchOutcome]:
    if spec.id != "static_eia_country_overviews":
        raise ValueError(f"unsupported static batch: {spec.id}")

    urls = eia_country_overview_urls()[: spec.max_discover]
    outcomes: list[FetchOutcome] = []
    for idx, link in enumerate(urls):
        child = SourceSpec(
            id=f"{spec.id}__{idx:03d}",
            title=f"{spec.title} [{idx}]",
            url=link,
            publisher=spec.publisher,
            tier=spec.tier,
            domain=spec.domain,
            format=spec.format,
            optional=True,
            tags=spec.tags,
        )
        outcomes.append(
            fetch_http(
                client,
                child,
                root,
                url=link,
                discovered_from=spec.url,
                suffix=f"__s{idx:03d}",
            )
        )
    return outcomes
