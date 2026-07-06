# Batch 071 — Country Authority: JM (Jamaica)

## Country significance
Jamaica is a **small island energy importer** with no domestic oil or gas production. The country imports ~40 kb/d crude and petroleum products, plus LNG via the **New Fortress Energy (NFE) FSRU** at Old Harbour Bay (2019, ~1.5 mtpa). NFE is the dominant energy actor — it supplies gas to Jamaica Public Service (JPS) power plants and industrial consumers. Jamaica is significant as a **benchmark case** for Caribbean LNG-to-power transitions and US LNG export market development (NFE sources LNG from US Gulf Coast). **Petrojam** (state refinery, Kingston, ~35 kb/d) processes imported crude for domestic consumption and regional product export. Strategically, Jamaica sits astride **Caribbean shipping lanes** and is a key regional hub. JM is a **CARICOM member**; energy poverty and oil import bill dominate fiscal policy.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-JM-ministry_petroleum | JM | — | ministry_petroleum | Ministry of Science, Energy, Telecommunications and Transport | msett.gov.jm | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-JM-noc | JM | — | noc | Petrojam – Jamaica's National Oil Refinery | petrojam.com | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-JM-mfa | JM | — | mfa | Ministry of Foreign Affairs and Foreign Trade | mfaft.gov.jm | international_agency | official | sanctions, policy | proposed |
| ca-JM-customs_export | JM | — | customs_export | Jamaica Customs Agency | jacustoms.gov.jm | international_agency | official | exports, export_license | proposed |
| ca-JM-upstream_regulator | JM | — | upstream_regulator | Petroleum Corporation of Jamaica (PCJ) | pcj.com | international_agency | official | production, force_majeure | proposed |
| ca-JM-port_maritime_authority | JM | — | port_maritime_authority | Port Authority of Jamaica | portjam.com | international_agency | official | vessel_loading, port_closure | proposed |
| ca-JM-national_exchange | JM | — | national_exchange | Jamaica Stock Exchange (JSE) | jamstockex.com | exchange | official | pricing_formula | proposed |
| ca-JM-central_bank | JM | — | central_bank | Bank of Jamaica | boj.org.jm | international_agency | official | pricing_formula | proposed |
| ca-JM-environment_regulator | JM | — | environment_regulator | National Environment and Planning Agency (NEPA) | nepa.gov.jm | international_agency | official | refinery_outage | proposed |
| ca-JM-coast_guard_navy | JM | — | coast_guard_navy | Jamaica Defence Force Coast Guard | jdf.mil.jm | international_agency | official | port_closure, force_majeure | proposed |

## Cross-check (key entries)

### ca-JM-noc (Petrojam)
- **Supply:** Petrojam Kingston refinery ~35 kb/d; imports Venezuelan/US crude; products for Jamaica + Caribbean export; NFE LNG-to-power parallel supply chain; Petrojam = fuel price subsidy mechanism
- **Geopolitics:** Petrojam Venezuela joint venture (PetroJam Ltd 49% PDVSA stake, politically contested); US-JM energy relations; CARICOM PetroCaribe legacy debt
- **Logistics:** Kingston port (Caribbean hub); Freeport terminal; NFE FSRU Old Harbour Bay (LNG regasification → JPS power)

### ca-JM-upstream_regulator (PCJ)
- **Supply:** PCJ manages upstream exploration licenses (no commercial finds yet); oversees energy security diversification; biofuel mandate; solar/LNG transition
- **Geopolitics:** PCJ-NFE relationship = US LNG market entry; CARICOM energy policy coordination; PetroCaribe winding down
- **Logistics:** NFE Old Harbour Bay FSRU = Caribbean LNG import pricing signal; Montego Bay port (northwest Jamaica)

## Expansion slots (10+)
- ca-JM-nfe_jamaica — New Fortress Energy Jamaica (FSRU Old Harbour Bay; US LNG import)
- ca-JM-jps — Jamaica Public Service Company (grid; gas-fired power demand)
- ca-JM-jisco — JISCO Alpart (Jamalco alumina — large energy consumer; bauxite/alumina = industrial demand signal)
- ca-JM-ocs_stats — Office of Customs & Statistics Jamaica (import data)
- ca-JM-petrocaribe — PetroCaribe legacy (Venezuela political risk signal)

## Anti-patterns
- Skip: Jamaica Gleaner energy section (secondary local press)
- Skip: Caribbean 360 energy coverage (regional aggregator)
