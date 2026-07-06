# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_075_geo_target_gibraltar.md  
**Fáze:** geo_target — krok gibraltar (Fáze 3, Strait of Gibraltar, chokepoint)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `gibraltar` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_073_geo_target_gibraltar.md` a zachovává konzervativní statusy: {'proposed': 7, 'empty': 5}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-gibraltar-port_authority | GI | gibraltar | port_authority | Gibraltar Port Authority | gibport.com | infrastructure | official | port_closure,vessel_loading | proposed |
| geo-gibraltar-pipeline_operator | — | gibraltar | pipeline_operator | (no pipeline through strait) | — | infrastructure | — | — | empty |
| geo-gibraltar-transit_naval | GB | gibraltar | transit_naval | Royal Navy (Gibraltar Squadron) | royalnavy.mod.uk | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-gibraltar-loading_terminal | — | gibraltar | loading_terminal | (transit chokepoint — no load terminal) | — | infrastructure | — | — | empty |
| geo-gibraltar-national_noc | — | gibraltar | national_noc | (transit hub — no NOC) | — | noc | — | — | empty |
| geo-gibraltar-shipping_lane | GI | gibraltar | shipping_lane | Gibraltar VTS / traffic separation | gibport.com | shipping | official | port_closure,vessel_loading | proposed |
| geo-gibraltar-customs_border | GI | gibraltar | customs_border | HM Customs Gibraltar | customs.gi | government_regulator | official | exports,imports | proposed |
| geo-gibraltar-insurance_war_risk | US | gibraltar | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-gibraltar-storage_operator | — | gibraltar | storage_operator | (none at chokepoint) | — | infrastructure | — | — | empty |
| geo-gibraltar-pricing_hub | — | gibraltar | pricing_hub | (transit — no pricing hub) | — | exchange | — | — | empty |
| geo-gibraltar-weather_hazard | GB | gibraltar | weather_hazard | Met Office (Gibraltar area) | metoffice.gov.uk | weather | official | port_closure,hurricane | proposed |
| geo-gibraltar-sanctions_enforcement | GB | gibraltar | sanctions_enforcement | HM Treasury (sanctions list) | gov.uk | government_regulator | official | sanctions | proposed |

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
  "phase_index": 7,
  "last_geo_target": "gibraltar",
  "crosscheck_cursor": 0,
  "last_batch_seq": 75
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_076_geo_target_ras_tanura.md` (Fáze 3, Ras Tanura).
