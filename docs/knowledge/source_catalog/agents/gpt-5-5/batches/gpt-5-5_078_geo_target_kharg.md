# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_078_geo_target_kharg.md  
**Fáze:** geo_target — krok kharg (Fáze 3, Kharg Island, load_port)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `kharg` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_076_geo_target_kharg.md` a zachovává konzervativní statusy: {'proposed': 9, 'unverified': 2, 'empty': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-kharg-port_authority | IR | kharg | port_authority | PMO — Kharg Island Port | pmo.ir | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-kharg-pipeline_operator | IR | kharg | pipeline_operator | NIOC pipeline network | nioc.ir | infrastructure | official | pipeline_outage,exports | proposed |
| geo-kharg-transit_naval | IR | kharg | transit_naval | IRGC Navy (Persian Gulf) | (no Tier-1 domain) | government_regulator | — | port_closure,vessel_loading | unverified |
| geo-kharg-loading_terminal | IR | kharg | loading_terminal | Kharg Island export terminals | nioc.ir | infrastructure | official | vessel_loading,exports | proposed |
| geo-kharg-national_noc | IR | kharg | national_noc | NIOC | nioc.ir | noc | official | production,exports,force_majeure | proposed |
| geo-kharg-shipping_lane | IR | kharg | shipping_lane | PMO maritime traffic | pmo.ir | shipping | official | vessel_loading,port_closure | proposed |
| geo-kharg-customs_border | IR | kharg | customs_border | IRICA (Iran Customs) | irica.gov.ir | government_regulator | official | exports,export_license | proposed |
| geo-kharg-insurance_war_risk | US | kharg | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading,sanctions | proposed |
| geo-kharg-storage_operator | IR | kharg | storage_operator | Kharg Island storage tanks | nioc.ir | infrastructure | official | storage_levels,exports | proposed |
| geo-kharg-pricing_hub | — | kharg | pricing_hub | (NIOC term contracts — no exchange) | — | exchange | — | pricing_formula | empty |
| geo-kharg-weather_hazard | IR | kharg | weather_hazard | Iran Meteorological Organization | irimo.ir | weather | official | port_closure,hurricane | unverified |
| geo-kharg-sanctions_enforcement | US | kharg | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions,export_license | proposed |

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
  "phase_index": 10,
  "last_geo_target": "kharg",
  "crosscheck_cursor": 0,
  "last_batch_seq": 78
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_079_geo_target_basra.md` (Fáze 3, Basra / Fao).
