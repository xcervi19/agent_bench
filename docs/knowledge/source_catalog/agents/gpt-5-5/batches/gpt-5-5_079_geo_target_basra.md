# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_079_geo_target_basra.md  
**Fáze:** geo_target — krok basra (Fáze 3, Basra / Fao, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `basra` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_077_geo_target_basra.md` a zachovává konzervativní statusy: {'proposed': 6, 'unverified': 5, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-basra-port_authority | IQ | basra | port_authority | GCPI (State Company for Ports) | scp.gov.iq | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-basra-pipeline_operator | IQ | basra | pipeline_operator | South Oil Company pipelines | oil.gov.iq | infrastructure | official | pipeline_outage,exports | unverified |
| geo-basra-transit_naval | IQ | basra | transit_naval | Iraqi Navy / Ministry of Defense | mod.mil.iq | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-basra-loading_terminal | IQ | basra | loading_terminal | Basra Oil Terminal (BOT) / Fao | scp.gov.iq | infrastructure | official | vessel_loading,exports | proposed |
| geo-basra-national_noc | IQ | basra | national_noc | Basra Oil Company (BOC) | boc.oil.gov.iq | noc | official | production,exports,force_majeure | unverified |
| geo-basra-shipping_lane | IQ | basra | shipping_lane | GCPI southern port traffic | scp.gov.iq | shipping | official | vessel_loading,port_closure | proposed |
| geo-basra-customs_border | IQ | basra | customs_border | Iraqi General Commission for Customs | customs.gov.iq | government_regulator | official | exports,export_license | unverified |
| geo-basra-insurance_war_risk | US | basra | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading | proposed |
| geo-basra-storage_operator | IQ | basra | storage_operator | Fao storage / offshore terminals | scp.gov.iq | infrastructure | official | storage_levels,exports | proposed |
| geo-basra-pricing_hub | — | basra | pricing_hub | (Basrah Medium — no local exchange) | — | exchange | — | pricing_formula | empty |
| geo-basra-weather_hazard | IQ | basra | weather_hazard | Iraqi Meteorological Authority | meteorology.gov.iq | weather | official | port_closure | unverified |
| geo-basra-sanctions_enforcement | US | basra | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions | proposed |

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
  "phase_index": 11,
  "last_geo_target": "basra",
  "crosscheck_cursor": 0,
  "last_batch_seq": 79
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_080_geo_target_yanbu.md` (Fáze 3, Yanbu).
