# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_055_country_authority_IL.md  
**Fáze:** country_authority — krok IL (Fáze 2, Israel)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `IL` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_053_country_authority_IL.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IL-ministry_petroleum | IL | — | ministry_petroleum | Ministry of Energy | gov.il/en/departments/ministry_of_energy | government_regulator | official | production,imports,storage_levels | proposed |
| ca-IL-noc | IL | — | noc | (no NOC — NewMed/Energean private) | — | noc | — | production,exports | empty |
| ca-IL-mfa | IL | — | mfa | Ministry of Foreign Affairs | gov.il/mfa | diplomacy | official | sanctions,export_license | proposed |
| ca-IL-customs_export | IL | — | customs_export | Israel Tax Authority (Customs) | taxes.gov.il | government_regulator | official | exports,export_license,imports | proposed |
| ca-IL-upstream_regulator | IL | — | upstream_regulator | Petroleum Commissioner (Ministry of Energy) | energy.economy.gov.il | government_regulator | official | production,term_contract | proposed |
| ca-IL-port_maritime_authority | IL | — | port_maritime_authority | Israel Ports Company | ports.org.il | infrastructure | official | vessel_loading,port_closure,imports | proposed |
| ca-IL-national_exchange | IL | — | national_exchange | Tel Aviv Stock Exchange (TASE) | tase.co.il | exchange | official | pricing_formula | unverified |
| ca-IL-central_bank | IL | — | central_bank | Bank of Israel | boi.org.il | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-IL-environment_regulator | IL | — | environment_regulator | Ministry of Environmental Protection | gov.il/en/departments/epa | government_regulator | official | refinery_outage,production | proposed |
| ca-IL-coast_guard_navy | IL | — | coast_guard_navy | Israeli Navy | navy.idf.il | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 51,
  "last_country": "IL",
  "crosscheck_cursor": 0,
  "last_batch_seq": 55
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_056_country_authority_JP.md` (Fáze 2, Japan autority).
