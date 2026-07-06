# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_037_country_authority_ES.md  
**Fáze:** country_authority — krok ES (Spain)  
**Datum:** 2026-07-06  

---

## Shrnutí

Spain = **největší LNG regasifikační kapacita v EU** (6 terminálů; ~40% EU LNG regasifikace);
klíčový vstupní bod pro US + Qatarský LNG do Evropy. Repsol (IOC, Spanish state ~0%
ale strategic company). Produkce minimální (~30 kb/d). Klíčové signály: **CORES
(Corporación de Reservas Estratégicas) stockpile data**, **Regas terminal sendout**
(Enagas; Enagás.es je dominantní gas TSO), **Algeciras straits transit** (Gibraltar).
Algeria–Spain Medgaz pipeline (8 bcm/yr; po přerušení Gazoduc Maroc-Europe 2021).
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-ES-ministry_petroleum | ES | — | ministry_petroleum | MITECO – Ministry for Ecological Transition and Demographic Challenge | miteco.gob.es | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-ES-noc | ES | — | noc | Repsol S.A. | repsol.com | international_agency | official | production, exports, force_majeure, term_contract | proposed |
| ca-ES-mfa | ES | — | mfa | Ministerio de Asuntos Exteriores | exteriores.gob.es | international_agency | official | sanctions, policy | proposed |
| ca-ES-customs_export | ES | — | customs_export | AEAT – Agencia Estatal de Administración Tributaria (Customs) | aeat.es | international_agency | official | imports, exports | proposed |
| ca-ES-upstream_regulator | ES | — | upstream_regulator | MITECO / CNMC (upstream concessions) | cnmc.es | international_agency | official | production, refinery_outage | proposed |
| ca-ES-port_maritime_authority | ES | — | port_maritime_authority | Puertos del Estado | puertos.es | international_agency | official | vessel_loading, port_closure | proposed |
| ca-ES-national_exchange | ES | — | national_exchange | MIBGAS – Iberian Gas Market / OMIP | mibgas.es | exchange | official | pricing_formula, term_contract | proposed |
| ca-ES-central_bank | ES | — | central_bank | Banco de España | bde.es | international_agency | official | pricing_formula | proposed |
| ca-ES-environment_regulator | ES | — | environment_regulator | MITECO (environment division, dual) | miteco.gob.es | international_agency | official | refinery_outage | proposed |
| ca-ES-coast_guard_navy | ES | — | coast_guard_navy | Armada Española (Spanish Navy) | armada.defensa.gob.es | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-ES-port_maritime_authority (Puertos del Estado) | Spain = 6 LNG regasification terminals (Enagas operated: Barcelona, Huelva, Cartagena, Sagunto, Bilbao, Mugardos/Ferrol); ~40% EU LNG import capacity; každý sendout report = tier-1 European gas supply signal | Spain-Algeria Medgaz pipeline (8 bcm); Spain odmítla obnovit GME (Maroc-Europe, přes Maroko, ukončen 2021) → diplomatická ostuda s Alžírem; Gibraltar chokepoint (Strait of Gibraltar) | Algeciras Bay = kontejnerové přestupní centrum; Gibraltar Strait VLCC transit (~3–4 mb/d Atlantic–Mediterranean); Bilbao LNG Enagás terminal | **proposed** — puertos.es aktivní |
| ca-ES-national_exchange (MIBGAS) | MIBGAS = Iberian gas spot market (Spain + Portugal); daily NBP-correlated gas price; TTF arbitrage přes LNG from US; MIBGAS PVB (Point of Virtual Balancing) = tier-1 Iberian gas price signal | MIBGAS under MITECO regulatory oversight; post-Iberian Exception price cap (2022–2023); Spain-France gas interconnection limited (bottleneck) | Enagas VTP + transmission network; MIBGAS physical delivery at Spanish entry points | **proposed** — mibgas.es aktivní |
| ca-ES-noc (Repsol) | Repsol = Spanish IOC (no meaningful state ownership); upstream ~600 kboed (USA Permian, North Sea, Libya, Algeria, Bolivia, Peru, Trinidad); každý Repsol quarterly = signal for LatAm + Africa supply | Repsol Bolivia operations (LNG Bolivia project); Repsol North Sea (Tracy-1 Norwegian Sea) | Repsol Cartagena refinery (~220 kb/d); Repsol Bilbao refinery; Repsol Petronor (Bilbao, País Vasco) | **proposed** — repsol.com aktivní |

### Analytická poznámka: Spain = EU LNG entry hub
- Spain's 6 terminals = swing capacity pro celou EU v LNG krizi
- MIBGAS PVB price vs TTF = spread signal pro LNG routing (US LNG diversion Spain vs NW Europe)
- Expansion: Enagas → enagas.es (gas TSO + LNG terminal operator; tier-1 Spanish gas signal)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 36, "last_country": "ES", "last_batch_seq": 37 }
```
