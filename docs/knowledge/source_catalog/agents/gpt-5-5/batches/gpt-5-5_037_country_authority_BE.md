# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_037_country_authority_BE.md  
**Fáze:** country_authority — krok BE (Fáze 2, Belgium)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá třetí dávka Fáze 2: `BE` × 10 typů autorit podle skeleton dimenze.  
Belgium je desk-critical pro Antwerp-Bruges refining/petrochem logistics, EU sanctions enforcement, petroleum product price regulation, strategic stocks, North Sea maritime coordination and eurozone financial context.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-BE-ministry_petroleum | BE | — | ministry_petroleum | FPS Economy - Directorate-General for Energy / Petroleum | economie.fgov.be | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-BE-noc | BE | — | noc | — | — | noc | official | production, exports, force_majeure, term_contract, vessel_loading | empty |
| ca-BE-mfa | BE | — | mfa | FPS Foreign Affairs, Foreign Trade and Development Cooperation | diplomatie.belgium.be | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-BE-customs_export | BE | — | customs_export | General Administration of Customs and Excise | fin.belgium.be | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-BE-upstream_regulator | BE | — | upstream_regulator | FPS Economy - Directorate-General for Energy | economie.fgov.be | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-BE-port_maritime_authority | BE | — | port_maritime_authority | Port of Antwerp-Bruges | portofantwerpbruges.com | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-BE-national_exchange | BE | — | national_exchange | Euronext Brussels | euronext.com | exchange | data_feed | pricing_formula | proposed |
| ca-BE-central_bank | BE | — | central_bank | National Bank of Belgium | nbb.be | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-BE-environment_regulator | BE | — | environment_regulator | FPS Public Health / Marine Environment | health.belgium.be | government_regulator | official | refinery_outage, force_majeure, port_closure | unverified |
| ca-BE-coast_guard_navy | BE | — | coast_guard_navy | Belgian Coast Guard | kustwacht.be | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-BE-ministry_petroleum | FPS Economy covers petroleum pricing, energy policy and strategic stocks. | EU sanctions and energy-security context. | Logistics indirect. | proposed |
| ca-BE-customs_export | Customs/Excise is relevant for EU external-border enforcement. | Sanctions and product-routing context. | Trade-flow relevance. | proposed |
| ca-BE-port_maritime_authority | Antwerp-Bruges is critical for products/refining/petrochem logistics. | EU trade and sanctions-route relevance. | Direct logistics relevance. | proposed |
| ca-BE-noc | Belgium has no direct NOC equivalent. | — | — | empty |
| ca-BE-environment_regulator | Marine environment surface is relevant but exact authority path should be validated. | North Sea incident context. | Domain/path needs validation before whitelist. | unverified |

---

### Unverified / Anti-patterns

- `ca-BE-noc` is `empty`: do not force private refiners or port operators into a national oil company slot.
- `ca-BE-environment_regulator` is `unverified`: validate the exact marine/environment authority path before whitelist.
- Port of Antwerp-Bruges is a logistics anchor, but refinery/product disruptions need operator, customs and shipping cross-checks before trading use.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 33,
  "last_country": "BE",
  "crosscheck_cursor": 0,
  "last_batch_seq": 37
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_038_country_authority_IT.md` (Fáze 2, Italy autority).
