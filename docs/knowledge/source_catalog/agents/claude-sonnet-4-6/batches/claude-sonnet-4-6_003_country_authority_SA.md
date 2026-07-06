# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_003_country_authority_SA.md  
**Fáze:** country_authority — krok SA (Saudi Arabia)  
**Datum:** 2026-07-04  

---

## Shrnutí

Fáze 2, dávka 1 — Saudi Arabia × 10 authority types. Saudi Arabia je primárně nejdůležitější
producent pro crude/LNG coverage: Aramco OSP pohybuje asijský benchmark, ministerstvo energie
nastavuje kvóty OPEC+, Mawani provozuje Ras Tanura a Yanbu. Celkem **10 slotů**; 8 proposed,
1 unverified (national_exchange), 1 analytická poznámka ke zdvojené doméně
(ministry_petroleum = upstream_regulator ve SA). Merge do catalog.json po schválení.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-SA-ministry_petroleum | SA | — | ministry_petroleum | Saudi Ministry of Energy | energy.gov.sa | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-SA-noc | SA | — | noc | Saudi Aramco | aramco.com | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-SA-mfa | SA | — | mfa | Saudi Ministry of Foreign Affairs | mofa.gov.sa | international_agency | official | sanctions, policy | proposed |
| ca-SA-customs_export | SA | — | customs_export | ZATCA – Zakat, Tax and Customs Authority | zatca.gov.sa | international_agency | official | exports, export_license | proposed |
| ca-SA-upstream_regulator | SA | — | upstream_regulator | Saudi Ministry of Energy (upstream licensing) | energy.gov.sa | international_agency | official | production, refinery_outage | proposed |
| ca-SA-port_maritime_authority | SA | — | port_maritime_authority | Saudi Ports Authority (Mawani) | mawani.gov.sa | international_agency | official | vessel_loading, port_closure | proposed |
| ca-SA-national_exchange | SA | — | national_exchange | Saudi Exchange (Tadawul) | saudiexchange.com.sa | exchange | official | pricing_formula, term_contract | unverified |
| ca-SA-central_bank | SA | — | central_bank | SAMA – Saudi Central Bank | sama.gov.sa | international_agency | official | sanctions | proposed |
| ca-SA-environment_regulator | SA | — | environment_regulator | NCEC – National Center for Environmental Compliance | ncec.gov.sa | international_agency | official | refinery_outage | proposed |
| ca-SA-coast_guard_navy | SA | — | coast_guard_navy | Saudi Coast Guard (Haras al-Sahl) | coastguard.gov.sa | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-SA-ministry_petroleum | Ministerstvo energie nastavuje Saudi produkční target a výchozí bod OPEC+ kvóty; přímý supply signal při každém oznámení ministra | Ministr Abdulaziz bin Salman → osobní vazba na krále; sdělení na press konferencích OPEC jsou price-moving ještě před MOMR | Nastavuje export policy; schvaluje Aramco OSP metodiku → logistický dopad na term contract ceny | **proposed** |
| ca-SA-noc | Saudi Aramco = 10–10.5 mb/d kapacita; každá změna output target nebo maintenance hláška pohybuje Brent/WTI o $1–3 | Aramco quarterly report + Investor Day = sovereign výhled; IPO-obligace transparency vyšší než u jiných NOC | Aramco provozuje Ras Tanura (5 mb/d), Yanbu, Rabigh; loading data = lagging signal ale officiální | **proposed** |
| ca-SA-mfa | MFA komunikuje postoj KSA k sankčnímu režimu USA/EU na Írán; diplomatické prohlášení ovlivňuje risk premium | Klíčový hráč Gulf Cooperation; sdělení o Jemenu, Íránu, Rusku pohybují geopolitickým spreadem | Nízká přímá logistická role | **proposed** |
| ca-SA-customs_export | ZATCA spravuje export deklarace; data o objemech exportu (zpoždění) | Sankční compliance: ZATCA ověřuje konečné destinace exportu crude | Dokumentace k lading bills; export license pro crude a produkty | **proposed** |
| ca-SA-upstream_regulator | Totožná instituce jako ministry_petroleum (energy.gov.sa) — v KSA není oddělený upstream regulator; role splývají | Ministerstvo vydává upstream licence Aramco; fakticky oligopol jednoho NOC | Upstream regulace = podmínka pro Aramco operace v Ghawar, Safaniya, Khurais | **proposed** — duplikátní doména s ca-SA-ministry_petroleum; entity je odlišná (jiná role); oba záznamy zachovat s poznámkou |
| ca-SA-port_maritime_authority | Mawani provozuje Ras Tanura (klíčový export point) a Yanbu; kongesce nebo uzávěra = 5–7% global supply risk | Mawani podléhá sovereignu; embargo nebo válečná událost v Zálivu = port closure trigger | Vessel scheduling, loading windows, port dues; Mawani.gov.sa vydává lodní oběžníky | **proposed** |
| ca-SA-national_exchange | Tadawul obchoduje Aramco akcie (2222.SR); volatilita Aramco equity = sentiment signal | Tadawul není komoditní burza; crude pricing se nenastavuje přes Tadawul | Žádná přímá logistická role | **unverified** — domain saudiexchange.com.sa ověřit; Tadawul je equity, ne commodity exchange; zvážit `empty` po review |
| ca-SA-central_bank | SAMA spravuje petrodolarové rezervy; policy rate ovlivňuje SAR peg → indirektní vliv na crude pricing USD baseline | SAMA monitoruje sankční compliance finančního systému; petrodolar flows přes SAMA | SAMA neovlivňuje přímo lodní logistiku | **proposed** |
| ca-SA-environment_regulator | NCEC audity rafinerií (Ras Tanura, Yanbu) mohou vyústit ve výpadek rafinerie | NCEC pod MEWA; vládní entita; politicky motivované výpadky by se hlásily přes NCEC | Rafinerie downtime → produkty supply shock | **proposed** |
| ca-SA-coast_guard_navy | Saudi Coast Guard chrání ropné terminály Ras Tanura a Yanbu; hrozba dronu/rakety (Houthi) → okamžitá port closure | Námořní složky MO v Zálivu; Hormuz patrol přímo ovlivňuje Aramco export koridory | Loading terminal security; escort pro VLCC convoy při zvýšeném riziku | **proposed** — domain coastguard.gov.sa zatím neověřen z externího zdroje; vysoká věrohodnost dle gov.sa vzoru |

