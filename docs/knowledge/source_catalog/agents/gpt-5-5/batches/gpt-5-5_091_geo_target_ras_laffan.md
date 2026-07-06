# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_091_geo_target_ras_laffan.md  
**Fáze:** geo_target — krok ras_laffan (Fáze 3, Ras Laffan, lng_terminal)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `ras_laffan` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_089_geo_target_ras_laffan.md` a zachovává konzervativní statusy: {'proposed': 8, 'unverified': 3, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-ras_laffan-port_authority | QA | ras_laffan | port_authority | Mwani Qatar | mwani.com.qa | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-ras_laffan-pipeline_operator | QA | ras_laffan | pipeline_operator | QatarEnergy North Field gas network | qatarenergy.qa | infrastructure | official | pipeline_outage,exports | proposed |
| geo-ras_laffan-transit_naval | QA | ras_laffan | transit_naval | Qatar Emiri Naval Forces | mod.gov.qa | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-ras_laffan-loading_terminal | QA | ras_laffan | loading_terminal | Ras Laffan LNG trains | qatarenergy.qa | infrastructure | official | vessel_loading,exports,force_majeure | proposed |
| geo-ras_laffan-national_noc | QA | ras_laffan | national_noc | QatarEnergy | qatarenergy.qa | noc | official | production,exports,force_majeure | proposed |
| geo-ras_laffan-shipping_lane | QA | ras_laffan | shipping_lane | Ras Laffan port traffic | qatarenergy.qa | shipping | official | vessel_loading,port_closure | proposed |
| geo-ras_laffan-customs_border | QA | ras_laffan | customs_border | General Authority of Customs | customs.gov.qa | government_regulator | official | exports,export_license | proposed |
| geo-ras_laffan-insurance_war_risk | US | ras_laffan | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-ras_laffan-storage_operator | — | ras_laffan | storage_operator | (LNG — no crude storage) | — | infrastructure | — | — | empty |
| geo-ras_laffan-pricing_hub | QA | ras_laffan | pricing_hub | Qatar Stock Exchange | qe.com.qa | exchange | official | pricing_formula | unverified |
| geo-ras_laffan-weather_hazard | QA | ras_laffan | weather_hazard | Qatar Meteorology Department | qweather.gov.qa | weather | official | port_closure,hurricane | unverified |
| geo-ras_laffan-sanctions_enforcement | QA | ras_laffan | sanctions_enforcement | Qatar Central Bank (sanctions) | qcb.gov.qa | government_regulator | official | sanctions | proposed |

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
  "phase_index": 23,
  "last_geo_target": "ras_laffan",
  "crosscheck_cursor": 0,
  "last_batch_seq": 91
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_092_geo_target_yamal.md` (Fáze 3, Yamal LNG).
