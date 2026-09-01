# India gas demand and supply balance

**Commodity:** gas  
**Geography:** India — national gas balance (domestic production + LNG imports vs. sector demand)  
**Last reviewed:** 2026-08-20  
**Analyst owner:** operator brief (pilot topic #45)

## Executive summary

India consumes roughly **200 mcm/d** of natural gas, split roughly **half imported LNG,
half domestic production**. Demand sits in four blocks: **fertilizers (~50 mcm/d)**,
**city gas distribution (~50 mcm/d)**, **power generation**, and **refining/petrochemicals**.
Unlike Europe or the US, India is **data-visible but forecast-poor** — the balance is
published monthly by PPAC and the regulator's CGD rounds are public, while forward views
are scarce. The scan must therefore anchor on **PPAC's monthly sector-wise consumption**,
**PNGRB's CGD authorisations**, and **CEA's generation data**, and treat any genuine
forecast or outlook as high-value precisely because it is rare.

The structural story to track is **city gas growth**: as PNGRB authorises new geographical
areas and operators connect new cities to the grid, CGD demand rises. Anything that moves
**Indian electricity** in general is in scope — gas-fired generation is the swing sector
between the fixed fertilizer offtake and the price-sensitive rest.

Numbers above are the operator's working baseline (2026-08-20), not measured values;
use them as orders of magnitude and correct them against PPAC when PPAC is reachable.

**Forecasts do exist for this market, contrary to the brief.** PNGRB publishes its own
demand projections — ~300 mmscmd by 2030 and ~423 mmscmd by 2040 (base case) — along with
rapid assessments and zonal pipeline studies. They are PDFs on `pngrb.gov.in` that generic
search does not rank; a domain-filtered search reaches them directly. Treat "India has no
forecasts" as false and go to the regulator first.

## Price drivers (trader lens)

1. **Domestic production vs. LNG import call** — every mcm/d ONGC/OIL/DGH does not deliver
   is an mcm/d that must be bought as spot or term LNG (Petronet, GAIL, GSPC portfolios).
2. **Fertilizer offtake** — the most price-insensitive block (**~58 mmscmd**, sourced from
   PNGRB projection work 2026-08-21; the operator's working baseline said ~50); driven by urea
   plant runs, subsidy policy and the monsoon-linked crop cycle, not by JKM.
3. **City gas connection growth** — PNGRB geographical-area rounds, CNG station and PNG
   household counts; the only structurally growing block.
4. **Gas-fired power economics** — gas plants run against coal and renewables; a summer
   demand peak or a coal/hydro shortfall pulls gas into the stack, and CEA generation data
   shows it first.
5. **Refinery and petrochemical runs** — internal fuel and feedstock demand tracking
   throughput at the large coastal refining complex.
6. **LNG price sensitivity** — Indian buyers are the marginal price-elastic bidder in Asia;
   spot JKM levels decide whether the import half of the balance is filled or demand is
   simply destroyed.
7. **Regasification and pipeline capacity** — terminal utilisation (Dahej, Hazira, Kochi,
   Ennore, Mundra) and GAIL's trunk network gate how much LNG can reach inland demand.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Petroleum Planning & Analysis Cell (PPAC) | Official gas balance and sector-wise consumption | Petroleum Planning & Analysis Cell (PPAC) |
| Petroleum & Natural Gas Regulatory Board (PNGRB) | Downstream regulator; CGD authorisations, tariffs | Petroleum and Natural Gas Regulatory Board (PNGRB) |
| Ministry of Petroleum and Natural Gas | Policy, pricing, allocation priority | Ministry of Petroleum and Natural Gas |
| Directorate General of Hydrocarbons (DGH) | Domestic production, blocks, licensing | Directorate General of Hydrocarbons |
| ONGC | Largest domestic producer | ONGC |
| GAIL (India) | Transmission network, LNG portfolio, marketing | GAIL (India) |
| Petronet LNG | Largest regas capacity (Dahej, Kochi) | Petronet LNG |
| Indian Gas Exchange (IGX) | Domestic traded gas prices and volumes | Indian Gas Exchange (IGX) |
| Central Electricity Authority (CEA) | Generation by fuel, gas plant load factors | Central Electricity Authority (CEA) |
| Ministry of Power | Power policy affecting gas-fired dispatch | Ministry of Power |
| IndianOil / BPCL / HPCL | Refining runs, own CGD and marketing arms | IndianOil, BPCL, HPCL |
| Gujarat Gas | Largest CGD operator — connection growth proxy | Gujarat Gas |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Petroleum Planning & Analysis Cell (PPAC) | ppac.gov.in | Monthly gas production, LNG imports, **sector-wise consumption** (fertilizer / CGD / power / refinery) — the balance itself | P1 |
| Petroleum and Natural Gas Regulatory Board (PNGRB) | pngrb.gov.in | CGD bidding rounds, geographical-area authorisations, minimum work programme, tariff orders | P1 |
| Ministry of Petroleum and Natural Gas | mopng.gov.in | Allocation priority, APM/domestic gas pricing, policy statements | P1 |
| Directorate General of Hydrocarbons | dghindia.gov.in | Domestic production, field approvals, licensing rounds | P1 |
| Central Electricity Authority (CEA) | cea.nic.in | Monthly generation by fuel; gas-based capacity and PLF; demand peaks | P1 |
| GAIL (India) | gailonline.com | Pipeline commissioning, transmission volumes, LNG contracting | P2 |
| Petronet LNG | petronetlng.in | Terminal utilisation, contract renegotiation, capacity expansion | P2 |
| Indian Gas Exchange (IGX) | igxindia.com | Traded domestic gas volumes and cleared prices | P2 |
| ONGC | ongcindia.com | Production trajectory of the domestic half of the balance | P2 |
| Ministry of Power | powermin.gov.in | Dispatch policy, gas-power schemes, demand-side measures | P2 |
| National Power Portal | npp.gov.in | Daily/monthly power generation and capacity dashboards | P2 |
| IndianOil | iocl.com | Refinery throughput; CGD arm | P3 |
| BPCL | bharatpetroleum.in | Refinery throughput; CGD arm | P3 |
| HPCL | hindustanpetroleum.com | Refinery throughput; CGD arm | P3 |
| Gujarat Gas | gujaratgas.com | CNG stations, PNG connections — city gas growth in the largest market | P3 |
| IEA | iea.org | India gas and electricity outlooks — one of the few genuine forecast sources | P2 |
| EIA | eia.gov | India in global balances | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official handle in `source_whitelist.json`; blocked on #31 (scraping infrastructure) |

## Infrastructure & logistics

Regasification is concentrated on the west coast — **Dahej** (Petronet, the largest),
**Hazira**, **Mundra**, **Kochi** — with **Ennore** on the east coast; terminal utilisation
is uneven because inland pipeline reach, not regas capacity, is usually the constraint.
GAIL's trunk network plus the national gas grid build-out determines which CGD areas can
physically be connected at all, which is why a PNGRB authorisation only converts to demand
once the pipeline arrives. Fertilizer plants and refineries sit on dedicated offtake;
CGD and power draw on whatever is left.

## Geopolitical triggers

- **APM / domestic gas price revision** — reprices the domestic half and shifts who bids for LNG.
- **Fertilizer subsidy or urea policy change** — moves the largest fixed block.
- **PNGRB CGD round award or missed work programme** — changes the structural growth path.
- **Coal, hydro or renewables shortfall in a demand peak** — pulls gas into power generation.
- **Spot LNG price spike** — India steps back from the market; import half of the balance shrinks.
- **Long-term LNG contract signing or renegotiation** (Qatar, US, ADNOC portfolios).
- **Domestic production surprise** (KG basin ramp-up or decline) — direct import substitution.
- **Monsoon** — simultaneously drives crop cycle (fertilizer) and hydro (power) demand.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| PPAC gas balance / sector consumption | monthly | ~3–4 weeks after month end, India time |
| PNGRB authorisations, tariff orders | event-driven | India time |
| CEA generation by fuel | monthly (plus daily dashboards) | India time |
| MoPNG / DGH policy statements | event-driven | India time |
| IGX volumes and prices | monthly / continuous | India time |
| IEA India outlooks | occasional | As published |

## Tier 2 context sources

World Bank / ADB India energy notes, university and think-tank gas demand studies,
company investor presentations (GAIL, Petronet, Gujarat Gas quarterly decks) — useful
for the forecast gap, but not primary scan anchors.

## Anti-patterns

- Treating a trade-press "India to import X mtpa by 2030" headline as a forecast without
  naming whose model it is — the forecast scarcity is exactly what makes this topic hard.
- Quoting national consumption without saying whether it is **production + imports** or
  **sector consumption**, and without the month — the two series differ.
- Reading a **PNGRB geographical-area award as delivered demand**; it is a right to build,
  years ahead of volume.
- Attributing a demand swing to CGD when it was gas-fired **power** responding to a heat
  wave (or the reverse) — split the sectors before drawing a conclusion.
- Confusing **mcm/d** with **mmscmd** conventions, or LNG **mtpa** with pipeline **mcm/d**,
  when comparing sources.
- Inventing operator or ministry domains not present in `source_whitelist.json`.

## Related playbooks

- india_discounted_crude.md — the crude/refining side of the same country
- lng_global_supply.md — the supply side of India's import half
- natural_gas_global.md
- qatar_ras_laffan_lng.md — largest term supplier
- us_lng_gulf_terminals.md — growing term supplier
- southeast_asia_lng_imports.md — competing price-elastic Asian demand
- japan_korea_lng_demand.md — the price-setting Asian buyers India bids against

## Changelog

- 2026-08-21 — fertilizer offtake corrected to ~58 mmscmd from PNGRB projection work;
  recorded that PNGRB publishes 2030/2040 demand projections, which the brief assumed did
  not exist. Both found via a domain-filtered search (#46 Build item 0).
- 2026-08-20 — initial draft for pilot topic #45. Fundamentals (200 mcm/d, ~50/50
  domestic/LNG, fertilizer ~50, CGD ~50) supplied by the operator as a working baseline;
  primary source table verified by domain reachability + page identity on 2026-08-20.
  Department of Fertilizers (`fert.gov.in`) and Grid Controller of India (`grid-india.in`)
  were unreachable from the authoring host and are deliberately **not** listed — fertilizer
  and grid-level demand route through PPAC and CEA until those two are verified.
