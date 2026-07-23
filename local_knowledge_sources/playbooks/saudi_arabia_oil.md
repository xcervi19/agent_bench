# Saudi Arabia oil

**Commodity:** crude  
**Geography:** Saudi Arabia — Arabian Gulf / Red Sea  
**Last reviewed:** 2026-07-23  

## Executive summary

Saudi Arabia is the OPEC+ swing supplier; Aramco OSP differentials and official production/capacity signals set East-of-Suez crude pricing. Scan must catch first: aramco.com OSP and ops commentary, Ministry of Energy policy, Mawani port throughput (Ras Tanura / Yanbu / Jubail), and MFA/security cues tied to Hormuz/Red Sea risk.

## Price drivers (trader lens)

1. Aramco OSP differential changes to Asia and other regions.
2. Kingdom production vs OPEC+ voluntary cut levels.
3. Ras Tanura / Gulf loading continuity vs Yanbu Red Sea optionality.
4. Spare capacity narrative and sudden max-capacity tests.
5. Regional security (Hormuz, Red Sea) altering Saudi export risk premia.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Saudi Aramco | NOC / OSP / producer | Saudi Aramco |
| Ministry of Energy | Energy policy | Ministry of Energy (energy.gov.sa / moenergy.gov.sa) |
| Saudi Ports Authority (Mawani) | Export ports | Saudi Ports Authority (Mawani) |
| Ministry of Foreign Affairs | Diplomacy | Ministry of Foreign Affairs (mofa.gov.sa) |
| Royal Saudi Navy | Maritime security | Royal Saudi Navy |
| OPEC | Quota framework | OPEC |
| Saudi Central Bank (SAMA) | FX / macro linkage | Saudi Central Bank (SAMA) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Saudi Aramco | aramco.com | OSP; production/capacity; outage notes | P1 |
| Ministry of Energy | energy.gov.sa | Policy / OPEC+ coordination signals | P1 |
| Ministry of Energy | moenergy.gov.sa | Ministry releases | P1 |
| Saudi Ports Authority (Mawani) | mawani.gov.sa | Ras Tanura / Yanbu / Jubail throughput | P1 |
| Ministry of Foreign Affairs | mofa.gov.sa | Security / Iran / regional diplomacy | P2 |
| Royal Saudi Navy | mod.gov.sa | Naval posture affecting loadings | P2 |
| OPEC | opec.org | Kingdom within OPEC+ tables | P1 |
| Saudi National Center for Meteorology | ncm.gov.sa | Gulf weather ops impact | P3 |
| Saudi Central Bank (SAMA) | sama.gov.sa | FX / sanctions linkage context | P3 |
| Saudi Exchange (Tadawul) | saudiexchange.sa | Financial Tier 2 only | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Primary Gulf export complex centered on Ras Tanura; Red Sea Yanbu provides canal-facing optionality. Pipelines link fields to both coasts. Hormuz risk affects Gulf loadings; Red Sea risk affects Yanbu — see strait_of_hormuz and red_sea_bab_el_mandeb.

## Geopolitical triggers

- OSP shock or unexpected production adjustment.
- Attack on energy infrastructure or export terminals.
- OPEC+ voluntary cut change led by Saudi.
- Hormuz escalation threatening Gulf loadings.
- Red Sea escalation affecting Yanbu programs.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Aramco OSP | monthly | Early month |
| Mawani / Aramco ops | event-driven | Gulf time |
| OPEC MOMR | monthly | Mid-month |
| Ministry releases | event-driven | Riyadh time |

## Tier 2 context sources

Tadawul; SAMA macro. Not primary for barrel availability.

## Anti-patterns

- Anonymous “OPEC delegate” social posts as Saudi policy.
- Using only secondary OSP “estimates” when aramco.com has posted.
- Ignoring Yanbu when framing all Saudi risk as Hormuz-only.

## Related playbooks

- opec_plus_policy.md
- oil_benchmarks_and_spreads.md
- strait_of_hormuz.md
- red_sea_bab_el_mandeb.md
- uae_oil_fujairah.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
