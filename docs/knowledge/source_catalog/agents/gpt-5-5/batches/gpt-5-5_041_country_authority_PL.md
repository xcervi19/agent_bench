# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_041_country_authority_PL.md  
**Fáze:** country_authority — krok PL (Fáze 2, Poland)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá sedmá dávka Fáze 2: `PL` × 10 typů autorit podle skeleton dimenze.  
Poland je desk-critical pro Russian sanctions enforcement, Baltic crude/product logistics, Gdansk/Naftoport routing, ORLEN refinery signals, Central Europe fuel balances and NATO/Baltic maritime security.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-PL-ministry_petroleum | PL | — | ministry_petroleum | Ministry of Energy Poland | gov.pl/web/energia | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-PL-noc | PL | — | noc | ORLEN | orlen.pl | noc | official | production, imports, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-PL-mfa | PL | — | mfa | Ministry of Foreign Affairs Poland | gov.pl/web/diplomacy | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-PL-customs_export | PL | — | customs_export | National Revenue Administration / PUESC | puesc.gov.pl | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-PL-upstream_regulator | PL | — | upstream_regulator | Energy Regulatory Office (URE) | ure.gov.pl | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-PL-port_maritime_authority | PL | — | port_maritime_authority | Maritime Office in Gdynia | umgdy.gov.pl | infrastructure | official | vessel_loading, port_closure, exports, imports | unverified |
| ca-PL-national_exchange | PL | — | national_exchange | Warsaw Stock Exchange | gpw.pl | exchange | data_feed | pricing_formula | proposed |
| ca-PL-central_bank | PL | — | central_bank | National Bank of Poland | nbp.pl | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-PL-environment_regulator | PL | — | environment_regulator | Ministry of Climate and Environment | gov.pl/web/klimat | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-PL-coast_guard_navy | PL | — | coast_guard_navy | Polish Navy | wojsko-polskie.pl/marynarka-wojenna | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-PL-ministry_petroleum | Primary official energy policy source. | Russia sanctions and Central Europe security context. | Logistics indirect. | proposed |
| ca-PL-noc | ORLEN is the key state-influenced downstream/refining anchor. | Strategic energy-security actor. | Direct refinery/product relevance, not a pure sovereign regulator. | proposed |
| ca-PL-upstream_regulator | URE is the energy regulatory source. | Market/regulatory context. | Less direct for cargoes. | proposed |
| ca-PL-port_maritime_authority | Maritime office source matters for Baltic logistics. | Gdansk/Naftoport route relevance. | Exact publication surface needs validation. | unverified |
| ca-PL-coast_guard_navy | Navy source matters for Baltic security. | NATO/Baltic security relevance. | Exact path needs validation. | unverified |

---

### Unverified / Anti-patterns

- `ORLEN` should be interpreted as a state-influenced strategic company, not a pure state authority.
- `ca-PL-customs_export`, `ca-PL-port_maritime_authority`, and `ca-PL-coast_guard_navy` need path validation before whitelist.
- Baltic disruption claims need ORLEN/operator, port, customs, shipping and NATO/security cross-checks.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 37,
  "last_country": "PL",
  "crosscheck_cursor": 0,
  "last_batch_seq": 41
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_042_country_authority_UA.md`.
