# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_031_country_authority_UZ.md  
**Fáze:** country_authority — krok UZ (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Uzbekistán (`UZ`), 10 slotů (`ca-UZ-{authority}`). Landlocked plynový producent; **stal se net
importérem plynu z Ruska (2023 swap)** — signál. Tranzit CA-China pipeline. 6 `proposed`, 1 `unverified`,
3 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-UZ-ministry_petroleum | ministry_petroleum | Ministry of Energy | minenergy.uz | government_regulator | official | production, imports | proposed |
| ca-UZ-noc | noc | Uzbekneftegaz | ung.uz | noc | official | production, imports | proposed |
| ca-UZ-mfa | mfa | Ministry of Foreign Affairs | mfa.uz | diplomacy | official | sanctions | proposed |
| ca-UZ-customs_export | customs_export | State Customs Committee | customs.uz | government_regulator | official | exports, imports | proposed |
| ca-UZ-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-UZ-port_maritime_authority | port_maritime_authority | — (landlocked) | — | — | — | — | empty |
| ca-UZ-national_exchange | national_exchange | Uzbek Republican Stock Exchange | uzse.uz | exchange | official | pricing_formula | unverified |
| ca-UZ-central_bank | central_bank | Central Bank of Uzbekistan | cbu.uz | government_regulator | official | sanctions | proposed |
| ca-UZ-environment_regulator | environment_regulator | State Committee for Ecology | — | government_regulator | official | refinery_outage | empty |
| ca-UZ-coast_guard_navy | coast_guard_navy | — (landlocked) | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-UZ-noc (Uzbekneftegaz) | domácí plyn (klesající) | **import z Ruska od 2023** | CA-China pipeline tranzit | proposed — role reversal signál |

### Unverified / poznámky

- **Net gas importér** od 2023 (Gazprom swap) — strukturální obrat, geopolitický signál (ruský vliv).
- **Unverified:** burza (`uzse.uz`); landlocked → 3 sloty `empty`.

### Progress po merge

`last_country: UZ`, `last_batch_seq: 31`
