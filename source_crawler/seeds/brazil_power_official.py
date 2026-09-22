"""Brazil's official power-system series — ONS open data (#53).

Why these are crawled rather than searched
------------------------------------------
Same argument as PPAC (#45), one step stronger. Brazil's system operator
publishes the entire dispatch picture as open data: stored energy per reservoir,
natural inflow energy per subsystem, half-hourly marginal cost, and hourly
generation by source. Measured on 2026-09-18, the portal carried **85 datasets**
and the four seeded here had been rewritten **the same afternoon** (last-modified
15:00-15:02 UTC) with data through 2026-09-16.

No search engine surfaces a 4 MB CSV of reservoir levels as an answer, and no
aggregator republishes it as a market signal. We know the URL. Asking for it is
strictly better than searching for it, and it costs nothing from the search
budget — the third channel of #49.

The trading chain these four series carry, end to end:

    ENA (inflow, forward-looking) -> EAR (storage, where we are)
      -> thermal dispatch in the subsystem balance -> CMO (what it costs)
      -> gas burn -> LNG import call -> a cargo that does not reach Europe

Why XLSX and not CSV
--------------------
Both formats are published at stable per-year URLs. The XLSX is seeded because
`source_crawler/extract.py` still lists `.csv` in its skip set ("no converter for
.csv"), which would download these files and never read them — the same shape of
gap that left `ppac_gas_lng_import` unextracted as an `.xls`. The CSV URL is
recorded beside each entry so the switch is a one-line change once a converter
exists.

Known blocker, recorded rather than worked around
-------------------------------------------------
`topics/feeds.py` truncates an exported feed at `MAX_CHARS_PER_FEED` (60 000)
taking the **head** of the text. These files are chronological and run to several
megabytes for a full year, so a straight export would hand the analyst **January**
and silently drop September. Until a recent-tail window exists, these feeds are
seeded and crawled but must not be quoted as current. See #53 build item 1.

Robots
------
`dados.ons.org.br/robots.txt` disallows `/api/` with `Crawl-Delay: 10`, so the
CKAN API is used **once, by an operator, to resolve these URLs** — not by the
crawler. The files themselves are served from `ons-aws-prod-opendata.s3.amazonaws.com`,
a different host, which carries no such restriction. Resolve-by-hand, poll-by-URL
is the same semi-automatic split PPAC's JavaScript download pages forced.
"""

from __future__ import annotations

from ..models import SourceConfig

# Required by the enroll gate even for feeds that never reach RAG.
_FEED_LABELS = {
    "label_assignment": "human",
    "document_type": "official_data",
    "use_for": ("facts",),
}

# ONS keys each file by calendar year and rewrites it in place as the year runs.
# The year is therefore the only moving part of the URL, and it moves once — a
# dated maintenance item rather than a pattern worth matching at runtime.
_YEAR = 2026
_S3 = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset"

BRAZIL_POWER_OFFICIAL_SOURCES: list[SourceConfig] = [
    SourceConfig(
        source_id="ons_ear_reservoir_daily",
        adapter="static_file",
        endpoint=f"{_S3}/ear_reservatorio_di/EAR_DIARIO_RESERVATORIOS_{_YEAR}.xlsx",
        title="ONS — Stored energy by reservoir, daily (EAR)",
        publisher="Operador Nacional do Sistema Elétrico (ONS), Brazil",
        # Daily series with a ~2-day publication lag; a daily poll is the
        # matching cadence and the whole reason this topic suits a daily cycle.
        interval_hours=24,
        commodity="power",
        region="BR",
        tier=1,
        domain="official_stats",
        tags=("ons", "brazil", "power", "hydro", "reservoir", "ear", "data_feed"),
        extras={
            "cadence": "daily",
            "extension": ".xlsx",
            "pipeline": "data_feed",
            "skip_rag": True,
            "csv_url": f"{_S3}/ear_reservatorio_di/EAR_DIARIO_RESERVATORIOS_{_YEAR}.csv",
            # Read 2026-09-18: 67 reservoirs, mean fill 71.2 %, range 29 %-143 %.
            "chronological": True,
        },
        **_FEED_LABELS,
    ),
    SourceConfig(
        source_id="ons_ena_subsystem_daily",
        adapter="static_file",
        endpoint=f"{_S3}/ena_subsistema_di/ENA_DIARIO_SUBSISTEMA_{_YEAR}.xlsx",
        title="ONS — Natural inflow energy by subsystem, daily (ENA)",
        publisher="Operador Nacional do Sistema Elétrico (ONS), Brazil",
        interval_hours=24,
        commodity="power",
        region="BR",
        tier=1,
        domain="official_stats",
        tags=("ons", "brazil", "power", "hydro", "inflow", "ena", "data_feed"),
        extras={
            "cadence": "daily",
            "extension": ".xlsx",
            "pipeline": "data_feed",
            "skip_rag": True,
            "csv_url": f"{_S3}/ena_subsistema_di/ENA_DIARIO_SUBSISTEMA_{_YEAR}.csv",
            # The forward signal: EAR says where storage is, ENA says where it
            # is going. Quoted against the long-term average, never alone.
            "chronological": True,
        },
        **_FEED_LABELS,
    ),
    SourceConfig(
        source_id="ons_subsystem_energy_balance",
        adapter="static_file",
        endpoint=f"{_S3}/balanco_energia_subsistema_ho/BALANCO_ENERGIA_SUBSISTEMA_{_YEAR}.xlsx",
        title="ONS — Hourly generation by source and load, per subsystem",
        publisher="Operador Nacional do Sistema Elétrico (ONS), Brazil",
        interval_hours=24,
        commodity="power",
        region="BR",
        tier=1,
        domain="official_stats",
        tags=("ons", "brazil", "power", "thermal", "wind", "dispatch", "data_feed"),
        extras={
            "cadence": "hourly",
            "extension": ".xlsx",
            "pipeline": "data_feed",
            "skip_rag": True,
            "csv_url": f"{_S3}/balanco_energia_subsistema_ho/BALANCO_ENERGIA_SUBSISTEMA_{_YEAR}.csv",
            # `val_gertermica` is the thermal column that turns into an LNG
            # call. Read 2026-09-16: thermal 11.0 % of national generation,
            # 5.9 GW of the national 9.9 GW sitting in the Southeast.
            "chronological": True,
        },
        **_FEED_LABELS,
    ),
    SourceConfig(
        source_id="ons_cmo_semi_hourly",
        adapter="static_file",
        endpoint=f"{_S3}/cmo_tm/CMO_SEMIHORARIO_{_YEAR}.xlsx",
        title="ONS — Marginal operating cost, half-hourly by subsystem (CMO)",
        publisher="Operador Nacional do Sistema Elétrico (ONS), Brazil",
        interval_hours=24,
        commodity="power",
        region="BR",
        tier=1,
        domain="official_stats",
        tags=("ons", "brazil", "power", "price", "cmo", "data_feed"),
        extras={
            "cadence": "half_hourly",
            "extension": ".xlsx",
            "pipeline": "data_feed",
            "skip_rag": True,
            "csv_url": f"{_S3}/cmo_tm/CMO_SEMIHORARIO_{_YEAR}.csv",
            # CMO is the operator's marginal cost, not CCEE's settlement price
            # (PLD). Related, different institutions, do not conflate.
            "chronological": True,
        },
        **_FEED_LABELS,
    ),
]
