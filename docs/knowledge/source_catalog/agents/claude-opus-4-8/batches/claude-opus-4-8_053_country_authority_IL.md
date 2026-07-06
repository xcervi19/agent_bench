# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_053_country_authority_IL.md  
**Fáze:** country_authority — krok IL (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Izrael (`IL`), 10 slotů (`ca-IL-{authority}`). **Plynový producent** (Leviathan, Tamar, Karish) → export do
EG/JO; geopoliticky citlivé (východní Středomoří, konflikt → shut-in Tamar riziko). Bez NOC. 6 `proposed`, 2 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-IL-ministry_petroleum | ministry_petroleum | Ministry of Energy & Infrastructure | gov.il | government_regulator | official | production, export_license | proposed |
| ca-IL-noc | noc | — (no NOC; Chevron/NewMed operate) | — | — | — | — | empty |
| ca-IL-mfa | mfa | Ministry of Foreign Affairs | gov.il | diplomacy | official | sanctions | proposed |
| ca-IL-customs_export | customs_export | Israel Tax Authority (Customs) | gov.il | government_regulator | official | exports | unverified |
| ca-IL-upstream_regulator | upstream_regulator | Natural Gas Authority (MoE) | gov.il | government_regulator | official | production | proposed |
| ca-IL-port_maritime_authority | port_maritime_authority | Israel Ports (Haifa/Ashdod) | gov.il | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-IL-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-IL-central_bank | central_bank | Bank of Israel | boi.org.il | government_regulator | official | sanctions | proposed |
| ca-IL-environment_regulator | environment_regulator | Ministry of Environmental Protection | gov.il | government_regulator | official | refinery_outage | unverified |
| ca-IL-coast_guard_navy | coast_guard_navy | Israeli Navy | idf.il | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IL-upstream_regulator (NGA) | Leviathan/Tamar/Karish | **konflikt → shut-in Tamar** (precedent) | export pipeline do EG | proposed — supply do EG LNG re-exportu |

### Poznámky

- **`ca-IL-noc` = empty:** bez NOC; Chevron/NewMed/Energean operují.
- Gaza/regionální konflikt → **shut-in Tamar** precedent (dopad na egyptský LNG re-export).
- `gov.il` je zastřešující — ověřit konkrétní pod-cesty pro MoE/NGA.

### Progress po merge

`last_country: IL`, `last_batch_seq: 53`
