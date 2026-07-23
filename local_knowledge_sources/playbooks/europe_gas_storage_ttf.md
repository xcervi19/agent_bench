# Europe gas storage / TTF

**Commodity:** gas  
**Geography:** European Union / NW Europe TTF  
**Last reviewed:** 2026-07-23  

## Executive summary

TTF is the European gas benchmark; storage fill (GIE) and ENTSOG flows are the physical anchors under EU policy. Scan must catch first: gie.eu, entsog.eu, ice.com TTF, energy.ec.europa.eu, and BMWK/ACER for policy/oversight.

## Price drivers (trader lens)

1. Daily storage trajectory vs seasonal norms.
2. Norwegian/LNG send-out vs demand.
3. ENTSOG maintenance and congestion.
4. EU storage mandate / emergency measures.
5. Weather-driven heating demand (Met Office / KNMI context).

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Gas Infrastructure Europe | AGSI storage | Gas Infrastructure Europe |
| ENTSOG | Flows | ENTSOG |
| ICE | TTF contracts | ICE |
| EU Energy | Policy | EU Energy |
| ACER | Oversight | ACER |
| Fed Ministry Economic Affairs & Climate (BMWK) | Germany | Fed Ministry Economic Affairs & Climate (BMWK) |
| UK Met Office | NW Europe weather | UK Met Office |
| KNMI | NL weather | KNMI |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Gas Infrastructure Europe | gie.eu | Daily EU storage fill | P1 |
| ENTSOG | entsog.eu | Cross-border flows / outages | P1 |
| ICE | ice.com | TTF settlements | P1 |
| EU Energy | energy.ec.europa.eu | Storage mandates; crisis measures | P1 |
| ACER | acer.europa.eu | Market integrity / REMIT context | P2 |
| Fed Ministry Economic Affairs & Climate (BMWK) | bmwk.de | German gas/LNG policy | P1 |
| Eurostat (energy) | ec.europa.eu/eurostat | Lagged stats | P3 |
| UK Met Office | metoffice.gov.uk | Demand weather | P2 |
| KNMI | knmi.nl | ARA weather | P2 |
| IEA | iea.org | Europe gas outlook | P1 |
| Equinor | equinor.com | Norway supply shocks | P1 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

UGS sites across EU, LNG regas (Gate/Zeebrugge/Iberia/Germany), and Norway pipes clear the post-Nord Stream system. TTF futures settle physical expectations. See nord_stream_alternatives_eu and norway_hammerfest_lng.

## Geopolitical triggers

- Storage mandate tightening mid-season.
- Norway or major LNG outage at low storage.
- Cold extreme with storage below 5-year band.
- Further Russian residual gas measures.
- Ukraine UGS/infrastructure attacks (Naftogaz context).

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| GIE AGSI | daily | Business days |
| ENTSOG | near-real-time | Continuous |
| ICE TTF | daily | Exchange close |
| EU/BMWK | event-driven | EU time |

## Tier 2 context sources

Eurostat; IEA outlooks. Live triad = GIE + ENTSOG + ICE.

## Anti-patterns

- Absolute % full without seasonal curve context.
- Social “TTF leak” channels.
- Counting regas nameplate as firm send-out.

## Related playbooks

- nord_stream_alternatives_eu.md
- norway_hammerfest_lng.md
- us_lng_gulf_terminals.md
- natural_gas_global.md
- ukraine_energy_war.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
