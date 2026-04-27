"""RSS feed registry + fetcher. Returns normalized items ready for ingestion."""

from dataclasses import dataclass
from datetime import datetime
from time import mktime

import feedparser

FEEDS_BY_COMMODITY: dict[str, list[str]] = {
    "power": [
        "https://www.reuters.com/markets/commodities/rss",
        "https://www.euractiv.com/sections/energy/feed/",
    ],
    "gas": [
        "https://www.reuters.com/markets/commodities/rss",
        "https://www.euractiv.com/sections/energy/feed/",
    ],
    "lng": [
        "https://www.reuters.com/markets/commodities/rss",
    ],
    "coal": [
        "https://www.reuters.com/markets/commodities/rss",
    ],
    "carbon": [
        "https://www.euractiv.com/sections/energy-environment/feed/",
    ],
}


@dataclass
class FeedItem:
    source: str
    url: str
    title: str
    summary: str
    published_at: datetime | None
    language: str | None


def fetch_feed(url: str, *, max_items: int = 25) -> list[FeedItem]:
    parsed = feedparser.parse(url)
    return [_normalize(url, e) for e in parsed.entries[:max_items]]


def _normalize(source: str, entry) -> FeedItem:
    return FeedItem(
        source=source,
        url=entry.get("link", ""),
        title=entry.get("title", "").strip(),
        summary=_clean_summary(entry.get("summary", "")),
        published_at=_to_datetime(entry.get("published_parsed")),
        language=entry.get("language"),
    )


def _clean_summary(html: str) -> str:
    if not html:
        return ""
    text = html.replace("<p>", " ").replace("</p>", " ")
    while "<" in text and ">" in text:
        start = text.index("<")
        end = text.index(">", start)
        text = text[:start] + text[end + 1 :]
    return " ".join(text.split())


def _to_datetime(struct_time) -> datetime | None:
    if not struct_time:
        return None
    return datetime.fromtimestamp(mktime(struct_time))
