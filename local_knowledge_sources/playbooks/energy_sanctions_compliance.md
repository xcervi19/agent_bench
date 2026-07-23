# Energy sanctions and compliance

**Commodity:** crude | LNG | gas | products  
**Geography:** global (US / UK / EU / UN regimes)  
**Last reviewed:** 2026-07-23  

## Executive summary

Sanctions and export controls remove or reroute barrels, tankers, insurers, and offtakers — repricing Russian, Iranian, and Venezuelan supply and shadow-fleet logistics. Scan must catch first: OFAC (treasury.gov) designations and licenses, UK OFSI (gov.uk), EU sanctions pages (ec.europa.eu), US State coordination, and BIS/commerce export-control overlays affecting energy equipment and services.

## Price drivers (trader lens)

1. New SDN / vessel / trader designations shrinking shadow-fleet capacity.
2. License/waiver grants or revocations (Venezuela, Iran-related, etc.).
3. Price-cap / services bans altering Russian FOB discounts and freight.
4. EU package changes on crude, products, or gas.
5. Enforcement actions that spike demurrage, P&I refusal, or STS friction.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| OFAC (Treasury) | US sanctions list / licenses | OFAC (Treasury) |
| BIS / OFAC (export controls) | US export controls | BIS / OFAC (export controls) |
| US Dept of State | Sanctions diplomacy | US Dept of State |
| HM Treasury (sanctions list) | UK OFSI | HM Treasury (sanctions list) |
| Foreign, Commonwealth & Development Office | UK diplomacy | Foreign, Commonwealth & Development Office |
| EU Sanctions (Russian gas linkage) | EU packages | EU Sanctions (Russian gas linkage) |
| EU Energy | Energy + sanctions policy overlap | EU Energy |
| IMO | Maritime regulatory / guidance | IMO |
| GISIS IMO | Flag / ship status screening | GISIS IMO |
| PDVSA | Venezuela NOC (target/license-sensitive) | PDVSA |
| Rosneft | Russia producer | Rosneft |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| OFAC (Treasury) | treasury.gov | SDN updates; GLs; FAQs; vessel designations | P1 |
| BIS / OFAC (export controls) | commerce.gov | Entity list / export control rules hitting energy | P1 |
| US Dept of State | state.gov | Sanctions policy coordination announcements | P1 |
| HM Treasury (sanctions list) | gov.uk | OFSI listings and enforcement | P1 |
| Foreign, Commonwealth & Development Office | gov.uk/fcdo | UK diplomatic sanctions framing | P2 |
| EU Sanctions (Russian gas linkage) | ec.europa.eu | Council packages; oil/gas measures | P1 |
| EU Energy | energy.ec.europa.eu | Energy-market measures tied to sanctions | P1 |
| IMO | imo.org | Maritime sanctions guidance | P2 |
| GISIS IMO | gisis.imo.org | Flag state / ship status for dark-fleet screening | P2 |
| Equasis | equasis.org | Ship particulars cross-check | P2 |
| EMSA | emsa.europa.eu | EU maritime safety / tracking context | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Enforcement bites at loading ports, STS hubs, insurers, and flag registries. Russian Pacific/Baltic/Black Sea routes, Iranian Gulf loadings, and Venezuelan upgrader/export chains are highest sensitivity. Cross-check russia_oil_exports, iran_oil_geopolitics, venezuela_sanctions_exports, and shipping screens (IMO/GISIS).

## Geopolitical triggers

- OFAC vessel wave or oil-trader designation.
- EU “next package” rumor confirmed on ec.europa.eu.
- Venezuela license change (broader or tighter offtake).
- UK OFSI alignment or divergence vs OFAC (basis risk for sterling trade).
- P&I / flag-state refusal cascading into freight spikes.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| OFAC SDN updates | event-driven | Often US business hours |
| EU Official Journal / sanctions pages | event-driven | Brussels hours |
| OFSI updates | event-driven | London hours |
| IMO circulars | ad hoc | imo.org |

## Tier 2 context sources

National MFA statements from producer/consumer states for political framing; Comtrade for lagged trade-pattern shifts after sanctions. Not a substitute for the legal text on treasury.gov / gov.uk / ec.europa.eu.

## Anti-patterns

- Relying on unverified “sanctions list PDF” mirrors.
- Assuming media paraphrase equals operative legal scope.
- Ignoring licenses/GLs when calling supply “banned.”
- Using AIS alone without OFAC/IMO registry cross-check for designated tonnage.

## Related playbooks

- russia_oil_exports.md
- iran_oil_geopolitics.md
- venezuela_sanctions_exports.md
- crude_oil_global.md
- opec_plus_policy.md

## Changelog

- 2026-07-23 — initial draft
