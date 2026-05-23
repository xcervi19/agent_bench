from __future__ import annotations

import json
import os
from pathlib import Path

import httpx

from .fetch import _target_path
from .models import FetchOutcome, SourceSpec

EIA_BASE = "https://api.eia.gov/v2"


def fetch_eia_series(
    client: httpx.Client,
    spec: SourceSpec,
    root: Path,
    api_key: str,
) -> FetchOutcome:
    if not spec.eia_series_id:
        raise ValueError(f"eia_series_id required for {spec.id}")

    path = spec.eia_series_id.lstrip("/")
    url = f"{EIA_BASE}/{path}"
    resp = client.get(url, params={"api_key": api_key})
    resp.raise_for_status()
    payload = resp.json()

    dest = _target_path(root, spec, ".json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return FetchOutcome(
        source_id=spec.id,
        status="ok",
        path=str(dest.relative_to(root)),
        bytes=dest.stat().st_size,
        content_type="application/json",
    )


def resolve_eia_api_key() -> str:
    key = os.environ.get("EIA_API_KEY", "").strip()
    if not key:
        raise RuntimeError("EIA_API_KEY is required for EIA API sources (register at https://www.eia.gov/opendata/)")
    return key
