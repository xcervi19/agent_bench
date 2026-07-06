# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_055_country_authority_CO.md  
**Fáze:** country_authority — krok CO (Colombia)  
**Datum:** 2026-07-06  

---

## Shrnutí

Colombia = **andský producent** (~730 kb/d crude; klesající z peak ~1 mb/d 2013).
**Ecopetrol** (státní NOC, NYSE + BVC listed). Klíčové signály: **Ecopetrol quarterly**,
**Cano Limón–Coveñas pipeline** (ELN/FARC attack history = supply disruption),
**Cartagena VLCC terminal** (Reficar refinery, ~165 kb/d). Petro-vláda (2022+) =
anti-oil policy rétorické riziko (nové licence zastaveny). Colombia = also Pacific Coast
crude exportér (Buenaventura). 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CO-ministry_petroleum | CO | — | ministry_petroleum | MinMinas – Ministry of Mines and Energy | minenergia.gov.co | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-CO-noc | CO | — | noc | Ecopetrol S.A. | ecopetrol.com.co | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-CO-mfa | CO | — | mfa | Ministry of Foreign Affairs | cancilleria.gov.co | international_agency | official | sanctions, policy | proposed |
| ca-CO-customs_export | CO | — | customs_export | DIAN – Tax and Customs Authority | dian.gov.co | international_agency | official | exports, export_license | proposed |
| ca-CO-upstream_regulator | CO | — | upstream_regulator | ANH – National Hydrocarbons Agency | anh.gov.co | international_agency | official | production, force_majeure | proposed |
| ca-CO-port_maritime_authority | CO | — | port_maritime_authority | Superintendencia de Puertos y Transporte | supertransporte.gov.co | international_agency | official | vessel_loading, port_closure | proposed |
| ca-CO-national_exchange | CO | — | national_exchange | BVC – Bolsa de Valores de Colombia | bvc.com.co | exchange | official | pricing_formula | proposed |
| ca-CO-central_bank | CO | — | central_bank | Banco de la República | banrep.gov.co | international_agency | official | pricing_formula | proposed |
| ca-CO-environment_regulator | CO | — | environment_regulator | ANLA – National Environmental Licensing Authority | anla.gov.co | international_agency | official | refinery_outage | proposed |
| ca-CO-coast_guard_navy | CO | — | coast_guard_navy | Armada Nacional de Colombia | armada.mil.co | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CO-noc (Ecopetrol) | Ecopetrol = state ~89%; NYSE (EC) + BVC listed; ~730 kb/d crude; Castilla, Chichimene, Rubiales fields; Reficar Cartagena refinery (165 kb/d); quarterly = tier-1 Colombia signal | President Petro (2022) stopped new upstream licences → Ecopetrol forced to manage existing assets only; each new licence moratorium signal = production decline outlook | Cano Limón–Coveñas pipeline (800 km; ELN/FARC historical attacks ~1,000+ times); Caño Limón field (Occidental Petroleum JV) | **proposed** — ecopetrol.com.co aktivní |
| ca-CO-upstream_regulator (ANH) | ANH = block licensing; každá ANH moratorium extension = supply decline signal; Colombia reserves ~2B barrels (6-year life at current production) | ANH pod MinMinas; Petro-era = no new exploratory blocks (2022+) = structural production decline | ANH production statistics = monthly Colombia field data | **proposed** |
| ca-CO-ministry_petroleum (MinMinas) | MinMinas = policy; Petro "energy transition" rétorické riziko; každý MinMinas anti-fossil fuel statement = COP-sensitive signal for IOC investment | Petro = leftist; Colombia Venezuela relations (normalised 2022) = potential Venezuelan crude re-export signal | Cartagena + Coveñas (Caribbean coast) + Buenaventura (Pacific) crude terminals | **proposed** |

### Expansion
- Cano Limón–Coveñas pipeline → oleoductos.com.co (OCY/Ecopetrol; key supply route)
- OCENSA pipeline (Oleoducto Central) → ocensa.com.co

---
```json
{ "phase": "country_authority", "phase_index": 41, "last_country": "CO", "last_batch_seq": 55 }
```
