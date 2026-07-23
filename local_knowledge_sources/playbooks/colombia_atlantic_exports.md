# Colombia Atlantic exports

**Commodity:** crude  
**Geography:** Colombia — Andean production / Caribbean Atlantic exports  
**Last reviewed:** 2026-07-23  

## Executive summary

Colombian crude exports hinge on Ecopetrol ops, pipeline security, and Caribbean load ports; licensing policy (ANH) sets medium-term supply. Scan must catch first: ecopetrol.com.co, minenergia.gov.co, anh.gov.co (no-new-licence policy notes), and armada.mil.co for export-route security.

## Price drivers (trader lens)

1. Ecopetrol production / pipeline FM (attacks, landslides).
2. Caribbean terminal restrictions.
3. ANH licensing stance (structural supply).
4. Security along Ocensa-class pipeline corridors.
5. USGC/Atlantic differentials for Colombian grades.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Ecopetrol | NOC | Ecopetrol |
| Ministry of Mines and Energy | Policy | Ministry of Mines and Energy |
| ANH Colombia | Upstream regulator | ANH Colombia |
| Colombian Navy | Maritime security | Colombian Navy |
| Ministry of Foreign Affairs | Diplomacy | Ministry of Foreign Affairs (cancilleria.gov.co) |
| Banco de la República | Macro/FX | Banco de la República |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Ecopetrol | ecopetrol.com.co | Production; pipeline status; FM; exports | P1 |
| Ministry of Mines and Energy | minenergia.gov.co | Energy/export policy | P1 |
| ANH Colombia | anh.gov.co | Licensing — “no new E&P licenses” policy signal | P1 |
| Colombian Navy | armada.mil.co | Coastal / export security | P2 |
| Ministry of Foreign Affairs | cancilleria.gov.co | Security diplomacy | P3 |
| Banco de la República | banrep.gov.co | COP / macro | P3 |
| EIA | eia.gov | Colombia in balances | P2 |
| OPEC | opec.org | Context only | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Andean fields move by pipeline to Caribbean export terminals; attacks and geohazards are recurring FM causes. Atlantic liftings compete into USGC and other Atlantic refiners. ANH licensing stance is a structural bearish supply note per whitelist.

## Geopolitical triggers

- Pipeline bombing / prolonged FM.
- ANH or ministry policy hardening against new E&P.
- Port strike or Navy security zone affecting loadings.
- Fiscal reform shock to Ecopetrol CAPEX.
- Major landslide season cutting pipeline throughput.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Ecopetrol releases | event-driven + periodic | Colombia time |
| MinEnergia / ANH | event-driven | Local |
| Navy notices | event-driven | Local |

## Tier 2 context sources

Banrep; BVC financial. Ecopetrol + ANH/MinEnergia are primary.

## Anti-patterns

- Guerrilla-claim social posts without Ecopetrol FM.
- Ignoring ANH licensing as only “politics,” not supply.
- Conflating Ecuador pipeline events with Colombia.

## Related playbooks

- ecuador_amazon_pipelines.md
- us_crude_gulf.md
- venezuela_sanctions_exports.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
