# Norway Hammerfest LNG

**Commodity:** LNG | gas  
**Geography:** Norway — Hammerfest LNG / Norwegian Continental Shelf  
**Last reviewed:** 2026-07-23  

## Executive summary

Equinor’s Hammerfest LNG and broader Norwegian gas export availability are critical for European TTF; outages reprice NWE gas quickly. Scan must catch first: equinor.com, sodir.no, regjeringen.no (OED), kystverket.no coastal traffic, and met.no weather.

## Price drivers (trader lens)

1. Hammerfest LNG unplanned outages / restart timelines.
2. Norwegian pipeline gas export maintenance (Equinor system).
3. Weather and coastal traffic constraints in the north.
4. EU storage trajectory interacting with Norway supply.
5. Hydropower/Nordic power overlays affecting gas burn (context).

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Equinor | Producer / Hammerfest | Equinor |
| Norwegian Offshore Directorate | Upstream data | Norwegian Offshore Directorate |
| Ministry of Energy (OED) | Policy | Ministry of Energy (OED) |
| Kystverket coastal traffic | Coastal traffic | Kystverket coastal traffic |
| Norwegian Meteorological Institute | Weather | Norwegian Meteorological Institute |
| Gas Infrastructure Europe | EU storage demand pull | Gas Infrastructure Europe |
| ICE | TTF | ICE |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Equinor | equinor.com | Hammerfest status; field/export FM | P1 |
| Norwegian Offshore Directorate | sodir.no | Production data | P1 |
| Ministry of Energy (OED) | regjeringen.no | Norway energy policy | P1 |
| Kystverket coastal traffic | kystverket.no | Coastal traffic / maritime ops | P2 |
| Norwegian Meteorological Institute | met.no | Arctic/North weather | P2 |
| Gas Infrastructure Europe | gie.eu | EU storage fill | P1 |
| ENTSOG | entsog.eu | Flow transparency toward EU | P1 |
| ICE | ice.com | TTF settlements | P1 |
| IEA | iea.org | Gas outlook | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Hammerfest LNG is Europe’s key Arctic Atlantic LNG source from Norway; pipeline gas to NWE is the larger volume sibling. Outage communications from Equinor move TTF within hours. See europe_gas_storage_ttf and natural_gas_global.

## Geopolitical triggers

- Hammerfest fire/outage recurrence.
- Broad Norwegian export maintenance season surprise.
- EU emergency gas measures interacting with Norway flows.
- Extreme Arctic weather cutting loadings.
- Security incident on Norwegian energy infrastructure.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Equinor notices | event-driven | Norway time |
| GIE / ENTSOG | daily / near-real-time | EU |
| ICE TTF | daily | Exchange close |
| met.no | continuous | Local |

## Tier 2 context sources

Oslo Bors financial; IEA outlooks. Equinor + OED/SODIR are primary.

## Anti-patterns

- Pricing TTF off rumor before equinor.com notice.
- Ignoring pipeline gas when only watching LNG trains.
- Conflating Hammerfest with Yamal Arctic LNG.

## Related playbooks

- europe_gas_storage_ttf.md
- natural_gas_global.md
- north_sea_crude.md
- lng_global_supply.md
- nord_stream_alternatives_eu.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
