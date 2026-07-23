# LNG — global supply

**Commodity:** LNG  
**Geography:** global  
**Last reviewed:** 2026-07-23  

## Executive summary

Global LNG balances are driven by Qatar North Field growth, US Gulf export utilization, Australian maintenance, and European/Asian demand competition. Scan must catch first: QatarEnergy project/export signals, Cheniere/US feedgas and export runs (EIA), GECF/IEA gas commentary, and EU storage/policy that pulls cargoes west.

## Price drivers (trader lens)

1. US LNG feedgas demand and terminal utilization (export capacity online).
2. Qatar Ras Laffan / North Field expansion commissioning and outage risk.
3. Australia NWS/Gorgon-class maintenance and weather disruption.
4. Europe storage fill vs Asia spot tenders (TTF vs JKM arb via ICE/EIA/GIE).
5. Canal/chokepoint diversion (Suez/Red Sea, Panama) adding voyage days and freight.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| QatarEnergy | Largest LNG exporter / Ras Laffan | QatarEnergy |
| Cheniere Sabine Pass LNG | US LNG export proxy | Cheniere Sabine Pass LNG |
| GECF | Gas exporters forum | GECF |
| IEA | Global gas/LNG outlook | IEA |
| EIA | US LNG export / Henry Hub context | EIA |
| Equinor | Atlantic LNG / Norway gas | Equinor |
| Petronas | SE Asia LNG (Bintulu) | Petronas |
| ICE | TTF / European gas pricing | ICE |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| QatarEnergy | qatarenergy.qa | North Field updates; Ras Laffan ops; offtake announcements | P1 |
| Cheniere Sabine Pass LNG | cheniere.com | Train utilization; shipping notices; feedgas commentary | P1 |
| EIA | eia.gov | Weekly natural gas; LNG export volumes; STEO gas | P1 |
| IEA | iea.org | Gas Market Report; winter/summer outlook | P1 |
| GECF | gecf.org | Producer statements; supply outlook | P2 |
| Equinor | equinor.com | Hammerfest / Norwegian LNG & pipeline gas availability | P1 |
| Petronas | petronas.com | Bintulu / Malaysia LNG cargo status | P2 |
| Ministry of Energy and Industry | mme.gov.qa | Qatar energy policy / project approvals | P2 |
| Gas Infrastructure Europe | gie.eu | EU storage fill (demand pull for cargoes) | P1 |
| ICE | ice.com | TTF settlements (arb vs Asia) | P2 |
| US DOE | energy.gov | LNG export authorizations | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Key liquefaction clusters: Ras Laffan (Qatar), USGC (Sabine Pass and peers), NW Australia, Yamal Arctic, Norway Hammerfest. Transit via Suez/Red Sea, Cape, Panama, and Malacca sets voyage time and freight. Regas demand hubs: NW Europe, NE Asia, SE Asia — see importer and terminal playbooks.

## Geopolitical triggers

- US DOE export-authorization or force-majeure-style terminal outage.
- Qatar project delay / force majeure at Ras Laffan.
- Red Sea / Suez diversion lengthening Qatar–Europe voyages.
- EU storage mandate or emergency demand destruction / fuel-switch policy.
- Sanctions affecting Russian Arctic LNG offtake or tankers (see energy_sanctions_compliance).

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| EIA natural gas weekly | weekly | Thu (US schedule) |
| GIE AGSI storage | daily | Business days (EU) |
| IEA Gas Market Report | quarterly / special updates | Per iea.org calendar |
| Cheniere / QatarEnergy releases | event-driven | Company IR / news pages |
| ICE TTF | continuous | Settlement end-of-day |

## Tier 2 context sources

GECF narrative reports; METI/JOGMEC importer stockpile context (Japan); Comtrade LNG bilateral lags. Useful for structural narrative, not same-day cargo risk.

## Anti-patterns

- Pricing off Twitter “cargo tracker” accounts without AIS + official confirmation.
- Treating all US export names as Cheniere — check whitelist entity coverage.
- Using oil MOMR as a substitute for LNG supply truth.
- Aggregator “LNG spot price” sites without exchange or offtaker confirmation.

## Related playbooks

- natural_gas_global.md
- qatar_ras_laffan_lng.md
- us_lng_gulf_terminals.md
- europe_gas_storage_ttf.md
- japan_korea_lng_demand.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft
