# US crude — Gulf Coast

**Commodity:** crude  
**Geography:** United States — USGC export / Midcon linkage  
**Last reviewed:** 2026-07-23  

## Executive summary

US Gulf Coast crude production, inventory, and export dock capacity set WTI and waterborne US grade availability. Scan must catch first: EIA WPSR/production/export series, CME WTI structure, Port of Corpus Christi and other USGC logistics, DOE SPR policy, and hurricane-season weather/ops risk.

## Price drivers (trader lens)

1. EIA weekly stocks (Cushing + PADD) and crude export volumes.
2. US production trajectory and Permian takeaway.
3. USGC export dock utilization and port restrictions.
4. SPR release/refill (DOE).
5. Hurricane / freeze-off outages hitting production and ports.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| EIA | Weekly/monthly petroleum data | EIA |
| US DOE | SPR / energy policy | US DOE |
| CME Group | WTI futures | CME Group |
| Port of Corpus Christi | Major crude export port | Port of Corpus Christi |
| API | Inventory preview | API |
| Cushing tank farm terminals | Midcon delivery storage | Cushing tank farm terminals |
| OFAC (Treasury) | Sanctions affecting trade counterparties | OFAC (Treasury) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| EIA | eia.gov | WPSR; production; crude exports; STEO | P1 |
| US DOE | energy.gov | SPR releases/exchanges; policy | P1 |
| CME Group | cmegroup.com | WTI settlements; delivery notices | P1 |
| Port of Corpus Christi | portofcc.com | Port status; export logistics | P1 |
| API | api.org | Weekly inventory preview | P2 |
| Cushing tank farm terminals | enterpriseproducts.com | Cushing terminal context | P2 |
| BIS / OFAC (export controls) | commerce.gov | Export-control overlays | P3 |
| OFAC (Treasury) | treasury.gov | Counterparty sanctions | P3 |
| NOAA CPC | cpc.ncep.noaa.gov | Seasonal weather / hurricane outlook context | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Permian and other shale barrels move to USGC export terminals; Cushing links Midcon WTI delivery. Waterborne arb to Europe/Asia depends on freight and grade. LNG feedgas competes for gas but crude export capacity is the oil focus — see cushing_wti_delivery and us_lng_gulf_terminals for adjacent hubs.

## Geopolitical triggers

- SPR emergency release.
- Major hurricane closing USGC ports/production.
- Pipeline outage isolating Permian from docks.
- Trade-policy / sanctions shock on crude counterparties.
- Strategic export-dock force majeure.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| EIA WPSR | weekly | Wed ~15:30 US-linked |
| API weekly | weekly | Tue (typical) |
| CME settlements | daily | Exchange close |
| Port notices | event-driven | Local |
| DOE SPR | event-driven | US time |

## Tier 2 context sources

API as preview only; commerce/OFAC for edge cases. EIA remains the stock/export anchor.

## Anti-patterns

- Trading solely off API without EIA confirmation.
- Ignoring export dock status when WTI is weak on “overproduction.”
- Using retail inventory blogs as primary.

## Related playbooks

- cushing_wti_delivery.md
- oil_benchmarks_and_spreads.md
- us_lng_gulf_terminals.md
- crude_oil_global.md
- panama_malacca_routes.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
