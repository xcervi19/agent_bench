# Canada heavy oil / TMX

**Commodity:** crude  
**Geography:** Canada — oil sands / Pacific TMX export path  
**Last reviewed:** 2026-07-23  

## Executive summary

Canadian heavy (WCS-linked) balances hinge on oil-sands output, US takeaway, and Pacific export capacity via TMX licensing/ops under federal regulators. Scan must catch first: CER and NRCan (TMX export licence / policy), CAPP production context, Transport Canada logistics, and Bank of Canada FX/netback signals.

## Price drivers (trader lens)

1. Oil-sands production and unplanned upgrader/coker outages.
2. TMX utilisation / Pacific export nominations vs US pipeline takeaway.
3. WCS differentials to WTI (netback).
4. Federal/provincial regulatory or protest disruptions.
5. CAD and Banxico-comparable macro (BoC) affecting CAPEX/netbacks.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Canada Energy Regulator (CER) | Federal energy regulator | Canada Energy Regulator (CER) |
| NRCan – Natural Resources Canada | Policy / TMX licence context | NRCan – Natural Resources Canada |
| Natural Resources Canada | Policy | Natural Resources Canada |
| CAPP | Industry production data | CAPP |
| Transport Canada | Transport / marine logistics | Transport Canada |
| Bank of Canada | FX / rates | Bank of Canada |
| Canada Border Services Agency (CBSA) | Cross-border oil trade docs | Canada Border Services Agency (CBSA) |
| Global Affairs Canada | Diplomacy / sanctions alignment | Global Affairs Canada |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Canada Energy Regulator (CER) | cer-rec.gc.ca | Pipeline / export regulation; ops data | P1 |
| NRCan – Natural Resources Canada | nrcan.gc.ca | TMX licence / oil sands / LNG Canada policy notes | P1 |
| Natural Resources Canada | natural-resources.canada.ca | Federal energy policy | P1 |
| CAPP | capp.ca | Canadian crude / oil sands output data | P1 |
| Transport Canada | tc.canada.ca | Marine/transport constraints | P2 |
| Canada Border Services Agency (CBSA) | cbsa-asfc.gc.ca | Export documentation / border oil trade | P2 |
| Bank of Canada | bankofcanada.ca | CAD/USD netback / rate signal | P2 |
| Global Affairs Canada | international.gc.ca | Trade/sanctions diplomacy | P3 |
| Environment and Climate Change Canada | canada.ca | Climate policy overlays | P3 |
| EIA | eia.gov | Canada in US/import balances | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Oil sands barrels move east/south to US or west via Pacific export capacity (TMX context in NRCan notes). Differentials encode pipeline constraints. Marine export weather and West Coast logistics sit under Transport Canada oversight.

## Geopolitical triggers

- TMX capacity/ops shock or regulatory action (CER/NRCan).
- Major oil-sands wildfire or facility outage.
- Cross-border trade friction (CBSA / US policy).
- Federal climate policy tightening oil-sands CAPEX.
- Prolonged WCS blowout signalling takeaway failure.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| CAPP / CER data | periodic | Canada time |
| NRCan / CER notices | event-driven | Canada time |
| BoC | scheduled + event | Canada time |
| EIA | weekly/monthly | US schedule |

## Tier 2 context sources

TMX Group (tmx.com) is a financial exchange — not the pipeline operator; do not treat as TMX pipeline primary. ECCC policy pages are context only.

## Anti-patterns

- Using tmx.com stock exchange as Trans Mountain ops source.
- Retail “WCS forecast” blogs as primary.
- Ignoring US takeaway when blaming only Pacific exports.

## Related playbooks

- us_crude_gulf.md
- oil_benchmarks_and_spreads.md
- mexico_maya_crude.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
