# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_039_country_authority_FR.md  
**Fáze:** country_authority — krok FR (France)  
**Datum:** 2026-07-06  

---

## Shrnutí

France = **TotalEnergies** (tier-1 global IOC; ~2.5 mboed upstream; LNG portfolio
~40 mtpa smluvní kapacita). Francie je méně závislá na ruském plynu než Německo
(~16% pre-2022 vs ~55% DE). **Fos-sur-Mer + Dunkerque LNG** = hlavní francouzské
terminály. CIM (Commité Interprofessionnel des Huiles) a GRTgaz (gas TSO).
Klíčové signály: **TotalEnergies quarterly** (tier-1 globální signal), **CRE (Commission
de Régulation de l'Énergie)** market data, **Fos/Dunkerque LNG arrivals**. 9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-FR-ministry_petroleum | FR | — | ministry_petroleum | MTECT – Ministry of Energy Transition | ecologie.gouv.fr | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-FR-noc | FR | — | noc | TotalEnergies SE | totalenergies.com | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-FR-mfa | FR | — | mfa | Ministère de l'Europe et des Affaires étrangères | diplomatie.gouv.fr | international_agency | official | sanctions, policy | proposed |
| ca-FR-customs_export | FR | — | customs_export | DGDDI – Direction Générale des Douanes et Droits Indirects | douane.gouv.fr | international_agency | official | imports, exports | proposed |
| ca-FR-upstream_regulator | FR | — | upstream_regulator | DGEC – Direction Générale de l'Energie et du Climat | ecologie.gouv.fr | international_agency | official | production, refinery_outage | proposed |
| ca-FR-port_maritime_authority | FR | — | port_maritime_authority | DGITM – Direction Générale des Infrastructures, des Transports et des Mobilités | ecologie.gouv.fr | international_agency | official | vessel_loading, port_closure | proposed |
| ca-FR-national_exchange | FR | — | national_exchange | Euronext Paris / ICE Endex (via EEX) | euronext.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-FR-central_bank | FR | — | central_bank | Banque de France | banque-france.fr | international_agency | official | pricing_formula | proposed |
| ca-FR-environment_regulator | FR | — | environment_regulator | DREAL (Directions Régionales de l'Environnement) | ecologie.gouv.fr | international_agency | official | refinery_outage | proposed |
| ca-FR-coast_guard_navy | FR | — | coast_guard_navy | Marine Nationale (French Navy) | defense.gouv.fr | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-FR-noc (TotalEnergies) | **TIER-1 globální**: TotalEnergies = 2.5 mboed upstream (Algeria, Angola, Nigeria, Libya, Kazakhstan, Norway, UK, UAE, Iraq, USA); LNG portfolio ~40 mtpa; každý TotalEnergies quarterly = global supply signal; každý TotalEnergies FM (Nigeria, Libya, Iraq) = immediate market event | TotalEnergies = French national champion; French government 10%+ stake (via APE); Mozambique LNG (force majeure 2021; restart timeline); Yemen block abandonment | Dunkerque LNG terminal (16.65 bcm/y); Fos-sur-Mer LNG terminal (8.25 bcm/y); Antifer crude port (VLCC anchor Le Havre) | **proposed** — totalenergies.com aktivní; tier-1 |
| ca-FR-ministry_petroleum (MTECT) | MTECT = post-ENGIE era energy governance; French gas diversification (LNG terminals Dunkerque/Fos); nuclear energy policy (restart 2022) | France = nuclear ~70% electricity → LNG demand for gas lower than DE; každý nuclear outage (EDF) = LNG demand surge signal | GRTgaz (gas TSO) + Teréga (south French) = gas network; MTECT oversight | **proposed** |
| ca-FR-coast_guard_navy | Marine Nationale = tier-1 French naval power; missions: Atlantic approach (VLCC), Mediterranean, Gulf of Guinea (anti-piracy Zone D) | France = permanent UNSC member; Paris prohlášení o West Africa stability = ENI/TotalEnergies security umbrella signal | Brest Naval Base; Toulon Mediterranean base; French aircraft carrier + NATO integration | **unverified** — defense.gouv.fr aktivní; Marine Nationale sub-domain ověřit |

### Expansion sloty
- GRTgaz → grtgaz.com (French gas TSO; TRS/PEG gas hub; post-2018 merger)
- Dunkerque LNG → dunkerquelng.com (EDF/TotalEnergies/Fluxys JV; tier-1 French LNG)
- CRE → cre.fr (energy market regulator; French gas/power prices)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 38, "last_country": "FR", "last_batch_seq": 39 }
```
