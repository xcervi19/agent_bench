# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_006_country_authority_RU.md  
**Fáze:** country_authority — krok RU (Russia)  
**Datum:** 2026-07-05  

---

## Shrnutí

Fáze 2, dávka 4 — Russia × 10 authority types. Rusko je třetí největší producer ropy
(~10 mb/d) a dominantní dodavatel plynu do Evropy. Od invaze 2022 je pod masivními
sankcemi G7/EU, což vytváří unikátní monitorovací logiku: **primární signály nejsou
ruské vládní weby** (propaganda, zpoždění), ale jejich protistrana — OFAC/EEAS sankční
opatření, G7 price cap, Urals discount na SPIMEX, Transneft pipeline flows. Přesto jsou
ruské primární domény nezbytné jako základ pro sledování: Rosneft zveřejňuje quarterly
produkční data (IFRS disclosure), Minenergo vydává statistiky, mid.ru je tier-1 diplomatický
signál. Celkem **10 slotů**; 8 proposed, 2 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-RU-ministry_petroleum | RU | — | ministry_petroleum | Minenergo – Ministry of Energy of Russia | minenergo.gov.ru | international_agency | official | policy, export_license, quota_rhetoric, production | proposed |
| ca-RU-noc | RU | — | noc | Rosneft | rosneft.ru | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-RU-mfa | RU | — | mfa | MFA Russia – Ministry of Foreign Affairs | mid.ru | international_agency | official | sanctions, policy | proposed |
| ca-RU-customs_export | RU | — | customs_export | FCS – Federal Customs Service of Russia | customs.gov.ru | international_agency | official | exports, export_license | proposed |
| ca-RU-upstream_regulator | RU | — | upstream_regulator | Rosnedra – Federal Agency for Subsoil Use | rosnedra.gov.ru | international_agency | official | production, refinery_outage | proposed |
| ca-RU-port_maritime_authority | RU | — | port_maritime_authority | Rosmorrechflot – Federal Agency for Maritime & River Transport | morflot.ru | international_agency | official | vessel_loading, port_closure | proposed |
| ca-RU-national_exchange | RU | — | national_exchange | SPIMEX – Saint Petersburg International Mercantile Exchange | spimex.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-RU-central_bank | RU | — | central_bank | CBR – Bank of Russia | cbr.ru | international_agency | official | sanctions | proposed |
| ca-RU-environment_regulator | RU | — | environment_regulator | Rosprirodnadzor – Federal Service for Supervision of Natural Resources | rpn.gov.ru | international_agency | official | refinery_outage, pipeline_outage | proposed |
| ca-RU-coast_guard_navy | RU | — | coast_guard_navy | Russian Navy (Black Sea / Pacific Fleet) | mil.ru | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-RU-ministry_petroleum | Minenergo publikuje měsíční statistiky produkce a exportu; ministr Shulginov (od 2020) vyjádření o OPEC+ compliance jsou price-moving | Minenergo koordinuje ruský postoj v OPEC+; každé oznámení o dobrovolných škrtech pohybuje trhem | Ministerstvo schvaluje exportní kvóty pro Transneft pipeline allocation | **proposed** — minenergo.gov.ru aktivní ruský vládní domain |
| ca-RU-noc | Rosneft = 40 % ruské produkce (4–4.5 mb/d); quarterly IFRS reports jsou jedny z mála reliable supply dat z Ruska post-2022 | Rosneft CEO Sechin je osobní vazba na Kreml; každý Sechin výrok o sankcích je geopolitický signal | Rosneft prodává Urals crude přes Primorsk (Baltik) a Novorossiysk (ČM) + ESPO přes Kozmino | **proposed** — rosneft.ru aktivní; anglická IR sekce dostupná ze Západu |
| ca-RU-mfa | Nízký přímý supply signal | mid.ru = tier-1 zdroj pro ruská diplomatická prohlášení; každý Lavrov výrok o energetické zbraňovizaci nebo Hormuz spolupráci pohybuje risk premium | Nízká přímá logistická role | **proposed** — mid.ru je ověřený domain; dostupný ze Západu |
| ca-RU-customs_export | FCS publikuje export data (zpoždění 2 měsíce post-2022; část dat utajená); obchodní statistiky čtelné přes UN COMTRADE | FCS administruje exportní licence pro crude/plynu; pod sankcemi část dokumentace přes third-country re-export (Indie, Turecko) | Dokumentace k Transneft pipeline loadingům; customs clearance pro LNG (Yamal/ESPO) | **proposed** — customs.gov.ru aktivní; datová dostupnost omezená post-sanctions |
| ca-RU-upstream_regulator | Rosnedra vydává licence pro upstream bloky; klíčový pro długodobý supply outlook (Greenfield Siberia, Arctic) | Rosnedra pod kontrolou státu; sankcemi omezený přístup k zahraniční technologii pro Arctic drilling → long-term supply constraint | Licence pokrývají Vankor, Samotlor, ESPO upstream | **proposed** — rosnedra.gov.ru je ověřená ruská vládní doména |
| ca-RU-port_maritime_authority | Rosmorrechflot reguluje přístavy Primorsk, Ust-Luga, Novorossiysk, Kozmino; udržovací oznámení = export disruption signal | Podléhá MoT; pod sankcemi západní lodní společnosti opustily ruské přístavy; TMT/shadow fleet obsadila prostor | Port cirkuláře pro Novorossiysk (CPC terminál), Primorsk (Transneft), Kozmino (ESPO) | **proposed** — morflot.ru aktivní |
| ca-RU-national_exchange | SPIMEX publikuje Urals export blend price; Russian Urals CIF Rotterdam byl replaced by SPIMEX quotes post-2022; key pro G7 price cap compliance monitoring ($60 ceiling) | SPIMEX je kritický indicator pro price cap breach monitoring; US Treasury sleduje zda Urals > $60/bbl | SPIMEX clearing pro OTC ruské ropné swapy; delivery point Primorsk | **proposed** — spimex.com je aktivní a přístupný |
| ca-RU-central_bank | CBR spravuje ruské FX rezervy ($600 bn pre-sanction, ~$300 bn zmrazeno 2022); CBR FX sales/policy → proxy pro ropný příjem | CBR je primárním cílem G7 zmrazení; každý update o zmrazených rezervách je geopolitický signal | CBR financuje Rosneft/Gazprom transakce; alternativní settlement přes Rupia/Yuan | **proposed** — cbr.ru aktivní a dostupný |
| ca-RU-environment_regulator | Rosprirodnadzor může nařídit zastavení pro znečištění (vzácné; Norilsk 2020 případ); pipeline integrity inspekce | Nízká přímá geopolitická role | Pipeline integrity pokrývá Druzhba/ESPO; rafinerie compliance | **proposed** — rpn.gov.ru ověřitelná doména |
| ca-RU-coast_guard_navy | Ruské námořnictvo blokuje Černé moře (post-2022); Black Sea Fleet = Novorossiysk / CPC export constraint; Tichomořská flotila = Kozmino | Černomořská blokáda ovlivňuje CPC/Azeri flows; každé vojenské cvičení nebo minová hrozba → Novorossiysk spread spike | Black Sea tanker corridor (Bospor je turecká sféra ale BF ovlivňuje vstup); Kozmino ESPO loader nemá námořní hrozbu | **unverified** — mil.ru je MoD domain; ruské námořnictvo (VMF) má sub-stránku na mil.ru/navy nebo navy.mil.ru; ověřit správnou sub-URL |

