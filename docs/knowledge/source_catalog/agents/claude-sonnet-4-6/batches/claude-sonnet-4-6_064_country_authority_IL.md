# Batch 064 — Country Authority: IL (Israel)

## Country significance
Israel is an **emerging Eastern Mediterranean gas power** following Leviathan (21.4 tcf, 2019 start), Tamar (10.8 tcf, 2013), and Karish (2022) fields. Israeli gas is piped to **Egypt and Jordan** (via sub-sea EMG + overland pipelines) and exported as LNG via **Egyptian liquefaction terminals** (ELNG Idku, SEGAS Damietta). Israel's **energy-security profile** is shaped by its strategic environment: Hamas/Hezbollah threats to offshore platforms, Iran proxy activity, and US-mediated Egypt-Israel gas deal. The **Delek Group** and **NewMed Energy** (previously Delek Drilling) + **Chevron** operate Leviathan. Regulatory authority sits with the Ministry of Energy and the Petroleum Commissioner. Israel is also a growing **solar/gas-peaker market**.

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-IL-ministry_petroleum | IL | — | ministry_petroleum | Ministry of Energy and Infrastructure | gov.il/en/ministries/energy | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-IL-noc | IL | — | noc | NewMed Energy (Delek Drilling successor) | newmedenergy.com | company | official | production, exports, term_contract | proposed |
| ca-IL-mfa | IL | — | mfa | Ministry of Foreign Affairs | mfa.gov.il | international_agency | official | sanctions, policy | proposed |
| ca-IL-customs_export | IL | — | customs_export | Israel Tax Authority (Customs) | taxes.gov.il | international_agency | official | exports, export_license | proposed |
| ca-IL-upstream_regulator | IL | — | upstream_regulator | Petroleum Commissioner (Ministry of Energy) | gov.il/en/ministries/energy | international_agency | official | production, force_majeure | proposed |
| ca-IL-port_maritime_authority | IL | — | port_maritime_authority | Israel Ports Company | israports.co.il | international_agency | official | vessel_loading, port_closure | proposed |
| ca-IL-national_exchange | IL | — | national_exchange | Tel Aviv Stock Exchange (TASE) | tase.co.il | exchange | official | pricing_formula | proposed |
| ca-IL-central_bank | IL | — | central_bank | Bank of Israel | boi.org.il | international_agency | official | pricing_formula | proposed |
| ca-IL-environment_regulator | IL | — | environment_regulator | Ministry of Environmental Protection | gov.il/en/ministries/environmental-protection | international_agency | official | force_majeure | proposed |
| ca-IL-coast_guard_navy | IL | — | coast_guard_navy | Israeli Navy (INF) | idf.il | international_agency | official | port_closure, force_majeure | proposed |

## Cross-check (key entries)

### ca-IL-noc (NewMed Energy)
- **Supply:** NewMed 45.34% Leviathan (Chevron op.); exports ~11 bcm/y to Egypt + Jordan; Aphrodite Cyprus JV; pipeline expansion discussions (Turkey, EU)
- **Geopolitics:** Gaza war 2023+ = Karish field shutdown risk; Hezbollah threat to Leviathan; US-brokered Egypt-Israel deal; normalization with Arab states = gas diplomacy
- **Logistics:** Leviathan FPSO at Mari-B field; EMG sub-sea pipeline to Egypt; East Med Gas Forum coordination

### ca-IL-coast_guard_navy (INF)
- **Supply:** Leviathan + Tamar platform protection; Gaza maritime blockade; Hezbollah/drone threat to offshore infrastructure
- **Geopolitics:** Iran-Israel direct confrontation risk; US carrier group coordination; platform attack = immediate supply disruption
- **Logistics:** Eastern Mediterranean SLOC control; Haifa port (LNG import terminal); Ashdod port (product imports)

## Expansion slots (10+)
- ca-IL-delek_group — Delek Group parent holding (TASE listed; Leviathan governance)
- ca-IL-chevron_leviathan — Chevron Israel (Leviathan 39.66% op.)
- ca-IL-east_med_gas_forum — Cairo-based regional gas body
- ca-IL-emg_pipeline — East Mediterranean Gas pipeline monitoring
- ca-IL-iai_security — IDF spokesperson (offshore threat advisories)

## Anti-patterns
- Skip: Jerusalem Post energy section (commentary only)
- Skip: Haaretz energy coverage (secondary, paywalled aggregation)
