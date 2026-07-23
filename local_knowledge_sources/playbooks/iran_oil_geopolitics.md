# Iran oil geopolitics

**Commodity:** crude  
**Geography:** Iran — Kharg / Gulf — sanctions nexus  
**Last reviewed:** 2026-07-23  

## Executive summary

Iranian barrels move under sanctions via official policy signals and maritime export logistics (Kharg, PMO); OFAC enforcement and Hormuz geopolitics reprice the shadow/official balance. Scan must catch first: SHANA/mop.ir and NIOC, PMO traffic, MFA diplomacy, and OFAC designations — then Hormuz security (UKMTO).

## Price drivers (trader lens)

1. Effective export volumes under sanctions (not nameplate).
2. New OFAC vessel/trader designations or license shifts.
3. Hormuz escalation risk linked to Iranian posture.
4. Kharg / terminal operational status (PMO, NIOC).
5. Buyer geopolitics (China/others) and discount vs Brent/Dubai.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| NIOC | National oil company | NIOC |
| NIOC (via SHANA) | Fast official news | NIOC (via SHANA) |
| Ministry of Petroleum | Policy | Ministry of Petroleum |
| PMO maritime traffic | Ports / loadings | PMO maritime traffic |
| Ministry of Foreign Affairs | Diplomacy | Ministry of Foreign Affairs (mfa.gov.ir) |
| IRICA (Iran Customs) | Customs | IRICA (Iran Customs) / IRICA (Iran Customs Administration) |
| OFAC (Treasury) | US sanctions | OFAC (Treasury) |
| UKMTO (Maritime Trade Ops) | Maritime incidents | UKMTO (Maritime Trade Ops) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| NIOC (via SHANA) | shana.ir | Fast ministry/NOC news | P1 |
| Ministry of Petroleum | mop.ir | Policy / export framing | P1 |
| NIOC | nioc.ir | Export strategy / Kharg | P1 |
| PMO maritime traffic | pmo.ir | Kharg / Bandar Abbas / Assaluyeh traffic | P1 |
| Ministry of Foreign Affairs | mfa.gov.ir | Escalation / nuclear / sanctions diplomacy | P1 |
| IRICA (Iran Customs) | irica.gov.ir | Customs / trade control signals | P2 |
| IRICA (Iran Customs Administration) | irica.ir | Alternate customs domain | P2 |
| CBI – Central Bank of Iran | cbi.ir | FX / trade finance context | P3 |
| Department of Environment | doe.ir | Environmental constraints (Tier 2) | P3 |
| OFAC (Treasury) | treasury.gov | SDN / vessel designations; GLs | P1 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Gulf incidents | P1 |
| IMO | imo.org | Maritime sanctions guidance | P2 |
| GISIS IMO | gisis.imo.org | Dark-fleet screening | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified Telegram/X handles in whitelist; SHANA is web domain `shana.ir` listed under Primary Official Sources |

## Infrastructure & logistics

Kharg Island remains the core crude export node; Assaluyeh/other Gulf ports matter for condensates/products. Exports interact with Hormuz transit and sanctions tanker screening. Cross-check strait_of_hormuz and energy_sanctions_compliance.

## Geopolitical triggers

- OFAC wave on Iranian-linked tonnage.
- MFA/military threat language on Hormuz.
- Nuclear diplomacy breakthrough or breakdown.
- Confirmed Kharg outage or strike.
- Major buyer policy shift on Iranian crude.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| SHANA / mop.ir / nioc.ir | event-driven | Iran time |
| OFAC updates | event-driven | US business hours |
| UKMTO | event-driven | As issued |
| PMO | ops / periodic | Iran time |

## Tier 2 context sources

CBI FX context; DOE environmental. Not same-day export truth.

## Anti-patterns

- Unverified “Iran export bpd” Telegram trackers as primary.
- Treating every MFA statement as imminent Hormuz closure.
- Ignoring OFAC when counting “available” Iranian barrels.

## Related playbooks

- strait_of_hormuz.md
- energy_sanctions_compliance.md
- opec_plus_policy.md
- crude_oil_global.md
- saudi_arabia_oil.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
