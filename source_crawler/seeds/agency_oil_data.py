from __future__ import annotations

from ..models import SourceConfig

_RAG_LABELS = {
    "label_assignment": "human",
    "document_type": "official_data",
    "use_for": ("facts", "trading_knowhow"),
}
# JODI is a data feed (CSV/ZIP → DB), not RAG — labels still required by enroll gate.
_FEED_LABELS = {
    "label_assignment": "human",
    "document_type": "official_data",
    "use_for": ("facts",),
}

AGENCY_OIL_DATA_SOURCES: list[SourceConfig] = [
    SourceConfig(
        source_id="opec_momr",
        adapter="opec_assetdb",
        endpoint="https://www.opec.org/monthly-oil-market-report.html",
        title="OPEC Monthly Oil Market Report (MOMR)",
        publisher="OPEC",
        interval_hours=168,
        commodity="crude_oil",
        tier=1,
        domain="supply_demand",
        tags=("opec", "momr", "quotas", "call_on_opec", "balance"),
        extras={
            "cadence": "monthly",
            "url_template": (
                "https://www.opec.org/assets/assetdb/momr-{month}-{year}.pdf"
            ),
            "extension": ".pdf",
            "download_aliases": ["momr.pdf", "MOMR.pdf"],
            "landing": "https://www.opec.org/opec_web/en/publications/338.htm",
            "portal": "https://momr.opec.org/",
        },
        **_RAG_LABELS,
    ),
    SourceConfig(
        source_id="opec_asb",
        adapter="opec_assetdb",
        endpoint="https://www.opec.org/annual-statistical-bulletin.html",
        title="OPEC Annual Statistical Bulletin (ASB)",
        publisher="OPEC",
        interval_hours=8760,
        commodity="crude_oil",
        tier=1,
        domain="supply_demand",
        tags=("opec", "asb", "reserves", "production", "exports"),
        extras={
            "cadence": "yearly",
            "url_template": "https://www.opec.org/assets/assetdb/asb-{year}.pdf",
            "extension": ".pdf",
            "download_aliases": ["asb.pdf", "ASB.pdf"],
            "landing": "https://www.opec.org/opec_web/en/publications/202.htm",
        },
        **_RAG_LABELS,
    ),
    SourceConfig(
        source_id="jodi_oil_world",
        adapter="jodi_dataset",
        endpoint="https://www.jodidata.org/oil/database/data-downloads.aspx",
        title="JODI Oil World Database",
        publisher="Joint Organisations Data Initiative",
        interval_hours=168,
        commodity="crude_oil",
        tier=1,
        domain="official_stats",
        tags=("jodi", "oil", "data_feed", "csv"),
        extras={
            "jodi_kind": "oil",
            "extension": ".zip",
            "pipeline": "data_feed",
            "skip_rag": True,
        },
        **_FEED_LABELS,
    ),
    SourceConfig(
        source_id="jodi_gas_world",
        adapter="jodi_dataset",
        endpoint="https://www.jodidata.org/gas/database/data-downloads.aspx",
        title="JODI Gas World Database",
        publisher="Joint Organisations Data Initiative",
        interval_hours=168,
        commodity="natural_gas",
        tier=1,
        domain="official_stats",
        tags=("jodi", "gas", "data_feed", "csv"),
        extras={
            "jodi_kind": "gas",
            "extension": ".zip",
            "pipeline": "data_feed",
            "skip_rag": True,
        },
        **_FEED_LABELS,
    ),
]
