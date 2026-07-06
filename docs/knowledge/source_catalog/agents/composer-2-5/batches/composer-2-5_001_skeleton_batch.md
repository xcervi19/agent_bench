# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_001_skeleton_batch.md  
**Fáze:** skeleton — krok batch (Fáze 0, celá fáze)  
**Datum:** 2026-07-04  

---

## Shrnutí

Inicializační dávka: master seznamy všech dimenzí, konvence ID slotů, projekce kapacity (~10 400 slotů).
Žádné domény — všechny sloty `empty`. Merge do `catalog.json` až po schválení.

---

## Dim 1 — Země (64, deduplikovaný seznam)

Pořadí dle briefu; `NO` uvedeno jednou (v briefu duplicitně).

| # | code | country |
|---|------|---------|
| 1 | SA | Saudi Arabia |
| 2 | IR | Iran |
| 3 | IQ | Iraq |
| 4 | RU | Russia |
| 5 | US | United States |
| 6 | AE | UAE |
| 7 | KW | Kuwait |
| 8 | QA | Qatar |
| 9 | OM | Oman |
| 10 | NO | Norway |
| 11 | BR | Brazil |
| 12 | CA | Canada |
| 13 | MX | Mexico |
| 14 | VE | Venezuela |
| 15 | NG | Nigeria |
| 16 | AO | Angola |
| 17 | LY | Libya |
| 18 | DZ | Algeria |
| 19 | EG | Egypt |
| 20 | CN | China |
| 21 | IN | India |
| 22 | MY | Malaysia |
| 23 | ID | Indonesia |
| 24 | AU | Australia |
| 25 | KZ | Kazakhstan |
| 26 | AZ | Azerbaijan |
| 27 | TM | Turkmenistan |
| 28 | UZ | Uzbekistan |
| 29 | TR | Turkey |
| 30 | GB | United Kingdom |
| 31 | DE | Germany |
| 32 | NL | Netherlands |
| 33 | BE | Belgium |
| 34 | IT | Italy |
| 35 | FR | France |
| 36 | ES | Spain |
| 37 | PL | Poland |
| 38 | UA | Ukraine |
| 39 | YE | Yemen |
| 40 | SD | Sudan |
| 41 | SS | South Sudan |
| 42 | CO | Colombia |
| 43 | GY | Guyana |
| 44 | SN | Senegal |
| 45 | GQ | Equatorial Guinea |
| 46 | CG | Congo (Republic) |
| 47 | GA | Gabon |
| 48 | TD | Chad |
| 49 | MR | Mauritania |
| 50 | BH | Bahrain |
| 51 | IL | Israel |
| 52 | JP | Japan |
| 53 | KR | South Korea |
| 54 | SG | Singapore |
| 55 | TH | Thailand |
| 56 | VN | Vietnam |
| 57 | PK | Pakistan |
| 58 | BD | Bangladesh |
| 59 | CL | Chile |
| 60 | PE | Peru |
| 61 | EC | Ecuador |
| 62 | TT | Trinidad & Tobago |
| 63 | JM | Jamaica |
| 64 | DK | Denmark |

---

## Dim 1 — Typy autorit (10)

| id | label |
|----|-------|
| ministry_petroleum | Energy / petroleum ministry |
| noc | National oil company |
| mfa | Ministry of foreign affairs |
| customs_export | Customs / export licensing |
| upstream_regulator | Upstream regulator |
| port_maritime_authority | Port & maritime authority |
| national_exchange | National commodity exchange |
| central_bank | Central bank (FX / sanctions linkage) |
| environment_regulator | Environment / emissions regulator |
| coast_guard_navy | Coast guard / naval transit authority |

**Fáze 2 sloty:** 64 × 10 = **640** (`ca-{CC}-{authority}`)

---

## Dim 2 — Geografické cíle (32)

| id | name | subtype |
|----|------|---------|
| hormuz | Strait of Hormuz | chokepoint |
| bab_el_mandeb | Bab el-Mandeb | chokepoint |
| suez | Suez Canal | chokepoint |
| panama | Panama Canal | chokepoint |
| malacca | Strait of Malacca | chokepoint |
| bospor | Turkish Straits (Bospor) | chokepoint |
| gibraltar | Strait of Gibraltar | chokepoint |
| ras_tanura | Ras Tanura | load_port |
| fujairah | Fujairah | load_port |
| kharg | Kharg Island | load_port |
| basra | Basra / Fao | load_port |
| yanbu | Yanbu | load_port |
| jebel_ali | Jebel Ali | load_port |
| singapore | Singapore bunkering hub | load_port |
| rotterdam | Rotterdam | load_port |
| novorossiysk | Novorossiysk | load_port |
| kozmino | Kozmino (ESPO) | load_port |
| loop | LOOP (Louisiana Offshore) | us_gulf_hub |
| houston_ship_channel | Houston Ship Channel | us_gulf_hub |
| sabine_pass | Sabine Pass LNG | us_gulf_hub |
| freeport | Freeport LNG | us_gulf_hub |
| corpus_christi | Corpus Christi | us_gulf_hub |
| ras_laffan | Ras Laffan | lng_terminal |
| yamal | Yamal LNG | lng_terminal |
| hammerfest | Hammerfest LNG | lng_terminal |
| cove_point | Cove Point LNG | lng_terminal |
| cushing | Cushing, OK | storage_pricing_hub |
| ara | ARA (Amsterdam-Rotterdam-Antwerp) | storage_pricing_hub |
| saldanha | Saldanha Bay | storage_pricing_hub |
| btc | Baku-Tbilisi-Ceyhan | pipeline_entity |
| druzhba | Druzhba pipeline system | pipeline_entity |
| tanap | TANAP | pipeline_entity |

