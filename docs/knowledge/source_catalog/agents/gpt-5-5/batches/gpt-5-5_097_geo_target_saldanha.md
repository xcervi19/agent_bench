# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_097_geo_target_saldanha.md  
**Fáze:** geo_target — krok saldanha (Fáze 3, Saldanha Bay, storage_pricing_hub)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `saldanha` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_095_geo_target_saldanha.md` a zachovává konzervativní statusy: {'proposed': 8, 'unverified': 4}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-saldanha-port_authority | ZA | saldanha | port_authority | Transnet National Ports Authority | tnpa.co.za | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-saldanha-pipeline_operator | ZA | saldanha | pipeline_operator | Transnet Pipelines | transnet.net | infrastructure | official | pipeline_outage,imports | unverified |
| geo-saldanha-transit_naval | ZA | saldanha | transit_naval | South African Navy | dod.mil.za | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-saldanha-loading_terminal | ZA | saldanha | loading_terminal | Saldanha Bay terminal | tnpa.co.za | infrastructure | official | vessel_loading,imports | proposed |
| geo-saldanha-national_noc | ZA | saldanha | national_noc | PetroSA | petrosa.co.za | noc | official | production,imports | proposed |
| geo-saldanha-shipping_lane | ZA | saldanha | shipping_lane | Saldanha Bay port traffic | tnpa.co.za | shipping | official | vessel_loading,port_closure | proposed |
| geo-saldanha-customs_border | ZA | saldanha | customs_border | SARS (Customs) | sars.gov.za | government_regulator | official | exports,imports | proposed |
| geo-saldanha-insurance_war_risk | US | saldanha | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-saldanha-storage_operator | ZA | saldanha | storage_operator | Strategic Fuel Fund (Saldanha storage) | sff.org.za | infrastructure | official | storage_levels,imports | proposed |
| geo-saldanha-pricing_hub | ZA | saldanha | pricing_hub | JSE | jse.co.za | exchange | official | pricing_formula | unverified |
| geo-saldanha-weather_hazard | ZA | saldanha | weather_hazard | SAWS (South African Weather Service) | weathersa.co.za | weather | official | port_closure,hurricane | proposed |
| geo-saldanha-sanctions_enforcement | ZA | saldanha | sanctions_enforcement | National Treasury (sanctions compliance) | treasury.gov.za | government_regulator | official | sanctions | unverified |

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
  "phase_index": 29,
  "last_geo_target": "saldanha",
  "crosscheck_cursor": 0,
  "last_batch_seq": 97
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_098_geo_target_btc.md` (Fáze 3, BTC).
