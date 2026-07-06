# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_007_country_authority_US.md  
**Fáze:** country_authority — krok US (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

USA (`US`), 10 slotů autorit (`ca-US-{authority}`). Strukturálně odlišné: **žádný NOC**
(soukromé IOCs), a burzy už pokryty globální vrstvou (CME) → 2 sloty `empty` odkazem, ne
halucinací. Trading signály: **SPR** (DOE), **shale produkce** (EIA 914/DPR), **LNG export
autorizace** (DOE FECM + FERC), **Gulf hurricane shut-ins**. Sankce běží přes **Treasury OFAC**
(ne State). 7 `proposed`, 2 `empty`, 1 `proposed` s expanzními poznámkami. Do whitelistu nezapisuji.

---

### Navržené / aktualizované sloty

| id | country | authority_type | entity | domain | category | type | signals | status |
|----|---------|----------------|--------|--------|----------|------|---------|--------|
| ca-US-ministry_petroleum | US | ministry_petroleum | US Dept of Energy (DOE) | energy.gov | government_regulator | official | storage_levels, production, export_license | proposed |
| ca-US-noc | US | noc | — | — | — | — | — | empty |
| ca-US-mfa | US | mfa | US Dept of State | state.gov | diplomacy | official | sanctions | proposed |
| ca-US-customs_export | US | customs_export | Customs & Border Protection (CBP) | cbp.gov | government_regulator | official | exports, export_license | proposed |
| ca-US-upstream_regulator | US | upstream_regulator | BSEE (offshore safety) | bsee.gov | government_regulator | official | production, force_majeure | proposed |
| ca-US-port_maritime_authority | US | port_maritime_authority | MARAD (Maritime Admin) | maritime.dot.gov | infrastructure | official | vessel_loading, port_closure | proposed |
| ca-US-national_exchange | US | national_exchange | — (covered by global CME) | — | — | — | — | empty |
| ca-US-central_bank | US | central_bank | Federal Reserve | federalreserve.gov | government_regulator | official | — | proposed |
| ca-US-environment_regulator | US | environment_regulator | EPA | epa.gov | government_regulator | official | refinery_outage | proposed |
| ca-US-coast_guard_navy | US | coast_guard_navy | US Coast Guard | uscg.mil | government_regulator | official | port_closure, force_majeure | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-US-ministry_petroleum (DOE) | shale produkce (EIA), SPR release/refill | energy diplomacy, LNG export policy | SPR sites | proposed — SPR & FECM LNG auth klíčové |
| ca-US-mfa (State) | — | sankce koordinace | — | proposed — ale enforcement = OFAC (Treasury) |
| ca-US-customs_export (CBP) | export objemy | export controls (BIS) | — | proposed — LNG auth přes DOE FECM/FERC |
| ca-US-upstream_regulator (BSEE) | offshore produkce, GoM | — | Gulf platform safety/shut-in | proposed — BOEM/FERC jako expanze |
| ca-US-coast_guard_navy (USCG) | — | — | port closures (hurricane), waterway | proposed — NAVCEN už v global shipping |
| ca-US-noc | — | — | — | empty — USA nemá NOC (IOCs soukromé, API v global) |

---

### Unverified / Anti-patterns / poznámky

- **`ca-US-noc` = empty:** USA nemá národní ropnou společnost; produkci sledovat přes EIA
  (global) + API (global) + soukromé IOCs (mimo whitelist autorit).
- **`ca-US-national_exchange` = empty:** pokryto globální vrstvou `gl-exchange-001` (CME/NYMEX,
  WTI, Henry Hub) — neduplikovat.
- **Klíčové expanzní sub-entity** (nemíchat, přidat v granularitě):
  - `ca-US-upstream_regulator__ferc` (ferc.gov) — interstate pipelines, LNG terminal siting
  - `ca-US-upstream_regulator__boem` (boem.gov) — offshore leasing
  - `ca-US-ministry_petroleum__fecm` (energy.gov/fecm) — LNG export authorizations
  - `ca-US-customs_export__bis` (bis.doc.gov) — export controls
  - `ca-US-mfa__ofac` (ofac.treasury.gov) — **sankční enforcement** (ne State)
- Anti-pattern: Baker Hughes rig count / private analytics jako „US authority" — cenné, ale
  komerční; State Dept jako sankční enforcement (to je OFAC/Treasury).

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 6,
  "last_country": "US",
  "crosscheck_cursor": 0,
  "last_batch_seq": 7
}
```

Po merge → **další dávka:** `claude-opus-4-8_008_country_authority_AE.md`
(Fáze 2, šestá země `AE` = UAE: MoEI, ADNOC, MoFA, Federal Customs, ADNOC upstream,
Fujairah/Abu Dhabi ports, ICE Futures Abu Dhabi (Murban), CBUAE, env, navy; Murban benchmark
& Fujairah bunkering signál).
