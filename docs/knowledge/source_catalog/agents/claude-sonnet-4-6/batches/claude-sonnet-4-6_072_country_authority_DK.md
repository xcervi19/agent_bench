# Batch 072 — Country Authority: DK (Denmark)

## Country significance
Denmark is a **North Sea mature producer** in structural decline — from ~400 kb/d oil peak (2004) to ~70 kb/d (2024+) — but retains strategic importance as operator of **Tyra gas field** (redeveloped 2024, ~90% of Danish gas production) and the **Danish Underground Consortium (DUC)** block (Total, Noreco, Mærsk Oil legacy → now TotalEnergies). Denmark controls the **Danish Straits (Øresund, Great Belt, Little Belt)** — critical chokepoints for Baltic Sea trade and Russian crude/products exports. **Energinet** is the Danish gas TSO connecting to European grid (Baltic Pipe from Norway via Denmark launched Oct 2022 = major European supply route). Denmark also controls **Greenland** (Arctic frontier exploration, REE/critical minerals) and the **Faroe Islands** (Equinor Brugdan gas, UK frontier). Denmark is an **IEA member** and active NATO/EU member — energy security policy is highly integrated.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-DK-ministry_petroleum | DK | — | ministry_petroleum | Ministry of Climate, Energy and Utilities | kefm.dk | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-DK-noc | DK | — | noc | Ørsted (former DONG Energy; now renewables-dominant) | orsted.com | company | official | production, exports, term_contract | proposed |
| ca-DK-mfa | DK | — | mfa | Ministry of Foreign Affairs | um.dk | international_agency | official | sanctions, policy | proposed |
| ca-DK-customs_export | DK | — | customs_export | Danish Customs Agency (Toldstyrelsen) | toldstyrelsen.dk | international_agency | official | exports, export_license | proposed |
| ca-DK-upstream_regulator | DK | — | upstream_regulator | Danish Energy Agency (DEA) | ens.dk | international_agency | official | production, force_majeure | proposed |
| ca-DK-gas_tso | DK | — | gas_tso | Energinet (gas TSO + Baltic Pipe) | energinet.dk | international_agency | official | pipeline_flow, supply_disruption | proposed |
| ca-DK-national_exchange | DK | — | national_exchange | Nasdaq Copenhagen | nasdaqomxnordic.com | exchange | official | pricing_formula | proposed |
| ca-DK-central_bank | DK | — | central_bank | Danmarks Nationalbank | nationalbanken.dk | international_agency | official | pricing_formula | proposed |
| ca-DK-environment_regulator | DK | — | environment_regulator | Danish Environmental Protection Agency (MST) | mst.dk | international_agency | official | refinery_outage | proposed |
| ca-DK-coast_guard_navy | DK | — | coast_guard_navy | Royal Danish Navy (Søværnet) | forsvaret.dk | international_agency | official | port_closure, force_majeure | proposed |

## Structural note: `port_maritime_authority` → `gas_tso`
Denmark's port authority (Port of Copenhagen, Port of Esbjerg) is less analytically significant for energy trading than **Energinet as gas TSO** — Energinet manages Baltic Pipe flows, Danish grid balancing, and is the primary signal for North Sea gas supply into Europe. Slot `port_maritime_authority` replaced with `gas_tso`; Esbjerg port (North Sea supply base) monitored via Energinet + DEA.

## Cross-check (key entries)

### ca-DK-upstream_regulator (DEA)
- **Supply:** DEA licenses North Sea blocks; DUC (TotalEnergies op.) = Tyra field (redeveloped 2024, ~3 bcm/y gas); Halfdan, Dan, Valdemar fields; DEA production statistics = tier-1 Danish upstream signal
- **Geopolitics:** Baltic Pipe (Norway→Denmark→Poland, 10 bcm/y, Oct 2022) = post-NordStream Europe supply alternative; Greenland critical minerals licensing; Danish Straits = Russian crude monitoring
- **Logistics:** Esbjerg port (North Sea helicopter + supply base); Fredericia refinery (Crossroads of Denmark terminal); Baltic Pipe Nybro entry point

### ca-DK-gas_tso (Energinet)
- **Supply:** Energinet gas flow data = Baltic Pipe + Danish grid; natural gas storage (Lille Torup + Stenlille UGS); daily transparency data (ENTSOG node); Tyra plateau deliverability
- **Geopolitics:** EU gas security coordination; Baltic Pipe alternative to Russian supply; Sabotage risk (post-NordStream precedent = Baltic infrastructure threat signal)
- **Logistics:** Nybro terminal (Norwegian gas entry); Ellund interconnection point (Germany); Dragør (Sweden); Danish Straits vessel traffic (ship-AIS monitoring)

## Expansion slots (10+)
- ca-DK-duc — Danish Underground Consortium (TotalEnergies/Noreco DUC)
- ca-DK-totalenergies_dk — TotalEnergies E&P Denmark (DUC operator)
- ca-DK-nordic_energy_regulators — NordREG (Nordic energy market regulator)
- ca-DK-baltic_pipe_monitor — Baltic Pipe Project tracking (GAZ-SYSTEM/Energinet)
- ca-DK-greenland_minerals — Geological Survey of Denmark and Greenland (GEUS)

## Anti-patterns
- Skip: The Local Denmark energy section (expat aggregator)
- Skip: Berlingske Tidende energy commentary (secondary Danish press)
