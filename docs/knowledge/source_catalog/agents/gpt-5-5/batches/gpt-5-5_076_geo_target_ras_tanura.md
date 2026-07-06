# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_076_geo_target_ras_tanura.md  
**Fáze:** geo_target — krok ras_tanura (Fáze 3, Ras Tanura, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `ras_tanura` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_074_geo_target_ras_tanura.md` a zachovává konzervativní statusy: {'proposed': 12}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-ras_tanura-port_authority | SA | ras_tanura | port_authority | Saudi Ports Authority (Mawani) | mawani.gov.sa | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-ras_tanura-pipeline_operator | SA | ras_tanura | pipeline_operator | East–West Petroline (Aramco) | aramco.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-ras_tanura-transit_naval | SA | ras_tanura | transit_naval | Royal Saudi Navy | mod.gov.sa | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-ras_tanura-loading_terminal | SA | ras_tanura | loading_terminal | Ras Tanura Marine Terminal | aramco.com | infrastructure | official | vessel_loading,exports | proposed |
| geo-ras_tanura-national_noc | SA | ras_tanura | national_noc | Saudi Aramco | aramco.com | noc | official | production,exports,force_majeure | proposed |
| geo-ras_tanura-shipping_lane | SA | ras_tanura | shipping_lane | Mawani VTS / Gulf traffic | mawani.gov.sa | shipping | official | vessel_loading,port_closure | proposed |
| geo-ras_tanura-customs_border | SA | ras_tanura | customs_border | ZATCA (Customs) | zatca.gov.sa | government_regulator | official | exports,export_license | proposed |
| geo-ras_tanura-insurance_war_risk | US | ras_tanura | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading | proposed |
| geo-ras_tanura-storage_operator | SA | ras_tanura | storage_operator | Ras Tanura tank farms | aramco.com | infrastructure | official | storage_levels,exports | proposed |
| geo-ras_tanura-pricing_hub | SA | ras_tanura | pricing_hub | Aramco OSP / Arab Light marker | aramco.com | noc | official | pricing_formula,exports | proposed |
| geo-ras_tanura-weather_hazard | SA | ras_tanura | weather_hazard | National Center for Meteorology | pme.gov.sa | weather | official | port_closure,hurricane | proposed |
| geo-ras_tanura-sanctions_enforcement | US | ras_tanura | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions | proposed |

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
  "phase_index": 8,
  "last_geo_target": "ras_tanura",
  "crosscheck_cursor": 0,
  "last_batch_seq": 76
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_077_geo_target_fujairah.md` (Fáze 3, Fujairah).
