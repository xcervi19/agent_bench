# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_041_country_authority_GB.md  
**Fáze:** country_authority — krok GB (United Kingdom)  
**Datum:** 2026-07-06  

---

## Shrnutí

UK = **North Sea Brent = globální crude benchmark** (ICE Brent futures). NSTA (North
Sea Transition Authority) = upstream regulator. UK produkce ~1 mb/d (klesající) + net
crude importer. BP (IOC, British origins) + Shell (Anglo-Dutch). Klíčové signály:
**NSTA production data**, **ICE Brent forward curve** (ICE London = tier-1),
**National Grid ESO gas storage** (UK NBP gas hub = druhý nejlikvidnější po TTF).
Dragon LNG (Wales), South Hook LNG (Milford Haven) = UK LNG terminals (Qatar supply).
9 proposed, 1 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-GB-ministry_petroleum | GB | — | ministry_petroleum | DESNZ – Department for Energy Security and Net Zero | gov.uk/desnz | international_agency | official | policy, import_licensing, quota_rhetoric | proposed |
| ca-GB-noc | GB | — | noc | NSTA – North Sea Transition Authority (upstream authority) | nstauthority.co.uk | international_agency | official | production, force_majeure | proposed |
| ca-GB-mfa | GB | — | mfa | FCDO – Foreign, Commonwealth and Development Office | gov.uk/fcdo | international_agency | official | sanctions, policy | proposed |
| ca-GB-customs_export | GB | — | customs_export | HMRC – HM Revenue and Customs | hmrc.gov.uk | international_agency | official | imports, exports | proposed |
| ca-GB-upstream_regulator | GB | — | upstream_regulator | NSTA – North Sea Transition Authority | nstauthority.co.uk | international_agency | official | production, force_majeure | proposed |
| ca-GB-port_maritime_authority | GB | — | port_maritime_authority | MCA – Maritime and Coastguard Agency | gov.uk/mca | international_agency | official | vessel_loading, port_closure | proposed |
| ca-GB-national_exchange | GB | — | national_exchange | ICE – Intercontinental Exchange (London) | theice.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-GB-central_bank | GB | — | central_bank | Bank of England | bankofengland.co.uk | international_agency | official | pricing_formula, sanctions | proposed |
| ca-GB-environment_regulator | GB | — | environment_regulator | NSTA (environment + decommissioning, dual) | nstauthority.co.uk | international_agency | official | refinery_outage, force_majeure | proposed |
| ca-GB-coast_guard_navy | GB | — | coast_guard_navy | Royal Navy | royalnavy.mod.uk | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-GB-national_exchange (ICE London) | **TIER-1 global**: ICE Brent = globální crude benchmark; ICE TTF gas (co-located s Dutch contract); ICE gasoil = European diesel benchmark; ICE Brent forward curve = tier-1 price signal for all crude markets | ICE regulated by FCA (UK); post-Brexit ICE London maintains EU access via ICE Endex; ICE Carbon (EUA futures) | ICE physical Brent delivery: BFOET basket (Brent, Forties, Oseberg, Ekofisk, Troll); North Sea physical market | **proposed** — theice.com aktivní; tier-1 |
| ca-GB-noc (NSTA) | NSTA (North Sea Transition Authority, ex-OGA) = UK upstream regulator + quasi-NOC role (no equity); monthly UKCS production data; Forties pipeline system (Ineos operated, ~450 kb/d); každá Forties pipeline outage = Brent price spike | NSTA licencing round data; maximising North Sea recovery vs net zero tension; Rosebank, Jackdaw field approvals | Flotta terminal (Orkney), Sullom Voe (Shetland), Kinneil, Grangemouth refinery (PetroIneos, ~150 kb/d) | **proposed** — nstauthority.co.uk aktivní |
| ca-GB-mfa (FCDO) | FCDO = UK sanctions authority (OFSI sub-office); UK Russia sanctions = Russian crude G7 price cap enforcement; FCDO trade sanctions decisions | UK post-Brexit independent sanctions regime (OFSI); UK Iran sanctions; Venezuela targeted sanctions; FCDO statements on energy security | UK-Norway North Sea cooperation; UKCS-Norway cross-border pipelines (FLAGS, SAGE, Langeled) | **proposed** |

### Expansion sloty
- National Grid ESO → nationalgrideso.com (UK gas + electricity TSO; NBP physical delivery)
- BP → bp.com (major UK-origin IOC; North Sea, Gulf of Mexico, Azerbaijan ACG; quarterly tier-1)
- South Hook LNG → southhooklng.com (Milford Haven; Qatar RasGas long-term; ~15 bcm/y)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 40, "last_country": "GB", "last_batch_seq": 41 }
```
