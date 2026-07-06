# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_095_geo_target_cushing.md  
**Fáze:** geo_target — krok cushing (Fáze 3, Cushing, storage_pricing_hub)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `cushing` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_093_geo_target_cushing.md` a zachovává konzervativní statusy: {'empty': 6, 'proposed': 5, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-cushing-port_authority | — | cushing | port_authority | (inland hub — no port) | — | infrastructure | — | — | empty |
| geo-cushing-pipeline_operator | US | cushing | pipeline_operator | Enterprise Products (Cushing interconnect) | enterpriseproducts.com | infrastructure | official | pipeline_outage,storage_levels | proposed |
| geo-cushing-transit_naval | — | cushing | transit_naval | (inland — no naval) | — | government_regulator | — | — | empty |
| geo-cushing-loading_terminal | US | cushing | loading_terminal | Cushing tank farm terminals | enterpriseproducts.com | infrastructure | official | storage_levels,exports | unverified |
| geo-cushing-national_noc | — | cushing | national_noc | (storage hub — no NOC) | — | noc | — | storage_levels | empty |
| geo-cushing-shipping_lane | — | cushing | shipping_lane | (inland — no shipping lane) | — | shipping | — | — | empty |
| geo-cushing-customs_border | — | cushing | customs_border | (inland pipeline hub) | — | government_regulator | — | — | empty |
| geo-cushing-insurance_war_risk | — | cushing | insurance_war_risk | (inland — N/A) | — | shipping | — | — | empty |
| geo-cushing-storage_operator | US | cushing | storage_operator | EIA Cushing weekly stocks | eia.gov | government_regulator | official | storage_levels | proposed |
| geo-cushing-pricing_hub | US | cushing | pricing_hub | CME Group (WTI delivery point) | cmegroup.com | exchange | official | pricing_formula,storage_levels | proposed |
| geo-cushing-weather_hazard | US | cushing | weather_hazard | NOAA / NWS Oklahoma | weather.gov | weather | official | pipeline_outage | proposed |
| geo-cushing-sanctions_enforcement | US | cushing | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions | proposed |

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
  "phase_index": 27,
  "last_geo_target": "cushing",
  "crosscheck_cursor": 0,
  "last_batch_seq": 95
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_096_geo_target_ara.md` (Fáze 3, ARA).
