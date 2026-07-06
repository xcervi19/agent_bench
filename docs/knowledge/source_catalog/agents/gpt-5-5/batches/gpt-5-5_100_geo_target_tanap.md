# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_100_geo_target_tanap.md  
**Fáze:** geo_target — krok tanap (Fáze 3, TANAP, pipeline_entity)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `tanap` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_098_geo_target_tanap.md` a zachovává konzervativní statusy: {'empty': 5, 'proposed': 6, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-tanap-port_authority | — | tanap | port_authority | (gas pipeline — no port) | — | infrastructure | — | — | empty |
| geo-tanap-pipeline_operator | TR | tanap | pipeline_operator | TANAP (Trans-Anatolian Pipeline) | tanap.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-tanap-transit_naval | — | tanap | transit_naval | (land pipeline — no naval) | — | government_regulator | — | — | empty |
| geo-tanap-loading_terminal | AZ | tanap | loading_terminal | TANAP entry point (Azerbaijan border) | tanap.com | infrastructure | official | exports,pipeline_outage | proposed |
| geo-tanap-national_noc | AZ | tanap | national_noc | SOCAR | socar.az | noc | official | production,exports,force_majeure | proposed |
| geo-tanap-shipping_lane | — | tanap | shipping_lane | (land pipeline — no lane) | — | shipping | — | — | empty |
| geo-tanap-customs_border | TR | tanap | customs_border | Turkish Customs | gumruk.gov.tr | government_regulator | official | exports,export_license | proposed |
| geo-tanap-insurance_war_risk | — | tanap | insurance_war_risk | (land pipeline — N/A) | — | shipping | — | — | empty |
| geo-tanap-storage_operator | — | tanap | storage_operator | (transit pipeline — no storage) | — | infrastructure | — | — | empty |
| geo-tanap-pricing_hub | TR | tanap | pricing_hub | Borsa Istanbul (gas markers) | borsaistanbul.com | exchange | official | pricing_formula,exports | unverified |
| geo-tanap-weather_hazard | TR | tanap | weather_hazard | Turkish State Meteorological Service | mgm.gov.tr | weather | official | pipeline_outage | proposed |
| geo-tanap-sanctions_enforcement | US | tanap | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions,export_license | proposed |

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
  "phase": "country_social",
  "phase_index": 0,
  "last_geo_target": "tanap",
  "crosscheck_cursor": 0,
  "last_batch_seq": 100
}
```

Po merge této dávky → **další fáze:** `country_social`, první dávka podle country pořadí `SA`.
