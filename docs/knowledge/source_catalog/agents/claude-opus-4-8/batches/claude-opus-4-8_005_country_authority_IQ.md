# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_005_country_authority_IQ.md  
**Fáze:** country_authority — krok IQ (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-05  

---

## Shrnutí

Irák (`IQ`), 10 slotů autorit (`ca-IQ-{authority}`). Klíčový trading nuance: **federal
(SOMO / Basra Oil Co) vs. KRG (Kurdistan)** export split — KRG export přes Ceyhan (ITP
pipeline) je od 2023 přerušen, což je opakovaný price/flow signal. **SOMO** je hlavní
exportní marketer (Basra Medium/Heavy OSP do Asie/Evropy). 6 `proposed`, 3 `unverified`,
1 `empty`. KRG MNR flaguji jako expanzní sub-entitu. Do `source_whitelist.json` nezapisuji.

---

### Navržené / aktualizované sloty

| id | country | authority_type | entity | domain | category | type | signals | status |
|----|---------|----------------|--------|--------|----------|------|---------|--------|
| ca-IQ-ministry_petroleum | IQ | ministry_petroleum | Ministry of Oil | oil.gov.iq | government_regulator | official | production, export_license, refinery_outage | proposed |
| ca-IQ-noc | IQ | noc | SOMO (State Oil Marketing Org) | somooil.gov.iq | noc | official | exports, term_contract, pricing_formula | proposed |
| ca-IQ-mfa | IQ | mfa | Ministry of Foreign Affairs | mofa.gov.iq | diplomacy | official | sanctions | proposed |
| ca-IQ-customs_export | IQ | customs_export | General Commission of Customs | customs.mof.gov.iq | government_regulator | official | exports, export_license | unverified |
| ca-IQ-upstream_regulator | IQ | upstream_regulator | — | — | — | — | — | empty |
| ca-IQ-port_maritime_authority | IQ | port_maritime_authority | General Company for Ports of Iraq (GCPI) | iraqiports.iq | infrastructure | official | vessel_loading, port_closure | unverified |
| ca-IQ-national_exchange | IQ | national_exchange | Iraq Stock Exchange (ISX) | isx-iq.net | exchange | official | pricing_formula | proposed |
| ca-IQ-central_bank | IQ | central_bank | Central Bank of Iraq (CBI) | cbi.iq | government_regulator | official | sanctions | proposed |
| ca-IQ-environment_regulator | IQ | environment_regulator | Ministry of Environment | moen.gov.iq | government_regulator | official | refinery_outage | unverified |
| ca-IQ-coast_guard_navy | IQ | coast_guard_navy | Iraqi Navy | — | diplomacy | official | port_closure | empty |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-IQ-ministry_petroleum | produkce, OPEC+ compliance (chronicky nad kvótou) | federal-KRG spor o zdroje | — | proposed |
| ca-IQ-noc (SOMO) | Basra grades produkce | export politika, OSP | Basra/Fao terminals, Ceyhan | proposed — nejvyšší priorita IQ |
| ca-IQ-mfa | — | US přítomnost, Írán vliv, sankce | — | proposed |
| ca-IQ-port_maritime_authority | — | — | Umm Qasr / Khor al-Zubair / Basra Oil Terminal | unverified — doména GCPI k ověření |
| ca-IQ-national_exchange (ISX) | — | — | akciová burza, ne crude pricing | proposed (Tier 2, nízká relevance) |
| ca-IQ-coast_guard_navy | — | Basra offshore terminal (ABOT/KAAOT) obrana | — | empty — bez oficiálního webu |

---

### Unverified / Anti-patterns / poznámky

- **`ca-IQ-upstream_regulator` = empty:** INOC (Iraq National Oil Company) opakovaně
  navrhován, ale nefunkční jako regulátor; integrováno pod Ministry of Oil + operující IOCs.
- **`ca-IQ-coast_guard_navy` = empty:** Iraqi Navy bez použitelného oficiálního webu;
  offshore terminály (ABOT/KAAOT) sledovat přes port authority + AIS.
- **Unverified domény** (`/source-discover`): customs (`customs.mof.gov.iq`), ports
  (`iraqiports.iq`), environment (`moen.gov.iq`).
- **KRG expanze (důležité):** Kurdistan Regional Government má vlastní **Ministry of Natural
  Resources** (`mnr.krg.org` — ověřit) a export přes **Ceyhan** (ITP pipeline, halted 2023).
  Kandidát na expanzní sub-entitu `ca-IQ-noc__krg_mnr` ve fázi granularity — federal SOMO
  a KRG exporty se **nesmí míchat** (odlišné toky, právní spor, různé kupce).
- Anti-pattern: brát iráckou produkci jako kvótově disciplinovanou (chronicky over-produces);
  neuvádět KRG a federal jako jeden export stream.

---

### Progress po merge (návrh)

```json
{
  "phase": "country_authority",
  "phase_index": 4,
  "last_country": "IQ",
  "crosscheck_cursor": 0,
  "last_batch_seq": 5
}
```

Po merge → **další dávka:** `claude-opus-4-8_006_country_authority_RU.md`
(Fáze 2, čtvrtá země `RU` = Russia: Energy Ministry, Rosneft/Gazprom/Transneft, MFA,
FCS customs, ports (Novorossiysk/Primorsk/Kozmino), SPIMEX exchange, CBR, env, navy;
vysoká sankční / price-cap relevance, ESPO & Urals discount signál).
