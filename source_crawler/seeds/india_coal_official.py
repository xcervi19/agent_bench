"""India's coal balance at the power plant, as the regulator reports it (#56).

A trading desk asked for Indian coal: mining, transport, prices, and above all
stocks. Search finds the news about a coal crunch. It does not find the table
the news is written from — the Central Electricity Authority's Daily Coal Stock
Report, where each of ~190 coal-fired stations (~225 GW) shows its stock against
the stock it must hold, the coal it received and burnt that day, and who is
meant to fix a shortfall.

Measured 2026-10-09 over the seven reports 10-02..10-08: all-plant stock 21.05 →
20.62 Mt (33 % of normative), receipts below burn on every one of the seven days,
87 plants critical on 10-08, eight of them newly so within the week — among them
NTPC Barh (3.3 GW) and Ramagundem (2.6 GW). That is the "coal stocks" in the
desk's own words, as a table, from the obliged party.

Daily is the matching cadence: CEA publishes each day's report the next day.

The three monthly series beside it answer the desk's other questions from the
parties that hold the numbers: how much was mined and despatched (Ministry of
Coal, every producer; Coal India, ~75 % of output, with its subsidiaries), and
what non-regulated coal is fetching (CIL's e-auction premium over its notified
price — the nearest thing India publishes to a domestic spot price). Measured
2026-10-09: August output -3.8 % y/y nationally, CIL September offtake +12.5 %
y/y, and September's e-auction cleared 94 % over notified price against 54 %
for April-September — a tightening market, read from the seller's own filing.
"""

from __future__ import annotations

from ..adapters.cea_coal_stock import LANDING_URL
from ..models import SourceConfig

# Required by the enroll gate even for feeds that never reach RAG.
_FEED_LABELS = {
    "label_assignment": "human",
    "document_type": "official_data",
    "use_for": ("facts",),
}

INDIA_COAL_OFFICIAL_SOURCES: list[SourceConfig] = [
    SourceConfig(
        source_id="cea_daily_coal_stock",
        adapter="cea_coal_stock",
        endpoint=LANDING_URL,
        title="CEA Daily Coal Stock Report — coal-fired power stations, India",
        publisher="Central Electricity Authority (CEA), Fuel Management Division",
        interval_hours=24,
        # `feeds.COMMODITY_SYNONYMS` carries `thermal coal` / `steam coal` to this.
        # Deliberately not `power`: a coal stock table is not evidence for every
        # Indian electricity question, and a topic about coal names coal.
        commodity="coal",
        region="IN",
        tier=1,
        domain="official_stats",
        tags=("cea", "npp", "india", "coal", "coal_stocks", "power", "data_feed"),
        extras={"cadence": "daily", "pipeline": "data_feed"},
        **_FEED_LABELS,
    ),
    SourceConfig(
        source_id="moc_monthly_coal_statistics",
        adapter="landing_link",
        endpoint="https://coal.gov.in/public-information/monthly-statistics-at-glance",
        title="Ministry of Coal — Monthly Coal Statistics at a glance",
        publisher="Ministry of Coal, Government of India",
        # Posted ~3-4 weeks after month end; weekly polling catches it.
        interval_hours=168,
        commodity="coal",
        region="IN",
        tier=1,
        domain="official_stats",
        tags=("moc", "india", "coal", "production", "despatch", "imports", "data_feed"),
        extras={
            "cadence": "monthly",
            # Production, despatch, power-sector supply and imports by producer,
            # month and fiscal year to date, for every producer — not just CIL.
            # The page lists newest first: msg-Aug26.pdf, msg-july26.pdf, …
            "link_pattern": r"/sites/default/files/\d{4}-\d{2}/msg-[A-Za-z]+\d{2}\.pdf$",
            "extension": ".pdf",
            "pipeline": "data_feed",
        },
        **_FEED_LABELS,
    ),
]


# Coal India's landing pages answer 403 to the VPS (measured 2026-10-09; 200 from
# the operator's machine), and one failed source fails the whole crawl — which
# would take the daily CEA feed down with it on the slot's cron. So CIL's two
# monthly filings are their own seed, crawled from wherever coalindia.in answers
# and published to the slot from there (docs/ops/commands.md). The files
# themselves sit on CloudFront and download from anywhere; only the page that
# names them is refused.
INDIA_COAL_CIL_SOURCES: list[SourceConfig] = [
    SourceConfig(
        source_id="cil_production_offtake",
        adapter="landing_link",
        endpoint="https://www.coalindia.in/performance/physical/",
        title="Coal India — provisional production and offtake by subsidiary (monthly)",
        publisher="Coal India Limited (stock-exchange filing)",
        interval_hours=168,
        commodity="coal",
        region="IN",
        tier=1,
        domain="official_stats",
        tags=("cil", "coal_india", "india", "coal", "production", "offtake", "data_feed"),
        extras={
            "cadence": "monthly",
            # Filed to BSE/NSE on the 1st for the month just ended — the earliest
            # official production number of the month. The annexure is a scan, so
            # a digit can arrive split ("8 5" for 8.5); the totals row reads cleanly.
            "link_pattern": r"cloudfront\.net/documents/[^\s\"']*[Pp]roduction[^\s\"']*\.pdf$",
            "extension": ".pdf",
            "pipeline": "data_feed",
        },
        **_FEED_LABELS,
    ),
    SourceConfig(
        source_id="cil_swma_eauction",
        adapter="landing_link",
        endpoint="https://www.coalindia.in/performance/swma-e-auction-data/",
        title="Coal India — SWMA e-auction: quantity offered, allocated, premium over notified price",
        publisher="Coal India Limited (stock-exchange filing)",
        interval_hours=168,
        commodity="coal",
        region="IN",
        tier=1,
        domain="official_stats",
        tags=("cil", "coal_india", "india", "coal", "e_auction", "price", "premium", "data_feed"),
        extras={
            "cadence": "monthly",
            # The premium over notified price is India's published domestic
            # spot signal: it widens when power plants scramble for coal.
            "link_pattern": r"cloudfront\.net/documents/[^\s\"']+\.pdf$",
            "extension": ".pdf",
            "pipeline": "data_feed",
        },
        **_FEED_LABELS,
    ),
]
