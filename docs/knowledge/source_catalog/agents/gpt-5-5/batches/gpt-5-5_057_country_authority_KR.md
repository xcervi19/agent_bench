# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_057_country_authority_KR.md  
**Fáze:** country_authority — krok KR (Fáze 2, South Korea)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `KR` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_055_country_authority_KR.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-KR-ministry_petroleum | KR | — | ministry_petroleum | MOTIE (Ministry of Trade, Industry and Energy) | motie.go.kr | government_regulator | official | production,imports,storage_levels | proposed |
| ca-KR-noc | KR | — | noc | KNOC | knoc.co.kr | noc | official | production,imports,term_contract | proposed |
| ca-KR-mfa | KR | — | mfa | Ministry of Foreign Affairs | mofa.go.kr | diplomacy | official | sanctions,export_license | proposed |
| ca-KR-customs_export | KR | — | customs_export | Korea Customs Service | customs.go.kr | government_regulator | official | exports,export_license,imports | proposed |
| ca-KR-upstream_regulator | KR | — | upstream_regulator | Korea National Oil Corporation — E&P | knoc.co.kr | government_regulator | official | production,term_contract | proposed |
| ca-KR-port_maritime_authority | KR | — | port_maritime_authority | Ministry of Oceans and Fisheries | mof.go.kr | infrastructure | official | vessel_loading,port_closure,imports | proposed |
| ca-KR-national_exchange | KR | — | national_exchange | Korea Exchange (KRX) | krx.co.kr | exchange | official | pricing_formula,imports | proposed |
| ca-KR-central_bank | KR | — | central_bank | Bank of Korea | bok.or.kr | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-KR-environment_regulator | KR | — | environment_regulator | Ministry of Environment | me.go.kr | government_regulator | official | refinery_outage,production | proposed |
| ca-KR-coast_guard_navy | KR | — | coast_guard_navy | Republic of Korea Navy | navy.mil.kr | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 53,
  "last_country": "KR",
  "crosscheck_cursor": 0,
  "last_batch_seq": 57
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_058_country_authority_SG.md` (Fáze 2, Singapore autority).
