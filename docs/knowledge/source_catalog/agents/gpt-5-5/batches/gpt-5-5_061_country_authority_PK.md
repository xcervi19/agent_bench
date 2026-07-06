# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_061_country_authority_PK.md  
**Fáze:** country_authority — krok PK (Fáze 2, Pakistan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `PK` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_059_country_authority_PK.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-PK-ministry_petroleum | PK | — | ministry_petroleum | Ministry of Energy (Petroleum Division) | mop.gov.pk | government_regulator | official | production,imports,storage_levels | proposed |
| ca-PK-noc | PK | — | noc | OGDC (Oil & Gas Development Company) | ogdcl.com | noc | official | production,exports,force_majeure | proposed |
| ca-PK-mfa | PK | — | mfa | Ministry of Foreign Affairs | mofa.gov.pk | diplomacy | official | sanctions,export_license | proposed |
| ca-PK-customs_export | PK | — | customs_export | Federal Board of Revenue (Customs) | fbr.gov.pk | government_regulator | official | exports,export_license,imports | proposed |
| ca-PK-upstream_regulator | PK | — | upstream_regulator | DGPC (Directorate General of Petroleum Concessions) | dgpc.gov.pk | government_regulator | official | production,term_contract | proposed |
| ca-PK-port_maritime_authority | PK | — | port_maritime_authority | Karachi Port Trust | kpt.gov.pk | infrastructure | official | vessel_loading,port_closure,imports | proposed |
| ca-PK-national_exchange | PK | — | national_exchange | Pakistan Stock Exchange | psx.com.pk | exchange | official | pricing_formula | unverified |
| ca-PK-central_bank | PK | — | central_bank | State Bank of Pakistan | sbp.org.pk | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-PK-environment_regulator | PK | — | environment_regulator | Pakistan EPA | pak-epa.org | government_regulator | official | refinery_outage,production | proposed |
| ca-PK-coast_guard_navy | PK | — | coast_guard_navy | Pakistan Navy | paknavy.gov.pk | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 57,
  "last_country": "PK",
  "crosscheck_cursor": 0,
  "last_batch_seq": 61
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_062_country_authority_BD.md` (Fáze 2, Bangladesh autority).
