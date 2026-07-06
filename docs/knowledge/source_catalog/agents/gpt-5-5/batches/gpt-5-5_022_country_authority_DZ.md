# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_022_country_authority_DZ.md  
**Fáze:** country_authority — krok DZ (Fáze 2, Algeria)  
**Datum:** 2026-07-06  

---

## Shrnutí

Osmnáctá dávka Fáze 2: `DZ` × 10 typů autorit podle skeleton dimenze.  
Algeria je desk-critical pro Sonatrach pipeline/LNG exports, Mediterranean gas/oil logistics, OPEC+ posture, refinery/feedstock disruptions and North Africa diplomacy.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-DZ-ministry_petroleum | DZ | — | ministry_petroleum | Ministry of Energy and Renewable Energies | energy.gov.dz | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-DZ-noc | DZ | — | noc | Sonatrach | sonatrach.com | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-DZ-mfa | DZ | — | mfa | Ministry of Foreign Affairs and National Community Abroad | mae.gov.dz | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-DZ-customs_export | DZ | — | customs_export | Direction Generale des Douanes | douane.gov.dz | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-DZ-upstream_regulator | DZ | — | upstream_regulator | ALNAFT | alnaft.dz | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-DZ-port_maritime_authority | DZ | — | port_maritime_authority | Algerian ports / Ministry of Public Works and Basic Infrastructures | mtp.gov.dz | infrastructure | official | vessel_loading, port_closure, exports | unverified |
| ca-DZ-national_exchange | DZ | — | national_exchange | Algiers Stock Exchange / SGBV | sgbv.dz | exchange | data_feed | pricing_formula | proposed |
| ca-DZ-central_bank | DZ | — | central_bank | Bank of Algeria | bank-of-algeria.dz | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-DZ-environment_regulator | DZ | — | environment_regulator | Ministry of Environment Algeria | me.gov.dz | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-DZ-coast_guard_navy | DZ | — | coast_guard_navy | Algerian Coast Guard / Ministry of National Defence | mdn.dz | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-DZ-ministry_petroleum | Primary upstream/downstream policy source. | OPEC+ and regional energy diplomacy channel. | Logistics indirect but useful for official disruptions. | proposed |
| ca-DZ-noc | Sonatrach is the core operational export and contract source. | Strategic state entity for Europe/North Africa energy security. | Direct LNG, pipeline, cargo and terminal relevance. | proposed |
| ca-DZ-upstream_regulator | ALNAFT covers upstream licensing/regulatory signal. | Sovereign licensing and foreign-partner relevance. | Project/production relevance; less port-specific. | proposed |
| ca-DZ-port_maritime_authority | Port/public works source may capture infrastructure notices. | Sovereign infrastructure source. | Exact canonical port authority surface needs validation. | unverified |
| ca-DZ-coast_guard_navy | Maritime security source matters in western/central Mediterranean. | Defense/security relevance. | Coast Guard is under defense domain; exact public source path needs validation. | unverified |

---

### Unverified / Anti-patterns

- `ca-DZ-port_maritime_authority` is `unverified`: Algeria has ministry-level and port-company surfaces; confirm canonical source before whitelist.
- `ca-DZ-coast_guard_navy` is `unverified`: `mdn.dz` is the defense anchor, but the specific Coast Guard/Navy publication path should be validated.
- Do not use trade press or ship-tracking summaries as primary evidence for Sonatrach force majeure or state export policy; use them as cross-checks.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 18,
  "last_country": "DZ",
  "crosscheck_cursor": 0,
  "last_batch_seq": 22
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_023_country_authority_EG.md` (Fáze 2, Egypt autority).
