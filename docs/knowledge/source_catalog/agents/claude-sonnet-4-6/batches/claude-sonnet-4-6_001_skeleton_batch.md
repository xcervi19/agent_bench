# Catalog batch

**Agent:** claude-sonnet-4-6 (Claude Sonnet 4.6)  
**Soubor:** claude-sonnet-4-6_001_skeleton_batch.md  
**Fáze:** skeleton — krok batch (Fáze 0, celá fáze najednou)  
**Datum:** 2026-07-04  

---

## Shrnutí

Inicializační dávka pro agenta `claude-sonnet-4-6`. Definuje master seznamy všech pěti dimenzí, konvenci ID slotů a projekci kapacity k cíli **≥10 000 slotů**. Žádné domény — skeleton fixuje pouze osy matice; všechny konkrétní sloty vznikají od Fáze 1 se statusem `empty`. Merge do `catalog.json` až po schválení v chatu.

---

## Dim 1 — Země (64, deduplikováno)

Pořadí dle briefu; `NO` je v briefu uvedeno dvakrát (pozice 10 a 65) → normalizováno na jednu položku. Výsledek: **64 unikátních zemí**.

| # | code | country | # | code | country |
|---|------|---------|---|------|---------|
| 1 | SA | Saudi Arabia | 33 | BE | Belgium |
| 2 | IR | Iran | 34 | IT | Italy |
| 3 | IQ | Iraq | 35 | FR | France |
| 4 | RU | Russia | 36 | ES | Spain |
| 5 | US | United States | 37 | PL | Poland |
| 6 | AE | UAE | 38 | UA | Ukraine |
| 7 | KW | Kuwait | 39 | YE | Yemen |
| 8 | QA | Qatar | 40 | SD | Sudan |
| 9 | OM | Oman | 41 | SS | South Sudan |
| 10 | NO | Norway | 42 | CO | Colombia |
| 11 | BR | Brazil | 43 | GY | Guyana |
| 12 | CA | Canada | 44 | SN | Senegal |
| 13 | MX | Mexico | 45 | GQ | Equatorial Guinea |
| 14 | VE | Venezuela | 46 | CG | Congo (Republic) |
| 15 | NG | Nigeria | 47 | GA | Gabon |
| 16 | AO | Angola | 48 | TD | Chad |
| 17 | LY | Libya | 49 | MR | Mauritania |
| 18 | DZ | Algeria | 50 | BH | Bahrain |
| 19 | EG | Egypt | 51 | IL | Israel |
| 20 | CN | China | 52 | JP | Japan |
| 21 | IN | India | 53 | KR | South Korea |
| 22 | MY | Malaysia | 54 | SG | Singapore |
| 23 | ID | Indonesia | 55 | TH | Thailand |
| 24 | AU | Australia | 56 | VN | Vietnam |
| 25 | KZ | Kazakhstan | 57 | PK | Pakistan |
| 26 | AZ | Azerbaijan | 58 | BD | Bangladesh |
| 27 | TM | Turkmenistan | 59 | CL | Chile |
| 28 | UZ | Uzbekistan | 60 | PE | Peru |
| 29 | TR | Turkey | 61 | EC | Ecuador |
| 30 | GB | United Kingdom | 62 | TT | Trinidad & Tobago |
| 31 | DE | Germany | 63 | JM | Jamaica |
| 32 | NL | Netherlands | 64 | DK | Denmark |

---

## Dim 1 — Typy autorit (10)

| id | label | primární signál |
|----|-------|-----------------|
| ministry_petroleum | Energy / petroleum ministry | policy, export_license, quota_rhetoric |
| noc | National oil company | production, exports, force_majeure, term_contract |
| mfa | Ministry of foreign affairs | sanctions, policy |
| customs_export | Customs / export licensing authority | exports, export_license |
| upstream_regulator | Upstream / licensing regulator | production, refinery_outage |
| port_maritime_authority | Port & maritime authority | vessel_loading, port_closure |
| national_exchange | National commodity / energy exchange | pricing_formula, term_contract |
| central_bank | Central bank (FX / sanctions linkage) | sanctions |
| environment_regulator | Environment / emissions regulator | refinery_outage |
| coast_guard_navy | Coast guard / naval transit authority | port_closure, force_majeure |

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
| transit_naval | Námořní / pobřežní stráž, VTS |
| loading_terminal | Load / discharge terminal operator |
| national_noc | NOC s loadingem v regionu |
| shipping_lane | Lane / traffic management authority |
| customs_border | Celní / transit režim |
| insurance_war_risk | War-risk / P&I oficiální advisories |
| storage_operator | Sklad / tank farm operator |
| pricing_hub | Pricing / benchmark hub |
| weather_hazard | Oficiální weather / hazard pro region |
| sanctions_enforcement | Sankční / embargo enforcement body |

