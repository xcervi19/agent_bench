# India discounted crude

**Commodity:** crude  
**Geography:** India — import/refining complex  
**Last reviewed:** 2026-07-23  

## Executive summary

India is a major buyer of discounted/sanctioned-linked crude (Urals and others) within its non-aligned sanctions stance; MoPNG and MEA signals plus port/shipping oversight set the offtake story. Scan must catch first: mopng.gov.in, mea.gov.in, dgshipping.gov.in, ONGC context, and OFAC/EU lists for compliance risk.

## Price drivers (trader lens)

1. Russian/other discount crude availability vs freight/insurance.
2. MoPNG policy on import sourcing and refining runs.
3. MEA diplomacy on sanctions alignment.
4. Port/VLCC terminal constraints (DG Shipping).
5. Rupee/FX (RBI) affecting import affordability.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Ministry of Petroleum and Natural Gas | Policy | Ministry of Petroleum and Natural Gas |
| Ministry of External Affairs | Diplomacy / sanctions stance | Ministry of External Affairs |
| Directorate General of Shipping | Ports / VLCC oversight | Directorate General of Shipping |
| ONGC | NOC | ONGC |
| Indian Navy | Maritime security | Indian Navy |
| Reserve Bank of India | FX | Reserve Bank of India |
| OFAC (Treasury) | Sanctions risk | OFAC (Treasury) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Ministry of Petroleum and Natural Gas | mopng.gov.in | Import/refining policy; stock statements | P1 |
| Ministry of External Affairs | mea.gov.in | Non-aligned sanctions / energy diplomacy | P1 |
| Directorate General of Shipping | dgshipping.gov.in | Paradip/Haldia/Mundra/JNPT/Vizag VLCC oversight | P1 |
| ONGC | ongcindia.com | Domestic production offsetting imports | P2 |
| Indian Navy | indiannavy.nic.in | Arabian Sea security | P2 |
| Reserve Bank of India | rbi.org.in | INR / import payment context | P2 |
| Ministry of Env, Forest & Climate | moef.gov.in | Refinery clearances | P3 |
| OFAC (Treasury) | treasury.gov | Secondary sanctions risk on trades | P1 |
| EU Sanctions (Russian gas linkage) | ec.europa.eu | EU measures affecting trade services | P2 |
| EIA | eia.gov | India in balances | P2 |
| IEA | iea.org | India demand | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

West/east coast VLCC-capable ports clear Middle East, Russian, and Atlantic barrels into a large refining system. Insurance/freight for discounted grades is as binding as FOB differentials. See energy_sanctions_compliance and russia_oil_exports.

## Geopolitical triggers

- MEA/MoPNG shift on Russian crude share.
- OFAC action hitting Indian offtakers/banks/tankers.
- Freight/insurance spike on shadow-fleet routes.
- Strategic reserve build/release.
- Domestic election/fuel-policy shock changing runs.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| MoPNG / MEA | event-driven | India time |
| DG Shipping | event / ops | India time |
| OFAC/EU | event-driven | US/EU hours |
| IEA/EIA | monthly | As published |

## Tier 2 context sources

RBI; MoEF clearances. MoPNG+MEA+sanctions lists are the core.

## Anti-patterns

- Broker “India bought X cargoes” without MoPNG/customs corroboration.
- Ignoring payment/insurance frictions when discounts look wide.
- Inventing IOC/BPCL domains not pulled from whitelist.

## Related playbooks

- russia_oil_exports.md
- energy_sanctions_compliance.md
- china_oil_gas_imports.md
- crude_oil_global.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
