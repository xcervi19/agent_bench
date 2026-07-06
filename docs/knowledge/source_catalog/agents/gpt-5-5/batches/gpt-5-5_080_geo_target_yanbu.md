# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_080_geo_target_yanbu.md  
**Fáze:** geo_target — krok yanbu (Fáze 3, Yanbu, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `yanbu` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_078_geo_target_yanbu.md` a zachovává konzervativní statusy: {'proposed': 12}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-yanbu-port_authority | SA | yanbu | port_authority | Saudi Ports Authority (Mawani) | mawani.gov.sa | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-yanbu-pipeline_operator | SA | yanbu | pipeline_operator | East–West Petroline (Yanbu terminus) | aramco.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-yanbu-transit_naval | SA | yanbu | transit_naval | Royal Saudi Navy | mod.gov.sa | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-yanbu-loading_terminal | SA | yanbu | loading_terminal | Yanbu export / refinery terminals | aramco.com | infrastructure | official | vessel_loading,exports | proposed |
| geo-yanbu-national_noc | SA | yanbu | national_noc | Saudi Aramco | aramco.com | noc | official | production,exports,force_majeure | proposed |
| geo-yanbu-shipping_lane | SA | yanbu | shipping_lane | Mawani Red Sea traffic | mawani.gov.sa | shipping | official | vessel_loading,port_closure | proposed |
| geo-yanbu-customs_border | SA | yanbu | customs_border | ZATCA (Customs) | zatca.gov.sa | government_regulator | official | exports,export_license | proposed |
| geo-yanbu-insurance_war_risk | US | yanbu | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading,sanctions | proposed |
| geo-yanbu-storage_operator | SA | yanbu | storage_operator | Yanbu refinery / tank storage | aramco.com | infrastructure | official | storage_levels,exports | proposed |
| geo-yanbu-pricing_hub | SA | yanbu | pricing_hub | Aramco OSP / export pricing | aramco.com | noc | official | pricing_formula,exports | proposed |
| geo-yanbu-weather_hazard | SA | yanbu | weather_hazard | National Center for Meteorology | pme.gov.sa | weather | official | port_closure,hurricane | proposed |
| geo-yanbu-sanctions_enforcement | US | yanbu | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions | proposed |

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
  "phase_index": 12,
  "last_geo_target": "yanbu",
  "crosscheck_cursor": 0,
  "last_batch_seq": 80
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_081_geo_target_jebel_ali.md` (Fáze 3, Jebel Ali).
