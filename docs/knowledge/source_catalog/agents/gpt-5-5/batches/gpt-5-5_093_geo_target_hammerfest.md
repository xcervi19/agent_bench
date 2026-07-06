# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_093_geo_target_hammerfest.md  
**Fáze:** geo_target — krok hammerfest (Fáze 3, Hammerfest LNG, lng_terminal)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `hammerfest` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_091_geo_target_hammerfest.md` a zachovává konzervativní statusy: {'proposed': 10, 'unverified': 1, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-hammerfest-port_authority | NO | hammerfest | port_authority | Norwegian Coastal Administration (Kystverket) | kystverket.no | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-hammerfest-pipeline_operator | NO | hammerfest | pipeline_operator | Snohvit pipeline (Equinor) | equinor.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-hammerfest-transit_naval | NO | hammerfest | transit_naval | Royal Norwegian Navy | forsvar.no | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-hammerfest-loading_terminal | NO | hammerfest | loading_terminal | Hammerfest LNG (Snohvit) | equinor.com | infrastructure | official | vessel_loading,exports,force_majeure | proposed |
| geo-hammerfest-national_noc | NO | hammerfest | national_noc | Equinor | equinor.com | noc | official | production,exports,force_majeure | unverified |
| geo-hammerfest-shipping_lane | NO | hammerfest | shipping_lane | Kystverket coastal traffic | kystverket.no | shipping | official | vessel_loading,port_closure | proposed |
| geo-hammerfest-customs_border | NO | hammerfest | customs_border | Norwegian Customs (Tolletaten) | toll.no | government_regulator | official | exports,export_license | proposed |
| geo-hammerfest-insurance_war_risk | US | hammerfest | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-hammerfest-storage_operator | — | hammerfest | storage_operator | (LNG — no crude storage) | — | infrastructure | — | — | empty |
| geo-hammerfest-pricing_hub | NO | hammerfest | pricing_hub | ICE Endex (TTF linkage) | theice.com | exchange | official | pricing_formula,exports | proposed |
| geo-hammerfest-weather_hazard | NO | hammerfest | weather_hazard | Norwegian Meteorological Institute | met.no | weather | official | port_closure,hurricane | proposed |
| geo-hammerfest-sanctions_enforcement | EU | hammerfest | sanctions_enforcement | EU Sanctions (Russian gas linkage) | ec.europa.eu | government_regulator | official | sanctions | proposed |

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
  "phase_index": 25,
  "last_geo_target": "hammerfest",
  "crosscheck_cursor": 0,
  "last_batch_seq": 93
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_094_geo_target_cove_point.md` (Fáze 3, Cove Point LNG).
