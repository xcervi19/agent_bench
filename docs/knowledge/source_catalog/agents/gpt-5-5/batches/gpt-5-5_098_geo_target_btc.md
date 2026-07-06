# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_098_geo_target_btc.md  
**Fáze:** geo_target — krok btc (Fáze 3, BTC, pipeline_entity)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `btc` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_096_geo_target_btc.md` a zachovává konzervativní statusy: {'proposed': 10, 'unverified': 2}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-btc-port_authority | TR | btc | port_authority | BOTAŞ — Ceyhan Marine Terminal | botas.gov.tr | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-btc-pipeline_operator | AZ | btc | pipeline_operator | BTC Pipeline (Caspian Pipeline) | caspianpipeline.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-btc-transit_naval | TR | btc | transit_naval | Turkish Naval Forces | deniz.kuvvetleri.tsk.tr | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-btc-loading_terminal | TR | btc | loading_terminal | Ceyhan export terminal | botas.gov.tr | infrastructure | official | vessel_loading,exports | proposed |
| geo-btc-national_noc | AZ | btc | national_noc | SOCAR | socar.az | noc | official | production,exports,force_majeure | proposed |
| geo-btc-shipping_lane | TR | btc | shipping_lane | Turkish Straits VTS (Ceyhan approach) | uab.gov.tr | shipping | official | vessel_loading,port_closure | proposed |
| geo-btc-customs_border | AZ | btc | customs_border | State Customs Committee (Azerbaijan) | customs.gov.az | government_regulator | official | exports,export_license | proposed |
| geo-btc-insurance_war_risk | US | btc | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading | proposed |
| geo-btc-storage_operator | TR | btc | storage_operator | Ceyhan tank storage | botas.gov.tr | infrastructure | official | storage_levels,exports | proposed |
| geo-btc-pricing_hub | TR | btc | pricing_hub | Borsa Istanbul | borsaistanbul.com | exchange | official | pricing_formula,exports | unverified |
| geo-btc-weather_hazard | TR | btc | weather_hazard | Turkish State Meteorological Service | mgm.gov.tr | weather | official | port_closure,pipeline_outage | proposed |
| geo-btc-sanctions_enforcement | US | btc | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions,export_license | proposed |

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
  "phase_index": 30,
  "last_geo_target": "btc",
  "crosscheck_cursor": 0,
  "last_batch_seq": 98
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_099_geo_target_druzhba.md` (Fáze 3, Druzhba).
