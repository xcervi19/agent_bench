# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_074_geo_target_bospor.md  
**Fáze:** geo_target — krok bospor (Fáze 3, Turkish Straits / Bospor, chokepoint)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `bospor` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_072_geo_target_bospor.md` a zachovává konzervativní statusy: {'proposed': 9, 'unverified': 2, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-bospor-port_authority | TR | bospor | port_authority | Turkish Straits VTS (UAB) | uab.gov.tr | infrastructure | official | port_closure,vessel_loading | proposed |
| geo-bospor-pipeline_operator | TR | bospor | pipeline_operator | BOTAŞ (TurkStream / gas transit) | botas.gov.tr | infrastructure | official | pipeline_outage,imports | proposed |
| geo-bospor-transit_naval | TR | bospor | transit_naval | Turkish Naval Forces | deniz.kuvvetleri.tsk.tr | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-bospor-loading_terminal | TR | bospor | loading_terminal | Ceyhan terminal (BTC approach) | botas.gov.tr | infrastructure | official | vessel_loading,exports | proposed |
| geo-bospor-national_noc | TR | bospor | national_noc | TPAO | tpao.gov.tr | noc | official | production,exports | proposed |
| geo-bospor-shipping_lane | TR | bospor | shipping_lane | Istanbul Strait traffic management | uab.gov.tr | shipping | official | port_closure,vessel_loading | proposed |
| geo-bospor-customs_border | TR | bospor | customs_border | Turkish Customs | gumruk.gov.tr | government_regulator | official | exports,export_license | proposed |
| geo-bospor-insurance_war_risk | US | bospor | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-bospor-storage_operator | — | bospor | storage_operator | (transit only) | — | infrastructure | — | — | empty |
| geo-bospor-pricing_hub | TR | bospor | pricing_hub | Borsa Istanbul | borsaistanbul.com | exchange | official | pricing_formula | unverified |
| geo-bospor-weather_hazard | TR | bospor | weather_hazard | Turkish State Meteorological Service | mgm.gov.tr | weather | official | port_closure | proposed |
| geo-bospor-sanctions_enforcement | TR | bospor | sanctions_enforcement | Ministry of Trade (Russian oil transit) | ticaret.gov.tr | government_regulator | official | sanctions,export_license | proposed |

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
  "phase_index": 6,
  "last_geo_target": "bospor",
  "crosscheck_cursor": 0,
  "last_batch_seq": 74
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_075_geo_target_gibraltar.md` (Fáze 3, Strait of Gibraltar).