**Fáze 3 sloty:** 32 × 12 = **384** (`geo-{target}-{subjekt}`)

---

## Dim 3 — Sociální role (9)

| id | label |
|----|-------|
| official_social_mfa | MFA official Telegram / X |
| official_social_noc | NOC official Telegram / X |
| official_social_ministry | Energy ministry official social |
| energy_correspondent | Tier-1 energy correspondent (desk-trusted) |
| local_field_reporter | Local field reporter |
| port_shipping_spotter | Port / shipping spotter |
| sanctions_tracker | Sanctions tracker (OFAC / EU lists + credible trackers) |
| producer_rhetoric | OPEC+ / producer rhetoric channel |
| ais_freight_commentator | AIS / freight data commentator |

**Fáze 4 sloty:** 64 × 9 = **576** (`soc-{CC}-{role}`)

---

## Dim 4 — Signály (15, tagy na entry)

`production`, `exports`, `imports`, `force_majeure`, `sanctions`, `export_license`,
`vessel_loading`, `port_closure`, `pipeline_outage`, `refinery_outage`, `quota_rhetoric`,
`hurricane`, `storage_levels`, `term_contract`, `pricing_formula`

Signály jsou **tagy** na slotu, ne samostatná osa násobící matici.

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

## Konvence ID slotů

```
ca-{CC}-{authority_type}          # country × authority   (Fáze 2)
geo-{geo_id}-{subjekt_id}         # geo × subjekt         (Fáze 3)
soc-{CC}-{social_role}            # country × social role  (Fáze 4)
gl-{category}-{nnn}               # global entity, zero-padded seq (Fáze 1)
```

Příklady: `ca-SA-noc`, `geo-hormuz-transit_naval`, `soc-IR-official_social_mfa`,
`gl-international_agency-001`

---

## Projekce kapacity → cíl ≥10 000 slotů

Base matice (jedna entita na slot):

| Fáze | ID | base slotů | kumulativně |
|------|-----|-----------|-------------|
| 0 | skeleton | 0 (jen dimenze) | 0 |
| 1 | global | 115 | 115 |
| 2 | country_authority | 640 | 755 |
| 3 | geo_target | 384 | 1 139 |
| 4 | country_social | 576 | 1 715 |

**Base = 1 715 slotů.** Cíle ≥10 000 dosahujeme řízenou granularitou sub-entit, ne
násobením prázdné matice — každý reálný úřad má více oficiálních publikačních kanálů:

| Vrstva expanze | mechanismus | odhad slotů |
|----------------|-------------|-------------|
| Sub-entity autorit | NOC divize (upstream/downstream/trading), regionální porty, pod-regulátoři: ø ~4 kanály / autorita s obsazenou entitou | 640 → ~2 560 |
| Geo sub-terminály | multi-berth porty, per-pipeline segment, per-terminal LNG train | 384 → ~1 500 |
| Social per-platform | Telegram + X + web press pro každou obsazenou roli | 576 → ~1 700 |
| Signal cross-ref sloty | pro playbook: kombinace obsazený slot × relevantní signal-tag (≤15) | ~4 000 |
| Globální rozšíření | per-report endpointy (EIA WPSR, OPEC MOMR, IEA OMR jako samostatné feed-sloty) | 115 → ~600 |

**Projekce:** ~2 560 + 1 500 + 1 700 + 4 000 + 600 ≈ **10 360 slotů**. Skeleton fixuje
1 715 base slotů; expanzní vrstvy vznikají inkrementálně během Fází 2–4 dle desk review,
každá s vlastním `status` (většina zpočátku `empty`).

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

N/A — skeleton fáze bez konkrétních entit / domén. Perspektivy supply / geopolitics /
logistics se aplikují od Fáze 1 na obsazené sloty.

---

### Unverified / Anti-patterns

- Duplicitní `NO` v briefu → normalizováno na jednu položku (64 zemí).
- Žádné domény v skeleton fázi — riziko halucinace před country/global dávkami.
- Signály **nejsou** násobič matice (15× blow-up); jsou tagy na obsazených slotech.
- Cíl 10 000 se **nemá** naplňovat prázdnými kartézskými sloty — expanze jen tam, kde
  reálná entita má více oficiálních kanálů.

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

Po merge skeletonu → **další dávka:** `claude-sonnet-4-6_002_global_batch.md` (Fáze 1,
~115 globálních entit: mezinárodní agentury, burzy, weather, shipping, industry bodies).

---

## Navrhovaná struktura `catalog.json` (merge po schválení)

Soubor bude obsahovat `dimensions` (všechny master seznamy výše), `entries: []` (prázdné,
plní se od Fáze 1), `progress` dle návrhu výše a `runner` = `{agent_slug, model_display_name}`.
