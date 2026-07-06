# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_032_country_authority_UZ.md  
**Fáze:** country_authority — krok UZ (Fáze 2, Uzbekistan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Dvacátá osmá dávka Fáze 2: `UZ` × 10 typů autorit podle skeleton dimenze.  
Uzbekistan je desk-critical pro Central Asia gas balances, Uzbekneftegaz production, regional pipeline swaps, domestic reform signals, customs/border flows and sanctions-sensitive Russia/China/Caspian routing.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-UZ-ministry_petroleum | UZ | — | ministry_petroleum | Ministry of Energy of Uzbekistan | gov.uz/en/minenergy | government_regulator | official | production, exports, imports, quota_rhetoric | proposed |
| ca-UZ-noc | UZ | — | noc | Uzbekneftegaz JSC | ung.uz | noc | official | production, exports, force_majeure, term_contract, vessel_loading | unverified |
| ca-UZ-mfa | UZ | — | mfa | Ministry of Foreign Affairs Uzbekistan | mfa.uz | diplomacy | official | sanctions, export_license, quota_rhetoric | proposed |
| ca-UZ-customs_export | UZ | — | customs_export | Customs Committee of Uzbekistan | customs.uz | government_regulator | official | exports, imports, export_license, sanctions | unverified |
| ca-UZ-upstream_regulator | UZ | — | upstream_regulator | Energy Market Development and Regulatory Agency | gov.uz/en/emdra | government_regulator | official | production, force_majeure, export_license | proposed |
| ca-UZ-port_maritime_authority | UZ | — | port_maritime_authority | — | — | infrastructure | official | vessel_loading, port_closure, exports | empty |
| ca-UZ-national_exchange | UZ | — | national_exchange | Tashkent Republican Stock Exchange | uzse.uz | exchange | data_feed | pricing_formula | unverified |
| ca-UZ-central_bank | UZ | — | central_bank | Central Bank of Uzbekistan | cbu.uz | government_regulator | official | sanctions, pricing_formula, imports, exports | proposed |
| ca-UZ-environment_regulator | UZ | — | environment_regulator | Ministry of Ecology, Environmental Protection and Climate Change | gov.uz/en/eco | government_regulator | official | refinery_outage, force_majeure, port_closure | unverified |
| ca-UZ-coast_guard_navy | UZ | — | coast_guard_navy | — | — | government_regulator | official | port_closure, vessel_loading, sanctions | empty |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-UZ-ministry_petroleum | Ministry of Energy is the primary oil/gas policy source. | Energy reforms and Central Asia gas balance relevance. | Logistics indirect. | proposed |
| ca-UZ-noc | Uzbekneftegaz is the state hydrocarbon company. | State reform and pipeline supply relevance. | Direct production/processing relevance, domain needs validation. | unverified |
| ca-UZ-upstream_regulator | EMDRA is the energy market regulator. | Reform/licensing signal. | Less direct for physical cargoes. | proposed |
| ca-UZ-port_maritime_authority | Uzbekistan is landlocked. | — | No direct maritime authority slot. | empty |
| ca-UZ-coast_guard_navy | Landlocked country; no relevant coast guard/navy public slot. | Border/security may matter but belongs elsewhere. | — | empty |

---

### Unverified / Anti-patterns

- `ca-UZ-noc`, `ca-UZ-customs_export`, `ca-UZ-national_exchange`, and `ca-UZ-environment_regulator` need manual domain/path validation before whitelist.
- `ca-UZ-port_maritime_authority` and `ca-UZ-coast_guard_navy` are `empty`: do not invent maritime sources for a landlocked country.
- Treat Uzbekistan supply claims as partial until cross-checked with buyer-country data, pipeline operators, customs and regional energy ministries.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 28,
  "last_country": "UZ",
  "crosscheck_cursor": 0,
  "last_batch_seq": 32
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_033_country_authority_TR.md` (Fáze 2, Turkey autority).
