# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_015_country_authority_MX.md  
**Fáze:** country_authority — krok MX (Mexico)  
**Datum:** 2026-07-05  

---

## Shrnutí

Mexico = ~1.9 mb/d (klesající od peak 3.4 mb/d v 2004); Pemex je chronicky poddlužena
a pod-investující. Klíčové signály: **Pemex produkční data** (měsíční, veřejné), **CNH
upstream data** (regulátor; detailní field-level), **Pemex Dos Bocas rafinérie** (Lopézův
megaproject; cost overruns = policy signal), **Cayo Arcas/Dos Bocas** terminály. ASEA jako
specifický mexický QHSE regulátor pro energetický sektor. 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-MX-ministry_petroleum | MX | — | ministry_petroleum | SENER – Secretaría de Energía | gob.mx/sener | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-MX-noc | MX | — | noc | Pemex – Petróleos Mexicanos | pemex.com | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-MX-mfa | MX | — | mfa | SRE – Secretaría de Relaciones Exteriores | gob.mx/sre | international_agency | official | sanctions, policy | proposed |
| ca-MX-customs_export | MX | — | customs_export | SAT – Servicio de Administración Tributaria | sat.gob.mx | international_agency | official | exports, export_license | proposed |
| ca-MX-upstream_regulator | MX | — | upstream_regulator | CNH – Comisión Nacional de Hidrocarburos | gob.mx/cnh | international_agency | official | production, refinery_outage | proposed |
| ca-MX-port_maritime_authority | MX | — | port_maritime_authority | CGPMM – Coordinación General de Puertos y Marina Mercante | gob.mx/cgpmm | international_agency | official | vessel_loading, port_closure | unverified |
| ca-MX-national_exchange | MX | — | national_exchange | BMV – Bolsa Mexicana de Valores | bmv.com.mx | exchange | official | pricing_formula | proposed |
| ca-MX-central_bank | MX | — | central_bank | Banxico – Banco de México | banxico.org.mx | international_agency | official | pricing_formula, sanctions | proposed |
| ca-MX-environment_regulator | MX | — | environment_regulator | ASEA – Agencia de Seguridad, Energía y Ambiente | gob.mx/asea | international_agency | official | refinery_outage, force_majeure | proposed |
| ca-MX-coast_guard_navy | MX | — | coast_guard_navy | Semar – Secretaría de Marina | semar.gob.mx | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-MX-noc (Pemex) | Pemex produkuje ~1.9 mb/d (Cantarell declining, Ku-Maloob-Zaap dominant); quarterly financials; heavy crude Maya = primární mexický export blend | Pemex má $100bn+ debt; každé vládní bail-out nebo bond issue = fiscal sustainability signal; Sheinbaum vs Claudia Lopez energy policy signal | Cayo Arcas Marine Terminal (Gulf of Mexico crude export hub); Coatzacoalcos a Salina Cruz rafinérie supply | **proposed** — pemex.com aktivní |
| ca-MX-upstream_regulator (CNH) | CNH publikuje měsíční produkční data field-by-field; více detailní než Pemex IR | CNH jako nezávislý regulátor byl oslaben re-centralizací pod AMLO/Sheinbaum; tendry omezeny | CNH licence pro Pemex + soukromé IOC blocks (TotalEnergies, Shell ve Deepwater) | **proposed** — gob.mx/cnh aktivní |
| ca-MX-port_maritime_authority (CGPMM) | CGPMM pod SCT koordinuje přístavy Cayo Arcas, Dos Bocas, Salina Cruz | Federální port authority; ověřit přesnou URL pod gob.mx (SCT restrukturalizace) | Dos Bocas LPG/crude terminal; Cayo Arcas = hlavní crude export | **unverified** — gob.mx/cgpmm jako URL ověřit; může být gob.mx/sct nebo jiný suffix post-restrukturalizace 2021 |

### Expansion sloty
- PMI Norteamérica (Pemex trading arm) → pmi.com.mx
- CENAGAS (gas pipeline operator) → gob.mx/cenagas
- Cayo Arcas Terminal (Marine) → Pemex operated geo slot

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 14, "last_country": "MX", "last_batch_seq": 15 }
```
