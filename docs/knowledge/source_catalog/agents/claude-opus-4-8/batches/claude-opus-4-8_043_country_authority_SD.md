# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_043_country_authority_SD.md  
**Fáze:** country_authority — krok SD (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Súdán (`SD`), 10 slotů (`ca-SD-{authority}`). **Občanská válka (SAF vs RSF)** → úřady nefunkční.
Trading význam = **tranzit jihosúdánské ropy** přes pipeline do **Port Sudan**; válka = chronické
force majeure na exportu SS. 1 `proposed`, 3 `unverified`, 6 `empty` — vědomě sparse.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-SD-ministry_petroleum | ministry_petroleum | Ministry of Energy & Petroleum | — | government_regulator | official | production, export_license | empty |
| ca-SD-noc | noc | Sudapet | — | noc | official | production, exports | unverified |
| ca-SD-mfa | mfa | Ministry of Foreign Affairs | — | diplomacy | official | sanctions | empty |
| ca-SD-customs_export | customs_export | Sudan Customs | — | government_regulator | official | exports | empty |
| ca-SD-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-SD-port_maritime_authority | port_maritime_authority | Port Sudan (SS crude terminal) | seaports.gov.sd | infrastructure | official | vessel_loading, port_closure, pipeline_outage | unverified |
| ca-SD-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-SD-central_bank | central_bank | Central Bank of Sudan | cbos.gov.sd | government_regulator | official | sanctions | unverified |
| ca-SD-environment_regulator | environment_regulator | — | — | — | — | — | empty |
| ca-SD-coast_guard_navy | coast_guard_navy | — | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SD-port_maritime_authority (Port Sudan) | — | válka SAF/RSF | **SS crude export terminál** — pipeline outage | unverified — klíč pro SS export |

### Unverified / poznámky

- **Válka** → úřady roztříštěné/nefunkční; většina `empty`.
- Súdán je hlavně **tranzitní země** pro South Sudan crude (Dar/Nile Blend → Port Sudan); přerušení = force majeure signál pro SS objemy.
- Reálný signál: SS operátoři + AIS na Port Sudan, ne súdánské úřady.

### Progress po merge

`last_country: SD`, `last_batch_seq: 43`
