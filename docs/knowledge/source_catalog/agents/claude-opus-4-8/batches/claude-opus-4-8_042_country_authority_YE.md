# Catalog batch

**Agent:** claude-opus-4-8 (Claude Opus 4.8)  
**Soubor:** claude-opus-4-8_042_country_authority_YE.md  
**Fáze:** country_authority — krok YE (Fáze 2, 1 země = 1 dávka)  
**Datum:** 2026-07-06  

---

## Shrnutí

Jemen (`YE`), 10 slotů (`ca-YE-{authority}`). Marginální producent; **strategická hodnota = Bab
el-Mandeb chokepoint + Houthi útoky na Rudé moře** (přesměrování kolem Mysu Dobré naděje = freight/
insurance signál). Občanská válka → úřady roztříštěné (Aden vláda vs. Houthi Sanaa). Většina slotů
`empty`/`unverified` — reálný signál přes geo (Bab el-Mandeb) + vojenské monitory. 1 `proposed`, 4 `unverified`, 5 `empty`.

### Navržené sloty

| id | authority_type | entity | domain | category | type | signals | status |
|----|----------------|--------|--------|----------|------|---------|--------|
| ca-YE-ministry_petroleum | ministry_petroleum | Ministry of Oil & Minerals | — | government_regulator | official | production | empty |
| ca-YE-noc | noc | YOGC / Safer | — | noc | official | production, exports | unverified |
| ca-YE-mfa | mfa | Ministry of Foreign Affairs (Aden) | — | diplomacy | official | sanctions | unverified |
| ca-YE-customs_export | customs_export | — | — | — | — | — | empty |
| ca-YE-upstream_regulator | upstream_regulator | — | — | — | — | — | empty |
| ca-YE-port_maritime_authority | port_maritime_authority | Aden / Hodeidah ports | — | infrastructure | official | port_closure, vessel_loading | unverified |
| ca-YE-national_exchange | national_exchange | — | — | — | — | — | empty |
| ca-YE-central_bank | central_bank | Central Bank of Yemen (split Aden/Sanaa) | — | government_regulator | official | sanctions | unverified |
| ca-YE-environment_regulator | environment_regulator | — | — | — | — | — | empty |
| ca-YE-coast_guard_navy | coast_guard_navy | Houthi forces / Yemeni Coast Guard | — | diplomacy | official | port_closure, force_majeure | empty |

### Cross-check (klíč)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| ca-YE-coast_guard_navy | — | **Houthi útoky na tankery** | Bab el-Mandeb reroute → Cape | empty — reálný signál přes vojenské/CENTCOM + AIS |
| ca-YE-port_maritime_authority | — | Hodeidah (Houthi) vs Aden (vláda) | Red Sea shipping | unverified |

### Unverified / Anti-patterns / poznámky

- **Strategická hodnota ≠ produkce:** Jemen sleduj kvůli **Bab el-Mandeb** (`bab_el_mandeb` geo Fáze 3),
  ne kvůli vlastní ropě. Houthi útoky = freight rate + war-risk insurance + reroute signál.
- **FSO Safer** (odstaveno, riziko úniku) — historický tail risk (částečně vyřešeno 2023 UN offload).
- Roztříštěné úřady (Aden vs. Sanaa) → většina `empty`; neuvádět jednu frakci jako národní autoritu.
- Reálné monitory: CENTCOM/UKMTO (Bab el-Mandeb advisories), AIS reroute data — patří do global shipping / geo, ne YE autority.

### Progress po merge

`last_country: YE`, `last_batch_seq: 42`
