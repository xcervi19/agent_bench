# Qatar Ras Laffan LNG

**Commodity:** LNG  
**Geography:** Qatar — Ras Laffan / North Field  
**Last reviewed:** 2026-07-23  

## Executive summary

QatarEnergy’s Ras Laffan complex and North Field expansion dominate global LNG supply growth; outages or Hormuz risk reprice JKM/TTF arb. Scan must catch first: qatarenergy.qa, mme.gov.qa, Mwani port status, GECF/IEA context, and UKMTO Hormuz advisories.

## Price drivers (trader lens)

1. Ras Laffan train availability and maintenance.
2. North Field expansion commissioning timing.
3. Hormuz transit risk on Qatar LNG.
4. Term vs spot allocation to Asia/Europe.
5. Extreme Gulf weather interrupting loadings.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| QatarEnergy | NOC / LNG | QatarEnergy |
| Ministry of Energy and Industry | Policy | Ministry of Energy and Industry |
| Mwani Qatar | Ports | Mwani Qatar |
| Ministry of Foreign Affairs | Diplomacy | Ministry of Foreign Affairs (mofa.gov.qa) |
| GECF | Exporter forum | GECF |
| IEA | Gas/LNG balances | IEA |
| UKMTO (Maritime Trade Ops) | Maritime risk | UKMTO (Maritime Trade Ops) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| QatarEnergy | qatarenergy.qa | Ras Laffan ops; North Field; offtake | P1 |
| Ministry of Energy and Industry | mme.gov.qa | Energy policy / project approvals | P1 |
| Mwani Qatar | mwani.com.qa | Port status | P1 |
| Ministry of Foreign Affairs | mofa.gov.qa | Diplomacy / security framing | P2 |
| GECF | gecf.org | Producer supply narrative | P2 |
| IEA | iea.org | Gas Market Report | P1 |
| EIA | eia.gov | Global LNG context | P2 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Hormuz/Gulf incidents | P1 |
| ICE | ice.com | TTF arb context | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Ras Laffan is the concentrated liquefaction/export hub; almost all Qatar LNG faces Hormuz transit. Expansion trains are the structural supply story. See lng_global_supply and strait_of_hormuz.

## Geopolitical triggers

- QatarEnergy FM / major train trip.
- Hormuz escalation.
- Diplomatic crisis affecting offtake politics.
- Red Sea diversion lengthening Europe voyages.
- Buyer force majeure cascade.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| QatarEnergy / mme.gov.qa | event-driven | Gulf time |
| IEA gas publications | quarterly / ad hoc | As published |
| UKMTO | event-driven | As issued |

## Tier 2 context sources

GECF outlooks. QatarEnergy remains primary.

## Anti-patterns

- Unofficial North Field delay Telegram rumors.
- Ignoring Hormuz when modeling Qatar–Europe delivery.
- Treating all Middle East LNG as Qatar.

## Related playbooks

- lng_global_supply.md
- kuwait_qatar_oil_gas.md
- strait_of_hormuz.md
- japan_korea_lng_demand.md
- europe_gas_storage_ttf.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
