"""Rule-based signal detection. Operates on recent events; emits Signal proposals."""

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from ..models import Event

CATEGORY_DIRECTION = {
    "supply_disruption": "bullish",
    "outage": "bullish",
    "demand_surge": "bullish",
    "policy": "neutral",
    "demand_drop": "bearish",
    "oversupply": "bearish",
}


@dataclass
class SignalProposal:
    kind: str
    commodity: str | None
    region: str | None
    direction: str
    confidence: float
    rationale: str
    event_ids: list[UUID]


def detect_signals(events: Iterable[Event]) -> list[SignalProposal]:
    grouped = _group_by_commodity_region(events)
    return [_build_proposal(key, items) for key, items in grouped.items() if _is_significant(items)]


def _group_by_commodity_region(events: Iterable[Event]) -> dict[tuple[str, str], list[Event]]:
    buckets: dict[tuple[str, str], list[Event]] = defaultdict(list)
    for e in events:
        buckets[(e.commodity or "unknown", e.region or "unknown")].append(e)
    return buckets


def _is_significant(events: list[Event]) -> bool:
    if not events:
        return False
    max_impact = max((e.impact_score or 0.0) for e in events)
    return max_impact >= 0.5 or len(events) >= 3


def _build_proposal(key: tuple[str, str], events: list[Event]) -> SignalProposal:
    commodity, region = key
    direction = _aggregate_direction(events)
    confidence = _aggregate_confidence(events)
    rationale = _summarize(events)
    return SignalProposal(
        kind="event_cluster",
        commodity=None if commodity == "unknown" else commodity,
        region=None if region == "unknown" else region,
        direction=direction,
        confidence=confidence,
        rationale=rationale,
        event_ids=[e.id for e in events],
    )


def _aggregate_direction(events: list[Event]) -> str:
    votes = [CATEGORY_DIRECTION.get(e.category, "neutral") for e in events]
    bullish = votes.count("bullish")
    bearish = votes.count("bearish")
    if bullish > bearish:
        return "bullish"
    if bearish > bullish:
        return "bearish"
    return "neutral"


def _aggregate_confidence(events: list[Event]) -> float:
    impacts = [e.impact_score or 0.0 for e in events]
    base = sum(impacts) / max(len(impacts), 1)
    cluster_bonus = min(len(events) * 0.05, 0.2)
    return round(min(base + cluster_bonus, 0.95), 2)


def _summarize(events: list[Event]) -> str:
    headlines = [e.summary for e in events[:3]]
    return " | ".join(headlines)
