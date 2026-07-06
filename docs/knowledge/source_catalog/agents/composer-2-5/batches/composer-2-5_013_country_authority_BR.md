# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_013_country_authority_BR.md  
**Fáze:** country_authority — krok BR (Fáze 2, země 11/64)  
**Datum:** 2026-07-05  

---

## Shrnutí

Brazil × 10 autorit. **9 proposed**, **1 unverified** (national_exchange — B3, limited crude futures).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-BR-ministry_petroleum | BR | — | ministry_petroleum | Ministry of Mines and Energy (MME) | gov.br/mme | government_regulator | official | production,exports,quota_rhetoric | proposed |
| ca-BR-noc | BR | — | noc | Petrobras | petrobras.com.br | noc | official | production,exports,force_majeure,term_contract | proposed |
| ca-BR-mfa | BR | — | mfa | Ministry of Foreign Affairs (MRE) | gov.br/mre | diplomacy | official | sanctions,export_license | proposed |
| ca-BR-customs_export | BR | — | customs_export | Receita Federal (Customs) | gov.br/receitafederal | government_regulator | official | exports,export_license,imports | proposed |
| ca-BR-upstream_regulator | BR | — | upstream_regulator | ANP (National Agency of Petroleum) | gov.br/anp | government_regulator | official | production,term_contract | proposed |
| ca-BR-port_maritime_authority | BR | — | port_maritime_authority | ANTAQ (National Waterway Transport Agency) | antaq.gov.br | infrastructure | official | vessel_loading,port_closure,exports | proposed |
| ca-BR-national_exchange | BR | — | national_exchange | B3 (Brasil Bolsa Balcão) | b3.com.br | exchange | official | pricing_formula | unverified |
| ca-BR-central_bank | BR | — | central_bank | Banco Central do Brasil | bcb.gov.br | government_regulator | official | sanctions,pricing_formula | proposed |
| ca-BR-environment_regulator | BR | — | environment_regulator | IBAMA | ibama.gov.br | government_regulator | official | refinery_outage,production | proposed |
| ca-BR-coast_guard_navy | BR | — | coast_guard_navy | Brazilian Navy | marinha.mil.br | government_regulator | official | port_closure,vessel_loading | proposed |

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-BR-noc | Pre-salt output, FPSO outages | Fuel subsidy / politics | Santos Basin loading, export terminals | **proposed** |
| ca-BR-upstream_regulator | ANP production / reserve data | Bid round policy | Pre-salt auction timelines | **proposed** |
| ca-BR-port_maritime_authority | — | — | Santos, Angra dos Reis, Rio terminals | **proposed** |

**Desk Tier 1:** petrobras.com.br + gov.br/anp + antaq.gov.br. ANP monthly production is primary data.

### Progress po merge (návrh)

`last_country: BR`, `last_batch_seq: 13`. **Další:** CA.
