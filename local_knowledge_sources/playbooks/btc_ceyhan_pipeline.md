# BTC / Ceyhan pipeline

**Commodity:** crude | gas (TANAP adjacency)  
**Geography:** Baku–Tbilisi–Ceyhan — Ceyhan, Türkiye  
**Last reviewed:** 2026-07-23  

## Executive summary

BTC moves Caspian crude to Ceyhan on the Mediterranean, bypassing Russia, Hormuz, and the Bosporus for those barrels; outages reprice CPC vs BTC optionality. Scan must catch first: bp.com (BTC Co), caspianpipeline.com, botas.gov.tr Ceyhan storage, enerji.gov.tr, and Azeri SOCAR/customs context.

## Price drivers (trader lens)

1. BTC throughput cuts / FM (pipeline or Ceyhan terminal).
2. Azeri production (ACG) feeding BTC.
3. Ceyhan storage/offtake constraints (BOTAŞ).
4. CPC outages increasing BTC strategic value (and vice versa).
5. Eastern Med security affecting Ceyhan loadings.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| BTC Co (BP-operated) | Pipeline operator context | BTC Co (BP-operated) |
| BTC Pipeline (Caspian Pipeline) | BTC ops site | BTC Pipeline (Caspian Pipeline) |
| Ceyhan tank storage | Terminal / BOTAŞ | Ceyhan tank storage |
| Ministry of Energy and Natural Resources | Türkiye energy | Ministry of Energy and Natural Resources |
| SOCAR | Azerbaijan NOC | SOCAR |
| State Customs Committee | Azerbaijan customs | State Customs Committee (customs.gov.az) |
| Ministry of Energy | Azerbaijan | Ministry of Energy (minenergy.gov.az) |
| Turkish Customs | Ceyhan re-export docs | Turkish Customs |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| BTC Co (BP-operated) | bp.com | BTC throughput / outage notices | P1 |
| BTC Pipeline (Caspian Pipeline) | caspianpipeline.com | Pipeline ops updates | P1 |
| Ceyhan tank storage | botas.gov.tr | Ceyhan storage / Turkish grid adjacency | P1 |
| Ministry of Energy and Natural Resources | enerji.gov.tr | Ceyhan / energy policy | P1 |
| SOCAR | socar.az | ACG / Shah Deniz; BTC/TANAP governance | P1 |
| Ministry of Energy | minenergy.gov.az | Azerbaijan export policy | P1 |
| State Customs Committee | customs.gov.az | BTC export declarations / Sangachal | P2 |
| Turkish Customs | gumruk.gov.tr | Ceyhan crude re-export docs | P2 |
| Ministry of Foreign Affairs | mfa.gov.tr | Corridor diplomacy | P3 |
| Kıyı Emniyeti (fog/current closures) | kiyiemniyeti.gov.tr | Contrast path vs Bosporus | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

BTC runs Caspian crude to Ceyhan Med terminal, explicitly noted in whitelist as bypassing RU+Hormuz+Bospor. BOTAŞ Ceyhan also sits at TANAP western context — gas adjacency matters for corridor politics. See kazakhstan_caspian_exports and turkish_straits_bospor.

## Geopolitical triggers

- BTC pump station attack or prolonged FM.
- Azerbaijan–Armenia or regional security shock.
- Ceyhan terminal strike / storage incident.
- CPC multi-week outage elevating BTC nominations.
- Turkish regulatory/customs friction at Ceyhan.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| bp.com / caspianpipeline.com | event-driven | As issued |
| BOTAŞ / enerji.gov.tr | event-driven | Türkiye time |
| SOCAR / minenergy.gov.az | event-driven | Azerbaijan time |

## Tier 2 context sources

Turkish/Azeri MFA framing; customs declaration context. Operator + energy ministries are primary.

## Anti-patterns

- Assuming all Caspian barrels are BTC (many are CPC).
- Social “BTC bombed” claims without bp.com/caspianpipeline confirmation.
- Ignoring Ceyhan storage as a separate bottleneck from the pipe.

## Related playbooks

- kazakhstan_caspian_exports.md
- turkish_straits_bospor.md
- tanap_tap_southern_corridor.md
- russia_oil_exports.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
