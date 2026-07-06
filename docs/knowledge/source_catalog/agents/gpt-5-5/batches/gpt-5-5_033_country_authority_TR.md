# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_033_country_authority_TR.md  
**Fáze:** country_authority — krok TR (Fáze 2, Turkey)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá devátá dávka Fáze 2: `TR` × 10 typů autorit podle skeleton dimenze.  
Turkey je desk-critical pro Bospor/Dardanelles transit, Black Sea gas, Ceyhan/BTC logistics, sanctions-routing, Russian flows, refinery/product trade and East Med/Black Sea security.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TR-ministry_petroleum | TR | — | ministry_petroleum | Ministry of Energy and Natural Resources | enerji.gov.tr | government_regulator | official | production, imports, exports, quota_rhetoric | proposed |
| ca-TR-noc | TR | — | noc | Turkiye Petrolleri A.O. (TPAO) | tpao.gov.tr | noc | official | production, force_majeure, term_contract, vessel_loading | proposed |
| ca-TR-mfa | TR | — | mfa | Ministry of Foreign Affairs Turkiye | mfa.gov.tr | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-TR-customs_export | TR | — | customs_export | Ministry of Trade / Customs | ticaret.gov.tr | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-TR-upstream_regulator | TR | — | upstream_regulator | Energy Market Regulatory Authority (EMRA/EPDK) | epdk.gov.tr | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-TR-port_maritime_authority | TR | — | port_maritime_authority | Directorate General for Maritime Affairs | denizcilik.uab.gov.tr | infrastructure | official | vessel_loading, port_closure, exports, imports | proposed |
| ca-TR-national_exchange | TR | — | national_exchange | Borsa Istanbul | borsaistanbul.com | exchange | data_feed | pricing_formula | proposed |
| ca-TR-central_bank | TR | — | central_bank | Central Bank of the Republic of Turkiye | tcmb.gov.tr | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-TR-environment_regulator | TR | — | environment_regulator | Ministry of Environment, Urbanization and Climate Change | cskb.gov.tr | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-TR-coast_guard_navy | TR | — | coast_guard_navy | Turkish Coast Guard Command | sg.gov.tr | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TR-ministry_petroleum | Primary energy policy source. | Russian flows, Black Sea and East Med policy relevance. | Logistics indirect. | proposed |
| ca-TR-noc | TPAO is the upstream NOC anchor. | Black Sea gas and regional projects relevance. | Less direct for transit than maritime/port sources. | proposed |
| ca-TR-port_maritime_authority | Maritime authority is central for Bospor/Dardanelles and port notices. | Sovereign logistics chokepoint source. | Direct transit/logistics relevance. | proposed |
| ca-TR-coast_guard_navy | Coast Guard matters for Black Sea/East Med security. | Sanctions/security relevance. | Security signal, not cargo confirmation alone. | proposed |
| ca-TR-customs_export | Trade/customs source is relevant but path needs validation. | Sanctions-routing context. | Trade-flow relevance. | unverified |

---

### Unverified / Anti-patterns

- `ca-TR-customs_export` is `unverified`: validate the exact customs publication surface before whitelist.
- Do not treat Borsa Istanbul or lira moves as physical oil/gas evidence without ministry, customs, port or shipping confirmation.
- Bospor transit belongs in geo/logistics phases; Turkey authority slots should anchor official context and cross-checks.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 29,
  "last_country": "TR",
  "crosscheck_cursor": 0,
  "last_batch_seq": 33
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_034_country_authority_GB.md`.
