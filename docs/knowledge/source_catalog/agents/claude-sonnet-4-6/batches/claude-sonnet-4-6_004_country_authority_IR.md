# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_004_country_authority_IR.md  
**Fáze:** country_authority — krok IR (Iran)  
**Datum:** 2026-07-04  

---

## Shrnutí

Fáze 2, dávka 2 — Iran × 10 authority types. Írán je klíčový pro tři tržní osy současně:
**sankce** (OFAC/EU SDN → 1–1.5 mb/d swing), **Hormuz** (IRGCN → okamžitý $5–10 risk premium
na Brent), **JCPOA/jaderný deal** (každé kolo vyjednávání pohybuje trhem o $3–5). Majority
íránských vládních webů je dostupná i ze Západu, ale spolehlivost a aktuálnost je nižší než
u OECD zdrojů — všechny navržené domény jsou z veřejně dostupného záznamu; flagujeme
ty s nejistotou. Celkem **10 slotů**; 7 proposed, 3 unverified.

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IR-ministry_petroleum | IR | — | ministry_petroleum | Iranian Ministry of Petroleum | mop.ir | international_agency | official | policy, export_license, quota_rhetoric, production | proposed |
| ca-IR-noc | IR | — | noc | NIOC – National Iranian Oil Company | nioc.ir | international_agency | official | production, exports, force_majeure, term_contract, pricing_formula | proposed |
| ca-IR-mfa | IR | — | mfa | Iranian Ministry of Foreign Affairs | mfa.gov.ir | international_agency | official | sanctions, policy | proposed |
| ca-IR-customs_export | IR | — | customs_export | IRICA – Islamic Republic of Iran Customs Administration | irica.gov.ir | international_agency | official | exports, export_license | proposed |
| ca-IR-upstream_regulator | IR | — | upstream_regulator | Ministry of Petroleum (upstream licensing & NIOC oversight) | mop.ir | international_agency | official | production, refinery_outage | proposed |
| ca-IR-port_maritime_authority | IR | — | port_maritime_authority | PMO – Ports and Maritime Organization of Iran | pmo.ir | international_agency | official | vessel_loading, port_closure | proposed |
| ca-IR-national_exchange | IR | — | national_exchange | IRENEX – Iran Energy Exchange | irenex.ir | exchange | official | pricing_formula, term_contract | unverified |
| ca-IR-central_bank | IR | — | central_bank | CBI – Central Bank of Iran | cbi.ir | international_agency | official | sanctions | proposed |
| ca-IR-environment_regulator | IR | — | environment_regulator | DOE – Department of Environment of Iran | doe.ir | international_agency | official | refinery_outage | proposed |
| ca-IR-coast_guard_navy | IR | — | coast_guard_navy | IRGC Navy (Sepah-e Pasdaran Naval Forces) | sepah.ir | international_agency | official | port_closure, force_majeure | unverified |

---

## Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IR-ministry_petroleum | MoP nastavuje NIOC produkční cíl; tiskové konference ministra Mohsena Pak (od 2023) jsou primárním signálem pro output guidance; každá změna exportního kvótního rámce se hlásí přes mop.ir | Ministerstvo implementuje ropný zákon; jaderný deal (JCPOA) = podmínka plného výstupu; každé diplomatické sdělení MoP linkováno na sankční status | MoP koordinuje s PMO přidělování terminálů; Kharg Island export přes NIOC/MoP protokol | **proposed** — mop.ir je ověřitelný íránský vládní domain (suffix .ir) |
| ca-IR-noc | NIOC = 3–3.5 mb/d pod sankcemi (2024); kapacita ~4 mb/d bez sankcí; NIOC reports jsou hlavním supply-side signálem pro íránský output | NIOC prodává crude přes "ghost fleet" bez označení; OFAC SDN listingy NIOC subsidiaries jsou přímý geopolitický trigger | Kharg Island (90 % íránského exportu) operovaný NIOC; Bandar Abbas sekundárně; loadingy přes frontové společnosti | **proposed** — nioc.ir aktivní; primárně perzský jazyk; monitorovat anglické press release sekce |
| ca-IR-mfa | Nízký přímý supply signál; ale MFA tiskové konference = JCPOA status proxy | Viceministr/mluvčí sdělení o sankcích, nukleárním programu a Hormuz jsou tier-1 geopolitický signal; přímo citovány v Brent futures pohybech | MFA nevydává přímo nautické nebo port closure oběžníky | **proposed** — mfa.gov.ir je standardní íránský vládní domain |
| ca-IR-customs_export | IRICA publikuje obchodní statistiky (zpoždění 2–3 měsíce); data o ropném exportu jsou sanitizovaná kvůli sankcím | IRICA administruje export licenses; sankční compliance monitoring; záznamy o destinacích exportu (Čína, Sýrie, Venezuela) | Celní doklady k crude tankerům procházejí IRICA; fakturační trasy přes třetí strany | **proposed** — irica.gov.ir je znám jako oficální doména |
| ca-IR-upstream_regulator | Totožná instituce jako ministry_petroleum — v Íránu není oddělenou upstream regulátor agentura; NIOC je operátor i de-facto regulator pod ministerstvem | Viz ca-IR-ministry_petroleum | Viz ca-IR-ministry_petroleum | **proposed** — duplikátní doména mop.ir; zachovat oba záznamy s odlišným authority_type; stejná logika jako SA |
| ca-IR-port_maritime_authority | PMO spravuje Bandar Abbas, Bandar Imam Khomeini a Bandar Asaluyeh (plynovody z Jižního Parsu); port statistics jsou dostupné na pmo.ir | PMO vydává port closure notifikace; při vojenském cvičení IRGCN v Perském zálivu PMO koordinuje s námořnictvem omezení | Kharg Island je technicky NIOC terminal, ale PMO koordinuje maritime regulaci; PMO přiděluje pobřežní přístavy | **proposed** — pmo.ir je aktivní a ověřitelný |
| ca-IR-national_exchange | IRENEX (Iran Energy Exchange) byl zřízen v 2012 pro obchodování s ropnými produkty a petrochemikáliemi na domácím trhu; pod sankcemi funguje omezeně | IRENEX slouží k denominaci transakcí v IRR; pod tlakem sankcí přešel na prodej crude v alternativních měnách (CNY); důkaz obchodování přes IRENEX = sankční červená vlajka | Nízká logistická role pro mezinárodní pozice | **unverified** — irenex.ir existuje jako doména; ověřit zda IRENEX stále aktivně obchoduje; trader relevance nízká pro přímé monitoring z Oeste |
| ca-IR-central_bank | CBI spravuje petrodolarové rezervy; pod OFAC sankcemi od 2019; US Treasury SDN listing na CBI 2019 = totální izolace | CBI je primárním cílem sankčního tlaku; každý nový OFAC opatřením vůči CBI je extrémní geopolitický trigger | CBI financuje NIOC crude prodeje; payment routing přes třetí strany (Irák, Čína) | **proposed** — cbi.ir aktivní; monitoring pro případné komuniké o sanctions waivers |
| ca-IR-environment_regulator | DOE Írán dohlíží na rafinerie a petrochemický komplex; výpadky z důvodu environmentálního narušení jsou vzácné ale možné | DOE je pod kontrolou vlády; neovlivňuje geopolitiku přímo | Rafinérská kapacita Írán ~2.3 mb/d (Abadan, Isfahan, Arak, Bandar Abbas) | **proposed** — doe.ir je standardní suffix; ověřit zda Department of Environment používá doe.ir |
| ca-IR-coast_guard_navy | IRGCN (Islamic Revolutionary Guard Corps Navy) = primární aktér v Hormuz; zodpovědný za všechna vessel seizures (Stena Impero 2019, Heritage 2023 atd.) | IRGCN je nejvýznamnější geopolitický operátor v katalogu pro force_majeure: každé cvičení, provokace nebo seizure = okamžitý $3–8 Brent spike | IRGCN patroluje severní pobřeží Hormuz; může uzavřít průliv; fast boat fleet přes Bandar Abbas | **unverified** — sepah.ir je IRGC hlavní doména; ale IRGCN nemusí mít oddělenou veřejnou sub-stránku; zvážit alterantivu: monitoring přes média a UKMTO spíše než přímý official feed |

---

## Unverified / Anti-patterns

### Unverified záznamy

| id | entity | domain navržená | problém |
|----|--------|----------------|---------|
| ca-IR-national_exchange | IRENEX | irenex.ir | Ověřit aktivitu; pod sankcemi nízká mezinárodní relevance; zvážit `empty` nebo downgrade priority |
| ca-IR-coast_guard_navy | IRGC Navy | sepah.ir | sepah.ir je IRGC obecná doména; IRGCN sub-sekce může být na irgcnavy.ir nebo jiné; IRGCN je SDN-listovaná entity (OFAC) — monitoring doporučen přes třetí strany (UKMTO, Intertanko) |
| ca-IR-environment_regulator | DOE Iran | doe.ir | doe.ir může být generická doména; ověřit že patří Department of Environment, ne jiné entitě |

### Íránská specifika pro monitoring

- **Primární real-time signál pro Írán** není íránský vládní web — je to kombinace:
  (1) IAEA safeguards reports (iaea.org), (2) UKMTO incident reports (ukmto.org),
  (3) OFAC SDN updates (ofac.treas.gov), (4) Iranian MFA press briefings (mfa.gov.ir).
- **Ghost fleet monitoring**: íránské tankery vypínají AIS; tracking přes Equasis a Lloyd's.
- **NIOC sub-entities**: NICO (National Iranian Tanker Company — nioc.ir/nico nebo nictc.ir),
  NIOC International Affairs = expansion sloty pro příští dávky.

### Anti-patterns

- PressTV (presstv.ir) — státní propaganda; žádný primární trading signal.
- Shana News Agency (shana.ir) — semi-official; agregátor pro MoP; zachovat jako Tier 2 monitoring only.
- Fars News — propaganda; skip.
- Naftiran Intertrade (NICO) — sanctioned intermediary; žádná webová presence ověřitelná.

---

## Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 3,
  "last_country": "IR",
  "crosscheck_cursor": 0,
  "last_batch_seq": 4
}
```

Po merge → **další dávka:** `claude-sonnet-4-6_005_country_authority_IQ.md`
(Fáze 2, třetí země = IQ – Iraq, 10 authority types).
