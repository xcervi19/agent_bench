# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_094_geo_target_cove_point.md  
**Fáze:** geo_target — krok cove_point (Fáze 3, Cove Point LNG, lng_terminal)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `cove_point` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_092_geo_target_cove_point.md` a zachovává konzervativní statusy: {'proposed': 9, 'empty': 2, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-cove_point-port_authority | US | cove_point | port_authority | Maryland Port Administration | maryland.gov | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-cove_point-pipeline_operator | US | cove_point | pipeline_operator | Dominion Energy Cove Point feedgas | dominionenergy.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-cove_point-transit_naval | US | cove_point | transit_naval | US Coast Guard | uscg.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-cove_point-loading_terminal | US | cove_point | loading_terminal | Cove Point LNG (Dominion Energy) | dominionenergy.com | infrastructure | official | vessel_loading,exports,force_majeure | proposed |
| geo-cove_point-national_noc | — | cove_point | national_noc | (LNG export — no NOC) | — | noc | — | exports | empty |
| geo-cove_point-shipping_lane | US | cove_point | shipping_lane | Chesapeake Bay LNG transit | dominionenergy.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-cove_point-customs_border | US | cove_point | customs_border | Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports,export_license | proposed |
| geo-cove_point-insurance_war_risk | US | cove_point | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-cove_point-storage_operator | — | cove_point | storage_operator | (LNG — no crude storage) | — | infrastructure | — | — | empty |
| geo-cove_point-pricing_hub | US | cove_point | pricing_hub | CME Group (Henry Hub / LNG linkage) | cmegroup.com | exchange | official | pricing_formula,exports | unverified |
| geo-cove_point-weather_hazard | US | cove_point | weather_hazard | NOAA / NWS (Atlantic storms) | weather.gov | weather | official | port_closure,hurricane | proposed |
| geo-cove_point-sanctions_enforcement | US | cove_point | sanctions_enforcement | FERC (LNG export authorization) | ferc.gov | government_regulator | official | export_license,sanctions | proposed |

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
  "phase_index": 26,
  "last_geo_target": "cove_point",
  "crosscheck_cursor": 0,
  "last_batch_seq": 94
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_095_geo_target_cushing.md` (Fáze 3, Cushing).
