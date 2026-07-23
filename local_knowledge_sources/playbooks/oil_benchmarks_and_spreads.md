# Oil benchmarks and spreads

**Commodity:** crude  
**Geography:** global (WTI, Brent, Murban, OSP-linked)  
**Last reviewed:** 2026-07-23  

## Executive summary

Benchmarks translate physical tightness into futures and differentials: WTI (CME/Cushing), Brent (ICE), Murban (ICE Endex / ADNOC system), and Middle East OSPs (Aramco). Scan must catch first: exchange settlements and contract notices, EIA stocks at Cushing/USGC, Aramco/ADNOC official selling differentials, and logistics that break arb (pipelines, waterborne freight, chokepoints).

## Price drivers (trader lens)

1. Cushing inventory and WTI delivery mechanics (EIA + CME).
2. North Sea / Atlantic Brent complex supply and ICE expiry dynamics.
3. Dubai/Murban / OSP differentials into Asia.
4. Time spreads (contango/backwardation) signaling storage economics.
5. Quality and freight differentials (light sweet vs heavy; Atlantic vs Pacific).

## Key entities

| Entity | Role | Whitelist ref |
|--------|------|---------------|
| CME Group | WTI / NYMEX | CME Group |
| ICE | Brent | ICE |
| ICE Endex (Amsterdam) | Murban / related | ICE Endex (Amsterdam) |
| EIA | Stocks / WPSR | EIA |
| Saudi Aramco | OSP | Saudi Aramco |
| ADNOC | Murban / UAE grades | ADNOC |
| DME / Gulf Mercantile | Gulf mercantile exchange | DME / Gulf Mercantile |
| Cushing tank farm terminals | WTI delivery storage | Cushing tank farm terminals |

## Primary Official Sources

| Entity | Domain | What to watch | Scan priority |
|--------|--------|---------------|---------------|
| CME Group | cmegroup.com | WTI settlements; delivery notices; contract specs | P1 |
| ICE | ice.com | Brent settlements; expiry / EFP | P1 |
| ICE Endex (Amsterdam) | theice.com | Murban benchmark pricing | P1 |
| EIA | eia.gov | Cushing and PADD stocks; WPSR | P1 |
| Saudi Aramco | aramco.com | Monthly OSP differentials | P1 |
| ADNOC | adnoc.ae | Murban OSP / production quality signals | P1 |
| DME / Gulf Mercantile | dubaimerc.com | Gulf contract / settlement context | P2 |
| Cushing tank farm terminals | enterpriseproducts.com | Cushing terminal / tank ops context | P2 |
| SGX | sgx.com | Asia paper/hedging context (Tier 2) | P3 |

## Official Social Media

| Entity | Handle / URL | Platform | Why faster than web |
|--------|--------------|----------|---------------------|
| — | — | — | No verified official social handles in `source_whitelist.json`; leave empty until validated |

## Infrastructure & logistics

WTI physical delivery centers on Cushing, Oklahoma storage and pipelines. Brent is waterborne North Sea-linked paper with global freight arb. Murban/UAE grades load Arabian Gulf / Fujairah logistics. Spreads move when pipelines, export docks, or chokepoints change effective deliverability — see cushing_wti_delivery, fujairah_storage_hub, north_sea_crude.

## Geopolitical triggers

- SPR release/refill altering USGC–Cushing balances (energy.gov / EIA).
- Red Sea / Hormuz risk repricing East-of-Suez differentials vs Atlantic.
- Sanctions narrowing Russian grade discounts vs Brent.
- ADNOC or Aramco OSP shock to Asia refining margins.
- Exchange position limits / delivery tender surprises.

## Data cadence

| Source | Frequency | Typical release time (UTC) |
|--------|-----------|----------------------------|
| EIA WPSR | weekly | Wed ~15:30 US-linked |
| CME / ICE settlements | daily | Exchange close |
| Aramco OSP | monthly | Early month |
| ADNOC Murban signals | monthly / event | adnoc.ae |

## Tier 2 context sources

SGX for Asia hedge context; DME pages for Gulf contract literacy. Do not substitute for CME/ICE settlements or official OSP posts.

## Anti-patterns

- Citing unofficial “Dubai assessment” blogs as OSP.
- Conflating ICE Brent with WTI without basis context.
- Ignoring Cushing stocks when trading WTI calendar spreads.
- Using retail CFDs as evidence of physical differential moves.

## Related playbooks

- crude_oil_global.md
- cushing_wti_delivery.md
- uae_oil_fujairah.md
- saudi_arabia_oil.md
- north_sea_crude.md
- fujairah_storage_hub.md

## Changelog

- 2026-07-23 — initial draft
