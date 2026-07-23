# China oil and gas imports

**Commodity:** crude | LNG | gas  
**Geography:** China — seaborne crude/LNG + pipeline gas  
**Last reviewed:** 2026-07-23  

## Executive summary

China is the marginal buyer for many crude and LNG cargoes and a pipeline gas sink from Central Asia/Russia. Scan must catch first: nea.gov.cn and customs.gov.cn (GACC), cnpc.com.cn, MFA energy diplomacy, and IEA/EIA for balance context.

## Price drivers (trader lens)

1. Crude import quotas / refinery runs (teapot vs majors).
2. GACC monthly import prints by crude/LNG.
3. NEA policy on stockpiling and gas demand.
4. Pipeline gas from Central Asia/Russia vs LNG arb.
5. Sanctions-compliance choices on Iranian/Russian barrels.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| National Energy Administration (NEA) | Energy policy | National Energy Administration (NEA) |
| General Admin of Customs (GACC) | Import data | General Admin of Customs (GACC) |
| CNPC | NOC / offtake | CNPC |
| Ministry of Foreign Affairs | Diplomacy | Ministry of Foreign Affairs (mfa.gov.cn / fmprc.gov.cn) |
| Ministry of Natural Resources | Resources policy | Ministry of Natural Resources |
| People’s Bank of China | Macro/FX | People’s Bank of China |
| IEA | Balances | IEA |
| EIA | Balances | EIA |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| National Energy Administration (NEA) | nea.gov.cn | Energy policy; gas/crude demand framing | P1 |
| General Admin of Customs (GACC) | customs.gov.cn | Crude/LNG import statistics | P1 |
| CNPC | cnpc.com.cn | Upstream/trading/pipeline offtake | P1 |
| Ministry of Foreign Affairs | mfa.gov.cn | Energy diplomacy | P2 |
| Ministry of Foreign Affairs | fmprc.gov.cn | Diplomatic releases | P2 |
| Ministry of Natural Resources | mnr.gov.cn | Resource policy | P3 |
| People’s Bank of China | pbc.gov.cn | Macro/FX | P3 |
| IEA | iea.org | China in oil/gas balances | P1 |
| EIA | eia.gov | China demand/import context | P2 |
| OPEC | opec.org | Demand outlook cross-check | P2 |
| UN COMTRADE | comtrade.un.org | Bilateral lags | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Seaborne crude via eastern/southern ports; LNG terminals along the coast; pipeline gas from Central Asia and Russia. Malacca/Hormuz risk affects seaborne energy. See turkmenistan_uzbekistan_gas_cn and panama_malacca_routes.

## Geopolitical triggers

- Quota or teapot crackdown cutting crude buys.
- Sanctions secondary-risk shift on Russian/Iranian grades.
- NEA strategic stock build/release signal.
- Pipeline gas dispute with Central Asia/Russia.
- Property/industrial demand shock.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| GACC | monthly | China schedule |
| NEA / CNPC | event-driven | China time |
| IEA/EIA | monthly / outlook | As published |

## Tier 2 context sources

PBOC; Comtrade lags. GACC+NEA are the import primaries.

## Anti-patterns

- Unofficial “China buying” tanker trackers as official imports.
- Ignoring pipeline gas when modeling only LNG.
- Inventing Sinopec domains not used from whitelist.

## Related playbooks

- india_discounted_crude.md
- turkmenistan_uzbekistan_gas_cn.md
- lng_global_supply.md
- energy_sanctions_compliance.md
- panama_malacca_routes.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
