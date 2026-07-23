# Southeast Asia LNG imports

**Commodity:** LNG  
**Geography:** SE Asia — Singapore / Malaysia / Indonesia / Thailand / Vietnam  
**Last reviewed:** 2026-07-23  

## Executive summary

SE Asia is both LNG exporter (Malaysia) and growing importer; policy and terminal status across ESDM, Petronas, EMA/MPA Singapore, MOIT Vietnam, and Thai energy ministry set regional LNG balances. Scan must catch first: petronas.com, ema.gov.sg / mpa.gov.sg, esdm.go.id, energy.go.th, moit.gov.vn.

## Price drivers (trader lens)

1. Petronas Bintulu export availability vs domestic allocation.
2. Singapore LNG/gas market rules (EMA) and bunker/hub ops (MPA).
3. Indonesia policy shifting LNG between export and domestic.
4. Thailand/Vietnam FSRU/import ramp schedules.
5. Competition with NE Asia for spot cargoes.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Petronas | Malaysia NOC / Bintulu LNG | Petronas |
| EMA — Licensing | Singapore LNG/gas regulator | EMA — Licensing |
| MPA Singapore | Port / strait hub | MPA Singapore |
| Ministry of Energy & Mineral Res. (ESDM) | Indonesia | Ministry of Energy & Mineral Res. (ESDM) |
| Ministry of Energy | Thailand | Ministry of Energy (energy.go.th) |
| Ministry of Industry and Trade (MOIT) | Vietnam | Ministry of Industry and Trade (MOIT) |
| Ministry of Economy (energy division) | Malaysia policy | Ministry of Economy (energy division) |
| Singapore Customs | Trade docs | Singapore Customs |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Petronas | petronas.com | Bintulu LNG; domestic vs export | P1 |
| EMA — Licensing | ema.gov.sg | Singapore LNG/gas market regulation | P1 |
| MPA Singapore | mpa.gov.sg | Hub/strait ops | P1 |
| Singapore Customs | customs.gov.sg | LNG cargo documentation | P2 |
| Ministry of Energy & Mineral Res. (ESDM) | esdm.go.id | Indonesia energy/LNG policy | P1 |
| Ministry of Energy | energy.go.th | Thailand energy / LNG imports | P1 |
| Ministry of Industry and Trade (MOIT) | moit.gov.vn | Vietnam energy/LNG policy | P1 |
| Ministry of Foreign Affairs | mofa.gov.vn | Vietnam diplomacy | P3 |
| Ministry of Economy (energy division) | ekonomi.gov.my | Malaysia energy policy | P2 |
| IEA | iea.org | SE Asia gas outlook | P2 |
| ReCAAP ISC (piracy) + MPA Singapore | recaap.org | Malacca security | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Bintulu exports; Singapore as trading/bunker/LNG node; Indonesia’s Bontang/Tangguh complex (customs notes elsewhere); emerging FSRUs in Thailand/Vietnam. Malacca security and Singapore hub ops bind regional logistics. See singapore_bunkering_hub and panama_malacca_routes.

## Geopolitical triggers

- Petronas FM or domestic gas crisis cutting exports.
- Indonesia export curtailment for domestic power.
- Singapore market rule change (EMA).
- FSRU delay in Vietnam/Thailand.
- Malacca security spike.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Petronas / ministries | event-driven | Local |
| EMA / MPA | event / ops | Singapore time |
| IEA | outlook | As published |

## Tier 2 context sources

MFA pages; ReCAAP. Operator/ministry primaries dominate.

## Anti-patterns

- Treating SE Asia as only demand — Malaysia still exports.
- Ignoring domestic allocation fights in Indonesia/Malaysia.
- Unofficial FSRU WhatsApp updates as COD confirmation.

## Related playbooks

- singapore_bunkering_hub.md
- lng_global_supply.md
- japan_korea_lng_demand.md
- australia_lng_nws_gorgon.md
- panama_malacca_routes.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
