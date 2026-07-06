# Batch 065 — Country Authority: VN (Vietnam)

## Country significance
Vietnam is Southeast Asia's **third-largest crude producer** (~200–240 kb/d) and a growing LNG importer. The **Cuu Long basin** (Bach Ho = White Tiger field, PetroVietnam op.) and **Nam Con Son basin** (Lan Tay/Lan Do gas) are legacy fields in structural decline. Vietnam imports gas from **Malaysia via PM3-CAA** and is building LNG import terminals (Son My, Thi Vai, Ha Tinh). **PetroVietnam (PVN)** is the dominant state conglomerate, with upstream subsidiary PVEP and downstream BSR Binh Son Refinery. Vietnam's **South China Sea territorial disputes** (with China, Philippines, Malaysia) directly create upstream drilling risk — China has repeatedly interfered with Vietnamese seismic surveys and drilling (2019 Lan Do, 2020 Ca Voi Xanh delays).

## Proposed slots

| id | country | geo_target | authority / role | entity | domain | category | type | signals | status |
|----|---------|------------|------------------|--------|--------|----------|------|---------|--------|
| ca-VN-ministry_petroleum | VN | — | ministry_petroleum | Ministry of Industry and Trade (MOIT) | moit.gov.vn | international_agency | official | policy, export_license, quota_rhetoric | proposed |
| ca-VN-noc | VN | — | noc | PetroVietnam (PVN) – Vietnam Oil and Gas Group | pvn.vn | international_agency | official | production, exports, term_contract, pricing_formula | proposed |
| ca-VN-mfa | VN | — | mfa | Ministry of Foreign Affairs | mofa.gov.vn | international_agency | official | sanctions, policy | proposed |
| ca-VN-customs_export | VN | — | customs_export | General Department of Vietnam Customs | customs.gov.vn | international_agency | official | exports, export_license | proposed |
| ca-VN-upstream_regulator | VN | — | upstream_regulator | Ministry of Natural Resources and Environment (MONRE) | monre.gov.vn | international_agency | official | production, force_majeure | proposed |
| ca-VN-port_maritime_authority | VN | — | port_maritime_authority | Vietnam Maritime Administration (VINAMARINE) | vinamarine.gov.vn | international_agency | official | vessel_loading, port_closure | proposed |
| ca-VN-national_exchange | VN | — | national_exchange | Ho Chi Minh Stock Exchange (HoSE) | hsx.vn | exchange | official | pricing_formula | proposed |
| ca-VN-central_bank | VN | — | central_bank | State Bank of Vietnam | sbv.gov.vn | international_agency | official | pricing_formula | proposed |
| ca-VN-environment_regulator | VN | — | environment_regulator | Vietnam Environment Administration (VEA) | vea.gov.vn | international_agency | official | refinery_outage | proposed |
| ca-VN-coast_guard_navy | VN | — | coast_guard_navy | Vietnam Coast Guard + Vietnam People's Navy | vietcoastguard.gov.vn | international_agency | official | port_closure, force_majeure | unverified |

## Cross-check (key entries)

### ca-VN-noc (PetroVietnam PVN)
- **Supply:** PVN total output ~550–600 kboe/d; Bach Ho crude (Cuu Long); Nam Con Son gas (Lan Tay/Lan Do → PM3-CAA); Ca Voi Xanh deepwater gas (ExxonMobil op., delayed by SCS dispute); Nghi Son + Binh Son refineries = domestic supply
- **Geopolitics:** SCS territorial disputes = drilling permit/force majeure risk; China CNOOC intimidation of PVEP rigs; US-Vietnam strategic partnership energy component
- **Logistics:** Vung Tau terminal (crude export hub); Ho Chi Minh City + Da Nang ports; LNG import Son My (GNL Hai Lam JV, Exxon+PVN+AES)

### ca-VN-coast_guard_navy (VCG + VPN)
- **Supply:** Bach Ho platform security; Ca Voi Xanh site patrol; SCS SLOC enforcement
- **Geopolitics:** Vietnam-China standoff at Vanguard Bank (2019); VCG vessels vs CNOOC survey ships = direct escalation signal
- **Logistics:** East Sea patrol; Cam Ranh Bay naval base; Cam Pha + Hon La coal terminal security

## Expansion slots (10+)
- ca-VN-pvep — PetroVietnam Exploration Production Corp (upstream subsidiary)
- ca-VN-bsr — Binh Son Refining (Dung Quat refinery 148 kb/d)
- ca-VN-nsr — Nghi Son Refinery (200 kb/d, PVN+Idemitsu+Kuwait op.)
- ca-VN-scs_monitor — AMTI/CSIS South China Sea Tribunal tracking
- ca-VN-petrovietnam_gas — PV GAS (downstream distribution)

## Anti-patterns
- Skip: VietnamPlus (English state news aggregator)
- Skip: Vietnam Investment Review energy section (secondary SEO)
