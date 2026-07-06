# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_058_country_authority_SG.md  
**Fáze:** country_authority — krok SG (Fáze 2, Singapore)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `SG` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_056_country_authority_SG.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SG-ministry_petroleum | SG | — | ministry_petroleum | MTI / EMA (Energy Market Authority) | ema.gov.sg | government_regulator | official | production,imports,storage_levels | proposed |
| ca-SG-noc | SG | — | noc | (no NOC — trading hub) | — | noc | — | imports | empty |
| ca-SG-mfa | SG | — | mfa | Ministry of Foreign Affairs | mfa.gov.sg | diplomacy | official | sanctions,export_license | proposed |
| ca-SG-customs_export | SG | — | customs_export | Singapore Customs | customs.gov.sg | government_regulator | official | exports,export_license,imports | proposed |
| ca-SG-upstream_regulator | SG | — | upstream_regulator | EMA — Licensing | ema.gov.sg | government_regulator | official | imports,term_contract | proposed |
| ca-SG-port_maritime_authority | SG | — | port_maritime_authority | MPA Singapore | mpa.gov.sg | infrastructure | official | vessel_loading,port_closure,imports | proposed |
| ca-SG-national_exchange | SG | — | national_exchange | SGX | sgx.com | exchange | official | pricing_formula | unverified |
| ca-SG-central_bank | SG | — | central_bank | Monetary Authority of Singapore | mas.gov.sg | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-SG-environment_regulator | SG | — | environment_regulator | NEA (National Environment Agency) | nea.gov.sg | government_regulator | official | refinery_outage,production | proposed |
| ca-SG-coast_guard_navy | SG | — | coast_guard_navy | Republic of Singapore Navy | mindef.gov.sg | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 54,
  "last_country": "SG",
  "crosscheck_cursor": 0,
  "last_batch_seq": 58
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_059_country_authority_TH.md` (Fáze 2, Thailand autority).
