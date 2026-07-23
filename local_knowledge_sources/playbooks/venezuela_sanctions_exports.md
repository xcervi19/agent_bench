# Venezuela sanctions exports

**Commodity:** crude  
**Geography:** Venezuela — upgraders / Caribbean export  
**Last reviewed:** 2026-07-23  

## Executive summary

Venezuelan heavy crude availability is a sanctions-and-license story: OFAC authorizations and PDVSA/INEA logistics determine whether barrels reach the water. Scan must catch first: treasury.gov OFAC licenses/SDN changes, pdvsa.com and inea.gob.ve ops signals, then buyer/waiver geopolitics.

## Price drivers (trader lens)

1. OFAC license grants, renewals, or revocations.
2. PDVSA production/upgrader status affecting exportable grades.
3. Port/terminal operability (INEA).
4. Diluent availability and blending constraints.
5. Heavy-sour differentials into USGC/Asia when licenses widen.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| PDVSA | NOC | PDVSA |
| INEA | Waterway / infra authority context | INEA |
| OFAC (Treasury) | Sanctions / licenses | OFAC (Treasury) |
| US Dept of State | Sanctions diplomacy | US Dept of State |
| BIS / OFAC (export controls) | Export controls | BIS / OFAC (export controls) |
| EIA | US import/impact context | EIA |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| OFAC (Treasury) | treasury.gov | GLs, FAQs, SDN, Venezuela-related actions | P1 |
| US Dept of State | state.gov | Policy coordination on Venezuela energy | P1 |
| BIS / OFAC (export controls) | commerce.gov | Control list overlays | P2 |
| PDVSA | pdvsa.com | Production / export / ops statements | P1 |
| INEA | inea.gob.ve | Port/waterway infrastructure status | P1 |
| EIA | eia.gov | US crude import impacts / balances | P2 |
| IMO | imo.org | Maritime sanctions guidance | P3 |
| GISIS IMO | gisis.imo.org | Tanker screening | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Orinoco Belt heavies need upgraders/diluent; Caribbean loadouts and sanctioned logistics chains dominate. License scope often specifies counterparties, terminals, or US entry — legal text on treasury.gov outranks market rumor.

## Geopolitical triggers

- OFAC general license change.
- Election/political shock altering enforcement posture.
- Major upgrader outage.
- Secondary sanctions threat on offtakers/tankers.
- USGC heavy-sour arb reopening on waiver expansion.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| OFAC / State | event-driven | US business hours |
| PDVSA / INEA | event-driven | Local |
| EIA | weekly/monthly | US schedule |

## Tier 2 context sources

EIA import tables for realized flows (lagged). Not a substitute for OFAC legal status.

## Anti-patterns

- Counting barrels from secondary media while licenses are expired.
- Ignoring diluent/upgrader bottlenecks when licenses exist.
- Unofficial “PDVSA cargo list” Telegram channels as primary.

## Related playbooks

- energy_sanctions_compliance.md
- us_crude_gulf.md
- crude_oil_global.md
- mexico_maya_crude.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
