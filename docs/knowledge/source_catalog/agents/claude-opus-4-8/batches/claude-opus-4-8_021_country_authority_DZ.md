# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_021_country_authority_DZ.md  
**Fáze:** country_authority — krok DZ (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Alžírsko (`DZ`), 10 slotů (`ca-DZ-{authority}`). **Klíčový dodavatel plynu do EU** (Medgaz→Španělsko,
Transmed→Itálie) + LNG Arzew/Skikda. **Sonatrach** dominantní; **ALNAFT/ARH** regulace. 7 `proposed`,
2 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-DZ-ministry_petroleum | ministry_petroleum | Ministry of Energy & Mines | energy.gov.dz | government_regulator | official | production, export_license | proposed |
| ca-DZ-noc | noc | Sonatrach | sonatrach.com | noc | official | production, exports, term_contract | proposed |
| ca-DZ-mfa | mfa | Ministry of Foreign Affairs | mae.gov.dz | diplomacy | official | sanctions | unverified |
| ca-DZ-customs_export | customs_export | Direction Générale des Douanes | douane.gov.dz | government_regulator | official | exports | proposed |
| ca-DZ-upstream_regulator | upstream_regulator | ALNAFT | alnaft.gov.dz | government_regulator | official | production, export_license | proposed |
| ca-DZ-port_maritime_authority | port_maritime_authority | Arzew / Skikda ports (Sonatrach) | — | infrastructure | official | vessel_loading, port_closure | unverified |
| ca-DZ-national_exchange | national_exchange | Bourse d'Alger | — | exchange | official | pricing_formula | empty |
| ca-DZ-central_bank | central_bank | Banque d'Algérie | bank-of-algeria.dz | government_regulator | official | sanctions | proposed |
| ca-DZ-environment_regulator | environment_regulator | Ministry of Environment | — | government_regulator | official | refinery_outage | unverified |
| ca-DZ-coast_guard_navy | coast_guard_navy | Algerian Navy / Coast Guard | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-DZ-noc (Sonatrach) | plyn/ropa produkce | **EU gas security** (Medgaz/Transmed) | Arzew, Skikda LNG; Hassi R'Mel | proposed — vysoká priorita pro EU plyn |
| ca-DZ-upstream_regulator (ALNAFT) | licenční data, produkce | — | — | proposed — ARH jako expanze |

### Unverified / poznámky

- **Unverified/empty:** MFA (`mae.gov.dz`), Environment, Arzew/Skikda porty (Sonatrach-operated), Bourse d'Alger (nefunkční pro ropu).
- **ARH** (Autorité de Régulation des Hydrocarbures) jako expanze regulátoru.
- Medgaz (Španělsko) / Transmed-Enrico Mattei (Itálie) = pipeline geo entity (Fáze 3 kandidát).
- Napětí s Marokem (GME pipeline uzavřen 2021) — geo signál.

### Progress po merge

`last_country: DZ`, `last_batch_seq: 21`
