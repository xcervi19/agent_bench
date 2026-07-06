# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_007_country_authority_US.md  
**Fáze:** country_authority — krok US (United States)  
**Datum:** 2026-07-05  

---

## Shrnutí

Fáze 2, dávka 5 — United States × 10 authority types. USA jsou největší producent ropy
(~13 mb/d) a LNG exportér #1. Klíčové specifika: **žádný státní NOC** (slot = empty;
SPR jako sovereign supply nástroj); mnoho US autorit je již v globální vrstvě (DOE, FERC,
MARAD, USCG, CFTC) — country sloty zachycují odlišnou analytickou dimenzi (country ×
authority vs globální entita). US MFA (State Dept) = primární sankční aktér pro ruský price
cap, íránské sankce i venezuelský waiver. BOEM = GoM shut-in autorita při hurikánech.
Celkem **10 slotů**; 9 proposed, 1 empty (noc).

---

## Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-US-ministry_petroleum | US | — | ministry_petroleum | US DOE – Department of Energy | energy.gov | international_agency | official | policy, storage_levels, production, exports | proposed |
| ca-US-noc | US | — | noc | — (no US state NOC; SPR managed by DOE) | — | — | — | — | empty |
| ca-US-mfa | US | — | mfa | US Department of State | state.gov | international_agency | official | sanctions, policy | proposed |
| ca-US-customs_export | US | — | customs_export | CBP – US Customs and Border Protection | cbp.dhs.gov | international_agency | official | exports, export_license | proposed |
| ca-US-upstream_regulator | US | — | upstream_regulator | BOEM – Bureau of Ocean Energy Management | boem.gov | international_agency | official | production, force_majeure | proposed |
| ca-US-port_maritime_authority | US | — | port_maritime_authority | USACE – US Army Corps of Engineers | usace.army.mil | international_agency | official | port_closure, vessel_loading | proposed |
| ca-US-national_exchange | US | — | national_exchange | CME Group / NYMEX | cmegroup.com | exchange | official | pricing_formula, term_contract | proposed |
| ca-US-central_bank | US | — | central_bank | Federal Reserve | federalreserve.gov | international_agency | official | pricing_formula, sanctions | proposed |
| ca-US-environment_regulator | US | — | environment_regulator | EPA – Environmental Protection Agency | epa.gov | international_agency | official | refinery_outage | proposed |
| ca-US-coast_guard_navy | US | — | coast_guard_navy | USCG – US Coast Guard | uscg.mil | international_agency | official | port_closure, vessel_loading, force_majeure | proposed |

---

## Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-US-ministry_petroleum | DOE vydává SPR release order (okamžitý $3–8 WTI pokles); LNG export terminal permit rozhodnutí (Sabine Pass, Freeport, Venture Global) jsou tier-1 supply signál | DOE koordinuje IEA emergency reserve koordinaci; SPR release = geopolitický signal síly v krizi (2022, Gaza) | DOE spravuje SPR lokace (Bryan Mound, West Hackberry, Big Hill, Bayou Choctaw); pipeline přístupy | **proposed** — energy.gov aktivní; duplicitní doména s gl-international_agency-017; odlišný analytický rámec (country ministry vs globální agentura) |
| ca-US-noc | USA nemá státní NOC; soukromý sektor (ExxonMobil, Chevron, ConocoPhillips) dominuje; SPR (~351 mb k 2024) je jedinou formou sovereign production control | SPR je politický nástroj; každý presidential directive k release je geopolitický signál | SPR čerpání přes pipelines do Gulf Coast rafinérií | **empty** — žádná entita; expansiní sloty: ExxonMobil, Chevron, ConocoPhillips (private); DOE SPR sub-feed |
| ca-US-mfa | State Dept vydává Iran sanctions waivers (180-day); Venezuela general licence; Russian oil price cap guidance — každá změna = přímý supply swing 0.5–1.5 mb/d | State Dept = primární geopolitický aktér pro energetické sankce; CAATSA, IFCA, EO 13662 administration | Nízká přímá logistická role; diplomatická nota ovlivňuje vessel insurance dostupnost | **proposed** — state.gov aktivní; duplicitní doména s gl-international_agency-025 (G7 price cap); country slot zachycuje plnou sankční šíři |
| ca-US-customs_export | CBP/Census Bureau publikuje měsíční US crude export data (2-month lag); věrohodné a úplné | CBP enforces export licence restrictions (Iran arms embargo, Cuba, etc.) | Dokumentace pro Houston Ship Channel, Sabine Pass, Corpus Christi crude exports | **proposed** — cbp.dhs.gov aktivní |
| ca-US-upstream_regulator | BOEM vydává GoM production shut-in orders při hurikánech (Cat 3+ = 5–7 mb/d kapacita v GoM offshore); BOEM lease sales určují dlouhodobý supply trend | BOEM lease moratorium = politické rozhodnutí; Biden 2021 pause = strukturální supply signal | GoM VLCC loading points (LOOP, Green Canyon, Walker Ridge) pod BOEM jurisdikcí | **proposed** — boem.gov aktivní; tier-1 pro hurricane season (červen–listopad) |
| ca-US-port_maritime_authority | USACE udržuje prohloubenou navigaci Houston Ship Channel (46 ft) a Mississippi River; dredging nebo uzávěra = okamžitá export constraint | USACE vydává emergency permits; přírodní katastrofa (hurikán, záplavy) aktivuje USACE port closure orders | Houston Ship Channel vedení přes USACE COE Galveston; Corpus Christi a Sabine Pass pod příslušnými USACE distrikty | **proposed** — usace.army.mil aktivní |
| ca-US-national_exchange | CME/NYMEX = globální WTI a Henry Hub benchmark; US country slot zdůrazňuje specificky americký kontext (Cushing physical delivery, EIA inventory vs futures reaction) | CFTC reguluje CME; position limit changes jsou geopolitický signal pro spekulativní positioning | WTI delivery point: Cushing, OK; CME clearinghouse = systémová infrastruktura | **proposed** — cmegroup.com duplicitní s gl-exchange-001; country context odlišný |
| ca-US-central_bank | Federal Reserve rate decisions pohybují USD; silný USD = slabší crude ceny (inverse correlation ~0.6); Fed policy je makro overlay pro každou crude pozici | Fed je globální geopolitický aktér; US Fed policy ovlivňuje EM currency a tím crude demand | Nízká přímá logistická role | **proposed** — federalreserve.gov aktivní |
| ca-US-environment_regulator | EPA fuel spec harmonogram (RVP waivers v léto, CBOB/RVP switchover) pohybuje crack spread; EPA biofuel waiver (RFS) pohybuje RIN cenou → refinery margin | EPA reguluje Tier 3 gasoline sulfur; climate regs ovlivňují refinery CAPEX | Rafinerie compliance → planned/unplanned downtime | **proposed** — epa.gov aktivní |
| ca-US-coast_guard_navy | USCG uzavírá přístavy při hurikánu (Houston, Corpus Christi, New Orleans): 24–72h alert → price spike; USCG vessel inspection = vetting pre-podmínka | USCG Port State Control = de-facto sanctions enforcement (iran-linked vessels) | USCG NAIS (Nationwide AIS) = přímý tracking přes Sabine Pass, LOOP, Houston | **proposed** — uscg.mil aktivní; duplicitní s gl-shipping-019; country context: US Gulf specifika |

---

## Expansion sloty (pro budoucí dávky)

| entita | domain | poznámka |
|--------|--------|----------|
| ExxonMobil | exxonmobil.com | Largest US private crude producer; Permian dominant |
| Chevron | chevron.com | GoM + Permian; LNG export via stake |
| ConocoPhillips | conocophillips.com | Permian/Eagle Ford; Alaska production |
| DOE SPR data feed | energy.gov/fe/petroleum-reserves | SPR stock level sub-feed; tier-1 |
| BSEE (offshore safety) | bsee.gov | GoM incident reporting; shut-in orders |
| Census Bureau trade data | census.gov/foreign-trade | Monthly crude/product export volumes |
| US BLM (federal onshore) | blm.gov | Federal land lease sales; onshore upstream |

---

## Unverified / Anti-patterns

Žádné unverified záznamy v této dávce — všechny US vládní domény jsou ověřitelné standardními .gov vzory.

### Anti-patterns

- EIA (eia.gov) — již v globální vrstvě; není country-level authority, je statistická agentura.
- FERC (ferc.gov) — již v globální vrstvě; US country expansion slot by byl FERCInterstate Gas pipeline data.
- AAA gasoline prices, GasBuddy — retail agregátoři; žádná primární role.

---

## Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 6,
  "last_country": "US",
  "crosscheck_cursor": 0,
  "last_batch_seq": 7
}
```

Po merge → **další dávka:** `claude-sonnet-4-6_008_country_authority_AE.md`
(Fáze 2, šestá země = AE – United Arab Emirates, 10 authority types).
