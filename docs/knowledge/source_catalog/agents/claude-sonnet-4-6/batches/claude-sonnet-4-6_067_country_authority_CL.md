# Batch 067 — Country Authority: CL (Chile)

## Country significance
Chile is South America's **second-largest LNG importer** and a major **copper/lithium** driven energy consumer. Domestic gas production is minimal; Chile imports virtually all its natural gas as LNG via **GNL Quintero** (~3 mtpa) and **GNL Mejillones** (~2.5 mtpa) terminals. Chile is heavily interconnected with Argentina via Transandean pipelines, but Argentine gas exports collapsed post-2004, forcing the LNG pivot. **ENAP** (state refiner) runs Biobío and Aconcagua refineries. Chile is a power-intensive mining economy — the Atacama lithium/copper industry requires firm power (gas peakers + solar). Chile's unique geography creates grid segmentation: SIC (central, Santiago+mining) and SING (northern, Atacama). Chile has no OPEC affiliation but is an **IEA member** (emergency oil reserve holder). Political dynamics (Boric government, lithium nationalization 2023) affect energy policy.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-CL-ministry_petroleum | CL | — | ministry_petroleum | Ministry of Energy (MINEN) | energia.gob.cl | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-CL-noc | CL | — | noc | ENAP – Empresa Nacional del Petróleo | enap.cl | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-CL-mfa | CL | — | mfa | Ministry of Foreign Affairs | minrel.gob.cl | international_agency | official | sanctions, policy | proposed |
| ca-CL-customs_export | CL | — | customs_export | Servicio Nacional de Aduanas | aduana.cl | international_agency | official | exports, export_license | proposed |
| ca-CL-upstream_regulator | CL | — | upstream_regulator | Comisión Nacional de Energía (CNE) | cne.cl | international_agency | official | production, force_majeure | proposed |
| ca-CL-port_maritime_authority | CL | — | port_maritime_authority | Directemar – Chilean Maritime Authority | directemar.cl | international_agency | official | vessel_loading, port_closure | proposed |
| ca-CL-national_exchange | CL | — | national_exchange | Bolsa de Comercio de Santiago | bolsadesantiago.com | exchange | official | pricing_formula | proposed |
| ca-CL-central_bank | CL | — | central_bank | Banco Central de Chile | bcentral.cl | international_agency | official | pricing_formula | proposed |
| ca-CL-environment_regulator | CL | — | environment_regulator | Superintendencia del Medio Ambiente (SMA) | sma.gob.cl | international_agency | official | refinery_outage | proposed |
| ca-CL-coast_guard_navy | CL | — | coast_guard_navy | Armada de Chile (Navy) | armada.cl | international_agency | official | port_closure, force_majeure | proposed |

## Cross-check (key entries)

### ca-CL-noc (ENAP)
- **Supply:** ENAP operates Biobío (116 kb/d) + Aconcagua (104 kb/d) refineries; imports ~100% crude (mostly Ecuador/Peru/USA/Algeria); manages GNL Quintero (20% ENAP + BG Shell + Endesa + METROGAS JV); Magallanes region domestic gas (minimal)
- **Geopolitics:** Boric lithium nationalization → SQM/Albemarle renegotiation = copper/lithium supply signal; Argentina gas import dependency vs Argentine political crisis; LNG import diversification from Qatar, USA
- **Logistics:** GNL Quintero (V región, near Valparaíso); GNL Mejillones (Antofagasta norte); Atacama pipeline from Argentina; Transandean pipelines (variable flow)

### ca-CL-upstream_regulator (CNE)
- **Supply:** CNE issues LNG import licenses; electricity price regulation (gas parity); strategic fuel reserve directives; biofuel mandate
- **Geopolitics:** CNE coordinates IEA strategic reserve; Atacama copper industry power contracts; grid decarbonization 2050 timeline
- **Logistics:** SING-SIC interconnection; transmission tariff regulation; spot LNG procurement tender oversight

## Expansion slots (10+)
- ca-CL-gnl_quintero — GNL Quintero terminal (LNG regasification; cargo arrivals)
- ca-CL-gnl_mejillones — GNL Mejillones (SUEZ/TotalEnergies JV)
- ca-CL-cochilco — Chilean Copper Commission (copper = energy demand proxy)
- ca-CL-ine_energy — INE Chile (industrial energy consumption statistics)
- ca-CL-coordinador_electrico — Coordinador Eléctrico Nacional (grid operator; gas dispatch)

## Anti-patterns
- Skip: El Mercurio energy coverage (editorial/secondary)
- Skip: Emol.com energy section (news aggregator)
