# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_099_geo_target_druzhba.md  
**Fáze:** geo_target — krok druzhba (Fáze 3, Druzhba, pipeline_entity)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `druzhba` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_097_geo_target_druzhba.md` a zachovává konzervativní statusy: {'empty': 4, 'proposed': 7, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-druzhba-port_authority | — | druzhba | port_authority | (pipeline system — no port) | — | infrastructure | — | — | empty |
| geo-druzhba-pipeline_operator | RU | druzhba | pipeline_operator | Transneft (Druzhba system) | transneft.ru | infrastructure | official | pipeline_outage,exports | proposed |
| geo-druzhba-transit_naval | — | druzhba | transit_naval | (land pipeline — no naval) | — | government_regulator | — | — | empty |
| geo-druzhba-loading_terminal | RU | druzhba | loading_terminal | Druzhba delivery points (Samara region) | transneft.ru | infrastructure | official | exports,pipeline_outage | proposed |
| geo-druzhba-national_noc | RU | druzhba | national_noc | Rosneft | rosneft.com | noc | official | production,exports,force_majeure | proposed |
| geo-druzhba-shipping_lane | — | druzhba | shipping_lane | (land pipeline — no lane) | — | shipping | — | — | empty |
| geo-druzhba-customs_border | RU | druzhba | customs_border | Federal Customs Service (FTS) | customs.gov.ru | government_regulator | official | exports,export_license | proposed |
| geo-druzhba-insurance_war_risk | — | druzhba | insurance_war_risk | (land pipeline — N/A) | — | shipping | — | — | empty |
| geo-druzhba-storage_operator | RU | druzhba | storage_operator | Transneft tank farms (route) | transneft.ru | infrastructure | official | storage_levels,exports | proposed |
| geo-druzhba-pricing_hub | RU | druzhba | pricing_hub | MOEX (Urals marker) | moex.com | exchange | official | pricing_formula,exports | proposed |
| geo-druzhba-weather_hazard | RU | druzhba | weather_hazard | Roshydromet | meteoinfo.ru | weather | official | pipeline_outage | unverified |
| geo-druzhba-sanctions_enforcement | EU | druzhba | sanctions_enforcement | EU Sanctions (Russian crude embargo) | ec.europa.eu | government_regulator | official | sanctions,export_license | proposed |

---

### Cross-check (3 perspektivy)

- Supply: prioritizovat `loading_terminal`, `pipeline_operator`, `national_noc`, `storage_operator` a fyzické export/import signály.
- Geopolitics: u chokepointů a pipeline sledovat `transit_naval`, `sanctions_enforcement`, `customs_border` a MFA/country authority cross-checky.
- Logistics: port, shipping lane, weather hazard a insurance war-risk zdroje jsou primární pro closure, congestion a vessel-loading signály.

---

### Unverified / Anti-patterns

- `unverified` položky před whitelistem ručně validovat proti oficiálním doménám a aktuální dostupnosti.
- `empty` položky neplnit náhradními komerčními nebo mediálními zdroji, pokud chybí přímý geo-subjekt.
- Market/pricing zdroje nepoužívat jako důkaz fyzického toku bez official/operator/port/shipping triangulace.

---

### Progress po merge (návrh)

```json
{
  "phase": "geo_target",
  "phase_index": 31,
  "last_geo_target": "druzhba",
  "crosscheck_cursor": 0,
  "last_batch_seq": 99
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_100_geo_target_tanap.md` (Fáze 3, TANAP).
