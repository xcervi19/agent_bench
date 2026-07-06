# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_020_country_authority_AO.md  
**Fáze:** country_authority — krok AO (Fáze 2, Angola)  
**Datum:** 2026-07-05  

---

## Shrnutí

Šestnáctá dávka Fáze 2: `AO` × 10 typů autorit podle skeleton dimenze.
Angola je desk-critical pro Atlantic crude exports, Sonangol/ANPG licensing, FPSO outages, OPEC+ policy and West Africa maritime/logistics.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-AO-ministry_petroleum | AO | — | ministry_petroleum | Ministry of Mineral Resources, Petroleum and Gas | mirempet.gov.ao | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-AO-noc | AO | — | noc | Sonangol | sonangol.co.ao | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-AO-mfa | AO | — | mfa | Angola Ministry of External Relations | mirex.gov.ao | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-AO-customs_export | AO | — | customs_export | General Tax Administration / Customs | agt.minfin.gov.ao | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-AO-upstream_regulator | AO | — | upstream_regulator | ANPG | anpg.co.ao | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-AO-port_maritime_authority | AO | — | port_maritime_authority | National Maritime Agency (AMN) | amn.gov.ao | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-AO-national_exchange | AO | — | national_exchange | BODIVA | bodiva.ao | exchange | data_feed | pricing_formula | proposed |
| ca-AO-central_bank | AO | — | central_bank | National Bank of Angola (BNA) | bna.ao | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-AO-environment_regulator | AO | — | environment_regulator | Ministry of Environment Angola | minamb.gov.ao | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-AO-coast_guard_navy | AO | — | coast_guard_navy | Angolan Navy / Ministry of Defence | mdn.gov.ao | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AO-ministry_petroleum | Primary petroleum policy source. | OPEC+/producer diplomacy context. | Logistics indirect. | proposed |
| ca-AO-noc | Sonangol is state oil company and export/operator source. | Strategic state entity. | Direct cargo/export relevance. | proposed |
| ca-AO-upstream_regulator | ANPG is concession/upstream regulator. | Sovereign licensing signal. | Direct production/project relevance. | proposed |
| ca-AO-port_maritime_authority | AMN covers maritime and port authority functions. | Sovereign maritime infrastructure source. | Direct port/navigation relevance. | proposed |
| ca-AO-coast_guard_navy | Navy/defense source would matter for maritime security. | Security relevance. | Exact public source needs validation. | unverified |

---

### Unverified / Anti-patterns

- `ca-AO-coast_guard_navy` is `unverified`: confirm exact Navy/defense source path before whitelist.
- `BODIVA` is capital-market context, not physical crude-flow confirmation.
- For FPSO/export outages, cross-check Sonangol/ANPG with operator releases and port/maritime signals.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 16,
  "last_country": "AO",
  "crosscheck_cursor": 0,
  "last_batch_seq": 20
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_021_country_authority_LY.md`.
