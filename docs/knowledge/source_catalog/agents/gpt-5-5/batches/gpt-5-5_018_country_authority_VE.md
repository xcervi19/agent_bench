# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_018_country_authority_VE.md  
**Fáze:** country_authority — krok VE (Fáze 2, Venezuela)  
**Datum:** 2026-07-05  

---

## Shrnutí

Čtrnáctá dávka Fáze 2: `VE` × 10 typů autorit podle skeleton dimenze.
Venezuela je desk-critical pro sanctions, PDVSA exports, Orinoco production, Caribbean logistics, opaque tanker flows a license/risk reversals.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-VE-ministry_petroleum | VE | — | ministry_petroleum | Ministry of Petroleum of Venezuela | minpet.gob.ve | government_regulator | official | production, exports, sanctions, quota_rhetoric | unverified |
| ca-VE-noc | VE | — | noc | PDVSA | pdvsa.com | noc | official | production, exports, force_majeure, term_contract, vessel_loading | proposed |
| ca-VE-mfa | VE | — | mfa | Ministry of Foreign Affairs of Venezuela (MPPRE) | mppre.gob.ve | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-VE-customs_export | VE | — | customs_export | SENIAT | seniat.gob.ve | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-VE-upstream_regulator | VE | — | upstream_regulator | Ministry of Petroleum of Venezuela | minpet.gob.ve | government_regulator | official | production, force_majeure, sanctions | unverified |
| ca-VE-port_maritime_authority | VE | — | port_maritime_authority | INEA | inea.gob.ve | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-VE-national_exchange | VE | — | national_exchange | Bolsa de Valores de Caracas | bolsadecaracas.com | exchange | data_feed | pricing_formula | unverified |
| ca-VE-central_bank | VE | — | central_bank | Central Bank of Venezuela | bcv.org.ve | government_regulator | official | sanctions, pricing_formula, imports, exports | unverified |
| ca-VE-environment_regulator | VE | — | environment_regulator | Ministry of Ecosocialism (MINEC) | minec.gob.ve | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-VE-coast_guard_navy | VE | — | coast_guard_navy | Venezuelan Navy / Ministry of Defense | milicia.mil.ve | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-VE-noc | PDVSA is direct operational source for production/export context. | Sanctions-sensitive state entity. | Direct tanker/export relevance. | proposed |
| ca-VE-mfa | Not a supply source. | Primary diplomatic/sanctions rhetoric channel. | Logistics indirect. | proposed |
| ca-VE-port_maritime_authority | INEA publishes aquatic/maritime notices. | Sovereign maritime authority. | Direct navigation and port signal. | proposed |
| ca-VE-ministry_petroleum | Relevant sovereign oil source. | Sanctions and production policy signal. | Domain requires confirmation before whitelist. | unverified |
| ca-VE-coast_guard_navy | Maritime security source would be useful. | Security/sanctions relevance. | Exact stable Navy source needs validation. | unverified |

---

### Unverified / Anti-patterns

- Several Venezuelan government domains require manual validation before whitelist because official web presence can be fragmented or intermittently available.
- `PDVSA` is a primary NOC source, but export confirmation still needs cross-checking with maritime/port/AIS and sanctions-license context.
- Do not use secondary sanctions databases as primary anchors; use them only for validation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 14,
  "last_country": "VE",
  "crosscheck_cursor": 0,
  "last_batch_seq": 18
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_019_country_authority_NG.md`.
