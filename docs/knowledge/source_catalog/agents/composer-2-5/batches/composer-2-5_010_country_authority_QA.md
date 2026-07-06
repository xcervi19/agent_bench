# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_010_country_authority_QA.md  
**Fáze:** country_authority — krok QA (Fáze 2, země 8/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

Qatar × 10 autorit. **9 proposed**, **1 unverified** (national_exchange).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-QA-ministry_petroleum | QA | — | ministry_petroleum | Ministry of Energy and Industry | mme.gov.qa | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-QA-noc | QA | — | noc | QatarEnergy | qatarenergy.qa | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-QA-mfa | QA | — | mfa | Ministry of Foreign Affairs | mofa.gov.qa | diplomacy | official | sanctions,export_license | proposed |
| ca-QA-customs_export | QA | — | customs_export | General Authority of Customs | customs.gov.qa | government_regulator | official | exports,export_license,imports | proposed |
| ca-QA-upstream_regulator | QA | — | upstream_regulator | QatarEnergy — Upstream | qatarenergy.qa | government_regulator | official | production,term_contract | proposed |
| ca-QA-port_maritime_authority | QA | — | port_maritime_authority | Mwani Qatar | mwani.com.qa | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-QA-national_exchange | QA | — | national_exchange | Qatar Stock Exchange | qe.com.qa | exchange | official | pricing_formula | unverified |
| ca-QA-central_bank | QA | — | central_bank | Qatar Central Bank | qcb.gov.qa | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-QA-environment_regulator | QA | — | environment_regulator | Ministry of Environment and Climate Change | mmecc.gov.qa | government_regulator | official | refinery_outage,production | proposed |
| ca-QA-coast_guard_navy | QA | — | coast_guard_navy | Ministry of Defence | mod.gov.qa | government_regulator | official | port_closure,vessel_loading | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-QA-noc | North Field expansion, LNG trains | LNG diplomacy / EU contracts | Ras Laffan / Mesaieed exports | **proposed** |
| ca-QA-ministry_petroleum | OPEC+ quota (condensate split) | Gulf mediation role | Export allocation | **proposed** |
| ca-QA-port_maritime_authority | — | — | Ras Laffan, Hamad Port | **proposed** |

**Desk Tier 1:** qatarenergy.qa + mme.gov.qa + mwani.com.qa. LNG focus — pair Ras Laffan geo batch later.

### Progress po merge (návrh)

`last_country: QA`, `last_batch_seq: 10`. **Další:** OM.
