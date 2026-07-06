# Batch 070 — Country Authority: TT (Trinidad and Tobago)

## Country significance
Trinidad and Tobago is the **Western Hemisphere's largest LNG exporter** (Atlantic LNG, ~15 mtpa capacity across 4 trains at Point Fortin) and the **largest natural gas producer in the Caribbean basin** (~3.2 bcfd peak, now ~2.6 bcfd declining). The economy is almost entirely driven by hydrocarbons (40%+ GDP). Key players: **NGC (National Gas Company)** aggregates all gas from upstream producers (bpTT ~50%, Shell, EOG Resources, BHP); **Heritage Petroleum** (state NOC for upstream); **Atlantic LNG** (bpTT op., Shell, NGC, Repsol consortium). TT is also a major **methanol and ammonia exporter** (Point Lisas petrochemical hub = downstream gas monetization). Bptt is the single most important upstream actor — any bpTT operational update (e.g. Mango/Cashima deepwater, Juniper, Cassia C) is a tier-1 signal. Gas decline from legacy shallow-water fields is a structural challenge; deepwater Calypso block holds promise.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-TT-ministry_petroleum | TT | — | ministry_petroleum | Ministry of Energy and Energy Industries | energy.gov.tt | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-TT-noc | TT | — | noc | Heritage Petroleum Company | heritagepetroleum.co.tt | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-TT-mfa | TT | — | mfa | Ministry of Foreign and CARICOM Affairs | foreign.gov.tt | international_agency | official | sanctions, policy | proposed |
| ca-TT-customs_export | TT | — | customs_export | Customs and Excise Division | customs.gov.tt | international_agency | official | exports, export_license | proposed |
| ca-TT-upstream_regulator | TT | — | upstream_regulator | Petroleum Company of Trinidad and Tobago (Petrotrin successor / MoE) | energy.gov.tt | international_agency | official | production, force_majeure | proposed |
| ca-TT-port_maritime_authority | TT | — | port_maritime_authority | Port Authority of Trinidad and Tobago | patnt.com | international_agency | official | vessel_loading, port_closure | proposed |
| ca-TT-national_exchange | TT | — | national_exchange | Trinidad and Tobago Stock Exchange (TTSE) | stockex.co.tt | exchange | official | pricing_formula | proposed |
| ca-TT-central_bank | TT | — | central_bank | Central Bank of Trinidad and Tobago | central-bank.org.tt | international_agency | official | pricing_formula | proposed |
| ca-TT-environment_regulator | TT | — | environment_regulator | Environmental Management Authority (EMA) | ema.co.tt | international_agency | official | refinery_outage | proposed |
| ca-TT-coast_guard_navy | TT | — | coast_guard_navy | Trinidad and Tobago Coast Guard | ttcg.mil.tt | international_agency | official | port_closure, force_majeure | proposed |

## Cross-check (key entries)

### ca-TT-noc (Heritage Petroleum)
- **Supply:** Heritage holds legacy onshore + shallow offshore TT fields (Trinmar); ~50 kb/d crude + condensate; main gas from bpTT (Juniper, Cassia C, Mango); Heritage → NGC → Atlantic LNG supply chain
- **Geopolitics:** bpTT dominant = UK-TT bilateral energy anchor; US EOG/BHP shallow water; Venezuela gas import discussion (Columbus Basin border); CARICOM energy diplomacy
- **Logistics:** Point Fortin (Atlantic LNG 4 trains); Point Lisas petrochemical hub (methanol/ammonia); Brighton crude terminal; Caribbean export hub

### ca-TT-upstream_regulator (MoE)
- **Supply:** MoE issues PSAs + PPAs; bpTT Juniper + Cassia C FID oversight; Calypso deepwater license (Shell/bpTT); gas decline management = structural supply signal
- **Geopolitics:** TT-Venezuela maritime boundary (Columbus Channel gas); LNG HH-linked pricing vs spot JKM; US LNG competitor awareness
- **Logistics:** Atlantic LNG cargo scheduling = HH price parity signal; ammonia + methanol = non-energy gas demand indicator

## Expansion slots (10+)
- ca-TT-bptt — bpTT (bp Trinidad and Tobago; ~50% upstream gas)
- ca-TT-ngc — NGC (National Gas Company; gas aggregator)
- ca-TT-atlantic_lng — Atlantic LNG Company (Point Fortin terminal)
- ca-TT-eog_resources — EOG Resources TT (Columbus Basin shallow water)
- ca-TT-point_lisas — Point Lisas Industrial Estate (methanol/ammonia)

## Anti-patterns
- Skip: Trinidad Guardian energy coverage (secondary local press)
- Skip: Loop TT news (aggregator)
