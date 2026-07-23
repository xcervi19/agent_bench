# Turkish Straits (Bosporus / Dardanelles)

**Commodity:** crude | products  
**Geography:** Türkiye — Bosporus and Dardanelles (Black Sea ↔ Mediterranean)  
**Last reviewed:** 2026-07-23  

## Executive summary

The Turkish Straits gate Russian, Kazakh, and other Black Sea crude/product exports to the Med. Fog, current, and administrative closures (Kıyı Emniyeti / VTS) create tanker queues that move Mediterranean differentials and Russian grade discounts. Scan must catch first: Kıyı Emniyeti and UAB VTS closure/delay notices, Turkish Customs transit signals, energy ministry/BOTAŞ Ceyhan context, and BTC as a Bosporus-bypass barrel path.

## Price drivers (trader lens)

1. Bosporus/Dardanelles transit delays and temporary closures (weather, traffic, security).
2. Black Sea loading programs (Russian / CPC-linked / other) waiting on strait slots.
3. War-risk and insurance around Black Sea approaches vs strait itself.
4. BTC–Ceyhan volumes as a partial bypass of RU+Bosporus (see btc_ceyhan_pipeline).
5. TRY/macro and Turkish refining pull (EPDK / Tupras context) affecting product flows.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Kıyı Emniyeti (fog/current closures) | Strait transit control | Kıyı Emniyeti (fog/current closures) |
| Turkish Straits VTS (UAB) | Vessel traffic service | Turkish Straits VTS (UAB) |
| Turkish Coast Guard | Strait security | Turkish Coast Guard |
| Turkish Customs | Transit cargo documentation | Turkish Customs |
| Ministry of Energy and Natural Resources | Energy / Ceyhan policy | Ministry of Energy and Natural Resources |
| Ceyhan tank storage | BTC / Med outlet | Ceyhan tank storage |
| BTC Co (BP-operated) | Bypass pipeline | BTC Co (BP-operated) |
| EPDK (Energy Market Regulator) | Market regulator | EPDK (Energy Market Regulator) |
| Turkish State Meteorological Service | Fog/storm forecasts | Turkish State Meteorological Service |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Kıyı Emniyeti (fog/current closures) | kiyiemniyeti.gov.tr | Closures, delays, transit rules | P1 |
| Turkish Straits VTS (UAB) | uab.gov.tr | VTS notices / traffic management | P1 |
| Turkish Coast Guard | sg.gov.tr | Security incidents affecting transit | P1 |
| Turkish Customs | gumruk.gov.tr | Transit cargo / Ceyhan re-export docs | P2 |
| Ministry of Energy and Natural Resources | enerji.gov.tr | Ceyhan / energy policy | P2 |
| Ceyhan tank storage | botas.gov.tr | BOTAŞ storage / grid / Ceyhan ops | P1 |
| BTC Co (BP-operated) | bp.com | BTC throughput / outage (Bosporus bypass) | P1 |
| EPDK (Energy Market Regulator) | epdk.gov.tr | Licensing / refining / market rules | P3 |
| Turkish State Meteorological Service | mgm.gov.tr | Fog and storm forecasts for closures | P2 |
| TPAO | tpao.gov.tr | Domestic upstream context | P3 |
| CBRT | tcmb.gov.tr | Macro/FX demand signal (Tier 2) | P3 |
| IMO | imo.org | Maritime transit guidance | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Bosporus and Dardanelles are narrow, one-way-regulated waterways; VLCC transit is constrained vs Suez-class economics. Black Sea load ports feed the queue; Ceyhan (BTC) and Turkish pipeline/gas grid (BOTAŞ) are parallel Med energy infrastructure. Sanctions/compliance on Russian barrels interact with strait logistics — see energy_sanctions_compliance and russia_oil_exports.

## Geopolitical triggers

- Multi-day fog/current closure stacking tanker days-to-clear.
- Security incident or Coast Guard restriction in the strait.
- Escalation in Black Sea shipping risk cutting loadings before the strait.
- BTC outage forcing more CPC/Black Sea barrels onto Bosporus path.
- Turkish regulatory change on hazardous cargo transit windows.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Kıyı Emniyeti / UAB VTS | event-driven / daily ops | Türkiye time |
| MGM weather | continuous / forecasts | Türkiye time |
| BOTAŞ / enerji.gov.tr | ops + policy releases | Event-driven |
| bp.com BTC updates | event-driven | As issued |

## Tier 2 context sources

CBRT macro pages; EPDK refining licensing background. Useful for demand/refining context, not same-day transit truth.

## Anti-patterns

- AIS queue screenshots without Kıyı Emniyeti confirmation of closure cause.
- Conflating Black Sea war-risk with an actual strait closure.
- Ignoring BTC as a bypass when reading “Bosporus bottleneck” narratives.
- Unofficial Telegram “strait closed” channels.

## Related playbooks

- russia_oil_exports.md
- kazakhstan_caspian_exports.md
- btc_ceyhan_pipeline.md
- energy_sanctions_compliance.md
- strait_of_gibraltar.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
