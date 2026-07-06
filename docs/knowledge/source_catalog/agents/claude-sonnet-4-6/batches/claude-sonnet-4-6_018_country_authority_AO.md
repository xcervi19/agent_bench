# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_018_country_authority_AO.md  
**Fáze:** country_authority — krok AO (Angola)  
**Datum:** 2026-07-05  

---

## Shrnutí

Angola = ~1.1 mb/d; největší producent subsaharské Afriky po Nigérii. Klíčové signály:
**Sonangol OSP** (Angola grades — Cabinda, Girassol, Dalia — klíčové pro čínský import),
**ANPG** (upstream regulator; bloková kola), **Sonangol quarterly** (produkční data).
Angola vystoupila z OPEC v 2023 (kvóty spor). Nové pre-salt bloky v Angolské pánvi
a Namibe Basin. 7 proposed, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-AO-ministry_petroleum | AO | — | ministry_petroleum | MIREMPET – Ministry of Mineral Resources, Petroleum and Gas | mirempet.gov.ao | international_agency | official | policy, export_license, quota_rhetoric | unverified |
| ca-AO-noc | AO | — | noc | Sonangol – Sociedade Nacional de Combustíveis de Angola | sonangol.co.ao | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-AO-mfa | AO | — | mfa | Ministério das Relações Exteriores | mirex.gov.ao | international_agency | official | sanctions, policy | proposed |
| ca-AO-customs_export | AO | — | customs_export | AGT – Autoridade Geral Tributária (Customs) | agt.gov.ao | international_agency | official | exports, export_license | proposed |
| ca-AO-upstream_regulator | AO | — | upstream_regulator | ANPG – Agência Nacional de Petróleo, Gás e Biocombustíveis | anpg.gov.ao | international_agency | official | production, refinery_outage | proposed |
| ca-AO-port_maritime_authority | AO | — | port_maritime_authority | IMPA – Instituto Marítimo e Portuário de Angola | impa.gov.ao | international_agency | official | vessel_loading, port_closure | unverified |
| ca-AO-national_exchange | AO | — | national_exchange | BODIVA – Bolsa de Dívida e Valores de Angola | bodiva.ao | exchange | official | pricing_formula | unverified |
| ca-AO-central_bank | AO | — | central_bank | BNA – Banco Nacional de Angola | bna.ao | international_agency | official | sanctions | proposed |
| ca-AO-environment_regulator | AO | — | environment_regulator | MINAMB – Ministério do Ambiente | minamb.gov.ao | international_agency | official | refinery_outage | proposed |
| ca-AO-coast_guard_navy | AO | — | coast_guard_navy | Marinha de Guerra de Angola | marinha.mil.ao | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (výběr klíčových + unverified)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-AO-noc (Sonangol) | Sonangol = monopol; operuje přes JVs s TotalEnergies, BP, Eni, Chevron; OSP pro Cabinda Grade = key West African sweet benchmark; produkce klesá z 2 mb/d (2008) na ~1.1 mb/d | Angola vystoupila z OPEC 12/2023 (produkční kvóta spor); každá Sonangol produkční guidance = OPEC impact | Lobito terminal (severní Angola), Palanca, Hungo terminály; VLCC loadingy přes Atlantic corridor do Číny (45-50% Angolan exports) | **proposed** — sonangol.co.ao aktivní |
| ca-AO-upstream_regulator (ANPG) | ANPG (oddělena od Sonangol 2018) vydává upstream licence; bloková kola pro Namibe a Benguela basin | ANPG jako independent regulator = strukturální zlepšení post-Lourenço reformy | ANPG koordinuje JV allokace pro blok loading | **proposed** — anpg.gov.ao aktivní |
| ca-AO-ministry_petroleum (MIREMPET) | Ministerstvo určuje export policy; post-OPEC departure = plná autonomie produkční politiky | MIREMPET politika Lourenço vlády = reforma státního sektoru (pozitivní IOC signal) | Koordinace s ANPG a Sonangol | **unverified** — mirempet.gov.ao: ověřit přesné zkratku ministerstva (mohlo být přejmenováno); alternativně minpet.gov.ao |
| ca-AO-port_maritime_authority (IMPA) | IMPA spravuje přístupy k Lobito, Luanda a Cabinda terminálům | Námořní jurisdikce pro Angolské pobřeží; offshore bezpečnost | Port clearance pro VLCC tankers v Cabinda | **unverified** — impa.gov.ao: ověřit zda IMPA má vlastní doménu nebo je pod jiným ministerstvem |

### Expansion sloty
- Sonangol sub-entities: Sonangol Pesquisa e Produção → sonangol.co.ao/pp
- Angola LNG (ALNG) → angolalng.com (LNG terminal Soyo; Chevron-led JV)
- Lobito Corridor railway (geopolitický signal: čínská BRI) → expansion

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 17, "last_country": "AO", "last_batch_seq": 18 }
```
