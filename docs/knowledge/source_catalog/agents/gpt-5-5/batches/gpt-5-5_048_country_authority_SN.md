# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_048_country_authority_SN.md  
**Fáze:** country_authority — krok SN (Fáze 2, Senegal)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `SN` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_046_country_authority_SN.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SN-ministry_petroleum | SN | — | ministry_petroleum | Ministry of Petroleum and Energy | energie.gouv.sn | government_regulator | official | production,imports,storage_levels | proposed |
| ca-SN-noc | SN | — | noc | (no NOC — import hub) | — | noc | — | imports | empty |
| ca-SN-mfa | SN | — | mfa | Ministry of Foreign Affairs | diplomatie.gouv.sn | diplomacy | official | sanctions,export_license | proposed |
| ca-SN-customs_export | SN | — | customs_export | Customs Senegal (DGD) | douanes.sn | government_regulator | official | exports,export_license,imports | proposed |
| ca-SN-upstream_regulator | SN | — | upstream_regulator | COS-Petrogaz (exploration JV) | cospetrogaz.sn | government_regulator | official | production,term_contract | unverified |
| ca-SN-port_maritime_authority | SN | — | port_maritime_authority | Port Autonome de Dakar | portdedakar.sn | infrastructure | official | vessel_loading,port_closure,imports | proposed |
| ca-SN-national_exchange | SN | — | national_exchange | BRVM (regional exchange) | brvm.org | exchange | official | pricing_formula | unverified |
| ca-SN-central_bank | SN | — | central_bank | Central Bank of West African States (BCEAO) | bceao.int | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-SN-environment_regulator | SN | — | environment_regulator | Ministry of Environment | environnement.gouv.sn | government_regulator | official | refinery_outage,production | proposed |
| ca-SN-coast_guard_navy | SN | — | coast_guard_navy | Senegalese Navy | gendarmerie.sn | government_regulator | official | port_closure,vessel_loading | unverified |

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
  "phase_index": 44,
  "last_country": "SN",
  "crosscheck_cursor": 0,
  "last_batch_seq": 48
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_049_country_authority_GQ.md` (Fáze 2, Equatorial Guinea autority).
