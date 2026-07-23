# Australia LNG — NWS / Gorgon

**Commodity:** LNG  
**Geography:** Australia NW Shelf — NWS / Gorgon / Wheatstone class  
**Last reviewed:** 2026-07-23  

## Executive summary

Australian NW Shelf LNG (NWS/Gorgon/Wheatstone class) is a pillar of Asia supply; maintenance, cyclones, and regulator actions move JKM. Scan must catch first: nopsema.gov.au and nopta.gov.au (NWS/Gorgon notes), amsa.gov.au and abf.gov.au for maritime/export docs, plus IEA/EIA for balance context. Operator IR domains not on whitelist are not cited.

## Price drivers (trader lens)

1. Planned turnarounds and unplanned train trips on NW Shelf projects.
2. Cyclone season curtailments (AMSA/weather ops).
3. NOPSEMA/NOPTA regulatory or title actions.
4. Asia demand pull (Japan/Korea/China) vs Europe arb.
5. Domestic gas policy debates affecting export flexibility.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| NOPSEMA | Offshore safety/environment regulator | NOPSEMA |
| NOPTA – National Offshore Petroleum Titles Administrator | Titles / production reporting | NOPTA – National Offshore Petroleum Titles Administrator |
| AMSA (Maritime Safety Authority) | Maritime safety (Dampier/Gladstone LNG) | AMSA (Maritime Safety Authority) |
| Australian Border Force | Export cargo documentation | Australian Border Force |
| Department of Foreign Affairs and Trade | Diplomacy | Department of Foreign Affairs and Trade |
| ASX | Financial Tier 2 | ASX |
| IEA | LNG balances | IEA |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| NOPSEMA | nopsema.gov.au | Safety/env actions; NWS/Gorgon/Wheatstone oversight notes | P1 |
| NOPTA – National Offshore Petroleum Titles Administrator | nopta.gov.au | Titles; OPGGS production reporting | P1 |
| AMSA (Maritime Safety Authority) | amsa.gov.au | Maritime safety; Dampier/Gladstone LNG | P1 |
| Australian Border Force | abf.gov.au | Karratha/Darwin/Gladstone export declarations | P2 |
| Department of Foreign Affairs and Trade | dfat.gov.au | Trade/energy diplomacy | P3 |
| ASX | asx.com.au | Listed operator financial Tier 2 only | P3 |
| IEA | iea.org | Gas/LNG outlook | P1 |
| EIA | eia.gov | Global LNG context | P2 |
| Royal Australian Navy | navy.gov.au | Maritime security context | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

NW Shelf projects load from Pilbara/northern ports (Karratha/Dampier class) into Asia-facing shipping. Cyclones and maintenance dominate seasonal risk. Gladstone is east-coast LNG (ABF/AMSA notes) — separate basin but same national regulator set.

## Geopolitical triggers

- NOPSEMA enforcement stoppage on a major train.
- Severe cyclone season cutting multiple projects.
- Domestic reservation policy shock.
- Prolonged Asia demand destruction.
- Maritime security incident off NW Australia.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| NOPSEMA / NOPTA | event-driven + reporting cycles | Australia time |
| AMSA / ABF | event / ops | Australia time |
| IEA | outlook / ad hoc | As published |

## Tier 2 context sources

ASX listings; DFAT. Do not invent Woodside/Chevron domains — not used unless present in whitelist.

## Anti-patterns

- Citing non-whitelist operator URLs as Primary Official Sources.
- Treating Gladstone and Gorgon as one maintenance event.
- Ignoring cyclone forecasts when modeling Q1 cargoes.

## Related playbooks

- lng_global_supply.md
- japan_korea_lng_demand.md
- southeast_asia_lng_imports.md
- china_oil_gas_imports.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic; operator IR domains absent from whitelist
