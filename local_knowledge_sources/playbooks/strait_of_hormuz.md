# Strait of Hormuz

**Commodity:** crude | LNG | products  
**Geography:** Persian Gulf — Strait of Hormuz  
**Last reviewed:** 2026-07-23  

## Executive summary

Hormuz is the primary chokepoint for Gulf crude and Qatar LNG; closure risk or harassment immediately reprices Brent and freight. Scan must catch first: UKMTO incident notices, Iranian MFA/ministry and NIOC/PMO port signals, Saudi/UAE naval and port authorities, and Fujairah/outside-Hormuz logistics (Duqm, Fujairah) that show rerouting.

## Price drivers (trader lens)

1. Transit incidents, seizures, or GPS interference reports (UKMTO).
2. Iranian export policy / Kharg loadings under sanctions (NIOC, PMO, mop.ir).
3. Saudi Ras Tanura / UAE loadings continuity (Mawani, ADNOC, AD Ports).
4. War-risk premiums and convoy/escort posture (Royal Navy, regional navies).
5. Fujairah storage and Oman Duqm as bypass / staging signals.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| UKMTO (Maritime Trade Ops) | Incident / advisory hub | UKMTO (Maritime Trade Ops) |
| NIOC | Iran producer / Kharg | NIOC |
| PMO maritime traffic | Iran ports throughput | PMO maritime traffic |
| Ministry of Petroleum | Iran policy (SHANA channel) | Ministry of Petroleum |
| NIOC (via SHANA) | Fast official news | NIOC (via SHANA) |
| Ministry of Foreign Affairs | Iran diplomacy | Ministry of Foreign Affairs (mfa.gov.ir) |
| Saudi Ports Authority (Mawani) | Saudi loadings | Saudi Ports Authority (Mawani) |
| Royal Saudi Navy | Gulf security | Royal Saudi Navy |
| ADNOC | UAE barrels / Fujairah link | ADNOC |
| AD Ports Group | UAE ports / Fujairah | AD Ports Group |
| Port of Fujairah | Outside-strait hub | Port of Fujairah |
| ASYAD Group | Oman ports (Duqm outside Hormuz) | ASYAD Group |
| QatarEnergy | LNG via Hormuz | QatarEnergy |
| Indian Navy | Escort / Arabian Sea | Indian Navy |
| Royal Navy | Kipion / escort ops | Royal Navy |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| UKMTO (Maritime Trade Ops) | ukmto.org | Incidents, warnings, GPS jamming notes | P1 |
| NIOC | nioc.ir | Export / Kharg strategy under stress | P1 |
| PMO maritime traffic | pmo.ir | Bandar Abbas / Kharg / Assaluyeh traffic | P1 |
| Ministry of Petroleum | mop.ir | Policy statements; SHANA-linked releases | P1 |
| NIOC (via SHANA) | shana.ir | Faster official ministry/NOC news | P1 |
| Ministry of Foreign Affairs | mfa.gov.ir | Escalation / de-escalation diplomacy | P1 |
| Saudi Ports Authority (Mawani) | mawani.gov.sa | Ras Tanura / Jubail / Yanbu throughput | P1 |
| Royal Saudi Navy | mod.gov.sa | Naval posture statements | P2 |
| Ministry of Foreign Affairs | mofa.gov.sa | Regional security statements | P2 |
| ADNOC | adnoc.ae | UAE production / export continuity | P1 |
| AD Ports Group | adports.ae | Fujairah / UAE port ops | P1 |
| Port of Fujairah | fujairahport.ae | Storage / bunker / diversion hub | P1 |
| Ministry of Energy and Infrastructure | moei.gov.ae | UAE energy / infra policy | P2 |
| Ministry of Foreign Affairs | mofa.gov.ae | UAE diplomacy | P2 |
| ASYAD Group | asyad.om | Sohar / Duqm / Salalah (Duqm outside Hormuz) | P2 |
| Ministry of Foreign Affairs | mofa.gov.om | Oman mediation / maritime diplomacy | P2 |
| QatarEnergy | qatarenergy.qa | Ras Laffan LNG cargo risk | P1 |
| Royal Navy | royalnavy.mod.uk | Escort / Kipion-related notices | P2 |
| Indian Navy | indiannavy.nic.in | Arabian Sea / escort context | P2 |
| IMO | imo.org | Maritime security guidance | P3 |
| Saudi National Center for Meteorology | ncm.gov.sa | Gulf weather ops impact | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified Telegram/X handles in `source_whitelist.json`; SHANA is whitelisted as web domain `shana.ir` (Primary Official Sources), not a social handle |

## Infrastructure & logistics

~20% of global oil trade typically transits Hormuz; Qatar LNG also depends on the strait. Key load points inside Gulf: Ras Tanura, UAE ports, Kuwait, Iraq Basra chain, Iranian Kharg. Staging outside: Fujairah, Oman Duqm/Sohar. Weather (haboob/storm) can amplify ops risk — ncm.gov.sa.

## Geopolitical triggers

- Vessel seizure, mine threat, or drone/missile strike on tanker.
- UKMTO elevated advisory or exclusion messaging.
- Iranian parliament / MFA threat to close strait (confirm on mfa.gov.ir / mop.ir).
- US/UK/regional escort surge or rules-of-engagement change.
- Sudden Fujairah inventory build or Duqm call-ups signaling preemptive reroute.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| UKMTO | event-driven / continuous | As issued |
| SHANA / mop.ir / nioc.ir | event-driven | Iran business hours |
| Mawani / AD Ports / Fujairah | ops / periodic stats | Local Gulf hours |
| QatarEnergy | event-driven | Company releases |

## Tier 2 context sources

IMO general maritime security pages; meteorology for ops delays. Secondary to UKMTO + coastal-state primary sources.

## Anti-patterns

- Unverified Telegram “Hormuz closed” channels.
- Treating every Gulf security headline as confirmed transit stoppage.
- Ignoring Fujairah/Duqm as outside-strait indicators.
- Using only secondary media without UKMTO or official MFA/NOC check.

## Related playbooks

- iran_oil_geopolitics.md
- saudi_arabia_oil.md
- uae_oil_fujairah.md
- qatar_ras_laffan_lng.md
- fujairah_storage_hub.md
- energy_sanctions_compliance.md
- red_sea_bab_el_mandeb.md

## Changelog

- 2026-07-23 — initial draft
