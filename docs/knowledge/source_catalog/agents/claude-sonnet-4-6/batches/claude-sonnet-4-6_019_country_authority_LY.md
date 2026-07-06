# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_019_country_authority_LY.md  
**Fáze:** country_authority — krok LY (Libya)  
**Datum:** 2026-07-05  

---

## Shrnutí

Libye = komplexní case: split-government (GNU Tripoli vs HoR/LNA Benghazi) + chronické
Force Majeure na ropných terminálech. Kapacita ~1.2 mb/d, ale produkce fluktuuje mezi
0.5–1.3 mb/d podle politické situace. **NOC** (noc.ly) je jediná společná instituce obou
vlád pro ropný sektor a je primárním zdrojem FM deklarací. Libyan light sweet crude (Es Sider,
Sharara grades) je klíčový benchmark pro středomořský krack spread. 7 proposed, 3 unverified;
zvláštní pozornost na dual-government problematiku.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-LY-ministry_petroleum | LY | — | ministry_petroleum | Ministry of Oil and Gas (GNU Tripoli) | nog.gov.ly | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-LY-noc | LY | — | noc | NOC – National Oil Corporation | noc.ly | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-LY-mfa | LY | — | mfa | Ministry of Foreign Affairs (GNU Tripoli) | foreign.gov.ly | international_agency | official | sanctions, policy | proposed |
| ca-LY-customs_export | LY | — | customs_export | Libyan Customs Authority | customs.gov.ly | international_agency | official | exports, export_license | unverified |
| ca-LY-upstream_regulator | LY | — | upstream_regulator | NOC (dual role — upstream regulator and NOC) | noc.ly | international_agency | official | production, force_majeure | proposed |
| ca-LY-port_maritime_authority | LY | — | port_maritime_authority | Libyan Ports Authority | lpa.gov.ly | international_agency | official | vessel_loading, port_closure | unverified |
| ca-LY-national_exchange | LY | — | national_exchange | LSM – Libyan Stock Market | lsm.ly | exchange | official | pricing_formula | unverified |
| ca-LY-central_bank | LY | — | central_bank | CBL – Central Bank of Libya (Tripoli) | cbl.gov.ly | international_agency | official | sanctions | proposed |
| ca-LY-environment_regulator | LY | — | environment_regulator | GAEB – General Authority for the Environment | gaeb.gov.ly | international_agency | official | refinery_outage | proposed |
| ca-LY-coast_guard_navy | LY | — | coast_guard_navy | Libyan Coast Guard (GNU-aligned) | lna.gov.ly | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (výběr klíčových)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-LY-noc (NOC noc.ly) | NOC je JEDINÝ trader-relevantní primary source pro libyjskou ropu: vydává FM deklarace, produkční reporty, terminal status; obě vládní frakce uznávají NOC autoritu | NOC funguje jako de-facto neutrální entita i za politického rozdělení; NOC chairman (Bengdara od 2022) komunikuje přes noc.ly | Es Sider, Ras Lanuf, Brega, Zueitina, Mellitah, Zawiya terminály — všechny pod NOC force majeure framework | **proposed** — noc.ly aktivní; tier-1 pro FM monitoring |
| ca-LY-ministry_petroleum (Ministry of Oil) | GNU Tripoli MOG vydává politiku ale NOC má operační autonomii; MOG prohlášení jsou sekundární k NOC | GNU kontroluje Tripoli/West; HoR Benghazi kontroluje East (kde jsou klíčové terminály Es Sider/Ras Lanuf); každá eskalace mezi frakcemi = FM risk | GNU policy pro Waha, Sharara, El Feel fields | **proposed** — nog.gov.ly: ověřit přesnou doménu; alternativně mog.gov.ly |
| ca-LY-central_bank (CBL) | CBL Tripoli = mezinárodně uznávaná; manages ropné příjmy | Historicky split CBL (2014–2021); dočasně reunifikovaná; každý CBL split = sovereign dysfunction signal | CBL financuje NOC operace; ropné příjmy přes CBL clearing | **proposed** — cbl.gov.ly aktivní |
| ca-LY-coast_guard_navy | Libyan Coast Guard (GNU-aligned) patroluje pobřeží; LNA (East) má vlastní námořní jednotky | Dvojí námořní autorita; migrantská krize; každý incident u terminálů = FM risk | Mellitah (offshore platform) a Bouri field security | **proposed** — lna.gov.ly je Libyan Naval Authority (GNU); ověřit zda správný název; LNA (Libyan National Army East) je jiná entita |

### Analytická poznámka: Libya monitoring
- **Tier-1**: noc.ly FM deklarace → každý Force Majeure announcement = okamžitý $0.50–$1.50 Brent spike
- **Tier-2**: UN Panel of Experts Libya reports (un.org/securitycouncil)
- Fieldwatch: Sharara (El Fil/Murzuq Basin) je nejzranitelnější vůči tribal/militia interruptions

### Expansion sloty
- Repsol Libya / TotalEnergies Libya press releases (IOC FM notices)
- NOC sub-terminals: Waha Oil Company, Arabian Gulf Oil Company (AGOCO)

---

## Progress po merge (návrh)
```json
{ "phase": "country_authority", "phase_index": 18, "last_country": "LY", "last_batch_seq": 19 }
```
