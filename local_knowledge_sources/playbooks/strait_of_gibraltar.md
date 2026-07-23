# Strait of Gibraltar

**Commodity:** crude | LNG | products  
**Geography:** Strait of Gibraltar — Atlantic ↔ Mediterranean  
**Last reviewed:** 2026-07-23  

## Executive summary

Gibraltar gates Atlantic–Mediterranean energy flows and is a major bunkering/STS node; congestion, weather, or security restrictions reprice Med vs Atlantic differentials and bunker costs. Scan must catch first: Gibraltar Port Authority and HM Customs notices, Spanish Puertos del Estado / MFA energy-security context, and EMSA/IMO maritime safety signals affecting the strait lane.

## Price drivers (trader lens)

1. Port/bunker hub disruptions at Gibraltar altering STS and fueling programs.
2. Strait traffic restrictions or security incidents delaying Med-bound crude/LNG.
3. Weather (Atlantic storms / strong currents) stacking delays at the gate.
4. Spillover from Red Sea/Suez diversions increasing Atlantic–Med approach traffic.
5. Spanish LNG regas and Med refining pull interacting with strait arrivals.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Gibraltar Port Authority | Port / bunker hub ops | Gibraltar Port Authority |
| HM Customs Gibraltar | Customs / control | HM Customs Gibraltar |
| Puertos del Estado | Spanish ports / LNG terminals | Puertos del Estado |
| Ministry of Foreign Affairs | Spain diplomacy / energy relations | Ministry of Foreign Affairs (exteriores.gob.es) |
| EMSA | EU maritime safety | EMSA |
| IMO | Maritime regulation | IMO |
| Suez Canal Authority (SCA) | Upstream diversion driver | Suez Canal Authority (SCA) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Gibraltar Port Authority | gibraltarport.com | Port status, bunker hub ops, restrictions | P1 |
| Gibraltar Port Authority | gibport.com | Alternate official port domain / notices | P1 |
| HM Customs Gibraltar | customs.gi | Customs/control measures affecting calls | P1 |
| Puertos del Estado | puertos.es | Spanish port/LNG terminal status (Med demand side) | P2 |
| Ministry of Foreign Affairs | exteriores.gob.es | Spain energy diplomacy (e.g. Algeria/Medgas context) | P2 |
| EMSA | emsa.europa.eu | Maritime safety / tracking context | P2 |
| IMO | imo.org | Routing / security guidance | P3 |
| GISIS IMO | gisis.imo.org | Ship status screening | P3 |
| Suez Canal Authority (SCA) | suezcanal.gov.eg | Diversions that overload Atlantic–Med approaches | P2 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Broader maritime threat context | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Strait connects Atlantic to western Mediterranean; Gibraltar bunker hub ranks among top European marine-fuel nodes. Spanish Med LNG terminals (Puertos del Estado footprint) sit downstream of the gate. Traffic interacts with Suez/Cape diversion cycles and Algerian pipeline/LNG politics on the southern Med shore.

## Geopolitical triggers

- Port closure or bunker supply shock at Gibraltar.
- Security incident or enhanced customs controls on STS.
- Spain–Algeria diplomatic energy stress affecting Medgas / gas balances (MFA).
- Surge of Cape/Suez-diverted tonnage congesting the strait approaches.
- EU maritime emergency measures (EMSA-linked) altering traffic rules.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Gibraltar Port Authority | event-driven / ops | Local |
| HM Customs Gibraltar | event-driven | Local |
| Puertos del Estado | ops / periodic | Spain time |
| EMSA / IMO | ad hoc | As issued |

## Tier 2 context sources

Spanish MFA diplomatic background; IMO general pages. Primary scan remains port authority + customs.

## Anti-patterns

- Bunker price Twitter as proof of strait closure.
- Conflating Gibraltar political news with confirmed navigation restriction.
- Ignoring Spanish LNG terminal status when reading Med gas/LNG arb.
- Unverified STS “dark fleet” rumors without GISIS/IMO cross-check.

## Related playbooks

- suez_canal_transit.md
- cape_route_saldanha.md
- rotterdam_antwerp_hub.md
- europe_gas_storage_ttf.md
- ara_nwe_products_storage.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
