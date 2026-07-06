# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_014_country_authority_BR.md  
**Fáze:** country_authority — krok BR (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Brazílie (`BR`), 10 slotů (`ca-BR-{authority}`). Rostoucí **pre-salt** producent (non-OPEC, ale
OPEC+ pozorovatel od 2024). **ANP** klíčová produkční/aukční data; **IBAMA** licencování
(Equatorial Margin / Foz do Amazonas) = supply signál. 10 `proposed`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-BR-ministry_petroleum | ministry_petroleum | Ministry of Mines & Energy (MME) | gov.br/mme | government_regulator | official | production, export_license | proposed |
| ca-BR-noc | noc | Petrobras | petrobras.com.br | noc | official | production, exports, term_contract | proposed |
| ca-BR-mfa | mfa | Itamaraty (Foreign Affairs) | gov.br/mre | diplomacy | official | sanctions | proposed |
| ca-BR-customs_export | customs_export | Receita Federal | gov.br/receitafederal | government_regulator | official | exports | proposed |
| ca-BR-upstream_regulator | upstream_regulator | ANP | gov.br/anp | government_regulator | official | production, export_license | proposed |
| ca-BR-port_maritime_authority | port_maritime_authority | ANTAQ | gov.br/antaq | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-BR-national_exchange | national_exchange | B3 (Brasil Bolsa Balcão) | b3.com.br | exchange | official | pricing_formula | proposed |
| ca-BR-central_bank | central_bank | Banco Central do Brasil | bcb.gov.br | government_regulator | official | — | proposed |
| ca-BR-environment_regulator | environment_regulator | IBAMA | gov.br/ibama | government_regulator | official | refinery_outage | proposed |
| ca-BR-coast_guard_navy | coast_guard_navy | Marinha do Brasil | marinha.mil.br | diplomacy | official | port_closure | proposed |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-BR-upstream_regulator (ANP) | produkce, aukce bloků | — | field data | proposed — klíčová data |
| ca-BR-environment_regulator (IBAMA) | licencování Equatorial Margin | těžební expanze vs. env | — | proposed — supply signál (Foz do Amazonas) |

### Unverified / poznámky

- Petrobras listed (NYSE/B3) — transparentní, ale politicky řízené (pricing policy, palivové dotace).
- B3 finanční; ropa se necenuje lokálně (Brent-linked).
- Pre-salt (Búzios, Tupi) = růstový driver; export do Číny/Evropy.

### Progress po merge

`last_country: BR`, `last_batch_seq: 14`
