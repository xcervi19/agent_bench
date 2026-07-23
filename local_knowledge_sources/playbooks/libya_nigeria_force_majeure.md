# Libya / Nigeria force majeure

**Commodity:** crude  
**Geography:** Libya; Nigeria (West Africa Atlantic)  
**Last reviewed:** 2026-07-23  

## Executive summary

Libya and Nigeria are high-beta OPEC+ suppliers where political, security, and pipeline/port force majeure regularly removes sweet Atlantic barrels. Scan must catch first: noc.ly and nnpcgroup.com FM/production notices, Nigerian Ports Authority / Navy security, and OPEC tables for involuntary underproduction vs quota.

## Price drivers (trader lens)

1. Libya NOC declared force majeure or field/port shutdowns.
2. Nigeria pipeline vandalism, theft, or terminal constraints.
3. Sudden restoration of barrels (peace deals / secured pipelines).
4. Quality/availability of light sweet grades into Europe.
5. OPEC+ compensation optics when outages are involuntary.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| NOC – National Oil Corporation | Libya NOC | NOC – National Oil Corporation |
| Central Bank of Libya | Oil-revenue context | Central Bank of Libya |
| NNPC Limited | Nigeria NOC | NNPC Limited |
| Nigerian Ports Authority | Ports | Nigerian Ports Authority |
| Nigerian Navy | Security | Nigerian Navy |
| Nigeria Customs Service | Trade control | Nigeria Customs Service |
| Central Bank of Nigeria | Macro/oil FX | Central Bank of Nigeria |
| OPEC | Quota framework | OPEC |
| Eni | IOC ops visibility (Libya/Nigeria footprint) | Eni |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| NOC – National Oil Corporation | noc.ly | FM declarations; field/port status | P1 |
| Central Bank of Libya | cbl.gov.ly | Revenue/shutdown macro signals | P3 |
| NNPC Limited | nnpcgroup.com | Production; FM; pipeline status | P1 |
| Nigerian Ports Authority | nigerianports.gov.ng | Terminal/port restrictions | P1 |
| Nigerian Navy | navy.mil.ng | Security ops affecting export routes | P2 |
| Nigeria Customs Service | customs.gov.ng | Export documentation disruptions | P3 |
| Central Bank of Nigeria | cbn.gov.ng | FX/oil proceeds context | P3 |
| OPEC | opec.org | Libya/Nigeria in MOMR | P1 |
| Eni | eni.com | Operator notices (cross-check, not state primary) | P2 |
| IMO | imo.org | Maritime security guidance | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Libya: Mediterranean load ports tied to contested field politics. Nigeria: Forcados/Bonny-class export systems sensitive to pipeline integrity and waterborne security. Both feed Atlantic Basin sweet crude balances into Europe.

## Geopolitical triggers

- NOC FM across major Libyan ports.
- Nigeria militant / theft surge cutting pipeline receipt.
- Political deal reopening Libyan fields overnight.
- Terminal blockade or Navy security zone expansion.
- OPEC+ meeting focused on African underproduction.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| NOC / NNPC FM notices | event-driven | Local |
| Nigerian Ports | event-driven | Local |
| OPEC MOMR | monthly | Mid-month |

## Tier 2 context sources

CBN/CBL macro; Eni operator IR. State NOC/port notices remain primary for FM.

## Anti-patterns

- Social militia claims without NOC/NNPC confirmation.
- Assuming OPEC quota equals available export cargoes.
- Ignoring quality/port specifics when saying “Nigeria offline.”

## Related playbooks

- opec_plus_policy.md
- crude_oil_global.md
- angola_algeria_africa_atlantic.md
- north_sea_crude.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
