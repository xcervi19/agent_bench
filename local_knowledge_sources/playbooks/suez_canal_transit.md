# Suez Canal transit

**Commodity:** crude | LNG | products  
**Geography:** Egypt — Suez Canal (Red Sea ↔ Mediterranean)  
**Last reviewed:** 2026-07-23  

## Executive summary

Suez shortens Europe–Asia energy voyages; toll hikes, draft limits, blockages, or Red Sea avoidance that starves canal arrivals reprice freight and delivery timing for crude, products, and LNG. Scan must catch first: Suez Canal Authority notices (stats, tolls, disruptions), Egypt MFA security framing, and UKMTO/Red Sea conditions that determine whether tankers still offer the canal.

## Price drivers (trader lens)

1. SCA transit capacity, convoy rules, and toll schedule changes.
2. Physical blockage or prolonged restriction (ship grounding, conflict spillover).
3. Southern Red Sea / Bab el-Mandeb risk diverting cargoes to Cape before they reach Suez.
4. LNG and clean-product voyage economics vs Cape (freight + boil-off + time).
5. SUMED pipeline alternative signalling when VLCC/canal pairing is constrained.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Suez Canal Authority (SCA) | Canal operator / tolls / stats | Suez Canal Authority (SCA) |
| Ministry of Foreign Affairs | Egypt diplomacy / Suez security | Ministry of Foreign Affairs (mfa.gov.eg) |
| UKMTO (Maritime Trade Ops) | Approach-sea incident advisories | UKMTO (Maritime Trade Ops) |
| Saudi Ports Authority (Mawani) | Red Sea load/discharge context | Saudi Ports Authority (Mawani) |
| IMO | Maritime guidance | IMO |
| EMSA | EU maritime safety context | EMSA |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Suez Canal Authority (SCA) | suezcanal.gov.eg | Transit stats, tolls, disruption / navigation notices | P1 |
| Ministry of Foreign Affairs | mfa.gov.eg | Suez / Red Sea security diplomacy | P1 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Southern approaches incidents that cut Suez nominations | P1 |
| Saudi Ports Authority (Mawani) | mawani.gov.sa | Yanbu / Red Sea port flows linked to canal lane | P2 |
| Saudi Meteorology (Red Sea) | pme.gov.sa | Weather compounding canal/Red Sea ops | P3 |
| IMO | imo.org | Routing / security guidance | P2 |
| EMSA | emsa.europa.eu | EU maritime tracking/safety context | P3 |
| GISIS IMO | gisis.imo.org | Ship status under elevated risk | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Canal links Red Sea to Mediterranean; pairs with SUMED for some VLCC economics. Upstream risk at Bab el-Mandeb and downstream Med ports (Augusta, Trieste, etc.) matter for realized arrivals. Cape of Good Hope is the full diversion path when Suez/Red Sea is avoided — see `cape_route_saldanha` and `red_sea_bab_el_mandeb`.

## Geopolitical triggers

- SCA emergency navigation notice or toll shock.
- Grounding / blockage closing northbound or southbound lane.
- Escalation that empties the southern Red Sea of tankers (UKMTO).
- Egypt security operations affecting canal zone access.
- Prolonged liner/tanker Red Sea avoidance collapsing canal energy transit counts.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| SCA transit stats / notices | periodic + event-driven | Cairo time |
| UKMTO | event-driven | As issued |
| MFA Egypt | event-driven | Cairo time |

## Tier 2 context sources

EMSA/IMO background pages; meteorology for delay vs security discrimination. Not substitutes for SCA primary notices.

## Anti-patterns

- Treating every Red Sea headline as confirmed Suez closure.
- Using social “canal blocked” clips without SCA confirmation.
- Double-counting Cape diversion freight and imaginary barrel loss at Suez.
- Ignoring toll/draft changes that alter VLCC economics without a “closure.”

## Related playbooks

- red_sea_bab_el_mandeb.md
- yemen_houthi_red_sea.md
- cape_route_saldanha.md
- strait_of_gibraltar.md
- lng_global_supply.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
