# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_057_country_authority_TH.md  
**Fáze:** country_authority — krok TH (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Thajsko (`TH`), 10 slotů (`ca-TH-{authority}`). **PTT/PTTEP** NOC, rafinér + rostoucí LNG importér; domácí
plyn (Gulf of Thailand) klesá. DMF regulátor. 8 `proposed`, 1 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-TH-ministry_petroleum | ministry_petroleum | Ministry of Energy | energy.go.th | government_regulator | official | production, imports | proposed |
| ca-TH-noc | noc | PTT / PTTEP | pttplc.com | noc | official | production, imports, refinery_outage | proposed |
| ca-TH-mfa | mfa | Ministry of Foreign Affairs | mfa.go.th | diplomacy | official | sanctions | proposed |
| ca-TH-customs_export | customs_export | Thai Customs Department | customs.go.th | government_regulator | official | imports | proposed |
| ca-TH-upstream_regulator | upstream_regulator | Dept of Mineral Fuels (DMF) | dmf.go.th | government_regulator | official | production, export_license | proposed |
| ca-TH-port_maritime_authority | port_maritime_authority | Port Authority of Thailand / Marine Dept | port.co.th | infrastructure | official | vessel_loading, port_closure | unverified |
| ca-TH-national_exchange | national_exchange | — (SET financial only) | — | — | — | — | empty |
| ca-TH-central_bank | central_bank | Bank of Thailand | bot.or.th | government_regulator | official | sanctions | proposed |
| ca-TH-environment_regulator | environment_regulator | Ministry of Natural Resources & Env | mnre.go.th | government_regulator | official | refinery_outage | proposed |
| ca-TH-coast_guard_navy | coast_guard_navy | Thai-MECC (Maritime Enforcement) | — | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-TH-noc (PTT/PTTEP) | Gulf of Thailand gas decline | Malacca import závislost | rafinerie, LNG terminály | proposed — rostoucí LNG demand |
| ca-TH-upstream_regulator (DMF) | Erawan/Bongkot pole | — | — | proposed |

### Poznámky

- Domácí plyn (Gulf of Thailand — Erawan/Bongkot) klesá → **rostoucí LNG import** (JKM demand signál).
- PTTEP i regionální upstream (Myanmar plyn dovoz) → geopolitická citlivost.
- SET = jen finanční burza (empty pro energy komodity).

### Progress po merge

`last_country: TH`, `last_batch_seq: 57`
