# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_049_country_authority_GQ.md  
**Fáze:** country_authority — krok GQ (Fáze 2, Equatorial Guinea)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `GQ` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_047_country_authority_GQ.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GQ-ministry_petroleum | GQ | — | ministry_petroleum | Ministry of Mines and Hydrocarbons | mmh.gob.gq | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-GQ-noc | GQ | — | noc | GEPetrol (National Oil Company) | gepetrol.gq | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-GQ-mfa | GQ | — | mfa | Ministry of Foreign Affairs | maege.gq | diplomacy | official | sanctions,export_license | unverified |
| ca-GQ-customs_export | GQ | — | customs_export | General Directorate of Customs | aduana.gq | government_regulator | official | exports,export_license,imports | unverified |
| ca-GQ-upstream_regulator | GQ | — | upstream_regulator | Ministry — Hydrocarbons Licensing | mmh.gob.gq | government_regulator | official | production,term_contract | proposed |
| ca-GQ-port_maritime_authority | GQ | — | port_maritime_authority | Port of Malabo / Bata | ports.gq | infrastructure | official | vessel_loading,port_closure,exports | unverified |
| ca-GQ-national_exchange | GQ | — | national_exchange | (none) | — | exchange | — | — | empty |
| ca-GQ-central_bank | GQ | — | central_bank | Bank of Central African States (BEAC) | beac.int | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-GQ-environment_regulator | GQ | — | environment_regulator | Ministry of Environment | medioambiente.gob.gq | government_regulator | official | refinery_outage,production | unverified |
| ca-GQ-coast_guard_navy | GQ | — | coast_guard_navy | Equatorial Guinea Navy | defensa.gob.gq | government_regulator | official | port_closure,vessel_loading | unverified |

---

### Cross-check (3 perspektivy)

- Supply: prioritizovat ministerstvo, NOC/upstream regulator a produkční/exportní signály.
- Geopolitics: používat MFA, customs a central bank jako sankční, licenční a platební kontext.
- Logistics: port/coast guard sloty používat jen po ověření domény; `empty` sloty nevynucovat náhradními komerčními zdroji.

---

### Unverified / Anti-patterns

- `unverified` položky před whitelistem ručně validovat proti oficiálním doménám a aktuální dostupnosti.
- `empty` položky neplnit soukromými firmami, pokud chybí přímý státní/NOC nebo maritime ekvivalent.
- Market/exchange zdroje nejsou důkaz fyzických toků bez triangulace s official, operator, port a shipping zdroji.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 45,
  "last_country": "GQ",
  "crosscheck_cursor": 0,
  "last_batch_seq": 49
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_050_country_authority_CG.md` (Fáze 2, Congo autority).
