# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_082_geo_target_singapore.md  
**Fáze:** geo_target — krok singapore (Fáze 3, Singapore bunkering hub, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `singapore` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_080_geo_target_singapore.md` a zachovává konzervativní statusy: {'proposed': 9, 'empty': 2, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-singapore-port_authority | SG | singapore | port_authority | MPA Singapore | mpa.gov.sg | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-singapore-pipeline_operator | — | singapore | pipeline_operator | (no pipeline — bunkering hub) | — | infrastructure | — | — | empty |
| geo-singapore-transit_naval | SG | singapore | transit_naval | Republic of Singapore Navy | mindef.gov.sg | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-singapore-loading_terminal | SG | singapore | loading_terminal | Singapore bunkering / STS hub | mpa.gov.sg | infrastructure | official | vessel_loading,imports | proposed |
| geo-singapore-national_noc | — | singapore | national_noc | (import hub — no NOC) | — | noc | — | imports | empty |
| geo-singapore-shipping_lane | SG | singapore | shipping_lane | MPA VTS / Traffic Separation | mpa.gov.sg | shipping | official | vessel_loading,port_closure | proposed |
| geo-singapore-customs_border | SG | singapore | customs_border | Singapore Customs | customs.gov.sg | government_regulator | official | exports,imports | proposed |
| geo-singapore-insurance_war_risk | US | singapore | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-singapore-storage_operator | SG | singapore | storage_operator | Jurong Island / tank storage | mpa.gov.sg | infrastructure | official | storage_levels,imports | proposed |
| geo-singapore-pricing_hub | SG | singapore | pricing_hub | SGX / regional markers | sgx.com | exchange | official | pricing_formula | unverified |
| geo-singapore-weather_hazard | SG | singapore | weather_hazard | MSS (Meteorological Service SG) | weather.gov.sg | weather | official | port_closure,hurricane | proposed |
| geo-singapore-sanctions_enforcement | SG | singapore | sanctions_enforcement | MAS (Monetary Authority) | mas.gov.sg | government_regulator | official | sanctions | proposed |

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
  "phase_index": 14,
  "last_geo_target": "singapore",
  "crosscheck_cursor": 0,
  "last_batch_seq": 82
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_083_geo_target_rotterdam.md` (Fáze 3, Rotterdam).
