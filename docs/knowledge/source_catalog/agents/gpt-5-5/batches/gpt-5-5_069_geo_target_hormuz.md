# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_069_geo_target_hormuz.md  
**Fáze:** geo_target — krok hormuz (Fáze 3, Strait of Hormuz, chokepoint)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `hormuz` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_067_geo_target_hormuz.md` a zachovává konzervativní statusy: {'proposed': 10, 'empty': 2}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-hormuz-port_authority | IR | hormuz | port_authority | PMO — Bandar Abbas Port | pmo.ir | infrastructure | official | port_closure,vessel_loading | proposed |
| geo-hormuz-pipeline_operator | — | hormuz | pipeline_operator | (no pipeline through strait) | — | infrastructure | — | pipeline_outage | empty |
| geo-hormuz-transit_naval | US | hormuz | transit_naval | US Naval Forces Central Command (5th Fleet) | cusnc.navy.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-hormuz-loading_terminal | IR | hormuz | loading_terminal | Bandar Abbas oil terminals | pmo.ir | infrastructure | official | vessel_loading,exports | proposed |
| geo-hormuz-national_noc | IR | hormuz | national_noc | NIOC | nioc.ir | noc | official | exports,force_majeure,production | proposed |
| geo-hormuz-shipping_lane | OM | hormuz | shipping_lane | Oman Maritime Security Centre | sm.gov.om | shipping | official | vessel_loading,port_closure | proposed |
| geo-hormuz-customs_border | IR | hormuz | customs_border | IRICA (Iran Customs) | irica.gov.ir | government_regulator | official | exports,export_license | proposed |
| geo-hormuz-insurance_war_risk | US | hormuz | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading,sanctions | proposed |
| geo-hormuz-storage_operator | — | hormuz | storage_operator | (Fujairah hub — separate geo target) | — | infrastructure | — | storage_levels | empty |
| geo-hormuz-pricing_hub | AE | hormuz | pricing_hub | DGCX (Dubai crude marker) | dgcx.ae | exchange | official | pricing_formula,exports | proposed |
| geo-hormuz-weather_hazard | OM | hormuz | weather_hazard | PACA Oman (Met / aviation weather) | paca.gov.om | weather | official | hurricane,port_closure | proposed |
| geo-hormuz-sanctions_enforcement | US | hormuz | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions,export_license | proposed |

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
  "phase_index": 1,
  "last_geo_target": "hormuz",
  "crosscheck_cursor": 0,
  "last_batch_seq": 69
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_070_geo_target_bab_el_mandeb.md` (Fáze 3, Bab el-Mandeb).
