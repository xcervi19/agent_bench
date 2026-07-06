# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_012_country_authority_QA.md  
**Fáze:** country_authority — krok QA (Fáze 2, Qatar)  
**Datum:** 2026-07-05  

---

## Shrnutí

Osmá dávka Fáze 2: `QA` × 10 typů autorit podle skeleton dimenze.
Qatar je desk-critical pro LNG/North Field expansion, QatarEnergy term contracts, Ras Laffan logistics, Gulf maritime security a LNG-to-Europe/Asia flow signals.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-QA-ministry_petroleum | QA | — | ministry_petroleum | Minister of State for Energy Affairs / QatarEnergy | qatarenergy.qa | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-QA-noc | QA | ras_laffan | noc | QatarEnergy | qatarenergy.qa | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-QA-mfa | QA | — | mfa | Qatar Ministry of Foreign Affairs | mofa.gov.qa | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-QA-customs_export | QA | — | customs_export | Qatar General Authority of Customs | customs.gov.qa | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-QA-upstream_regulator | QA | ras_laffan | upstream_regulator | QatarEnergy Legal & Regulatory Framework | qatarenergy.qa | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-QA-port_maritime_authority | QA | ras_laffan | port_maritime_authority | Mwani Qatar | mwani.com.qa | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-QA-national_exchange | QA | — | national_exchange | Qatar Stock Exchange | qse.com.qa | exchange | data_feed | pricing_formula | proposed |
| ca-QA-central_bank | QA | — | central_bank | Qatar Central Bank | qcb.gov.qa | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-QA-environment_regulator | QA | — | environment_regulator | Ministry of Environment and Climate Change | mecc.gov.qa | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-QA-coast_guard_navy | QA | — | coast_guard_navy | General Directorate of Coasts and Borders Security / MOI | moi.gov.qa | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-QA-ministry_petroleum | Energy minister role is tightly tied to QatarEnergy leadership and policy. | Sovereign LNG and term-contract policy signal. | Indirect but critical for North Field and export strategy. | proposed |
| ca-QA-noc | Direct NOC source for LNG, upstream and export operations. | State strategic entity. | Direct Ras Laffan and LNG cargo relevance. | proposed |
| ca-QA-customs_export | Customs source for import/export enforcement. | Sanctions/transshipment relevance. | Direct clearance signal. | proposed |
| ca-QA-upstream_regulator | QatarEnergy is legally mandated to conduct or authorise petroleum operations. | State energy governance signal. | Direct project/field development relevance. | proposed |
| ca-QA-port_maritime_authority | Qatar port authority/operator. | Sovereign infrastructure source. | Direct vessel/loading/closure relevance, cross-check Ras Laffan operator data. | proposed |
| ca-QA-coast_guard_navy | MOI Coasts and Borders Security source. | Maritime/security enforcement relevance. | Direct Gulf maritime movement and port approach relevance. | proposed |

---

### Unverified / Anti-patterns

- `ca-QA-ministry_petroleum` and `ca-QA-upstream_regulator` both use `qatarenergy.qa` because QatarEnergy and the Minister of State for Energy Affairs are institutionally intertwined; avoid inventing a separate ministry domain.
- `Mwani Qatar` is port infrastructure coverage, but Ras Laffan-specific operational details may require QatarEnergy or terminal-level cross-checks.
- `Qatar Stock Exchange` is listed-market context, not physical LNG cargo confirmation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 8,
  "last_country": "QA",
  "crosscheck_cursor": 0,
  "last_batch_seq": 12
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_013_country_authority_OM.md` (Fáze 2, Oman autority).
