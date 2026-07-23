# Mexico Maya crude

**Commodity:** crude  
**Geography:** Mexico — Gulf export grades (Maya)  
**Last reviewed:** 2026-07-23  

## Executive summary

Pemex production and export policy set Maya and Mexican heavy/medium availability into USGC and wider markets. Scan must catch first: pemex.com ops/export signals, SENER and CNH regulatory cues, ASEA safety/environment actions, and Banxico FX context for netbacks.

## Price drivers (trader lens)

1. Pemex production declines/outages and export programme cuts.
2. Maya differential vs WTI/USGC heavies.
3. CNH / SENER policy on upstream and export priorities.
4. ASEA safety stoppages at platforms/terminals.
5. USGC refining demand for Maya-quality resid feedstock.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Pemex | NOC | Pemex |
| SENER Mexico | Energy ministry | SENER Mexico |
| CNH (Hydrocarbons Commission) | Upstream regulator | CNH (Hydrocarbons Commission) |
| ASEA | Safety / environmental regulator | ASEA |
| SAT / Aduanas | Customs | SAT / Aduanas |
| Banco de México (Banxico) | FX | Banco de México (Banxico) |
| EIA | US import context | EIA |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Pemex | pemex.com | Production; exports; FM; terminal status | P1 |
| SENER Mexico | gob.mx/sener | Energy policy; export framing | P1 |
| CNH (Hydrocarbons Commission) | gob.mx/cnh | Upstream licensing / production oversight | P1 |
| ASEA | gob.mx/asea | Safety/environmental stoppages | P1 |
| SAT / Aduanas | sat.gob.mx | Export customs administration | P2 |
| Banco de México (Banxico) | banxico.org.mx | MXN netback / macro | P3 |
| EIA | eia.gov | Mexico in US crude imports / STEO | P2 |
| OPEC | opec.org | Mexico context if relevant to balances | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Gulf of Mexico platforms and export terminals feed USGC and other buyers; Maya is a key heavy sour grade for complex refiners. Outages and fuel-oil/domestic priority can cut exportable barrels quickly.

## Geopolitical triggers

- Pemex major platform/terminal FM.
- ASEA-ordered production halt.
- Policy shift prioritizing domestic refining over exports.
- Hurricane in Mexican Gulf waters.
- USGC heavy-sour arb collapse reducing liftings.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Pemex releases | event-driven + periodic | Mexico time |
| SENER / CNH / ASEA | event-driven | Mexico time |
| EIA | weekly/monthly | US schedule |

## Tier 2 context sources

Banxico; OPEC footnotes. Pemex + regulators are primary.

## Anti-patterns

- Unofficial Maya price Telegram feeds as OSP truth.
- Ignoring ASEA when platforms are offline.
- Conflating Chile CNH (cnh.gob.cl) with Mexico CNH — use gob.mx/cnh only.

## Related playbooks

- us_crude_gulf.md
- venezuela_sanctions_exports.md
- canada_heavy_oil_tmx.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
