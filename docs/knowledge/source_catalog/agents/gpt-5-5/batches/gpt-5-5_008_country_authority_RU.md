# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_008_country_authority_RU.md  
**Fáze:** country_authority — krok RU (Fáze 2, Russia)  
**Datum:** 2026-07-05  

---

## Shrnutí

Čtvrtá dávka Fáze 2: `RU` × 10 typů autorit podle skeleton dimenze.
Russia je desk-critical pro crude/products exports, sanctions, Black Sea/Baltic/Arctic logistics, pipeline politics a price-cap enforcement.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-RU-ministry_petroleum | RU | — | ministry_petroleum | Ministry of Energy of the Russian Federation | minenergo.gov.ru | government_regulator | official | production, exports, sanctions, quota_rhetoric | proposed |
| ca-RU-noc | RU | — | noc | Rosneft | rosneft.com | noc | official | production, exports, force_majeure, term_contract | unverified |
| ca-RU-mfa | RU | — | mfa | Ministry of Foreign Affairs of Russia | mid.ru | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-RU-customs_export | RU | — | customs_export | Federal Customs Service of Russia | customs.gov.ru | government_regulator | official | exports, imports, export_license, sanctions | proposed |
| ca-RU-upstream_regulator | RU | — | upstream_regulator | Federal Agency for Mineral Resources (Rosnedra) | rosnedra.gov.ru | government_regulator | official | production, export_license, force_majeure | proposed |
| ca-RU-port_maritime_authority | RU | novorossiysk | port_maritime_authority | Federal Agency for Sea and River Transport (Rosmorrechflot) | morflot.gov.ru | infrastructure | official | vessel_loading, port_closure, exports | proposed |
| ca-RU-national_exchange | RU | — | national_exchange | SPIMEX | spimex.com | exchange | data_feed | pricing_formula, exports, sanctions | proposed |
| ca-RU-central_bank | RU | — | central_bank | Bank of Russia | cbr.ru | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-RU-environment_regulator | RU | — | environment_regulator | Rosprirodnadzor | rpn.gov.ru | government_regulator | official | refinery_outage, force_majeure, port_closure | proposed |
| ca-RU-coast_guard_navy | RU | — | coast_guard_navy | Russian Ministry of Defence / Navy | mil.ru | government_regulator | official | port_closure, vessel_loading, sanctions | unverified |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-RU-ministry_petroleum | Primary energy policy and production/export signal. | Direct sanctions and OPEC+ rhetoric channel. | Logistics indirect. | proposed |
| ca-RU-noc | Rosneft is a state-controlled oil champion, but not a sole national oil company. | Sanctions-sensitive entity. | Relevant for export and project operations. | unverified |
| ca-RU-upstream_regulator | Subsoil licensing and mineral resource oversight. | Regulatory signal under state control. | Indirect logistics impact. | proposed |
| ca-RU-port_maritime_authority | Maritime/port federal authority. | Sovereign transport infrastructure source. | Direct Black Sea/Baltic/Arctic port relevance. | proposed |
| ca-RU-coast_guard_navy | Navy/defense source matters for maritime security. | Direct escalation/sanctions security relevance. | Public Navy-specific source should be narrowed before whitelist. | unverified |

---

### Unverified / Anti-patterns

- `ca-RU-noc` is `unverified`: Russia has several state-linked oil companies; Rosneft is the main state-controlled champion, not a clean single NOC equivalent.
- `ca-RU-coast_guard_navy` is `unverified`: use exact Navy / Border Guard path if a stable official path is confirmed before whitelist.
- `SPIMEX` is useful for pricing and product market data, not direct physical export confirmation.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 4,
  "last_country": "RU",
  "crosscheck_cursor": 0,
  "last_batch_seq": 8
}
```

Po merge této dávky → další pending dávka v této sérii: `gpt-5-5_009_country_authority_US.md`.
