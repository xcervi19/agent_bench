# North Sea crude

**Commodity:** crude  
**Geography:** UK / Norway North Sea  
**Last reviewed:** 2026-07-23  

## Executive summary

North Sea grades anchor the Brent complex; Equinor/Norway volumes and UK NSTA field status, plus ICE Brent structure, set Atlantic sweet pricing. Scan must catch first: equinor.com and sodir.no / regjeringen.no, nstauthority.co.uk, ice.com Brent settlements, and Met Office / offshore weather impacting loadings.

## Price drivers (trader lens)

1. Planned and unplanned North Sea field/FPSO outages.
2. ICE Brent expiry and physical programme tightness.
3. Norwegian production guidance (Equinor / OED).
4. UK Continental Shelf decline vs maintenance seasons.
5. Weather downtime in loading windows.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Equinor | Norway producer | Equinor |
| Norwegian Offshore Directorate | Norway upstream data | Norwegian Offshore Directorate |
| Ministry of Energy (OED) | Norway policy | Ministry of Energy (OED) |
| NSTA (UK North Sea) | UK regulator | NSTA (UK North Sea) |
| ICE | Brent futures | ICE |
| UK Met Office | Weather | UK Met Office |
| Royal Navy | Offshore security | Royal Navy |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Equinor | equinor.com | Field status; FM; production | P1 |
| Norwegian Offshore Directorate | sodir.no | Production / resource data | P1 |
| Ministry of Energy (OED) | regjeringen.no | Norway energy policy | P1 |
| NSTA (UK North Sea) | nstauthority.co.uk | UKCS production / consents | P1 |
| ICE | ice.com | Brent settlements / expiry | P1 |
| UK Met Office | metoffice.gov.uk | Offshore weather | P2 |
| Royal Navy | royalnavy.mod.uk | Offshore security ops | P3 |
| Oslo Bors | oslobors.no | Financial Tier 2 | P3 |
| IEA | iea.org | North Sea in balances | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Offshore platforms and FPSOs load into North Sea/Atlantic shipping; Forties/Ekofisk-class systems feed Brent. Maintenance seasons (summer) and winter storms cut programmes. Links to oil_benchmarks_and_spreads and rotterdam_antwerp_hub for refining offtake.

## Geopolitical triggers

- Major Norwegian outage (Equinor FM).
- UKCS labour / energy-policy shock.
- Security incident on offshore infrastructure.
- Extreme North Sea storm sequence.
- Brent contract specification / expiry dislocation.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Equinor / NSTA / SODIR | event + periodic | Local |
| ICE Brent | daily | Exchange close |
| Met Office | continuous | UK time |

## Tier 2 context sources

Oslo Bors; Bank of England macro. Not programme primary.

## Anti-patterns

- Pricing Brent only from social “outage lists.”
- Ignoring Norway vs UK split in Atlantic sweet supply.
- Conflating gas outages with crude programme cuts without check.

## Related playbooks

- oil_benchmarks_and_spreads.md
- norway_hammerfest_lng.md
- rotterdam_antwerp_hub.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
