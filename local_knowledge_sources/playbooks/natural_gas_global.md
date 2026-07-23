# Natural gas — global

**Commodity:** gas  
**Geography:** global  
**Last reviewed:** 2026-07-23  

## Executive summary

Pipeline gas and LNG jointly clear regional balances; Europe TTF and US Henry Hub are the tradable anchors, with Asia priced off LNG spot/term. Scan must catch first: EIA US gas fundamentals, ENTSOG/GIE European flows and storage, ICE TTF, IEA/GECF supply commentary, and any disruption to Norwegian, Russian residual, or US LNG-linked feedgas.

## Price drivers (trader lens)

1. US production, storage, and power burn (EIA) → Henry Hub and LNG feedgas.
2. EU storage trajectory and TSO flows (GIE, ENTSOG) → TTF.
3. Norwegian / Equinor availability vs residual Russian pipeline policy.
4. Weather-driven demand (NW Europe, NE Asia, US).
5. LNG cargo arb swinging molecules between basins (see lng_global_supply).

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| EIA | US gas weekly / STEO | EIA |
| ENTSOG | EU gas TSO transparency | ENTSOG |
| Gas Infrastructure Europe | EU storage AGSI | Gas Infrastructure Europe |
| ICE | TTF / European gas contracts | ICE |
| CME Group | Henry Hub futures | CME Group |
| IEA | Global gas balances | IEA |
| GECF | Exporter forum | GECF |
| Equinor | Norway supply | Equinor |
| ACER | EU regulatory / market integrity | ACER |
| EU Energy | Policy / storage mandates | EU Energy |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| EIA | eia.gov | Weekly natural gas storage; production; steo | P1 |
| Gas Infrastructure Europe | gie.eu | Daily EU storage fill by site/country | P1 |
| ENTSOG | entsog.eu | Cross-border flow transparency; maintenance | P1 |
| ICE | ice.com | TTF settlements and contract specs | P1 |
| CME Group | cmegroup.com | Henry Hub settlements | P1 |
| IEA | iea.org | Gas Market Report; winter risk | P1 |
| Equinor | equinor.com | Field / export availability notices | P1 |
| GECF | gecf.org | Producer supply narrative | P2 |
| ACER | acer.europa.eu | REMIT / market oversight signals | P2 |
| EU Energy | energy.ec.europa.eu | Storage mandates; emergency measures | P1 |
| Eurostat (energy) | ec.europa.eu/eurostat | EU energy statistics (lagged) | P3 |
| UK Met Office | metoffice.gov.uk | NW Europe demand weather | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Major pipeline corridors: Norway–NW Europe, residual Russia–Europe routes, Southern Corridor (TANAP/TAP), Central Asia–China. LNG bridges basins when pipeline is constrained. Storage: EU AGSI sites, US lower-48 inventories. See hub and corridor playbooks for TTF, Nord Stream alternatives, and Southern Corridor detail.

## Geopolitical triggers

- Norwegian outage or Equinor force majeure.
- Further EU measures on residual Russian gas / transit.
- Cold/heat extremes vs storage below seasonal norms.
- US freeze-offs or hurricane outages hitting production and LNG feedgas.
- Ukraine transit / infrastructure attacks affecting CEE flows.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| EIA weekly gas storage | weekly | Thu ~15:30 US-linked |
| GIE AGSI | daily | Business days |
| ENTSOG transparency | near-real-time / daily | Continuous |
| ICE TTF settlement | daily | Exchange close |
| IEA gas publications | quarterly / ad hoc | iea.org calendar |

## Tier 2 context sources

Eurostat lagged energy stats; GECF annual outlooks; national meteorology beyond Met Office for regional demand. Not for intraday TTF risk.

## Anti-patterns

- Using oil inventory prints as gas balance proxies.
- Unofficial “TTF leak” Telegram channels.
- Ignoring storage seasonality (absolute % full without YoY/curve context).
- Treating all Russian gas as zero without checking residual pipeline / LNG pathways still in whitelist scope.

## Related playbooks

- lng_global_supply.md
- europe_gas_storage_ttf.md
- nord_stream_alternatives_eu.md
- us_lng_gulf_terminals.md
- norway_hammerfest_lng.md

## Changelog

- 2026-07-23 — initial draft
