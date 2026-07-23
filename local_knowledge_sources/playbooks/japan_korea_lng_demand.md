# Japan / Korea LNG demand

**Commodity:** LNG  
**Geography:** Japan; South Korea  
**Last reviewed:** 2026-07-23  

## Executive summary

Japan and Korea are premium LNG term buyers; METI/JOGMEC and MOTIE/customs signals move JKM and term renegotiations. Scan must catch first: meti.go.jp (ANRE/JCC notes), jogmec.go.jp, motie.go.kr, customs.go.kr, and MFA diplomacy.

## Price drivers (trader lens)

1. Nuclear/power-burn switching vs LNG restocking (Japan).
2. Korea industrial/power LNG demand and customs import prints.
3. Term contract renegotiations and spot tender cadence.
4. Weather (heating/cooling) extremes.
5. Competition with Europe for Atlantic/Pacific cargoes.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Agency for Natural Resources and Energy (ANRE) | Japan energy policy / JCC | Agency for Natural Resources and Energy (ANRE) |
| JOGMEC | Stockpiling / upstream support | JOGMEC |
| Ministry of Foreign Affairs | Japan diplomacy | Ministry of Foreign Affairs (mofa.go.jp) |
| MOTIE (Ministry of Trade, Industry and Energy) | Korea energy | MOTIE (Ministry of Trade, Industry and Energy) |
| Korea Customs Service | Import data | Korea Customs Service |
| Ministry of Foreign Affairs | Korea diplomacy | Ministry of Foreign Affairs (mofa.go.kr) |
| IEA | Gas balances | IEA |
| ICE | TTF arb context | ICE |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Agency for Natural Resources and Energy (ANRE) | meti.go.jp | JCC; monthly oil/LNG statistics; policy | P1 |
| JOGMEC | jogmec.go.jp | Stockpiling / security of supply | P1 |
| Ministry of Foreign Affairs | mofa.go.jp | Energy diplomacy | P2 |
| MOTIE (Ministry of Trade, Industry and Energy) | motie.go.kr | Korea energy policy | P1 |
| Korea Customs Service | customs.go.kr | Crude/LNG import data by source | P1 |
| Ministry of Foreign Affairs | mofa.go.kr | Korea diplomacy | P2 |
| IEA | iea.org | NE Asia gas outlook | P1 |
| EIA | eia.gov | LNG trade context | P2 |
| ICE | ice.com | TTF for arb | P2 |
| GECF | gecf.org | Producer narrative | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Multiple Japanese and Korean regas terminals clear Qatar, Australia, US, and other LNG. Term contracts dominate; spot tops up weather/nuclear gaps. See qatar_ras_laffan_lng, australia_lng_nws_gorgon, us_lng_gulf_terminals.

## Geopolitical triggers

- Nuclear restart/delay shifting Japan LNG.
- Cold winter restock panic.
- Sanctions compliance change on Russian LNG offtake.
- Strike/outage at a major regas hub.
- Sudden Europe–Asia price arb flip.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| METI/ANRE stats | monthly | Japan time |
| Korea Customs | monthly | Korea time |
| MOTIE / JOGMEC | event + periodic | Local |
| IEA | outlook | As published |

## Tier 2 context sources

GECF; MFA framing. METI/MOTIE/customs are demand primaries.

## Anti-patterns

- Pricing JKM only from European TTF without NE Asia official stats.
- Unofficial utility Telegram tenders as confirmed awards.
- Ignoring nuclear schedule in Japan LNG models.

## Related playbooks

- lng_global_supply.md
- qatar_ras_laffan_lng.md
- australia_lng_nws_gorgon.md
- europe_gas_storage_ttf.md
- china_oil_gas_imports.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
