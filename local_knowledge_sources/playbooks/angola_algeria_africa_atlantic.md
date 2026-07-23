# Angola / Algeria — Africa Atlantic

**Commodity:** crude | gas  
**Geography:** Angola (Atlantic); Algeria (Med / OPEC+)  
**Last reviewed:** 2026-07-23  

## Executive summary

Angola supplies Atlantic medium/sweet barrels via Sonangol/ANPG; Algeria’s Sonatrach is an OPEC+ and Med gas/crude pillar. Scan must catch first: sonangol.co.ao, anpg.co.ao, mirempet.gov.ao; sonatrach.com and energy.gov.dz; OPEC tables for both.

## Price drivers (trader lens)

1. Angola block/production declines vs new project start-ups.
2. Algeria OPEC+ crude policy and Sonatrach export programmes.
3. Med gas geopolitics affecting Algeria (pipeline/LNG) spillovers to oil narrative.
4. Atlantic Basin grade competition into China/Europe.
5. Domestic political/security events hitting export continuity.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Sonangol | Angola NOC | Sonangol |
| ANPG | Angola upstream regulator | ANPG |
| MIREMPET | Angola petroleum ministry | MIREMPET |
| Sonatrach | Algeria NOC | Sonatrach |
| Ministry of Energy & Mines | Algeria | Ministry of Energy & Mines |
| OPEC | Quota framework | OPEC |
| Ministry of Foreign Affairs | Angola / Algeria diplomacy | mirex.gov.ao / mae.gov.dz |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Sonangol | sonangol.co.ao | Production / export / FM | P1 |
| ANPG | anpg.co.ao | Licensing / upstream status | P1 |
| MIREMPET | mirempet.gov.ao | Petroleum policy | P1 |
| Ministry of Foreign Affairs | mirex.gov.ao | Angola diplomacy | P3 |
| Banco Nacional de Angola | bna.ao | FX / oil revenue context | P3 |
| Sonatrach | sonatrach.com | Crude/gas export programmes | P1 |
| Ministry of Energy & Mines | energy.gov.dz | Algeria energy policy / OPEC+ | P1 |
| Ministry of Foreign Affairs | mae.gov.dz | Algeria diplomacy (Medgas context) | P2 |
| OPEC | opec.org | Angola/Algeria MOMR tables | P1 |
| IEA | iea.org | Africa supply context | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Angola: Atlantic load ports for Block 0/15/17-class barrels. Algeria: Mediterranean crude/condensate and major gas export system — oil scan still starts with Sonatrach/ministry; gas detail overlaps europe_gas_storage_ttf and nord_stream_alternatives_eu.

## Geopolitical triggers

- Sonangol/ANPG FM or licence dispute.
- Algeria OPEC+ cut surprise or Sonatrach strike/outage.
- Spain–Algeria diplomatic energy stress (Spanish MFA context).
- Security event near export terminals.
- OPEC+ African compensation schedule.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Sonangol / Sonatrach / ministries | event-driven | Local |
| OPEC MOMR | monthly | Mid-month |

## Tier 2 context sources

BNA macro; IEA Africa chapters. NOC/ministry primary for programmes.

## Anti-patterns

- Mixing Angola crude outages into Algeria gas headlines without check.
- Unofficial WAF fixture lists as production truth.
- Ignoring OPEC+ framing for Algeria.

## Related playbooks

- opec_plus_policy.md
- libya_nigeria_force_majeure.md
- congo_gabon_equatorial_guinea.md
- europe_gas_storage_ttf.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
