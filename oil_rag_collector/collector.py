from __future__ import annotations

import json
from pathlib import Path

from .discover import run_discovery
from .eia_api import fetch_eia_series, resolve_eia_api_key
from .fetch import DomainRateLimiter, build_client, fetch_http
from .static_batch import run_static_batch
from .models import CollectionManifest, FetchOutcome
from .registry import export_registry_json, sources_for_download


def run_collection(
    output_dir: Path,
    *,
    max_tier: int = 2,
    timeout_sec: float = 90.0,
    skip_eia_api: bool = False,
) -> CollectionManifest:
    output_dir.mkdir(parents=True, exist_ok=True)
    registry_path = output_dir / "sources_registry.json"
    registry_path.write_text(
        json.dumps(export_registry_json(), indent=2),
        encoding="utf-8",
    )

    manifest = CollectionManifest(output_dir=str(output_dir.resolve()), max_tier=max_tier)
    limiter = DomainRateLimiter()
    specs = sources_for_download(max_tier=max_tier)

    eia_key: str | None = None
    if not skip_eia_api and any(s.fetch == "eia_api" for s in specs):
        eia_key = resolve_eia_api_key()

    with build_client(timeout_sec) as client:
        for spec in specs:
            limiter.wait(spec.url)
            if spec.fetch == "eia_api":
                if skip_eia_api:
                    manifest.outcomes.append(
                        FetchOutcome(spec.id, "skipped", error="eia_api_skipped")
                    )
                    continue
                outcome = fetch_eia_series(client, spec, output_dir, eia_key or "")
            elif spec.fetch == "discover_links":
                discovered = run_discovery(client, spec, output_dir)
                manifest.outcomes.extend(discovered)
                continue
            elif spec.fetch == "static_urls":
                batch = run_static_batch(client, spec, output_dir)
                manifest.outcomes.extend(batch)
                continue
            else:
                outcome = fetch_http(client, spec, output_dir)
            manifest.outcomes.append(outcome)

    manifest_path = output_dir / "collection_manifest.json"
    manifest_path.write_text(json.dumps(manifest.to_dict(), indent=2), encoding="utf-8")
    return manifest
