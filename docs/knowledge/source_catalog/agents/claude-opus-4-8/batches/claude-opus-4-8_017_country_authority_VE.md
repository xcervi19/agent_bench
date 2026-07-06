# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_017_country_authority_VE.md  
**Fáze:** country_authority — krok VE (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Venezuela (`VE`), 10 slotů (`ca-VE-{authority}`). **Silné sankce** (OFAC; Chevron licence GL),
kolaps a částečné oživení produkce, **Orinoco heavy crude**, Jose terminal. Oficiální data
**extrémně neprůhledná** → cross-check přes OPEC sekundární zdroje + AIS. Vládní weby nestabilní →
hodně `unverified`. 4 `proposed`, 4 `unverified`, 2 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-VE-ministry_petroleum | ministry_petroleum | Ministry of Petroleum (MinPetróleo) | minpet.gob.ve | government_regulator | official | production, export_license | unverified |
| ca-VE-noc | noc | PDVSA | pdvsa.com | noc | official | production, exports, sanctions | proposed |
| ca-VE-mfa | mfa | Ministry of Foreign Affairs (Cancillería) | mppre.gob.ve | diplomacy | official | sanctions | proposed |
| ca-VE-customs_export | customs_export | SENIAT | seniat.gob.ve | government_regulator | official | exports | unverified |
| ca-VE-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-VE-port_maritime_authority | port_maritime_authority | INEA (Espacios Acuáticos) | inea.gob.ve | infrastructure | official | vessel_loading, port_closure | unverified |
| ca-VE-national_exchange | national_exchange | Bolsa de Valores de Caracas | bolsadecaracas.com | exchange | official | pricing_formula | unverified |
| ca-VE-central_bank | central_bank | Banco Central de Venezuela (BCV) | bcv.org.ve | government_regulator | official | sanctions | proposed |
| ca-VE-environment_regulator | environment_regulator | Ministry of Ecosocialism (MINEC) | minec.gob.ve | government_regulator | official | refinery_outage | unverified |
| ca-VE-coast_guard_navy | coast_guard_navy | Venezuelan Navy | — | diplomacy | official | port_closure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-VE-noc (PDVSA) | produkce (oficiální nespolehlivá) | OFAC sankce, Chevron GL | Jose terminal, Orinoco upgraders | proposed — data cross-check nutný |
| ca-VE-mfa | — | sankční úlevy vs. volby, US jednání | — | proposed — klíč pro licence signál |

### Unverified / Anti-patterns / poznámky

- **Sankční kontext (kritické):** OFAC licence (Chevron GL 41/následné) = hlavní price/volume signál;
  oficiální VE data nespolehlivá — cross-check OPEC MOMR secondary sources + AIS (Jose loadings).
- **Unverified domény** (nestabilní vládní weby): MinPetróleo, SENIAT, INEA, MINEC, Bolsa Caracas.
- **`upstream_regulator` = empty:** integrováno pod PDVSA/ministerstvo.
- **`coast_guard_navy` = empty:** bez použitelného webu.
- Anti-pattern: brát venezuelská oficiální produkční čísla jako pravdivá; sledovat Chevron/OFAC + AIS.

### Progress po merge

`last_country: VE`, `last_batch_seq: 17`
