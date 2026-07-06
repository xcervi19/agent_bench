# Batch 066 — Country Authority: BD (Bangladesh)

## Country significance
Bangladesh is a **gas-dependent developing economy** facing an acute natural gas depletion crisis. Domestic output (~2.7 bcm/y, peak ~30 bcm in 2010) from Titas, Habiganj, Sylhet fields is sharply declining. To compensate, BD operates **two FSRUs** (Summit LNG + Excelerate Moheshkhali) with combined ~7.5 mtpa regasification capacity and is building onshore LNG terminal at Kutubdia. The state energy conglomerate **Petrobangla** coordinates upstream (BAPEX) and downstream (TITAS Gas, Karnaphuli Gas). **Power shortages** (load-shedding) are endemic whenever LNG cargo procurement falters, making BD a price-sensitive spot LNG importer. IOCs Chevron (Bibiyana field = ~50% domestic gas) and Shell historically dominated upstream. The Bay of Bengal deepwater frontier (BB-08, BB-09) remains underexplored due to maritime boundary disputes with Myanmar and India (settled ICJ 2012/2014 but investment slow).

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-BD-ministry_petroleum | BD | — | ministry_petroleum | Ministry of Power, Energy and Mineral Resources | mpemr.gov.bd | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-BD-noc | BD | — | noc | Petrobangla – Bangladesh Oil, Gas and Mineral Corporation | petrobangla.gov.bd | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-BD-mfa | BD | — | mfa | Ministry of Foreign Affairs | mofa.gov.bd | international_agency | official | sanctions, policy | proposed |
| ca-BD-customs_export | BD | — | customs_export | Bangladesh Customs (NBR) | nbr.gov.bd | international_agency | official | exports, export_license | proposed |
| ca-BD-upstream_regulator | BD | — | upstream_regulator | BAPEX – Bangladesh Oil, Gas and Mineral Corp (upstream) | bapex.com.bd | international_agency | official | production, force_majeure | proposed |
| ca-BD-port_maritime_authority | BD | — | port_maritime_authority | Chittagong Port Authority | cpa.gov.bd | international_agency | official | vessel_loading, port_closure | proposed |
| ca-BD-national_exchange | BD | — | national_exchange | Dhaka Stock Exchange (DSE) | dsebd.org | exchange | official | pricing_formula | proposed |
| ca-BD-central_bank | BD | — | central_bank | Bangladesh Bank | bb.org.bd | international_agency | official | pricing_formula | proposed |
| ca-BD-environment_regulator | BD | — | environment_regulator | Department of Environment (DoE) | doe.gov.bd | international_agency | official | refinery_outage | proposed |
| ca-BD-coast_guard_navy | BD | — | coast_guard_navy | Bangladesh Coast Guard + Bangladesh Navy | coastguard.gov.bd | international_agency | official | port_closure, force_majeure | proposed |

## Cross-check (key entries)

### ca-BD-noc (Petrobangla)
- **Supply:** Petrobangla coordinates all gas field output; Titas (Jalalabad), Habiganj, Sylhet, Bibiyana (Chevron 100%); FSRU LNG procurements = spot market signal; load-shedding alerts = demand spike indicator
- **Geopolitics:** US Chevron Bibiyana dominance (protest sensitivity); India-Bangladesh power interconnect; Bay of Bengal maritime boundary = exploration unlock; LNG import price sensitivity = political stability risk
- **Logistics:** Moheshkhali FSRU (Excelerate + Summit); LNG truck/CNG distribution inland; Chittagong port LNG jetty; Payra port (deep sea under development)

### ca-BD-port_maritime_authority (Chittagong CPA)
- **Supply:** Chittagong = >90% Bangladesh seaborne trade; LNG import FSRU mooring at Moheshkhali; Payra port LNG expansion
- **Geopolitics:** Bay of Bengal chokepoint; Cyclone risk = FSRU anchor drag + cargo disruption (seasonal May/Oct)
- **Logistics:** CPA vessel scheduling; FSRU berth availability; cyclone evacuation notices

## Expansion slots (10+)
- ca-BD-summit_lng — Summit Group (FSRU operator + power)
- ca-BD-titas_gas — TITAS Gas Transmission (distribution)
- ca-BD-bpdb — Bangladesh Power Development Board (power-gas demand signal)
- ca-BD-chevron_bibiyana — Chevron Bangladesh (Bibiyana field; ~1.2 bcfd)
- ca-BD-imo_cyclone — IMO/BIMCO Bay of Bengal cyclone alerts

## Anti-patterns
- Skip: The Daily Star (BD) energy commentary (secondary)
- Skip: bdnews24.com energy section (aggregator)
