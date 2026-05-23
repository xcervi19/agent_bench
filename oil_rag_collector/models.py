from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Literal


class DomainCluster(StrEnum):
    MARKET_PRICE = "market_price"
    SUPPLY_DEMAND = "supply_demand"
    INFRASTRUCTURE = "infrastructure"
    GEOPOLITICS = "geopolitics"
    MARITIME_LOGISTICS = "maritime_logistics"
    TRADING_MECHANICS = "trading_mechanics"
    REFERENCE_BOOK = "reference_book"


class SourceFormat(StrEnum):
    PDF = "pdf"
    HTML = "html"
    JSON = "json"
    API = "api"
    METADATA_ONLY = "metadata_only"


FetchKind = Literal["http_get", "eia_api", "discover_links", "static_urls"]


@dataclass(frozen=True)
class SourceSpec:
    id: str
    title: str
    url: str
    publisher: str
    tier: int
    domain: DomainCluster
    format: SourceFormat
    fetch: FetchKind = "http_get"
    commodity: str = "crude_oil"
    region: str | None = None
    tags: tuple[str, ...] = ()
    notes: str = ""
    enabled: bool = True
    optional: bool = False
    eia_series_id: str | None = None
    discover_seed_url: str | None = None
    discover_link_pattern: str | None = None
    max_discover: int = 25


@dataclass
class FetchOutcome:
    source_id: str
    status: Literal["ok", "skipped", "failed"]
    path: str | None = None
    bytes: int = 0
    content_type: str | None = None
    error: str | None = None
    discovered_from: str | None = None


@dataclass
class CollectionManifest:
    schema_version: int = 1
    collector_version: str = "1.0.0"
    output_dir: str = ""
    max_tier: int = 2
    outcomes: list[FetchOutcome] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "collector_version": self.collector_version,
            "output_dir": self.output_dir,
            "max_tier": self.max_tier,
            "stats": {
                "ok": sum(1 for o in self.outcomes if o.status == "ok"),
                "skipped": sum(1 for o in self.outcomes if o.status == "skipped"),
                "failed": sum(1 for o in self.outcomes if o.status == "failed"),
            },
            "outcomes": [
                {
                    "source_id": o.source_id,
                    "status": o.status,
                    "path": o.path,
                    "bytes": o.bytes,
                    "content_type": o.content_type,
                    "error": o.error,
                    "discovered_from": o.discovered_from,
                }
                for o in self.outcomes
            ],
        }
