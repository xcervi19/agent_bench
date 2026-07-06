# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_057_country_authority_SN.md  
**Fáze:** country_authority — krok SN (Senegal)  
**Datum:** 2026-07-06  

---

## Shrnutí

Senegal = **nový producent** (Sangomar offshore field, ~100 kb/d, Woodside operated,
first oil June 2024). **Grand Tortue Ahmeyim LNG** (GTG; Senegal+Mauritania border;
BP operated; ~2.5 mtpa FLNG; first cargo 2024). Klíčové signály: **Woodside/BP FLNG
loading schedules**, **Sangomar FPSO Léopold Sédar Senghor cargo tracking**.
Senegal = West Africa new producer; PETROSEN = státní NOC. 8 proposed, 1 empty, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SN-ministry_petroleum | SN | — | ministry_petroleum | Ministry of Petroleum and Energies | petrole.gouv.sn | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-SN-noc | SN | — | noc | Petrosen – Société des Pétroles du Sénégal | petrosen.sn | international_agency | official | production, exports, term_contract | proposed |
| ca-SN-mfa | SN | — | mfa | Ministry of Foreign Affairs | diplomatie.gouv.sn | international_agency | official | sanctions, policy | proposed |
| ca-SN-customs_export | SN | — | customs_export | Direction Générale des Douanes | douanes.gouv.sn | international_agency | official | exports, export_license | proposed |
| ca-SN-upstream_regulator | SN | — | upstream_regulator | PETROSEN (upstream licensing, dual) | petrosen.sn | international_agency | official | production, force_majeure | proposed |
| ca-SN-port_maritime_authority | SN | — | port_maritime_authority | Port Autonome de Dakar | portdakar.sn | international_agency | official | vessel_loading, port_closure | proposed |
| ca-SN-national_exchange | SN | — | national_exchange | BRVM – Bourse Régionale des Valeurs Mobilières (West Africa) | brvm.org | exchange | official | pricing_formula | proposed |
| ca-SN-central_bank | SN | — | central_bank | BCEAO – Banque Centrale des États de l'Afrique de l'Ouest | bceao.int | international_agency | official | pricing_formula | proposed |
| ca-SN-environment_regulator | SN | — | environment_regulator | DEEC – Direction de l'Environnement et des Établissements Classés | deec.sn | international_agency | official | force_majeure | proposed |
| ca-SN-coast_guard_navy | SN | — | coast_guard_navy | Marine Nationale du Sénégal | marine.sn | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SN-noc (Petrosen) | Petrosen = 18% in Sangomar + 10% in GTA (Grand Tortue Ahmeyim); Woodside = 82% Sangomar operated; BP = 56% GTA operated; každý Petrosen/Woodside/BP update = West Africa new supply signal | Senegal pro-Western; Faye government 2024 = reviewed some energy contracts (Adani, other); GTA = cross-border with Mauritania (joint OMRG governance) | Sangomar FPSO (offshore ~5 km from shore); GTA FLNG vessel (maritime border SN/MR); Dakar port = product import | **proposed** |
| ca-SN-port_maritime_authority (Dakar) | Port of Dakar = major West African hub; crude product import; Sangomar FPSO offloads via shuttle tankers to Dakar or export markets | Port Dakar = Senegal gateway; Atlantic facing; France historically dominant | GTA FLNG = 2.5 mtpa capacity; first cargo 2024; GTG JV supply to Europe as West Africa LNG diversification | **proposed** |

### Expansion
- Woodside Senegal → woodside.com/senegal (Sangomar operator; first oil 2024)
- BP Mauritania-Senegal → bp.com/gta (GTA FLNG operator)
- OMRG (Organisme de Mise en Valeur du fleuve Gambie) → parallel GNLC governance

---
```json
{ "phase": "country_authority", "phase_index": 43, "last_country": "SN", "last_batch_seq": 57 }
```
