# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_046_country_authority_GE.md  
**Fáze:** country_authority — krok GE (Georgia)  
**Datum:** 2026-07-06  

---

## Shrnutí

Georgia = **tranzitní stát pro BTC pipeline** (Baku–Tbilisi–Ceyhan; prochází přes Georgii)
a **SCP/TANAP gas pipeline** (South Caucasus Pipeline). Minimální vlastní produkce.
Klíčové signály: **BTC Georgian section integrity**, **TICG (Trans-Caucasus
pipeline Georgian section)**, **Supsa crude terminal** (Batumi; alternativní Black Sea
export bod pro Azeri crude pre-BTC). Geo = klíčový chokepoint mezi Caspian a Mediterranean;
každé destabilizační geo-politické události v Gruzii (Ruská 2008 invaze = BTC přerušení
precedent) = primární signal. 8 proposed, 2 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GE-ministry_petroleum | GE | — | ministry_petroleum | Ministry of Economy and Sustainable Development | economy.ge | international_agency | official | policy, export_license | proposed |
| ca-GE-noc | GE | — | noc | GOGC – Georgian Oil and Gas Corporation | gogc.ge | international_agency | official | production, term_contract | proposed |
| ca-GE-mfa | GE | — | mfa | Ministry of Foreign Affairs | mfa.gov.ge | international_agency | official | sanctions, policy | proposed |
| ca-GE-customs_export | GE | — | customs_export | Revenue Service (Customs) | rs.ge | international_agency | official | exports, export_license | proposed |
| ca-GE-upstream_regulator | GE | — | upstream_regulator | Georgian National Energy and Water Supply Regulatory Commission | gnerc.gov.ge | international_agency | official | production, pipeline_outage | proposed |
| ca-GE-port_maritime_authority | GE | — | port_maritime_authority | Batumi Port (BSCP / JSC Batumi Sea Port) | batumiport.com | international_agency | official | vessel_loading, port_closure | unverified |
| ca-GE-national_exchange | GE | — | national_exchange | GSE – Georgian Stock Exchange | gse.ge | exchange | official | pricing_formula | proposed |
| ca-GE-central_bank | GE | — | central_bank | National Bank of Georgia | nbg.gov.ge | international_agency | official | sanctions | proposed |
| ca-GE-environment_regulator | GE | — | environment_regulator | Ministry of Environment and Agriculture | mepa.gov.ge | international_agency | official | pipeline_outage | proposed |
| ca-GE-coast_guard_navy | GE | — | coast_guard_navy | Georgian Coast Guard | coastguard.gov.ge | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GE-port_maritime_authority (Batumi) | Batumi Black Sea port = BTC alternative crude export (Supsa terminal nearby); Batumi Oil Terminal (SOCAR subsidiary) for Azeri crude re-export | Georgia = pro-Western pivot; EU candidate status 2023; Georgian Dream party tensions; Russia-Georgia 2008 war: BTC sabotage proximity precedent | Supsa Marine Terminal (BP operated; ~100 kb/d) = secondary Azeri crude Black Sea export; Batumi → Turkish Straits | **unverified** — batumiport.com ověřit; alternativa: batumi-port.ge |
| ca-GE-mfa | Georgia = BTC host state; každé Russia-Georgia diplomatic crisis = pipeline security alert; Georgian Dream pro-Russian tilt (2024) = Western concern signal | MFA Georgia prohlášení o neutralita/EU vs Russia = tier-1 geopolitical signal pro BTC + TANAP security | BTC Georgian section: 250 km through Georgia; major pump station Gardabani; 2008 war: BTC shut down 3 days | **proposed** |
| ca-GE-upstream_regulator (GNERC) | GNERC = Georgian energy regulator; domestic gas distribution; SOCAR Georgia gas supply; každý GNERC supply interruption order = Georgian industrial demand signal | Georgia imports ~99% gas from Azerbaijan (SOCAR) → complete TANAP-dependent; no Russian gas imports since 2006 | SCP (South Caucasus Pipeline) Georgian section → Turkey interconnect; Gardabani gas distribution hub | **proposed** |

### Expansion sloty
- BTC Co. (Georgian section operator) → btcco.com (BP operated; Georgian segment data)
- Supsa Marine Terminal → bp.com/supsa (Black Sea Azeri crude export)
- SOCAR Georgia → socarge.com (dominant gas distributor Georgia)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 45, "last_country": "GE", "last_batch_seq": 46 }
```
