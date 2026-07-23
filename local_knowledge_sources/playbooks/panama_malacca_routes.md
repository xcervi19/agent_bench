# Panama and Malacca routes

**Commodity:** crude | LNG | products  
**Geography:** Panama Canal; Strait of Malacca / Singapore Strait  
**Last reviewed:** 2026-07-23  

## Executive summary

Panama draft/transit limits and Malacca/Singapore congestion jointly shape Atlantic–Pacific and Middle East–Asia voyage economics for products, LNG, and some crude. Scan must catch first: Panama Canal Authority draft/reservation notices, MPA Singapore and ReCAAP security/traffic signals, and Malaysian/Indonesian Malacca governance cues that change STS and transit risk.

## Price drivers (trader lens)

1. ACP draft restrictions and slot auctions (drought / lake levels) delaying USGC–Asia LNG and products.
2. Malacca/Singapore Strait congestion, pilotage, and bunker hub status (MPA).
3. Piracy / armed robbery / dark-fleet STS enforcement (ReCAAP, MMEA).
4. Freight and voyage-day shocks when Panama forces Cape Horn / Suez alternatives.
5. Singapore bunker price and availability as Asia hub cost signal.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Panama Canal Authority (ACP) | Canal draft / transit | Panama Canal Authority (ACP) |
| MPA Singapore | Singapore Strait / bunker hub | MPA Singapore |
| ReCAAP ISC (piracy) + MPA Singapore | Piracy / sea robbery info | ReCAAP ISC (piracy) + MPA Singapore |
| Maritime Enforcement Agency (MMEA) | Malacca enforcement | Maritime Enforcement Agency (MMEA) |
| Ministry of Foreign Affairs | Singapore diplomacy / Malacca | Ministry of Foreign Affairs (mfa.gov.sg) |
| Ministry of Foreign Affairs (Wisma Putra) | Malaysia / Malacca | Ministry of Foreign Affairs (Wisma Putra) |
| Ministry of Foreign Affairs | Indonesia / archipelago sea lanes | Ministry of Foreign Affairs (kemlu.go.id) |
| Republic of Singapore Navy | Strait security | Republic of Singapore Navy |
| IMO | Maritime regulation | IMO |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Panama Canal Authority (ACP) | pancanal.com | Draft limits, transit slots, advisories | P1 |
| MPA Singapore | mpa.gov.sg | Port/strait notices; bunker hub ops | P1 |
| ReCAAP ISC (piracy) + MPA Singapore | recaap.org | Incident reports; Malacca/Singapore risk | P1 |
| Maritime Enforcement Agency (MMEA) | mmea.gov.my | STS interdiction / Malacca enforcement | P2 |
| Ministry of Foreign Affairs | mfa.gov.sg | Malacca governance / sanctions compliance | P2 |
| Ministry of Foreign Affairs (Wisma Putra) | kln.gov.my | Malaysia Malacca / EEZ diplomacy | P2 |
| Ministry of Foreign Affairs | kemlu.go.id | Indonesia archipelagic sea lane policy | P2 |
| Republic of Singapore Navy | mindef.gov.sg | Strait patrol / security posture | P2 |
| IMO | imo.org | Routing and maritime security guidance | P3 |
| GISIS IMO | gisis.imo.org | Ship/flag screening for dark fleet | P3 |
| EMSA | emsa.europa.eu | EU maritime context (Tier 2) | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Panama connects USGC/Caribbean to Pacific Asia — critical for US LNG and clean products when draft allows. Malacca/Singapore is the primary Gulf–NE Asia crude/LNG choke; Lombok/Makassar are longer Indonesian alternatives. Singapore bunker complex clears a large share of marine fuel demand — see singapore_bunkering_hub.

## Geopolitical triggers

- ACP multi-week severe draft cut (drought).
- Major collision, blockage, or naval incident in Singapore/Malacca Strait.
- Coordinated dark-fleet crackdown altering STS patterns.
- South China Sea / Natuna EEZ flare affecting Indonesian routing rhetoric.
- Sudden Singapore bunker supply disruption.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| ACP advisories | event-driven + seasonal | Panama time |
| MPA notices | event-driven / ops | Singapore time |
| ReCAAP reports | periodic + incidents | As published |
| MMEA releases | event-driven | Malaysia time |

## Tier 2 context sources

MFA diplomatic framing from SG/MY/ID; IMO general guidance. Not a substitute for ACP draft tables or MPA notices.

## Anti-patterns

- Using only freight broker tweets for “Panama closed.”
- Conflating Malacca piracy stats with confirmed VLCC blockage.
- Ignoring draft feet/meters — “restricted” ≠ zero transit.
- Treating Kra Canal advocacy as near-term capacity.

## Related playbooks

- singapore_bunkering_hub.md
- us_lng_gulf_terminals.md
- cape_route_saldanha.md
- suez_canal_transit.md
- lng_global_supply.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
