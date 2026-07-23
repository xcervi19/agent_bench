# Ukraine energy war

**Commodity:** gas | crude | products  
**Geography:** Ukraine — energy infrastructure / transit remnant  
**Last reviewed:** 2026-07-23  

## Executive summary

Attacks on Ukrainian energy infrastructure and the end of Russian gas transit reshape EU gas risk and regional oil product logistics. Scan must catch first: naftogaz.com (transit ended / UGS notes), mev.gov.ua, mfa.gov.ua, customs.gov.ua, and EU/GIE/ENTSOG for spillover into TTF.

## Price drivers (trader lens)

1. Strikes on generation, transmission, or UGS-related assets.
2. Naftogaz / GTS transit status (whitelist: transit ended 2025 note).
3. EU storage and ENTSOG rerouting after lost transit.
4. Ukrainian import logistics for fuels under wartime customs.
5. Escalation risk premium on Black Sea energy shipping.

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Naftogaz | NOC / UGS / transit context | Naftogaz |
| Ministry of Energy | Ukraine energy | Ministry of Energy (mev.gov.ua) |
| Ministry of Foreign Affairs | Diplomacy | Ministry of Foreign Affairs (mfa.gov.ua) |
| State Customs Service | Wartime trade data | State Customs Service |
| National Bank of Ukraine | Macro | National Bank of Ukraine |
| Gas Infrastructure Europe | EU storage spillover | Gas Infrastructure Europe |
| ENTSOG | EU flows | ENTSOG |
| EU Energy | Policy | EU Energy |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Naftogaz | naftogaz.com | UGS; transit status; infra damage framing | P1 |
| Ministry of Energy | mev.gov.ua | Grid/fuel emergency measures | P1 |
| Ministry of Foreign Affairs | mfa.gov.ua | War diplomacy / energy appeals | P1 |
| State Customs Service | customs.gov.ua | Wartime import declarations (partial) | P2 |
| National Bank of Ukraine | bank.gov.ua | Macro/FX wartime signal | P3 |
| Ministry of Environmental Protection and Natural Resources | mepr.gov.ua | Env/damage context | P3 |
| Gas Infrastructure Europe | gie.eu | EU storage response | P1 |
| ENTSOG | entsog.eu | Flow reconfiguration | P1 |
| EU Energy | energy.ec.europa.eu | Emergency gas measures | P1 |
| ICE | ice.com | TTF | P1 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Black Sea maritime risk if relevant | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Ukrainian UGS historically mattered for EU winter; whitelist notes Russian transit ended 2025 with GTS Operator expansion reference — treat transit as closed unless official restart. Attacks on power/gas assets create domestic fuel crises with secondary product import demand. See europe_gas_storage_ttf and nord_stream_alternatives_eu.

## Geopolitical triggers

- Mass strike on energy infrastructure ahead of winter.
- Official change to transit/UGS export policy.
- EU emergency measures responding to Ukrainian infra loss.
- Black Sea port export/import shock.
- Escalation involving nuclear plant risk (monitor via MFA/ministry — not rumor).

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| Naftogaz / mev.gov.ua / MFA | event-driven | Ukraine time |
| GIE / ENTSOG / ICE | daily / continuous | EU |
| Customs | partial / event | Local |

## Tier 2 context sources

NBU macro; MEPR. Wartime data gaps are expected — do not invent missing GTS domains beyond whitelist.

## Anti-patterns

- Telegram channel damage claims without ministry/Naftogaz confirmation.
- Assuming transit still flows after official end notes.
- Pricing TTF only on Ukraine headlines without GIE/ENTSOG check.

## Related playbooks

- europe_gas_storage_ttf.md
- nord_stream_alternatives_eu.md
- energy_sanctions_compliance.md
- turkish_straits_bospor.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
