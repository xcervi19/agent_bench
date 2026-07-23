# Congo / Gabon / Equatorial Guinea

**Commodity:** crude  
**Geography:** Republic of Congo; Gabon; Equatorial Guinea (Gulf of Guinea)  
**Last reviewed:** 2026-07-23  

## Executive summary

Smaller Gulf of Guinea OPEC+/Atlantic producers where NOC and port status move niche grades. Scan must catch first: snpc.cg and Pointe-Noire port; gabonoil.ga and Owendo/Libreville ports; mmh.gob.gq for EG; OPEC tables for membership/compliance context.

## Price drivers (trader lens)

1. Field decline vs short-cycle outages at each producer.
2. Port restrictions at Pointe-Noire / Owendo affecting liftings.
3. OPEC+ policy for Gabon/EG (and Congo as relevant).
4. Local political/fiscal shocks to NOC operations.
5. Atlantic Basin competition for light/medium African barrels.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| SNPC (Société Nationale des Pétroles du Congo) | Congo NOC | SNPC (Société Nationale des Pétroles du Congo) |
| Ministry of Hydrocarbons | Congo | Ministry of Hydrocarbons |
| Port Autonome de Pointe-Noire | Congo export port | Port Autonome de Pointe-Noire |
| Gabon Oil Company (GOC) | Gabon NOC | Gabon Oil Company (GOC) |
| Port of Owendo / Libreville | Gabon ports | Port of Owendo / Libreville |
| Ministry of Mines and Hydrocarbons | Equatorial Guinea | Ministry of Mines and Hydrocarbons |
| OPEC | Quota framework | OPEC |
| BEAC (Central African) | Regional FX context | BEAC (Central African) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| SNPC (Société Nationale des Pétroles du Congo) | snpc.cg | Production / export / FM | P1 |
| Ministry of Hydrocarbons | hydrocarbures.gouv.cg | Congo petroleum policy | P1 |
| Port Autonome de Pointe-Noire | port-pointenoire.cg | Port status / restrictions | P1 |
| Ministry of Foreign Affairs | diplomatie.gouv.cg | Congo diplomacy | P3 |
| Gabon Oil Company (GOC) | gabonoil.ga | Gabon production / export | P1 |
| Port of Owendo / Libreville | portsgabon.ga | Gabon port ops | P1 |
| Ministry of Mines and Hydrocarbons | mmh.gob.gq | EG licensing; GEPetrol/EGLNG oversight notes | P1 |
| OPEC | opec.org | Gabon/EG/Congo in MOMR as applicable | P1 |
| BEAC (Central African) | beac.int | Regional macro/FX | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Pointe-Noire and Gabonese Atlantic ports clear modest but price-sensitive cargoes into Europe/Asia. EG offshore systems link crude and EGLNG governance under mmh.gob.gq notes. Treat each country’s FM separately — do not assume regional co-movement.

## Geopolitical triggers

- SNPC/GOC FM or port strike.
- EG ministry licensing shock or EGLNG-linked disruption.
- OPEC+ cut allocation change for Gabon/EG.
- Security incident in Gulf of Guinea shipping lanes.
- Fiscal crisis freezing NOC liftings.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| NOC / ministry / port notices | event-driven | Local |
| OPEC MOMR | monthly | Mid-month |

## Tier 2 context sources

BEAC; MFA pages. Ports + NOCs remain primary.

## Anti-patterns

- One “WAF outage” headline covering three countries without entity check.
- Unofficial fixture WhatsApp lists as production data.
- Ignoring port status when NOC claims normal output.

## Related playbooks

- angola_algeria_africa_atlantic.md
- libya_nigeria_force_majeure.md
- opec_plus_policy.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
