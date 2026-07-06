# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_096_geo_target_ara.md  
**Fáze:** geo_target — krok ara (Fáze 3, ARA, storage_pricing_hub)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `ara` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_094_geo_target_ara.md` a zachovává konzervativní statusy: {'proposed': 10, 'unverified': 1, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-ara-port_authority | NL | ara | port_authority | Port of Rotterdam Authority | portofrotterdam.com | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-ara-pipeline_operator | NL | ara | pipeline_operator | Rotterdam-Rhine Pipeline (RRP) | portofrotterdam.com | infrastructure | official | pipeline_outage,imports | unverified |
| geo-ara-transit_naval | NL | ara | transit_naval | Royal Netherlands Navy | defensie.nl | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-ara-loading_terminal | NL | ara | loading_terminal | ARA tank / product terminals | portofamsterdam.com | infrastructure | official | vessel_loading,imports,storage_levels | proposed |
| geo-ara-national_noc | — | ara | national_noc | (import hub — no NOC) | — | noc | — | imports | empty |
| geo-ara-shipping_lane | NL | ara | shipping_lane | ARA VTS / port traffic | portofrotterdam.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-ara-customs_border | NL | ara | customs_border | Dutch Customs | belastingdienst.nl | government_regulator | official | exports,imports | proposed |
| geo-ara-insurance_war_risk | US | ara | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-ara-storage_operator | NL | ara | storage_operator | ARA tank storage (Rotterdam/Amsterdam) | portofrotterdam.com | infrastructure | official | storage_levels,imports | proposed |
| geo-ara-pricing_hub | NL | ara | pricing_hub | ICE Endex (Amsterdam) | theice.com | exchange | official | pricing_formula,storage_levels | proposed |
| geo-ara-weather_hazard | NL | ara | weather_hazard | KNMI | knmi.nl | weather | official | port_closure,hurricane | proposed |
| geo-ara-sanctions_enforcement | EU | ara | sanctions_enforcement | EU Sanctions (Russian product ban) | ec.europa.eu | government_regulator | official | sanctions | proposed |

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
  "phase_index": 28,
  "last_geo_target": "ara",
  "crosscheck_cursor": 0,
  "last_batch_seq": 96
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_097_geo_target_saldanha.md` (Fáze 3, Saldanha Bay).
