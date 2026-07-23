# Cushing WTI delivery

**Commodity:** crude  
**Geography:** Cushing, Oklahoma — WTI delivery hub  
**Last reviewed:** 2026-07-23  

## Executive summary

Cushing inventories and tank/pipeline operability set WTI physical delivery and calendar spreads. Scan must catch first: EIA Cushing/PADD stocks, CME delivery notices, and enterpriseproducts.com terminal/tank-farm context linking Midcon storage to USGC takeaway.

## Price drivers (trader lens)

1. EIA weekly Cushing crude stocks.
2. Pipeline flows in/out of Cushing (Midcon vs Gulf).
3. CME delivery month tenders / EFP activity.
4. Tank capacity utilization and operational constraints.
5. SPR or USGC shocks transmitting into Midcon balances.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| EIA | Weekly stocks | EIA |
| CME Group | WTI contract / delivery | CME Group |
| Cushing tank farm terminals | Storage / terminal ops | Cushing tank farm terminals |
| US DOE | SPR policy spillover | US DOE |
| API | Inventory preview | API |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| EIA | eia.gov | Cushing stocks; WPSR; PADD balances | P1 |
| CME Group | cmegroup.com | WTI specs; settlements; delivery notices | P1 |
| Cushing tank farm terminals | enterpriseproducts.com | Tank/terminal and takeaway context | P1 |
| API | api.org | Weekly inventory preview | P2 |
| US DOE | energy.gov | SPR actions affecting US balances | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Cushing is the NYMEX WTI delivery point with extensive tank farms and pipeline interconnects to Permian, Rockies, and USGC. Storage economics drive contango/backwardation. See us_crude_gulf and oil_benchmarks_and_spreads.

## Geopolitical triggers

- Major pipeline outage isolating Cushing.
- SPR release flooding USGC and reversing Midcon flows.
- CME delivery dislocation / force majeure-style logistics event.
- Extreme weather impairing Midcon movements.
- Strategic tank fire / terminal incident.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| EIA WPSR | weekly | Wed ~15:30 US-linked |
| API weekly | weekly | Tue typical |
| CME | daily / delivery cycle | Exchange schedule |

## Tier 2 context sources

API preview only. Enterprise Products pages for logistics literacy, not a substitute for EIA stocks.

## Anti-patterns

- Trading Cushing off Twitter “tank pictures.”
- Ignoring USGC export capacity when Cushing builds.
- Treating API as final vs EIA.

## Related playbooks

- us_crude_gulf.md
- oil_benchmarks_and_spreads.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
