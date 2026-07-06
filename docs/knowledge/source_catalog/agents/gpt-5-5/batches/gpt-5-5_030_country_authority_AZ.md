# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_030_country_authority_AZ.md  
**Fáze:** country_authority — krok AZ (Fáze 2, Azerbaijan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá šestá dávka Fáze 2: `AZ` × 10 typů autorit podle skeleton dimenze.  
Azerbaijan je desk-critical pro Azeri Light, BTC/South Caucasus corridor, SOCAR exports, Caspian logistics, Armenia/Iran/Russia geopolitical risk and Middle Corridor chokepoints.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-AZ-ministry_petroleum | AZ | — | ministry_petroleum | Ministry of Energy of Azerbaijan | minenergy.gov.az | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-AZ-noc | AZ | — | noc | SOCAR | socar.az | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-AZ-mfa | AZ | — | mfa | Ministry of Foreign Affairs Azerbaijan | mfa.gov.az | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-AZ-customs_export | AZ | — | customs_export | State Customs Committee | customs.gov.az | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-AZ-upstream_regulator | AZ | — | upstream_regulator | Azerbaijan Energy Regulatory Agency (AERA) | regulator.gov.az | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-AZ-port_maritime_authority | AZ | — | port_maritime_authority | Port of Baku | portofbaku.com | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-AZ-national_exchange | AZ | — | national_exchange | Baku Stock Exchange | bfb.az | exchange | data_feed | pricing_formula | unverified |
| ca-AZ-central_bank | AZ | — | central_bank | Central Bank of Azerbaijan | cbar.az | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-AZ-environment_regulator | AZ | — | environment_regulator | Ministry of Ecology and Natural Resources | eco.gov.az | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-AZ-coast_guard_navy | AZ | — | coast_guard_navy | State Border Service / Coast Guard | dsx.gov.az | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AZ-ministry_petroleum | Primary official energy policy source. | OPEC+ and regional corridor context. | Logistics indirect. | proposed |
| ca-AZ-noc | SOCAR is core NOC/operator source. | Strategic actor in Caspian/BTC corridor. | Direct export and cargo relevance. | proposed |
| ca-AZ-customs_export | Customs source supports trade-control checks. | Sanctions and regional trade relevance. | Trade-flow relevance. | proposed |
| ca-AZ-port_maritime_authority | Port of Baku is key Caspian/Middle Corridor source. | Corridor and sanctions-route relevance. | Direct port/logistics signal. | proposed |
| ca-AZ-national_exchange | Exchange domain needs confirmation. | Limited geopolitical value. | Not physical flow confirmation. | unverified |

---

### Unverified / Anti-patterns

- `ca-AZ-national_exchange` is `unverified`: validate the Baku Stock Exchange canonical domain before whitelist.
- Do not use Port of Baku notices as a substitute for BTC or SOCAR export confirmation; use them as logistics cross-checks.
- Regional conflict or sanctions claims need MFA, SOCAR/customs and logistics triangulation before trading use.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 26,
  "last_country": "AZ",
  "crosscheck_cursor": 0,
  "last_batch_seq": 30
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_031_country_authority_TM.md`.
