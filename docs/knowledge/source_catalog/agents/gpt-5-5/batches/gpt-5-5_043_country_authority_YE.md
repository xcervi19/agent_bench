# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_043_country_authority_YE.md  
**Fáze:** country_authority — krok YE (Fáze 2, Yemen)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá devátá dávka Fáze 2: `YE` × 10 typů autorit podle skeleton dimenze.  
Yemen je desk-critical pro Red Sea/Bab el-Mandeb security, port closures, fuel import bottlenecks, Safer/Marib production signals, sanctions risk and split-authority source validation.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-YE-ministry_petroleum | YE | — | ministry_petroleum | Ministry of Oil and Minerals Yemen | mom-ye.com | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-YE-noc | YE | — | noc | Safer Exploration & Production Operations Company | sepocye.com | noc | official | production, force_majeure, term_contract, vessel_loading | proposed |
| ca-YE-mfa | YE | — | mfa | Yemen Ministry of Foreign Affairs | mofa-ye.org | diplomacy | official | sanctions, export_license, quota_rhetoric | unverified |
| ca-YE-customs_export | YE | — | customs_export | Yemen Customs Authority | yemen-customs.net | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-YE-upstream_regulator | YE | — | upstream_regulator | Ministry of Oil and Minerals Yemen | mom-ye.com | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-YE-port_maritime_authority | YE | — | port_maritime_authority | Yemen Red Sea Ports Corporation | yrspc.gov.ye | infrastructure | official | vessel_loading, port_closure, exports, imports | unverified |
| ca-YE-national_exchange | YE | — | national_exchange | — | — | exchange | data_feed | pricing_formula | empty |
| ca-YE-central_bank | YE | — | central_bank | Central Bank of Yemen | cby-ye.com | government_regulator | official | sanctions, pricing_formula, imports, exports | unverified |
| ca-YE-environment_regulator | YE | — | environment_regulator | Yemen Environment Protection Authority | epa-ye.com | government_regulator | official | refinery_outage, force_majeure, port_closure | unverified |
| ca-YE-coast_guard_navy | YE | — | coast_guard_navy | Yemen Coast Guard / Navy | — | government_regulator | official | port_closure, vessel_loading, sanctions | empty |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-YE-ministry_petroleum | Primary oil policy source where accessible. | Split-authority and sanctions context. | Logistics indirect. | proposed |
| ca-YE-noc | Safer is important for Marib/Block 18 and legacy production. | Control and conflict context affects interpretation. | Direct production relevance. | proposed |
| ca-YE-customs_export | Customs can support import/fuel-flow checks. | Sanctions and border-control relevance. | Trade-flow relevance. | proposed |
| ca-YE-port_maritime_authority | Red Sea ports are core logistics signal. | Direct conflict and blockade context. | Exact official authority needs validation. | unverified |
| ca-YE-coast_guard_navy | Maritime security matters but no stable source is clear. | High security relevance. | Leave empty rather than inventing a source. | empty |

---

### Unverified / Anti-patterns

- Yemen has competing authorities and unstable official web presence; validate every `unverified` domain before whitelist.
- Do not treat factional media or port claims as sovereign evidence without provenance and maritime/security cross-checks.
- For trading alerts, triangulate ministry/Safer/customs with port notices, shipping security advisories and conflict reporting.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 39,
  "last_country": "YE",
  "crosscheck_cursor": 0,
  "last_batch_seq": 43
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_044_country_authority_SD.md`.