---

## Unverified / Anti-patterns

### Unverified záznamy

| id | entity | domain navržená | problém |
|----|--------|----------------|---------|
| ca-SA-national_exchange | Saudi Exchange (Tadawul) | saudiexchange.com.sa | Tadawul je equity exchange, ne commodity; zvážit `empty` nebo ponechat jako low-priority equity sentiment proxy |
| ca-SA-coast_guard_navy | Saudi Coast Guard | coastguard.gov.sa | Domain neověřen externě; gov.sa vzor vysoká pravděpodobnost; manuálně validovat |

### Duplicitní doménová poznámka

`ca-SA-ministry_petroleum` a `ca-SA-upstream_regulator` sdílejí doménu `energy.gov.sa`.
V KSA je Ministry of Energy souběžně petroleum ministry i upstream regulátor — žádná oddělená agentura neexistuje.
Oba záznamy zachovat se zřetelně odlišnými `entity` a `authority_type`; sloučení do whitelistu = 1 entry s kombinovanými signals.

### Anti-patterns

- Aramco IR microsite (aramco.com/en/investors) — sub-feed, ne samostatná entita; zachytit jako expansion slot v budoucí dávce.
- Saudi Gazette / Arab News — mediální agregátoři; žádná primární role.
- Argus Arabia — sekundární agregátor.

---

## Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 1,
  "last_country": "SA",
  "crosscheck_cursor": 0,
  "last_batch_seq": 3
}
```

Po merge → **další dávka:** `claude-sonnet-4-6_004_country_authority_IR.md`
(Fáze 2, druhá země = IR – Iran, 10 authority types).
