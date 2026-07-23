# Turkmenistan / Uzbekistan gas to China

**Commodity:** gas  
**Geography:** Central Asia — China pipeline corridor  
**Last reviewed:** 2026-07-23  

## Executive summary

Central Asian pipeline gas to China (CAGP-class) is a structural China supply source; Uzbekistan transit/production and Turkmen volumes interact with CNPC offtake. Scan must catch first: mfa.gov.tm, minenergy.uz / mfa.uz / customs.uz, cnpc.com.cn, and mfa.gov.cn — without inventing missing Turkmengaz domains.

## Price drivers (trader lens)

1. Turkmen export volume changes (diplomatic/NOC signals).
2. Uzbekistan production/transit declarations (customs/energy ministry).
3. CNPC offtake / China demand (NEA/CNPC).
4. Pipeline technical outages on Central Asia–China routes.
5. Price renegotiation politics along the corridor.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Ministry of Foreign Affairs | Turkmenistan diplomacy | Ministry of Foreign Affairs (mfa.gov.tm) |
| Ministry of Energy | Uzbekistan | Ministry of Energy (minenergy.uz) |
| Ministry of Foreign Affairs | Uzbekistan | Ministry of Foreign Affairs (mfa.uz) |
| State Customs Committee | Uzbekistan customs / CAGP notes | State Customs Committee (customs.uz) |
| Central Bank of Uzbekistan | Macro | Central Bank of Uzbekistan |
| CNPC | China NOC offtaker/operator | CNPC |
| Ministry of Foreign Affairs | China | Ministry of Foreign Affairs (mfa.gov.cn) |
| National Energy Administration (NEA) | China energy | National Energy Administration (NEA) |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Ministry of Foreign Affairs | mfa.gov.tm | Turkmen energy export diplomacy | P1 |
| Ministry of Energy | minenergy.uz | Uzbekistan gas policy / production | P1 |
| Ministry of Foreign Affairs | mfa.uz | Transit diplomacy | P2 |
| State Customs Committee | customs.uz | CAGP transit declarations; LPG/product notes | P1 |
| Central Bank of Uzbekistan | cbu.uz | Macro/FX context | P3 |
| CNPC | cnpc.com.cn | Offtake / pipeline ops framing | P1 |
| Ministry of Foreign Affairs | mfa.gov.cn | China–Central Asia energy diplomacy | P2 |
| National Energy Administration (NEA) | nea.gov.cn | China gas policy / demand | P1 |
| People’s Bank of China | pbc.gov.cn | Macro Tier 2 | P3 |
| IEA | iea.org | China/Central Asia gas context | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Pipeline gas from Turkmenistan across Uzbekistan/Kazakhstan systems into China is the core route (CAGP notes on customs.uz). Whitelist lacks a dedicated Turkmengaz domain — do not invent; use MFA + Chinese offtaker/NEA. Complements china_oil_gas_imports.

## Geopolitical triggers

- Corridor price dispute or volume renegotiation.
- Uzbekistan transit restriction.
- CNPC nomination cut on China demand weakness.
- Technical rupture on Central Asia–China pipelines.
- Broader China–Central Asia diplomatic stress.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Ministries / customs | event-driven / periodic | Local |
| CNPC / NEA | event-driven | China time |
| IEA | outlook | As published |

## Tier 2 context sources

PBOC/CBU macro. Explicit gap: no Turkmengaz domain on whitelist — flag rather than fabricate.

## Anti-patterns

- Inventing turkmengaz.tm or similar not in source_whitelist.json.
- Treating all China gas imports as LNG only.
- Using secondary “Belt and Road” blogs as flow data.

## Related playbooks

- china_oil_gas_imports.md
- natural_gas_global.md
- lng_global_supply.md
- russia_oil_exports.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic; Turkmengaz domain not on whitelist
