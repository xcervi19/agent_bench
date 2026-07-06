# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_081_geo_target_jebel_ali.md  
**Fáze:** geo_target — krok jebel_ali (Fáze 3, Jebel Ali, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `jebel_ali` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_079_geo_target_jebel_ali.md` a zachovává konzervativní statusy: {'proposed': 11, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-jebel_ali-port_authority | AE | jebel_ali | port_authority | DP World — Jebel Ali Port | dpworld.com | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-jebel_ali-pipeline_operator | AE | jebel_ali | pipeline_operator | ADNOC pipeline network (UAE supply) | adnoc.ae | infrastructure | official | pipeline_outage,imports | proposed |
| geo-jebel_ali-transit_naval | AE | jebel_ali | transit_naval | UAE Armed Forces (Navy) | mod.gov.ae | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-jebel_ali-loading_terminal | AE | jebel_ali | loading_terminal | Jebel Ali bulk / container terminals | dpworld.com | infrastructure | official | vessel_loading,imports | proposed |
| geo-jebel_ali-national_noc | AE | jebel_ali | national_noc | ADNOC | adnoc.ae | noc | official | production,exports,imports | proposed |
| geo-jebel_ali-shipping_lane | AE | jebel_ali | shipping_lane | Jebel Ali VTS / port traffic | dpworld.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-jebel_ali-customs_border | AE | jebel_ali | customs_border | Dubai Customs | dubaicustoms.gov.ae | government_regulator | official | exports,imports | proposed |
| geo-jebel_ali-insurance_war_risk | US | jebel_ali | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading | proposed |
| geo-jebel_ali-storage_operator | AE | jebel_ali | storage_operator | Jebel Ali tank / product storage | dpworld.com | infrastructure | official | storage_levels,imports | proposed |
| geo-jebel_ali-pricing_hub | AE | jebel_ali | pricing_hub | DGCX (Dubai crude marker) | dgcx.ae | exchange | official | pricing_formula | proposed |
| geo-jebel_ali-weather_hazard | AE | jebel_ali | weather_hazard | NCM (National Center of Meteorology) | ncm.ae | weather | official | port_closure,hurricane | proposed |
| geo-jebel_ali-sanctions_enforcement | AE | jebel_ali | sanctions_enforcement | UAE Central Bank (sanctions) | centralbank.ae | government_regulator | official | sanctions | proposed |

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
  "phase_index": 13,
  "last_geo_target": "jebel_ali",
  "crosscheck_cursor": 0,
  "last_batch_seq": 81
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_082_geo_target_singapore.md` (Fáze 3, Singapore bunkering hub).
