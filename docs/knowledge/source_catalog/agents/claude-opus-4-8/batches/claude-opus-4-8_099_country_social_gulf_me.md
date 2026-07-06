# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_099_country_social_gulf_me.md  
**Fáze:** country_social — klastr Gulf/Middle East (Fáze 4)  
**Datum:** 2026-07-06  

---

## Metodika Fáze 4 (platí pro všechny klastry 099-103)

9 social rolí × 64 zemí = 576 slotů. **Anti-halucinace: nevymýšlím konkrétní X/Telegram handly.**
Vyplňuji jen **smysluplné** sloty:
- `official_social_mfa|ministry|noc` → `unverified` ukazatel na již katalogizovanou oficiální entitu
  (poznámka „verify handle"), `proposed` jen když je kanál = oficiální news/domain (SHANA, Libya NOC).
- `sanctions_tracker` → `proposed` pro IR/RU/VE/US (UANI, TankerTrackers, OFAC, price-cap monitors).
- `local_field_reporter` → `proposed` jen desk-důvěryhodné (Rudaw IQ); jinak `unverified`/`empty`.
- **Ostatní role = `empty` implicitně přes dimension matrix** (neenumerováno kvůli objemu).

## Klastr: SA, IR, IQ, RU (+ US), AE, KW, QA, OM

| země | klíčové sloty | status |
|------|---------------|--------|
| SA | mfa, ministry, noc (Aramco), producer_rhetoric | unverified |
| IR | ministry+noc = **SHANA (proposed)**, sanctions_tracker **UANI (proposed)** | mix |
| IQ | ministry, noc (SOMO), **Rudaw local (proposed)** | mix |
| RU | mfa, ministry, noc, **sanctions_tracker price-cap (proposed)** | mix |
| AE/KW/QA/OM | noc (ADNOC/KPC/QatarEnergy/PDO-OQ) + mfa | unverified |

`last_batch_seq: 99`
