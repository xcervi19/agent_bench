# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_062_country_authority_BD.md  
**Fáze:** country_authority — krok BD (Fáze 2, Bangladesh)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `BD` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_060_country_authority_BD.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-BD-ministry_petroleum | BD | — | ministry_petroleum | Ministry of Power, Energy and Mineral Resources | powerdivision.gov.bd | government_regulator | official | production,imports,storage_levels | proposed |
| ca-BD-noc | BD | — | noc | BAPEX / Petrobangla | petrobangla.org.bd | noc | official | production,imports,force_majeure | proposed |
| ca-BD-mfa | BD | — | mfa | Ministry of Foreign Affairs | mofa.gov.bd | diplomacy | official | sanctions,export_license | proposed |
| ca-BD-customs_export | BD | — | customs_export | National Board of Revenue (Customs) | nbr.gov.bd | government_regulator | official | exports,import_license,imports | proposed |
| ca-BD-upstream_regulator | BD | — | upstream_regulator | Hydrocarbon Unit (Energy Division) | hud.gov.bd | government_regulator | official | production,term_contract | proposed |
| ca-BD-port_maritime_authority | BD | — | port_maritime_authority | Chittagong Port Authority | cpa.gov.bd | infrastructure | official | vessel_loading,port_closure,imports | proposed |
| ca-BD-national_exchange | BD | — | national_exchange | Dhaka Stock Exchange | dsebd.org | exchange | official | pricing_formula | unverified |
| ca-BD-central_bank | BD | — | central_bank | Bangladesh Bank | bb.org.bd | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-BD-environment_regulator | BD | — | environment_regulator | Department of Environment | doe.gov.bd | government_regulator | official | refinery_outage,production | proposed |
| ca-BD-coast_guard_navy | BD | — | coast_guard_navy | Bangladesh Navy | navy.mil.bd | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 58,
  "last_country": "BD",
  "crosscheck_cursor": 0,
  "last_batch_seq": 62
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_063_country_authority_CL.md` (Fáze 2, Chile autority).