**Fáze 3 subjekty (12 per geo cíl):**

| subjekt_id | popis |
|------------|-------|
| port_authority | Oficiální port / terminal operator |
| pipeline_operator | Provozovatel potrubí |
| transit_naval | Námořní / pobřežní stráž |
| loading_terminal | Load / discharge terminal |
| national_noc | NOC s loading v regionu |
| shipping_lane | VTS / lane management |
| customs_border | Celní / transit režim |
| insurance_war_risk | War-risk / P&I signály (oficiální advisories) |
| storage_operator | Sklad / tank farm |
| pricing_hub | Pricing / benchmark hub |
| weather_hazard | Oficiální weather pro region |
| sanctions_enforcement | Sankční / embargo enforcement body |

**Fáze 3 sloty:** 32 × 12 = **384** (`geo-{target}-{subjekt}`)

---

## Dim 3 — Sociální role (9)

| id | label |
|----|-------|
| official_social_mfa | MFA official Telegram/X |
| official_social_noc | NOC official Telegram/X |
| official_social_ministry | Energy ministry official social |
| energy_correspondent | Tier-1 energy correspondent (desk-trusted) |
| local_field_reporter | Local field reporter |
| port_shipping_spotter | Port / shipping spotter |
| sanctions_tracker | Sanctions tracker (OFAC/EU lists + credible trackers) |
| producer_rhetoric | OPEC+ / producer rhetoric channel |
| ais_freight_commentator | AIS / freight data commentator |

**Fáze 4 sloty:** 64 × 9 = **576** (`soc-{CC}-{role}`)

---

## Dim 4 — Signály (15, tagy na entry)

`production`, `exports`, `imports`, `force_majeure`, `sanctions`, `export_license`,
`vessel_loading`, `port_closure`, `pipeline_outage`, `refinery_outage`, `quota_rhetoric`,
`hurricane`, `storage_levels`, `term_contract`, `pricing_formula`

Signály jsou **tagy** na slotu, ne samostatná dimenze násobící matici.

---

## Dim 5 — Globální vrstva (5 kategorií)

| category | planned_slots | fáze |
|----------|---------------|------|
| international_agency | 40 | global batch 1 |
| exchange | 25 | global batch 1 |
| weather | 15 | global batch 1 |
| shipping | 20 | global batch 1 |
| industry_body | 15 | global batch 1 |

**Fáze 1 sloty:** **115** (`gl-{category}-{seq}`)

---

## Projekce kapacity

| Fáze | ID | slotů | kumulativně |
|------|-----|-------|-------------|
| 0 | skeleton | 0 (jen dimenze) | 0 |
| 1 | global | 115 | 115 |
| 2 | country_authority | 640 | 755 |
| 3 | geo_target | 384 | 1 139 |
| 4 | country_social | 576 | 1 715 |
| 5 | crosscheck | re-validace | — |

**Rozšíření nad 1 715:** každý `country_authority` slot může nést až 15 signal-tag kombinací
pro playbook cross-ref; cílových **≥10 000** dosáhneme fází 2–4 s granularitou sub-entit
(NOC divize, regionální porty, regulatorní pod-úřady) dle potřeby desk review — skeleton
fixuje **1 715 base slotů** + rezerva pro rozšíření v průběhu country/geo dávek.

---

## Konvence ID slotů

```
ca-{CC}-{authority_type}          # country × authority
geo-{geo_id}-{subjekt_id}         # geo × subjekt
soc-{CC}-{social_role}            # country × social role
gl-{category}-{nnn}               # global entity (zero-padded seq)
```

Příklad: `ca-SA-noc`, `geo-hormuz-transit_naval`, `soc-IR-official_social_mfa`, `gl-international_agency-001`

---

### Navržené / aktualizované sloty (skeleton — dimenze only)

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| _dim_countries | — | — | 64 codes | — | — | — | — | — | empty |
| _dim_authorities | — | — | 10 types | — | — | — | — | — | empty |
| _dim_geo | — | 32 targets | 12 subjekty | — | — | — | — | — | empty |
| _dim_social | — | — | 9 roles | — | — | — | — | — | empty |
| _dim_signals | — | — | 15 tags | — | — | — | — | — | empty |
| _dim_global | — | — | 5 categories / 115 slots | — | — | — | — | — | empty |

---

### Cross-check (3 perspektivy)

N/A — skeleton fáze bez konkrétních entit/domén.

---

### Unverified / Anti-patterns

- Duplicitní `NO` v briefu — normalizováno na jednu položku (64 zemí).
- Nepřidávat domény v skeleton fázi — riziko halucinace před country/global dávkami.
- Signály jako násobič dimenzí (15× matice) — **ne** v skeletonu; tagy až u filled slotů.

---

### Progress po merge (návrh)

```json
{
  "phase": "global",
  "phase_index": 0,
  "last_country": null,
  "crosscheck_cursor": 0,
  "last_batch_seq": 1
}
```

Po merge skeletonu → **další dávka:** `composer-2-5_002_global_batch.md` (Fáze 1, ~115 globálních entit: agentury, burzy, weather, shipping, industry bodies).

---

## Navrhovaná struktura `catalog.json` (merge po schválení)

Soubor obsahuje `dimensions` (všechny master seznamy výše), `entries: []` (prázdné),
`progress` dle návrhu. Entries se plní od Fáze 1.
