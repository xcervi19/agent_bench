# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_086_geo_target_loop.md  
**Fáze:** geo_target — krok loop (Fáze 3, LOOP, us_gulf_hub)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `loop` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_084_geo_target_loop.md` a zachovává konzervativní statusy: {'proposed': 11, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-loop-port_authority | US | loop | port_authority | LOOP LLC | loopllc.com | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-loop-pipeline_operator | US | loop | pipeline_operator | LOOP pipeline system | loopllc.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-loop-transit_naval | US | loop | transit_naval | US Coast Guard | uscg.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-loop-loading_terminal | US | loop | loading_terminal | LOOP offshore oil port | loopllc.com | infrastructure | official | vessel_loading,exports | proposed |
| geo-loop-national_noc | — | loop | national_noc | (export hub — no NOC) | — | noc | — | exports | empty |
| geo-loop-shipping_lane | US | loop | shipping_lane | LOOP vessel scheduling | loopllc.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-loop-customs_border | US | loop | customs_border | Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports,export_license | proposed |
| geo-loop-insurance_war_risk | US | loop | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-loop-storage_operator | US | loop | storage_operator | LOOP cavern storage | loopllc.com | infrastructure | official | storage_levels,exports | proposed |
| geo-loop-pricing_hub | US | loop | pricing_hub | CME Group (NYMEX WTI / LLS) | cmegroup.com | exchange | official | pricing_formula,storage_levels | proposed |
| geo-loop-weather_hazard | US | loop | weather_hazard | NOAA / NWS (Gulf hurricanes) | weather.gov | weather | official | port_closure,hurricane | proposed |
| geo-loop-sanctions_enforcement | US | loop | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions,export_license | proposed |

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
  "phase_index": 18,
  "last_geo_target": "loop",
  "crosscheck_cursor": 0,
  "last_batch_seq": 86
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_087_geo_target_houston_ship_channel.md` (Fáze 3, Houston Ship Channel).
