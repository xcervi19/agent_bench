# Yamal Arctic LNG

**Commodity:** LNG  
**Geography:** Russia Arctic — Yamal / Northern Sea Route  
**Last reviewed:** 2026-07-23  

## Executive summary

Novatek-led Arctic LNG (Yamal-class) is a sanctioned, ice-class logistics story; cargoes and offtake shift with OFAC/EU measures and Arctic navigation seasons. Scan must catch first: novatek.ru, minenergo.gov.ru, rosmorport.ru, and treasury.gov / ec.europa.eu sanctions updates.

## Price drivers (trader lens)

1. Sanctions designations on projects, tankers, or offtakers.
2. Icebreaker / NSR seasonal navigability.
3. Train outages at Arctic LNG plants.
4. Europe vs Asia offtake redirection under compliance pressure.
5. Russian energy ministry policy on LNG prioritization.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Novatek | Arctic LNG operator | Novatek |
| Ministry of Energy | Russia policy | Ministry of Energy (minenergo.gov.ru) |
| Rosmorport | Ports | Rosmorport |
| OFAC (Treasury) | US sanctions | OFAC (Treasury) |
| EU Sanctions (Russian gas linkage) | EU packages | EU Sanctions (Russian gas linkage) |
| HM Treasury (sanctions list) | UK OFSI | HM Treasury (sanctions list) |
| IMO | Maritime guidance | IMO |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Novatek | novatek.ru | Project status; shipping; production | P1 |
| Ministry of Energy | minenergo.gov.ru | LNG / export policy | P1 |
| Rosmorport | rosmorport.ru | Port/logistics status | P2 |
| OFAC (Treasury) | treasury.gov | SDN / vessel / project actions | P1 |
| EU Sanctions (Russian gas linkage) | ec.europa.eu | EU LNG/oil package changes | P1 |
| HM Treasury (sanctions list) | gov.uk | OFSI listings | P1 |
| GISIS IMO | gisis.imo.org | Ship/flag screening | P2 |
| IMO | imo.org | Arctic/maritime guidance | P3 |
| IEA | iea.org | LNG balance impact | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Arctic ice-class LNG carriers and seasonal NSR vs conventional routes define delivery risk. Sanctions can strand or reroute cargoes even when plants run. Pair with energy_sanctions_compliance and russia_oil_exports.

## Geopolitical triggers

- New OFAC/EU designation on Arctic LNG entities or fleet.
- Winter ice extreme delaying loadings.
- Major train trip at Yamal-class plant.
- Insurance/P&I withdrawal from Arctic LNG trade.
- Buyer compliance exit from Russian LNG.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Novatek / minenergo | event-driven | Moscow time |
| OFAC / EU / OFSI | event-driven | US/EU/UK hours |
| IEA | outlook / ad hoc | As published |

## Tier 2 context sources

IEA for balance math. Legal sanctions text outranks market rumor on “still flowing.”

## Anti-patterns

- AIS-only “Yamal sailing” without sanctions-list check.
- Assuming summer NSR always open for energy schedules.
- Conflating pipeline gas sanctions with LNG project status.

## Related playbooks

- energy_sanctions_compliance.md
- russia_oil_exports.md
- lng_global_supply.md
- europe_gas_storage_ttf.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
