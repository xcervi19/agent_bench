# Fujairah storage hub

**Commodity:** crude | products  
**Geography:** Fujairah, UAE — Gulf of Oman (outside Hormuz)  
**Last reviewed:** 2026-07-23  

## Executive summary

Fujairah is East-of-Suez’s key independent storage and bunker hub outside Hormuz; inventory and port status transmit Hormuz-risk and East-of-Suez product balances. Scan must catch first: fujairahport.ae, adports.ae, adnoc.ae, and UKMTO/Hormuz cues that drive precautionary stock builds.

## Price drivers (trader lens)

1. Fujairah crude/product inventory swings.
2. Port or tank-farm operational restrictions.
3. Hormuz escalation boosting outside-strait storage demand.
4. Bunker supply quality/availability at Fujairah.
5. ADNOC system barrels interacting with hub tanks.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Port of Fujairah | Port / storage hub | Port of Fujairah |
| AD Ports Group | Ports group | AD Ports Group |
| ADNOC | UAE NOC / grades | ADNOC |
| Ministry of Energy and Infrastructure | Policy | Ministry of Energy and Infrastructure |
| UKMTO (Maritime Trade Ops) | Gulf maritime risk | UKMTO (Maritime Trade Ops) |
| ICE Endex (Amsterdam) | Murban pricing context | ICE Endex (Amsterdam) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Port of Fujairah | fujairahport.ae | Port/storage/bunker status | P1 |
| AD Ports Group | adports.ae | Fujairah phase / UAE port ops | P1 |
| ADNOC | adnoc.ae | System barrels / Murban / ops | P1 |
| Ministry of Energy and Infrastructure | moei.gov.ae | Energy infra policy | P2 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Hormuz/Gulf incidents | P1 |
| Ministry of Foreign Affairs | mofa.gov.ae | Security diplomacy | P2 |
| ICE Endex (Amsterdam) | theice.com | Murban settlements | P2 |
| IMO | imo.org | Maritime guidance | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Located on the Gulf of Oman, Fujairah bypasses Hormuz for storage/bunkering and some export logistics. Large tank farms clear crude and refined products for East-of-Suez. Pair with uae_oil_fujairah and strait_of_hormuz.

## Geopolitical triggers

- Hormuz threat premium spike.
- Tank farm fire / port FM.
- Bunker contamination event.
- Regional war-risk insurance surge.
- ADNOC outage pushing more barrels into hub tanks or cutting them.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Fujairah Port / AD Ports | event-driven / ops | Gulf time |
| ADNOC | monthly OSP + event | Gulf time |
| UKMTO | event-driven | As issued |

## Tier 2 context sources

Unofficial weekly stock services are not whitelist primaries — prefer port/ADNOC confirmation. ICE Endex for price context only.

## Anti-patterns

- Anonymous Fujairah stock screenshots as primary.
- Assuming Fujairah stocks always mean Hormuz closed.
- Mixing Ruwais inside-Hormuz loadings with Fujairah hub tanks without label.

## Related playbooks

- uae_oil_fujairah.md
- strait_of_hormuz.md
- singapore_bunkering_hub.md
- oil_benchmarks_and_spreads.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
