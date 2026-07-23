# ARA / NWE products storage

**Commodity:** products  
**Geography:** Amsterdam–Rotterdam–Antwerp — Northwest Europe  
**Last reviewed:** 2026-07-23  

## Executive summary

ARA is Europe’s products pricing and storage hinge; barge/terminal status and Dutch/Belgian port ops move gasoline/diesel/jet differentials. Scan must catch first: portofrotterdam.com, portofantwerpbruges.com, portofamsterdam.com, Dutch Customs (douane.nl), KNMI weather, and ICE product-related settlements where relevant.

## Price drivers (trader lens)

1. ARA independent storage builds/draws (gasoline/diesel/jet).
2. Rhine/barge logistics and weather constraints.
3. Refinery runs / turnarounds in NWE feeding ARA.
4. Export arb to US Atlantic / West Africa / Med.
5. Port congestion or terminal force majeure.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Port of Rotterdam Authority | Core ARA oil port | Port of Rotterdam Authority |
| Port of Antwerp-Bruges | ARA petchem / products | Port of Antwerp-Bruges |
| ARA tank / product terminals | Amsterdam terminals | ARA tank / product terminals |
| Dutch Customs | Import/export docs | Dutch Customs |
| KNMI | Weather | KNMI |
| Ministry of Climate & Green Growth | NL energy policy | Ministry of Climate & Green Growth |
| ICE | European energy contracts | ICE |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Port of Rotterdam Authority | portofrotterdam.com | Port status; oil hub ops | P1 |
| Port of Antwerp-Bruges | portofantwerpbruges.com | Port/terminal status; Zeebrugge LNG adjacency | P1 |
| ARA tank / product terminals | portofamsterdam.com | Amsterdam tank/product terminal status | P1 |
| Dutch Customs | douane.nl | ARA crude/product documentation signals | P2 |
| KNMI | knmi.nl | ARA/North Sea weather; barge/port impact | P2 |
| Ministry of Climate & Green Growth | rijksoverheid.nl | NL energy/LNG policy overlays | P3 |
| ICE | ice.com | European settlements context | P2 |
| EMSA | emsa.europa.eu | EU maritime safety | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

ARA tank farms and barge network clear NWE products; Rotterdam is the largest EU oil port. Antwerp adds petchem/products depth; Amsterdam terminals complete the triangle. Weather and Rhine water levels historically bind barge flows.

## Geopolitical triggers

- Major terminal fire / FM in ARA.
- Rhine extreme low/high water cutting barge supply.
- EU products sanctions enforcement changing export flows.
- Strike action at Dutch/Belgian ports.
- Refinery outage cluster in NWE.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Port authority notices | event-driven / ops | Local |
| KNMI | continuous | NL time |
| Dutch Customs | periodic / event | Local |
| ICE | daily | Exchange close |

## Tier 2 context sources

Rijksoverheid policy pages; EMSA. Port authorities remain primary for ops.

## Anti-patterns

- Unofficial ARA stock WhatsApp sheets as sole truth.
- Ignoring barge constraints when reading flat-price strength.
- Conflating TTF gas storage with products tanks.

## Related playbooks

- rotterdam_antwerp_hub.md
- north_sea_crude.md
- europe_gas_storage_ttf.md
- oil_benchmarks_and_spreads.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
