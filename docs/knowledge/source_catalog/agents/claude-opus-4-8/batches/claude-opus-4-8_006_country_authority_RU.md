# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_006_country_authority_RU.md  
**Fáze:** country_authority — krok RU (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Rusko (`RU`), 10 slotů autorit (`ca-RU-{authority}`). Nejvíc obsazená země zatím — Rusko má
funkční upstream regulátor (**Rosnedra**) i komoditní burzu (**SPIMEX**). Trading kontext:
**G7 price cap ($60), Urals discount k Brentu, ESPO do Asie, shadow fleet**. Oficiální customs
data **utajena od 2022** → toky se ověřují přes importní customs (CN/IN) + AIS. Rusko není jeden
NOC: Rosneft (ropa), Transneft (export pipeline logistika), Gazprom (plyn) — flaguji jako expanze.
9 `proposed`, 1 `empty`. Do `source_whitelist.json` nezapisuji.

---

### Navržené / aktualizované sloty

| id | country | authority_type | entity | domain | category | type | signals | status |
|----|---------|----------------|--------|--------|----------|------|---------|--------|
| ca-RU-ministry_petroleum | RU | ministry_petroleum | Ministry of Energy (Minenergo) | minenergo.gov.ru | government_regulator | official | production, export_license, quota_rhetoric | proposed |
| ca-RU-noc | RU | noc | Rosneft | rosneft.com | noc | official | production, exports, term_contract | proposed |
| ca-RU-mfa | RU | mfa | Ministry of Foreign Affairs (MID) | mid.ru | diplomacy | official | sanctions | proposed |
| ca-RU-customs_export | RU | customs_export | Federal Customs Service (FCS) | customs.gov.ru | government_regulator | official | exports, export_license | proposed |
| ca-RU-upstream_regulator | RU | upstream_regulator | Rosnedra (Subsoil Use Agency) | rosnedra.gov.ru | government_regulator | official | production | proposed |
| ca-RU-port_maritime_authority | RU | port_maritime_authority | Rosmorport | rosmorport.ru | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-RU-national_exchange | RU | national_exchange | SPIMEX (SPb Int'l Mercantile Exchange) | spimex.com | exchange | official | pricing_formula, storage_levels | proposed |
| ca-RU-central_bank | RU | central_bank | Bank of Russia (CBR) | cbr.ru | government_regulator | official | sanctions | proposed |
| ca-RU-environment_regulator | RU | environment_regulator | Rosprirodnadzor | rpn.gov.ru | government_regulator | official | refinery_outage | proposed |
| ca-RU-coast_guard_navy | RU | coast_guard_navy | Russian Navy / FSB Border Service | — | diplomacy | official | port_closure | empty |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-RU-ministry_petroleum | produkce, OPEC+ kvóta, refining | price cap reakce, export daně | — | proposed |
| ca-RU-noc (Rosneft) | produkce, upstream | největší producent, sankce | Transneft export nodes | proposed — Transneft/Gazprom jako expanze |
| ca-RU-mfa (MID) | — | sankce, price cap rétorika | — | proposed |
| ca-RU-customs_export (FCS) | export objemy | **data utajena od 2022** | — | proposed — čísla nedostupná, cross-check CN/IN customs + AIS |
| ca-RU-upstream_regulator (Rosnedra) | licence, produkce | — | — | proposed |
| ca-RU-national_exchange (SPIMEX) | domácí bilance produktů | — | domestic fuel pricing, export benchmark | proposed — relevantnější než akciová burza |
| ca-RU-port_maritime_authority | — | — | Novorossiysk / Primorsk / Ust-Luga / Kozmino | proposed |

---

### Unverified / Anti-patterns / poznámky

- **`ca-RU-coast_guard_navy` = empty:** bez použitelného oficiálního webu; Black Sea / Baltic
  transit riziko sledovat přes MFA + port authority + AIS.
- **Sankční kontext (kritické):** FCS export data **utajena od 2022**; oficiální ruské zdroje
  = policy/rétorika, ne volume truth. Skutečné toky: importní customs (China GAC, India DGCIS),
  AIS, ESPO/Urals spready. Shadow fleet & STS obchází price cap.
- **Expanzní sub-entity NOC** (nemíchat): `ca-RU-noc__transneft` (transneft.ru — export pipeline
  logistika, klíčové pro Druzhba/ESPO outage), `ca-RU-noc__gazprom` (gazprom.com — plyn),
  `ca-RU-noc__gazprom_neft`, `ca-RU-noc__novatek` (novatek.ru — LNG Yamal). Rosneft ≠ celý ruský export.
- Anti-pattern: brát ruská oficiální export čísla jako pravdivá; Moscow Exchange (moex.com) je
  finanční, ne komoditní pro ropu — proto SPIMEX ve slotu exchange.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 5,
  "last_country": "RU",
  "crosscheck_cursor": 0,
  "last_batch_seq": 6
}
```

Po merge → **další dávka:** `claude-opus-4-8_007_country_authority_US.md`
(Fáze 2, pátá země `US` = United States: DOE/EIA, žádný NOC (IOCs/API), State Dept, CBP,
BOEM/BSEE upstream, USACE/port authorities, NYMEX/CME, Fed, EPA, USCG; SPR & shale signál).
