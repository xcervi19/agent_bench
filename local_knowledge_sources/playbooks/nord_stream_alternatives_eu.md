# Nord Stream alternatives (EU)

**Commodity:** gas  
**Geography:** European Union — post-Nord Stream gas system  
**Last reviewed:** 2026-07-23  

## Executive summary

After Nord Stream losses, EU balances clear via LNG terminals, Norway pipes, Southern Corridor, residual east routes, and storage. Scan must catch first: gie.eu storage, entsog.eu flows, energy.ec.europa.eu policy, acer.europa.eu oversight, BMWK (DE), and ICE TTF.

## Price drivers (trader lens)

1. EU storage fill vs seasonal norms (GIE).
2. Norwegian and LNG send-out substituting lost Russian pipe.
3. ENTSOG cross-border congestion.
4. EU emergency/storage mandate policy.
5. Cold snaps vs industrial demand destruction.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Gas Infrastructure Europe | Storage AGSI | Gas Infrastructure Europe |
| ENTSOG | TSO transparency | ENTSOG |
| EU Energy | Policy / mandates | EU Energy |
| ACER | Regulatory oversight | ACER |
| Fed Ministry Economic Affairs & Climate (BMWK) | Germany policy | Fed Ministry Economic Affairs & Climate (BMWK) |
| ICE | TTF | ICE |
| Puertos del Estado | Spain LNG terminals | Puertos del Estado |
| Port of Antwerp-Bruges | Zeebrugge LNG | Port of Antwerp-Bruges |
| Naftogaz | Ukraine transit/UGS context | Naftogaz |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Gas Infrastructure Europe | gie.eu | Daily storage fill | P1 |
| ENTSOG | entsog.eu | Cross-border flows / maintenance | P1 |
| EU Energy | energy.ec.europa.eu | Storage mandates; emergency measures | P1 |
| ACER | acer.europa.eu | Market oversight / REMIT context | P2 |
| Fed Ministry Economic Affairs & Climate (BMWK) | bmwk.de | German gas/LNG policy | P1 |
| ICE | ice.com | TTF settlements | P1 |
| Eurostat (energy) | ec.europa.eu/eurostat | Lagged energy stats | P3 |
| Puertos del Estado | puertos.es | Spanish regas terminals | P2 |
| Port of Antwerp-Bruges | portofantwerpbruges.com | Zeebrugge LNG | P2 |
| Naftogaz | naftogaz.com | Transit ended notes; UGS context | P2 |
| EU Sanctions (Russian gas linkage) | ec.europa.eu | Residual Russian gas measures | P1 |
| IEA | iea.org | Europe gas outlook | P1 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Substitution stack: Norway pipes, US/Qatar/other LNG into NW Europe and Iberia, TANAP/TAP, residual TürkAkım/other, and large UGS. Nord Stream itself is not a live primary path — monitor alternatives and policy. See europe_gas_storage_ttf and tanap_tap_southern_corridor.

## Geopolitical triggers

- EU storage mandate change or emergency intervention.
- Norway or major LNG outage during low storage.
- Further sanctions on residual Russian gas.
- Ukraine infrastructure attacks affecting UGS/transit remnants.
- Iberian–French interconnection congestion limiting LNG redistribution.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| GIE AGSI | daily | Business days |
| ENTSOG | near-real-time | Continuous |
| ICE TTF | daily | Exchange close |
| EU Energy / BMWK | event-driven | EU time |

## Tier 2 context sources

Eurostat lags; IEA outlooks. GIE+ENTSOG+TTF are the live triad.

## Anti-patterns

- Obsessing over Nord Stream repair rumors vs live GIE/ENTSOG.
- Counting nameplate LNG regas as firm send-out.
- Ignoring storage seasonality.

## Related playbooks

- europe_gas_storage_ttf.md
- norway_hammerfest_lng.md
- us_lng_gulf_terminals.md
- tanap_tap_southern_corridor.md
- ukraine_energy_war.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
