# Crude oil — global balances

**Commodity:** crude  
**Geography:** global  
**Last reviewed:** 2026-07-23  

## Executive summary

Global crude pricing is set by OPEC+ supply policy, OECD inventories, US production/exports, and chokepoint risk. Scan must catch first: OPEC MOMR / ministerial decisions, IEA Oil Market Report / stock signals, EIA WPSR and crude export runs, and any OFAC/EU measure that removes barrels from the seaborne market.

## Price drivers (trader lens)

1. OPEC+ effective spare capacity and compliance vs announced cuts/increases.
2. OECD commercial stocks and SPR policy (IEA / EIA / DOE).
3. US shale output and Gulf Coast crude export capacity (EIA weekly).
4. Benchmark structure (Brent vs WTI, time spreads) reflecting physical tightness.
5. Geopolitical / sanctions barrel loss (Iran, Russia, Venezuela) and force majeure.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| OPEC | Producer group / MOMR | OPEC |
| IEA | OECD demand/stocks / emergency stocks | IEA |
| EIA | US + global reference weekly data | EIA |
| JODI | National oil balance submissions | JODI |
| IEF | Producer–consumer dialogue; hosts JODI | IEF |
| Saudi Aramco | Marginal OSP / largest exporter | Saudi Aramco |
| CME Group | WTI futures / settlements | CME Group |
| ICE | Brent futures / settlements | ICE |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| OPEC | opec.org | MOMR; production tables; ministerial communiqués | P1 |
| IEA | iea.org | Oil Market Report; stock/demand revisions; emergency stock actions | P1 |
| EIA | eia.gov | WPSR; STEO; crude production & export series | P1 |
| JODI | jodidata.org | Oil World Database balances (lagged confirmation) | P1 |
| IEF | ief.org | Joint statements; JODI governance | P2 |
| Saudi Aramco | aramco.com | OSP differentials; production / capacity commentary | P1 |
| US DOE | energy.gov | SPR releases / exchanges | P1 |
| CME Group | cmegroup.com | WTI contract specs, settlements, delivery notices | P2 |
| ICE | ice.com | Brent settlements; expiry / EFP flows | P2 |
| UN COMTRADE | comtrade.un.org | Bilateral crude trade (lagged) | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Seaborne crude hinges on Hormuz, Malacca, Cape, Suez/Red Sea, and Bosporus routes; USGC and Middle East loading terminals set Atlantic/Asia arb. Storage hubs (Cushing, ARA, Fujairah, Singapore) transmit inventory tightness into differentials. Related detail in chokepoint and hub playbooks.

## Geopolitical triggers

- OPEC+ cut/raise or non-compliance surprise.
- New OFAC / EU / UK sanctions on producers, tankers, or insurers.
- Strait of Hormuz or Red Sea transit disruption.
- Major NOC force majeure (Libya, Nigeria, Iraq southern exports).
- Coordinated SPR release or refill announcement (DOE / IEA members).

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| EIA WPSR | weekly | Wed ~15:30 (US winter/summer shifts) |
| OPEC MOMR | monthly | Mid-month (watch opec.org calendar) |
| IEA Oil Market Report | monthly | Mid-month |
| JODI oil | monthly (lagged) | After national submissions |
| Aramco OSP | monthly | Early month for next-month loadings |

## Tier 2 context sources

IEF dialogues; UN Comtrade bilateral lags; exchange contract-spec pages for delivery mechanics. Not primary scan anchors for breaking supply shocks.

## Anti-patterns

- Treating Bloomberg/Reuters headlines as primary without tracing to OPEC/IEA/EIA/NOC.
- SEO “oil price today” blogs; retail broker research as supply truth.
- Unverified Telegram “OPEC leak” channels.
- Using lagged Comtrade as a real-time balance signal.

## Related playbooks

- opec_plus_policy.md
- oil_benchmarks_and_spreads.md
- energy_sanctions_compliance.md
- lng_global_supply.md
- strait_of_hormuz.md

## Changelog

- 2026-07-23 — initial draft
