# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_062_country_authority_MR.md  
**Fáze:** country_authority — krok MR (Mauritania)  
**Datum:** 2026-07-06  

---

## Shrnutí

Mauritania = **nový producent + LNG** prostřednictvím **Grand Tortue Ahmeyim (GTA)**
(sdílená s Senegalem; BP operated; ~2.5 mtpa FLNG; první náklad 2024). Chinguetti crude
field (TotalEnergies, offline 2020; stará infrastruktura). **SMHPM** = státní NOC.
Banda gas field (Kosmos Energy) = potential. Klíčové signály: **BP GTA FLNG loadings**,
**Kosmos Energy Mauritania reports**. 8 proposed, 1 empty, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-MR-ministry_petroleum | MR | — | ministry_petroleum | Ministry of Petroleum, Mines and Energy | petrole.gov.mr | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-MR-noc | MR | — | noc | SMHPM – Société Mauritanienne des Hydrocarbures et de Patrimoine Minier | smhpm.mr | international_agency | official | production, exports, term_contract | proposed |
| ca-MR-mfa | MR | — | mfa | Ministry of Foreign Affairs | mae.gov.mr | international_agency | official | sanctions, policy | proposed |
| ca-MR-customs_export | MR | — | customs_export | Direction Générale des Douanes | douanes.gov.mr | international_agency | official | exports, export_license | proposed |
| ca-MR-upstream_regulator | MR | — | upstream_regulator | SMHPM (upstream licensing, dual) | smhpm.mr | international_agency | official | production, force_majeure | proposed |
| ca-MR-port_maritime_authority | MR | — | port_maritime_authority | Port Autonome de Nouakchott | pan.mr | international_agency | official | vessel_loading, port_closure | proposed |
| ca-MR-national_exchange | MR | — | national_exchange | — (no stock exchange) | — | — | — | — | empty |
| ca-MR-central_bank | MR | — | central_bank | BCM – Banque Centrale de Mauritanie | bcm.mr | international_agency | official | pricing_formula | proposed |
| ca-MR-environment_regulator | MR | — | environment_regulator | Ministry of Environment | medd.gov.mr | international_agency | official | force_majeure | proposed |
| ca-MR-coast_guard_navy | MR | — | coast_guard_navy | Mauritanian Navy | — | — | — | — | unverified |

---

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-MR-noc (SMHPM) | SMHPM = 10% in GTA; BP = 56% + Kosmos = 27% + Petrosen (SN) = 7%; GTA FLNG = 2.5 mtpa capacity; Banda gas field (future); Chinguetti = mostly depleted (~20 kb/d legacy) | Mauritania-Senegal OMRG (cross-border GTA governance); Ghazouani government pro-Western; IMF programme | GTA FLNG = 2 FLNG trains on maritime border MR/SN; Nouakchott port = shallow water; GTA shuttle tankers offshore | **proposed** |
| ca-MR-ministry_petroleum | MR Ministry = GTA governance + Banda development approvals; Kosmos Energy block licensing | Mauritania non-aligned; French + Chinese influence; Sahel security (JNIM jihadist threats inland but offshore stable) | Nouakchott port limited crude capacity; GTA FLNG offshore | **proposed** |

### Expansion
- BP GTA FLNG → bp.com/gta (primary operator; cross-border MR+SN)
- Kosmos Energy Mauritania → kosmosenergy.com (Banda gas, Bir Allah blocks)

---
```json
{ "phase": "country_authority", "phase_index": 48, "last_country": "MR", "last_batch_seq": 62 }
```
