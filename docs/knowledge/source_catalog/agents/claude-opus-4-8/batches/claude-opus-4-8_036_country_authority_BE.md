# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_036_country_authority_BE.md  
**Fáze:** country_authority — krok BE (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Belgie (`BE`), 10 slotů (`ca-BE-{authority}`). Součást **ARA hubu** (Antverpy = petchem/rafinace) +
**Zeebrugge LNG** (Fluxys, gas transit/reload hub). Žádný NOC. 7 `proposed`, 1 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-BE-ministry_petroleum | ministry_petroleum | FPS Economy | economie.fgov.be | government_regulator | official | imports | proposed |
| ca-BE-noc | noc | — | — | — | — | — | empty |
| ca-BE-mfa | mfa | FPS Foreign Affairs | diplomatie.belgium.be | diplomacy | official | sanctions | proposed |
| ca-BE-customs_export | customs_export | Belgian Customs (FPS Finance) | financien.belgium.be | government_regulator | official | imports, exports | proposed |
| ca-BE-upstream_regulator | upstream_regulator | CREG (energy regulator) | creg.be | government_regulator | official | pricing_formula | proposed |
| ca-BE-port_maritime_authority | port_maritime_authority | Port of Antwerp-Bruges | portofantwerpbruges.com | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-BE-national_exchange | national_exchange | — (TTF/ICE) | — | — | — | — | empty |
| ca-BE-central_bank | central_bank | National Bank of Belgium | nbb.be | government_regulator | official | sanctions | proposed |
| ca-BE-environment_regulator | environment_regulator | Regional (Flanders/Wallonia) | — | government_regulator | official | refinery_outage | unverified |
| ca-BE-coast_guard_navy | coast_guard_navy | — | — | — | — | — | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-BE-port_maritime_authority (Antwerp-Bruges) | — | EU import gateway | **ARA petchem/refining; Zeebrugge LNG** | proposed |
| ca-BE-upstream_regulator (CREG) | — | — | gas market oversight | proposed — Fluxys jako expanze |

### Unverified / poznámky

- **`ca-BE-noc` = empty; `national_exchange` = empty** (gas na TTF/ICE).
- **Fluxys** (fluxys.com) — provozovatel Zeebrugge LNG + tranzitní plynovody; klíčová expanze (gas reload hub, dřív ruský LNG transhipment).
- Antverpy = součást ARA (`ara` geo Fáze 3).
- Environment regionální (Flanders VMM / Wallonia) → `unverified`.

### Progress po merge

`last_country: BE`, `last_batch_seq: 36`
