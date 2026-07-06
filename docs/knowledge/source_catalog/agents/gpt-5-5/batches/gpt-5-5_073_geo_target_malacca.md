# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_073_geo_target_malacca.md  
**Fáze:** geo_target — krok malacca (Fáze 3, Strait of Malacca, chokepoint)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `malacca` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_071_geo_target_malacca.md` a zachovává konzervativní statusy: {'proposed': 11, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-malacca-port_authority | SG | malacca | port_authority | MPA Singapore | mpa.gov.sg | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-malacca-pipeline_operator | MY | malacca | pipeline_operator | Petronas RAPID pipeline corridor | petronas.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-malacca-transit_naval | SG | malacca | transit_naval | Republic of Singapore Navy | mindef.gov.sg | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-malacca-loading_terminal | SG | malacca | loading_terminal | Singapore bunkering hub | mpa.gov.sg | infrastructure | official | vessel_loading,imports | proposed |
| geo-malacca-national_noc | MY | malacca | national_noc | Petronas | petronas.com | noc | official | exports,production | proposed |
| geo-malacca-shipping_lane | SG | malacca | shipping_lane | MPA VTS / Traffic Separation | mpa.gov.sg | shipping | official | port_closure,vessel_loading | proposed |
| geo-malacca-customs_border | SG | malacca | customs_border | Singapore Customs | customs.gov.sg | government_regulator | official | exports,imports | proposed |
| geo-malacca-insurance_war_risk | US | malacca | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-malacca-storage_operator | SG | malacca | storage_operator | Jurong / storage tank farms | mpa.gov.sg | infrastructure | official | storage_levels | proposed |
| geo-malacca-pricing_hub | SG | malacca | pricing_hub | SGX / regional markers | sgx.com | exchange | official | pricing_formula | unverified |
| geo-malacca-weather_hazard | SG | malacca | weather_hazard | MSS (Meteorological Service SG) | weather.gov.sg | weather | official | port_closure,hurricane | proposed |
| geo-malacca-sanctions_enforcement | SG | malacca | sanctions_enforcement | MAS (Monetary Authority) | mas.gov.sg | government_regulator | official | sanctions | proposed |

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
  "phase_index": 5,
  "last_geo_target": "malacca",
  "crosscheck_cursor": 0,
  "last_batch_seq": 73
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_074_geo_target_bospor.md` (Fáze 3, Turkish Straits / Bospor).
