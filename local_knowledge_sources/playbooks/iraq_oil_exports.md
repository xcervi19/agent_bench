# Iraq oil exports

**Commodity:** crude  
**Geography:** Iraq — Basra Gulf exports / northern outlets  
**Last reviewed:** 2026-07-23  

## Executive summary

Iraq’s seaborne crude is dominated by southern Basra loadings marketed via SOMO; outages, weather, OPEC+ math, and northern/Turkey politics move Basra differentials. Scan must catch first: oil.gov.iq and SOMO, MFA security framing, and Gulf weather/port continuity affecting southern terminals.

## Price drivers (trader lens)

1. Basra oil terminal loading programs and unplanned outages.
2. SOMO OSP/marketing signals vs peer Gulf grades.
3. OPEC+ compensation / quota vs actual southern exports.
4. Security incidents on southern infrastructure or export routes.
5. Northern export politics (Turkey corridor) as secondary path risk.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Ministry of Oil | Policy / upstream | Ministry of Oil (oil.gov.iq) |
| SOMO (State Oil Marketing Org) | Crude marketing | SOMO (State Oil Marketing Org) |
| Ministry of Foreign Affairs | Diplomacy / security | Ministry of Foreign Affairs (mofa.gov.iq) |
| Central Bank of Iraq | FX / budget oil linkage | Central Bank of Iraq |
| OPEC | Quota framework | OPEC |
| Saudi National Center for Meteorology | Regional Gulf weather | Saudi National Center for Meteorology |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Ministry of Oil | oil.gov.iq | Production / export policy; field status | P1 |
| SOMO (State Oil Marketing Org) | somooil.gov.iq | Marketing / OSP / customer notices | P1 |
| Ministry of Foreign Affairs | mofa.gov.iq | Security and corridor diplomacy | P2 |
| Central Bank of Iraq | cbi.iq | Oil-revenue / FX context | P3 |
| OPEC | opec.org | Iraq in MOMR / quota tables | P1 |
| Saudi National Center for Meteorology | ncm.gov.sa | Gulf weather affecting Basra loadings | P2 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Northern Gulf maritime incidents | P2 |
| IMO | imo.org | Maritime guidance | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Southern export terminals near Basra are the main seaborne outlet; weather and maintenance drive short-term program cuts. Northern pipeline politics (Türkiye) are a separate risk channel. Gulf security overlaps Hormuz approaches for laden tankers.

## Geopolitical triggers

- Southern terminal attack or force majeure.
- Budget/political crisis freezing export policy.
- OPEC+ compensation schedule forcing deeper cuts.
- Turkey corridor dispute cutting northern flows.
- Major SOMO term-contract restructuring.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| SOMO / Ministry of Oil | event-driven + periodic | Iraq time |
| OPEC MOMR | monthly | Mid-month |
| Weather / UKMTO | continuous / event | As issued |

## Tier 2 context sources

CBI macro; ISX financial (Tier 2). Not primary for loadings.

## Anti-patterns

- Local unverified “Basra closed” social posts.
- Conflating northern politics with southern seaborne availability.
- Using only OPEC quota as realized export volume.

## Related playbooks

- opec_plus_policy.md
- strait_of_hormuz.md
- saudi_arabia_oil.md
- kuwait_qatar_oil_gas.md
- turkish_straits_bospor.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
