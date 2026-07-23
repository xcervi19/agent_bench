# TANAP / TAP Southern Corridor

**Commodity:** gas  
**Geography:** Azerbaijan — Türkiye (TANAP) — Europe (TAP)  
**Last reviewed:** 2026-07-23  

## Executive summary

The Southern Gas Corridor (TANAP/TAP) diversifies EU gas away from Russian routes via Shah Deniz volumes. Scan must catch first: tanap.com, socar.az, enerji.gov.tr / botas.gov.tr, minenergy.gov.az, and Italian customs metering notes (adm.gov.it) for TAP arrivals.

## Price drivers (trader lens)

1. Shah Deniz / SOCAR upstream or corridor outages.
2. TANAP throughput restrictions in Türkiye.
3. TAP delivery interruptions into Italy/Europe.
4. EU demand/storage competing with corridor nominations.
5. Geopolitical stress on Caucasus transit.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| TANAP (Trans-Anatolian Pipeline) | Türkiye segment | TANAP (Trans-Anatolian Pipeline) |
| SOCAR | Azerbaijan NOC | SOCAR |
| Ministry of Energy | Azerbaijan | Ministry of Energy (minenergy.gov.az) |
| Ministry of Energy and Natural Resources | Türkiye | Ministry of Energy and Natural Resources |
| Ceyhan tank storage | BOTAŞ / corridor adjacency | Ceyhan tank storage |
| Agenzia delle Dogane | TAP import metering (IT) | Agenzia delle Dogane |
| ENTSOG | EU flow transparency | ENTSOG |
| Gas Infrastructure Europe | Storage | Gas Infrastructure Europe |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| TANAP (Trans-Anatolian Pipeline) | tanap.com | Throughput / ops notices | P1 |
| SOCAR | socar.az | Shah Deniz; BTC/TANAP governance | P1 |
| Ministry of Energy | minenergy.gov.az | Export policy | P1 |
| Ministry of Energy and Natural Resources | enerji.gov.tr | TürkAkım/TANAP/Ceyhan policy | P1 |
| Ceyhan tank storage | botas.gov.tr | BOTAŞ grid / terminus context | P1 |
| State Customs Committee | customs.gov.az | Corridor export declarations | P2 |
| Agenzia delle Dogane | adm.gov.it | TAP gas import metering | P1 |
| ENTSOG | entsog.eu | Cross-border flows | P1 |
| Gas Infrastructure Europe | gie.eu | EU storage | P2 |
| ICE | ice.com | TTF settlements | P2 |
| EU Energy | energy.ec.europa.eu | Corridor policy support | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Gas from Azerbaijan crosses Türkiye on TANAP and continues via TAP into SE Europe/Italy. BOTAŞ systems and Ceyhan energy complex are adjacent infrastructure. Complements nord_stream_alternatives_eu as a diversification path.

## Geopolitical triggers

- Caucasus security shock cutting Shah Deniz.
- TANAP/TAP FM or force reduction.
- Türkiye–EU energy politics altering nominations.
- Italian entry-point constraint (customs/metering alerts).
- Competing Russian route politics (TürkAkım) crowding policy attention.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| TANAP / SOCAR / ministries | event-driven | Local |
| ENTSOG / GIE | near-real-time / daily | EU |
| adm.gov.it | periodic / event | Italy time |

## Tier 2 context sources

Borsa Italiana energy listings (SNAM mention) — financial Tier 2 only. Corridor operators/ministries are primary.

## Anti-patterns

- Treating TANAP volumes as fungible with LNG cargoes same-day.
- Ignoring Italian entry data when blaming only Azerbaijan upstream.
- Unofficial “corridor cut” Telegram channels.

## Related playbooks

- nord_stream_alternatives_eu.md
- europe_gas_storage_ttf.md
- btc_ceyhan_pipeline.md
- natural_gas_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
