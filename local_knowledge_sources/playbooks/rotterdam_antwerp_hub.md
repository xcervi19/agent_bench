# Rotterdam / Antwerp hub

**Commodity:** crude | products | LNG  
**Geography:** Port of Rotterdam; Port of Antwerp-Bruges  
**Last reviewed:** 2026-07-23  

## Executive summary

Rotterdam and Antwerp form the core NW Europe energy gateway for crude, products, and adjacent LNG (Gate / Zeebrugge). Scan must catch first: both port authorities’ ops notices, Dutch Customs, rijksoverheid.nl energy/LNG policy, and weather (KNMI) affecting port callability.

## Price drivers (trader lens)

1. Crude discharge/load disruptions at Rotterdam.
2. Antwerp petchem/products logistics shocks.
3. Gate/Zeebrugge LNG adjacency pulling or pushing hub balances.
4. Congestion, strikes, or draft/weather limits.
5. EU sanctions/compliance checks slowing Russian-origin residual flows.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Port of Rotterdam Authority | Largest EU oil port | Port of Rotterdam Authority |
| Port of Antwerp-Bruges | ARA petchem; Zeebrugge LNG | Port of Antwerp-Bruges |
| Dutch Customs | Trade documentation | Dutch Customs |
| Ministry of Climate & Green Growth | NL energy/LNG policy | Ministry of Climate & Green Growth |
| KNMI | Weather | KNMI |
| Gas Infrastructure Europe | EU gas storage context | Gas Infrastructure Europe |
| ICE | TTF / energy contracts | ICE |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Port of Rotterdam Authority | portofrotterdam.com | Crude/products hub status; Gate LNG notes | P1 |
| Port of Antwerp-Bruges | portofantwerpbruges.com | Port ops; Zeebrugge LNG | P1 |
| Dutch Customs | douane.nl | Import/export declarations context | P2 |
| Ministry of Climate & Green Growth | rijksoverheid.nl | Groningen closure / LNG diversification / Gate | P2 |
| KNMI | knmi.nl | Port weather | P2 |
| Gas Infrastructure Europe | gie.eu | Storage fill (gas side of hub) | P2 |
| ICE | ice.com | TTF settlements | P2 |
| EMSA | emsa.europa.eu | Maritime safety | P3 |
| EU Energy | energy.ec.europa.eu | EU policy overlays | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Rotterdam handles deepsea crude and products with Gate LNG nearby; Antwerp-Bruges adds petchem and Zeebrugge LNG. Together they define ARA hub optionality. Pair with ara_nwe_products_storage and europe_gas_storage_ttf.

## Geopolitical triggers

- Port-wide strike or cyber/ops outage.
- EU enforcement action concentrating inspections at NL/BE ports.
- LNG terminal trip at Gate/Zeebrugge during tight TTF.
- Extreme North Sea storm closing berths.
- Major refinery fire inland feeding the hub.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Port notices | event-driven | Local |
| GIE storage | daily | Business days |
| ICE TTF | daily | Exchange close |
| KNMI | continuous | Local |

## Tier 2 context sources

EU Energy policy pages; EMSA. Ports are the ops primary.

## Anti-patterns

- AIS berth counts without port authority confirmation of restriction.
- Treating Antwerp and Rotterdam as interchangeable for every grade.
- Gas storage tweets as crude hub truth.

## Related playbooks

- ara_nwe_products_storage.md
- europe_gas_storage_ttf.md
- north_sea_crude.md
- nord_stream_alternatives_eu.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
