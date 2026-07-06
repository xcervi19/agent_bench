# Catalog batch

**Agent:** gpt-5-5 (GPT-5.5)  
**Soubor:** gpt-5-5_056_country_authority_JP.md  
**Fáze:** country_authority — krok JP (Fáze 2, Japan)  
**Datum:** 2026-07-06  

---

## Shrnutí

Autonomně vygenerovaná dávka Fáze 2 pro `JP` podle skeleton dimenze. Zdroje byly převzaty z referenční auditní dávky `composer-2-5_054_country_authority_JP.md` a zachovávají konzervativní statusy `proposed`, `unverified` a `empty`.

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-JP-ministry_petroleum | JP | — | ministry_petroleum | METI (Ministry of Economy, Trade and Industry) | meti.go.jp | government_regulator | official | production,imports,storage_levels | proposed |
| ca-JP-noc | JP | — | noc | JOGMEC | jogmec.go.jp | noc | official | production,imports,term_contract | proposed |
| ca-JP-mfa | JP | — | mfa | Ministry of Foreign Affairs | mofa.go.jp | diplomacy | official | sanctions,export_license | proposed |
| ca-JP-customs_export | JP | — | customs_export | Japan Customs (NACS) | customs.go.jp | government_regulator | official | exports,export_license,imports | proposed |
| ca-JP-upstream_regulator | JP | — | upstream_regulator | Agency for Natural Resources and Energy (ANRE) | meti.go.jp | government_regulator | official | production,term_contract | proposed |
| ca-JP-port_maritime_authority | JP | — | port_maritime_authority | MLIT (Maritime Bureau) | mlit.go.jp | infrastructure | official | vessel_loading,port_closure,imports | proposed |
| ca-JP-national_exchange | JP | — | national_exchange | TOCOM / Osaka Exchange | tocom.or.jp | exchange | official | pricing_formula,imports | proposed |
| ca-JP-central_bank | JP | — | central_bank | Bank of Japan | boj.or.jp | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-JP-environment_regulator | JP | — | environment_regulator | Ministry of the Environment | env.go.jp | government_regulator | official | refinery_outage,production | proposed |
| ca-JP-coast_guard_navy | JP | — | coast_guard_navy | Japan Coast Guard | kcg.go.jp | government_regulator | official | port_closure,vessel_loading | proposed |

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
  "phase_index": 52,
  "last_country": "JP",
  "crosscheck_cursor": 0,
  "last_batch_seq": 56
}
```

Po merge této dávky → **další dávka:** `gpt-5-5_057_country_authority_KR.md` (Fáze 2, South Korea autority).
