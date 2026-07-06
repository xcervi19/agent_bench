# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_005_country_authority_IQ.md  
**Fáze:** country_authority — krok IQ (Iraq)  
**Datum:** 2026-07-05  

---

## Shrnutí

Fáze 2, dávka 3 — Iraq × 10 authority types. Irák je druhý největší producent OPEC
(~4.2–4.5 mb/d) a chronicky nad kvótou. Klíčové signály: **SOMO OSP** (Official Selling
Price nastavuje asijský bazal), **Basra terminál** (Khor al-Amaya SPM + Fao offloading
buoys), **KRG Kirkuk** (sporná oblast, pipeline Ceyhan), **OPEC non-compliance** (každé
irácké překročení kvóty = geopolitický třecí bod). Složitost: MOO a SOMO sdílejí doménu;
KRG má vlastní export jurisdikci (expansion slot). Celkem **10 slotů**; 6 proposed,
4 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IQ-ministry_petroleum | IQ | — | ministry_petroleum | Iraqi Ministry of Oil | oil.gov.iq | international_agency | official | policy, export_license, quota_rhetoric, production | proposed |
| ca-IQ-noc | IQ | — | noc | SOMO – State Oil Marketing Organization | somo.oil.gov.iq | international_agency | official | exports, pricing_formula, term_contract | unverified |
| ca-IQ-mfa | IQ | — | mfa | Iraqi Ministry of Foreign Affairs | mofa.gov.iq | international_agency | official | sanctions, policy | proposed |
| ca-IQ-customs_export | IQ | — | customs_export | GCA – General Customs Authority of Iraq | customs.gov.iq | international_agency | official | exports, export_license | unverified |
| ca-IQ-upstream_regulator | IQ | — | upstream_regulator | Ministry of Oil (upstream licensing) | oil.gov.iq | international_agency | official | production, refinery_outage | proposed |
| ca-IQ-port_maritime_authority | IQ | — | port_maritime_authority | GAIP – General Authority for Iraqi Ports | iraqiports.gov.iq | international_agency | official | vessel_loading, port_closure | unverified |
| ca-IQ-national_exchange | IQ | — | national_exchange | ISX – Iraq Stock Exchange | isx.iq | exchange | official | pricing_formula | unverified |
| ca-IQ-central_bank | IQ | — | central_bank | CBI – Central Bank of Iraq | cbi.iq | international_agency | official | sanctions | proposed |
| ca-IQ-environment_regulator | IQ | — | environment_regulator | Iraqi Ministry of Environment | environment.gov.iq | international_agency | official | refinery_outage | proposed |
| ca-IQ-coast_guard_navy | IQ | — | coast_guard_navy | Iraqi Navy (Al-Quwwat al-Bahriyya al-Iraqiyya) | mod.mil.iq | international_agency | official | port_closure, force_majeure | proposed |

---

## Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IQ-ministry_petroleum | MOO nastavuje produkční target a Basra Heavy/Basra Medium export cíle; ministr Hayan Abdul-Ghani tiskové konference jsou OPEC compliance signal | Iraq je OPEC's nejproblematičtější člen kvůli chronickému překračování kvót; každé MOO oznámení o "kompenzačních škrtech" pohybuje trhem | MOO koordinuje SOMO a Basra Oil Company (BOC) exportní scheduling; oil.gov.iq vydává produkční statistiky | **proposed** — oil.gov.iq je ověřitelná iraácká vládní doména |
| ca-IQ-noc | SOMO je primární trader-relevantní entita pro Irák: nastavuje měsíční OSP pro Basra Heavy a Basra Medium, podepisuje term kontrakty s asijskými rafineriemi | SOMO announcements o OSP jsou okamžitý tržní signal; rozdíl Basra Heavy – Arab Heavy OSP = arb indicator pro blendery | SOMO kontroluje crude allokaci přes VLCC loadingy na SPM Buoys; SOMO lodní nominace = lagging logistický signal | **unverified** — domain somo.oil.gov.iq je pravděpodobná (subdoména MOO); alternativně somo.gov.iq; nutná validace |
| ca-IQ-mfa | Nízký přímý supply signál | Irácko-íránské vztahy (Iran proxy militie), americko-irácká přítomnost, kurdská autonomie — všechno jsou geopolitické riskovéosy | Nízká přímá logistická role | **proposed** — mofa.gov.iq je standardní doménový vzor |
| ca-IQ-customs_export | GCA zpracovává export celní doklady; data jsou zpoždění a omezená transparentností | GCA administruje vývozní licence crude; v praxi SOMO dokumentaci integruje | Celní clearance pro Basra/Khor al-Amaya tankerové loadingy | **unverified** — customs.gov.iq existuje ale může být neaktuální; alternativní domain neznámá |
| ca-IQ-upstream_regulator | Totožná instituce jako ministry_petroleum; žádná oddělená upstream regulační agentura v Iráku | Viz ca-IQ-ministry_petroleum | Viz ca-IQ-ministry_petroleum | **proposed** — duplikátní doména; zachovat oba záznamy |
| ca-IQ-port_maritime_authority | GAIP spravuje Umm Qasr (general cargo), Khor al-Zubair; přístav Fao (grand port megaproject) | GAIP je pod federální vládou; kurdsko-federální spory neovlivňují Basra terminály přímo | Khor al-Amaya SPM a FAO SPM jsou klíčové pro VLCC loading; údržba nebo porucha = okamžitý supply disruption | **unverified** — iraqiports.gov.iq existuje jako doména; ověřit zda GAIP ji spravuje aktuálně |
| ca-IQ-national_exchange | ISX je akciová burza (Baghdad); žádné komoditní futures | Nízká geopolitická relevance pro crude | Žádná logistická relevance | **unverified** — isx.iq je aktivní domain; zvážit `empty` pro národní burzu; ISX = equity sentiment proxy, ne commodity |
| ca-IQ-central_bank | CBI spravuje ropné příjmy státu; USD auction window = petrodollar recycling | Irácképetrole dollars procházejí skrz CBI; US Treasury má dohled nad CBI USD transakcemi (protiirázký tlak na Írán) | Nízká přímá logistická role | **proposed** — cbi.iq je standardní doménový vzor pro Central Bank of Iraq |
| ca-IQ-environment_regulator | Ministerstvo životního prostředí může nařídit dočasné zastavení pro gas flaring; Basra refinery compliance | Nízká přímá geopolitická role | Gas flaring compliance affect Basra Gas Company (BGC) operations | **proposed** — environment.gov.iq pravděpodobná doména; nižší trader relevance |
| ca-IQ-coast_guard_navy | Irácké námořnictvo chrání Khor al-Amaya SPM a fao VLCC loading area; malá flotila (< 20 lodí) | Íránský vliv na irácké bezpečnostní síly; US naval presence v Zálivu; irácké námořnictvo limitovaná autonomie | Umm Qasr port security; escort pro přístup k SPM buoys | **proposed** — mod.mil.iq je MoD domain; naval sub-entita pravděpodobně na stejné doméně |

---

## Expansion sloty (pro budoucí dávky — nezapisovat nyní)

| entita | domain | poznámka |
|--------|--------|----------|
| INOC – Iraq National Oil Company | inoc.gov.iq | Reactivated 2018; oddělená od SOMO; upstream holding |
| Basra Oil Company (BOC) | basraoil.gov.iq | Jižní produkce; Rumaila, West Qurna-2 |
| North Oil Company (NOC Iraq) | noc.gov.iq | Kirkuk; KRG spor |
| KRG Ministry of Natural Resources | mnr.krg.org | Autonomní export přes Ceyhan (KRG pipeline) |
| Midland Oil Company | midlandoil.gov.iq | Středoirácká produkce |

---

## Unverified / Anti-patterns

### Unverified záznamy

| id | entity | domain navržená | problém |
|----|--------|----------------|---------|
| ca-IQ-noc (SOMO) | SOMO | somo.oil.gov.iq | Ověřit: SOMO může být na somo.gov.iq; subdoména MOO je logická ale nepotvrzena |
| ca-IQ-customs_export | GCA | customs.gov.iq | Doména existuje; ověřit aktivitu a správu GCA |
| ca-IQ-port_maritime_authority | GAIP | iraqiports.gov.iq | Ověřit GAIP jako správce domény |
| ca-IQ-national_exchange | ISX | isx.iq | Equity burza; zvážit `empty` pro komoditní slot |

### Anti-patterns

- Iraqi media (Iraqi News, Shafaq News) — agregátoři; žádná primární role.
- KRG pipeline data přes BOTAS (turecký SO) — sekundární zdroj; BOTAS je expansion pro TR.
- Petro Rabigh / Lukoil Iraq komunikace — IOC tiskové zprávy; sekundární.

---

## Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 4,
  "last_country": "IQ",
  "crosscheck_cursor": 0,
  "last_batch_seq": 5
}
```

Po merge → **další dávka:** `claude-sonnet-4-6_006_country_authority_RU.md`
(Fáze 2, čtvrtá země = RU – Russia, 10 authority types).
