# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_054_country_authority_SS.md  
**Fáze:** country_authority — krok SS (South Sudan)  
**Datum:** 2026-07-06  

---

## Shrnutí

South Sudan = **landlocked oil producer** (~150 kb/d, mostly Blocks 3/7 + 1/2/4 = Unity/Thar
Jath/Paloch). **100 % exportu musí projít Súdánem** (GNPOC/Dar Blend pipeline → Port Sudan).
NILEPET = státní NOC. Každá SD–SS diplomatická krize = supply disruption. Klíčové signály:
**pipeline transit fee disputes**, **Dar Blend OSP** (South Sudan Dar crude benchmark),
**SSPOC upstream reports**. Nestabilní stát = primárně third-party monitoring. 5 proposed, 2 empty, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SS-ministry_petroleum | SS | — | ministry_petroleum | Ministry of Petroleum | mop.gov.ss | international_agency | official | policy, export_license | unverified |
| ca-SS-noc | SS | — | noc | Nilepet – Nile Petroleum Corporation | nilepet.com | international_agency | official | production, exports, term_contract | proposed |
| ca-SS-mfa | SS | — | mfa | Ministry of Foreign Affairs | mfa.gov.ss | international_agency | official | sanctions, policy | proposed |
| ca-SS-customs_export | SS | — | customs_export | National Revenue Authority | nra.gov.ss | international_agency | official | exports | unverified |
| ca-SS-upstream_regulator | SS | — | upstream_regulator | SSPOC – South Sudan Petroleum Oversight Committee | sspoc.gov.ss | international_agency | official | production | unverified |
| ca-SS-port_maritime_authority | SS | — | port_maritime_authority | — (landlocked; exports via Sudan/Port Sudan) | — | — | — | — | empty |
| ca-SS-national_exchange | SS | — | national_exchange | — (no stock exchange) | — | — | — | — | empty |
| ca-SS-central_bank | SS | — | central_bank | Bank of South Sudan | bss.gov.ss | international_agency | official | sanctions | proposed |
| ca-SS-environment_regulator | SS | — | environment_regulator | Ministry of Environment and Forestry | moef.gov.ss | international_agency | official | refinery_outage | proposed |
| ca-SS-coast_guard_navy | SS | — | coast_guard_navy | SSPDF (Navy/River Forces) | — | — | — | — | proposed |

---

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SS-noc (Nilepet) | Nilepet = state NOC; Blocks 3/7 (Dar Petroleum, CNPC 41% + Petronas 40%); Blocks 1/2/4 (ONGC+Petronas+CNPC); ~150 kb/d; Dar Blend OSP = SS crude benchmark | SS-Sudan transit fee disputes = periodic supply shutdown (2012 full shutdown); každé pipeline fee dispute = supply disruption | GNPOC pipeline (1,600 km to Port Sudan); Petrodar pipeline (parallel, shorter); entirely Sudan-dependent | **proposed** |
| ca-SS-mfa | SS = US-friendly (independence 2011 US-supported); pero internal conflict (2013-2018 civil war; 2020 peace deal fragile) | IGAD peace process; každé ceasefire violation = production field security risk; Heglig dispute with Sudan | Nil River boats for domestic fuel distribution; Juba + Malakal as inland hubs | **proposed** |

### Expansion
- Dar Petroleum (CNPC JV) → darpetroleumoperations.com (primary SS upstream)
- SSPOC → sspoc.gov.ss (upstream oversight body)

---
```json
{ "phase": "country_authority", "phase_index": 40, "last_country": "SS", "last_batch_seq": 54 }
```
