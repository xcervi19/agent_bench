# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_092_geo_target_yamal.md  
**Fáze:** geo_target — krok yamal (Fáze 3, Yamal LNG, lng_terminal)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `yamal` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_090_geo_target_yamal.md` a zachovává konzervativní statusy: {'proposed': 7, 'unverified': 4, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-yamal-port_authority | RU | yamal | port_authority | Yamal LNG / Sabetta port | novatek.ru | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-yamal-pipeline_operator | RU | yamal | pipeline_operator | Yamal gas pipeline network | novatek.ru | infrastructure | official | pipeline_outage,exports | proposed |
| geo-yamal-transit_naval | RU | yamal | transit_naval | Russian Navy (Northern Fleet) | structure.mil.ru | government_regulator | official | port_closure,vessel_loading | unverified |
| geo-yamal-loading_terminal | RU | yamal | loading_terminal | Sabetta LNG terminal | novatek.ru | infrastructure | official | vessel_loading,exports,force_majeure | proposed |
| geo-yamal-national_noc | RU | yamal | national_noc | Novatek | novatek.ru | noc | official | production,exports,force_majeure | proposed |
| geo-yamal-shipping_lane | RU | yamal | shipping_lane | Northern Sea Route (Atomflot) | rosatom.ru | shipping | official | vessel_loading,port_closure | unverified |
| geo-yamal-customs_border | RU | yamal | customs_border | Federal Customs Service (FTS) | customs.gov.ru | government_regulator | official | exports,export_license | proposed |
| geo-yamal-insurance_war_risk | US | yamal | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading,sanctions | proposed |
| geo-yamal-storage_operator | — | yamal | storage_operator | (LNG — no crude storage) | — | infrastructure | — | — | empty |
| geo-yamal-pricing_hub | RU | yamal | pricing_hub | MOEX (gas/LNG markers) | moex.com | exchange | official | pricing_formula,exports | unverified |
| geo-yamal-weather_hazard | RU | yamal | weather_hazard | Roshydromet (Arctic) | meteoinfo.ru | weather | official | port_closure,hurricane | unverified |
| geo-yamal-sanctions_enforcement | US | yamal | sanctions_enforcement | OFAC (Novatek / Yamal sanctions) | treasury.gov | government_regulator | official | sanctions,export_license | proposed |

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
  "phase_index": 24,
  "last_geo_target": "yamal",
  "crosscheck_cursor": 0,
  "last_batch_seq": 92
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_093_geo_target_hammerfest.md` (Fáze 3, Hammerfest LNG).
