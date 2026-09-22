# Brazil power — hydro balance, thermal dispatch and the LNG call

**Commodity:** power / gas  
**Geography:** Brazil — Sistema Interligado Nacional (SIN), four subsystems: SE/CO, S, NE, N  
**Last reviewed:** 2026-09-18  
**Analyst owner:** second country pilot (#53)

## Executive summary

Brazil runs a **hydro-dominated grid with large seasonal storage**. The system operator
(ONS) dispatches thermal plant against reservoir levels rather than against a market
merit order alone: when stored energy falls, thermal runs. A material share of that
thermal is **gas-fired**, and part of that gas is **imported LNG**. Brazil is therefore a
**price-elastic Atlantic-basin LNG buyer whose demand is forecastable from public
hydrology** — and every input to that forecast is published **daily, in Portuguese, by
the operator itself**.

That is the whole reason this topic exists. The driver is not a scoop; it is an open data
series that mainstream aggregators do not carry as a market signal. Whoever reads ONS
directly sees Brazil's LNG call forming days before it is reported as news.

**Measured from ONS's own series on 2026-09-16** — these are read values, not the
operator's estimates:

- National generation mix: **hydro ~64 %, wind ~21.6 %, thermal 11.0 %, solar ~3 %**
  (daily aggregate, `balanco-energia-subsistema`).
- **67 reservoirs reporting, mean stored-energy fill 71.2 %** (`ear-diario-por-reservatorio`).
- Stress is **concentrated, not national**: A. Vermelha 32 %, São Simão 37 %, Paraibuna 37 %
  in the Southeast/Paraná basins, while southern reservoirs (Garibaldi, São Roque,
  Quebra Queixo) sit **above 100 %** of their own reference.
- Northeast is wind-led: at 23:00 on 2026-09-16 the subsystem ran **21.2 GW wind against
  3.8 GW hydro and 0.4 GW thermal**.
- Southeast carries the thermal fleet: **5.9 GW of the national 9.9 GW**.

September is the end of the Southeast dry season, so these are **seasonal-low readings
before the November wet season**. Read any single number against its subsystem and its
season, never as "Brazil".

## Price drivers (trader lens)

1. **Stored energy (EAR) by subsystem** — the level itself. The Southeast/Centre-West
   holds most of the storage, so the national average hides the number that matters.
2. **Natural inflow energy (ENA) against the long-term average** — the *forward* signal.
   EAR says where we are; ENA says where we are going, days to weeks ahead.
3. **Thermal dispatch and marginal cost (CMO)** — published half-hourly per subsystem;
   the price at which the operator is willing to burn fuel instead of water.
4. **Northeast wind** — structurally large and volatile. A windy week in the Nordeste
   displaces thermal nationally; a still week does the opposite, with no reservoir change.
5. **The LNG import call** — terminal send-out into gas-fired plant. This is the link to
   the Atlantic basin and to European gas prices: cargoes Brazil buys do not reach Europe.
6. **Inter-subsystem transmission limits** — surplus in the South cannot always relieve
   the Southeast; a constraint turns a national surplus into a local thermal dispatch.
7. **Tariff flags (bandeiras tarifárias)** — the policy pass-through of thermal cost to
   consumers, and a public signal of how expensive the operator expects dispatch to be.
8. **Domestic pre-salt associated gas versus imported LNG** — the substitution that decides
   whether higher thermal dispatch becomes an actual import.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| ONS — Operador Nacional do Sistema Elétrico | System operator; dispatch, reservoirs, load, open data | ONS |
| CCEE — Câmara de Comercialização de Energia Elétrica | Market settlement, PLD, contracted volumes | CCEE |
| ANEEL | Power regulator; auctions, tariffs, generation register | ANEEL |
| MME — Ministério de Minas e Energia | Energy policy, monthly energy bulletin | MME |
| CNPE | National energy policy council; dispatch and security-of-supply decisions | CNPE |
| ANP | Oil & gas regulator; domestic gas production and LNG import volumes | ANP |
| Petrobras | Largest gas supplier; terminals, thermal fuel contracts | Petrobras |
| INMET | Meteorology — rainfall driving inflows | INMET |
| ABRACEEL | Free-market traders' association; market structure commentary | ABRACEEL |
| IBGE | Macro and industrial output behind load | IBGE |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| ONS — open data portal | dados.ons.org.br | **85 published datasets**: EAR, ENA, CMO, subsystem balance, load, capacity | P1 |
| ONS — operator site | ons.org.br | Operation bulletins, weekly operating programme, load and generation now | P1 |
| CCEE | ccee.org.br | PLD, InfoMercado, settlement and contracted volumes | P1 |
| ANEEL | gov.br/aneel | Auctions, tariff flags, generation register, indicators | P1 |
| MME | gov.br/mme | Monthly energy bulletin; policy on thermal dispatch and LNG | P1 |
| ANP | gov.br/anp | Monthly natural gas production, LNG import volumes, terminal data | P1 |
| CNPE | gov.br/mme (CNPE pages) | Security-of-supply and out-of-merit dispatch resolutions | P2 |
| INMET | portal.inmet.gov.br | Rainfall and forecasts over the generating basins | P2 |
| Petrobras | petrobras.com.br | Gas supply, terminal utilisation, thermal fuel contracting | P2 |
| ABRACEEL | abraceel.com.br | Market-structure and liberalisation commentary | P3 |
| IBGE | ibge.gov.br | Industrial production behind load growth | P3 |
| EIA | eia.gov | Brazil country analysis; LNG trade in global balances | P2 |
| World Bank | data.worldbank.org | Long-run energy and macro series | P3 |

**Deliberately absent, and why.** `epe.gov.br` (Empresa de Pesquisa Energética — the
planning office that publishes the Balanço Energético Nacional and the ten-year plan)
returned **HTTP 500 on two attempts on 2026-09-18**, and `dadosabertos.aneel.gov.br`
**timed out**. Both are exactly the sources a forecast section would want. Neither is
listed until it verifies, for the same reason `fert.gov.in` and `grid-india.in` were
refused on the India topic: an unreachable domain in the register is a query that silently
returns nothing. Re-check both before the first run.

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official handle in `source_whitelist.json`; blocked on #31 |

## Infrastructure & logistics

Storage is concentrated in the **Southeast/Centre-West** on the Paraná, Grande, Paranaíba
and São Francisco basins; the **South** has small storage and is rain-driven week to week;
the **North** (Tucuruí, Belo Monte) is run-of-river heavy, so its output tracks inflow with
almost no buffer; the **Northeast** is wind- and solar-led with hydro on the São Francisco.
Because the four subsystems are linked by long transmission corridors with real limits, a
national surplus does **not** guarantee that the deficit subsystem avoids thermal dispatch.
Gas-fired plant sits mostly in the Southeast and Northeast, fed by domestic pre-salt gas
through Petrobras' network and by **LNG through import terminals**, which is where a
Brazilian hydrology story becomes an Atlantic-basin cargo story.

## Geopolitical and market triggers

- **A dry-season inflow miss in the Southeast** — the classic thermal-dispatch trigger.
- **CNPE or ONS ordering out-of-merit thermal dispatch** for security of supply.
- **Tariff flag escalation** — public confirmation that expensive dispatch is expected.
- **A sustained still period in the Northeast** — removes ~20 GW of wind without warning.
- **LNG spot price moves** — decide whether the thermal call is met by import or by
  demand-side measures; the same JKM/TTF level that Europe is bidding against.
- **Pre-salt gas supply interruption or pipeline outage** — converts thermal dispatch
  directly into an import requirement.
- **Transmission outage between subsystems** — localises a surplus.
- **Auction results and new capacity commissioning** — the structural path of the mix.

## Data cadence

| Source | Frequency | Observed lag (2026-09-18) |
|--------|-----------|---------------------------|
| ONS `balanco-energia-subsistema` (hourly generation by source) | hourly | ~2 days |
| ONS `ear-diario-por-reservatorio` (stored energy) | daily | ~2 days |
| ONS `ena-diario-por-subsistema` (natural inflow energy) | daily | ~2 days |
| ONS `cmo-semi-horario` (marginal cost) | half-hourly | ~2 days |
| CCEE PLD / InfoMercado | weekly / monthly | days |
| ANEEL tariff flags, auctions | event-driven | same day |
| MME monthly energy bulletin | monthly | weeks |
| ANP gas production and LNG imports | monthly | ~6-8 weeks |

**This cadence is the point.** India's anchor series (PPAC) is monthly, and two of the
first nine daily refresh cycles on that topic added nothing at all. Brazil's anchor series
update **daily with a two-day lag**, so a daily cycle has something new to read every time
it runs.

## Tier 2 context sources

ONS data dictionaries (one PDF per series — the definitive explainer for every column we
poll), OIES papers on Latin American power and LNG, EIA Brazil country analysis, World Bank
series, university and think-tank studies of the Brazilian dispatch model. Useful for
framing; not primary scan anchors.

## Anti-patterns

- **Quoting "Brazilian reservoir levels" without the subsystem.** On 2026-09-16 the same
  country held a reservoir at 32 % and another at 143 %. The national mean is a summary,
  not a signal.
- **Treating Northeast wind as firm.** It swung from over 21 GW within a single evening's
  readings; the thermal it displaces returns when the wind stops.
- **Confusing CMO with PLD.** CMO is the operator's marginal operating cost; PLD is the
  settlement price CCEE publishes. Related, not interchangeable, and sourced from different
  institutions.
- **Reading MW as MWh.** ONS publishes instantaneous power and energy aggregates in the
  same file family.
- **Treating "thermal" as "gas".** Brazilian thermal includes coal, fuel oil, diesel,
  biomass and nuclear. Only part of a thermal increase becomes an LNG cargo.
- **Asserting an LNG import volume from a dispatch number.** The chain runs dispatch →
  gas burn → domestic supply shortfall → import. Each step needs its own source.
- **Citing EPE** until `epe.gov.br` verifies — see above.
- **Inventing operator or ministry domains** not present in `source_whitelist.json`.

## Related playbooks

- brazil_pre_salt.md — the upstream oil and associated-gas side of the same country
- lng_global_supply.md — the supply side of Brazil's import call
- europe_gas_storage_ttf.md — the market on the other side of the same cargo
- us_lng_gulf_terminals.md — the nearest swing supplier into the Atlantic basin
- natural_gas_global.md
- qatar_ras_laffan_lng.md
- japan_korea_lng_demand.md — the Asian bid Brazil competes against

## Changelog

- 2026-09-18 — initial draft for the second country pilot (#53). Every primary domain in
  the table above was verified on 2026-09-18 by **reachability plus page identity**, the
  same gate used for India. `epe.gov.br` (HTTP 500, twice) and `dadosabertos.aneel.gov.br`
  (timeout) failed the gate and are deliberately excluded. The structural numbers in the
  executive summary were **measured** from ONS open data on 2026-09-16, not estimated:
  daily generation mix, 67-reservoir mean fill, and the per-subsystem split.
