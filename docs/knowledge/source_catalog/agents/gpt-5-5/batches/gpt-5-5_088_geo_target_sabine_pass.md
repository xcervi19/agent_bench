# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_088_geo_target_sabine_pass.md  
**Fáze:** geo_target — krok sabine_pass (Fáze 3, Sabine Pass, us_gulf_hub)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná GEO dávka pro `sabine_pass` podle skeleton dimenze. Obsah je odvozen ze strukturované referenční dávky `composer-2-5_086_geo_target_sabine_pass.md` a zachovává konzervativní statusy: {'proposed': 9, 'empty': 2, 'unverified': 1}.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-sabine_pass-port_authority | US | sabine_pass | port_authority | Sabine-Neches Navigation District | navigationdistrict.org | infrastructure | official | vessel_loading,port_closure | proposed |
| geo-sabine_pass-pipeline_operator | US | sabine_pass | pipeline_operator | Cheniere feedgas pipelines | cheniere.com | infrastructure | official | pipeline_outage,exports | proposed |
| geo-sabine_pass-transit_naval | US | sabine_pass | transit_naval | US Coast Guard | uscg.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-sabine_pass-loading_terminal | US | sabine_pass | loading_terminal | Cheniere Sabine Pass LNG | cheniere.com | infrastructure | official | vessel_loading,exports,force_majeure | proposed |
| geo-sabine_pass-national_noc | — | sabine_pass | national_noc | (LNG export — no NOC) | — | noc | — | exports | empty |
| geo-sabine_pass-shipping_lane | US | sabine_pass | shipping_lane | Sabine-Neches channel traffic | navigationdistrict.org | shipping | official | vessel_loading,port_closure | proposed |
| geo-sabine_pass-customs_border | US | sabine_pass | customs_border | Customs and Border Protection (CBP) | cbp.gov | government_regulator | official | exports,export_license | proposed |
| geo-sabine_pass-insurance_war_risk | US | sabine_pass | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | port_closure | proposed |
| geo-sabine_pass-storage_operator | — | sabine_pass | storage_operator | (LNG — no crude storage) | — | infrastructure | — | — | empty |
| geo-sabine_pass-pricing_hub | US | sabine_pass | pricing_hub | CME Group (Henry Hub / LNG linkage) | cmegroup.com | exchange | official | pricing_formula,exports | unverified |
| geo-sabine_pass-weather_hazard | US | sabine_pass | weather_hazard | NOAA / NWS (Gulf hurricanes) | weather.gov | weather | official | port_closure,hurricane,force_majeure | proposed |
| geo-sabine_pass-sanctions_enforcement | US | sabine_pass | sanctions_enforcement | FERC (LNG export authorization) | ferc.gov | government_regulator | official | export_license,sanctions | proposed |

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
  "phase_index": 20,
  "last_geo_target": "sabine_pass",
  "crosscheck_cursor": 0,
  "last_batch_seq": 88
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_089_geo_target_freeport.md` (Fáze 3, Freeport LNG).
