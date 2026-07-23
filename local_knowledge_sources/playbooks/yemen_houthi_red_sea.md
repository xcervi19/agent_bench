# Yemen / Houthi Red Sea

**Commodity:** crude | LNG | products  
**Geography:** Yemen conflict — Red Sea / Bab el-Mandeb approaches  
**Last reviewed:** 2026-07-23  

## Executive summary

Houthi-linked attacks and the wider Yemen conflict drive Red Sea avoidance, Suez under-utilisation, and Cape diversions for energy shipping. Scan must catch first: ukmto.org incidents, suezcanal.gov.eg knock-on transit, royalnavy.mod.uk ops, and mfa.gov.eg security diplomacy — without inventing Yemeni ministry domains not on the whitelist.

## Price drivers (trader lens)

1. Confirmed attacks on tankers/boxships (UKMTO).
2. Carrier/tanker Red Sea avoidance extending voyage times.
3. SCA transit collapse as southern approaches empty.
4. War-risk insurance spikes.
5. Escalation involving shore targets or wider coalition strikes.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| UKMTO (Maritime Trade Ops) | Incident advisories | UKMTO (Maritime Trade Ops) |
| Suez Canal Authority (SCA) | Canal transit impact | Suez Canal Authority (SCA) |
| Royal Navy | Naval ops | Royal Navy |
| Ministry of Foreign Affairs | Egypt Red Sea/Suez diplomacy | Ministry of Foreign Affairs (mfa.gov.eg) |
| IMO | Maritime security guidance | IMO |
| EMSA | EU maritime safety | EMSA |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| UKMTO (Maritime Trade Ops) | ukmto.org | Attacks, warnings, GPS interference | P1 |
| Suez Canal Authority (SCA) | suezcanal.gov.eg | Transit stats / disruption notices | P1 |
| Royal Navy | royalnavy.mod.uk | Escort / strike ops affecting risk | P1 |
| Ministry of Foreign Affairs | mfa.gov.eg | Egypt Red Sea / Suez security statements | P1 |
| IMO | imo.org | Maritime security guidance | P2 |
| GISIS IMO | gisis.imo.org | Ship status screening | P2 |
| EMSA | emsa.europa.eu | EU maritime context | P3 |
| Saudi Ports Authority (Mawani) | mawani.gov.sa | Yanbu / Red Sea Saudi port impact | P2 |
| Ministry of Foreign Affairs | mofa.gov.sa | Saudi Red Sea diplomacy | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated. Do not invent Houthi media handles. |

## Infrastructure & logistics

Conflict risk concentrates at Bab el-Mandeb and southern Red Sea lanes feeding Suez. Diversion path is Cape of Good Hope. Whitelist lacks dedicated Yemen energy-ministry domains — do not fabricate; rely on maritime/coalition/Egyptian/Saudi primaries.

## Geopolitical triggers

- Mass-casualty or tanker-sinking event confirmed by UKMTO.
- Coalition escalation changing rules of engagement.
- SCA formal advisory altering transit.
- Ceasefire that restores liner/tanker confidence (confirm via UKMTO + SCA stats).
- Spillover into Hormuz rhetoric (cross-check strait_of_hormuz).

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| UKMTO | event-driven | As issued |
| SCA | periodic + event | Cairo time |
| Royal Navy / MFA | event-driven | As issued |

## Tier 2 context sources

IMO/EMSA background. Conflict political detail from non-whitelist activist media is not a primary scan anchor.

## Anti-patterns

- Unverified Telegram attack videos as sole confirmation.
- Inventing Yemeni .gov domains not in source_whitelist.json.
- Double-counting Cape freight and imaginary lost Suez barrels.

## Related playbooks

- red_sea_bab_el_mandeb.md
- suez_canal_transit.md
- cape_route_saldanha.md
- lng_global_supply.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic; no Yemen ministry domains on whitelist
