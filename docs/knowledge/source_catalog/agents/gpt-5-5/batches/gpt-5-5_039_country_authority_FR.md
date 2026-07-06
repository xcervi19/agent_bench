# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_039_country_authority_FR.md  
**Fáze:** country_authority — krok FR (Fáze 2, France)  
**Datum:** 2026-07-06  

---

## Shrnutí

Třicátá pátá dávka Fáze 2: `FR` × 10 typů autorit podle skeleton dimenze.  
France je desk-critical pro European refining/product flows, strategic stocks, sanctions policy, Mediterranean/Atlantic logistics, nuclear/electricity substitution effects and eurozone financial context.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-FR-ministry_petroleum | FR | — | ministry_petroleum | Ministry for Ecological Transition / DGEC | ecologie.gouv.fr | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-FR-noc | FR | — | noc | — | — | noc | official | production, exports, force_majeure, term_contract, vessel_loading | empty |
| ca-FR-mfa | FR | — | mfa | Ministry for Europe and Foreign Affairs | diplomatie.gouv.fr | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-FR-customs_export | FR | — | customs_export | French Customs | douane.gouv.fr | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-FR-upstream_regulator | FR | — | upstream_regulator | Commission de Regulation de l'Energie (CRE) | cre.fr | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-FR-port_maritime_authority | FR | — | port_maritime_authority | Ministry of the Sea / maritime portal | mer.gouv.fr | infrastructure | official | vessel_loading, port_closure, exports, imports | unverified |
| ca-FR-national_exchange | FR | — | national_exchange | Euronext Paris | euronext.com | exchange | data_feed | pricing_formula | proposed |
| ca-FR-central_bank | FR | — | central_bank | Banque de France | banque-france.fr | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-FR-environment_regulator | FR | — | environment_regulator | Ministry for Ecological Transition | ecologie.gouv.fr | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-FR-coast_guard_navy | FR | — | coast_guard_navy | French Navy / maritime prefectures | defense.gouv.fr | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-FR-ministry_petroleum | Primary energy policy and security source. | EU sanctions and supply-security context. | Logistics indirect. | proposed |
| ca-FR-customs_export | Customs is relevant for sanctions and trade enforcement. | EU external enforcement context. | Trade-flow relevance. | proposed |
| ca-FR-port_maritime_authority | Maritime surface matters for ports and sea incidents. | Atlantic/Mediterranean logistics relevance. | Exact canonical path needs validation. | unverified |
| ca-FR-noc | France has no direct NOC slot equivalent. | — | — | empty |
| ca-FR-coast_guard_navy | Navy/maritime prefecture source matters for security. | Security relevance. | Exact publication path needs validation. | unverified |

---

### Unverified / Anti-patterns

- `ca-FR-noc` is `empty`: do not force TotalEnergies into a national oil company slot.
- `ca-FR-port_maritime_authority` and `ca-FR-coast_guard_navy` require path validation before whitelist.
- French refinery and product-flow claims need operator, customs, port and shipping cross-checks.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 35,
  "last_country": "FR",
  "crosscheck_cursor": 0,
  "last_batch_seq": 39
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_040_country_authority_ES.md`.
