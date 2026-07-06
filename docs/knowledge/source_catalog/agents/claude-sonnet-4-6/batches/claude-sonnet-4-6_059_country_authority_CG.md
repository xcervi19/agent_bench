# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_059_country_authority_CG.md  
**Fáze:** country_authority — krok CG (Republic of Congo / Congo-Brazzaville)  
**Datum:** 2026-07-06  

---

## Shrnutí

Republic of Congo (Congo-Brazzaville) = **~250 kb/d crude** (SNPC + TotalEnergies JV;
Moho-Bilondo deepwater). **SNPC** = státní NOC. TotalEnergies = dominantní IOC operator.
Djeno terminal = jediný crude export terminal (Pointe-Noire). Congo = OPEC member.
Klíčové signály: **TotalEnergies Congo quarterly** (Moho-Bilondo, Lianzi),
**SNPC OSP**, **Djeno terminal cargo**. 8 proposed, 1 empty, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CG-ministry_petroleum | CG | — | ministry_petroleum | Ministry of Hydrocarbons | mhsp.cg | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-CG-noc | CG | — | noc | SNPC – Société Nationale des Pétroles du Congo | snpc-congo.cg | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-CG-mfa | CG | — | mfa | Ministry of Foreign Affairs | mae.gouv.cg | international_agency | official | sanctions, policy | proposed |
| ca-CG-customs_export | CG | — | customs_export | Direction Générale des Douanes | douanes.gouv.cg | international_agency | official | exports, export_license | proposed |
| ca-CG-upstream_regulator | CG | — | upstream_regulator | Ministry of Hydrocarbons (dual) | mhsp.cg | international_agency | official | production, force_majeure | proposed |
| ca-CG-port_maritime_authority | CG | — | port_maritime_authority | Port Autonome de Pointe-Noire | papn.cg | international_agency | official | vessel_loading, port_closure | proposed |
| ca-CG-national_exchange | CG | — | national_exchange | — (no stock exchange) | — | — | — | — | empty |
| ca-CG-central_bank | CG | — | central_bank | BEAC – Banque des États de l'Afrique Centrale | beac.int | international_agency | official | pricing_formula | proposed |
| ca-CG-environment_regulator | CG | — | environment_regulator | Ministry of Environment | mde.gouv.cg | international_agency | official | refinery_outage | proposed |
| ca-CG-coast_guard_navy | CG | — | coast_guard_navy | Congolese Navy (Marine Nationale) | — | — | — | — | unverified |

---

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-CG-noc (SNPC) | SNPC = state NOC; Moho-Bilondo deepwater (TotalEnergies 53.5% op.; ~90 kb/d); Lianzi (Chevron+SNPC); SNPC OSP = CG crude benchmark; Djeno terminal cargo = primary signal | Sassou Nguesso government = authoritarian; OPEC member; TotalEnergies dominant (ENI also present); Chinese IOCs entering | Djeno terminal (Pointe-Noire coast); VLCC crude loading; Congo River no crude pipeline | **proposed** |
| ca-CG-port_maritime_authority | Pointe-Noire = Congo's main port; Djeno crude terminal (SNPC); TotalEnergies logistique base | Pointe-Noire = Atlantic Gulf of Guinea corridor; ENI Litchendjili gas development (2024+) | ENI + TotalEnergies Congo deepwater platforms; Djeno FPSO/tanker loading | **proposed** |

### Expansion
- TotalEnergies Congo → totalenergies.com/congo (Moho-Bilondo operator; primary signal)
- ENI Congo → eni.com/congo (Litchendjili gas, Nene Marine)

---
```json
{ "phase": "country_authority", "phase_index": 45, "last_country": "CG", "last_batch_seq": 59 }
```
