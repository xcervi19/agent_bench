# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_047_country_authority_LB.md  
**Fáze:** country_authority — krok LB (Lebanon)  
**Datum:** 2026-07-06  

---

## Shrnutí

Lebanon = **žádná současná produkce** ale klíčový pro **Eastern Mediterranean gas geopolitiku**:
Block 9 (TotalEnergies + ENI + QatarEnergy JV; první explorační vrt 2023; Aphrodite-field
proximity) + Block 4. Tripoli port = historický ropovod terminus (Trans-Arabian Pipeline,
neaktivní). Ekonomická krize + politická paralýza = omezená státní kapacita. Klíčové pro
sledování: **offshore licensing progres** a **Hezbollah/IDF conflict impact** na Eastern
Med shipping insurance. 6 proposed, 2 empty, 2 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-LB-ministry_petroleum | LB | — | ministry_petroleum | Ministry of Energy and Water | energyandwater.gov.lb | international_agency | official | policy, export_license | proposed |
| ca-LB-noc | LB | — | noc | — (no operational Lebanese NOC) | — | — | — | — | empty |
| ca-LB-mfa | LB | — | mfa | Ministry of Foreign Affairs | mfa.gov.lb | international_agency | official | sanctions, policy | proposed |
| ca-LB-customs_export | LB | — | customs_export | Lebanese Customs | customs.gov.lb | international_agency | official | imports | proposed |
| ca-LB-upstream_regulator | LB | — | upstream_regulator | LNHC – Lebanese Petroleum Administration | lpa.gov.lb | international_agency | official | production, force_majeure | unverified |
| ca-LB-port_maritime_authority | LB | — | port_maritime_authority | Port of Beirut Authority | portofbeirut.com | international_agency | official | vessel_loading, port_closure | proposed |
| ca-LB-national_exchange | LB | — | national_exchange | BSE – Beirut Stock Exchange | bse.com.lb | exchange | official | pricing_formula | proposed |
| ca-LB-central_bank | LB | — | central_bank | Banque du Liban | bdl.gov.lb | international_agency | official | sanctions | proposed |
| ca-LB-environment_regulator | LB | — | environment_regulator | Ministry of Environment | moe.gov.lb | international_agency | official | pipeline_outage | proposed |
| ca-LB-coast_guard_navy | LB | — | coast_guard_navy | Lebanese Armed Forces (Navy) | lebarmy.gov.lb | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-LB-upstream_regulator (LPA / LNHC) | LPA (Lebanese Petroleum Administration) = upstream regulator; Block 9 JV (TotalEnergies 35% + ENI 35% + QatarEnergy 30%); první vrt 2023 (Qana structure → results 2024); Block 4 = future potential | Lebanon-Israel maritime boundary deal (US brokered, October 2022) = prerequisite pro Block 9 drilling; Hezbollah conflict destabilizes offshore exploration; každý LPA drilling update = Eastern Med supply signal | Offshore deep water blocks; Tripoli historical pipeline terminus (TAP = Trans-Arabian Pipeline, idle since 1975) | **unverified** — lpa.gov.lb ověřit; LPA může mít nefunkční web |
| ca-LB-mfa | MFA Lebanon = proxy pro Hezbollah-IDF conflict level; každé MFA Lebanon statement post-ceasefire = restoration of Eastern Med shipping normal sentiment | Lebanon = pivotální pro Israel-Hamas-Hezbollah conflict trajectory; každá eskalace = Eastern Mediterranean insurance premium spike + Suez routing impact | Beirut port (2020 explosion aftermath; partial restoration); Tripoli port = secondary | **proposed** |
| ca-LB-port_maritime_authority (Beirut) | Port of Beirut = Lebanon's primary import hub (crude products, wheat); 2020 explosion severely damaged; partial reconstruction | Beirut port reconstruction = Lebanese political economy signal; Hezbollah presence in port area (pre-2020 documented) | LNG import terminal discussions (Golar/New Fortress Energy floating terminal proposal, stalled); fuel oil imports for EdL (electricity utility) | **proposed** |

### Analytická poznámka: Lebanon omezená hodnota jako primary source
- Lebanon = **observational asset** spíše než primary data source
- Hlavní hodnota = geopolitický proxy pro Eastern Med conflict escalation
- Expansion: IDF/Israel MFA statements (Israel.gov.il) = counterpart signals
- UNIFIL (UN Interim Force in Lebanon) → unifil.unmissions.org = conflict monitoring

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 46, "last_country": "LB", "last_batch_seq": 47 }
```
