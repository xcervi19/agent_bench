# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_023_country_authority_EG.md  
**Fáze:** country_authority — krok EG (Fáze 2, Egypt)  
**Datum:** 2026-07-06  

---

## Shrnutí

Devatenáctá dávka Fáze 2: `EG` × 10 typů autorit podle skeleton dimenze.  
Egypt je desk-critical pro Suez/SUMED logistics, Mediterranean gas, refined-product imports, LNG hub ambitions, payment risk and Red Sea spillover.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-EG-ministry_petroleum | EG | — | ministry_petroleum | Ministry of Petroleum and Mineral Resources | petroleum.gov.eg | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-EG-noc | EG | — | noc | Egyptian General Petroleum Corporation (EGPC) | egpc.com.eg | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-EG-mfa | EG | — | mfa | Ministry of Foreign Affairs Egypt | mfa.gov.eg | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-EG-customs_export | EG | — | customs_export | Egyptian Customs Authority | customs.gov.eg | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-EG-upstream_regulator | EG | — | upstream_regulator | Gas Regulatory Authority | gasreg.org.eg | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-EG-port_maritime_authority | EG | — | port_maritime_authority | Egyptian Authority for Maritime Safety / transport ministry surface | mts.gov.eg | infrastructure | official | vessel_loading, port_closure, exports | unverified |
| ca-EG-national_exchange | EG | — | national_exchange | Egyptian Exchange (EGX) | egx.com.eg | exchange | data_feed | pricing_formula | proposed |
| ca-EG-central_bank | EG | — | central_bank | Central Bank of Egypt | cbe.org.eg | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-EG-environment_regulator | EG | — | environment_regulator | Egyptian Environmental Affairs Agency / Ministry of Environment | eeaa.gov.eg | government_regulator | official | refinery_outage, force_majeure, port_closure | unverified |
| ca-EG-coast_guard_navy | EG | — | coast_guard_navy | Egyptian Navy / Ministry of Defence | mod.gov.eg | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-EG-ministry_petroleum | Primary oil/gas policy source. | Energy hub and payment/fiscal policy context. | Logistics indirect. | proposed |
| ca-EG-noc | EGPC is central for oil-sector operations and imports. | State commercial/policy interface. | Relevant for cargo/import context. | proposed |
| ca-EG-upstream_regulator | Gas regulator matters for market and hub rules. | Regional gas diplomacy context. | Less direct for crude liftings. | proposed |
| ca-EG-port_maritime_authority | Maritime source is important for Suez/ports. | Sovereign infrastructure source. | Exact authority domain/path requires validation. | unverified |
| ca-EG-coast_guard_navy | Naval source matters for Red Sea/East Med security. | Security and sanctions relevance. | Exact public Navy source requires validation. | unverified |

---

### Unverified / Anti-patterns

- `ca-EG-customs_export`, `ca-EG-port_maritime_authority`, `ca-EG-environment_regulator`, and `ca-EG-coast_guard_navy` need manual domain/path validation before whitelist.
- Do not confuse Suez Canal Authority/SUMED operational notices with general petroleum ministry policy; they belong in geo/logistics phases if added separately.
- Cross-check Egyptian supply and transit claims against Suez, port, shipping and company sources before trading use.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 19,
  "last_country": "EG",
  "crosscheck_cursor": 0,
  "last_batch_seq": 23
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_024_country_authority_CN.md`.
