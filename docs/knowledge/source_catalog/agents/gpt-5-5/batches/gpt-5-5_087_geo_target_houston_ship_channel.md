# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_087_geo_target_houston_ship_channel.md  
**Fáze:** geo_target — krok houston_ship_channel (Fáze 3, Houston Ship Channel, us_gulf_hub)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `houston_ship_channel` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_085_geo_target_houston_ship_channel.md` a zachovává konzervativní statusy: {'proposed': 10, 'unverified': 1, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-houston_ship_channel-port_authority | US | houston_ship_channel | port_authority | Port Houston | porthouston.com | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-houston_ship_channel-pipeline_operator | US | houston_ship_channel | pipeline_operator | Enterprise Products (Gulf Coast hub) | enterpriseproducts.com | infrastructure | official | pipeline_outage,exports | unverified |
| geo-houston_ship_channel-transit_naval | US | houston_ship_channel | transit_naval | US Coast Guard (Sector Houston-Galveston) | uscg.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-houston_ship_channel-loading_terminal | US | houston_ship_channel | loading_terminal | Houston Ship Channel export terminals | porthouston.com | infrastructure | official | vessel_loading,exports,refinery_outage | proposed |
| geo-houston_ship_channel-national_noc | — | houston_ship_channel | national_noc | (no NOC — private operators) | — | noc | — | exports | empty |
| geo-houston_ship_channel-shipping_lane | US | houston_ship_channel | shipping_lane | Port Houston VTS / traffic | porthouston.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-houston_ship_channel-customs_border | US | houston_ship_channel | customs_border | Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports,export_license | proposed |
| geo-houston_ship_channel-insurance_war_risk | US | houston_ship_channel | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-houston_ship_channel-storage_operator | US | houston_ship_channel | storage_operator | EIA Gulf Coast storage data | eia.gov | government_regulator | official | storage_levels,exports | proposed |
| geo-houston_ship_channel-pricing_hub | US | houston_ship_channel | pricing_hub | CME Group (WTI / Gulf Coast diff) | cmegroup.com | exchange | official | pricing_formula,exports | proposed |
| geo-houston_ship_channel-weather_hazard | US | houston_ship_channel | weather_hazard | NOAA / NWS Houston | weather.gov | weather | official | port_closure,hurricane,refinery_outage | proposed |
| geo-houston_ship_channel-sanctions_enforcement | US | houston_ship_channel | sanctions_enforcement | BIS / OFAC (export controls) | commerce.gov | government_regulator | official | sanctions,export_license | proposed |

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
  "phase_index": 19,
  "last_geo_target": "houston_ship_channel",
  "crosscheck_cursor": 0,
  "last_batch_seq": 87
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_088_geo_target_sabine_pass.md` (Fáze 3, Sabine Pass).
