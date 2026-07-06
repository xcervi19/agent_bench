# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_044_country_authority_SD.md  
**Fáze:** country_authority — krok SD (Fáze 2, Sudan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Čtyřicátá dávka Fáze 2: `SD` × 10 typů autorit podle skeleton dimenze.  
Sudan je desk-critical pro conflict-driven production/export disruption, Red Sea/Port Sudan logistics, pipeline relations with South Sudan, sanctions exposure and fragile official-source reliability.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SD-ministry_petroleum | SD | — | ministry_petroleum | Ministry of Energy and Petroleum Sudan | mop.gov.sd | government_regulator | official | production, exports, imports, quota_rhetoric | proposed |
| ca-SD-noc | SD | — | noc | Sudapet | sudapet.com | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-SD-mfa | SD | — | mfa | Sudan Ministry of Foreign Affairs | sudan.gov.sd | diplomacy | official | sanctions, export_license, quota_rhetoric | unverified |
| ca-SD-customs_export | SD | — | customs_export | Sudan Customs / government portal | sudan.gov.sd | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-SD-upstream_regulator | SD | — | upstream_regulator | Ministry of Energy and Petroleum Sudan | mop.gov.sd | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-SD-port_maritime_authority | SD | — | port_maritime_authority | Sea Ports Corporation Sudan | sudanports.gov.sd | infrastructure | official | vessel_loading, port_closure, exports, imports | unverified |
| ca-SD-national_exchange | SD | — | national_exchange | Khartoum Stock Exchange | kse.com.sd | exchange | data_feed | pricing_formula | unverified |
| ca-SD-central_bank | SD | — | central_bank | Central Bank of Sudan | cbos.gov.sd | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-SD-environment_regulator | SD | — | environment_regulator | Sudan environmental authority / government portal | sudan.gov.sd | government_regulator | official | refinery_outage, force_majeure, port_closure | unverified |
| ca-SD-coast_guard_navy | SD | — | coast_guard_navy | Sudan Navy / Ministry of Defence | — | government_regulator | official | port_closure, vessel_loading, sanctions | empty |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SD-ministry_petroleum | Primary oil policy source where accessible. | Civil-war and sanctions context. | Logistics indirect. | proposed |
| ca-SD-noc | Sudapet is the national oil company anchor. | Strategic state entity. | Direct production/concession relevance. | proposed |
| ca-SD-port_maritime_authority | Port Sudan logistics are critical. | Red Sea and conflict routing relevance. | Exact official domain/path needs validation. | unverified |
| ca-SD-central_bank | Payment/macro context is relevant during conflict. | Sanctions and FX relevance. | Indirect logistics signal. | proposed |
| ca-SD-coast_guard_navy | Maritime security matters but stable public source is not clear. | Red Sea security relevance. | Leave empty rather than inventing source. | empty |

---

### Unverified / Anti-patterns

- Sudan official web presence is fragile; validate `unverified` entries before whitelist.
- Do not treat conflict-party statements as state authority without provenance.
- For Port Sudan or pipeline disruption claims, cross-check with port, shipping, South Sudan, operator and security evidence.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 40,
  "last_country": "SD",
  "crosscheck_cursor": 0,
  "last_batch_seq": 44
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_045_country_authority_SS.md`.
