# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_071_geo_target_suez.md  
**Fáze:** geo_target — krok suez (Fáze 3, Suez Canal, chokepoint)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `suez` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_069_geo_target_suez.md` a zachovává konzervativní statusy: {'proposed': 9, 'unverified': 3}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-suez-port_authority | EG | suez | port_authority | Suez Canal Authority (SCA) | suezcanal.gov.eg | infrastructure | official | port_closure,vessel_loading | proposed |
| geo-suez-pipeline_operator | EG | suez | pipeline_operator | SUMED Pipeline | sumed.org.eg | infrastructure | official | pipeline_outage,exports | proposed |
| geo-suez-transit_naval | EG | suez | transit_naval | Egyptian Navy | navy.mil.eg | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-suez-loading_terminal | EG | suez | loading_terminal | Ain Sukhna terminal area | sczone.gov.eg | infrastructure | official | vessel_loading,exports | proposed |
| geo-suez-national_noc | EG | suez | national_noc | EGPC | egpc.com.eg | noc | official | exports,production | proposed |
| geo-suez-shipping_lane | EG | suez | shipping_lane | SCA Traffic Management | suezcanal.gov.eg | shipping | official | port_closure,vessel_loading | proposed |
| geo-suez-customs_border | EG | suez | customs_border | Egyptian Customs | customs.gov.eg | government_regulator | official | exports,export_license | proposed |
| geo-suez-insurance_war_risk | US | suez | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-suez-storage_operator | EG | suez | storage_operator | SCZone storage | sczone.gov.eg | infrastructure | official | storage_levels | proposed |
| geo-suez-pricing_hub | — | suez | pricing_hub | (transit fees — SCA tariff page) | suezcanal.gov.eg | infrastructure | official | pricing_formula | proposed |
| geo-suez-weather_hazard | EG | suez | weather_hazard | Egyptian Meteorological Authority | eema.gov.eg | weather | official | port_closure | unverified |
| geo-suez-sanctions_enforcement | EG | suez | sanctions_enforcement | Central Bank of Egypt (transit payments) | cbe.org.eg | government_regulator | official | sanctions | unverified |

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
  "phase_index": 3,
  "last_geo_target": "suez",
  "crosscheck_cursor": 0,
  "last_batch_seq": 71
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_072_geo_target_panama.md` (Fáze 3, Panama Canal).
