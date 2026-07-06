# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_040_country_authority_ES.md  
**Fáze:** country_authority — krok ES (Fáze 2, Spain)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá šestá dávka Fáze 2: `ES` × 10 typů autorit podle skeleton dimenze.  
Spain je desk-critical pro LNG regas capacity, Mediterranean/Atlantic product flows, Gibraltar-adjacent routing, North Africa gas exposure, EU sanctions enforcement and refinery/product export balances.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-ES-ministry_petroleum | ES | — | ministry_petroleum | Ministry for Ecological Transition / Secretary of State for Energy | miteco.gob.es | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-ES-noc | ES | — | noc | — | — | noc | official | production, exports, force_majeure, term_contract, vessel_loading | empty |
| ca-ES-mfa | ES | — | mfa | Ministry of Foreign Affairs Spain | exteriores.gob.es | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-ES-customs_export | ES | — | customs_export | Tax Agency / Customs | sede.agenciatributaria.gob.es | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-ES-upstream_regulator | ES | — | upstream_regulator | CNMC | cnmc.es | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-ES-port_maritime_authority | ES | — | port_maritime_authority | Puertos del Estado | puertos.es | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-ES-national_exchange | ES | — | national_exchange | BME Spanish Exchanges | bolsasymercados.es | exchange | data_feed | pricing_formula | proposed |
| ca-ES-central_bank | ES | — | central_bank | Banco de Espana | bde.es | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-ES-environment_regulator | ES | — | environment_regulator | Ministry for Ecological Transition | miteco.gob.es | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-ES-coast_guard_navy | ES | — | coast_guard_navy | Spanish Navy / Ministry of Defence | defensa.gob.es | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-ES-ministry_petroleum | Primary energy policy and hydrocarbons source. | North Africa gas and EU sanctions context. | Logistics indirect. | proposed |
| ca-ES-port_maritime_authority | Puertos del Estado is central for port/logistics notices. | Gibraltar/Mediterranean logistics relevance. | Direct port/logistics relevance. | proposed |
| ca-ES-upstream_regulator | CNMC supervises energy-market function. | Market and regulatory context. | Less direct for cargoes. | proposed |
| ca-ES-noc | Spain has no direct NOC slot equivalent. | — | — | empty |
| ca-ES-customs_export | Customs source matters for trade enforcement. | Sanctions and EU external-border context. | Exact publication surface needs validation. | unverified |

---

### Unverified / Anti-patterns

- `ca-ES-noc` is `empty`: do not force Repsol/Cepsa/Enagas into a NOC slot.
- `ca-ES-customs_export` and `ca-ES-coast_guard_navy` need path validation before whitelist.
- Spain LNG and product-flow claims need Enagas, port, customs, operator and shipping triangulation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 36,
  "last_country": "ES",
  "crosscheck_cursor": 0,
  "last_batch_seq": 40
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_041_country_authority_PL.md`.
