# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_063_country_authority_EC.md  
**Fáze:** country_authority — krok EC (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Ekvádor (`EC`), 10 slotů (`ca-EC-{authority}`). **Bývalý OPEC** (odešel 2020); Petroecuador NOC, Oriente/Napo
crude; **SOTE/OCP Amazon pipeline** = force majeure riziko (sesuvy/erozn). Yasuní referendum (blok 43 stop). 7 `proposed`, 2 `unverified`, 1 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-EC-ministry_petroleum | ministry_petroleum | Ministry of Energy & Mines | recursosyenergia.gob.ec | government_regulator | official | production, export_license | proposed |
| ca-EC-noc | noc | Petroecuador | eppetroecuador.ec | noc | official | production, exports, force_majeure | proposed |
| ca-EC-mfa | mfa | Ministry of Foreign Affairs | cancilleria.gob.ec | diplomacy | official | sanctions | unverified |
| ca-EC-customs_export | customs_export | SENAE (Aduana) | aduana.gob.ec | government_regulator | official | exports | proposed |
| ca-EC-upstream_regulator | upstream_regulator | ARCERNNR / Ministry | controlhidrocarburos.gob.ec | government_regulator | official | production, export_license | unverified |
| ca-EC-port_maritime_authority | port_maritime_authority | Balao terminal (Esmeraldas) / SPTMF | — | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-EC-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-EC-central_bank | central_bank | Banco Central del Ecuador | bce.fin.ec | government_regulator | official | sanctions | proposed |
| ca-EC-environment_regulator | environment_regulator | Ministry of Environment (MAATE) | ambiente.gob.ec | government_regulator | official | force_majeure, refinery_outage | proposed |
| ca-EC-coast_guard_navy | coast_guard_navy | Ecuadorian Navy (DIRNEA) | armada.mil.ec | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-EC-noc (Petroecuador) | Oriente/Napo crude | Yasuní blok 43 stop (referendum) | **SOTE/OCP Amazon pipeline** — erozn/sesuvy | proposed — force majeure supply signál |

### Poznámky

- **Amazon pipeline (SOTE/OCP)** = opakované přerušení erozí řeky Coca → force majeure na Oriente/Napo exportu (Balao).
- **Yasuní blok 43** zastaven referendem 2023 → strukturální pokles produkce.
- Bývalý OPEC (odešel 2020) → produkce mimo kvótový systém.

### Progress po merge

`last_country: EC`, `last_batch_seq: 63`
