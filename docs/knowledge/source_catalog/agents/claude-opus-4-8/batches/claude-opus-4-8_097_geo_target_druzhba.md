# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_097_geo_target_druzhba.md  
**Fáze:** geo_target — krok druzhba (Fáze 3, 1 geo cíl = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

**Druzhba pipeline** (`druzhba`, pipeline_entity), 12 slotů. Ruská ropa do střední Evropy; **jižní větev
(HU/SK/CZ) má výjimku z EU embarga**. Klíč = **pipeline_operator (Transneft/MOL)**, **sanctions (výjimka)**,
**UA drony na čerpací stanice (2024-25)**. 1 `proposed`, 4 `unverified`, 7 `empty`.

### Navržené sloty (klíčové)

| id | subject | entity | domain | category | signals | status |
|----|---------|--------|--------|----------|---------|--------|
| gt-druzhba-pipeline_operator | pipeline_operator | Transneft + Ukrtransnafta/MOL/Slovnaft | transneft.ru | infrastructure | pipeline_outage | unverified |
| gt-druzhba-national_noc | national_noc | Transneft (RU) / MOL (HU) | mol.hu | infrastructure | imports, refinery_outage | proposed |
| gt-druzhba-insurance_war_risk | insurance_war_risk | UA drone strikes on pumping stations | — | industry_body | force_majeure, pipeline_outage | unverified |
| gt-druzhba-sanctions_enforcement | sanctions_enforcement | EU sanctions (southern Druzhba exemption) | — | government_regulator | sanctions | unverified |

### Poznámky

- Jižní Druzhba (HU/SK/CZ landlocked výjimka) = politický spor; MOL/Slovnaft závislé.
- UA drony/údery na čerpací stanice (2024-25) = opakovaný pipeline_outage signál.
- Ostatní sloty `empty` (inland pipeline; pricing Urals globální).

### Progress po merge

`phase: geo_target`, `last_geo_target: druzhba`, `last_batch_seq: 97`
