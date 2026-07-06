# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_037_country_authority_IT.md  
**Fáze:** country_authority — krok IT (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Itálie (`IT`), 10 slotů (`ca-IT-{authority}`). **Eni** major (africký plyn: Libye, Transmed/Alžírsko,
Zohr/Egypt). Středomořské **gas hub** ambice (Transmed, TAP endpoint, TAL Trieste→střední Evropa).
PSV gas hub. 9 `proposed`, 1 `unverified`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-IT-ministry_petroleum | ministry_petroleum | Ministry of Environment & Energy Security (MASE) | mase.gov.it | government_regulator | official | imports, production | proposed |
| ca-IT-noc | noc | Eni | eni.com | noc | official | production, imports, term_contract | proposed |
| ca-IT-mfa | mfa | Ministry of Foreign Affairs (Farnesina) | esteri.it | diplomacy | official | sanctions | proposed |
| ca-IT-customs_export | customs_export | Agenzia delle Dogane | adm.gov.it | government_regulator | official | imports, exports | proposed |
| ca-IT-upstream_regulator | upstream_regulator | ARERA (energy regulator) | arera.it | government_regulator | official | pricing_formula | proposed |
| ca-IT-port_maritime_authority | port_maritime_authority | Port System Authorities (Trieste/Genoa) | — | infrastructure | official | vessel_loading, pipeline_outage | unverified |
| ca-IT-national_exchange | national_exchange | GME (Gestore Mercati Energetici) | mercatoelettrico.org | exchange | official | pricing_formula | proposed |
| ca-IT-central_bank | central_bank | Banca d'Italia | bancaditalia.it | government_regulator | official | sanctions | proposed |
| ca-IT-environment_regulator | environment_regulator | ISPRA | isprambiente.gov.it | government_regulator | official | refinery_outage | proposed |
| ca-IT-coast_guard_navy | coast_guard_navy | Italian Coast Guard (Guardia Costiera) | guardiacostiera.gov.it | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IT-noc (Eni) | africká produkce | **Transmed/Alžírsko, Zohr/Egypt, Libye** | Mazara del Vallo landing | proposed — nejvyšší priorita |
| ca-IT-port_maritime_authority | — | TAL → Rakousko/Německo | Trieste (TAL), Genoa, Augusta refining | unverified — port authority domény |

### Unverified / poznámky

- **`ca-IT-port_maritime_authority` = unverified:** italské přístavy jednotlivé Autorità di Sistema Portuale — ověřit konkrétní (Trieste = TAL pipeline start).
- **PSV** (Punto di Scambio Virtuale) gas hub — Itálie usiluje být "jižní EU gas hub" (Mattei plán).
- **TAP** (Trans Adriatic Pipeline) endpoint Puglia — ázerbájdžánský plyn; **Transmed** (Alžírsko).
- GME = plyn/elektřina burza; PSV pricing.

### Progress po merge

`last_country: IT`, `last_batch_seq: 37`