---

## Expansion sloty (pro budoucí dávky)

| entita | domain | poznámka |
|--------|--------|----------|
| Gazprom | gazprom.ru | Dominantní Russian gas; ESPO pipeline partner; LNG via Sakhalin |
| Novatek | novatek.ru | Yamal LNG, Arctic LNG 2; tier-1 LNG signál |
| Lukoil | lukoil.ru | Largest private Russian oil co; ~15 % produkce |
| Transneft | transneft.ru | State pipeline monopoly; Druzhba, ESPO, Primorsk flows |
| Gazprom Neft | gazprom-neft.ru | Gazprom's oil arm; Siberia, Black Sea shelf |
| FGUP Rosmorport | rosmorport.ru | Port operator (FSUE); spravuje Primorsk a Novorossiysk terminály |

---

## Unverified / Anti-patterns

### Unverified záznamy

| id | entity | domain navržená | problém |
|----|--------|----------------|---------|
| ca-RU-coast_guard_navy | Russian Navy (VMF) | mil.ru | mil.ru je MoD; VMF sub-stránka: ověřit navy.mil.ru nebo mil.ru/navy |

### Ruská specifika pro monitoring post-2022

- **Urals tracking**: SPIMEX quote + Argus Urals FOB Primorsk (Argus = aggregator ale de-facto benchmark post-Platts exit) + India import data (PPAC).
- **Shadow fleet**: Equasis + Lloyd's List Intelligence pro tracking bez AIS; ABS/DNV class withdrawal = sanctions enforcement signal.
- **G7 price cap**: US Treasury OFAC + UK OFSI vydávají compliance guidance; každá změna $60 cap = tier-1 event.
- Rosneft a Gazprom jsou SDN-adjacent ale ne přímo SDN-listed; situace se mění — sledovat OFAC aktualizace.

### Anti-patterns

- RT/TASS/RIA Novosti — státní propaganda; žádný primární analytický signál.
- Kommersant/Vedomosti — ruská media; sekundární; doménová přístupnost po 2022 omezená.
- Sberbank CIB výzkum — distributor pod sankcemi.

---

## Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 5,
  "last_country": "RU",
  "crosscheck_cursor": 0,
  "last_batch_seq": 6
}
```

Po merge → **další dávka:** `claude-sonnet-4-6_007_country_authority_US.md`
(Fáze 2, pátá země = US – United States, 10 authority types).
