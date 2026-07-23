# Israel Levant gas

**Commodity:** gas  
**Geography:** Israel — Levant Basin / regional export links  
**Last reviewed:** 2026-07-23  

## Executive summary

Israel’s offshore gas (Leviathan/Tamar-class system) supplies domestic demand and regional exports; conflict and regulatory actions can cut flows and reprice East Med energy risk. Scan must catch first: energy.economy.gov.il / gov.il ministry of energy, taxes.gov.il export declarations, gov.il/mfa diplomacy, and regional security spillover to Egypt export links.

## Price drivers (trader lens)

1. Offshore field / platform security shutdowns.
2. Petroleum Commissioner / ministry export or production directives.
3. Pipeline export interruptions (e.g. EMG-linked notes on customs).
4. Regional conflict intensity near energy infrastructure.
5. Egypt offtake / LNG reconversion knock-ons (mfa.gov.eg context).

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Petroleum Commissioner (Ministry of Energy) | Upstream regulator | Petroleum Commissioner (Ministry of Energy) |
| Ministry of Energy | Energy policy | Ministry of Energy (gov.il) |
| Ministry of Foreign Affairs | Diplomacy | Ministry of Foreign Affairs (gov.il/mfa) |
| Israel Tax Authority (Customs) | Export declarations | Israel Tax Authority (Customs) |
| Ministry of Environmental Protection | Env compliance | Ministry of Environmental Protection |
| Ministry of Foreign Affairs | Egypt adjacency | Ministry of Foreign Affairs (mfa.gov.eg) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Petroleum Commissioner (Ministry of Energy) | energy.economy.gov.il | Upstream/export regulation | P1 |
| Ministry of Energy | gov.il/en/departments/ministry_of_energy | Policy; emergency measures | P1 |
| Ministry of Foreign Affairs | gov.il/mfa | Security diplomacy affecting energy | P1 |
| Israel Tax Authority (Customs) | taxes.gov.il | Gas export declarations (EMG notes) | P1 |
| Ministry of Environmental Protection | gov.il | / gov.il/en/departments/epa — env stoppages | P2 |
| Ministry of Foreign Affairs | mfa.gov.eg | Egypt energy security adjacency | P2 |
| IEA | iea.org | East Med gas context | P3 |
| IMO | imo.org | Offshore maritime security guidance | P3 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Broader maritime threat context | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Levant Basin offshore platforms feed domestic power/industry and export pipelines toward neighbors (customs notes reference EMG sub-sea). Conflict can force precautionary shutdowns even without direct hits. Regional LNG in Egypt can be affected if pipeline gas drops.

## Geopolitical triggers

- Direct threat/attack on offshore platforms.
- Ministry-ordered production/export halt.
- Escalation with neighbors cutting pipeline exports.
- Major env/regulatory stoppage.
- Broader Red Sea conflict sucking naval/security resources (cross-check yemen_houthi_red_sea).

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Ministry / Petroleum Commissioner | event-driven | Israel time |
| Customs declarations | periodic / event | Local |
| MFA | event-driven | Local |

## Tier 2 context sources

IEA East Med notes; IMO. Israeli ministry/customs are primary.

## Anti-patterns

- Inventing operator IR domains not on whitelist.
- Social “platform hit” claims without ministry confirmation.
- Ignoring Egypt offtake linkage when modeling Israeli export cuts.

## Related playbooks

- yemen_houthi_red_sea.md
- europe_gas_storage_ttf.md
- natural_gas_global.md
- red_sea_bab_el_mandeb.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
