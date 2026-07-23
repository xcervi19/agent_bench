# Kuwait / Qatar oil and gas

**Commodity:** crude | LNG | gas  
**Geography:** Kuwait; Qatar (Ras Laffan / North Field)  
**Last reviewed:** 2026-07-23  

## Executive summary

Kuwait is a core OPEC+ crude exporter via KPC; Qatar is the LNG heavyweight via QatarEnergy/Ras Laffan. Scan must catch first: kpc.com.kw and moo.gov.kw for Kuwait barrels; qatarenergy.qa and mme.gov.qa for LNG/policy; Mwani/KPA for port continuity; Hormuz risk for both Gulf exporters.

## Price drivers (trader lens)

1. Kuwait OPEC+ compliance and KPC export program changes.
2. Qatar North Field / Ras Laffan train availability and expansion timing.
3. Hormuz transit risk on Kuwait crude and Qatar LNG.
4. Asian term LNG renegotiations and spot tender cadence (Qatar).
5. Gulf weather and port restrictions (KPA / Mwani).

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| Kuwait Petroleum Corporation (KPC) | Kuwait NOC | Kuwait Petroleum Corporation (KPC) |
| Ministry of Oil | Kuwait policy | Ministry of Oil (moo.gov.kw) |
| Kuwait Ports Authority (KPA) | Kuwait ports | Kuwait Ports Authority (KPA) |
| QatarEnergy | Qatar NOC / LNG | QatarEnergy |
| Ministry of Energy and Industry | Qatar policy | Ministry of Energy and Industry |
| Mwani Qatar | Qatar ports | Mwani Qatar |
| Ministry of Foreign Affairs | Kuwait / Qatar diplomacy | mofa.gov.kw / mofa.gov.qa |
| OPEC | Kuwait quota | OPEC |
| GECF | Gas exporter forum | GECF |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| Kuwait Petroleum Corporation (KPC) | kpc.com.kw | Production / export / FM | P1 |
| Ministry of Oil | moo.gov.kw | Oil policy; OPEC+ framing | P1 |
| Kuwait Ports Authority (KPA) | kpa.gov.kw | Port/export logistics | P1 |
| Ministry of Foreign Affairs | mofa.gov.kw | Kuwait security diplomacy | P2 |
| QatarEnergy | qatarenergy.qa | Ras Laffan / North Field / LNG offtake | P1 |
| Ministry of Energy and Industry | mme.gov.qa | Qatar energy policy | P1 |
| Mwani Qatar | mwani.com.qa | Port status | P2 |
| Ministry of Foreign Affairs | mofa.gov.qa | Qatar diplomacy | P2 |
| OPEC | opec.org | Kuwait in OPEC+ tables | P1 |
| GECF | gecf.org | Gas exporter narrative | P2 |
| UKMTO (Maritime Trade Ops) | ukmto.org | Gulf maritime risk | P1 |
| IEA | iea.org | LNG/gas balance context | P2 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

Kuwait crude loads from Gulf terminals under Hormuz risk. Qatar LNG concentrates at Ras Laffan with the same strait exposure — detail in qatar_ras_laffan_lng and strait_of_hormuz. Dual coverage in one playbook because desks often monitor both as Gulf OPEC+/GECF peers.

## Geopolitical triggers

- Kuwait FM or OPEC+ compensation cut.
- QatarEnergy force majeure / train trip.
- Hormuz escalation.
- Gulf diplomatic crisis involving either capital.
- Major Asian buyer contract restructuring with Qatar.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| KPC / QatarEnergy releases | event-driven | Gulf time |
| OPEC MOMR | monthly | Mid-month |
| mme.gov.qa / moo.gov.kw | event-driven | Local |
| UKMTO | event-driven | As issued |

## Tier 2 context sources

GECF outlooks; IEA gas reports. Secondary to NOC/ministry primaries.

## Anti-patterns

- Mixing Kuwait crude outages into Qatar LNG balances without checking.
- Unofficial North Field “delay” rumors without qatarenergy.qa.
- Ignoring Hormuz as shared risk factor.

## Related playbooks

- qatar_ras_laffan_lng.md
- opec_plus_policy.md
- strait_of_hormuz.md
- lng_global_supply.md
- saudi_arabia_oil.md

## Changelog

- 2026-07-23 — initial draft; RAG unavailable (rag_adhoc unreachable from authoring host) — drafted from whitelist + desk logic
