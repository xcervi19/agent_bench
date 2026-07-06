# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_013_country_authority_BR.md  
**Fáze:** country_authority — krok BR (Brazil)  
**Datum:** 2026-07-05  

---

## Shrnutí

Brazil = ~3.8 mb/d (2024), rychle rostoucí deep-water producer (pre-salt Santos Basin).
Klíčové signály: **Petrobras quarterly** (tier-1 LatAm E&P disclosure), **ANP production data**
(weekly/monthly field-level), **IBAMA** (environmental licensing pro offshore drilling = kritický
bottleneck pro Equatorial Margin expansion), **Lula energy policy** (Petrobras dividend vs
reinvestment tension). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-BR-ministry_petroleum | BR | — | ministry_petroleum | MME – Ministry of Mines and Energy | mme.gov.br | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-BR-noc | BR | — | noc | Petrobras | petrobras.com.br | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-BR-mfa | BR | — | mfa | Itamaraty – Ministry of Foreign Affairs | gov.br/mre | international_agency | official | sanctions, policy | proposed |
| ca-BR-customs_export | BR | — | customs_export | RFB – Receita Federal do Brasil (Customs) | rfb.gov.br | international_agency | official | exports, export_license | proposed |
| ca-BR-upstream_regulator | BR | — | upstream_regulator | ANP – National Petroleum, Natural Gas and Biofuels Agency | anp.gov.br | international_agency | official | production, refinery_outage | proposed |
| ca-BR-port_maritime_authority | BR | — | port_maritime_authority | ANTAQ – National Waterway Transportation Agency | antaq.gov.br | international_agency | official | vessel_loading, port_closure | proposed |
| ca-BR-national_exchange | BR | — | national_exchange | B3 – Brasil Bolsa Balcão | b3.com.br | exchange | official | pricing_formula, term_contract | proposed |
| ca-BR-central_bank | BR | — | central_bank | BCB – Banco Central do Brasil | bcb.gov.br | international_agency | official | pricing_formula, sanctions | proposed |
| ca-BR-environment_regulator | BR | — | environment_regulator | IBAMA – Brazilian Institute of Environment and Renewable Resources | ibama.gov.br | international_agency | official | refinery_outage, force_majeure | proposed |
| ca-BR-coast_guard_navy | BR | — | coast_guard_navy | Marinha do Brasil – Brazilian Navy | marinha.mil.br | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-BR-noc (Petrobras) | Petrobras = 3.4 mb/d (2024); pre-salt Santos Basin (Tupi, Búzios) = 70 % produkce; quarterly earnings + business plan 5Y jsou tier-1 signal pro LatAm crude output | Petrobras je 36 % státní (Lula government); politické napětí management/dividendy → stock price signal | FPSO loading v Santos Basin a Campos Basin; export přes terminál Angra dos Reis a São Sebastião | **proposed** — petrobras.com.br aktivní; anglická IR sekce dostupná |
| ca-BR-upstream_regulator (ANP) | ANP publikuje měsíční produkční bulletin (field-level data); licenční kola → long-term supply | ANP je pod MME; reguluje Equatorial Margin licensing (environmentální spor s IBAMA) | ANP spravuje povinnosti ohledně reportingu pro offshore operators | **proposed** — anp.gov.br aktivní |
| ca-BR-environment_regulator (IBAMA) | IBAMA blokující Petrobras Equatorial Margin licenci (2022–2024) = přímý long-term supply constraint; každé IBAMA rozhodnutí o offshore license je price-moving pro Brazilian crude futures | IBAMA je pod Ministry of Environment; politické napětí Lula/Petrobras vs IBAMA ekologové | Environmental licensing bottleneck pro nové FPSOs | **proposed** — ibama.gov.br aktivní |

### Expansion sloty
- ANP produkční bulletin feed → anp.gov.br/producao-de-petroleo (sub-feed)
- Petrobras IR release calendar → petrobras.com.br/en/investors
- TBG (Trans Brasil Gasoduto) → tbg.com.br (gas pipeline)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 12, "last_country": "BR", "last_batch_seq": 13 }
```
