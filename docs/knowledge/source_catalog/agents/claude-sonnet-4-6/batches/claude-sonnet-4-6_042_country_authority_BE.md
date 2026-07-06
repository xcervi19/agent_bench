# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_042_country_authority_BE.md  
**Fáze:** country_authority — krok BE (Belgium)  
**Datum:** 2026-07-06  

---

## Shrnutí

Belgium = **Zeebrugge LNG terminal** = tier-1 European LNG hub (11 bcm/y; historicky
základní cena ZEE = NBP proxy). Antwerp = druhý největší evropský přístav.
ARA (Amsterdam–Rotterdam–Antwerp) barge product market = European product pricing centrum.
Fluxys = klíčový TSO (belgický + mezinárodní: Zeebrugge, interconnect DE/FR/UK).
Žádný domácí upstream. 9 proposed, 1 empty (noc).

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-BE-ministry_petroleum | BE | — | ministry_petroleum | FPS Economy (Energy Division) | economie.fgov.be | international_agency | official | policy, import_licensing | proposed |
| ca-BE-noc | BE | — | noc | — (no Belgian state NOC) | — | — | — | — | empty |
| ca-BE-mfa | BE | — | mfa | SPF Affaires Étrangères | diplomatie.belgium.be | international_agency | official | sanctions, policy | proposed |
| ca-BE-customs_export | BE | — | customs_export | ADBS – Administration Générale des Douanes et Accises | fiscus.fgov.be | international_agency | official | imports, exports | proposed |
| ca-BE-upstream_regulator | BE | — | upstream_regulator | CREG – Commission de Régulation de l'Électricité et du Gaz | creg.be | international_agency | official | production, pipeline_outage | proposed |
| ca-BE-port_maritime_authority | BE | — | port_maritime_authority | Port of Antwerp-Bruges | portofantwerpbruges.com | international_agency | official | vessel_loading, port_closure | proposed |
| ca-BE-national_exchange | BE | — | national_exchange | Euronext Brussels | euronext.com | exchange | official | pricing_formula | proposed |
| ca-BE-central_bank | BE | — | central_bank | National Bank of Belgium | nbb.be | international_agency | official | pricing_formula | proposed |
| ca-BE-environment_regulator | BE | — | environment_regulator | IRCEL – Belgian Interregional Environment Agency | irceline.be | international_agency | official | refinery_outage | proposed |
| ca-BE-lng_hub | BE | — | port_maritime_authority | Fluxys – Belgian Gas TSO + Zeebrugge LNG | fluxys.com | international_agency | official | vessel_loading, term_contract, pricing_formula | proposed |

---

## Poznámka ke struktuře
`ca-BE-lng_hub` použit jako druhý port/infrastructure slot namísto coast_guard_navy
(Belgian Navy minimální relevance; Fluxys/Zeebrugge = tier-1 Belgian energy signal).

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-BE-lng_hub (Fluxys/Zeebrugge) | **TIER-1**: Zeebrugge LNG terminal (11 bcm/y; Fluxys operated); hub pro US LNG do Evropy; Qatargas long-term contracts; každý Zeebrugge sendout = European winter gas supply signal; ZEE day-ahead = NBP correlated | Fluxys = Belgian TSO + minority stakeholder v Interconnector (UK-Belgium pipeline); Fluxys shareholding v Dunkerque LNG (France) | Zeebrugge UK–Belgium Interconnector (IUK; 20 bcm/y bidirectional); Zeebrugge = ARA crude feeder via river barge | **proposed** — fluxys.com aktivní |
| ca-BE-port_maritime_authority (Antwerp-Bruges) | Port of Antwerp-Bruges = ARA hub; crude tanker arrivals feed Shell Antwerp (~360 kb/d) + Total Antwerp petrochemicals; ARA product barge market = European crack spread signal; monthly tonnage stats | Antwerp = 2nd largest EU port by tonnage; ISPS security compliance; Belgium = EU Council permanent host | IUK Interconnector landing + Zeebrugge FSRU; canal transport to German Ruhr region | **proposed** |
| ca-BE-upstream_regulator (CREG) | CREG reguluje belgický gas + electricity trh; ZEE gas hub price oversight; každé CREG tariff decision = Fluxys throughput cost signal | CREG kooperuje s ACER (EU agency); Belgium nuclear fleet exit timeline (Doel 4, Tihange 3 extended to 2035) = LNG demand signal | Fluxys interconnect DE/FR/UK + Zeebrugge terminal | **proposed** |

### Expansion sloty
- Elia → elia.be (Belgian electricity TSO; nuclear + LNG demand proxy)
- Shell Antwerp → shell.be (Antwerp refinery ~360 kb/d; ARA product hub)
- IUK Interconnector → interconnector.com (UK-Belgium gas pipeline; bidirectional)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 41, "last_country": "BE", "last_batch_seq": 42 }
```
