# Ecuador Amazon pipelines

**Commodity:** crude  
**Geography:** Ecuador — Amazon upstream / Pacific export  
**Last reviewed:** 2026-07-23  

## Executive summary

Ecuador’s Amazon production depends on pipeline integrity to Pacific terminals; ruptures, protests, and environmental stoppages quickly cut Oriente/Napo-class exports. Scan must catch first: petroecuador.ec, recursosyenergia.gob.ec, ambiente.gob.ec (Yasuní context), and armada.mil.ec for coastal/export security.

## Price drivers (trader lens)

1. Pipeline ruptures / force majeure on Amazon–coast systems.
2. Environmental and indigenous protest stoppages.
3. Yasuní / block policy decisions (ambiente.gob.ec notes).
4. Petroecuador operational and fiscal constraints.
5. Pacific export weather and Navy security posture.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Petroecuador | NOC | Petroecuador |
| Ministry of Energy and Non-Renewable Natural Resources | Energy policy | Ministry of Energy and Non-Renewable Natural Resources |
| Ministry of Environment | Environment / Yasuní | Ministry of Environment |
| Ecuadorian Navy | Maritime / coastal security | Ecuadorian Navy |
| Central Bank of Ecuador | Macro/oil revenue | Central Bank of Ecuador |
| Ministry of Foreign Affairs | Diplomacy | Ministry of Foreign Affairs (cancilleria.gob.ec) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Petroecuador | petroecuador.ec | Production; pipeline FM; export status | P1 |
| Ministry of Energy and Non-Renewable Natural Resources | recursosyenergia.gob.ec | Upstream / export policy | P1 |
| Ministry of Environment | ambiente.gob.ec | Yasuní block 43 / environmental stoppages | P1 |
| Ecuadorian Navy | armada.mil.ec | Pacific coast / port security; tanker coordination notes | P2 |
| Central Bank of Ecuador | bce.fin.ec | Oil revenue / macro | P3 |
| Ministry of Foreign Affairs | cancilleria.gob.ec | Diplomatic framing | P3 |
| EIA | eia.gov | Ecuador in balances | P2 |
| OPEC | opec.org | Ecuador history/context in oil politics | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Amazon fields feed pipelines over the Andes to Pacific export terminals; single-point pipeline failures dominate outage risk. Environmental policy (Yasuní) can remove barrels structurally. FLOPEC/tanker notes appear in Navy whitelist commentary.

## Geopolitical triggers

- Confirmed pipeline rupture FM.
- Protest-driven production halt.
- Yasuní / licensing referendum or ministry ban.
- Coastal security incident affecting loadings.
- Fiscal crisis limiting diluent/ops spend.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Petroecuador / ministries | event-driven | Ecuador time |
| Environment notices | event-driven | Local |

## Tier 2 context sources

BCE macro; MFA. Pipeline FM notices are the scan priority.

## Anti-patterns

- Social protest videos without Petroecuador FM confirmation.
- Treating every Amazon spill rumor as export halt.
- Ignoring ambiente.gob.ec on Yasuní structural risk.

## Related playbooks

- colombia_atlantic_exports.md
- mexico_maya_crude.md
- crude_oil_global.md
- panama_malacca_routes.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
