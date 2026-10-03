"""Japan's nuclear fleet, as its operators are obliged to report it (#55).

A customer asked to follow Japanese nuclear power: planned operation, outages and
any news that moves it. Searching finds the news. It does not find the register
the news is written from — JEPX's HJKS, where every unit of 100 MW and above must
post a planned stop, an unplanned stop or a derating, with the cause and the
expected return date.

Measured 2026-10-03: 217 nuclear entries across ten operators, nine updated since
September. The newest three were Ohi 3 (unplanned, generator failure since 08-08,
no return date given), Ohi 3's periodic inspection booked from 10-05, and Onagawa 2's
next inspection booked for 2027-07 → 2028-08. That is "planned operation" in the
customer's own words, as a table, from the obliged party.

Daily is the matching cadence: the register is edited the hour a unit trips.
"""

from __future__ import annotations

from ..adapters.hjks_outages import OUTAGES_URL
from ..models import SourceConfig

JAPAN_NUCLEAR_OFFICIAL_SOURCES: list[SourceConfig] = [
    SourceConfig(
        source_id="jepx_hjks_nuclear_outages",
        adapter="hjks_outages",
        endpoint=OUTAGES_URL,
        title="JEPX HJKS — nuclear unit outages and deratings, Japan",
        publisher="Japan Electric Power Exchange (JEPX), 発電情報公開システム",
        interval_hours=24,
        # `feeds.COMMODITY_SYNONYMS` carries `nuclear` / `nuclear energy` to this.
        # Deliberately not `power`: that would hand an outage table to every
        # Japanese electricity topic, and a topic about the fleet names it.
        commodity="nuclear_power",
        region="JP",
        tier=1,
        domain="official_stats",
        tags=("jepx", "hjks", "japan", "nuclear", "power", "outage", "data_feed"),
        label_assignment="human",
        document_type="official_data",
        use_for=("facts",),
        extras={"cadence": "daily", "pipeline": "data_feed"},
    ),
]
