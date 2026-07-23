# Russia oil exports

**Commodity:** crude | products  
**Geography:** Russia — Baltic / Black Sea / Pacific / pipeline  
**Last reviewed:** 2026-07-23  

## Executive summary

Russian crude and product exports clear under sanctions, price-cap, and shadow-fleet constraints across Baltic, Black Sea, and Pacific (Kozmino) routes. Scan must catch first: minenergo.gov.ru and Rosneft, Transneft/Kozmino logistics, Rosmorport, OFAC/EU/UK sanctions updates, and Turkish Straits delays for Black Sea barrels.

## Price drivers (trader lens)

1. Seaborne crude loadings by basin vs sanctions enforcement intensity.
2. New OFAC/EU/UK designations on vessels, traders, or services.
3. Transneft / Kozmino Pacific program changes.
4. Bosporus delays stacking Black Sea barrels.
5. Discount vs Brent (Urals/ESPO structure) as enforcement proxy.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Ministry of Energy | Policy | Ministry of Energy (minenergo.gov.ru) |
| Rosneft | Largest producer | Rosneft |
| Kozmino tank storage | Pacific export node | Kozmino tank storage |
| Transneft (RU) / MOL (HU) | Pipeline / EU land context | Transneft (RU) / MOL (HU) |
| Novatek | Condensate / LNG-adjacent | Novatek |
| Rosmorport | Ports | Rosmorport |
| OFAC (Treasury) | US sanctions | OFAC (Treasury) |
| EU Sanctions (Russian gas linkage) | EU packages | EU Sanctions (Russian gas linkage) |
| HM Treasury (sanctions list) | UK OFSI | HM Treasury (sanctions list) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Ministry of Energy | minenergo.gov.ru | Production / export policy | P1 |
| Rosneft | rosneft.com | Output and export guidance | P1 |
| Kozmino tank storage | transneft.ru | Pacific pipeline/terminal logistics | P1 |
| Rosmorport | rosmorport.ru | Port status | P2 |
| Novatek | novatek.ru | Arctic / condensate / LNG-linked signals | P2 |
| OFAC (Treasury) | treasury.gov | SDN / vessel waves; GLs | P1 |
| EU Sanctions (Russian gas linkage) | ec.europa.eu | Oil/product package changes | P1 |
| HM Treasury (sanctions list) | gov.uk | OFSI listings | P1 |
| Kıyı Emniyeti (fog/current closures) | kiyiemniyeti.gov.tr | Bosporus delays for Black Sea exports | P1 |
| IMO | imo.org | Maritime sanctions guidance | P2 |
| GISIS IMO | gisis.imo.org | Dark-fleet screening | P2 |
| OPEC | opec.org | Russia in OPEC+ tables | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Export basins: Baltic product/crude ports, Black Sea (Bosporus-constrained), Pacific Kozmino ESPO, plus residual pipeline politics into Europe. Shadow-fleet STS and flag changes are enforcement battlegrounds — pair with energy_sanctions_compliance and turkish_straits_bospor.

## Geopolitical triggers

- OFAC tanker designation wave.
- EU ban/enforcement tightening on products or services.
- Transneft outage or Kozmino constraint.
- Black Sea security shock cutting loadings.
- OPEC+ Russian “pledge” vs observed seaborne flows divergence.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| minenergo / Rosneft | event-driven | Moscow time |
| OFAC / EU / OFSI | event-driven | US/EU/UK hours |
| Kıyı Emniyeti | event-driven / daily ops | Türkiye time |
| Transneft | ops / event | As issued |

## Tier 2 context sources

MOL Hungary pipeline context pages; GECF/IEA for gas overlap. Crude export truth remains ministry/NOC + sanctions + ports.

## Anti-patterns

- AIS-only “export estimates” without sanctions-list cross-check.
- Treating quota pledges as seaborne reality.
- Ignoring Pacific vs Baltic basis when quoting a single “Russian discount.”

## Related playbooks

- energy_sanctions_compliance.md
- turkish_straits_bospor.md
- opec_plus_policy.md
- yamal_arctic_lng.md
- kazakhstan_caspian_exports.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
