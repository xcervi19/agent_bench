# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_045_country_authority_CO.md  
**Fáze:** country_authority — krok CO (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Kolumbie (`CO`), 10 slotů (`ca-CO-{authority}`). **Ecopetrol** dominantní. Petro vláda **zastavila nové
průzkumné licence** (žádné nové kontrakty/fracking) → dlouhodobý bearish supply signál, klesající rezervy.
Coveñas export terminál. 8 `proposed`, 1 `unverified`, 1 pozn.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-CO-ministry_petroleum | ministry_petroleum | Ministry of Mines & Energy | minenergia.gov.co | government_regulator | official | production, export_license | proposed |
| ca-CO-noc | noc | Ecopetrol | ecopetrol.com.co | noc | official | production, exports, term_contract | proposed |
| ca-CO-mfa | mfa | Ministry of Foreign Affairs | cancilleria.gov.co | diplomacy | official | sanctions | proposed |
| ca-CO-customs_export | customs_export | DIAN | dian.gov.co | government_regulator | official | exports | proposed |
| ca-CO-upstream_regulator | upstream_regulator | ANH (Agencia Nac. de Hidrocarburos) | anh.gov.co | government_regulator | official | production, export_license | proposed |
| ca-CO-port_maritime_authority | port_maritime_authority | Coveñas / Cartagena (DIMAR) | dimar.mil.co | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-CO-national_exchange | national_exchange | Bolsa de Valores de Colombia (bvc) | bvc.com.co | exchange | official | pricing_formula | unverified |
| ca-CO-central_bank | central_bank | Banco de la República | banrep.gov.co | government_regulator | official | sanctions | proposed |
| ca-CO-environment_regulator | environment_regulator | ANLA | anla.gov.co | government_regulator | official | refinery_outage | proposed |
| ca-CO-coast_guard_navy | coast_guard_navy | Colombian Navy / DIMAR | armada.mil.co | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CO-upstream_regulator (ANH) | rezervy, licenční kola | **Petro: stop novým licencím** | — | proposed — bearish supply signál |
| ca-CO-noc (Ecopetrol) | Castilla/Vasconia produkce | pipeline útoky (ELN) | Coveñas export | proposed |

### Unverified / poznámky

- **Unverified:** bvc (`bvc.com.co`) — finanční, Tier 2.
- Petro vláda: žádné nové E&P kontrakty → strukturální pokles produkce (multi-letý signál).
- Pipeline sabotáž (Caño Limón-Coveñas, ELN) = občasný force majeure.

### Progress po merge

`last_country: CO`, `last_batch_seq: 45`
