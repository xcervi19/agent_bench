# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_047_country_authority_GY.md  
**Fáze:** country_authority — krok GY (Fáze 2, Guyana)  
**Datum:** 2026-07-06  

---

## Shrnutí

Čtyřicátá třetí dávka Fáze 2: `GY` × 10 typů autorit podle skeleton dimenze.  
Guyana je desk-critical pro Stabroek offshore production growth, FPSO outages, Exxon/Hess/CNOOC project signals, Venezuela border risk, crude exports, royalty/tax policy and Atlantic maritime security.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GY-ministry_petroleum | GY | — | ministry_petroleum | Ministry of Natural Resources Guyana | mnr.gov.gy | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-GY-noc | GY | — | noc | — | — | noc | official | production, exports, force_majeure, term_contract, vessel_loading | empty |
| ca-GY-mfa | GY | — | mfa | Ministry of Foreign Affairs Guyana | minfor.gov.gy | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-GY-customs_export | GY | — | customs_export | Guyana Revenue Authority | gra.gov.gy | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-GY-upstream_regulator | GY | — | upstream_regulator | Petroleum Management Programme | petroleum.gov.gy | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-GY-port_maritime_authority | GY | — | port_maritime_authority | Maritime Administration Department Guyana | maritime.gov.gy | infrastructure | official | vessel_loading, port_closure, exports, imports | unverified |
| ca-GY-national_exchange | GY | — | national_exchange | Guyana Association of Securities Companies and Intermediaries | gasci.com | exchange | data_feed | pricing_formula | unverified |
| ca-GY-central_bank | GY | — | central_bank | Bank of Guyana | bankofguyana.org.gy | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-GY-environment_regulator | GY | — | environment_regulator | Environmental Protection Agency Guyana | epa.gov.gy | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-GY-coast_guard_navy | GY | — | coast_guard_navy | Guyana Defence Force / Coast Guard | gdf.mil.gy | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GY-ministry_petroleum | Primary petroleum policy and resource-management source. | Venezuela border and licensing context. | Logistics indirect. | proposed |
| ca-GY-upstream_regulator | Petroleum Management Programme is the petroleum management surface. | Project approvals and audit context. | Direct production/project relevance. | proposed |
| ca-GY-customs_export | GRA is relevant for export/tax and customs context. | Royalty/tax policy relevance. | Trade-flow support. | proposed |
| ca-GY-noc | Guyana has no established NOC equivalent. | — | — | empty |
| ca-GY-coast_guard_navy | Coast Guard matters for offshore security. | Venezuela/Atlantic security relevance. | Exact domain/path needs validation. | unverified |

---

### Unverified / Anti-patterns

- `ca-GY-noc` is `empty`: do not force Exxon/Hess/CNOOC or a planned petroleum commission into a NOC slot.
- `ca-GY-port_maritime_authority`, `ca-GY-national_exchange`, and `ca-GY-coast_guard_navy` need manual domain/path validation before whitelist.
- For FPSO/offshore disruptions, prioritize operator releases, MNR/petroleum notices, EPA filings and shipping/export evidence.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 43,
  "last_country": "GY",
  "crosscheck_cursor": 0,
  "last_batch_seq": 47
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_048_country_authority_SN.md` (Fáze 2, Senegal autority).
