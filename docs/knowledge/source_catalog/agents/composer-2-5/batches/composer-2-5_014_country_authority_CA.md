# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_014_country_authority_CA.md  
**Fáze:** country_authority — krok CA (Fáze 2, země 12/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

Canada × 10 autorit. **9 proposed**, **1 empty** (noc — žádná státní NOC; soukromé + provinční korporace).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CA-ministry_petroleum | CA | — | ministry_petroleum | Natural Resources Canada (NRCan) | nrcan.gc.ca | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-CA-noc | CA | — | noc | (no national NOC) | — | noc | — | production,exports | empty |
| ca-CA-mfa | CA | — | mfa | Global Affairs Canada | international.gc.ca | diplomacy | official | sanctions,export_license | proposed |
| ca-CA-customs_export | CA | — | customs_export | Canada Border Services Agency (CBSA) | cbsa-asfc.gc.ca | government_regulator | official | exports,export_license,imports | proposed |
| ca-CA-upstream_regulator | CA | — | upstream_regulator | Canada Energy Regulator (CER) | cer-rec.gc.ca | government_regulator | official | production,term_contract,pipeline_outage | proposed |
| ca-CA-port_maritime_authority | CA | — | port_maritime_authority | Transport Canada — Marine Safety | tc.canada.ca | infrastructure | official | vessel_loading,port_closure | proposed |
| ca-CA-national_exchange | CA | — | national_exchange | Montreal Exchange (MX) | m-x.ca | exchange | official | pricing_formula,storage_levels | proposed |
| ca-CA-central_bank | CA | — | central_bank | Bank of Canada | bankofcanada.ca | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-CA-environment_regulator | CA | — | environment_regulator | Environment and Climate Change Canada | canada.ca | government_regulator | official | refinery_outage,production | proposed |
| ca-CA-coast_guard_navy | CA | — | coast_guard_navy | Canadian Coast Guard | ccg-gcc.gc.ca | government_regulator | official | port_closure,vessel_loading | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CA-upstream_regulator | CER pipeline / production data | TMX / Line 5 diplomacy | Keystone / Trans Mountain flows | **proposed** |
| ca-CA-ministry_petroleum | Oil sands policy, emissions cap | US trade / pipeline politics | Export capacity to US Gulf | **proposed** |
| ca-CA-noc | Private producers (Suncor, Cenovus, CNRL) | — | No state NOC | **empty** — playbook: majors + CER |

**Desk Tier 1:** cer-rec.gc.ca + nrcan.gc.ca + m-x.ca (WCS). Alberta regulator **AER** (` aer.ca`) — playbook extension (provincial).

### Progress po merge (návrh)

`last_country: CA`, `last_batch_seq: 14`. **Další:** MX.

### Whitelist kandidáti (Tier 1, po schválení — 5 zemí)

QA: `qatarenergy.qa`, `mme.gov.qa` | OM: `oq.com`, `pdo.co.om` | NO: `npd.no`, `equinor.com` | BR: `petrobras.com.br`, `gov.br/anp` | CA: `cer-rec.gc.ca`, `nrcan.gc.ca`
