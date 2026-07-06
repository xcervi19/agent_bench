# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_072_geo_target_panama.md  
**Fáze:** geo_target — krok panama (Fáze 3, Panama Canal, chokepoint)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `panama` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_070_geo_target_panama.md` a zachovává konzervativní statusy: {'proposed': 6, 'unverified': 4, 'empty': 2}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-panama-port_authority | PA | panama | port_authority | Panama Canal Authority (ACP) | pancanal.com | infrastructure | official | port_closure,vessel_loading | proposed |
| geo-panama-pipeline_operator | PA | panama | pipeline_operator | Trans-Panama Pipeline (Petroterminal) | petroterminal.com | infrastructure | official | pipeline_outage,exports | unverified |
| geo-panama-transit_naval | PA | panama | transit_naval | SENAN (Panama Navy) | senan.gob.pa | government_regulator | official | port_closure | unverified |
| geo-panama-loading_terminal | PA | panama | loading_terminal | Balboa / Cristobal terminals | pancanal.com | infrastructure | official | vessel_loading | proposed |
| geo-panama-national_noc | — | panama | national_noc | (transit hub — no NOC) | — | noc | — | — | empty |
| geo-panama-shipping_lane | PA | panama | shipping_lane | ACP VTS / transit scheduling | pancanal.com | shipping | official | port_closure,vessel_loading | proposed |
| geo-panama-customs_border | PA | panama | customs_border | National Customs Authority | arafat.gob.pa | government_regulator | official | exports,imports | unverified |
| geo-panama-insurance_war_risk | US | panama | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-panama-storage_operator | — | panama | storage_operator | (none at canal) | — | infrastructure | — | — | empty |
| geo-panama-pricing_hub | PA | panama | pricing_hub | ACP toll / reservation fees | pancanal.com | infrastructure | official | pricing_formula | proposed |
| geo-panama-weather_hazard | PA | panama | weather_hazard | ETESA (Met/Hydrology) | etesa.gob.pa | weather | official | port_closure | unverified |
| geo-panama-sanctions_enforcement | US | panama | sanctions_enforcement | OFAC (sanctioned vessel transit) | treasury.gov | government_regulator | official | sanctions | proposed |

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
  "phase_index": 4,
  "last_geo_target": "panama",
  "crosscheck_cursor": 0,
  "last_batch_seq": 72
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_073_geo_target_malacca.md` (Fáze 3, Strait of Malacca).
