# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_085_geo_target_kozmino.md  
**Fáze:** geo_target — krok kozmino (Fáze 3, Kozmino, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `kozmino` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_083_geo_target_kozmino.md` a zachovává konzervativní statusy: {'proposed': 10, 'unverified': 2}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-kozmino-port_authority | RU | kozmino | port_authority | Transneft — Kozmino port | transneft.ru | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-kozmino-pipeline_operator | RU | kozmino | pipeline_operator | ESPO pipeline (Transneft) | transneft.ru | infrastructure | official | pipeline_outage,exports | proposed |
| geo-kozmino-transit_naval | RU | kozmino | transit_naval | Russian Navy (Pacific Fleet) | structure.mil.ru | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-kozmino-loading_terminal | RU | kozmino | loading_terminal | Kozmino export terminal | transneft.ru | infrastructure | official | vessel_loading,exports | proposed |
| geo-kozmino-national_noc | RU | kozmino | national_noc | Rosneft | rosneft.com | noc | official | production,exports,force_majeure | proposed |
| geo-kozmino-shipping_lane | RU | kozmino | shipping_lane | Rosmorport (Far East) | rosmorport.ru | shipping | official | vessel_loading,port_closure | proposed |
| geo-kozmino-customs_border | RU | kozmino | customs_border | Federal Customs Service (FTS) | customs.gov.ru | government_regulator | official | exports,export_license | proposed |
| geo-kozmino-insurance_war_risk | US | kozmino | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading,sanctions | proposed |
| geo-kozmino-storage_operator | RU | kozmino | storage_operator | Kozmino tank storage | transneft.ru | infrastructure | official | storage_levels,exports | proposed |
| geo-kozmino-pricing_hub | RU | kozmino | pricing_hub | MOEX (ESPO blend marker) | moex.com | exchange | official | pricing_formula,exports | proposed |
| geo-kozmino-weather_hazard | RU | kozmino | weather_hazard | Roshydromet | meteoinfo.ru | weather | official | port_closure,hurricane | unverified |
| geo-kozmino-sanctions_enforcement | US | kozmino | sanctions_enforcement | OFAC (Russian oil price cap) | treasury.gov | government_regulator | official | sanctions,export_license | proposed |

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
  "phase_index": 17,
  "last_geo_target": "kozmino",
  "crosscheck_cursor": 0,
  "last_batch_seq": 85
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_086_geo_target_loop.md` (Fáze 3, LOOP).
