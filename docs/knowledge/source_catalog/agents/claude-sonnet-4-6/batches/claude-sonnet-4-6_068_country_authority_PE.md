# Batch 068 — Country Authority: PE (Peru)

## Country significance
Peru is the **second-largest Latin American LNG exporter** after Trinidad, operating **Peru LNG** (Pampa Melchorita terminal, 4.45 mtpa) — the only LNG export facility in South America after Trinidad. The **Camisea gas project** (blocks 88 + 56, TGP pipeline, PLNG) supplies domestic gas (Lima, fertilizers) and LNG export. Upstream operated by **Pluspetrol** (Argentina) with Shell, Repsol, Hunt Oil, Sonatrach, and Tecpetrol as block partners. Peru also has legacy **crude production in the Amazon basin** (Block 192 = Loreto, politically contested with indigenous communities) and a mature offshore sector (Talara). **Petroperú** (state refiner) is financially troubled (2022 near-bankruptcy, USD 4bn debt restructuring). Peru is an IEA associate; LNG exports go primarily to **Spain, Mexico, South Korea, Japan**. Political instability (5 presidents 2016–2022, Boluarte government 2022+) = licensing risk signal.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-PE-ministry_petroleum | PE | — | ministry_petroleum | Ministry of Energy and Mines (MINEM) | minem.gob.pe | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-PE-noc | PE | — | noc | Petroperú – Petróleos del Perú | petroperu.com.pe | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-PE-mfa | PE | — | mfa | Ministry of Foreign Affairs (Cancillería) | rree.gob.pe | international_agency | official | sanctions, policy | proposed |
| ca-PE-customs_export | PE | — | customs_export | SUNAT – Aduanas | sunat.gob.pe | international_agency | official | exports, export_license | proposed |
| ca-PE-upstream_regulator | PE | — | upstream_regulator | OSINERGMIN – Energy & Mines Regulatory Agency | osinergmin.gob.pe | international_agency | official | production, force_majeure | proposed |
| ca-PE-port_maritime_authority | PE | — | port_maritime_authority | Autoridad Portuaria Nacional (APN) | apn.gob.pe | international_agency | official | vessel_loading, port_closure | proposed |
| ca-PE-national_exchange | PE | — | national_exchange | Bolsa de Valores de Lima (BVL) | bvl.com.pe | exchange | official | pricing_formula | proposed |
| ca-PE-central_bank | PE | — | central_bank | Banco Central de Reserva del Perú (BCRP) | bcrp.gob.pe | international_agency | official | pricing_formula | proposed |
| ca-PE-environment_regulator | PE | — | environment_regulator | OEFA – Environmental Assessment and Enforcement Agency | oefa.gob.pe | international_agency | official | pipeline_outage, force_majeure | proposed |
| ca-PE-coast_guard_navy | PE | — | coast_guard_navy | Marina de Guerra del Perú | marina.mil.pe | international_agency | official | port_closure, force_majeure | proposed |

## Cross-check (key entries)

### ca-PE-noc (Petroperú)
- **Supply:** Petroperú Talara refinery (95 kb/d, modernized 2022); Block 192 crude import (Amazon Loreto basin); Camisea downstream affiliate (not Petroperú direct); 2022 debt crisis = refinery throughput signal
- **Geopolitics:** Petroperú solvency = political risk; Boluarte government credit guarantee; indigenous Block 192 protests (Loreto = force majeure signal); Pluspetrol Camisea upstream independent
- **Logistics:** Talara port terminal (Pacific VLCC crude import); Paita port; Callao oil terminal; TGP pipeline (Camisea → Lima/coast)

### ca-PE-upstream_regulator (OSINERGMIN)
- **Supply:** Block 88 (Pluspetrol) + Block 56 (Repsol/Hunt) = Camisea production approvals; PERUPETRO upstream contract registry; LNG export allocation oversight
- **Geopolitics:** Amazon indigenous consultation FPIC requirement = drilling delay signal; MINEM-OSINERGMIN split jurisdiction on Block 192
- **Logistics:** TGP (Transportadora de Gas del Perú) pipeline to coast; Peru LNG Pampa Melchorita jetty; LNG carrier scheduling to Spain/Mexico/Korea

## Expansion slots (10+)
- ca-PE-peru_lng — Peru LNG terminal (Pampa Melchorita; cargo schedules)
- ca-PE-pluspetrol — Pluspetrol Norte (Camisea Block 88 op.)
- ca-PE-tgp — Transportadora de Gas del Perú (pipeline)
- ca-PE-perupetro — Perupetro SA (upstream license registry)
- ca-PE-osinergmin_stats — OSINERGMIN gas + electricity statistics

## Anti-patterns
- Skip: Peru21 energy coverage (tabloid secondary)
- Skip: Gestión.pe energy section (financial news aggregator)
