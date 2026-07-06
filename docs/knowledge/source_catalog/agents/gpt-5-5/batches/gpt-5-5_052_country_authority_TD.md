# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_052_country_authority_TD.md  
**Fáze:** country_authority — krok TD (Fáze 2, Chad)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `TD` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_050_country_authority_TD.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TD-ministry_petroleum | TD | — | ministry_petroleum | Ministry of Petroleum and Energy | energie.gouv.td | government_regulator | official | production,exports | unverified |
| ca-TD-noc | TD | — | noc | Société des Hydrocarbures du Tchad (SHT) | sht.td | noc | official | production,exports,force_majeure | unverified |
| ca-TD-mfa | TD | — | mfa | Ministry of Foreign Affairs | diplomatie.gouv.td | diplomacy | official | sanctions,export_license | unverified |
| ca-TD-customs_export | TD | — | customs_export | Chad Customs | douanes.td | government_regulator | official | exports,export_license | unverified |
| ca-TD-upstream_regulator | TD | — | upstream_regulator | Hydrocarbons Licensing (Ministry) | energie.gouv.td | government_regulator | official | production,term_contract | unverified |
| ca-TD-port_maritime_authority | TD | — | port_maritime_authority | (landlocked — pipeline to Cameroon) | — | infrastructure | — | exports | empty |
| ca-TD-national_exchange | TD | — | national_exchange | (none) | — | exchange | — | — | empty |
| ca-TD-central_bank | TD | — | central_bank | BEAC (Central African) | beac.int | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-TD-environment_regulator | TD | — | environment_regulator | Ministry of Environment | environnement.gouv.td | government_regulator | official | refinery_outage,production | unverified |
| ca-TD-coast_guard_navy | TD | — | coast_guard_navy | (landlocked) | — | government_regulator | — | — | empty |

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
  "phase_index": 48,
  "last_country": "TD",
  "crosscheck_cursor": 0,
  "last_batch_seq": 52
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_053_country_authority_MR.md` (Fáze 2, Mauritania autority).
