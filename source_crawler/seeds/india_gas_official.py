"""India's official gas statistics — PPAC (#45).

Why these are crawled rather than searched
------------------------------------------
The India pilot's first run (test1, 2026-09-03) cited PNGRB, CEA, MoPNG, GAIL and
IndianOil, but **not PPAC** — the one source the playbook calls the balance
itself. The audit afterwards showed why, and it was not a routing failure:

  * a domain-filtered search *does* reach ppac.gov.in, but the index serves its
    old PDFs — the newest monthly report it returned was December 2024, in a run
    dated September 2026;
  * the current numbers are not on an HTML page at all. They are `.xlsx`
    downloads, which the evidence fetcher (`topics/search_content.py`) records as
    `unsupported`;
  * fetched directly, with our own user agent and one polite request, PPAC hands
    the file over with HTTP 200 and a `last-modified` inside the last fortnight.

So the failure was the *acquisition strategy*, not the source. We know PPAC's
URL; we do not need to discover it through a search engine, and searching for it
returns staler data than asking for it does. That is the third channel argued for
in #49 — known sources polled directly, off the search budget.

What is here, and what deliberately is not
------------------------------------------
`sectoral-consumption` and `import` publish their files as plain links in the
served HTML, so `landing_link` can follow them. The `consumption` and
`production` pages build their download links in JavaScript; those are **not**
seeded, because guessing at a scripted download is exactly the kind of
engineering we are not doing here. They belong to the semi-automatic
`browser-fetch` route (`docs/architecture/source_acquisition_pipeline.md`), where
a person saves the file once.

Both files are `data_feed` / `skip_rag`: they are monthly time series, not
explainers. Putting a spreadsheet of numbers through chunk-and-embed would give
the corpus prose it cannot use, while the value here is the balance itself.
"""

from __future__ import annotations

from ..models import SourceConfig

# Required by the enroll gate even for feeds that never reach RAG.
_FEED_LABELS = {
    "label_assignment": "human",
    "document_type": "official_data",
    "use_for": ("facts",),
}

# PPAC versions every upload with a publication timestamp and keeps the tail of
# the name stable, so the tail is what we match on:
#   1787815916_4_NG-C-Sectoral-Consumption.xlsx
#   ^^^^^^^^^^ changes each release      ^^^^^^ stable
# `NG-C` marks the current series, `NG-H` the historical one — matching `NG-C`
# keeps us on the live file rather than the archive.

INDIA_GAS_OFFICIAL_SOURCES: list[SourceConfig] = [
    SourceConfig(
        source_id="ppac_gas_sectoral_consumption",
        adapter="landing_link",
        endpoint="https://ppac.gov.in/natural-gas/sectoral-consumption",
        title="PPAC — Natural Gas Sectoral Consumption (monthly)",
        publisher="Petroleum Planning & Analysis Cell (PPAC), Government of India",
        # Monthly series, published roughly 3-4 weeks after month end; weekly
        # polling catches it without hammering the ministry.
        interval_hours=168,
        commodity="natural_gas",
        region="IN",
        tier=1,
        domain="official_stats",
        tags=("ppac", "india", "gas", "sectoral_consumption", "fertilizer", "cgd", "data_feed"),
        extras={
            "cadence": "monthly",
            # The demand split the operator brief is built around: fertilizer,
            # city gas, power, refinery. Nothing else publishes it officially.
            "link_pattern": r"NG-C[-_]Sectoral[-_]Consumption\.xlsx?$",
            "extension": ".xlsx",
            "pipeline": "data_feed",
            "skip_rag": True,
        },
        **_FEED_LABELS,
    ),
    SourceConfig(
        source_id="ppac_gas_lng_import",
        adapter="landing_link",
        endpoint="https://ppac.gov.in/natural-gas/import",
        title="PPAC — LNG Imports (monthly)",
        publisher="Petroleum Planning & Analysis Cell (PPAC), Government of India",
        interval_hours=168,
        commodity="natural_gas",
        region="IN",
        tier=1,
        domain="official_stats",
        tags=("ppac", "india", "lng", "imports", "import_dependence", "data_feed"),
        extras={
            "cadence": "monthly",
            # Half of India's balance is imported; this is the series that says
            # how much, against which "import dependence" claims are checked.
            "link_pattern": r"NG-C[-_]LNG[-_]Import\.xlsx?$",
            "extension": ".xls",
            "pipeline": "data_feed",
            "skip_rag": True,
        },
        **_FEED_LABELS,
    ),
]
