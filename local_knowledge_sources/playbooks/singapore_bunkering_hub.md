# Singapore bunkering hub

**Commodity:** products  
**Geography:** Singapore — Malacca / Singapore Strait  
**Last reviewed:** 2026-07-23  

## Executive summary

Singapore is the world’s top bunker hub and a key Asia products/entrepôt node; MPA notices, customs, and strait security reprice marine fuel and regional product balances. Scan must catch first: mpa.gov.sg, customs.gov.sg, ema.gov.sg (LNG/gas market), ReCAAP incidents, and MFA sanctions-compliance framing.

## Price drivers (trader lens)

1. MPA bunker quality/ops incidents or supply disruptions.
2. Strait congestion or security events (ReCAAP / Navy).
3. Refinery runs on Jurong Island affecting product availability.
4. HSFO/VLSFO spreads and scrubber economics.
5. Sanctions enforcement on dark-fleet bunkering/STS.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| MPA Singapore | Port / bunker authority | MPA Singapore |
| Singapore Customs | Trade docs | Singapore Customs |
| EMA — Licensing | LNG/gas market regulator | EMA — Licensing |
| ReCAAP ISC (piracy) + MPA Singapore | Sea robbery / piracy | ReCAAP ISC (piracy) + MPA Singapore |
| Republic of Singapore Navy | Strait security | Republic of Singapore Navy |
| Ministry of Foreign Affairs | Sanctions / Malacca diplomacy | Ministry of Foreign Affairs (mfa.gov.sg) |
| NEA (National Environment Agency) | Industrial/env compliance | NEA (National Environment Agency) |
| SGX | Freight/fuel derivatives | SGX |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| MPA Singapore | mpa.gov.sg | Bunker hub ops; port/strait notices | P1 |
| Singapore Customs | customs.gov.sg | Entrepôt crude/product/LNG docs | P2 |
| EMA — Licensing | ema.gov.sg | Singapore LNG/gas market rules | P2 |
| ReCAAP ISC (piracy) + MPA Singapore | recaap.org | Incidents near Malacca/Singapore | P1 |
| Republic of Singapore Navy | mindef.gov.sg | Strait security posture | P2 |
| Ministry of Foreign Affairs | mfa.gov.sg | Sanctions compliance; Malacca governance | P2 |
| NEA (National Environment Agency) | nea.gov.sg | Jurong Island env/ops constraints | P3 |
| SGX | sgx.com | Freight/fuel derivatives context | P3 |
| IMO | imo.org | Bunker/sulphur regulations | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Bunker stems clear a huge share of global marine fuel demand; Singapore Strait is a narrow VLCC bottleneck. Entrepôt refining/trading links Middle East crude and Asia products. See panama_malacca_routes.

## Geopolitical triggers

- MPA bunker contamination / supply crisis.
- Major collision or security incident in the strait.
- Sanctions crackdown on STS bunkering.
- Refinery outage on Jurong Island.
- Malacca governance diplomatic flare (SG/MY/ID).

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| MPA notices | event-driven / ops | Singapore time |
| ReCAAP | periodic + incidents | As published |
| Customs / EMA | event / periodic | Local |

## Tier 2 context sources

SGX derivatives; NEA compliance. MPA remains bunker primary.

## Anti-patterns

- Bunker price Twitter as proof of hub outage.
- Ignoring ReCAAP when fixtures avoid the strait.
- Treating Singapore only as LNG — miss bunker product risk.

## Related playbooks

- panama_malacca_routes.md
- fujairah_storage_hub.md
- southeast_asia_lng_imports.md
- oil_benchmarks_and_spreads.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
