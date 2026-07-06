# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_084_geo_target_novorossiysk.md  
**Fáze:** geo_target — krok novorossiysk (Fáze 3, Novorossiysk, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `novorossiysk` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_082_geo_target_novorossiysk.md` a zachovává konzervativní statusy: {'proposed': 10, 'unverified': 2}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-novorossiysk-port_authority | RU | novorossiysk | port_authority | Novorossiysk Commercial Sea Port | nvr-port.ru | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-novorossiysk-pipeline_operator | RU | novorossiysk | pipeline_operator | Caspian Pipeline Consortium (CPC) | cpc.ru | infrastructure | official | pipeline_outage,exports | proposed |
| geo-novorossiysk-transit_naval | RU | novorossiysk | transit_naval | Russian Navy (Black Sea Fleet) | structure.mil.ru | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-novorossiysk-loading_terminal | RU | novorossiysk | loading_terminal | CPC / Transneft export terminals | transneft.ru | infrastructure | official | vessel_loading,exports | proposed |
| geo-novorossiysk-national_noc | RU | novorossiysk | national_noc | Rosneft | rosneft.com | noc | official | production,exports,force_majeure | proposed |
| geo-novorossiysk-shipping_lane | RU | novorossiysk | shipping_lane | Rosmorport (Novorossiysk) | rosmorport.ru | shipping | official | vessel_loading,port_closure | proposed |
| geo-novorossiysk-customs_border | RU | novorossiysk | customs_border | Federal Customs Service (FTS) | customs.gov.ru | government_regulator | official | exports,export_license | proposed |
| geo-novorossiysk-insurance_war_risk | US | novorossiysk | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading,sanctions | proposed |
| geo-novorossiysk-storage_operator | RU | novorossiysk | storage_operator | Transneft tank storage | transneft.ru | infrastructure | official | storage_levels,exports | proposed |
| geo-novorossiysk-pricing_hub | RU | novorossiysk | pricing_hub | MOEX (Urals marker) | moex.com | exchange | official | pricing_formula,exports | proposed |
| geo-novorossiysk-weather_hazard | RU | novorossiysk | weather_hazard | Roshydromet | meteoinfo.ru | weather | official | port_closure,hurricane | unverified |
| geo-novorossiysk-sanctions_enforcement | US | novorossiysk | sanctions_enforcement | OFAC (Russian oil price cap) | treasury.gov | government_regulator | official | sanctions,export_license | proposed |

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
  "phase_index": 16,
  "last_geo_target": "novorossiysk",
  "crosscheck_cursor": 0,
  "last_batch_seq": 84
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_085_geo_target_kozmino.md` (Fáze 3, Kozmino).
