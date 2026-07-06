# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_053_country_authority_MR.md  
**Fáze:** country_authority — krok MR (Fáze 2, Mauritania)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `MR` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_051_country_authority_MR.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-MR-ministry_petroleum | MR | — | ministry_petroleum | Ministry of Petroleum, Energy and Mines | mpem.gov.mr | government_regulator | official | production,exports | unverified |
| ca-MR-noc | MR | — | noc | SMH (Société Mauritanienne des Hydrocarbures) | smh.mr | noc | official | production,exports,force_majeure | unverified |
| ca-MR-mfa | MR | — | mfa | Ministry of Foreign Affairs | diplomatie.gov.mr | diplomacy | official | sanctions,export_license | unverified |
| ca-MR-customs_export | MR | — | customs_export | General Directorate of Customs | douanes.gov.mr | government_regulator | official | exports,export_license,imports | unverified |
| ca-MR-upstream_regulator | MR | — | upstream_regulator | Hydrocarbons Directorate | mpem.gov.mr | government_regulator | official | production,term_contract | unverified |
| ca-MR-port_maritime_authority | MR | — | port_maritime_authority | Port of Nouakchott / Nouadhibou | portsnouakchott.mr | infrastructure | official | vessel_loading,port_closure,exports | unverified |
| ca-MR-national_exchange | MR | — | national_exchange | (none) | — | exchange | — | — | empty |
| ca-MR-central_bank | MR | — | central_bank | Central Bank of Mauritania | bcm.mr | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-MR-environment_regulator | MR | — | environment_regulator | Ministry of Environment | environnement.gov.mr | government_regulator | official | refinery_outage,production | unverified |
| ca-MR-coast_guard_navy | MR | — | coast_guard_navy | Mauritanian Navy | defense.gov.mr | government_regulator | official | port_closure,vessel_loading | unverified |

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
  "phase_index": 49,
  "last_country": "MR",
  "crosscheck_cursor": 0,
  "last_batch_seq": 53
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_054_country_authority_BH.md` (Fáze 2, Bahrain autority).
