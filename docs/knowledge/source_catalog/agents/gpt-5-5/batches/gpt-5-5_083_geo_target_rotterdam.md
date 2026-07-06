# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_083_geo_target_rotterdam.md  
**Fáze:** geo_target — krok rotterdam (Fáze 3, Rotterdam, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `rotterdam` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_081_geo_target_rotterdam.md` a zachovává konzervativní statusy: {'proposed': 10, 'unverified': 1, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-rotterdam-port_authority | NL | rotterdam | port_authority | Port of Rotterdam Authority | portofrotterdam.com | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-rotterdam-pipeline_operator | NL | rotterdam | pipeline_operator | Rotterdam-Rhine Pipeline (RRP) | portofrotterdam.com | infrastructure | official | pipeline_outage,imports | unverified |
| geo-rotterdam-transit_naval | NL | rotterdam | transit_naval | Royal Netherlands Navy | defensie.nl | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-rotterdam-loading_terminal | NL | rotterdam | loading_terminal | Europoort / Maasvlakte terminals | portofrotterdam.com | infrastructure | official | vessel_loading,imports | proposed |
| geo-rotterdam-national_noc | — | rotterdam | national_noc | (import hub — no NOC) | — | noc | — | imports | empty |
| geo-rotterdam-shipping_lane | NL | rotterdam | shipping_lane | Rotterdam VTS / port traffic | portofrotterdam.com | shipping | official | vessel_loading,port_closure | proposed |
| geo-rotterdam-customs_border | NL | rotterdam | customs_border | Dutch Customs | belastingdienst.nl | government_regulator | official | exports,imports | proposed |
| geo-rotterdam-insurance_war_risk | US | rotterdam | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-rotterdam-storage_operator | NL | rotterdam | storage_operator | ARA tank storage (Rotterdam hub) | portofrotterdam.com | infrastructure | official | storage_levels,imports | proposed |
| geo-rotterdam-pricing_hub | NL | rotterdam | pricing_hub | ICE Endex (Amsterdam) | theice.com | exchange | official | pricing_formula,storage_levels | proposed |
| geo-rotterdam-weather_hazard | NL | rotterdam | weather_hazard | KNMI (Royal Netherlands Meteorological Institute) | knmi.nl | weather | official | port_closure,hurricane | proposed |
| geo-rotterdam-sanctions_enforcement | EU | rotterdam | sanctions_enforcement | EU Sanctions (Russian product ban) | ec.europa.eu | government_regulator | official | sanctions | proposed |

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
  "phase_index": 15,
  "last_geo_target": "rotterdam",
  "crosscheck_cursor": 0,
  "last_batch_seq": 83
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_084_geo_target_novorossiysk.md` (Fáze 3, Novorossiysk).
