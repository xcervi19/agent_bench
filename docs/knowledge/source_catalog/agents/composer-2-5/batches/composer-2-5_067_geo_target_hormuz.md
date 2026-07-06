# Catalog batch

**Agent:** composer-2-5 (Composer 2.5)  
**Soubor:** composer-2-5_067_geo_target_hormuz.md  
**Fáze:** geo_target — krok hormuz (Fáze 3, geo 1/32)  
**Datum:** 2026-07-06  

---

## Shrnutí

Strait of Hormuz × 12 subjektů. **9 proposed**, **1 unverified**, **2 empty** (pipeline / storage — mimo přímý transit).

---

### Navržené / aktualizované sloty

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| geo-hormuz-port_authority | IR | hormuz | port_authority | PMO — Bandar Abbas Port | pmo.ir | infrastructure | official | port_closure,vessel_loading | proposed |
| geo-hormuz-pipeline_operator | — | hormuz | pipeline_operator | (no pipeline through strait) | — | infrastructure | — | pipeline_outage | empty |
| geo-hormuz-transit_naval | US | hormuz | transit_naval | US Naval Forces Central Command (5th Fleet) | cusnc.navy.mil | government_regulator | official | port_closure,vessel_loading | proposed |
| geo-hormuz-loading_terminal | IR | hormuz | loading_terminal | Bandar Abbas oil terminals | pmo.ir | infrastructure | official | vessel_loading,exports | proposed |
| geo-hormuz-national_noc | IR | hormuz | national_noc | NIOC | nioc.ir | noc | official | exports,force_majeure,production | proposed |
| geo-hormuz-shipping_lane | OM | hormuz | shipping_lane | Oman Maritime Security Centre | sm.gov.om | shipping | official | vessel_loading,port_closure | proposed |
| geo-hormuz-customs_border | IR | hormuz | customs_border | IRICA (Iran Customs) | irica.gov.ir | government_regulator | official | exports,export_license | proposed |
| geo-hormuz-insurance_war_risk | US | hormuz | insurance_war_risk | US MARAD Advisory | maritime.dot.gov | shipping | official | vessel_loading,sanctions | proposed |
| geo-hormuz-storage_operator | — | hormuz | storage_operator | (Fujairah hub — separate geo target) | — | infrastructure | — | storage_levels | empty |
| geo-hormuz-pricing_hub | AE | hormuz | pricing_hub | DGCX (Dubai crude marker) | dgcx.ae | exchange | official | pricing_formula,exports | proposed |
| geo-hormuz-weather_hazard | OM | hormuz | weather_hazard | PACA Oman (Met / aviation weather) | paca.gov.om | weather | official | hurricane,port_closure | proposed |
| geo-hormuz-sanctions_enforcement | US | hormuz | sanctions_enforcement | OFAC (Treasury) | treasury.gov | government_regulator | official | sanctions,export_license | proposed |

---

### Cross-check (3 perspektivy)

| id | supply | geopolitics | logistics | verdict |
|----|--------|-------------|-----------|---------|
| geo-hormuz-national_noc | NIOC export ops | IR closure rhetoric / IRGC seizures | Kharg/Bandar Abbas loadings | **proposed** — pair `ca-IR-noc` |
| geo-hormuz-transit_naval | — | US-Iran escalation | 5th Fleet escort / tanker interdiction | **proposed** — IRGC ops: no clean official domain → playbook |
| geo-hormuz-port_authority | — | — | Bandar Abbas congestion / closure | **proposed** |
| geo-hormuz-shipping_lane | — | Oman neutrality | VTS / traffic separation scheme | **proposed** |
| geo-hormuz-sanctions_enforcement | — | Iran oil sanctions enforcement | Shadow fleet / insurance linkage | **proposed** |
| geo-hormuz-insurance_war_risk | — | War-risk premium spikes | MARAD zone advisories | **proposed** |
| geo-hormuz-pricing_hub | Dubai sour marker | — | Middle East diff discovery | **proposed** |

---

### Unverified / Anti-patterns

| id | issue |
|----|-------|
| geo-hormuz-pipeline_operator | No subsea pipeline through Hormuz chokepoint |
| geo-hormuz-storage_operator | Fujairah = `geo-fujairah-*` batch; not duplicated here |
| geo-hormuz-transit_naval | IRGC Navy — operational lead on Iranian side; no Tier-1 whitelist domain |

**Desk note:** Hormuz = **nioc.ir + pmo.ir + cusnc.navy.mil + treasury.gov**. Also monitor Saudi/Iraq exports transiting (Aramco/SOMO — country slots). Kharg Island → `geo-kharg` batch.

**Playbook extensions:** `mfa.gov.ir` (closure rhetoric), `aramco.com` (Gulf export volume through strait).

---

### Progress po merge (návrh)

```json
{
  "phase": "geo_target",
  "phase_index": 1,
  "last_geo_target": "hormuz",
  "crosscheck_cursor": 0,
  "last_batch_seq": 67
}
```

**Další dávka:** `composer-2-5_068_geo_target_bab_el_mandeb.md` (Bab el-Mandeb × 12 subjektů).

### Whitelist kandidáti (Tier 1, po schválení)

`pmo.ir`, `nioc.ir`, `cusnc.navy.mil`, `irica.gov.ir`, `maritime.dot.gov`, `treasury.gov`, `dgcx.ae`
