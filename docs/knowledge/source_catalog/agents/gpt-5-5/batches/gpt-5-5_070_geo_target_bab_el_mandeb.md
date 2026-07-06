# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_070_geo_target_bab_el_mandeb.md  
**Fáze:** geo_target — krok bab_el_mandeb (Fáze 3, Bab el-Mandeb, chokepoint)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `bab_el_mandeb` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_068_geo_target_bab_el_mandeb.md` a zachovává konzervativní statusy: {'proposed': 7, 'empty': 3, 'unverified': 2}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-bab_el_mandeb-port_authority | DJ | bab_el_mandeb | port_authority | Port of Djibouti | portofdjibouti.dj | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-bab_el_mandeb-pipeline_operator | — | bab_el_mandeb | pipeline_operator | (no pipeline through strait) | — | infrastructure | — | — | empty |
| geo-bab_el_mandeb-transit_naval | — | bab_el_mandeb | transit_naval | Combined Maritime Forces (CMF) | combinedmaritimeforces.com | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-bab_el_mandeb-loading_terminal | SA | bab_el_mandeb | loading_terminal | Yanbu export terminal (Red Sea transit) | aramco.com | infrastructure | official | vessel_loading,exports | proposed |
| geo-bab_el_mandeb-national_noc | SA | bab_el_mandeb | national_noc | Saudi Aramco | aramco.com | noc | official | exports,vessel_loading | proposed |
| geo-bab_el_mandeb-shipping_lane | GB | bab_el_mandeb | shipping_lane | UKMTO (Maritime Trade Ops) | ukmto.org | shipping | official | port_closure,vessel_loading | proposed |
| geo-bab_el_mandeb-customs_border | YE | bab_el_mandeb | customs_border | Yemen Customs | customs.gov.ye | government_regulator | official | exports,export_license | unverified |
| geo-bab_el_mandeb-insurance_war_risk | US | bab_el_mandeb | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading,sanctions | proposed |
| geo-bab_el_mandeb-storage_operator | — | bab_el_mandeb | storage_operator | (none at chokepoint) | — | infrastructure | — | — | empty |
| geo-bab_el_mandeb-pricing_hub | — | bab_el_mandeb | pricing_hub | (Red Sea freight risk — no exchange) | — | exchange | — | pricing_formula | empty |
| geo-bab_el_mandeb-weather_hazard | SA | bab_el_mandeb | weather_hazard | Saudi Meteorology (Red Sea) | pme.gov.sa | weather | official | port_closure | unverified |
| geo-bab_el_mandeb-sanctions_enforcement | US | bab_el_mandeb | sanctions_enforcement | OFAC (Houthi / Iran linkage) | treasury.gov | government_regulator | official | sanctions | proposed |

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
  "phase_index": 2,
  "last_geo_target": "bab_el_mandeb",
  "crosscheck_cursor": 0,
  "last_batch_seq": 70
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_071_geo_target_suez.md` (Fáze 3, Suez Canal).
