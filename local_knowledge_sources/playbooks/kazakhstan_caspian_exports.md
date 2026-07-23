# Kazakhstan Caspian exports

**Commodity:** crude  
**Geography:** Kazakhstan — CPC / Caspian — Black Sea / BTC optionality  
**Last reviewed:** 2026-07-23  

## Executive summary

Kazakh crude mainly reaches markets via CPC to the Black Sea and alternative Caspian–BTC paths; outages, weather, and Russia-transit geopolitics move CPC blend differentials. Scan must catch first: energo.gov.kz and KazMunayGas, cpc.ru operational status, Turkish Straits delays, and BTC/Ceyhan as bypass context.

## Price drivers (trader lens)

1. CPC pipeline/terminal outages or force majeure.
2. Black Sea loading interruptions and Bosporus queues.
3. Kazakh production policy / KMG guidance.
4. BTC volumes as partial bypass of CPC/RU exposure.
5. Sanctions/compliance friction on transit and shipping.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Ministry of Energy | Kazakhstan policy | Ministry of Energy (energo.gov.kz) |
| KazMunayGas (KMG) | NOC | KazMunayGas (KMG) |
| Caspian Pipeline Consortium (CPC) | Main export pipeline | Caspian Pipeline Consortium (CPC) |
| Ministry of Foreign Affairs | Diplomacy | Ministry of Foreign Affairs (mfa.gov.kz) |
| State Revenue Committee (Customs) | Customs | State Revenue Committee (Customs) |
| BTC Co (BP-operated) | Bypass pipeline | BTC Co (BP-operated) |
| Ceyhan tank storage | Med outlet | Ceyhan tank storage |
| Kıyı Emniyeti (fog/current closures) | Bosporus transit | Kıyı Emniyeti (fog/current closures) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Ministry of Energy | energo.gov.kz | Production / export policy | P1 |
| KazMunayGas (KMG) | kmg.kz | Output; marketing; FM | P1 |
| Caspian Pipeline Consortium (CPC) | cpc.ru | Pipeline/terminal status; FM | P1 |
| Ministry of Foreign Affairs | mfa.gov.kz | Transit diplomacy | P2 |
| State Revenue Committee (Customs) | kgd.gov.kz | Export documentation signals | P3 |
| BTC Co (BP-operated) | bp.com | BTC throughput (bypass) | P1 |
| BTC Pipeline (Caspian Pipeline) | caspianpipeline.com | BTC ops context | P2 |
| Ceyhan tank storage | botas.gov.tr | Ceyhan storage / offtake | P2 |
| Kıyı Emniyeti (fog/current closures) | kiyiemniyeti.gov.tr | Bosporus delays for CPC barrels | P1 |
| SOCAR | socar.az | Azerbaijan corridor context | P3 |
| OFAC (Treasury) | treasury.gov | Sanctions affecting transit/shipping | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

CPC to Novorossiysk-area Black Sea loadings is the dominant path; storms and maintenance historically cut CPC. BTC to Ceyhan diversifies away from Russian Black Sea/Bosporus for some Caspian barrels. See turkish_straits_bospor and btc_ceyhan_pipeline.

## Geopolitical triggers

- CPC FM or prolonged Black Sea terminal outage.
- Storm damage / repair timelines on CPC.
- Transit-fee or political dispute with Russia.
- Bosporus multi-day closure stacking CPC cargoes.
- Sanctions enforcement complicating CPC shipping.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| CPC / KMG / energo.gov.kz | event-driven | Local |
| Kıyı Emniyeti | event-driven / daily ops | Türkiye time |
| bp.com BTC | event-driven | As issued |

## Tier 2 context sources

SOCAR/Azerbaijan corridor context; customs. CPC + ministry remain primary.

## Anti-patterns

- Blaming “Kazakh outage” for what is a Bosporus queue.
- Ignoring BTC bypass when CPC is down.
- Unofficial CPC throughput Telegram trackers as sole source.

## Related playbooks

- turkish_straits_bospor.md
- btc_ceyhan_pipeline.md
- russia_oil_exports.md
- energy_sanctions_compliance.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
