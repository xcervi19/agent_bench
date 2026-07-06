# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_021_country_authority_LY.md  
**Fáze:** country_authority — krok LY (Fáze 2, Libya)  
**Datum:** 2026-07-05  

---

## Shrnutí

Sedmnáctá dávka Fáze 2: `LY` × 10 typů autorit podle skeleton dimenze.
Libya je desk-critical pro NOC force majeure, militia/port blockades, Es Sider/Ras Lanuf/Zawiya flows, central bank payment splits and political fragmentation risk.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-LY-ministry_petroleum | LY | — | ministry_petroleum | Libya Ministry of Oil and Gas | oil.gov.ly | government_regulator | official | production, exports, quota_rhetoric, term_contract | unverified |
| ca-LY-noc | LY | — | noc | National Oil Corporation Libya | noc.ly | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-LY-mfa | LY | — | mfa | Libya Ministry of Foreign Affairs | foreign.gov.ly | diplomacy | official | sanctions, export_license, quota_rhetoric | unverified |
| ca-LY-customs_export | LY | — | customs_export | Libyan Customs Authority | customs.gov.ly | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-LY-upstream_regulator | LY | — | upstream_regulator | National Oil Corporation Libya | noc.ly | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-LY-port_maritime_authority | LY | — | port_maritime_authority | Libyan Ports / Transport Authority | transport.gov.ly | infrastructure | official | vessel_loading, port_closure, exports | unverified |
| ca-LY-national_exchange | LY | — | national_exchange | Libyan Stock Market | lsm.gov.ly | exchange | data_feed | pricing_formula | unverified |
| ca-LY-central_bank | LY | — | central_bank | Central Bank of Libya | cbl.gov.ly | government_regulator | official | sanctions, pricing_formula, imports, exports | unverified |
| ca-LY-environment_regulator | LY | — | environment_regulator | Environment General Authority Libya | ega.gov.ly | government_regulator | official | refinery_outage, force_majeure, port_closure | unverified |
| ca-LY-coast_guard_navy | LY | — | coast_guard_navy | Libyan Navy / Coast Guard | navy.mil.ly | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-LY-noc | NOC is the critical operational and force-majeure source. | Central actor in political fragmentation and export blockades. | Direct port/loading relevance. | proposed |
| ca-LY-customs_export | Customs authority has trade-control relevance. | Sanctions/export enforcement context. | Clearance signal, less direct for crude liftings. | proposed |
| ca-LY-upstream_regulator | NOC often acts as operational/regulatory anchor in practice. | Political legitimacy issues affect source interpretation. | Direct production relevance. | proposed |
| ca-LY-ministry_petroleum | Relevant policy source if active/canonical. | High political fragmentation risk. | Domain requires validation. | unverified |
| ca-LY-coast_guard_navy | Maritime security source would matter. | Direct militia/security and sanctions relevance. | Exact official source needs validation. | unverified |

---

### Unverified / Anti-patterns

- Many Libya authority domains are `unverified` due to fragmented institutions and unstable official web presence; validate before whitelist.
- For trading alerts, prioritize `noc.ly` force majeure and port statements, then cross-check with maritime/logistics evidence.
- Do not treat rival-government or local militia media as primary state authority without explicit provenance.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 17,
  "last_country": "LY",
  "crosscheck_cursor": 0,
  "last_batch_seq": 21
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_022_country_authority_DZ.md` (Fáze 2, Algeria autority).
