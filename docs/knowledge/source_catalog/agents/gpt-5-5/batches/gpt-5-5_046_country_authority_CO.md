# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_046_country_authority_CO.md  
**Fáze:** country_authority — krok CO (Fáze 2, Colombia)  
**Datum:** 2026-07-06  

---

## Shrnutí

Čtyřicátá druhá dávka Fáze 2: `CO` × 10 typů autorit podle skeleton dimenze.  
Colombia je desk-critical pro Ecopetrol production/export signals, Caribbean/Pacific ports, pipeline/security disruptions, sanctions-adjacent Venezuela exposure, refinery/product balances and Caribbean maritime security.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CO-ministry_petroleum | CO | — | ministry_petroleum | Ministry of Mines and Energy | minenergia.gov.co | government_regulator | official | production, exports, imports, quota_rhetoric | proposed |
| ca-CO-noc | CO | — | noc | Ecopetrol | ecopetrol.com.co | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-CO-mfa | CO | — | mfa | Ministry of Foreign Affairs Colombia | cancilleria.gov.co | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-CO-customs_export | CO | — | customs_export | DIAN | dian.gov.co | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-CO-upstream_regulator | CO | — | upstream_regulator | National Hydrocarbons Agency (ANH) | anh.gov.co | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-CO-port_maritime_authority | CO | — | port_maritime_authority | DIMAR / Maritime Authority | dimar.mil.co | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-CO-national_exchange | CO | — | national_exchange | Bolsa de Valores de Colombia | bvc.com.co | exchange | data_feed | pricing_formula | proposed |
| ca-CO-central_bank | CO | — | central_bank | Banco de la Republica | banrep.gov.co | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-CO-environment_regulator | CO | — | environment_regulator | Ministry of Environment and Sustainable Development | minambiente.gov.co | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-CO-coast_guard_navy | CO | — | coast_guard_navy | Colombian Navy | armada.mil.co | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CO-ministry_petroleum | Primary official energy policy source. | Venezuela exposure and export-policy relevance. | Logistics indirect. | proposed |
| ca-CO-noc | Ecopetrol is core state-controlled oil company source. | Strategic national producer. | Direct production/export/refinery relevance. | proposed |
| ca-CO-upstream_regulator | ANH is the upstream hydrocarbon regulator. | Licensing and production context. | Direct project/production relevance. | proposed |
| ca-CO-port_maritime_authority | DIMAR is relevant for maritime and port safety context. | Caribbean/Pacific maritime security relevance. | Direct logistics relevance. | proposed |
| ca-CO-coast_guard_navy | Navy source matters for Caribbean/Pacific security. | Smuggling/security and Venezuela context. | Maritime signal, not cargo proof alone. | proposed |

---

### Unverified / Anti-patterns

- Ecopetrol is commercial/state-controlled; interpret company releases with operator and ministry context.
- Colombia pipeline disruption claims need Ecopetrol, security, community, regulator and port/shipping cross-checks.
- Do not use BVC market moves as physical supply evidence without official and logistics confirmation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 42,
  "last_country": "CO",
  "crosscheck_cursor": 0,
  "last_batch_seq": 46
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_047_country_authority_GY.md`.
