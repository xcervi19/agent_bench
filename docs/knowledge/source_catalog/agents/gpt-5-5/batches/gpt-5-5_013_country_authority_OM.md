# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_013_country_authority_OM.md  
**Fáze:** country_authority — krok OM (Fáze 2, Oman)  
**Datum:** 2026-07-05  

---

## Shrnutí

Devátá dávka Fáze 2: `OM` × 10 typů autorit podle skeleton dimenze.
Oman je desk-relevant pro Hormuz-adjacent logistics, Oman Blend pricing, Duqm/Sohar/Salalah corridors, LNG exports a Gulf/Arabian Sea weather/security risk.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-OM-ministry_petroleum | OM | — | ministry_petroleum | Oman Ministry of Energy and Minerals | mem.gov.om | government_regulator | official | production, exports, quota_rhetoric, term_contract | proposed |
| ca-OM-noc | OM | — | noc | OQ | oq.com | noc | official | production, exports, force_majeure, term_contract | proposed |
| ca-OM-mfa | OM | — | mfa | Oman Ministry of Foreign Affairs | mofa.gov.om | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-OM-customs_export | OM | — | customs_export | Royal Oman Police Customs | rop.gov.om | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-OM-upstream_regulator | OM | — | upstream_regulator | Oman Ministry of Energy and Minerals | mem.gov.om | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-OM-port_maritime_authority | OM | — | port_maritime_authority | ASYAD Group | asyad.om | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-OM-national_exchange | OM | — | national_exchange | Muscat Stock Exchange | msx.om | exchange | data_feed | pricing_formula | proposed |
| ca-OM-central_bank | OM | — | central_bank | Central Bank of Oman | cbo.gov.om | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-OM-environment_regulator | OM | — | environment_regulator | Environment Authority Oman | ea.gov.om | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-OM-coast_guard_navy | OM | — | coast_guard_navy | Royal Oman Police Coast Guard | rop.gov.om | government_regulator | official | port_closure, vessel_loading, sanctions | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-OM-ministry_petroleum | Primary policy and production/export source. | OPEC+ and Gulf energy policy context. | Logistics indirect. | proposed |
| ca-OM-noc | Integrated state energy company source. | Strategic state energy entity. | Relevant to upstream/downstream operations. | proposed |
| ca-OM-customs_export | Customs likely under Royal Oman Police. | Sanctions/export enforcement relevance. | Direct clearance signal, but exact customs path should be narrowed. | unverified |
| ca-OM-port_maritime_authority | ASYAD covers logistics and port corridor operations. | State logistics/infrastructure relevance. | Direct port/logistics signal. | proposed |
| ca-OM-coast_guard_navy | ROP coast guard source. | Maritime security relevance. | Direct Arabian Sea/Gulf of Oman movement relevance. | proposed |

---

### Unverified / Anti-patterns

- `ca-OM-customs_export` is `unverified`: confirm exact ROP Customs path before whitelist.
- `ASYAD` is logistics/operator coverage; cross-check terminal-specific issues with port/operator notices.
- `OQ` is the state energy group, but Oman LNG may be needed as a separate LNG playbook/geo source.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 9,
  "last_country": "OM",
  "crosscheck_cursor": 0,
  "last_batch_seq": 13
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_014_country_authority_NO.md`.
