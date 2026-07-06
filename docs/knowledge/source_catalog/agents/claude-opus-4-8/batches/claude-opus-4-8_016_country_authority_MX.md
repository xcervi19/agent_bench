# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_016_country_authority_MX.md  
**Fáze:** country_authority — krok MX (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Mexiko (`MX`), 10 slotů (`ca-MX-{authority}`). Trading: **Pemex klesající produkce** + vysoký dluh,
**Maya heavy crude**, Dos Bocas rafinerie (snižuje export syrové), **Hacienda ropný hedge** (největší
sovereign hedge). CNH oslabena reformami. 9 `proposed`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-MX-ministry_petroleum | ministry_petroleum | Secretaría de Energía (SENER) | gob.mx/sener | government_regulator | official | production, export_license | proposed |
| ca-MX-noc | noc | Pemex | pemex.com | noc | official | production, exports, refinery_outage | proposed |
| ca-MX-mfa | mfa | Secretaría de Relaciones Exteriores (SRE) | gob.mx/sre | diplomacy | official | sanctions | proposed |
| ca-MX-customs_export | customs_export | Agencia Nacional de Aduanas (ANAM) | anam.gob.mx | government_regulator | official | exports | proposed |
| ca-MX-upstream_regulator | upstream_regulator | Comisión Nacional de Hidrocarburos (CNH) | gob.mx/cnh | government_regulator | official | production | proposed |
| ca-MX-port_maritime_authority | port_maritime_authority | SEMAR / ASIPONA ports | gob.mx/semar | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-MX-national_exchange | national_exchange | Bolsa Mexicana de Valores (BMV) | bmv.com.mx | exchange | official | pricing_formula | proposed |
| ca-MX-central_bank | central_bank | Banco de México (Banxico) | banxico.org.mx | government_regulator | official | — | proposed |
| ca-MX-environment_regulator | environment_regulator | ASEA (energy sector safety/env) | gob.mx/asea | government_regulator | official | refinery_outage | proposed |
| ca-MX-coast_guard_navy | coast_guard_navy | — (SEMAR overlaps port slot) | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-MX-noc (Pemex) | klesající produkce, dluh | palivová soběstačnost (Dos Bocas) | Maya export (US Gulf refiners) | proposed — nejvyšší priorita |
| ca-MX-upstream_regulator (CNH) | produkční data, kontrakty | oslabena reformami (AMLO/Sheinbaum) | — | proposed |

### Unverified / poznámky

- **`ca-MX-coast_guard_navy` = empty:** SEMAR (námořnictvo) řeší i přístavy → ve slotu port_maritime;
  neduplikovat do coast_guard.
- **Hacienda oil hedge** (Ministry of Finance program) — cenný makro signál, ale finanční tajný;
  sledovat přes SHCP zprávy, ne jako autoritu.
- Dos Bocas + Deer Park (Pemex US) snižují export syrové Maya → import produktů klesá.
- CNH pod politickým tlakem — data hodnota může klesat.

### Progress po merge

`last_country: MX`, `last_batch_seq: 16`
