# US LNG Gulf terminals

**Commodity:** LNG  
**Geography:** US Gulf Coast liquefaction / export  
**Last reviewed:** 2026-07-23  

## Executive summary

USGC LNG exports (Cheniere and peers) link Henry Hub to global LNG; feedgas, DOE/FERC authorization, and hurricane risk set cargo availability. Scan must catch first: cheniere.com, eia.gov gas/LNG series, energy.gov authorizations, ferc.gov, portofcc.com, and CME Henry Hub.

## Price drivers (trader lens)

1. Feedgas demand / terminal utilization.
2. DOE export authorization and FERC outage/authorization news.
3. Hurricane / freeze-offs cutting production or docks.
4. HH vs TTF/JKM arb incentivizing cargoes.
5. Panama draft limits delaying Asia-bound voyages.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Cheniere Sabine Pass LNG | Export proxy / operator IR | Cheniere Sabine Pass LNG |
| EIA | US gas & LNG data | EIA |
| US DOE | Export authorizations | US DOE |
| FERC (LNG export authorization) | FERC oversight | FERC (LNG export authorization) |
| Port of Corpus Christi | Export port | Port of Corpus Christi |
| CME Group | Henry Hub | CME Group |
| BSEE (offshore safety) | Offshore safety | BSEE (offshore safety) |
| Panama Canal Authority (ACP) | Asia route constraint | Panama Canal Authority (ACP) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Cheniere Sabine Pass LNG | cheniere.com | Train utilization; shipping; feedgas | P1 |
| EIA | eia.gov | Weekly gas; LNG exports; STEO | P1 |
| US DOE | energy.gov | LNG export authorizations | P1 |
| FERC (LNG export authorization) | ferc.gov | Authorization / facility dockets | P1 |
| Port of Corpus Christi | portofcc.com | Port status | P1 |
| CME Group | cmegroup.com | Henry Hub settlements | P1 |
| BSEE (offshore safety) | bsee.gov | Offshore safety stoppages | P2 |
| Customs and Border Protection (CBP) | cbp.gov | Trade control context | P3 |
| Panama Canal Authority (ACP) | pancanal.com | Draft limits for USGC–Asia LNG | P2 |
| NOAA / NWS Houston | weather.gov | Hurricane / Gulf weather | P1 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Sabine Pass and other USGC liquefaction trains take Permian/Haynesville-linked feedgas; exports clear to Europe and Asia (Panama-sensitive). Weather.gov Houston is the ops weather primary. See lng_global_supply and panama_malacca_routes.

## Geopolitical triggers

- DOE policy shock on export authorizations.
- Major hurricane closing USGC LNG.
- FERC-ordered facility curtailment.
- Freeze-off crushing feedgas.
- Prolonged Panama drought stranding Asia schedules.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| EIA weekly gas | weekly | Thu US-linked |
| Cheniere releases | event-driven | US time |
| DOE/FERC | event-driven | US time |
| Weather.gov | continuous | US time |

## Tier 2 context sources

CBP; BSEE for edge safety events. EIA + Cheniere + DOE/FERC are core.

## Anti-patterns

- Treating Cheniere as all US LNG capacity without checking other trains.
- Ignoring feedgas when counting nameplate export capacity.
- Broker cargo lists without EIA confirmation of export trend.

## Related playbooks

- lng_global_supply.md
- natural_gas_global.md
- us_crude_gulf.md
- panama_malacca_routes.md
- europe_gas_storage_ttf.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
