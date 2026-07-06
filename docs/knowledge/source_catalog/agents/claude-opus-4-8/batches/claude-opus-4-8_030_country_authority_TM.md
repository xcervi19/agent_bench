# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_030_country_authority_TM.md  
**Fáze:** country_authority — krok TM (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Turkmenistan (`TM`), 10 slotů (`ca-TM-{authority}`). **Extrémně uzavřený režim** — většina zdrojů
nedostupná/nespolehlivá. Plyn dominantně do **Číny** (Central Asia-China pipeline); TAPI aspirační.
Data se reálně čtou přes **China GACC importy**, ne z TM. Jen 1 `proposed`, 4 `unverified`, 5 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-TM-ministry_petroleum | ministry_petroleum | State Concern Turkmengaz | — | government_regulator | official | production, exports | empty |
| ca-TM-noc | noc | Turkmengaz / Turkmennebit | turkmengaz.gov.tm | noc | official | production, exports | unverified |
| ca-TM-mfa | mfa | Ministry of Foreign Affairs | mfa.gov.tm | diplomacy | official | sanctions | unverified |
| ca-TM-customs_export | customs_export | State Customs Service | customs.gov.tm | government_regulator | official | exports | unverified |
| ca-TM-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-TM-port_maritime_authority | port_maritime_authority | Turkmenbashi Port (Caspian) | — | infrastructure | official | vessel_loading | empty |
| ca-TM-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-TM-central_bank | central_bank | Central Bank of Turkmenistan | cbt.tm | government_regulator | official | sanctions | unverified |
| ca-TM-environment_regulator | environment_regulator | — | — | — | — | — | empty |
| ca-TM-coast_guard_navy | coast_guard_navy | — (Caspian) | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TM-noc (Turkmengaz) | plyn produkce (neprůhledná) | závislost na Číně (monopson) | CA-China pipeline (Line A/B/C/D) | unverified — data via CN GACC |

### Unverified / Anti-patterns / poznámky

- **Uzavřený režim:** oficiální TM weby nespolehlivé/nedostupné → většina `unverified`/`empty`.
- **Reálný signál:** čínské importní statistiky (GACC) + gas pipeline flow (Galkynysh field).
- **TAPI** (Turkmenistan-Afghanistan-Pakistan-India) — aspirační, geopoliticky blokovaný.
- Anti-pattern: brát TM oficiální produkční čísla jako fakt; jen China-side data jsou ověřitelná.

### Progress po merge

`last_country: TM`, `last_batch_seq: 30`
