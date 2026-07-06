# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_090_geo_target_corpus_christi.md  
**Fáze:** geo_target — krok corpus_christi (Fáze 3, Corpus Christi, us_gulf_hub)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `corpus_christi` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_088_geo_target_corpus_christi.md` a zachovává konzervativní statusy: {'proposed': 10, 'unverified': 1, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-corpus_christi-port_authority | US | corpus_christi | port_authority | Port of Corpus Christi | portofcc.com | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-corpus_christi-pipeline_operator | US | corpus_christi | pipeline_operator | Gray Oak / EPIC crude pipelines | portofcc.com | infrastructure | official | pipeline_outage,exports | unverified |
| geo-corpus_christi-transit_naval | US | corpus_christi | transit_naval | US Coast Guard | uscg.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-corpus_christi-loading_terminal | US | corpus_christi | loading_terminal | Corpus Christi crude + Cheniere LNG export | portofcc.com | infrastructure | official | vessel_loading,exports,force_majeure | proposed |
| geo-corpus_christi-national_noc | — | corpus_christi | national_noc | (export hub — no NOC) | — | noc | — | exports | empty |
| geo-corpus_christi-shipping_lane | US | corpus_christi | shipping_lane | Port Corpus Christi traffic | portofcc.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-corpus_christi-customs_border | US | corpus_christi | customs_border | Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports,export_license | proposed |
| geo-corpus_christi-insurance_war_risk | US | corpus_christi | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-corpus_christi-storage_operator | US | corpus_christi | storage_operator | EIA Gulf Coast storage data | eia.gov | government_regulator | official | storage_levels,exports | proposed |
| geo-corpus_christi-pricing_hub | US | corpus_christi | pricing_hub | CME Group (WTI / Gulf Coast diff) | cmegroup.com | exchange | official | pricing_formula,exports | proposed |
| geo-corpus_christi-weather_hazard | US | corpus_christi | weather_hazard | NOAA / NWS (Gulf hurricanes) | weather.gov | weather | official | port_closure,hurricane | proposed |
| geo-corpus_christi-sanctions_enforcement | US | corpus_christi | sanctions_enforcement | FERC (LNG export authorization) | ferc.gov | government_regulator | official | export_license,sanctions | proposed |

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
  "phase_index": 22,
  "last_geo_target": "corpus_christi",
  "crosscheck_cursor": 0,
  "last_batch_seq": 90
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_091_geo_target_ras_laffan.md` (Fáze 3, Ras Laffan).
