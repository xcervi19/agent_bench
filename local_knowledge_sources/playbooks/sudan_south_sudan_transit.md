# Sudan / South Sudan transit

**Commodity:** crude  
**Geography:** South Sudan production — Sudan transit to Red Sea  
**Last reviewed:** 2026-07-23  

## Executive summary

South Sudanese crude depends on pipeline transit through Sudan to Red Sea ports; war, fee disputes, and Nilepet/ops failures can zero exports quickly. Scan must catch first: nilepet.com, cbos.gov.sd war/macro context, and Red Sea security (UKMTO / SCA approaches) affecting the outlet.

## Price drivers (trader lens)

1. Pipeline transit restart/stop decisions between Juba and Khartoum.
2. Nilepet / block operator production status.
3. Sudan conflict intensity near pipeline/port infrastructure.
4. Transit-fee or political deal headlines confirmed by officials.
5. Red Sea security for laden tankers leaving Port Sudan area.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Nilepet (South Sudan) | South Sudan NOC | Nilepet (South Sudan) |
| Central Bank of Sudan | Sudan macro / war context | Central Bank of Sudan |
| UKMTO (Maritime Trade Ops) | Red Sea maritime risk | UKMTO (Maritime Trade Ops) |
| Suez Canal Authority (SCA) | Downstream Red Sea–Med lane | Suez Canal Authority (SCA) |
| Ministry of Foreign Affairs | Egypt Red Sea security context | Ministry of Foreign Affairs (mfa.gov.eg) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Nilepet (South Sudan) | nilepet.com | Production; block status; export framing | P1 |
| Central Bank of Sudan | cbos.gov.sd | War-economy / FX signals tied to oil | P2 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Red Sea incidents near outlet | P1 |
| Suez Canal Authority (SCA) | suezcanal.gov.eg | Broader Red Sea–Med logistics | P2 |
| Ministry of Foreign Affairs | mfa.gov.eg | Red Sea security diplomacy | P3 |
| OPEC | opec.org | Balance footnotes if any | P3 |
| IMO | imo.org | Maritime guidance | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Upstream in South Sudan (Dar/GNPOC-related blocks per Nilepet notes) ships via Sudan pipeline to Red Sea. Conflict can sever transit independent of wellhead capability. Outlet risk overlaps yemen_houthi_red_sea / red_sea_bab_el_mandeb for tanker acceptance.

## Geopolitical triggers

- Formal transit suspension or restart agreement.
- Attack on pipeline/pump stations.
- Nilepet declaration of FM.
- Escalation in Sudanese civil conflict near energy assets.
- Red Sea advisory making Port Sudan liftings uninsurable.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Nilepet | event-driven | Local |
| CBOS | periodic / event | Local |
| UKMTO | event-driven | As issued |

## Tier 2 context sources

Whitelist coverage for Sudanese energy ministry domains is thin — do not invent ministries. Rely on Nilepet + CBOS + Red Sea maritime primaries; flag gaps rather than fabricating domains.

## Anti-patterns

- Inventing Sudanese ministry URLs not in source_whitelist.json.
- Treating every Juba political headline as pipeline restart.
- Ignoring Red Sea insurance as a binding constraint.

## Related playbooks

- red_sea_bab_el_mandeb.md
- yemen_houthi_red_sea.md
- suez_canal_transit.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic; thin Sudan ministry whitelist coverage noted
