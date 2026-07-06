# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_010_country_authority_AE.md  
**Fáze:** country_authority — krok AE (Fáze 2, UAE)  
**Datum:** 2026-07-05  

---

## Shrnutí

Šestá dávka Fáze 2: `AE` × 10 typů autorit podle skeleton dimenze.
UAE je desk-critical pro Murban, ADNOC exports, Fujairah storage/bunkers, Jebel Ali logistics, Hormuz-adjacent risk a sanctions/transshipment screening.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-AE-ministry_petroleum | AE | — | ministry_petroleum | UAE Ministry of Energy and Infrastructure | moei.gov.ae | government_regulator | official | production, exports, imports, quota_rhetoric | proposed |
| ca-AE-noc | AE | fujairah | noc | ADNOC | adnoc.ae | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-AE-mfa | AE | — | mfa | UAE Ministry of Foreign Affairs | mofa.gov.ae | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-AE-customs_export | AE | — | customs_export | Federal Authority for Identity, Citizenship, Customs & Port Security (ICP) | icp.gov.ae | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-AE-upstream_regulator | AE | — | upstream_regulator | Abu Dhabi Department of Energy | doe.gov.ae | government_regulator | official | production, force_majeure, export_license | unverified |
| ca-AE-port_maritime_authority | AE | jebel_ali | port_maritime_authority | AD Ports Group | adportsgroup.com | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-AE-national_exchange | AE | — | national_exchange | Securities and Commodities Authority (SCA) | sca.gov.ae | exchange | data_feed | pricing_formula | proposed |
| ca-AE-central_bank | AE | — | central_bank | Central Bank of the UAE | centralbank.ae | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-AE-environment_regulator | AE | — | environment_regulator | Ministry of Climate Change and Environment | moccae.gov.ae | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-AE-coast_guard_navy | AE | hormuz | coast_guard_navy | UAE Ministry of Defence / Navy | mod.gov.ae | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AE-ministry_petroleum | Federal energy/infrastructure policy signal. | OPEC+ and regional energy diplomacy context. | Maritime/infrastructure remit helps logistics context. | proposed |
| ca-AE-noc | Direct operator for production, Murban and export projects. | State-owned strategic entity. | Direct terminal/export relevance. | proposed |
| ca-AE-customs_export | Customs and port-security authority. | Sanctions/transshipment enforcement relevance. | Direct clearance and port-security signal. | proposed |
| ca-AE-upstream_regulator | Abu Dhabi-level regulator is relevant but not a single federal upstream regulator. | Emirate-level energy governance. | Indirect logistics relevance. | unverified |
| ca-AE-port_maritime_authority | Operator/infrastructure source, not a sovereign ministry. | Strategic port and corridor relevance. | Direct port/logistics signal. | proposed |
| ca-AE-coast_guard_navy | Defense/navy source matters for Gulf security. | Direct maritime escalation relevance. | Need exact stable Navy/coast guard path before whitelist. | unverified |

---

### Unverified / Anti-patterns

- `ca-AE-upstream_regulator` is `unverified`: UAE upstream authority is emirate-level, especially Abu Dhabi; confirm exact regulator path before whitelist.
- `ca-AE-port_maritime_authority` uses an operator/infrastructure group; do not treat it as sovereign confirmation without MOEI/ICP cross-check.
- `ca-AE-coast_guard_navy` is `unverified`: confirm exact official naval/coast guard source path before whitelist.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 6,
  "last_country": "AE",
  "crosscheck_cursor": 0,
  "last_batch_seq": 10
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_011_country_authority_KW.md`.
