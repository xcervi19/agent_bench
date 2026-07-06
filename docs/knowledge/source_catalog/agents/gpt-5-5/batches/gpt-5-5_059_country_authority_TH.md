# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_059_country_authority_TH.md  
**Fáze:** country_authority — krok TH (Fáze 2, Thailand)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `TH` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_057_country_authority_TH.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TH-ministry_petroleum | TH | — | ministry_petroleum | Ministry of Energy | energy.go.th | government_regulator | official | production,imports,storage_levels | proposed |
| ca-TH-noc | TH | — | noc | PTTEP (PTT Exploration and Production) | pttep.com | noc | official | production,exports,force_majeure | proposed |
| ca-TH-mfa | TH | — | mfa | Ministry of Foreign Affairs | mfa.go.th | diplomacy | official | sanctions,export_license | proposed |
| ca-TH-customs_export | TH | — | customs_export | Thai Customs Department | customs.go.th | government_regulator | official | exports,export_license,imports | proposed |
| ca-TH-upstream_regulator | TH | — | upstream_regulator | Department of Mineral Fuels (DMF) | dmf.go.th | government_regulator | official | production,term_contract | proposed |
| ca-TH-port_maritime_authority | TH | — | port_maritime_authority | Port Authority of Thailand | port.co.th | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-TH-national_exchange | TH | — | national_exchange | TFEX | tfex.co.th | exchange | official | pricing_formula | proposed |
| ca-TH-central_bank | TH | — | central_bank | Bank of Thailand | bot.or.th | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-TH-environment_regulator | TH | — | environment_regulator | Ministry of Natural Resources and Environment | mnre.go.th | government_regulator | official | refinery_outage,production | proposed |
| ca-TH-coast_guard_navy | TH | — | coast_guard_navy | Royal Thai Navy | navy.mi.th | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 55,
  "last_country": "TH",
  "crosscheck_cursor": 0,
  "last_batch_seq": 59
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_060_country_authority_VN.md` (Fáze 2, Vietnam autority).
