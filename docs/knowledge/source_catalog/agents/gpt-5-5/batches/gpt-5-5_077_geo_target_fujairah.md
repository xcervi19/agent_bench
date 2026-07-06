# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_077_geo_target_fujairah.md  
**Fáze:** geo_target — krok fujairah (Fáze 3, Fujairah, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `fujairah` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_075_geo_target_fujairah.md` a zachovává konzervativní statusy: {'proposed': 11, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-fujairah-port_authority | AE | fujairah | port_authority | Port of Fujairah | fujairahport.ae | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-fujairah-pipeline_operator | AE | fujairah | pipeline_operator | ADNOC Habshan–Fujairah pipeline | adnoc.ae | infrastructure | official | pipeline_outage,exports | proposed |
| geo-fujairah-transit_naval | AE | fujairah | transit_naval | UAE Armed Forces (Navy) | mod.gov.ae | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-fujairah-loading_terminal | AE | fujairah | loading_terminal | Fujairah Oil Industry Zone (FOIZ) | fujairahport.ae | infrastructure | official | vessel_loading,exports | proposed |
| geo-fujairah-national_noc | AE | fujairah | national_noc | ADNOC | adnoc.ae | noc | official | production,exports,force_majeure | proposed |
| geo-fujairah-shipping_lane | AE | fujairah | shipping_lane | Port of Fujairah VTS | fujairahport.ae | shipping | official | vessel_loading,port_closure | proposed |
| geo-fujairah-customs_border | AE | fujairah | customs_border | UAE Federal Customs | fcsc.gov.ae | government_regulator | official | exports,imports | proposed |
| geo-fujairah-insurance_war_risk | US | fujairah | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading | proposed |
| geo-fujairah-storage_operator | AE | fujairah | storage_operator | FOIZ tank storage hub | fujairahport.ae | infrastructure | official | storage_levels,exports | proposed |
| geo-fujairah-pricing_hub | AE | fujairah | pricing_hub | DGCX (Dubai crude marker) | dgcx.ae | exchange | official | pricing_formula | proposed |
| geo-fujairah-weather_hazard | AE | fujairah | weather_hazard | NCM (National Center of Meteorology) | ncm.ae | weather | official | port_closure,hurricane | proposed |
| geo-fujairah-sanctions_enforcement | AE | fujairah | sanctions_enforcement | UAE Central Bank (sanctions) | centralbank.ae | government_regulator | official | sanctions | proposed |

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
  "phase_index": 9,
  "last_geo_target": "fujairah",
  "crosscheck_cursor": 0,
  "last_batch_seq": 77
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_078_geo_target_kharg.md` (Fáze 3, Kharg Island).
