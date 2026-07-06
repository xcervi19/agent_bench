# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_089_geo_target_freeport.md  
**Fáze:** geo_target — krok freeport (Fáze 3, Freeport LNG, us_gulf_hub)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `freeport` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_087_geo_target_freeport.md` a zachovává konzervativní statusy: {'proposed': 9, 'empty': 2, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-freeport-port_authority | US | freeport | port_authority | Port Freeport | portfreeport.com | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-freeport-pipeline_operator | US | freeport | pipeline_operator | Freeport LNG feedgas | freeportlng.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-freeport-transit_naval | US | freeport | transit_naval | US Coast Guard | uscg.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-freeport-loading_terminal | US | freeport | loading_terminal | Freeport LNG | freeportlng.com | infrastructure | official | vessel_loading,exports,force_majeure | proposed |
| geo-freeport-national_noc | — | freeport | national_noc | (LNG export — no NOC) | — | noc | — | exports | empty |
| geo-freeport-shipping_lane | US | freeport | shipping_lane | Port Freeport channel traffic | portfreeport.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-freeport-customs_border | US | freeport | customs_border | Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports,export_license | proposed |
| geo-freeport-insurance_war_risk | US | freeport | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-freeport-storage_operator | — | freeport | storage_operator | (LNG — no crude storage) | — | infrastructure | — | — | empty |
| geo-freeport-pricing_hub | US | freeport | pricing_hub | CME Group (Henry Hub / LNG linkage) | cmegroup.com | exchange | official | pricing_formula,exports | unverified |
| geo-freeport-weather_hazard | US | freeport | weather_hazard | NOAA / NWS (Gulf hurricanes) | weather.gov | weather | official | port_closure,hurricane,force_majeure | proposed |
| geo-freeport-sanctions_enforcement | US | freeport | sanctions_enforcement | FERC (LNG export authorization) | ferc.gov | government_regulator | official | export_license,sanctions | proposed |

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
  "phase_index": 21,
  "last_geo_target": "freeport",
  "crosscheck_cursor": 0,
  "last_batch_seq": 89
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_090_geo_target_corpus_christi.md` (Fáze 3, Corpus Christi).
