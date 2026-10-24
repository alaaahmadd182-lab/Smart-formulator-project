# Open questions and conflicts (all products)

Generated 2026-10-24 by `build_conflicts_report.py` from the `open_questions`, `conflicts` and `fields` of every JSON file in `Products_json` (base oils, additive packages, additive components). Final values (`value_final`, `unit_final`, `status_final`, `source_final`, written by `integrate_products.py`) are used where present, otherwise the original keys.

| Section | Count |
|---|---|
| 1. Unresolved conflicts | 2 |
| 2a. Properties whose value_final was resolved | 31 |
| 2b. Conflict records marked resolved | 37 (6 needed no value change) |
| 2c. value_final corrected or left null during unit integration | 2 |
| 3. Reported numeric values with no method, unit or reference temperature | 401 |
| 4. Open questions | 1394 (in 209 products) |

## 1. Unresolved conflicts

The resolution rules could not choose a value for these. The value_final shown is the field as it stands, pending supplier confirmation.

### ARAMCO_LUBEREF_DURA_BS150_YANBU (Base oils, tier3)
- **Recorded conflict:** {"field": "sulfur", "sources": [{"file": "DL2-13944.pdf", "page": 1, "printed_text": "Sulfur Content ppm 1.3‡ (‡ D2622)"}, {"file": "DL2-12173.pdf", "page": 1, "printed_text": "Sulfur Content Max WT% 1.3"}], "note": "Conflicting units (ppm vs wt.%). 1.3 wt.% retained from guaranteed specification; verify before use."}
- **Property:** `tier3 fields.sulfur`; value_final **1.3 wt.%** (printed: 1.3; source DL2-12173.pdf p.1)
- **Why unresolved:** DL2-13944.pdf prints '1.3 ppm' and DL2-12173.pdf prints 'Max WT% 1.3'. Same number, units 10,000x apart, so one sheet is almost certainly misprinted. The rules cannot pick between them; confirm with Aramco. value_final shows the field as it stands.

### ERGON_HYGOLD_L750 (Base oils, tier1)
- **Recorded conflict:** {"property": "density_at_15_6_c", "description": "TDS reports density at 15.6°C = 0.854 g/cm3 but specific gravity at 15.6°C = 0.9183; these appear inconsistent. Neither has been silently corrected.", "sources": [{"file": "DL2-10414.pdf", "page": 1}]}
- **Property:** `tier1 fields.density`; value_final **0.854 g/cm³** (printed: TDS reports density at 15.6°C 0.854 g/cm3; conflicts with specific gravity 0.9183; source DL2-10414.pdf p.1)
- **Why unresolved:** a single TDS (DL2-10414.pdf) prints density 0.854 g/cm³ and specific gravity 0.9183 at 15.6 °C, which contradict each other. This is not a two-document conflict, so the rules do not apply; confirm with Ergon. value_final shows the density as printed.

## 2. Resolved values

Rules (user decision 2026-10-24): TDS (or PDS / bulletin / specification sheet) preferred over SDS; same document type -> newest dated edition, or the average (status Calculated) when the dates cannot be compared; text values take the newest; a measured or typical number beats a bound; the user decisions of 2026-10-18 on RF6077 and RF6088F are kept.

### 2a. Properties whose value_final was resolved

| Class | Product | Tier | Property | Original value | value_final | Final status | Final source | How it was resolved |
|---|---|---|---|---|---|---|---|---|
| Additive packages | INFINEUM_D3424 | tier2 | `flash_point` | 110 C | **190 °C** | Reported | DL2-10204.pdf p.1 | TDS preferred over SDS: TDS typical 190 °C (DL2-10204.pdf p.1, 2004) chosen over SDS lower bound '>110 °C' (p.6, 2008), which was in the field under the old newest-document rule. |
| Additive packages | RICHFUL_RF6066 | tier2 | `tbn` | 108 mg KOH/g | **107 mg KOH/g** | Calculated | DL2-13819.pdf p.1; DL2-15451.pdf p.1 | Same document type, editions undated so the newest cannot be determined; average taken: TDS 106 and 108 mg KOH/g -> 107. SDS value (106) not used: TDS preferred over SDS. |
| Additive packages | RICHFUL_RF6066 | tier2 | `elements.Ca` | 3.15 wt.% | **3.075 wt.%** | Calculated | DL2-13819.pdf p.1; DL2-15451.pdf p.1 | Same document type, editions undated so the newest cannot be determined; average taken: TDS 3.0 and 3.15 wt.% -> 3.075 wt.%. |
| Additive packages | RICHFUL_RF6066 | tier2 | `elements.Zn` | 1.24 wt.% | **1.27 wt.%** | Calculated | DL2-13819.pdf p.1; DL2-15451.pdf p.1 | Same document type, editions undated so the newest cannot be determined; average taken: TDS 1.3 and 1.24 wt.% -> 1.27 wt.%. |
| Additive packages | RICHFUL_RF6066 | tier2 | `kv100` | 185 mm²/s | **206 cSt** | Calculated | DL2-13819.pdf p.1; DL2-15451.pdf p.1 | Same document type, editions undated so the newest cannot be determined; average taken: TDS 227 and 185 cSt -> 206 cSt. The two TDS differ by about 20 %, so this average is weak; check with Richful. SDS values (200, 185) not used: TDS preferred over SDS. |
| Additive packages | RICHFUL_RF6066 | tier2 | `density` | 988 kg/m3 | **0.989 g/cm³** | Calculated | DL2-13819.pdf p.1; DL2-15451.pdf p.1 | Same document type, editions undated so the newest cannot be determined; average taken: TDS DL2-13819.pdf 990 kg/m³ and TDS DL2-15451.pdf 988 kg/m³ (both at 20 °C) -> 989 kg/m³ = 0.989 g/cm³. SDS values (990 kg/m³, 0.988 g/cm³) not used: TDS preferred over SDS. |
| Additive packages | RICHFUL_RF6069 | tier2 | `kv100` | 142 mm²/s | **118 cSt** | Reported | DL2-15618.pdf p.1 | TDS preferred over SDS: TDS DL2-15618.pdf 118 cSt chosen over SDS DL2-15619.pdf 142 cSt (2022-01-04). |
| Additive packages | RICHFUL_RF6077 | tier2 | `kv100` | 150 mm²/s | **150 cSt** | reported | DL2-15542.pdf p.5 | User decision of 2026-10-18 kept (SDS DL2-15542.pdf 150 cSt); it overrides the TDS-preferred rule, which would give TDS DL2-15536.pdf 160 cSt. |
| Additive packages | RICHFUL_RF6077 | tier2 | `density` | 0.991 g/cm³ | **0.991 g/cm³** | reported | DL2-15542.pdf p.5 | User decision of 2026-10-18 kept (SDS DL2-15542.pdf 0.991 g/cm³ at 15 °C); it overrides the TDS-preferred rule, which would give TDS DL2-15536.pdf 998 kg/m³ at 20 °C. |
| Additive packages | RICHFUL_RF6078 | tier1 | `treat_rate_matrix[0].treat_rate_wt_pct` | – (printed: –) | **11.35 wt.%** | Calculated | DL2-15832.pdf p.1; RF6078%20-%20TDS.pdf p.1 | Same document type, editions undated so the newest cannot be determined; average taken: row 'ACEA E7/API CI-4' is 11.85 % in DL2-15832.pdf and 10.85 % in 'RF6078 - TDS.pdf' -> 11.35 %. The two sheets label their second row differently ('API CI-4' vs 'API CI-4 Plus'), so the average is weak; check with Richful. |
| Additive packages | RICHFUL_RF6078 | tier2 | `density` | 972 kg/m3 | **0.972 g/cm³** | Reported | DL2-15832.pdf p.1; RF6078%20-%20TDS.pdf p.1 | TDS preferred over SDS: both TDS print 972 kg/m³ at 20 °C (= 0.972 g/cm³); SDS DL2-15833.pdf 975 kg/m³ not used. |
| Additive packages | RICHFUL_RF6081 | tier2 | `kv100` | 132.0 mm2/s | **132 cSt** | reported | DL2-15836.pdf p.2 | TDS preferred over SDS: TDS DL2-15836.pdf 132 cSt kept over SDS DL2-15837.pdf 130 cSt (the TDS is also newer). |
| Additive packages | RICHFUL_RF6088F | tier2 | `kv100` | 178.2 mm²/s | **178.2 cSt** | reported | DL2-15840.pdf p.5 | User decision of 2026-10-18 kept (SDS DL2-15840.pdf 178.2 cSt); it overrides the TDS-preferred rule, which would give TDS DL2-15839.pdf 177 cSt. |
| Additive packages | RICHFUL_RF6088F | tier2 | `density` | 963.0 kg/m³ | **0.963 g/cm³** | reported | DL2-15839.pdf p.1 | User decision of 2026-10-18 kept (TDS DL2-15839.pdf 963 kg/m³ at 20 °C); agrees with TDS preferred over SDS (SDS DL2-15840.pdf relative density 0.958 not used). |
| Additive packages | RICHFUL_RF6406 | tier1 | `treat_rate_matrix[10].treat_rate_wt_pct` | 4.1 % | **3.9 %** | Calculated | DL2-15456.pdf p.1; DL2-14746.pdf p.1 | Same document type, editions undated so the newest cannot be determined; average taken: row 'CF/SF Multi' is 4.1 % in DL2-15456.pdf and 3.7 % in DL2-14746.pdf -> 3.9 %. |
| Additive packages | RICHFUL_RF6406 | tier2 | `tbn` | 185 mg KOH/g | **185 mg KOH/g** | Reported | DL2-15456.pdf p.1 | Measured value beats a bound: TDS DL2-15456.pdf typical 185 mg KOH/g chosen over TDS DL2-14746.pdf '≥180' (a minimum, not a measurement). |
| Base oils | FORMOSA_150N_GII_PLUS | tier2 | `flash_point` | – (printed: Min 210 C) | **– °C** | Reported | DL2-10001.pdf p.1 | TDS preferred over SDS: specification sheet DL2-10001.pdf 'Min 210 C' kept over SDS DL2-10011.pdf '>230 C'. Both are bounds, so there is no single measured value. |
| Base oils | NYNAS_NS_3 | tier1 | `kv40` | 2.92 cSt | **2.92 cSt** | Reported | DL2-15474.pdf p.2 | Same document type; newest edition used: 2024 edition DL2-15474.pdf 2.92 cSt over 2016 edition DL2-12382.pdf 2.84 cSt. |
| Base oils | NYNAS_NS_3 | tier1 | `density` | 0.863 kg/dm3 | **0.863 g/cm³** | Reported | DL2-15474.pdf p.2 | Same document type; newest edition used: 2024 edition DL2-15474.pdf 0.863 over 2016 edition DL2-12382.pdf 0.860. |
| Base oils | NYNAS_NS_3 | tier2 | `flash_point` | 95 C | **95 °C** | Reported | DL2-15474.pdf p.2 | Same document type; newest edition used: 2024 edition DL2-15474.pdf 95 °C over 2016 edition DL2-12382.pdf 94 °C. |
| Base oils | NYNAS_NS_3 | tier3 | `sulfur` | 10 ppm | **0.001 wt.%** | Reported | DL2-15474.pdf p.2 | Same document type; newest edition used: 2024 edition DL2-15474.pdf 'Typical < 10 ppm' over 2016 edition DL2-12382.pdf 30 ppm. '<10 ppm' is a typical result below the reporting limit, not a specification bound, so the measured-beats-bound rule does not apply. |
| Base oils | NYNAS_NYFROST_32 | tier1 | `kv40` | 32 cSt | **32 cSt** | Reported | DL2-11510.pdf p.2 | TDS preferred over SDS: PDS DL2-11510.pdf 32 cSt kept over SDS DL2-13444.pdf 31 cSt. |
| Base oils | NYNAS_NYFROST_32 | tier2 | `flash_point` | 176 C | **176 °C** | Reported | DL2-11510.pdf p.2 | TDS preferred over SDS: PDS DL2-11510.pdf typical 176 °C (Pensky-Martens) kept over SDS DL2-13444.pdf bound '>180 °C'. |
| Base oils | PETRONAS_ETRO_6_PLUS | tier1 | `kv40` | 32.55 cSt | **32.55 cSt** | Reported | DL2-10234.pdf p.1 | TDS preferred over SDS: TDS DL2-10234.pdf 32.55 cSt kept over SDS DL2-14610.pdf 34.79 cSt. |
| Base oils | PETRONAS_ETRO_6_PLUS | tier1 | `density` | 0.8486 g/cm3 | **0.8429 g/cm³** | Reported | DL2-10234.pdf p.1 | TDS preferred over SDS: TDS DL2-10234.pdf 0.8429 kg/L chosen over SDS DL2-14610.pdf 0.8486 g/cm³ at 15 °C, which was in the field. The TDS prints no measurement temperature. |
| Base oils | PETRONAS_ETRO_6_PLUS | tier2 | `noack_volatility` | 5.7 wt% | **5.7 wt.%** | Reported | DL2-10234.pdf p.1 | TDS preferred over SDS: TDS DL2-10234.pdf 5.7 wt.% kept over SDS DL2-14610.pdf 5.3 wt.%. |
| Base oils | PETRONAS_ETRO_6_PLUS | tier2 | `flash_point` | 240 C | **240 °C** | Reported | DL2-10234.pdf p.1 | TDS preferred over SDS: TDS DL2-10234.pdf 240 °C (ASTM D92, COC) kept over SDS DL2-14610.pdf 228 °C (ASTM D93, PMCC). Different methods, so the two values are not directly comparable. |
| Base oils | PETRO_CANADA_PURITY_L65 | tier1 | `viscosity_index` | 92 – | **92 unitless** | Reported | DL2-10020.pdf p.2 | TDS DL2-10020.pdf 92 kept over the Petro-Canada marketing brochure (104), which is neither a TDS nor an SDS and is not in the archive. |
| Base oils | SHELL_RISELLA_X_415 | tier1 | `density` | 806 kg/m3 | **0.806 g/cm³** | Reported | DL2-13728.pdf p.1 | TDS preferred over SDS: TDS DL2-13728.pdf 806 kg/m³ kept over SDS DL2-13729.pdf 803.5 kg/m³. |
| Base oils | SHELL_RISELLA_X_420 | tier1 | `density` | 816 kg/m3 | **0.816 g/cm³** | Reported | DL2-13726.pdf p.1 | TDS preferred over SDS: TDS DL2-13726.pdf 816 kg/m³ kept over SDS DL2-13730.pdf 813.8 kg/m³. |
| Base oils | SHELL_RISELLA_X_430 | tier1 | `density` | 828 kg/m3 | **0.828 g/cm³** | Reported | DL2-13727.pdf p.1 | TDS preferred over SDS: TDS DL2-13727.pdf 828 kg/m³ kept over SDS DL2-13731.pdf 824.8 kg/m³. |

### 2b. Conflict records marked resolved

Every resolved entry of the `conflicts` arrays (duplicates across tier files listed once). Entries pointing to a property are detailed in 2a; the others needed no value change, e.g. claim conflicts where the fields already held the newest edition.

| Class | Product | Tier | Recorded conflict | Final resolution |
|---|---|---|---|---|
| Additive packages | AFTON_HITEC_12200 | tier1 | {"field": "tier1.performance_claims / tier1.treat_rate_matrix (MTU 2.0, row 10.3% + 5.0% HiTEC® 12255, SAE 15W-40, GP I)", "values": [{"value": "MTU 2.0 claimed", "printed_text": "dot in MTU 2.0 column", "file": "DL2-11412.PDF", "page": 2, "revision_date": "05/18"}, {"value": "MTU 2.0 not claimed", "printed_text": "no dot in MTU 2.0 column", "file": "DL2-14639.pdf", "page": 2, "revision_date": "08/18"}], "note": "05/18 vs 08/18 bulletin. Newer (08/18) used in the fields; not resolved."} | Same document type; newest edition used (08/18 bulletin: not claimed); text value, not averaged. Fields already hold it. |
| Additive packages | AFTON_HITEC_12200 | tier1 | {"field": "tier1.performance_claims / tier1.treat_rate_matrix (DDC 93K215, row 11.7% + 0.9% HiTEC® 12260, SAE 10W-30, GP II)", "values": [{"value": "DDC 93K215 not claimed", "printed_text": "no dot in DDC 93K215 column", "file": "DL2-11412.PDF", "page": 2, "revision_date": "05/18"}, {"value": "DDC 93K215 claimed", "printed_text": "dot in DDC 93K215 column", "file": "DL2-14639.pdf", "page": 2, "revision_date": "08/18"}], "note": "05/18 vs 08/18 bulletin. Newer (08/18) used in the fields; not resolved."} | Same document type; newest edition used (08/18 bulletin: claimed); text value, not averaged. Fields already hold it. |
| Additive packages | INFINEUM_D3424 | tier2 | {"field": "tier2.flash_point", "values": [{"value": 190, "printed_text": "Flash Point (PM) 190 °C ASTM D 93", "file": "DL2-10204.pdf", "page": 1, "revision_date": "2004-11-09"}, {"value": 110, "printed_text": "Flash Point [Method]: >110C (230F) [ ASTM D-93]", "file": "DL2-10204.pdf", "page": 6, "revision_date": "2008-12-02"}], "note": "TDS typical (2004, p.1) vs SDS lower bound (2008, p.6; also p.3 Section 5). Values are compatible (190 > 110) but printed differently; per rule the field holds the more recent SDS value. Not resolved."} | TDS preferred over SDS; see fields.flash_point.resolution. |
| Additive packages | LUBRIZOL_CV7540 | tier1 | {"field": "tier1.performance_claims (Cummins CES 20076 claim code)", "values": [{"value": "L", "printed_text": "Cummins CES 20076 L", "file": "DL2-14638.pdf", "page": 1, "revision_date": "2020-01-20"}, {"value": "A", "printed_text": "Cummins CES 20076 A", "file": "DL2-15581.pdf", "page": 1, "revision_date": "2022-05-13"}], "note": "2020 sheet: 'L - Licensable'; 2022 sheet: 'A - Approved'. Fields use the newer 2022 sheet. Not resolved."} | Same document type; newest edition used (2022 sheet: 'A - Approved'); text value, not averaged. |
| Additive packages | LUBRIZOL_CV7540 | tier1 | {"field": "tier1.performance_claims (Cummins CES 20077 claim code)", "values": [{"value": "L", "printed_text": "Cummins CES 20077 L", "file": "DL2-14638.pdf", "page": 1, "revision_date": "2020-01-20"}, {"value": "A", "printed_text": "Cummins CES 20077 A", "file": "DL2-15581.pdf", "page": 1, "revision_date": "2022-05-13"}], "note": "2020 sheet: 'L - Licensable'; 2022 sheet: 'A - Approved'. Fields use the newer 2022 sheet. Not resolved."} | Same document type; newest edition used (2022 sheet: 'A - Approved'); text value, not averaged. |
| Additive packages | LUBRIZOL_CV7540 | tier1 | {"field": "tier1.performance_claims (Cummins CES 20078 claim code)", "values": [{"value": "L", "printed_text": "Cummins CES 20078 L", "file": "DL2-14638.pdf", "page": 1, "revision_date": "2020-01-20"}, {"value": "A", "printed_text": "Cummins CES 20078 A", "file": "DL2-15581.pdf", "page": 1, "revision_date": "2022-05-13"}], "note": "2020 sheet: 'L - Licensable'; 2022 sheet: 'A - Approved'. Fields use the newer 2022 sheet. Not resolved."} | Same document type; newest edition used (2022 sheet: 'A - Approved'); text value, not averaged. |
| Additive packages | RICHFUL_RF6066 | tier2 | {"field": "tier2.density", "values": [{"value": 990, "printed_text": "Density( 20℃), kg/m3 990 GB/T13377，ASTMD4052", "file": "DL2-13819.pdf", "page": 1, "revision_date": null}, {"value": 988, "printed_text": "Density (20℃), kg/m3 968-1008 988 SH/T 0604, ASTM D4052", "file": "DL2-15451.pdf", "page": 1, "revision_date": null}, {"value": 990, "printed_text": "Density 990 kg/m3", "file": "DL2-13820.pdf", "page": 5, "revision_date": "2020-07-06"}, {"value": 0.988, "printed_text": "Density : 0.988 g/cm³ (20 °C)", "file": "DL2-15831.pdf", "page": 5, "revision_date": "2021-09-02"}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved."} | See fields.density.resolution. |
| Additive packages | RICHFUL_RF6066 | tier2 | {"field": "tier2.kv100", "values": [{"value": 227, "printed_text": "Kinematic Viscosity, ( 100℃), mm2/s 227 GB/T265，ASTMD445", "file": "DL2-13819.pdf", "page": 1, "revision_date": null}, {"value": 185, "printed_text": "Kinematic Viscosity (100℃), mm2/s Report 185 GB/T 265, ASTM D445", "file": "DL2-15451.pdf", "page": 1, "revision_date": null}, {"value": 200, "printed_text": "Kinematic viscosity 200 mm2/s (100 °C)", "file": "DL2-13820.pdf", "page": 5, "revision_date": "2020-07-06"}, {"value": 185, "printed_text": "Viscosity, dynamic : 185 mm²/s (100 °C)", "file": "DL2-15831.pdf", "page": 5, "revision_date": "2021-09-02"}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved."} | See fields.kv100.resolution. |
| Additive packages | RICHFUL_RF6066 | tier2 | {"field": "tier2.tbn", "values": [{"value": 106, "printed_text": "Total Base Number, mgKOH/g 106 SH/T0251，ASTMD2896", "file": "DL2-13819.pdf", "page": 1, "revision_date": null}, {"value": 108, "printed_text": "Total Base Number, mgKOH/g 97-119 108 SH/T 0251, ASTM D2896", "file": "DL2-15451.pdf", "page": 1, "revision_date": null}, {"value": 106, "printed_text": "Total base number 106 mgKOH/g", "file": "DL2-13820.pdf", "page": 5, "revision_date": "2020-07-06"}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved."} | See fields.tbn.resolution. |
| Additive packages | RICHFUL_RF6066 | tier2 | {"field": "tier2.elements.Zn", "values": [{"value": 1.3, "printed_text": "Zn Content, %（m/m） 1.3 GB/T17476，ASTM D4951", "file": "DL2-13819.pdf", "page": 1, "revision_date": null}, {"value": 1.24, "printed_text": "Zn Content, m% 1.13-1.38 1.24 GB/T 17476, ASTM D4951", "file": "DL2-15451.pdf", "page": 1, "revision_date": null}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved."} | See fields.elements.Zn.resolution. |
| Additive packages | RICHFUL_RF6066 | tier2 | {"field": "tier2.elements.Ca", "values": [{"value": 3.0, "printed_text": "Ca Content,%（m/m） 3.0 GB/T17476，ASTM D4951", "file": "DL2-13819.pdf", "page": 1, "revision_date": null}, {"value": 3.15, "printed_text": "Ca Content, m% 2.82-3.44 3.15 GB/T 17476, ASTM D4951", "file": "DL2-15451.pdf", "page": 1, "revision_date": null}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved."} | See fields.elements.Ca.resolution. |
| Additive packages | RICHFUL_RF6069 | tier2 | {"field": "tier2.kv100", "values": [{"value": 118, "printed_text": "Kinematic Viscosity (100℃), mm2/s Report 118 GB/T 265, ASTM D445", "file": "DL2-15618.pdf", "page": 1, "revision_date": null}, {"value": 142, "printed_text": "Viscosity, kinematic : 142 mm²/s (100 °C, ASTM D445)", "file": "DL2-15619.pdf", "page": 5, "revision_date": "2022-01-04"}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved."} | See fields.kv100.resolution. |
| Additive packages | RICHFUL_RF6077 | tier2 | {"field": "tier2.density", "values": [{"value": 998.0, "printed_text": "Density (20℃), kg/m3 978-1018 998 GB/T 13377, ASTM D4052", "file": "DL2-15536.pdf", "page": 1, "revision_date": null}, {"value": 0.991, "printed_text": "Density : 0.991 g/cm3 (15 °C)", "file": "DL2-15542.pdf", "page": 5, "revision_date": "2023-11-16"}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved. Resolved 2026-10-18 by user decision: 0.991 g/cm³ from DL2-15542.pdf used."} | User decision of 2026-10-18 kept; see fields.density.resolution. |
| Additive packages | RICHFUL_RF6077 | tier2 | {"field": "tier2.kv100", "values": [{"value": 160.0, "printed_text": "Kinematic Viscosity (100℃), mm2/s Report 160 GB/T 265, ASTM D445", "file": "DL2-15536.pdf", "page": 1, "revision_date": null}, {"value": 150, "printed_text": "Viscosity, kinematic : 150mm2/s (100 °C)", "file": "DL2-15542.pdf", "page": 5, "revision_date": "2023-11-16"}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved. Resolved 2026-10-18 by user decision: 150 mm²/s from DL2-15542.pdf used."} | User decision of 2026-10-18 kept; see fields.kv100.resolution. |
| Additive packages | RICHFUL_RF6078 | tier1 | {"field": "tier1.treat_rate_matrix (ACEA E7/API CI-4)", "values": [{"value": 11.85, "printed_text": "ACEA E7/API CI-4 10W-30, 10W-40, 15W-40, 20W-50 11.85%", "file": "DL2-15832.pdf", "page": 1, "revision_date": null}, {"value": 10.85, "printed_text": "ACEA E7/API CI-4 10W-30, 10W-40, 15W-40, 20W-50 10.85%", "file": "RF6078%20-%20TDS.pdf", "page": 1, "revision_date": null}], "note": "Both TDS undated; DL2-15832.pdf lists API CI-4 alone at 10.85%, 'RF6078 - TDS.pdf' lists API CI-4 Plus at 11.85%. Not resolved."} | See fields.treat_rate_matrix[0].treat_rate_wt_pct.resolution. The 'values' in this entry are correct; the note text has the two files swapped. |
| Additive packages | RICHFUL_RF6078 | tier2 | {"field": "tier2.density", "values": [{"value": 972.0, "printed_text": "Density (20℃), kg/m3 952-992 972 GB/T 13377, ASTM D4052", "file": "DL2-15832.pdf", "page": 1, "revision_date": null}, {"value": 972.0, "printed_text": "Density (20℃), kg/m3 952-992 972 SH/T 0604, ASTM D4052", "file": "RF6078%20-%20TDS.pdf", "page": 1, "revision_date": null}, {"value": 975, "printed_text": "Density : 975 kg/m³ (20 °C, ASTM D4052)", "file": "DL2-15833.pdf", "page": 5, "revision_date": "2021-09-02"}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved."} | See fields.density.resolution. |
| Additive packages | RICHFUL_RF6081 | tier2 | {"field": "tier2.kv100", "values": [{"value": 132.0, "printed_text": "Kinematic Viscosity (100℃), mm2/s Report 132 ASTM D445", "file": "DL2-15836.pdf", "page": 2, "revision_date": "2025-05-13"}, {"value": 130, "printed_text": "Viscosity, kinematic : 130 mm2/s (100 °C)", "file": "DL2-15837.pdf", "page": 5, "revision_date": "2025-04-09"}], "note": "All documents dated; field holds the most recent (DL2-15836.pdf). Not resolved."} | See fields.kv100.resolution. |
| Additive packages | RICHFUL_RF6088F | tier2 | {"field": "tier2.density", "values": [{"value": 963.0, "printed_text": "Density (20℃), kg/m3 943-983 963 SH/T 0604，ASTM D4052", "file": "DL2-15839.pdf", "page": 1, "revision_date": null}, {"value": 0.958, "printed_text": "Relative density : 0.958 g/cm3@20℃", "file": "DL2-15840.pdf", "page": 5, "revision_date": "2024-10-17"}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved. Resolved 2026-10-18 by user decision: 963.0 kg/m³ from DL2-15839.pdf used."} | User decision of 2026-10-18 kept; see fields.density.resolution. |
| Additive packages | RICHFUL_RF6088F | tier2 | {"field": "tier2.kv100", "values": [{"value": 177.0, "printed_text": "Kinematic Viscosity (100℃), mm2/s Report 177 GB/T 265，ASTM D445", "file": "DL2-15839.pdf", "page": 1, "revision_date": null}, {"value": 178.2, "printed_text": "Viscosity, kinematic : 178.2 mm2/s @100℃", "file": "DL2-15840.pdf", "page": 5, "revision_date": "2024-10-17"}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved. Resolved 2026-10-18 by user decision: 178.2 mm²/s from DL2-15840.pdf used."} | User decision of 2026-10-18 kept; see fields.kv100.resolution. |
| Additive packages | RICHFUL_RF6406 | tier1 | {"field": "tier1.treat_rate_matrix (API CF/SF, Multi)", "values": [{"value": 4.1, "printed_text": "CF/SF Multi 4.1%", "file": "DL2-15456.pdf", "page": 1, "revision_date": null}, {"value": 3.7, "printed_text": "CF/SF （Multi） 3.7", "file": "DL2-14746.pdf", "page": 1, "revision_date": null}], "note": "Both TDS undated; not resolved."} | See fields.treat_rate_matrix[10].treat_rate_wt_pct.resolution. |
| Additive packages | RICHFUL_RF6406 | tier2 | {"field": "tier2.tbn", "values": [{"value": 185.0, "printed_text": "Total Base Number, mgKOH/g 168-198 185 SH/T0251, ASTM D2896", "file": "DL2-15456.pdf", "page": 1, "revision_date": null}, {"value": 180, "printed_text": "Total Base Number，mgKOH/g ≥180 SH/T0251，ASTMD2896", "file": "DL2-14746.pdf", "page": 1, "revision_date": null}], "note": "At least one document is undated, so the most recent cannot be determined; field left null. Not resolved."} | See fields.tbn.resolution. |
| Base oils | ARAMCO_LUBEREF_DURA_BS150_YANBU | tier1 | {"field": "density", "note": "The 0.894 kg/L typical density is at 15.6°C (DL2-13944), not 15°C; do not treat it as a 15°C measurement."} | No value conflict: a note that the density is at 15.6 °C, not 15 °C. |
| Base oils | FORMOSA_150N_GII_PLUS | tier2 | {"field": "flash_point", "source_a": {"file": "DL2-10001.pdf", "page": 1, "value": "minimum 210 C"}, "source_b": {"file": "DL2-10011.pdf", "page": 3, "value": ">230 C"}, "note": "SDS and specification use different threshold statements; preserve both without assuming equivalence."} | TDS preferred over SDS; see tier2 fields.flash_point.resolution. |
| Base oils | NYNAS_NS_3 | tier1 | {"property": "kv40", "primary": {"value": 2.92, "source_file": "DL2-15474.pdf", "page": 2}, "alternate": {"value": 2.84, "source_file": "DL2-12382.pdf", "page": 2}, "note": "Different typical values in 2024 and 2016 editions; newer edition selected."} | Same document type; newest edition used; see tier1 fields.kv40.resolution. |
| Base oils | NYNAS_NS_3 | tier1 | {"property": "density", "primary": {"value": 0.863, "source_file": "DL2-15474.pdf", "page": 2}, "alternate": {"value": 0.86, "source_file": "DL2-12382.pdf", "page": 2}, "note": "Different typical values in 2024 and 2016 editions."} | Same document type; newest edition used; see tier1 fields.density.resolution. |
| Base oils | NYNAS_NS_3 | tier1 | {"property": "flash_point", "primary": {"value": 95, "source_file": "DL2-15474.pdf", "page": 2}, "alternate": {"value": 94, "source_file": "DL2-12382.pdf", "page": 2}, "note": "Different typical PM flash points in two editions."} | Same document type; newest edition used; see tier2 fields.flash_point.resolution. |
| Base oils | NYNAS_NS_3 | tier1 | {"property": "sulfur", "primary": {"value": "<10 ppm", "source_file": "DL2-15474.pdf", "page": 2}, "alternate": {"value": "30 ppm", "source_file": "DL2-12382.pdf", "page": 2}, "note": "Older typical 30 ppm versus newer upper-bound <10 ppm; not interchangeable."} | Same document type; newest edition used; see tier3 fields.sulfur.resolution. |
| Base oils | NYNAS_NYFROST_32 | tier1 | {"property": "kv40", "source_a": "DL2-11510.pdf p.2 (2016-11-01)", "value_a": "32 cSt (typical)", "source_b": "DL2-13444.pdf p.6 (2020-05-23)", "value_b": "31 cSt (SDS)", "resolution": "Retained supplier PDS typical value; SDS discrepancy flagged."} | TDS preferred over SDS; see tier1 fields.kv40.resolution. |
| Base oils | NYNAS_NYFROST_32 | tier1 | {"property": "flash_point", "source_a": "DL2-11510.pdf p.2 (2016-11-01)", "value_a": "176°C typical, Pensky-Martens (ASTM D93)", "source_b": "DL2-13444.pdf p.6 (2020-05-23)", "value_b": ">180°C closed cup Pensky-Martens", "resolution": "Not numerically compatible; PDS typical retained and SDS limit flagged for review."} | TDS preferred over SDS; see tier2 fields.flash_point.resolution. |
| Base oils | PETRONAS_ETRO_6_PLUS | tier1 | {"property": "kv40", "primary_source": "DL2-10234.pdf", "primary_value": "32.55 cSt at 40°C (ASTM D445)", "comparison_source": "DL2-14610.pdf", "comparison_value": "34.79 mm²/s at 40°C (ASTM D445), page 4", "assessment": "Different reported values; retain TDS typical value, flag for review."} | TDS preferred over SDS; see tier1 fields.kv40.resolution. |
| Base oils | PETRONAS_ETRO_6_PLUS | tier1 | {"property": "flash_point", "primary_source": "DL2-10234.pdf", "primary_value": "240°C ASTM D92 (COC)", "comparison_source": "DL2-14610.pdf", "comparison_value": "228°C ASTM D93 (PMCC), page 3", "assessment": "Different methods, not directly comparable; both values retained."} | TDS preferred over SDS; see tier2 fields.flash_point.resolution. |
| Base oils | PETRONAS_ETRO_6_PLUS | tier1 | {"property": "noack_volatility", "primary_source": "DL2-10234.pdf", "primary_value": "5.7 mass% ASTM D5800-B", "comparison_source": "DL2-14610.pdf", "comparison_value": "5.3 mass% ASTM D5800 B, page 4", "assessment": "Different reported values; retain TDS typical value, flag for review."} | TDS preferred over SDS; see tier2 fields.noack_volatility.resolution. |
| Base oils | PETRONAS_ETRO_6_PLUS | tier1 | {"property": "density", "primary_source": "DL2-10234.pdf", "primary_value": "0.8429 kg/L (temperature not stated)", "comparison_source": "DL2-14610.pdf", "comparison_value": "0.8486 g/cm³ at 15°C ASTM D4052, page 4", "assessment": "TDS lacks measurement temperature; SDS has a stated temperature and is used in the density field, with its own source."} | TDS preferred over SDS; see tier1 fields.density.resolution. |
| Base oils | PETRO_CANADA_PURITY_L65 | tier1 | {"note": "Viscosity index differs between manufacturer documents: DL2-10020.pdf (2015-07), page 2, reports 92; Petro-Canada's World-Class Base Oils brochure reports 104. The original value of 92 is retained pending reconciliation."} | TDS kept; see tier1 fields.viscosity_index.resolution. |
| Base oils | SHELL_RISELLA_X_415 | tier1 | {"field": "density", "tds": {"value": 806, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13728.pdf", "page": 1}, "sds": {"value": 803.5, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13729.pdf", "page": 8, "revision_date": "2018-10-26"}, "note": "Different reported values at same temperature; TDS selected as primary, SDS retained for reconciliation."} | TDS preferred over SDS; see tier1 fields.density.resolution. |
| Base oils | SHELL_RISELLA_X_420 | tier1 | {"field": "density", "tds": {"value": 816, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13726.pdf", "page": 1, "revision_date": "2014-06-02"}, "sds": {"value": 813.8, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13730.pdf", "page": 8, "revision_date": "2018-10-26"}, "note": "Different supplier-reported values at same temperature; TDS retained as primary, SDS separately documented."} | TDS preferred over SDS; see tier1 fields.density.resolution. |
| Base oils | SHELL_RISELLA_X_430 | tier1 | {"field": "density", "tds": {"value": 828, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13727.pdf", "page": 1, "revision_date": "2014-06-02"}, "sds": {"value": 824.8, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13731.pdf", "page": 7, "revision_date": "2020-01-13"}, "note": "Different supplier-reported values at same temperature; TDS retained as primary, SDS separately documented."} | TDS preferred over SDS; see tier1 fields.density.resolution. |

### 2c. value_final corrected or left null during unit integration

| Class | Product | Tier | Property | Printed | value | value_final | Note |
|---|---|---|---|---|---|---|---|
| Additive packages | TIANHE_P_TEC_3232 | tier2 | `density` | Density, kg/m3, at 15℃ 1.0130 ASTM D4052 | 1.013 kg/m3 | – g/cm³ | converted density 0.001013 g/cm³ is outside 0.6-1.3, so the printed number and unit disagree; value_final left null until checked |
| Base oils | ARAMCO_LUBEREF_PRIMA_110 | tier1 | `density` | 850 | 0.85 kg/m3 | 0.85 g/cm³ | value field 0.85 does not match printed text '850' in kg/m3; value_final taken from the printed text |

## 3. Reported numeric values with no test method, no unit or no reference temperature

401 reported numeric values: 347 with no method, 4 with no unit, 55 with no reference temperature. A reference temperature is checked only where the property needs one (ccs, ccs_viscosity, delta_kv100_cst, density, hths, kv100, kv40, mrv, mrv_viscosity, noack_volatility, yield_stress); viscosity index and shear stability index are unitless. Treat rates, doses and composition shares are recommendations, not test results, so they are checked for a unit but not for a method. For Noack the method itself fixes 250 °C / 1 h, but the temperature is still listed when it is not recorded.

### Base oils (194)

| Product | Tier | Property | Value | Unit | Missing |
|---|---|---|---|---|---|
| ADNOC_ADBASE_2CST | tier1 | `kv40` | 7.5 | cSt | method |
| ADNOC_ADBASE_2CST | tier1 | `kv100` | 2.3 | cSt | method |
| ADNOC_ADBASE_2CST | tier1 | `viscosity_index` | 115 | unitless | method |
| ADNOC_ADBASE_2CST | tier1 | `density` | 0.823 | g/cm³ | method |
| ADNOC_ADBASE_2CST | tier2 | `pour_point` | -27 | °C | method |
| ADNOC_ADBASE_2CST | tier2 | `flash_point` | 170 | °C | method |
| ADNOC_ADBASE_2CST | tier3 | `sulfur` | 0.0003 | wt.% | method |
| ADNOC_ADBASE_2CST | tier3 | `saturates` | 99.8 | wt.% | method |
| ADNOC_ADBASE_2CST | tier3 | `aromatics` | 0.2 | wt.% | method |
| ADNOC_ADBASE_3CST | tier1 | `kv40` | 12 | cSt | method |
| ADNOC_ADBASE_3CST | tier1 | `kv100` | 3.05 | cSt | method |
| ADNOC_ADBASE_3CST | tier1 | `viscosity_index` | 120 | unitless | method |
| ADNOC_ADBASE_3CST | tier1 | `density` | 0.825 | g/cm³ | method |
| ADNOC_ADBASE_3CST | tier2 | `pour_point` | -24 | °C | method |
| ADNOC_ADBASE_3CST | tier2 | `flash_point` | 190 | °C | method |
| ADNOC_ADBASE_3CST | tier3 | `sulfur` | 0.0003 | wt.% | method |
| ADNOC_ADBASE_3CST | tier3 | `saturates` | 99.8 | wt.% | method |
| ADNOC_ADBASE_3CST | tier3 | `aromatics` | 0.2 | wt.% | method |
| ADNOC_ADBASE_4CST | tier1 | `kv40` | 20 | cSt | method |
| ADNOC_ADBASE_4CST | tier1 | `kv100` | 4.35 | cSt | method |
| ADNOC_ADBASE_4CST | tier1 | `viscosity_index` | 130 | unitless | method |
| ADNOC_ADBASE_4CST | tier1 | `density` | 0.832 | g/cm³ | method |
| ADNOC_ADBASE_4CST | tier1 | `ccs[0]` | 1400 | mPa·s | method |
| ADNOC_ADBASE_4CST | tier2 | `noack_volatility` | 12.5 | wt.% | method, temperature |
| ADNOC_ADBASE_4CST | tier2 | `pour_point` | -18 | °C | method |
| ADNOC_ADBASE_4CST | tier2 | `flash_point` | 220 | °C | method |
| ADNOC_ADBASE_4CST | tier3 | `sulfur` | 0.0003 | wt.% | method |
| ADNOC_ADBASE_4CST | tier3 | `saturates` | 99.8 | wt.% | method |
| ADNOC_ADBASE_4CST | tier3 | `aromatics` | 0.2 | wt.% | method |
| ADNOC_ADBASE_6CST | tier1 | `kv40` | 34 | cSt | method |
| ADNOC_ADBASE_6CST | tier1 | `kv100` | 6.18 | cSt | method |
| ADNOC_ADBASE_6CST | tier1 | `viscosity_index` | 137 | unitless | method |
| ADNOC_ADBASE_6CST | tier1 | `density` | 0.844 | g/cm³ | method |
| ADNOC_ADBASE_6CST | tier1 | `ccs[0]` | 3700 | mPa·s | method |
| ADNOC_ADBASE_6CST | tier2 | `noack_volatility` | 6.8 | wt.% | method, temperature |
| ADNOC_ADBASE_6CST | tier2 | `pour_point` | -15 | °C | method |
| ADNOC_ADBASE_6CST | tier2 | `flash_point` | 235 | °C | method |
| ADNOC_ADBASE_6CST | tier3 | `sulfur` | 0.0003 | wt.% | method |
| ADNOC_ADBASE_6CST | tier3 | `saturates` | 99.8 | wt.% | method |
| ADNOC_ADBASE_6CST | tier3 | `aromatics` | 0.2 | wt.% | method |
| ADNOC_ADBASE_8CST | tier1 | `kv40` | 49 | cSt | method |
| ADNOC_ADBASE_8CST | tier1 | `kv100` | 8.05 | cSt | method |
| ADNOC_ADBASE_8CST | tier1 | `viscosity_index` | 137 | unitless | method |
| ADNOC_ADBASE_8CST | tier1 | `density` | 0.845 | g/cm³ | method |
| ADNOC_ADBASE_8CST | tier1 | `ccs[0]` | 8000 | mPa·s | method |
| ADNOC_ADBASE_8CST | tier2 | `noack_volatility` | 3.5 | wt.% | method, temperature |
| ADNOC_ADBASE_8CST | tier2 | `pour_point` | -12 | °C | method |
| ADNOC_ADBASE_8CST | tier2 | `flash_point` | 255 | °C | method |
| ADNOC_ADBASE_8CST | tier3 | `sulfur` | 0.0003 | wt.% | method |
| ADNOC_ADBASE_8CST | tier3 | `saturates` | 99.8 | wt.% | method |
| ADNOC_ADBASE_8CST | tier3 | `aromatics` | 0.2 | wt.% | method |
| GS_CALTEX_150BS | tier1 | `kv40` | 445.5 | cSt | temperature |
| GS_CALTEX_150BS | tier1 | `kv100` | 33.8 | cSt | temperature |
| GS_CALTEX_150N | tier1 | `kv40` | 28.81 | cSt | temperature |
| GS_CALTEX_150N | tier1 | `kv100` | 5.23 | cSt | temperature |
| GS_CALTEX_150N | tier2 | `noack_volatility` | 13.8 | wt.% | temperature |
| GS_CALTEX_220N | tier1 | `kv40` | 49.38 | cSt | temperature |
| GS_CALTEX_220N | tier1 | `kv100` | 7.23 | cSt | temperature |
| GS_CALTEX_220N | tier2 | `noack_volatility` | 6.8 | wt.% | temperature |
| GS_CALTEX_2CST_H | tier1 | `kv40` | 7.3 | cSt | temperature |
| GS_CALTEX_2CST_H | tier1 | `kv100` | 2.2 | cSt | temperature |
| GS_CALTEX_2CST_L | tier1 | `kv40` | 7.15 | cSt | temperature |
| GS_CALTEX_2CST_L | tier1 | `kv100` | 2.16 | cSt | temperature |
| GS_CALTEX_600N | tier1 | `kv40` | 107.05 | cSt | temperature |
| GS_CALTEX_600N | tier1 | `kv100` | 12.04 | cSt | temperature |
| GS_CALTEX_60N | tier1 | `kv40` | 7.73 | cSt | temperature |
| GS_CALTEX_60N | tier1 | `kv100` | 2.13 | cSt | temperature |
| CHEVRON_SYNFLUID_DIMER_C10 | tier1 | `kv40` | 4.9 | cSt | method |
| CHEVRON_SYNFLUID_DIMER_C10 | tier1 | `kv100` | 1.7 | cSt | method |
| CHEVRON_SYNFLUID_DIMER_C10 | tier2 | `pour_point` | -73 | °C | method |
| CHEVRON_SYNFLUID_DIMER_C12 | tier1 | `kv40` | 7.7 | cSt | method |
| CHEVRON_SYNFLUID_DIMER_C12 | tier1 | `kv100` | 2.3 | cSt | method |
| CHEVRON_SYNFLUID_DIMER_C12 | tier2 | `pour_point` | -63 | °C | method |
| CHEVRON_SYNFLUID_MPAO_100 | tier1 | `kv40` | 1023 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_100 | tier1 | `kv100` | 101 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_100 | tier1 | `viscosity_index` | 192.0 | unitless | method |
| CHEVRON_SYNFLUID_MPAO_100 | tier2 | `pour_point` | -44 | °C | method |
| CHEVRON_SYNFLUID_MPAO_100 | tier2 | `flash_point` | 265 | °C | method |
| CHEVRON_SYNFLUID_MPAO_150 | tier1 | `kv40` | 1719 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_150 | tier1 | `kv100` | 156 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_150 | tier1 | `viscosity_index` | 205.0 | unitless | method |
| CHEVRON_SYNFLUID_MPAO_150 | tier2 | `pour_point` | -39 | °C | method |
| CHEVRON_SYNFLUID_MPAO_150 | tier2 | `flash_point` | 278 | °C | method |
| CHEVRON_SYNFLUID_MPAO_40 | tier1 | `kv40` | 347 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_40 | tier1 | `kv100` | 41 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_40 | tier1 | `viscosity_index` | 172.0 | unitless | method |
| CHEVRON_SYNFLUID_MPAO_40 | tier2 | `pour_point` | -50 | °C | method |
| CHEVRON_SYNFLUID_MPAO_40 | tier2 | `flash_point` | 244 | °C | method |
| CHEVRON_SYNFLUID_MPAO_50 | tier1 | `kv40` | 405 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_50 | tier1 | `kv100` | 47 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_50 | tier1 | `viscosity_index` | 176.0 | unitless | method |
| CHEVRON_SYNFLUID_MPAO_50 | tier2 | `pour_point` | -50 | °C | method |
| CHEVRON_SYNFLUID_MPAO_50 | tier2 | `flash_point` | 253 | °C | method |
| CHEVRON_SYNFLUID_MPAO_65 | tier1 | `kv40` | 605 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_65 | tier1 | `kv100` | 65 | cSt | method |
| CHEVRON_SYNFLUID_MPAO_65 | tier1 | `viscosity_index` | 181.0 | unitless | method |
| CHEVRON_SYNFLUID_MPAO_65 | tier2 | `pour_point` | -46 | °C | method |
| CHEVRON_SYNFLUID_PAO_2 | tier1 | `kv40` | 5.1 | cSt | method |
| CHEVRON_SYNFLUID_PAO_2 | tier1 | `kv100` | 1.7 | cSt | method |
| CHEVRON_SYNFLUID_PAO_2 | tier2 | `pour_point` | -73 | °C | method |
| CHEVRON_SYNFLUID_PAO_2 | tier2 | `flash_point` | 159 | °C | method |
| CHEVRON_SYNFLUID_PAO_40 | tier1 | `kv40` | 410 | cSt | method |
| CHEVRON_SYNFLUID_PAO_40 | tier1 | `kv100` | 40 | cSt | method |
| CHEVRON_SYNFLUID_PAO_40 | tier1 | `viscosity_index` | 145.0 | unitless | method |
| CHEVRON_SYNFLUID_PAO_40 | tier2 | `pour_point` | -34 | °C | method |
| CHEVRON_SYNFLUID_PAO_40 | tier2 | `flash_point` | 294 | °C | method |
| CHEVRON_SYNFLUID_PAO_4 | tier1 | `kv40` | 16.8 | cSt | method |
| CHEVRON_SYNFLUID_PAO_4 | tier1 | `kv100` | 3.9 | cSt | method |
| CHEVRON_SYNFLUID_PAO_4 | tier1 | `viscosity_index` | 124.0 | unitless | method |
| CHEVRON_SYNFLUID_PAO_4 | tier2 | `noack_volatility` | 13.4 | wt.% | method |
| CHEVRON_SYNFLUID_PAO_4 | tier2 | `pour_point` | -68 | °C | method |
| CHEVRON_SYNFLUID_PAO_4 | tier2 | `flash_point` | 226 | °C | method |
| CHEVRON_SYNFLUID_PAO_5 | tier1 | `kv40` | 24.1 | cSt | method |
| CHEVRON_SYNFLUID_PAO_5 | tier1 | `kv100` | 5.1 | cSt | method |
| CHEVRON_SYNFLUID_PAO_5 | tier1 | `viscosity_index` | 144.0 | unitless | method |
| CHEVRON_SYNFLUID_PAO_5 | tier2 | `noack_volatility` | 5.5 | wt.% | method |
| CHEVRON_SYNFLUID_PAO_5 | tier2 | `pour_point` | -45 | °C | method |
| CHEVRON_SYNFLUID_PAO_5 | tier2 | `flash_point` | 245 | °C | method |
| CHEVRON_SYNFLUID_PAO_6 | tier1 | `kv40` | 30.5 | cSt | method |
| CHEVRON_SYNFLUID_PAO_6 | tier1 | `kv100` | 5.9 | cSt | method |
| CHEVRON_SYNFLUID_PAO_6 | tier1 | `viscosity_index` | 137.0 | unitless | method |
| CHEVRON_SYNFLUID_PAO_6 | tier2 | `noack_volatility` | 6.6 | wt.% | method |
| CHEVRON_SYNFLUID_PAO_6 | tier2 | `pour_point` | -61 | °C | method |
| CHEVRON_SYNFLUID_PAO_6 | tier2 | `flash_point` | 245 | °C | method |
| CHEVRON_SYNFLUID_PAO_6_HVI | tier1 | `kv40` | 29.1 | cSt | method |
| CHEVRON_SYNFLUID_PAO_6_HVI | tier1 | `kv100` | 5.9 | cSt | method |
| CHEVRON_SYNFLUID_PAO_6_HVI | tier1 | `viscosity_index` | 150.0 | unitless | method |
| CHEVRON_SYNFLUID_PAO_6_HVI | tier2 | `noack_volatility` | 4.9 | wt.% | method |
| CHEVRON_SYNFLUID_PAO_6_HVI | tier2 | `pour_point` | -44 | °C | method |
| CHEVRON_SYNFLUID_PAO_6_HVI | tier2 | `flash_point` | 249 | °C | method |
| CHEVRON_SYNFLUID_PAO_7 | tier1 | `kv40` | 37.3 | cSt | method |
| CHEVRON_SYNFLUID_PAO_7 | tier1 | `kv100` | 7 | cSt | method |
| CHEVRON_SYNFLUID_PAO_7 | tier1 | `viscosity_index` | 148.0 | unitless | method |
| CHEVRON_SYNFLUID_PAO_7 | tier2 | `noack_volatility` | 3.3 | wt.% | method |
| CHEVRON_SYNFLUID_PAO_7 | tier2 | `pour_point` | -42 | °C | method |
| CHEVRON_SYNFLUID_PAO_7 | tier2 | `flash_point` | 262 | °C | method |
| CHEVRON_SYNFLUID_PAO_8 | tier1 | `kv40` | 46.4 | cSt | method |
| CHEVRON_SYNFLUID_PAO_8 | tier1 | `kv100` | 7.8 | cSt | method |
| CHEVRON_SYNFLUID_PAO_8 | tier1 | `viscosity_index` | 138.0 | unitless | method |
| CHEVRON_SYNFLUID_PAO_8 | tier2 | `noack_volatility` | 3.5 | wt.% | method |
| CHEVRON_SYNFLUID_PAO_8 | tier2 | `pour_point` | -56 | °C | method |
| CHEVRON_SYNFLUID_PAO_8 | tier2 | `flash_point` | 262 | °C | method |
| CHEVRON_SYNFLUID_PAO_8_BLEND | tier1 | `kv40` | 46 | cSt | method |
| CHEVRON_SYNFLUID_PAO_8_BLEND | tier1 | `kv100` | 7.8 | cSt | method |
| CHEVRON_SYNFLUID_PAO_8_BLEND | tier1 | `viscosity_index` | 145.0 | unitless | method |
| CHEVRON_SYNFLUID_PAO_8_BLEND | tier2 | `noack_volatility` | 2.5 | wt.% | method |
| CHEVRON_SYNFLUID_PAO_8_BLEND | tier2 | `pour_point` | -45 | °C | method |
| CHEVRON_SYNFLUID_PAO_8_BLEND | tier2 | `flash_point` | 266 | °C | method |
| CHEVRON_SYNFLUID_PAO_9 | tier1 | `kv40` | 53.9 | cSt | method |
| CHEVRON_SYNFLUID_PAO_9 | tier1 | `kv100` | 9 | cSt | method |
| CHEVRON_SYNFLUID_PAO_9 | tier1 | `viscosity_index` | 146.0 | unitless | method |
| CHEVRON_SYNFLUID_PAO_9 | tier2 | `noack_volatility` | 2.2 | wt.% | method |
| CHEVRON_SYNFLUID_PAO_9 | tier2 | `pour_point` | -36 | °C | method |
| CHEVRON_SYNFLUID_PAO_9 | tier2 | `flash_point` | 276 | °C | method |
| FORMOSA_150N_GII_PLUS | tier1 | `kv40` | 29.3 | cSt | method |
| FORMOSA_150N_GII_PLUS | tier1 | `kv100` | 5.2 | cSt | method |
| FORMOSA_150N_GII_PLUS | tier1 | `density` | 0.85 | relative density | method |
| FORMOSA_500N_GII | tier1 | `kv40` | 85 | cSt | method |
| FORMOSA_500N_GII | tier1 | `kv100` | 11 | cSt | method |
| FORMOSA_500N_GII | tier1 | `density` | 0.87 | relative density | method |
| NESTE_NEXBASE_3043 | tier2 | `noack_volatility` | 14.2 | wt.% | temperature |
| NESTE_NEXBASE_3050 | tier2 | `noack_volatility` | 8.4 | wt.% | temperature |
| NESTE_NEXBASE_3060 | tier2 | `noack_volatility` | 7.2 | wt.% | temperature |
| NESTE_NEXBASE_3080 | tier2 | `noack_volatility` | 3.5 | wt.% | temperature |
| NYNAS_NYBASE_70 | tier2 | `noack_volatility` | 60 | wt.% | temperature |
| PETRONAS_EQUINAS_4 | tier2 | `noack_volatility` | 13.9 | wt.% | temperature |
| PETRONAS_EQUINAS_6 | tier1 | `kv40` | 32.56 | cSt | temperature |
| PETRONAS_EQUINAS_6 | tier1 | `kv100` | 6.08 | cSt | temperature |
| PETRONAS_EQUINAS_6 | tier2 | `noack_volatility` | 5.9 | wt.% | temperature |
| PETRONAS_EQUINAS_8 | tier2 | `noack_volatility` | 4 | wt.% | temperature |
| PETRONAS_ETRO_3 | tier2 | `noack_volatility` | 42 | wt.% | temperature |
| PETRONAS_ETRO_4 | tier2 | `noack_volatility` | 13.8 | wt.% | temperature |
| PETRONAS_ETRO_4_PLUS | tier2 | `noack_volatility` | 13.2 | wt.% | temperature |
| PETRONAS_ETRO_6 | tier2 | `noack_volatility` | 7.1 | wt.% | temperature |
| PETRONAS_ETRO_6_PLUS | tier1 | `density` | 0.8429 | g/cm³ | temperature |
| PETRONAS_ETRO_6_PLUS | tier2 | `noack_volatility` | 5.7 | wt.% | temperature |
| PETRONAS_M500 | tier2 | `noack_volatility` | 2.5 | wt.% | temperature |
| PETRO_CANADA_PURITY_1003 | tier2 | `noack_volatility` | 15.5 | wt.% | temperature |
| PETRO_CANADA_PURITY_1017 | tier2 | `noack_volatility` | 22.4 | wt.% | temperature |
| PETRO_CANADA_PURITY_1020 | tier2 | `noack_volatility` | 33.6 | wt.% | temperature |
| PETRO_CANADA_PURITY_2204 | tier2 | `noack_volatility` | 10 | wt.% | temperature |
| PETRO_CANADA_PURITY_2305 | tier2 | `noack_volatility` | 10 | wt.% | temperature |
| PETRO_CANADA_PURITY_VHVI_2 | tier2 | `noack_volatility` | 60.2 | wt.% | temperature |
| PETRO_CANADA_PURITY_VHVI_3 | tier2 | `noack_volatility` | 30.2 | wt.% | temperature |
| PETRO_CANADA_PURITY_VHVI_4 | tier2 | `noack_volatility` | 12.2 | wt.% | temperature |
| PETRO_CANADA_PURITY_VHVI_6 | tier2 | `noack_volatility` | 9 | wt.% | temperature |
| PETRO_CANADA_PURITY_VHVI_8 | tier2 | `noack_volatility` | 4 | wt.% | temperature |
| S_OIL_ULTRA_S_4 | tier2 | `noack_volatility` | 14.5 | wt.% | temperature |
| S_OIL_ULTRA_S_6 | tier2 | `noack_volatility` | 8 | wt.% | temperature |
| S_OIL_ULTRA_S_8 | tier2 | `noack_volatility` | 4.1 | wt.% | temperature |
| YUBASE_3 | tier2 | `noack_volatility` | 40 | wt.% | temperature |
| YUBASE_4 | tier2 | `noack_volatility` | 15 | wt.% | temperature |
| YUBASE_5 | tier2 | `noack_volatility` | 12 | wt.% | temperature |
| YUBASE_6 | tier2 | `noack_volatility` | 7 | wt.% | temperature |

### Additive packages (205)

| Product | Tier | Property | Value | Unit | Missing |
|---|---|---|---|---|---|
| AFTON_HITEC_12010 | tier2 | `kv40` | 1313 | cSt | method |
| AFTON_HITEC_12010 | tier2 | `kv100` | 64 | cSt | method |
| AFTON_HITEC_12010 | tier2 | `density` | 1.044 | g/cm³ | method |
| AFTON_HITEC_12200 | tier2 | `tbn` | 103 | mg KOH/g | method |
| AFTON_HITEC_12200 | tier2 | `kv40` | 4100 | cSt | method |
| AFTON_HITEC_12200 | tier2 | `kv100` | 190 | cSt | method |
| AFTON_HITEC_12200 | tier2 | `density` | 0.989 | g/cm³ | method |
| AFTON_HITEC_12208 | tier2 | `tbn` | 62 | mg KOH/g | method |
| AFTON_HITEC_12208 | tier2 | `kv100` | 110 | cSt | method |
| AFTON_HITEC_12208 | tier2 | `density` | 0.9572 | g/cm³ | method |
| AFTON_HITEC_12210M | tier2 | `tbn` | 55 | mg KOH/g | method |
| AFTON_HITEC_12210M | tier2 | `kv40` | 1997 | cSt | method |
| AFTON_HITEC_12210M | tier2 | `kv100` | 108 | cSt | method |
| AFTON_HITEC_12210M | tier2 | `density` | 0.95 | g/cm³ | method |
| AFTON_HITEC_12210 | tier2 | `tbn` | 55 | mg KOH/g | method |
| AFTON_HITEC_12210 | tier2 | `kv100` | 108 | cSt | method |
| AFTON_HITEC_12210 | tier2 | `density` | 0.9466 | g/cm³ | method, temperature |
| AFTON_HITEC_12360 | tier2 | `tbn` | 61 | mg KOH/g | method |
| AFTON_HITEC_12360 | tier2 | `kv100` | 133 | cSt | method |
| AFTON_HITEC_12360 | tier2 | `density` | 0.951 | g/cm³ | method |
| AFTON_HITEC_12400 | tier2 | `tbn` | 61 | mg KOH/g | method |
| AFTON_HITEC_12400 | tier2 | `kv100` | 133 | cSt | method |
| AFTON_HITEC_12400 | tier2 | `density` | 0.951 | g/cm³ | method |
| AFTON_HITEC_8712 | tier2 | `kv40` | 1800 | cSt | method |
| AFTON_HITEC_8712 | tier2 | `kv100` | 95 | cSt | method |
| AFTON_HITEC_8712 | tier2 | `density` | 1.033 | g/cm³ | method, temperature |
| AFTON_HITEC_8788B | tier2 | `kv40` | 2850 | cSt | method |
| AFTON_HITEC_8788B | tier2 | `kv100` | 145 | cSt | method |
| AFTON_HITEC_8788B | tier2 | `density` | 0.958 | g/cm³ | method |
| AFTON_HITEC_8799B | tier2 | `kv40` | 3000 | cSt | method |
| AFTON_HITEC_8799B | tier2 | `kv100` | 145 | cSt | method |
| AFTON_HITEC_8799B | tier2 | `density` | 0.956 | g/cm³ | method |
| HiTEC_8766B | tier2 | `tbn` | 74 | mg KOH/g | method |
| HiTEC_8766B | tier2 | `kv100` | 140 | cSt | method |
| HiTEC_8766B | tier2 | `density` | 0.969 | g/cm³ | method |
| BRB_PETROLAD_8099 | tier2 | `elements.Ca` | 3.22 | wt.% | method |
| BRB_PETROLAD_8099 | tier2 | `elements.Zn` | 1.1 | wt.% | method |
| BRB_PETROLAD_8099 | tier2 | `elements.P` | 0.99 | wt.% | method |
| BRB_PETROLAD_8099 | tier2 | `elements.N` | 0.58 | wt.% | method |
| LUBRIZOL_16008 | tier2 | `tbn` | 182 | mg KOH/g | method |
| LUBRIZOL_16008 | tier2 | `sulfated_ash` | 26 | wt.% | method |
| LUBRIZOL_16008 | tier2 | `elements.Ca` | 6.8 | wt.% | method |
| LUBRIZOL_16008 | tier2 | `elements.Zn` | 2 | wt.% | method |
| LUBRIZOL_16008 | tier2 | `elements.P` | 1.82 | wt.% | method |
| LUBRIZOL_16008 | tier2 | `elements.N` | 0.26 | wt.% | method |
| LUBRIZOL_16008 | tier2 | `elements.S` | 4.8 | wt.% | method |
| LUBRIZOL_16008 | tier2 | `kv40` | 900 | cSt | method |
| LUBRIZOL_16008 | tier2 | `kv100` | 71 | cSt | method |
| LUBRIZOL_16008 | tier2 | `density` | 1.065 | specific gravity (dimensionless) | method |
| LUBRIZOL_16008 | tier2 | `pour_point` | -24 | °C | method |
| LUBRIZOL_3589C | tier2 | `sulfated_ash` | 25 | wt.% | method |
| LUBRIZOL_3589C | tier2 | `elements.Ca` | 6.56 | wt.% | method |
| LUBRIZOL_3589C | tier2 | `elements.Zn` | 1.91 | wt.% | method |
| LUBRIZOL_3589C | tier2 | `elements.P` | 1.72 | wt.% | method |
| LUBRIZOL_3589C | tier2 | `elements.N` | 0.3 | wt.% | method |
| LUBRIZOL_3589C | tier2 | `elements.S` | 4.86 | wt.% | method |
| LUBRIZOL_3589C | tier2 | `kv40` | 2234 | cSt | method |
| LUBRIZOL_3589C | tier2 | `kv100` | 116 | cSt | method |
| LUBRIZOL_3589C | tier2 | `density` | 1.069 | specific gravity (dimensionless) | method |
| LUBRIZOL_3589C | tier2 | `pour_point` | -15 | °C | method |
| LUBRIZOL_3700D | tier2 | `sulfated_ash` | 13.4 | wt.% | method |
| LUBRIZOL_3700D | tier2 | `elements.Ca` | 3.4 | wt.% | method |
| LUBRIZOL_3700D | tier2 | `elements.Zn` | 1.23 | wt.% | method |
| LUBRIZOL_3700D | tier2 | `elements.P` | 1.11 | wt.% | method |
| LUBRIZOL_3700D | tier2 | `elements.N` | 0.58 | wt.% | method |
| LUBRIZOL_3700D | tier2 | `elements.S` | 3.25 | wt.% | method |
| LUBRIZOL_3700D | tier2 | `kv40` | 2710 | cSt | method |
| LUBRIZOL_3700D | tier2 | `kv100` | 155 | cSt | method |
| LUBRIZOL_3700D | tier2 | `density` | 0.999 | specific gravity (dimensionless) | method |
| LUBRIZOL_3700D | tier2 | `pour_point` | -15 | °C | method |
| LUBRIZOL_3700 | tier2 | `sulfated_ash` | 12.6 | wt.% | method |
| LUBRIZOL_3700 | tier2 | `elements.Ca` | 3.2 | wt.% | method |
| LUBRIZOL_3700 | tier2 | `elements.Zn` | 1.15 | wt.% | method |
| LUBRIZOL_3700 | tier2 | `elements.P` | 1.05 | wt.% | method |
| LUBRIZOL_3700 | tier2 | `elements.N` | 0.53 | wt.% | method |
| LUBRIZOL_3700 | tier2 | `elements.S` | 3.07 | wt.% | method |
| LUBRIZOL_3700 | tier2 | `kv40` | 1950 | cSt | method |
| LUBRIZOL_3700 | tier2 | `kv100` | 116 | cSt | method |
| LUBRIZOL_3700 | tier2 | `density` | 0.981 | specific gravity (dimensionless) | method |
| LUBRIZOL_3700 | tier2 | `pour_point` | -21 | °C | method |
| LUBRIZOL_4986D | tier2 | `sulfated_ash` | 8.6 | wt.% | method |
| LUBRIZOL_4986D | tier2 | `elements.Ca` | 2.06 | wt.% | method |
| LUBRIZOL_4986D | tier2 | `elements.Zn` | 0.99 | wt.% | method |
| LUBRIZOL_4986D | tier2 | `elements.P` | 0.91 | wt.% | method |
| LUBRIZOL_4986D | tier2 | `elements.N` | 0.65 | wt.% | method |
| LUBRIZOL_4986D | tier2 | `elements.S` | 3.1 | wt.% | method |
| LUBRIZOL_4986D | tier2 | `kv40` | 1925 | cSt | method |
| LUBRIZOL_4986D | tier2 | `kv100` | 105 | cSt | method |
| LUBRIZOL_4986D | tier2 | `density` | 0.973 | specific gravity (dimensionless) | method |
| LUBRIZOL_4986D | tier2 | `pour_point` | -18 | °C | method |
| LUBRIZOL_4986E | tier2 | `sulfated_ash` | 9.1 | wt.% | method |
| LUBRIZOL_4986E | tier2 | `elements.Ca` | 2.26 | wt.% | method |
| LUBRIZOL_4986E | tier2 | `elements.Zn` | 0.97 | wt.% | method |
| LUBRIZOL_4986E | tier2 | `elements.P` | 0.89 | wt.% | method |
| LUBRIZOL_4986E | tier2 | `elements.N` | 0.64 | wt.% | method |
| LUBRIZOL_4986E | tier2 | `elements.S` | 3 | wt.% | method |
| LUBRIZOL_4986E | tier2 | `kv40` | 1860 | cSt | method |
| LUBRIZOL_4986E | tier2 | `kv100` | 112 | cSt | method |
| LUBRIZOL_4986E | tier2 | `density` | 0.973 | specific gravity (dimensionless) | method |
| LUBRIZOL_4986E | tier2 | `pour_point` | -18 | °C | method |
| LUBRIZOL_4986F | tier2 | `sulfated_ash` | 10.4 | wt.% | method |
| LUBRIZOL_4986F | tier2 | `elements.Ca` | 2.65 | wt.% | method |
| LUBRIZOL_4986F | tier2 | `elements.Zn` | 0.92 | wt.% | method |
| LUBRIZOL_4986F | tier2 | `elements.P` | 0.85 | wt.% | method |
| LUBRIZOL_4986F | tier2 | `elements.N` | 0.61 | wt.% | method |
| LUBRIZOL_4986F | tier2 | `elements.S` | 3 | wt.% | method |
| LUBRIZOL_4986F | tier2 | `kv40` | 1600 | cSt | method |
| LUBRIZOL_4986F | tier2 | `kv100` | 97 | cSt | method |
| LUBRIZOL_4986F | tier2 | `density` | 0.974 | specific gravity (dimensionless) | method |
| LUBRIZOL_4986F | tier2 | `pour_point` | -18 | °C | method |
| LUBRIZOL_4986G | tier2 | `sulfated_ash` | 9.6 | wt.% | method |
| LUBRIZOL_4986G | tier2 | `elements.Ca` | 2.39 | wt.% | method |
| LUBRIZOL_4986G | tier2 | `elements.Zn` | 0.96 | wt.% | method |
| LUBRIZOL_4986G | tier2 | `elements.P` | 0.88 | wt.% | method |
| LUBRIZOL_4986G | tier2 | `elements.N` | 0.63 | wt.% | method |
| LUBRIZOL_4986G | tier2 | `elements.S` | 3 | wt.% | method |
| LUBRIZOL_4986G | tier2 | `kv40` | 1900 | cSt | method |
| LUBRIZOL_4986G | tier2 | `kv100` | 115 | cSt | method |
| LUBRIZOL_4986G | tier2 | `density` | 0.976 | specific gravity (dimensionless) | method |
| LUBRIZOL_4986G | tier2 | `pour_point` | -18 | °C | method |
| LUBRIZOL_4986 | tier2 | `sulfated_ash` | 8.6 | wt.% | method |
| LUBRIZOL_4986 | tier2 | `elements.Ca` | 2.08 | wt.% | method |
| LUBRIZOL_4986 | tier2 | `elements.Zn` | 0.99 | wt.% | method |
| LUBRIZOL_4986 | tier2 | `elements.P` | 0.91 | wt.% | method |
| LUBRIZOL_4986 | tier2 | `elements.N` | 0.65 | wt.% | method |
| LUBRIZOL_4986 | tier2 | `elements.S` | 3.1 | wt.% | method |
| LUBRIZOL_4986 | tier2 | `kv40` | 1950 | cSt | method |
| LUBRIZOL_4986 | tier2 | `kv100` | 110 | cSt | method |
| LUBRIZOL_4986 | tier2 | `density` | 0.973 | specific gravity (dimensionless) | method |
| LUBRIZOL_4986 | tier2 | `pour_point` | -18 | °C | method |
| LUBRIZOL_4987 | tier2 | `sulfated_ash` | 9.1 | wt.% | method |
| LUBRIZOL_4987 | tier2 | `elements.Ca` | 2.26 | wt.% | method |
| LUBRIZOL_4987 | tier2 | `elements.Zn` | 0.91 | wt.% | method |
| LUBRIZOL_4987 | tier2 | `elements.P` | 0.84 | wt.% | method |
| LUBRIZOL_4987 | tier2 | `elements.N` | 0.6 | wt.% | method |
| LUBRIZOL_4987 | tier2 | `elements.S` | 3.1 | wt.% | method |
| LUBRIZOL_4987 | tier2 | `kv40` | 1650 | cSt | method |
| LUBRIZOL_4987 | tier2 | `kv100` | 100 | cSt | method |
| LUBRIZOL_4987 | tier2 | `density` | 0.973 | specific gravity (dimensionless) | method |
| LUBRIZOL_4987 | tier2 | `pour_point` | -21 | °C | method |
| LUBRIZOL_CV1100 | tier2 | `tbn` | 68 | mg KOH/g | method |
| LUBRIZOL_CV1100 | tier2 | `elements.Ca` | 1.705 | wt.% | method |
| LUBRIZOL_CV1100 | tier2 | `elements.P` | 0.71 | wt.% | method |
| LUBRIZOL_CV1100 | tier2 | `elements.N` | 0.912 | wt.% | method |
| LUBRIZOL_CV1100 | tier2 | `kv40` | 1305 | cSt | method |
| LUBRIZOL_CV1100 | tier2 | `kv100` | 80 | cSt | method |
| LUBRIZOL_CV1100 | tier2 | `density` | 0.952 | specific gravity (dimensionless) | method |
| LUBRIZOL_CV1100 | tier2 | `pour_point` | -21 | °C | method |
| LUBRIZOL_CV2301 | tier2 | `sulfated_ash` | 11.9 | wt.% | method |
| LUBRIZOL_CV2301 | tier2 | `elements.Ca` | 3.06 | wt.% | method |
| LUBRIZOL_CV2301 | tier2 | `elements.Zn` | 1.02 | wt.% | method |
| LUBRIZOL_CV2301 | tier2 | `elements.P` | 0.927 | wt.% | method |
| LUBRIZOL_CV2301 | tier2 | `elements.N` | 0.53 | wt.% | method |
| LUBRIZOL_CV2301 | tier2 | `kv40` | 1970 | cSt | method |
| LUBRIZOL_CV2301 | tier2 | `kv100` | 110 | cSt | method |
| LUBRIZOL_CV2301 | tier2 | `density` | 0.982 | specific gravity (dimensionless) | method |
| LUBRIZOL_CV2301 | tier2 | `pour_point` | -18 | °C | method |
| LUBRIZOL_CV2601 | tier2 | `sulfated_ash` | 6.5 | wt.% | method |
| LUBRIZOL_CV2601 | tier2 | `elements.Ca` | 0.823 | wt.% | method |
| LUBRIZOL_CV2601 | tier2 | `elements.Mg` | 0.521 | wt.% | method |
| LUBRIZOL_CV2601 | tier2 | `elements.Zn` | 0.537 | wt.% | method |
| LUBRIZOL_CV2601 | tier2 | `elements.P` | 0.498 | wt.% | method |
| LUBRIZOL_CV2601 | tier2 | `elements.B` | 0.123 | wt.% | method |
| LUBRIZOL_CV2601 | tier2 | `elements.N` | 0.886 | wt.% | method |
| LUBRIZOL_CV2601 | tier2 | `kv40` | 3800 | cSt | method |
| LUBRIZOL_CV2601 | tier2 | `kv100` | 175 | cSt | method |
| LUBRIZOL_CV2601 | tier2 | `density` | 0.955 | specific gravity (dimensionless) | method |
| LUBRIZOL_CV2601 | tier2 | `pour_point` | -12 | °C | method |
| LUBRIZOL_CV3515 | tier2 | `tbn` | 99 | mg KOH/g | method |
| LUBRIZOL_CV3515 | tier2 | `elements.Ca` | 2.706 | wt.% | method |
| LUBRIZOL_CV3515 | tier2 | `elements.P` | 0.702 | wt.% | method |
| LUBRIZOL_CV3515 | tier2 | `elements.N` | 0.977 | wt.% | method |
| LUBRIZOL_CV3515 | tier2 | `kv40` | 1347 | cSt | method |
| LUBRIZOL_CV3515 | tier2 | `kv100` | 76 | cSt | method |
| LUBRIZOL_CV3515 | tier2 | `density` | 0.972 | specific gravity (dimensionless) | method |
| LUBRIZOL_CV3515 | tier2 | `pour_point` | -18 | °C | method |
| MINGLAN_T3161 | tier1 | `treat_rate_matrix[0].treat_rate_wt_pct` | 12.0 | – | unit |
| MINGLAN_T3161 | tier1 | `treat_rate_matrix[1].treat_rate_wt_pct` | 11.0 | – | unit |
| MINGLAN_T3161 | tier1 | `treat_rate_matrix[2].treat_rate_wt_pct` | 9.0 | – | unit |
| MINGLAN_T3161 | tier1 | `treat_rate_matrix[3].treat_rate_wt_pct` | 7.0 | – | unit |
| CHEVRON_N204 | tier2 | `kv40` | 3890 | cSt | method |
| CHEVRON_N204 | tier2 | `density` | 0.985 | g/cm³ | method |
| CHEVRON_N216 | tier2 | `kv40` | 3320 | cSt | method |
| CHEVRON_N216 | tier2 | `density` | 0.9902 | g/cm³ | method |
| CHEVRON_OLOA_59230 | tier2 | `density` | 0.9927 | g/cm³ | method |
| CHEVRON_OLOA_59766 | tier2 | `kv40` | 2486 | cSt | method |
| CHEVRON_OLOA_59766 | tier2 | `density` | 0.9929 | g/cm³ | method |
| RICHFUL_RF6077 | tier2 | `kv100` | 150 | cSt | method |
| RICHFUL_RF6077 | tier2 | `density` | 0.991 | g/cm³ | method |
| RICHFUL_RF6079 | tier2 | `kv100` | 140 | cSt | method |
| RICHFUL_RF6079 | tier2 | `density` | 1 | g/cm³ | method |
| RICHFUL_RF6079 | tier2 | `flash_point` | 180 | °C | method |
| RICHFUL_RF6088F | tier2 | `kv100` | 178.2 | cSt | method |
| RICHFUL_RF6088F | tier2 | `flash_point` | 180 | °C | method |
| RICHFUL_RF6088 | tier2 | `kv100` | 100 | cSt | method |
| RICHFUL_RF6088 | tier2 | `density` | 0.955 | g/cm³ | method |
| RICHFUL_RF6088 | tier2 | `flash_point` | 180 | °C | method |
| RICHFUL_RF6089 | tier2 | `kv100` | 92 | cSt | method |
| RICHFUL_RF6089 | tier2 | `density` | 0.953 | g/cm³ | method |
| RICHFUL_RF6406 | tier2 | `kv100` | 72 | cSt | method |
| RICHFUL_RF6406 | tier2 | `density` | 1.06 | g/cm³ | method |
| SAMA_P2021A | tier2 | `tbn` | 71 | mg KOH/g | method |
| SAMA_P2021A | tier2 | `sulfated_ash` | 7.6 | wt.% | method |
| SAMA_P2021A | tier2 | `kv100` | 145 | cSt | method |
| SAMA_P2021A | tier2 | `density` | 0.958 | g/cm³ | method |

### Additive components (2)

| Product | Tier | Property | Value | Unit | Missing |
|---|---|---|---|---|---|
| AFTON_HITEC_8767B | tier1 | `function_specific_markers.tbn` | 38 | mg KOH/g | method |
| LUBRIZOL_CV6320 | tier1 | `function_specific_markers.tbn` | 1 | mg KOH/g | method |

## 4. Open questions

### Base oils

#### ADNOC_ADBASE_2CST
- (tier1) `ccs`: CCS is printed as '-' for 2 cSt: ask whether a value exists and at which temperature. (sources: DL2-12221.pdf)
- (tier1) `kv40; kv100; viscosity_index; density`: No test method is printed for KV40, KV100, VI and density on the brochure. (sources: DL2-12221.pdf)
- (tier2) `mrv`: MRV viscosity and yield stress are not reported anywhere for this product. (sources: DL2-12221.pdf)
- (tier2) `noack_volatility`: Noack is printed as '-' (not reported) for 2 cSt. (sources: DL2-12221.pdf)
- (tier2) `flash_point`: Flash point 170 deg C has no method (COC or PMCC): unusable until the method is confirmed. (sources: DL2-12221.pdf)
- (tier2) `pour_point`: Pour point has no test method printed. (sources: DL2-12221.pdf)
- (tier3) `cloud_point; wax_content`: Cloud point and wax content are not reported. (sources: DL2-12221.pdf)
- (tier3) `sulfur; saturates; aromatics`: Sulfur, saturates and aromatics have no test method printed. (sources: DL2-12221.pdf)

#### ADNOC_ADBASE_3CST
- (tier1) `ccs`: CCS is printed as '-' for 3 cSt. (sources: DL2-12221.pdf)
- (tier1) `kv40; kv100; viscosity_index; density`: No test method printed on the brochure for KV40, KV100, VI and density. (sources: DL2-12221.pdf)
- (tier2) `mrv`: MRV viscosity and yield stress not reported anywhere. (sources: DL2-12221.pdf)
- (tier2) `noack_volatility`: Noack is printed as '-' for 3 cSt. (sources: DL2-12221.pdf)
- (tier2) `flash_point`: Flash point 190 deg C has no method (COC/PMCC). (sources: DL2-12221.pdf)
- (tier2) `pour_point`: Pour point has no test method printed. (sources: DL2-12221.pdf)
- (tier3) `cloud_point; wax_content`: Cloud point and wax content not reported. (sources: DL2-12221.pdf)
- (tier3) `sulfur; saturates; aromatics`: Sulfur, saturates and aromatics have no test method printed. (sources: DL2-12221.pdf)

#### ADNOC_ADBASE_4CST
- (tier1) `kv40; kv100; viscosity_index; density`: No test method printed on the brochure for typical KV40, KV100, VI and density (spec sheet gives ASTM D445 / D2270 / D4052 for limits). (sources: DL2-12221.pdf; DL2-12420.jpg)
- (tier1) `api_group_chemistry.chemistry`: Chemistry is general knowledge only (sheet says Group III / high-purity base oil, not hydrocracked/mineral). (sources: DL2-12420.jpg)
- (tier2) `mrv`: MRV viscosity and yield stress are not reported anywhere. (sources: DL2-12221.pdf; DL2-12420.jpg)
- (tier2) `flash_point`: Flash point 220 deg C (brochure typical) has no method printed; the spec sheet's limit is COC. Confirm the typical value is also COC (COC and PMCC differ). (sources: DL2-12221.pdf; DL2-12420.jpg)
- (tier2) `noack_volatility`: Noack typical value has no test temperature/duration printed (spec sheet cites ASTM 5800 Method B). (sources: DL2-12221.pdf; DL2-12420.jpg)
- (tier3) `cloud_point; wax_content`: Cloud point and wax content are not reported. (sources: DL2-12221.pdf; DL2-12420.jpg)
- (tier3) `sulfur; saturates; aromatics`: Spec sheet gives sulfur only as a maximum limit (10 mg/kg); brochure typical is '<3' mg/kg. Saturates/aromatics 'Report' only on spec sheet: no method on the typical values. (sources: DL2-12221.pdf; DL2-12420.jpg)

#### ADNOC_ADBASE_6CST
- (tier1) `kv40; kv100; viscosity_index; density`: No test method printed on the brochure for typical KV40, KV100, VI and density (spec sheet gives ASTM D445 / D2270 / D4052 for limits). (sources: DL2-12221.pdf; DL2-12421.jpg)
- (tier1) `api_group_chemistry.chemistry`: Chemistry is general knowledge only (sheet says Group III / high-purity base oil, not hydrocracked/mineral). (sources: DL2-12421.jpg)
- (tier2) `mrv`: MRV viscosity and yield stress are not reported anywhere. (sources: DL2-12221.pdf; DL2-12421.jpg)
- (tier2) `flash_point`: Flash point 235 deg C (brochure typical) has no method printed; the spec sheet's limit is COC. Confirm the typical value is also COC (COC and PMCC differ). (sources: DL2-12221.pdf; DL2-12421.jpg)
- (tier2) `noack_volatility`: Noack typical value has no test temperature/duration printed (spec sheet cites ASTM 5800 Method B). (sources: DL2-12221.pdf; DL2-12421.jpg)
- (tier3) `cloud_point; wax_content`: Cloud point and wax content are not reported. (sources: DL2-12221.pdf; DL2-12421.jpg)
- (tier3) `sulfur; saturates; aromatics`: Spec sheet gives sulfur only as a maximum limit (10 mg/kg); brochure typical is '<3' mg/kg. Saturates/aromatics 'Report' only on spec sheet: no method on the typical values. (sources: DL2-12221.pdf; DL2-12421.jpg)

#### ADNOC_ADBASE_8CST
- (tier1) `kv40; kv100; viscosity_index; density`: No test method printed on the brochure for typical KV40, KV100, VI and density (spec sheet gives ASTM D445 / D2270 / D4052 for limits). (sources: DL2-12221.pdf; DL2-12468.jpg)
- (tier1) `api_group_chemistry.chemistry`: Chemistry is general knowledge only (sheet says Group III / high-purity base oil, not hydrocracked/mineral). (sources: DL2-12468.jpg)
- (tier2) `mrv`: MRV viscosity and yield stress are not reported anywhere. (sources: DL2-12221.pdf; DL2-12468.jpg)
- (tier2) `flash_point`: Flash point 255 deg C (brochure typical) has no method printed; the spec sheet's limit is COC. Confirm the typical value is also COC (COC and PMCC differ). (sources: DL2-12221.pdf; DL2-12468.jpg)
- (tier2) `noack_volatility`: Noack typical value has no test temperature/duration printed (spec sheet cites ASTM 5800 Method B). (sources: DL2-12221.pdf; DL2-12468.jpg)
- (tier3) `cloud_point; wax_content`: Cloud point and wax content are not reported. (sources: DL2-12221.pdf; DL2-12468.jpg)
- (tier3) `sulfur; saturates; aromatics`: Spec sheet gives sulfur only as a maximum limit (10 mg/kg); brochure typical is '<3' mg/kg. Saturates/aromatics 'Report' only on spec sheet: no method on the typical values. (sources: DL2-12221.pdf; DL2-12468.jpg)

#### ARAMCO_LUBEREF_DURA_150_JEDDAH
- (tier1) `kv100; density; ccs[]`: KV100, density and CCS are not reported in the reviewed source specifications. (sources: DL2-12173.pdf; DL2-15783.pdf)
- (tier2) `mrv[].mrv_viscosity; mrv[].yield_stress; noack_volatility`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12173.pdf; DL2-15783.pdf)
- (tier3) `saturates; aromatics; cloud_point; wax_content`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12173.pdf; DL2-15783.pdf)

#### ARAMCO_LUBEREF_DURA_500_JEDDAH
- (tier1) `kv100; density; ccs[]`: KV100, density and CCS are not reported in the reviewed source specifications. (sources: DL2-12173.pdf)
- (tier2) `mrv[].mrv_viscosity; mrv[].yield_stress; noack_volatility`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12173.pdf)
- (tier3) `saturates; aromatics; cloud_point; wax_content`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12173.pdf)

#### ARAMCO_LUBEREF_DURA_BS150_YANBU
- (tier1) `kv40; ccs[]`: KV40 and CCS are not reported in the reviewed source specifications. (sources: DL2-13944.pdf; DL2-12648.pdf; DL2-12173.pdf)
- (tier2) `mrv[].mrv_viscosity; mrv[].yield_stress; noack_volatility`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-13944.pdf; DL2-12648.pdf; DL2-12173.pdf)
- (tier3) `saturates; aromatics; cloud_point; wax_content`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-13944.pdf; DL2-12648.pdf; DL2-12173.pdf)

#### ARAMCO_LUBEREF_PRIMA_110
- (tier1) `kv100; ccs[]`: KV100 and CCS are not reported in the reviewed specifications. (sources: DL2-12172.pdf)
- (tier2) `mrv[].mrv_viscosity; mrv[].yield_stress`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12172.pdf)
- (tier3) `aromatics; cloud_point; wax_content`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12172.pdf)

#### ARAMCO_LUBEREF_PRIMA_230
- (tier2) `mrv[].mrv_viscosity; mrv[].yield_stress`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12172.pdf)
- (tier3) `aromatics; cloud_point; wax_content`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12172.pdf)

#### ARAMCO_LUBEREF_PRIMA_500
- (tier1) `kv40; ccs[]`: KV40 and CCS are not confirmed for the specific Luberef PRIMA 500 product represented by DL2-12172.pdf. (sources: DL2-12172.pdf)
- (tier2) `mrv[].mrv_viscosity; mrv[].yield_stress`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12172.pdf)
- (tier3) `aromatics; cloud_point; wax_content`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12172.pdf)

#### ARAMCO_LUBEREF_PRIMA_70
- (tier1) `kv40; density; ccs[]`: KV40, density and CCS are not reported in the reviewed source specifications. (sources: DL2-12172.pdf; DL2-15448.pdf)
- (tier2) `mrv[].mrv_viscosity; mrv[].yield_stress; noack_volatility`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12172.pdf; DL2-15448.pdf)
- (tier3) `aromatics; cloud_point; wax_content`: Not reported in reviewed source specifications; preserve as missing. (sources: DL2-12172.pdf; DL2-15448.pdf)

#### BAPCO_BAPBASE_4
- (tier1) `api_group_chemistry.chemistry`: Exact grade-specific chemistry and CAS number have not been verified from a BAPbase 4 SDS.
- (tier1) `density`: Original Bapco specification says 'To be reported'. An external Ergon catalog gives specific gravity 0.834 at 15/4°C, but no directly reported density in kg/m3 has been entered.
- (tier3) `cloud_point`: Document says To be reported; no value.

#### BAPCO_BAPBASE_6
- (tier1) `api_group_chemistry.chemistry`: Exact grade-specific chemistry and CAS number have not been verified from a BAPbase 6 SDS.
- (tier1) `density`: Original Bapco specification provides no numerical density. External Ergon/MOGO 2025 catalog reports specific gravity 0.839 at 15/4°C, but no directly reported density in kg/m3 has been entered.

#### BAPCO_BAPBASE_8
- (tier1) `api_group_chemistry.chemistry`: Exact grade-specific chemistry and CAS number have not been verified from a BAPbase 8 SDS.
- (tier1) `density`: Original Bapco specification says 'To be reported'. External Ergon/MOGO catalog reports specific gravity 0.847 at 15/4°C, but no directly reported density in kg/m3 has been entered.

#### GS_CALTEX_150BS
- (tier1) SDS not provided among the two supplier files; reconciliation pending.
- (tier1) No density, sulfur, saturates, CCS or MRV values stated in product specification.
- (tier2) SDS not provided among the two supplier files; reconciliation pending.
- (tier2) No density, sulfur, saturates, CCS or MRV values stated in product specification.
- (tier3) SDS not provided among the two supplier files; reconciliation pending.
- (tier3) No density, sulfur, saturates, CCS or MRV values stated in product specification.

#### GS_CALTEX_150N
- (tier1) SDS not supplied in the GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV and cloud point not stated in supplied specification.
- (tier2) SDS not supplied in the GS Caltex source folder; reconciliation pending.
- (tier2) Density, sulfur, saturates, CCS, MRV and cloud point not stated in supplied specification.
- (tier3) SDS not supplied in the GS Caltex source folder; reconciliation pending.
- (tier3) Density, sulfur, saturates, CCS, MRV and cloud point not stated in supplied specification.

#### GS_CALTEX_220N
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV and cloud point not stated in supplied specification.
- (tier2) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier2) Density, sulfur, saturates, CCS, MRV and cloud point not stated in supplied specification.
- (tier3) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier3) Density, sulfur, saturates, CCS, MRV and cloud point not stated in supplied specification.

#### GS_CALTEX_2CST_H
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.
- (tier2) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier2) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.
- (tier3) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier3) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.

#### GS_CALTEX_2CST_L
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.
- (tier2) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier2) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.
- (tier3) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier3) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.

#### GS_CALTEX_600N
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.
- (tier2) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier2) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.
- (tier3) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier3) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.

#### GS_CALTEX_60N
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.
- (tier2) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier2) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.
- (tier3) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier3) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.

#### CHEVRON_GROUP_II_100R
- (tier1) `density`: Not reported in supplier specification.
- (tier3) `sulfur`: Supplier says Report, without a numerical sulfur value.

#### CHEVRON_GROUP_II_110RLV
- (tier1) `density`: Not reported in supplier specification.
- (tier3) `sulfur`: Supplier says Report, without a numerical sulfur value.

#### CHEVRON_GROUP_II_150R
- (tier1) `density`: Not reported in supplier specification.
- (tier3) `sulfur`: Supplier says Report, without a numerical sulfur value.

#### CHEVRON_GROUP_II_220R
- (tier1) `density`: Not reported in supplier specification.
- (tier3) `sulfur`: Supplier says Report, without a numerical sulfur value.

#### CHEVRON_GROUP_II_600R
- (tier1) `density`: Not reported in supplier specification.
- (tier3) `sulfur`: Supplier says Report, without a numerical sulfur value.

#### CHEVRON_GROUP_II_60R
- (tier1) `api_group_chemistry.api_group`: 60R API group cell is blank in supplied table; heading alone is not an explicit classification.
- (tier1) `density`: Not reported in supplier specification.
- (tier3) `sulfur`: Supplier says Report, without a numerical sulfur value.

#### CHEVRON_SYNFLUID_DIMER_C10
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_DIMER_C12
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_MPAO_100
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_MPAO_150
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_MPAO_40
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_MPAO_50
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_MPAO_65
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_2
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_2_5
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_40
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_4
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_5
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_6
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_6_HVI
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_7
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_8
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_8_BLEND
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### CHEVRON_SYNFLUID_PAO_9
- (tier1) `api_group_chemistry.api_group`: PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing.

#### ERGON_HYGOLD_100E
- (tier1) API group is not explicitly stated in supplier specification; independent classification not yet verified.
- (tier1) Corresponding SDS needs product-matched review before final audit.
- (tier2) API group is not explicitly stated in supplier specification; independent classification not yet verified.
- (tier2) Corresponding SDS needs product-matched review before final audit.
- (tier3) API group is not explicitly stated in supplier specification; independent classification not yet verified.
- (tier3) Corresponding SDS needs product-matched review before final audit.

#### ERGON_HYGOLD_100
- (tier1) API group not stated in supplier specification; independent classification not yet verified.
- (tier1) SDS DL2-10029.pdf requires field-by-field reconciliation before final audit.
- (tier2) API group not stated in supplier specification; independent classification not yet verified.
- (tier2) SDS DL2-10029.pdf requires field-by-field reconciliation before final audit.
- (tier3) API group not stated in supplier specification; independent classification not yet verified.
- (tier3) SDS DL2-10029.pdf requires field-by-field reconciliation before final audit.

#### ERGON_HYGOLD_5000BS
- (tier1) API group not explicitly stated.
- (tier1) SDS not yet reconciled.
- (tier2) API group not explicitly stated.
- (tier2) SDS not yet reconciled.
- (tier3) API group not explicitly stated.
- (tier3) SDS not yet reconciled.

#### ERGON_HYGOLD_60
- (tier1) API group not explicitly stated; do not infer from naphthenic description.
- (tier1) SDS DL2-10027.pdf requires full cross-check.
- (tier2) API group not explicitly stated; do not infer from naphthenic description.
- (tier2) SDS DL2-10027.pdf requires full cross-check.
- (tier3) API group not explicitly stated; do not infer from naphthenic description.
- (tier3) SDS DL2-10027.pdf requires full cross-check.

#### ERGON_HYGOLD_70E
- (tier1) API group not explicitly stated; do not infer from naphthenic description.
- (tier1) SDS not yet reconciled.
- (tier2) API group not explicitly stated; do not infer from naphthenic description.
- (tier2) SDS not yet reconciled.
- (tier3) API group not explicitly stated; do not infer from naphthenic description.
- (tier3) SDS not yet reconciled.

#### ERGON_HYGOLD_L1200
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS DL2-10032.pdf requires cross-check.
- (tier2) API group not explicitly stated; leave missing.
- (tier2) SDS DL2-10032.pdf requires cross-check.
- (tier3) API group not explicitly stated; leave missing.
- (tier3) SDS DL2-10032.pdf requires cross-check.

#### ERGON_HYGOLD_L150
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.
- (tier2) API group not explicitly stated; leave missing.
- (tier2) SDS reconciliation pending.
- (tier3) API group not explicitly stated; leave missing.
- (tier3) SDS reconciliation pending.

#### ERGON_HYGOLD_L2000
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.
- (tier2) API group not explicitly stated; leave missing.
- (tier2) SDS reconciliation pending.
- (tier3) API group not explicitly stated; leave missing.
- (tier3) SDS reconciliation pending.

#### ERGON_HYGOLD_L200
- (tier1) API group not explicitly stated.
- (tier1) SDS reconciliation pending.
- (tier2) API group not explicitly stated.
- (tier2) SDS reconciliation pending.
- (tier3) API group not explicitly stated.
- (tier3) SDS reconciliation pending.

#### ERGON_HYGOLD_L250E
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.
- (tier2) API group not explicitly stated; leave missing.
- (tier2) SDS reconciliation pending.
- (tier3) API group not explicitly stated; leave missing.
- (tier3) SDS reconciliation pending.

#### ERGON_HYGOLD_L350E
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.
- (tier2) API group not explicitly stated; leave missing.
- (tier2) SDS reconciliation pending.
- (tier3) API group not explicitly stated; leave missing.
- (tier3) SDS reconciliation pending.

#### ERGON_HYGOLD_L500
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.
- (tier2) API group not explicitly stated; leave missing.
- (tier2) SDS reconciliation pending.
- (tier3) API group not explicitly stated; leave missing.
- (tier3) SDS reconciliation pending.

#### ERGON_HYGOLD_L750
- (tier1) API group not explicitly stated.
- (tier1) SDS reconciliation pending.
- (tier1) Density and specific gravity conflict in supplier TDS; verify with supplier.
- (tier2) API group not explicitly stated.
- (tier2) SDS reconciliation pending.
- (tier2) Density and specific gravity conflict in supplier TDS; verify with supplier.
- (tier3) API group not explicitly stated.
- (tier3) SDS reconciliation pending.
- (tier3) Density and specific gravity conflict in supplier TDS; verify with supplier.

#### ERGON_HYGOLD_OLYMPUS_L500
- (tier1) API group not explicitly stated.
- (tier1) SDS DL2-10026.pdf reconciliation pending.
- (tier2) API group not explicitly stated.
- (tier2) SDS DL2-10026.pdf reconciliation pending.
- (tier3) API group not explicitly stated.
- (tier3) SDS DL2-10026.pdf reconciliation pending.

#### ERGON_HYGOLD_P150BS
- (tier1) API group not explicitly stated.
- (tier1) SDS cross-check pending.
- (tier1) Specific gravity 0.8931 at 15.6°C and density 7.437 lb/gal at 15.6°C are supplier-reported; no conversion into canonical density field.
- (tier2) API group not explicitly stated.
- (tier2) SDS cross-check pending.
- (tier2) Specific gravity 0.8931 at 15.6°C and density 7.437 lb/gal at 15.6°C are supplier-reported; no conversion into canonical density field.
- (tier3) API group not explicitly stated.
- (tier3) SDS cross-check pending.
- (tier3) Specific gravity 0.8931 at 15.6°C and density 7.437 lb/gal at 15.6°C are supplier-reported; no conversion into canonical density field.

#### ERGON_HYGOLD_P40
- (tier1) API group not explicitly stated.
- (tier1) SDS cross-check pending.
- (tier2) API group not explicitly stated.
- (tier2) SDS cross-check pending.
- (tier3) API group not explicitly stated.
- (tier3) SDS cross-check pending.

#### ERGON_HYGOLD_P70N
- (tier1) API group not explicitly stated.
- (tier1) SDS cross-check pending.
- (tier1) Supplier specific gravity 0.8559 and density 0.8552 g/cm3 at 15.6°C differ slightly; retained separately without equating.
- (tier2) API group not explicitly stated.
- (tier2) SDS cross-check pending.
- (tier2) Supplier specific gravity 0.8559 and density 0.8552 g/cm3 at 15.6°C differ slightly; retained separately without equating.
- (tier3) API group not explicitly stated.
- (tier3) SDS cross-check pending.
- (tier3) Supplier specific gravity 0.8559 and density 0.8552 g/cm3 at 15.6°C differ slightly; retained separately without equating.

#### ERGON_HY_40
- (tier1) API group not explicitly stated.
- (tier1) SDS cross-check pending.
- (tier1) Specific gravity reported at 15.6°C; density not directly reported.
- (tier1) PMCC flash point and water content specification retained in ingestion log because template does not offer dedicated fields.
- (tier2) API group not explicitly stated.
- (tier2) SDS cross-check pending.
- (tier2) Specific gravity reported at 15.6°C; density not directly reported.
- (tier2) PMCC flash point and water content specification retained in ingestion log because template does not offer dedicated fields.
- (tier3) API group not explicitly stated.
- (tier3) SDS cross-check pending.
- (tier3) Specific gravity reported at 15.6°C; density not directly reported.
- (tier3) PMCC flash point and water content specification retained in ingestion log because template does not offer dedicated fields.

#### FORMOSA_150N_GII_PLUS
- (tier1) Supplier group II+ is a commercial subclass, not a separate API group.
- (tier1) Density reported as relative density, not mass density; preserve original units.
- (tier1) KV40 reported only in SDS, not specification.
- (tier2) SDS flash point >230 C and specification minimum 210 C differ in stated thresholds; not necessarily contradictory.

#### FORMOSA_500N_GII
- (tier1) Density reported as relative density, not mass density; preserve original units.
- (tier1) KV40 reported only in SDS, not specification.

#### NESTE_NEXBASE_3020
- (tier1) No product TDS supplied for NEXBASE 3020; only two matching SDS files.
- (tier1) API group, KV100, VI, mass density, sulfur and other absent properties remain missing.
- (tier1) Relative density 0.82 at 15°C must not be treated as mass density.
- (tier2) No product TDS supplied for NEXBASE 3020; only two matching SDS files.
- (tier2) API group, KV100, VI, mass density, sulfur and other absent properties remain missing.
- (tier2) Relative density 0.82 at 15°C must not be treated as mass density.
- (tier3) No product TDS supplied for NEXBASE 3020; only two matching SDS files.
- (tier3) API group, KV100, VI, mass density, sulfur and other absent properties remain missing.
- (tier3) Relative density 0.82 at 15°C must not be treated as mass density.

#### NESTE_NEXBASE_3043
- (tier1) TDS edition 5.2 has no calendar revision date; no date inferred.
- (tier1) SDS DL2-15010.pdf reports KV40 typical 20 mm²/s, flash point >220°C, pour point ≤−12°C and relative density 0.82–0.84 at 15°C; these are consistent with TDS values/limits, but SDS density is relative density, not directly substituted for TDS mass density.
- (tier2) TDS edition 5.2 has no calendar revision date; no date inferred.
- (tier2) SDS DL2-15010.pdf reports KV40 typical 20 mm²/s, flash point >220°C, pour point ≤−12°C and relative density 0.82–0.84 at 15°C; these are consistent with TDS values/limits, but SDS density is relative density, not directly substituted for TDS mass density.
- (tier3) TDS edition 5.2 has no calendar revision date; no date inferred.
- (tier3) SDS DL2-15010.pdf reports KV40 typical 20 mm²/s, flash point >220°C, pour point ≤−12°C and relative density 0.82–0.84 at 15°C; these are consistent with TDS values/limits, but SDS density is relative density, not directly substituted for TDS mass density.

#### NESTE_NEXBASE_3050
- (tier1) TDS edition 4.2 does not provide a calendar revision date.
- (tier1) No independently identified NEXBASE 3050 SDS among the text-searchable supplier PDFs; SDS reconciliation pending.
- (tier2) TDS edition 4.2 does not provide a calendar revision date.
- (tier2) No independently identified NEXBASE 3050 SDS among the text-searchable supplier PDFs; SDS reconciliation pending.
- (tier3) TDS edition 4.2 does not provide a calendar revision date.
- (tier3) No independently identified NEXBASE 3050 SDS among the text-searchable supplier PDFs; SDS reconciliation pending.

#### NESTE_NEXBASE_3060
- (tier1) TDS edition 6.2 has no calendar revision date.
- (tier1) SDS DL2-12735.pdf checked; its pour-point and flash-point limits are compatible with TDS specifications.
- (tier2) TDS edition 6.2 has no calendar revision date.
- (tier2) SDS DL2-12735.pdf checked; its pour-point and flash-point limits are compatible with TDS specifications.
- (tier3) TDS edition 6.2 has no calendar revision date.
- (tier3) SDS DL2-12735.pdf checked; its pour-point and flash-point limits are compatible with TDS specifications.

#### NESTE_NEXBASE_3080
- (tier1) TDS edition 2.2 does not specify a calendar revision date.
- (tier1) SDS specific to NEXBASE 3080 not independently verified.
- (tier2) TDS edition 2.2 does not specify a calendar revision date.
- (tier2) SDS specific to NEXBASE 3080 not independently verified.
- (tier3) TDS edition 2.2 does not specify a calendar revision date.
- (tier3) SDS specific to NEXBASE 3080 not independently verified.

#### NYNAS_BASE_STOCK_20
- (tier1) API group not explicitly stated in supplier PDS.
- (tier1) SDS reconciliation pending.
- (tier2) API group not explicitly stated in supplier PDS.
- (tier2) SDS reconciliation pending.
- (tier3) API group not explicitly stated in supplier PDS.
- (tier3) SDS reconciliation pending.

#### NYNAS_BNS_5
- (tier1) API group and base-oil chemistry not explicitly stated in this PDS.
- (tier1) SDS reconciliation pending.
- (tier2) API group and base-oil chemistry not explicitly stated in this PDS.
- (tier2) SDS reconciliation pending.
- (tier3) API group and base-oil chemistry not explicitly stated in this PDS.
- (tier3) SDS reconciliation pending.

#### NYNAS_NS_3
- (tier1) SDS reconciliation pending.
- (tier1) Older PDS DL2-12382.pdf (2016-11-01) has different typical values; confirm appropriate commercial revision.
- (tier2) SDS reconciliation pending.
- (tier2) Older PDS DL2-12382.pdf (2016-11-01) has different typical values; confirm appropriate commercial revision.
- (tier3) SDS reconciliation pending.
- (tier3) Older PDS DL2-12382.pdf (2016-11-01) has different typical values; confirm appropriate commercial revision.

#### NYNAS_NYBASE_70
- (tier1) API group not explicitly stated: marketed for Group I replacement, not classified as Group I.
- (tier1) SDS reconciliation pending.
- (tier2) API group not explicitly stated: marketed for Group I replacement, not classified as Group I.
- (tier2) SDS reconciliation pending.
- (tier3) API group not explicitly stated: marketed for Group I replacement, not classified as Group I.
- (tier3) SDS reconciliation pending.

#### NYNAS_NYFROST_100
- (tier1) Grade-specific SDS reconciliation pending.
- (tier2) Grade-specific SDS reconciliation pending.
- (tier3) Grade-specific SDS reconciliation pending.

#### NYNAS_NYFROST_32
- (tier1) Resolve SDS KV40 31 cSt versus PDS 32 cSt and SDS PM flash >180°C versus PDS PM typical 176°C.
- (tier1) Check whether differing document dates or test conditions explain discrepancy.
- (tier2) Resolve SDS KV40 31 cSt versus PDS 32 cSt and SDS PM flash >180°C versus PDS PM typical 176°C.
- (tier2) Check whether differing document dates or test conditions explain discrepancy.
- (tier3) Resolve SDS KV40 31 cSt versus PDS 32 cSt and SDS PM flash >180°C versus PDS PM typical 176°C.
- (tier3) Check whether differing document dates or test conditions explain discrepancy.

#### NYNAS_NYFROST_68
- (tier1) API group not explicitly stated in supplied PDS.
- (tier1) Grade-specific SDS reconciliation pending.
- (tier2) API group not explicitly stated in supplied PDS.
- (tier2) Grade-specific SDS reconciliation pending.
- (tier3) API group not explicitly stated in supplied PDS.
- (tier3) Grade-specific SDS reconciliation pending.

#### NYNAS_S_3B
- (tier1) SDS DL2-13379.pdf has rounded KV40 3 cSt vs PDS 3.20 cSt; no definitive contradiction (SDS rounded).
- (tier1) SDS flash >100°C consistent with PDS 107°C; SDS density 0.86 g/cm3 rounded vs PDS 0.859 g/cm3.
- (tier2) SDS DL2-13379.pdf has rounded KV40 3 cSt vs PDS 3.20 cSt; no definitive contradiction (SDS rounded).
- (tier2) SDS flash >100°C consistent with PDS 107°C; SDS density 0.86 g/cm3 rounded vs PDS 0.859 g/cm3.
- (tier3) SDS DL2-13379.pdf has rounded KV40 3 cSt vs PDS 3.20 cSt; no definitive contradiction (SDS rounded).
- (tier3) SDS flash >100°C consistent with PDS 107°C; SDS density 0.86 g/cm3 rounded vs PDS 0.859 g/cm3.

#### NYNAS_T_3
- (tier1) Grade-specific SDS not reconciled.
- (tier2) Grade-specific SDS not reconciled.
- (tier3) Grade-specific SDS not reconciled.

#### NYNAS_T_4
- (tier1) Grade-specific SDS not reconciled.
- (tier2) Grade-specific SDS not reconciled.
- (tier3) Grade-specific SDS not reconciled.

#### NYNAS_T_600
- (tier1) Grade-specific SDS not reconciled.
- (tier2) Grade-specific SDS not reconciled.
- (tier3) Grade-specific SDS not reconciled.

#### NYNAS_T_9
- (tier1) Grade-specific SDS not reconciled.
- (tier2) Grade-specific SDS not reconciled.
- (tier3) Grade-specific SDS not reconciled.

#### PETRONAS_EQUINAS_4
- (tier1) No grade-specific TDS in supplied product source; only SDS available.
- (tier1) API base oil group not explicitly stated in SDS.
- (tier1) Pour point, sulfur, viscosity index and CCS not reported.
- (tier2) No grade-specific TDS in supplied product source; only SDS available.
- (tier2) API base oil group not explicitly stated in SDS.
- (tier2) Pour point, sulfur, viscosity index and CCS not reported.
- (tier3) No grade-specific TDS in supplied product source; only SDS available.
- (tier3) API base oil group not explicitly stated in SDS.
- (tier3) Pour point, sulfur, viscosity index and CCS not reported.

#### PETRONAS_EQUINAS_6
- (tier1) No separate grade-specific TDS found in supplied inventory.
- (tier1) API group, sulfur, viscosity index and CCS not explicitly reported.
- (tier2) No separate grade-specific TDS found in supplied inventory.
- (tier2) API group, sulfur, viscosity index and CCS not explicitly reported.
- (tier3) No separate grade-specific TDS found in supplied inventory.
- (tier3) API group, sulfur, viscosity index and CCS not explicitly reported.

#### PETRONAS_EQUINAS_8
- (tier1) No separately verified grade-specific SDS for EQUINAS 8; reconciliation pending.
- (tier2) No separately verified grade-specific SDS for EQUINAS 8; reconciliation pending.
- (tier3) No separately verified grade-specific SDS for EQUINAS 8; reconciliation pending.

#### PETRONAS_ETRO_3
- (tier1) No grade-specific SDS independently verified for ETRO 3.
- (tier1) No calendar revision date stated on product data sheet.
- (tier2) No grade-specific SDS independently verified for ETRO 3.
- (tier2) No calendar revision date stated on product data sheet.
- (tier3) No grade-specific SDS independently verified for ETRO 3.
- (tier3) No calendar revision date stated on product data sheet.

#### PETRONAS_ETRO_4
- (tier1) Supplementary DL2-12475.pdf is image-only and has not been independently reconciled.
- (tier1) No grade-specific SDS independently verified for ETRO 4.
- (tier1) No calendar revision date stated on PDS.
- (tier1) Density measurement temperature is not stated in the PDS; do not infer it.
- (tier2) Supplementary DL2-12475.pdf is image-only and has not been independently reconciled.
- (tier2) No grade-specific SDS independently verified for ETRO 4.
- (tier2) No calendar revision date stated on PDS.
- (tier2) Density measurement temperature is not stated in the PDS; do not infer it.
- (tier3) Supplementary DL2-12475.pdf is image-only and has not been independently reconciled.
- (tier3) No grade-specific SDS independently verified for ETRO 4.
- (tier3) No calendar revision date stated on PDS.
- (tier3) Density measurement temperature is not stated in the PDS; do not infer it.

#### PETRONAS_ETRO_4_PLUS
- (tier1) No grade-specific SDS independently verified for ETRO 4+.
- (tier1) No calendar revision date stated on PDS.
- (tier1) Density temperature is not specified; density remains Missing in temperature-dependent template field.
- (tier2) No grade-specific SDS independently verified for ETRO 4+.
- (tier2) No calendar revision date stated on PDS.
- (tier2) Density temperature is not specified; density remains Missing in temperature-dependent template field.
- (tier3) No grade-specific SDS independently verified for ETRO 4+.
- (tier3) No calendar revision date stated on PDS.
- (tier3) Density temperature is not specified; density remains Missing in temperature-dependent template field.

#### PETRONAS_ETRO_6
- (tier1) No separate grade-specific SDS verified for ETRO 6.
- (tier1) KV40 and density not reported in supplied TDS.
- (tier1) No dated revision on TDS.
- (tier1) Flash specification is printed as >220°C; no conversion to >=220°C.
- (tier2) No separate grade-specific SDS verified for ETRO 6.
- (tier2) KV40 and density not reported in supplied TDS.
- (tier2) No dated revision on TDS.
- (tier2) Flash specification is printed as >220°C; no conversion to >=220°C.
- (tier3) No separate grade-specific SDS verified for ETRO 6.
- (tier3) KV40 and density not reported in supplied TDS.
- (tier3) No dated revision on TDS.
- (tier3) Flash specification is printed as >220°C; no conversion to >=220°C.

#### PETRONAS_ETRO_6_PLUS
- (tier1) TDS lacks calendar revision date.
- (tier1) KV40 and Noack differences between TDS and SDS require source-level review.
- (tier1) Flash values are method-specific (D92 vs D93); not interchangeable.
- (tier1) TDS density 0.8429 kg/L has no stated test temperature; SDS density at 15°C used instead.
- (tier2) TDS lacks calendar revision date.
- (tier2) KV40 and Noack differences between TDS and SDS require source-level review.
- (tier2) Flash values are method-specific (D92 vs D93); not interchangeable.
- (tier2) TDS density 0.8429 kg/L has no stated test temperature; SDS density at 15°C used instead.
- (tier3) TDS lacks calendar revision date.
- (tier3) KV40 and Noack differences between TDS and SDS require source-level review.
- (tier3) Flash values are method-specific (D92 vs D93); not interchangeable.
- (tier3) TDS density 0.8429 kg/L has no stated test temperature; SDS density at 15°C used instead.

#### PETRONAS_M500
- (tier1) No independently verified grade-specific SDS for M500.
- (tier1) TDS has no stated calendar revision date.
- (tier2) No independently verified grade-specific SDS for M500.
- (tier2) TDS has no stated calendar revision date.
- (tier3) No independently verified grade-specific SDS for M500.
- (tier3) TDS has no stated calendar revision date.

#### PETRO_CANADA_PURITY_1003
- (tier1) Individual API group not explicitly assigned in the supplier family brochure (Group II and Group II+ are described collectively).
- (tier1) Grade-specific SDS reconciliation pending.
- (tier1) Additional Petro-Canada documents not yet reconciled against this brochure.
- (tier2) Individual API group not explicitly assigned in the supplier family brochure (Group II and Group II+ are described collectively).
- (tier2) Grade-specific SDS reconciliation pending.
- (tier2) Additional Petro-Canada documents not yet reconciled against this brochure.
- (tier3) Individual API group not explicitly assigned in the supplier family brochure (Group II and Group II+ are described collectively).
- (tier3) Grade-specific SDS reconciliation pending.
- (tier3) Additional Petro-Canada documents not yet reconciled against this brochure.

#### PETRO_CANADA_PURITY_1017
- (tier1) Individual API group not explicitly assigned in supplier family brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_1020
- (tier1) Individual API group not explicitly assigned in supplier family brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_2204
- (tier1) Individual API group not explicitly assigned in supplier family brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_2305
- (tier1) Individual API group not explicitly assigned in supplier family brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_L35
- (tier1) Viscosity index, sulfur and CCS are not reported for L35 in the cited brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Viscosity index, sulfur and CCS are not reported for L35 in the cited brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Viscosity index, sulfur and CCS are not reported for L35 in the cited brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_L40
- (tier1) API Group II confirmed from an additional official Petro-Canada manufacturer brochure; the original DL2-10020.pdf did not explicitly assign a grade-specific group.
- (tier1) Viscosity index, sulfur and CCS are not reported for L40 in the cited brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Viscosity index, sulfur and CCS are not reported for L40 in the cited brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Viscosity index, sulfur and CCS are not reported for L40 in the cited brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_L45
- (tier1) API Group II confirmed from an additional official Petro-Canada manufacturer brochure; the original DL2-10020.pdf did not explicitly assign a grade-specific group.
- (tier1) Viscosity index remains unreported for PURITY L45. CCS values at -20°C, -25°C, -30°C and -35°C were obtained from the manufacturer's March 2023 brochure.
- (tier1) Grade-specific SDS and differences between brochure editions require reconciliation.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Viscosity index, sulfur, Noack, saturates, aromatics and CCS are not reported for L45 in the cited brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Viscosity index, sulfur, Noack, saturates, aromatics and CCS are not reported for L45 in the cited brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_L50
- (tier1) API Group II confirmed from Petro-Canada's official Group II typical-properties table; the original DL2-10020.pdf did not explicitly assign a grade-specific group.
- (tier1) Viscosity index remains unreported for PURITY L50.
- (tier1) CCS at -20°C and -25°C confirmed from Petro-Canada's official product comparison using ASTM D5293. No values are reported there for -30°C or -35°C.
- (tier1) Grade-specific SDS and differences between the original 2015 brochure and newer manufacturer documentation require reconciliation.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Viscosity index, sulfur, Noack and CCS are not reported for L50 in the cited brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Viscosity index, sulfur, Noack and CCS are not reported for L50 in the cited brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_L60
- (tier1) API Group II verified from Petro-Canada's official World-Class Base Oils brochure; the original 2015 brochure did not explicitly classify L60.
- (tier1) Sulfur, Noack, saturates, aromatics and CCS are not reported for L60 in the cited brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Sulfur, Noack, saturates, aromatics and CCS are not reported for L60 in the cited brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Sulfur, Noack, saturates, aromatics and CCS are not reported for L60 in the cited brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_L65
- (tier1) API Group II confirmed for PURITY L65 using Petro-Canada's official World-Class Base Oils brochure.
- (tier1) No grade-specific CCS measurement has been verified for PURITY L65.
- (tier1) Noack volatility and grade-specific SDS require further verification.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Noack and CCS are not reported for L65 in the cited brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- (tier3) Individual API group not explicitly assigned in supplier family brochure.
- (tier3) Noack and CCS are not reported for L65 in the cited brochure.
- (tier3) Grade-specific SDS and other brochure editions require reconciliation.

#### PETRO_CANADA_PURITY_VHVI_2
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Cross-check duplicate supplier brochure files DL2-11262.pdf through DL2-11265.pdf and any grade-specific SDS during final audit.
- (tier2) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier2) Cross-check duplicate supplier brochure files DL2-11262.pdf through DL2-11265.pdf and any grade-specific SDS during final audit.
- (tier3) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier3) Cross-check duplicate supplier brochure files DL2-11262.pdf through DL2-11265.pdf and any grade-specific SDS during final audit.

#### PETRO_CANADA_PURITY_VHVI_3
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Confirm against grade-specific SDS and other brochure editions during final audit.
- (tier2) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier2) Confirm against grade-specific SDS and other brochure editions during final audit.
- (tier3) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier3) Confirm against grade-specific SDS and other brochure editions during final audit.

#### PETRO_CANADA_PURITY_VHVI_4
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Confirm against grade-specific SDS and other brochure editions during final audit.
- (tier2) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier2) Confirm against grade-specific SDS and other brochure editions during final audit.
- (tier3) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier3) Confirm against grade-specific SDS and other brochure editions during final audit.

#### PETRO_CANADA_PURITY_VHVI_6
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Confirm against grade-specific SDS and other brochure editions during final audit.
- (tier2) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier2) Confirm against grade-specific SDS and other brochure editions during final audit.
- (tier3) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier3) Confirm against grade-specific SDS and other brochure editions during final audit.

#### PETRO_CANADA_PURITY_VHVI_8
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Confirm against grade-specific SDS and other brochure editions during final audit.
- (tier2) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier2) Confirm against grade-specific SDS and other brochure editions during final audit.
- (tier3) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier3) Confirm against grade-specific SDS and other brochure editions during final audit.

#### SHELL_RISELLA_X_415
- (tier1) Shell identifies Risella X 415 as a GTL-derived technical white/process oil, but no explicit grade-specific API base-oil Group classification has been verified. API Group remains Missing.
- (tier1) Chemistry is supported by the historical TDS DL2-13728.pdf: GTL-derived hydrocarbon fluid, highly saturated with a high degree of iso-paraffinic structures. Shell's newer official TDS also describes the product as a highly refined paraffinic process oil made using GTL technology.
- (tier1) No grade-specific CCS apparent viscosity, ASTM D5293 measurement, or CCS test temperature has been verified for Shell Risella X 415.
- (tier1) TDS DL2-13728.pdf reports density of 806 kg/m3 at 15°C, whereas SDS DL2-13729.pdf reports 803.5 kg/m3 at 15°C. The document variation requires reconciliation.
- (tier1) The historical TDS is dated 2013-02-08 and the cited SDS is revised 2018-10-26. Shell has issued newer technical information; document-version reconciliation remains necessary.
- (tier2) Shell Risella X 415 is marketed as a GTL-derived process/technical white oil. API lubricant base-oil Group classification is treated as Not Required for its documented application, subject to project applicability rules.
- (tier2) MRV low-temperature pumpability testing is treated as Not Required for the documented process-oil application. No MRV viscosity, yield stress, or test temperature is reported in the supplied TDS.
- (tier2) The TDS reports Noack volatility of 40 mass% at 250°C for 1 hour, ASTM D5800. Preserve this measured value despite the product's process-oil classification.
- (tier2) TDS DL2-13728.pdf reports density of 806 kg/m3 at 15°C, while SDS DL2-13729.pdf reports 803.5 kg/m3 at 15°C. This discrepancy requires reconciliation.
- (tier2) The TDS is dated 2013-02-08 and the cited SDS was revised 2018-10-26. Confirm applicable document revisions before final approval.
- (tier3) API group is not explicitly assigned by the supplier; GTL chemistry is not an API group declaration.
- (tier3) TDS density at 15 C is 806 kg/m3, while SDS DL2-13729.pdf p.8 reports 803.5 kg/m3 at 15 C; document variation requires reconciliation.
- (tier3) TDS dated 2013 and SDS revised 2018; confirm current revisions before final approval.

#### SHELL_RISELLA_X_420
- (tier1) Shell Risella X 420 is described as a GTL-derived process oil. API lubricant base-oil Group classification is treated as Not Required under the proposed project applicability rule; confirm this interpretation is accepted by the professor's template.
- (tier1) Chemistry is recorded from TDS DL2-13726.pdf, page 1, dated 2014-06-02: GTL-derived hydrocarbon fluid, highly saturated with a high degree of iso-paraffinic structures.
- (tier1) CCS viscosity is treated as Not Required for the documented process-oil application. No grade-specific CCS viscosity or test temperature is reported in the supplied TDS.
- (tier1) TDS DL2-13726.pdf reports density of 816 kg/m3 at 15°C, whereas SDS DL2-13730.pdf reports 813.8 kg/m3 at 15°C. The discrepancy requires reconciliation.
- (tier1) The historical TDS is dated 2014-06-02 and the cited SDS was revised 2018-10-26. Confirm applicable document revisions before final approval.
- (tier2) Shell Risella X 420 is marketed as a GTL-derived process oil. API lubricant base-oil Group classification is treated as Not Required under the proposed project applicability rule; confirm this interpretation is accepted by the professor's template.
- (tier2) Chemistry is recorded from TDS DL2-13726.pdf, page 1, dated 2014-06-02: GTL-derived hydrocarbon fluid, highly saturated with a high degree of iso-paraffinic structures.
- (tier2) MRV low-temperature pumpability testing is treated as Not Required for the documented process-oil application. No grade-specific MRV apparent viscosity, yield stress, or test temperature is reported in the supplied TDS.
- (tier2) Noack volatility is reported as 12 mass% at 250°C for 1 hour, ASTM D5800, in TDS DL2-13726.pdf.
- (tier2) TDS DL2-13726.pdf reports density of 816 kg/m3 at 15°C, whereas SDS DL2-13730.pdf reports 813.8 kg/m3 at 15°C. The discrepancy requires reconciliation.
- (tier2) The historical TDS is dated 2014-06-02 and the cited SDS was revised 2018-10-26. Confirm applicable document revisions before final approval.
- (tier3) API group not explicitly stated; GTL origin is not a supplier API group declaration.
- (tier3) TDS density 816 kg/m3 at 15 C versus SDS DL2-13730.pdf p.8 813.8 kg/m3 at 15 C; verify revisions and reconcile.
- (tier3) Confirm latest TDS/SDS editions before final approval.

#### SHELL_RISELLA_X_430
- (tier1) Shell Risella X 430 is described as a GTL-derived process oil. API lubricant base-oil Group classification is treated as Not Required under the proposed project applicability rule; confirm acceptance of this classification with the professor.
- (tier1) Chemistry is recorded from TDS DL2-13727.pdf, page 1, dated 2014-06-02: GTL-derived hydrocarbon fluid, highly saturated with a high degree of iso-paraffinic structures.
- (tier1) CCS cold-cranking viscosity is treated as Not Required for the documented process-oil application. No grade-specific CCS viscosity, test method, or test temperature is provided in the supplied TDS.
- (tier1) TDS DL2-13727.pdf reports density of 828 kg/m3 at 15°C, whereas SDS DL2-13731.pdf reports 824.8 kg/m3 at 15°C. The discrepancy requires reconciliation.
- (tier1) The historical TDS is dated 2014-06-02 and the cited SDS was revised 2020-01-13. Confirm applicable document revisions before final approval.
- (tier2) Shell Risella X 430 is described as a GTL-derived process oil. API lubricant base-oil Group classification is treated as Not Required under the proposed project applicability rule; confirm acceptance of this interpretation with the professor.
- (tier2) Chemistry is recorded from TDS DL2-13727.pdf, page 1, dated 2014-06-02: GTL-derived hydrocarbon fluid, highly saturated with a high degree of iso-paraffinic structures.
- (tier2) MRV low-temperature pumpability testing is treated as Not Required for the documented process-oil application. No grade-specific MRV apparent viscosity, yield stress, or test temperature is reported in the supplied TDS.
- (tier2) Noack volatility is reported as 2.0 mass% at 250°C for 1 hour, ASTM D5800, in TDS DL2-13727.pdf.
- (tier2) TDS DL2-13727.pdf reports density of 828 kg/m3 at 15°C, whereas SDS DL2-13731.pdf reports 824.8 kg/m3 at 15°C. The discrepancy requires reconciliation.
- (tier2) The historical TDS is dated 2014-06-02 and the cited SDS was revised 2020-01-13. Confirm applicable document revisions before final approval.
- (tier3) API group not explicitly stated; GTL origin is not a supplier API group declaration.
- (tier3) TDS density 828 kg/m3 at 15 C versus SDS DL2-13731.pdf p.7 824.8 kg/m3 at 15 C; verify revisions and reconcile.
- (tier3) Confirm latest TDS/SDS editions before final approval.

#### S_OIL_ARAMCO_ULTRA_8
- (tier1) API group not explicitly specified in the original 2018 SDS.
- (tier1) The original SDS reports viscosity ranges; S-OIL's official technical specifications provide additional typical properties.
- (tier1) Verify whether the SDS relative density 0.847 at 15°C is dimensionless relative density rather than absolute mass density; do not silently convert.
- (tier1) CCS viscosity of 6,300 mPa.s at -30°C (ASTM D5293) was obtained from S-OIL's official technical specifications, not the original SDS.
- (tier1) Final source-level audit and alternate document reconciliation pending.
- (tier2) API group not explicitly specified in the original SDS.
- (tier2) The original SDS reports viscosity ranges; additional typical properties are available in Aramco's grade-specific technical datasheet.
- (tier2) Verify whether the SDS relative density 0.847 at 15°C is dimensionless relative density rather than absolute mass density; do not silently convert.
- (tier2) MRV viscosity and its test temperature are not reported in the reviewed manufacturer technical specifications.
- (tier2) Final source-level audit and alternate document reconciliation pending.
- (tier3) API group not explicitly specified in the source SDS.
- (tier3) A grade-specific TDS with typical values should be located; the SDS reports ranges only.
- (tier3) Verify whether the SDS relative density 0.847 at 15°C is dimensionless relative density rather than absolute mass density; do not silently convert.
- (tier3) Final source-level audit and alternate document reconciliation pending.

#### S_OIL_PREMIUM_P_20
- (tier1) API Group III confirmed for aramcoULTRA 8 using Aramco's official 2024 base-oil catalog; classification was not explicitly stated in the original 2018 SDS.
- (tier1) S-OIL's official Premium Series catalog reports specific gravity 0.8520 at 15/4°C (ASTM D1298), but absolute density remains unverified.
- (tier1) No grade-specific CCS viscosity or test temperature was verified for P-20.
- (tier1) Grade-specific SDS and additional technical documentation require reconciliation.
- (tier2) API group not explicitly specified in reviewed Premium Series datasheets.
- (tier2) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics not reported in the reviewed product sheets.
- (tier2) Final source-level audit and grade-specific SDS reconciliation pending.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for S-OIL P-20 (Premium 100N); no test temperature or ASTM D4684 measurement is available in the reviewed documentation.
- (tier3) API group not explicitly specified in reviewed Premium Series datasheets.
- (tier3) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier3) Noack volatility, CCS viscosity, saturates and aromatics not reported in the reviewed product sheets.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

#### S_OIL_PREMIUM_P_31
- (tier1) No explicit API Group classification has been verified for historical S-OIL P-31 (Premium 150N).
- (tier1) Chemistry is described using S-OIL's Premium Series hydrotreating and MEK-dewaxing process; grade-specific chemical composition and CAS number remain unverified.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for P-31.
- (tier1) The catalog reports specific gravity at 15/4°C, which must not be silently treated as absolute density.
- (tier1) Grade-specific SDS and additional manufacturer documentation require reconciliation.
- (tier2) API Group remains unverified for the historical S-OIL P-31 (Premium 150N) grade.
- (tier2) Specific gravity at 15/4°C is dimensionless and has not been transcribed as absolute density.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for P-31; no ASTM D4684 measurement or test temperature was found in the reviewed documentation.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier2) Final source-level audit and grade-specific SDS reconciliation pending.
- (tier3) API group not explicitly specified in reviewed Premium Series datasheets.
- (tier3) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier3) Noack volatility, CCS viscosity, saturates and aromatics not reported in the reviewed product sheets.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

#### S_OIL_PREMIUM_P_480
- (tier1) Historical P-480 (150BS) API Group has not been explicitly verified in the reviewed manufacturer documents.
- (tier1) Chemistry confirmed using S-OIL Premium-480 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic, CAS 64742-57-0, purity 100%.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed as absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature was verified.
- (tier1) Noack volatility, saturates and aromatics remain unverified.
- (tier1) Final source-level reconciliation between the original product datasheet and grade-specific SDS pending.
- (tier2) Historical P-480 (150BS) API Group remains unverified.
- (tier2) Chemistry identified in S-OIL's Premium-480 SDS revised 2015-06-10; grade-specific composition should be reconciled with the original product datasheet.
- (tier2) Specific gravity at 15/4°C is dimensionless and must not be transcribed as absolute density.
- (tier2) MRV viscosity and MRV yield stress have not been verified for P-480; no grade-specific test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier2) Final source-level audit and SDS reconciliation pending.
- (tier3) API group not explicitly specified in reviewed Premium Series datasheet.
- (tier3) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier3) Noack volatility, CCS viscosity, saturates and aromatics not reported in the reviewed product sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

#### S_OIL_PREMIUM_P_8
- (tier1) API Group classification for historical S-OIL P-8 (Premium 60N) has not been explicitly verified.
- (tier1) Chemistry confirmed in S-OIL Premium-8 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8; purity 100%.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed as absolute density.
- (tier1) No grade-specific CCS viscosity or test temperature has been verified for P-8.
- (tier1) Noack volatility, saturates and aromatics remain unverified.
- (tier1) Final source-level reconciliation between the original product datasheet and grade-specific SDS pending.
- (tier2) API Group for historical S-OIL P-8 (Premium 60N) remains unverified.
- (tier2) Chemistry identified in S-OIL Premium-8 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8.
- (tier2) Specific gravity at 15/4°C is dimensionless and must not be transcribed as absolute density.
- (tier2) MRV viscosity and MRV yield stress have not been verified for P-8; no grade-specific test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier2) Final source-level reconciliation between the original product datasheet and grade-specific SDS pending.
- (tier3) API group and chemistry not explicitly specified in reviewed Premium Series datasheet.
- (tier3) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier3) Noack volatility, CCS viscosity, saturates and aromatics not reported in reviewed product sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

#### S_OIL_PREMIUM_P_96
- (tier1) API Group for historical S-OIL P-96 (Premium 500N) has not been explicitly verified.
- (tier1) Chemistry confirmed in S-OIL Premium-96 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7; purity 100%.
- (tier1) Historical product catalog reports specific gravity 0.8811 at 15/4°C (ASTM D1298), not an absolute density measurement.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for P-96.
- (tier1) Noack volatility, saturates and aromatics remain unverified for the historical P-96 grade.
- (tier1) Final source-level reconciliation between original product datasheet and grade-specific SDS pending.
- (tier2) API Group for historical S-OIL P-96 (Premium 500N) remains unverified.
- (tier2) Chemistry identified in S-OIL Premium-96 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7.
- (tier2) Historical S-OIL catalog reports specific gravity 0.8811 at 15/4°C (ASTM D1298), which is dimensionless and must not be transcribed as absolute density.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for P-96; no grade-specific MRV test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier2) Final source-level reconciliation between original product datasheet and grade-specific SDS pending.
- (tier3) API group and chemistry not explicitly specified in reviewed Premium Series datasheet.
- (tier3) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier3) Noack volatility, CCS viscosity, saturates and aromatics not reported in reviewed product sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

#### S_OIL_SUPER_S_31
- (tier1) API Group for historical S-OIL S-31 (Super 150N) is not explicitly established by the reviewed historical datasheet or SDS; manufacturer mapping to aramcoPRIMA 150 requires classification reconciliation.
- (tier1) Chemistry confirmed in S-OIL Super-31 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7; purity 100%.
- (tier1) S-OIL SDS reports relative density 0.8634 at 15°C; this is not an explicitly reported absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for S-31.
- (tier1) Noack volatility, saturates and aromatics remain unverified for the historical S-31 grade.
- (tier1) Final reconciliation between original DL2-12392.pdf and manufacturer SDS pending.
- (tier2) API Group for historical S-OIL S-31 (Super 150N) has not been explicitly verified.
- (tier2) Chemistry identified in S-OIL Super-31 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7.
- (tier2) S-OIL's SDS reports relative density 0.8634 at 15°C; this must not be transcribed directly as absolute density.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for S-31; no grade-specific MRV test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier2) Final reconciliation between original DL2-12392.pdf and manufacturer SDS pending.
- (tier3) API group is not explicitly specified in the reviewed Super Series brochure.
- (tier3) Specific gravity at 15/4 °C is dimensionless and is not an absolute density measurement.
- (tier3) Noack volatility, CCS, saturates, and aromatics are not numerically reported in the reviewed sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

#### S_OIL_SUPER_S_8
- (tier1) API Group for historical S-OIL S-8 (Super 60N) has not been explicitly verified.
- (tier1) S-OIL lists a grade-specific Super 8 SDS, but its Section 3 chemical composition and CAS number require direct verification.
- (tier1) Specific gravity 0.8719 at 15/4°C (ASTM D1298) is dimensionless and must not be transcribed as absolute density.
- (tier1) The original datasheet prints L-40.0 for pour point; the notation requires source-level verification before assigning a numeric value.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified.
- (tier1) Noack volatility, saturates and aromatics remain unverified.
- (tier1) Final reconciliation between DL2-12392.pdf and the grade-specific Super 8 SDS pending.
- (tier2) API Group for historical S-OIL S-8 (Super 60N) remains unverified.
- (tier2) Grade-specific Super 8 SDS composition and CAS number require direct verification.
- (tier2) Specific gravity 0.8719 at 15/4°C (ASTM D1298) is dimensionless and must not be transcribed as absolute density.
- (tier2) Pour point is printed as L-40.0 °C (ASTM D5950); qualifier or encoding remains ambiguous. Numeric value deliberately left null.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for S-8; no MRV test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier2) Final reconciliation between DL2-12392.pdf and grade-specific Super 8 SDS pending.
- (tier3) API group not explicitly specified in Super Series brochure.
- (tier3) Specific gravity 15/4°C 0.8719 (ASTM D1298) is dimensionless, not density.
- (tier3) Pour point cell prints L-40.0 (ASTM D5950); unclear if this is a qualifier or character encoding. Numeric pour point deliberately not assigned pending supplier verification.
- (tier3) Noack volatility, CCS, saturates and aromatics not numerically reported.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

#### S_OIL_SUPER_S_96
- (tier1) API Group for historical S-OIL S-96 (Super 500N) has not been explicitly verified.
- (tier1) Chemistry confirmed in S-OIL Super-96 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7; purity 100%.
- (tier1) Historical S-OIL catalog reports specific gravity 0.8762 at 15/4°C (ASTM D1298), not an absolute density measurement.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for historical S-96; modern aramcoPRIMA 500 measurements must not be substituted.
- (tier1) Noack volatility, saturates and aromatics remain unverified.
- (tier1) Final source-level reconciliation between DL2-12392.pdf and the grade-specific SDS pending.
- (tier2) API Group for historical S-OIL S-96 (Super 500N) has not been explicitly verified.
- (tier2) Chemistry identified in S-OIL Super-96 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7.
- (tier2) Historical S-OIL catalog reports specific gravity 0.8762 at 15/4°C (ASTM D1298), which must not be transcribed directly as absolute density.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for historical S-96; no grade-specific test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier2) Final source-level reconciliation between DL2-12392.pdf and the grade-specific SDS pending.
- (tier3) API group is not explicitly specified in the reviewed Super Series brochure.
- (tier3) Specific gravity at 15/4 °C is dimensionless and is not an absolute density measurement.
- (tier3) Noack volatility, CCS, saturates, and aromatics are not numerically reported in the reviewed sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

#### S_OIL_ULTRA_S_2
- (tier1) Chemistry is recorded from SDS DL2-15235.pdf, Section 3: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 2.
- (tier1) Noack volatility is marked with a dash in the Ultra-S 2 column and must remain Missing.
- (tier1) Final source-level reconciliation between DL2-11177.pdf and DL2-15235.pdf remains pending.
- (tier2) Chemistry is recorded from SDS DL2-15235.pdf, Section 3: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8.
- (tier2) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier2) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 2.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for Ultra-S 2; no grade-specific MRV test temperature is available.
- (tier2) Noack volatility is marked with a dash in the Ultra-S 2 column and must remain Missing.
- (tier2) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15235.pdf remains pending.
- (tier3) API group not explicitly specified in the reviewed Ultra-S series brochure.
- (tier3) Specific gravity 15/4 °C is dimensionless and is not absolute density.
- (tier3) Noack volatility is marked with a dash in the Ultra-S 2 column, and must remain Missing.
- (tier3) SDS DL2-15235.pdf revised June 10, 2015; final source-level audit pending.

#### S_OIL_ULTRA_S_3
- (tier1) Chemistry is recorded from SDS DL2-15236.pdf, Section 3: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8. Final source-level verification remains pending.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 3.
- (tier1) Noack volatility is marked with a dash in the Ultra-S 3 column and must remain Missing.
- (tier1) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15236.pdf remains pending.
- (tier2) Chemistry is recorded from SDS DL2-15236.pdf, Section 3: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8. Final source-level verification remains pending.
- (tier2) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier2) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 3.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for Ultra-S 3; no grade-specific MRV test temperature is available.
- (tier2) Noack volatility is marked with a dash in the Ultra-S 3 column and must remain Missing.
- (tier2) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15236.pdf remains pending.
- (tier3) API group not explicitly specified in the reviewed Ultra-S series brochure.
- (tier3) Specific gravity 15/4 °C is dimensionless and is not absolute density.
- (tier3) Noack volatility is marked with a dash in the Ultra-S 3 column and remains Missing.
- (tier3) SDS DL2-15236.pdf revised June 10, 2015; final source-level audit pending.

#### S_OIL_ULTRA_S_4
- (tier1) S-OIL Ultra-S 4 SDS revised 2015-06-10 reports Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-54-7; purity 100%. The printed description and CAS number appear inconsistent and require supplier clarification.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 4.
- (tier1) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15139.pdf remains pending.
- (tier2) SDS DL2-15139.pdf, revised 2015-06-10, reports 'Distillates (petroleum), hydrotreated light paraffinic' with CAS 64742-54-7. The printed description and CAS number appear inconsistent and require supplier clarification.
- (tier2) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier2) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 4.
- (tier2) MRV apparent viscosity, MRV yield stress, and MRV test temperature have not been verified for Ultra-S 4.
- (tier2) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15139.pdf remains pending.
- (tier3) API group not explicitly specified in reviewed supplier documents.
- (tier3) Specific gravity 15/4 °C is dimensionless and is not absolute density.
- (tier3) SDS DL2-15139.pdf revised June 10, 2015; final source-level audit pending.

#### S_OIL_ULTRA_S_6
- (tier1) Chemistry is recorded from SDS DL2-15237.pdf, Section 3: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7. Final source-level verification remains pending.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 6.
- (tier1) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15237.pdf remains pending.
- (tier2) Chemistry is recorded from SDS DL2-15237.pdf, Section 3: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7. Final source-level verification remains pending.
- (tier2) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier2) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 6.
- (tier2) MRV apparent viscosity, MRV yield stress, and MRV test temperature have not been verified for Ultra-S 6.
- (tier2) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15237.pdf remains pending.
- (tier3) API group not explicitly specified in reviewed supplier documents.
- (tier3) Specific gravity 15/4 °C is dimensionless and is not absolute density.
- (tier3) SDS DL2-15237.pdf revised June 10, 2015; final source-level audit pending.

#### S_OIL_ULTRA_S_8
- (tier1) Chemistry is recorded from SDS DL2-15238.pdf, Section 3: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7. The SDS revision date is recorded as 2015-06-10.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 8.
- (tier1) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15238.pdf remains pending.
- (tier2) API Group III classification is supported by S-OIL's published Ultra-S/aramcoULTRA product-family equivalence, but is not explicitly printed in the historical grade-specific SDS.
- (tier2) Chemistry is recorded from SDS DL2-15238.pdf, Section 3: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7; revision date 2015-06-10.
- (tier2) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier2) No grade-specific MRV apparent viscosity, MRV yield stress, or MRV test temperature has been verified for Ultra-S 8.
- (tier2) Current S-OIL product information includes CCS viscosity and density for Ultra-S 8, but these values have not been reconciled with historical product data sheet DL2-11177.pdf and must not be silently incorporated.
- (tier2) Final reconciliation between historical product data sheet DL2-11177.pdf, SDS DL2-15238.pdf, and current manufacturer product information remains pending.
- (tier3) API group not explicitly specified in reviewed supplier documents.
- (tier3) Specific gravity (15/4 °C) is dimensionless and not absolute density.
- (tier3) Grade-specific SDS DL2-15238.pdf revised June 10, 2015; final source-level audit pending.

#### YUBASE_3
- (tier1) Resolve the YUBASE 3 API Group discrepancy between the current SK Enmove manufacturer webpage (Group III product range) and the January 2021 SK corporate offering circular, page 52 (YUBASE 3 explicitly listed as Group II).
- (tier1) Document is headed NARMAK TRADE S.R.O.; confirm manufacturer/supplier relationship with YUBASE-SK.
- (tier1) API group and chemistry are not explicitly stated in this document.
- (tier1) Specific gravity row is printed with unit g/m3, which is inconsistent with the stated value 0,8299; do not interpret as verified density or specific gravity without clarification.
- (tier2) Confirm the manufacturer and distributor relationship between SK and NARMAK TRADE S.R.O. for archived YUBASE 3.
- (tier2) Resolve the API Group classification of archived YUBASE 3. Current SK Enmove product information presents YUBASE 3 within its Group III range, while a January 2021 SK corporate offering circular explicitly lists YUBASE 3 as Group II.
- (tier2) The archived property sheet does not explicitly state the product chemistry. Obtain grade-specific manufacturer documentation before assigning a chemistry description.
- (tier2) The specific-gravity entry reports 0.8299 with the questionable unit g/m3. Verify the original units and measurement conditions before recording a density value.
- (tier2) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in DL2-11303.pdf.
- (tier2) Noack volatility is reported as 40 wt% using DIN 51581. The source transcription does not specify a test temperature; do not assume one.
- (tier2) Confirm the archived property sheet's issue date and applicable product revision.
- (tier3) Document is headed NARMAK TRADE S.R.O.; confirm manufacturer/supplier relationship with YUBASE-SK.
- (tier3) API group and chemistry are not explicitly stated in this document.
- (tier3) Specific gravity row is printed with unit g/m3, which is inconsistent with the stated value 0,8299; do not interpret as verified density or specific gravity without clarification.

#### YUBASE_4
- (tier1) Confirm the manufacturer and distributor relationship between SK Corporation/SK Enmove and NARMAK TRADE S.R.O. for archived YUBASE 4.
- (tier1) API Group III classification is supported by SK Enmove manufacturer information but is not explicitly stated in archived property sheet DL2-11304.pdf. Confirm that the classification applies to the archived grade.
- (tier1) Historical SK Corporation YUBASE 4 MSDS No. 739-YU4-02, dated 1999-02-12, identifies the chemistry as hydrotreated heavy paraffinic petroleum distillate (CAS 64742-54-7). Confirm that this historical composition applies to the archived NARMAK TRADE product grade.
- (tier1) The specific-gravity entry at 15°C is printed as 0.8338 with the inconsistent unit g/m3. Verify the original unit and measurement conditions before assigning a density value.
- (tier1) No grade-specific CCS cold-cranking viscosity, test temperature, or test method is reported in archived property sheet DL2-11304.pdf.
- (tier1) Confirm the issue date of the archived NARMAK TRADE property sheet and whether newer applicable TDS/SDS revisions are available.
- (tier2) Confirm the manufacturer and distributor relationship between SK Corporation/SK Enmove and NARMAK TRADE S.R.O. for archived YUBASE 4.
- (tier2) API Group III classification is supported by SK Enmove manufacturer information, but is not explicitly stated in archived property sheet DL2-11304.pdf. Confirm that the classification applies to the archived grade.
- (tier2) Historical SK Corporation YUBASE 4 MSDS No. 739-YU4-02, dated 1999-02-12, identifies hydrotreated heavy paraffinic petroleum distillate (CAS 64742-54-7). Confirm that this composition applies to the archived grade.
- (tier2) The specific-gravity entry at 15°C is printed as 0.8338 with the inconsistent unit g/m3. Verify the original unit and measurement conditions before assigning density.
- (tier2) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in archived property sheet DL2-11304.pdf.
- (tier2) Noack volatility is reported as 15 wt% using DIN 51581. The source transcription does not specify a test temperature; do not assume one.
- (tier2) Confirm the archived property sheet's issue date and applicable product revision.
- (tier3) Document is headed NARMAK TRADE S.R.O.; confirm manufacturer/supplier relationship with YUBASE-SK.
- (tier3) API group and chemistry are not explicitly stated in this document.
- (tier3) Specific gravity at 15 °C is printed as 0,8338 with unit g/m3, an inconsistent unit; do not infer density or specific gravity without clarification.

#### YUBASE_5
- (tier1) SK Lubricants officially describes the YUBASE brand as API Group III, but the located manufacturer publication does not explicitly classify YUBASE 5. Obtain grade-specific confirmation before final approval.
- (tier1) API Group III classification is supported by SK Enmove manufacturer information, but is not explicitly stated in archived property sheet DL2-11304.pdf. Confirm that the classification applies to the archived grade.
- (tier1) Historical SK Corporation YUBASE 4 MSDS No. 739-YU4-02, dated 1999-02-12, identifies hydrotreated heavy paraffinic petroleum distillate (CAS 64742-54-7). Confirm that this composition applies to the archived grade.
- (tier1) The specific-gravity entry at 15°C is printed as 0.8338 with the inconsistent unit g/m3. Verify the original unit and measurement conditions before assigning density.
- (tier1) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in archived property sheet DL2-11304.pdf.
- (tier1) Noack volatility is reported as 15 wt% using DIN 51581. The source transcription does not specify a test temperature; do not assume one.
- (tier1) Confirm the archived property sheet's issue date and applicable product revision.
- (tier2) Confirm the manufacturer and distributor relationship between SK Lubricants/SK Enmove and NARMAK TRADE S.R.O. for archived YUBASE 5.
- (tier2) SK Lubricants describes the YUBASE brand as API Group III, but the available manufacturer publication does not explicitly identify YUBASE 5. Confirm the grade-specific API Group classification for archived product DL2-11305.pdf.
- (tier2) The archived property sheet does not explicitly report chemical composition. Obtain grade-specific manufacturer SDS documentation before assigning chemistry or a CAS number.
- (tier2) The specific-gravity entry at 15°C is printed as 0.8363 with the inconsistent unit g/m3. Verify the original units and measurement conditions before assigning a density value.
- (tier2) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in archived property sheet DL2-11305.pdf.
- (tier2) Noack volatility is reported as 12 wt% using DIN 51581. The supplied transcription does not specify a test temperature; do not assume one.
- (tier2) Confirm the archived property sheet's issue date and applicable product revision.
- (tier3) Document issued by NARMAK TRADE S.R.O.; confirm manufacturer/supplier relationship with YUBASE-SK.
- (tier3) API group and chemistry are not explicitly stated.
- (tier3) Specific gravity at 15 °C printed as 0,8363 with inconsistent unit g/m3; do not infer density or specific gravity without clarification.

#### YUBASE_6
- (tier1) Confirm the manufacturer and distributor relationship between SK Lubricants/SK Enmove and NARMAK TRADE S.R.O. for archived YUBASE 6.
- (tier1) API Group III is supported by SK Enmove's official manufacturer information but is not explicitly declared in archived property sheet DL2-11306.pdf. Confirm applicability to the historical grade.
- (tier1) SK Lubricants YUBASE 6 SDS dated 2020-01-01 identifies the chemistry as distillates (petroleum), hydrotreated heavy paraffinic, CAS 64742-54-7, at 100%. Confirm that this SDS applies to the undated archived NARMAK TRADE grade.
- (tier1) The specific-gravity entry at 15°C is printed as 0.8423 with the inconsistent unit g/m3. Verify the original units and measurement conditions before assigning density.
- (tier1) No grade-specific CCS viscosity, test temperature, or test method is reported in archived property sheet DL2-11306.pdf.
- (tier1) Confirm the archived property sheet's issue date and applicable product revision.
- (tier2) Confirm the manufacturer and distributor relationship between SK Lubricants/SK Enmove and NARMAK TRADE S.R.O. for archived YUBASE 6.
- (tier2) API Group III is supported by external SK Enmove manufacturer information but is not explicitly declared in archived property sheet DL2-11306.pdf. Confirm applicability to the historical grade.
- (tier2) A historical SK Lubricants YUBASE 6 SDS dated 2020-01-01 identifies the chemistry as distillates (petroleum), hydrotreated heavy paraffinic, CAS 64742-54-7. Confirm that this SDS applies to the undated archived grade.
- (tier2) The specific-gravity entry at 15°C is printed as 0.8423 with the inconsistent unit g/m3. Verify the original units and measurement conditions before assigning density.
- (tier2) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in archived property sheet DL2-11306.pdf.
- (tier2) Noack volatility is reported as 7 wt% using DIN 51581. The supplied transcription does not specify a test temperature; do not assume one.
- (tier2) Confirm the archived property sheet's issue date and applicable product revision.
- (tier3) Document issued by NARMAK TRADE S.R.O.; confirm manufacturer/supplier relationship with YUBASE-SK.
- (tier3) API group and chemistry are not explicitly stated.
- (tier3) Specific gravity at 15 °C printed as 0,8423 with inconsistent unit g/m3; do not infer density or specific gravity without clarification.

### Additive packages

#### AFTON_HITEC_12010
- (tier1) Supplier: Section 1 of DL2-15021.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier' (first: Afton Chemical Asia Pte. Ltd.; also Afton Chemical Corporation, Richmond, VA). Confirm which name to record.
- (tier1) Only an SDS is in the archive for HiTEC 12010 (DL2-15021.pdf). No TDS/product bulletin, so package type, claims, SAE grades, treat rates, co-components and published formulations are all missing; these could be looked up later in an Afton product bulletin.
- (tier1) package_type left Missing: the SDS (p.1) only says 'Lubricating Oil Additive'; it does not state PVL/CVL/HDDO etc. The old Product_JSON subclass 'performance additive package' is not printed on the sheet.
- (tier2) Supplier: Section 1 of DL2-15021.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier' (first: Afton Chemical Asia Pte. Ltd.; also Afton Chemical Corporation, Richmond, VA). Confirm which name to record.
- (tier2) Only an SDS is in the archive for HiTEC 12010 (DL2-15021.pdf). No TDS/product bulletin, so package type, claims, SAE grades, treat rates, co-components and published formulations are all missing; these could be looked up later in an Afton product bulletin.
- (tier2) TBN, sulfated ash, all elements (Ca, Mg, Zn, P, B, Mo, N, S) and pour point are not printed in DL2-15021.pdf; Section 9 (p.6-7) has no pour point entry.
- (tier2) DL2-15021.pdf p.2 Section 3 lists 'Phosphorodithioic acid, mixed O,O-bis(2-ethylhexyl and iso-Bu and iso-Pr) esters, zinc salts' (CAS 85940-28-9) at 10 - 15 %. This is a ZDDP component share, not Zn or P element content, so Zn/P stay Missing.
- (tier2) DL2-15021.pdf p.2 Section 3 lists two base-oil carriers (hydrotreated heavy paraffinic 64742-54-7, 15 - 25 %; solvent-dewaxed heavy paraffinic 64742-65-0, 15 - 25 %) and p.15 (Korea ISHL) lists 'Mineral oil 35 - 45' %. The package templates have no carrier field.
- (tier2) Density: the old Product_JSON gives 1044 kg/m3 (converted); the sheet prints 1.044 g/cm³ at 15°C (p.6). Same value, kept in the printed unit.

#### AFTON_HITEC_12200
- (tier1) Product name differs between documents: bulletins DL2-11412.PDF p.1-2 and DL2-14639.pdf p.1-2 print 'HiTEC® 12200' / 'HiTEC® 12200 HDEO Additive Package'; SDS DL2-12074.pdf p.1 prints 'HiTEC® 12200 Performance Additive' (SDS no. H12200).
- (tier1) Supplier: bulletins (DL2-14639.pdf p.2) name Afton Chemical Corporation; SDS DL2-12074.pdf p.1 lists Afton Chemical Asia Pte. Ltd. and other Afton entities under 'Manufacturer / Supplier'.
- (tier1) revision_date: bulletins print only '05/18' (DL2-11412.PDF p.2) and '08/18' (DL2-14639.pdf p.2) in the copyright line; SDS DL2-12074.pdf p.1 'Date of issue/Date of revision: 7/16/2019'. product.revision_date is a list in source_file order.
- (tier1) Claim type: every matrix column sits under the printed header 'Approvals' (DL2-14639.pdf p.2), including API categories, so claim_type = 'approval'. Columns MB 228.1, MB 229.1 and MAN 3275 carry footnote 5 'Meets requirements of (MRO)' and are set to 'meets'. Please confirm this reading.
- (tier1) Treat rates and booster doses are printed as '%' with no mass/volume basis (DL2-14639.pdf p.2); only footnote 3 says '% wt'. Unit kept as '%'.
- (tier1) Rows and columns only in the 08/18 bulletin (DL2-14639.pdf p.2), absent from 05/18 (DL2-11412.PDF p.2): row '10.8% + 0.9% HiTEC® 12260, SAE 10W-30, GP II' (API CI-4, API SL); row '10.8% + 0.6% HiTEC® 9552, SAE 10W-40, GP II/III' (API SN, API SL, API SJ, ACEA A3/B4-16, MB 229.3, RN 0700); columns API SN, MB 229.3, RN 0700. Not treated as conflicts (additions, not disagreements).
- (tier1) Footnote 6 differs: 05/18 (DL2-11412.PDF p.2) '6 Formulations, available in Q2 2018' on the two SAE 10W-40 rows; 08/18 (DL2-14639.pdf p.2) '6 11.15% HiTEC® 12252 = 10.8% HiTEC® 12200 + 0.35% HiTEC® 9552' on the 10.8% SAE 15W-40 GP I row.
- (tier1) No complete published formulation (all ingredients summing to 100 wt.%) is printed; published_formulations left Missing. The bar charts on DL2-14639.pdf p.2 (Mack T-12, Cat 1K, Seq IIIF, T8E vs 'API CI-4 Limit'/'Reserve') have no numeric values and were not recorded.
- (tier1) Old Product_JSON has no claims, route matrix or co-components for this product although both bulletins print them; the new file fills them from DL2-14639.pdf p.2.
- (tier2) Product name differs between documents: bulletins DL2-11412.PDF p.1-2 and DL2-14639.pdf p.1-2 print 'HiTEC® 12200' / 'HiTEC® 12200 HDEO Additive Package'; SDS DL2-12074.pdf p.1 prints 'HiTEC® 12200 Performance Additive' (SDS no. H12200).
- (tier2) Supplier: bulletins (DL2-14639.pdf p.2) name Afton Chemical Corporation; SDS DL2-12074.pdf p.1 lists Afton Chemical Asia Pte. Ltd. and other Afton entities under 'Manufacturer / Supplier'.
- (tier2) revision_date: bulletins print only '05/18' (DL2-11412.PDF p.2) and '08/18' (DL2-14639.pdf p.2) in the copyright line; SDS DL2-12074.pdf p.1 'Date of issue/Date of revision: 7/16/2019'. product.revision_date is a list in source_file order.
- (tier2) Sulfated ash, all elements (Ca, Mg, Zn, P, B, Mo, N, S) and pour point are not printed in any of the three documents.
- (tier2) SDS DL2-12074.pdf p.2 Section 3 component shares (not element contents, so element fields stay Missing): overbased calcium sulfurized tetrapropenyl phenate 5 - 10 %; two zinc dialkyldithiophosphates 3 - 5 % each; base-oil distillates 15 - 25 % (x2) and 1 - 3 % (x2).
- (tier2) SDS DL2-12074.pdf p.20 (Japan PRTR) lists 'Boron compounds 5 - 10' %. This is a component share, not boron content; B stays Missing.
- (tier2) Density: old Product_JSON gives 989 kg/m3 (converted); the sheet prints 0.989 g/ml at 15°C (DL2-14639.pdf p.2). Same value, kept in printed unit.

#### AFTON_HITEC_12208
- (tier1) Only a product bulletin is available for HiTEC 12208 (no SDS in the archive).
- (tier1) Claim wording: the table header says 'Approvals', the text (p.2) says 'can be formulated into premium lubricant meeting API CK-4', 'can also be formulated into API FA-4 lubricant' and 'It can also meet Cummins approvals'. claim_type set to 'approval' from the table header; please confirm.
- (tier1) Bar charts on DL2-15364.pdf p.2 (Mack T-12 wear, Volvo T-13 oxidation) give performance reserves (43%, 22%, 48%, 70%) vs API CK-4/FA-4 limits; candidate-oil test results, no formulation given, not recorded.
- (tier1) No co-components (VM/PPD/booster) and no published formulation are printed.
- (tier2) Only a product bulletin is available for HiTEC 12208 (no SDS in the archive).
- (tier2) KV40, sulfated ash, all elements and pour point are not printed in DL2-15364.pdf.
- (tier2) Density: old Product_JSON gives 957.2 kg/m3 (converted); sheet prints 0.9572 g/ml at 15°C (p.2).

#### AFTON_HITEC_12210M
- (tier1) Product name differs: bulletins print 'HiTEC® 12210M' (DL2-11796.pdf, DL2-15568.pdf p.1-2); SDS prints 'HiTEC® 12210M Performance Additive' (DL2-15569.pdf p.1).
- (tier1) Supplier: bulletins name Afton Chemical Corporation; SDS DL2-15569.pdf p.1 lists Afton entities under 'Manufacturer / Supplier'.
- (tier1) Claims table changed between bulletins. 05/18 (DL2-11796.pdf p.2) columns not in 04/22: API CJ-4 (CK-4 15W-40 and 10W-30), Ford WSS-M2C214-B1 (FA-4 10W-30), ACEA E7-16, ACEA E9-16, MTU 2.1, Deutz DQC III-10LA. 04/22 (DL2-15568.pdf p.2) adds row API CK-4 10W-40 and columns ACEA E7-22, ACEA E11-22, MAN 3775, Deutz DQC III-18LA, Allison TES 439. For the columns present in both, the dots agree, so no conflict entries. Fields use the 04/22 table.
- (tier1) 05/18 text names only HiTEC® 5748A as the VM and only SAE 15W-40/10W-30 for CK-4; 04/22 adds HiTEC® 5748 and SAE 10W-40.
- (tier1) Required VM dose is not printed in either bulletin; left Missing.
- (tier1) Permitted base oils: only 'in a range of market basestocks' / 'in appropriate grades and base stocks' (DL2-15568.pdf p.2); left Missing.
- (tier1) Radar chart 'Afton CK-4 vs. CJ-4 Performance Comparison' (p.2) has no numeric values; not recorded.
- (tier2) Product name differs: bulletins print 'HiTEC® 12210M' (DL2-11796.pdf, DL2-15568.pdf p.1-2); SDS prints 'HiTEC® 12210M Performance Additive' (DL2-15569.pdf p.1).
- (tier2) Supplier: bulletins name Afton Chemical Corporation; SDS DL2-15569.pdf p.1 lists Afton entities under 'Manufacturer / Supplier'.
- (tier2) Sulfated ash, all elements and pour point are not printed in any of the three documents.
- (tier2) SDS DL2-15569.pdf p.2-3 Section 3 component shares (not element contents): ZDDP (85940-28-9) ≥5 - ≤10 %, overbased calcium sulfurized phenate ≥3 - ≤5 %, base-oil distillates ≥15-≤25, ≥10-≤15, ≥5-≤10 %; p.22 (Korea) 'Mineral oil ≥35 - ≤45' and 'Molybdenum and its compounds ≥0.30 - ≤0.50' %. Mo/Zn/Ca left Missing.
- (tier2) KV40 is printed as 'Minimum' in the SDS (p.8); the old Product_JSON also records it as a minimum. Only source of KV40.

#### AFTON_HITEC_12210
- (tier1) Only a product bulletin is available for HiTEC 12210 (no SDS in the archive).
- (tier1) Required VM HiTEC® 5748A (OCP) is named (DL2-11418.pdf p.2) but its dose is not printed; dose left Missing.
- (tier1) Permitted base oils: the sheet only says 'in a range of market basestocks' and 'in appropriate grades and base stocks' (p.2); no API group named, field left Missing.
- (tier1) OEM claim is generic ('designed to meet ... including Caterpillar, Cummins, ...'), no specific OEM specification numbers; recorded as claim_type 'other'.
- (tier1) Radar chart 'Afton PC-11 vs. CJ-4 Performance Comparison' (p.2) has no numeric values; not recorded.
- (tier2) Only a product bulletin is available for HiTEC 12210 (no SDS in the archive).
- (tier2) Density printed as 7.90 lbs/gal without a temperature (DL2-11418.pdf p.2); specific gravity 0.948 @ 15.6/15.6°C printed on the same page. Kept in printed unit; temperature for density left null.
- (tier2) KV40, sulfated ash, all elements and pour point are not printed in DL2-11418.pdf.

#### AFTON_HITEC_12360
- (tier1) Only a product bulletin is available for HiTEC 12360 (no SDS in the archive).
- (tier1) MAN 3677 and Scania LDF-4 are marked '*' = 'Approvals pending ...' (DL2-13692.pdf p.2); recorded as claim_type 'other', not 'approval'.
- (tier1) Required VM HiTEC® 5748 (25SSI OCP) named but dose not printed.
- (tier1) Bar charts p.2 (ISB cam lobe wear, Mack T13 IR peak height, CAT C13 oil consumption vs CK-4 limit, reserves 78%/45%/36%/37%/35%) are candidate-oil results without formulations; not recorded.
- (tier2) Only a product bulletin is available for HiTEC 12360 (no SDS in the archive).
- (tier2) Text p.2: 'HiTEC® 12360 contains 1% ash content so it is compatible with after treatment devices'. It is not clear whether this is the package or the finished oil sulfated ash; sulfated_ash left Missing.
- (tier2) KV40, all elements and pour point are not printed in DL2-13692.pdf.

#### AFTON_HITEC_12400
- (tier1) User decision 2026-10-17: 13 claims marked with a filled dot (DL2-15365.pdf p.2) are recorded as Reported with claim_type left unspecified (null), because the legend does not define the filled dot; flagged for review. Claims with only '○ Pending completion of Field Trial' or '◉ Approval pending' marks keep claim_type 'other'.
- (tier1) Only a product bulletin is available for HiTEC 12400 (no SDS in the archive).
- (tier1) DL2-15365.pdf p.2: the table has 22 symbol columns but only 21 header labels; row 'ACEA E4 SAE 10W-40 + HiTEC® 611' has an '◉ Approval pending' mark in column 22, which has no header. Recorded as '(column 22, no header printed)'.
- (tier1) Table headers are vector graphics (not text); column assignment was read from a 400 dpi image and the symbol positions from the text layer (Wingdings glyphs).
- (tier1) HiTEC® 611 booster dose and the OCP VM identity/dose are not printed.
- (tier1) Bar charts p.2 (Caterpillar C13, Cummins ISM, Volvo T-13, OM501LA, OM646LA, Mack T-12 vs industry limit; OM501LA fuel economy '19 % better') have no formulation; not recorded.
- (tier2) Only a product bulletin is available for HiTEC 12400 (no SDS in the archive).
- (tier2) KV40, sulfated ash, all elements and pour point are not printed in DL2-15365.pdf.
- (tier2) The typical characteristics (0.951 g/ml, 150 °C, 133 mm2/s, TBN 61) are identical to HiTEC 12360 (DL2-13692.pdf); copied as printed.

#### AFTON_HITEC_8712
- (tier1) Supplier: DL2-15020.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier'; first listed (Afton Chemical Asia Pte. Ltd.) recorded.
- (tier1) Only an SDS is in the archive for HiTEC 8712. Package type, claims, grades, treat rates, base oils, co-components and formulations are not printed; could be looked up later in an Afton bulletin.
- (tier1) Product name printed as 'HiTEC® 8712 Performance Additive' (p.1); old Product_JSON uses 'HiTEC 8712'.
- (tier1) The SDS does not say this is a package; composition (p.2) shows mineral oil 30 - 60 %, calcium long-chain alkylphenate sulfide 10 - 19.9 % and ZDDP 10 - 19.9 %. Old Product_JSON classifies it as 'performance additive package'; please confirm package vs component.
- (tier2) Supplier: DL2-15020.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier'; first listed (Afton Chemical Asia Pte. Ltd.) recorded.
- (tier2) Only an SDS is in the archive for HiTEC 8712. Package type, claims, grades, treat rates, base oils, co-components and formulations are not printed; could be looked up later in an Afton bulletin.
- (tier2) Product name printed as 'HiTEC® 8712 Performance Additive' (p.1); old Product_JSON uses 'HiTEC 8712'.
- (tier2) Density 1.033 g/cm³ printed without temperature; relative density 1.036 also printed (DL2-15020.pdf p.6). Temperature left null.
- (tier2) TBN, sulfated ash, elements and pour point not printed. Section 3 (p.2) component shares: calcium alkylphenate sulfide 10 - 19.9 %, ZDDP 10 - 19.9 %, mineral oil 30 - 60 % (also p.10 ISHL 'Mineral Oil 30 - 60'); not element contents.

#### AFTON_HITEC_8788B
- (tier1) Supplier: DL2-15016.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier'; first listed (Afton Chemical Asia Pte. Ltd.) recorded.
- (tier1) Only an SDS is in the archive for HiTEC 8788B; claims, SAE grades, treat rates, base oils, co-components and formulations are not printed (could be looked up later in an Afton product bulletin).
- (tier2) Supplier: DL2-15016.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier'; first listed (Afton Chemical Asia Pte. Ltd.) recorded.
- (tier2) Only an SDS is in the archive for HiTEC 8788B; claims, SAE grades, treat rates, base oils, co-components and formulations are not printed (could be looked up later in an Afton product bulletin).
- (tier2) TBN, sulfated ash, all elements and pour point are not printed in DL2-15016.pdf.
- (tier2) DL2-15016.pdf p.2-3 Section 3 component shares (not element contents): overbased calcium sulfurized phenate 5 - 10 %, alkyl esters of alkyl phenate alkanoic acid 3 - 5 %, two ZDDPs 1 - 3 % each, base-oil distillates 15 - 25 % (x2) and 1 - 3 % (x2). p.21 (Japan PRTR) 'Boron compounds 5 - 10' % (component share, B left Missing).
- (tier2) Density: old Product_JSON gives 958 kg/m3 (converted); sheet prints 0.958 g/cm³ at 15°C (p.7).

#### AFTON_HITEC_8799B
- (tier1) Supplier: DL2-15017.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier'; first listed (Afton Chemical Asia Pte. Ltd.) recorded.
- (tier1) Only an SDS is in the archive for HiTEC 8799B; claims, SAE grades, treat rates, base oils, co-components and formulations are not printed (could be looked up later in an Afton product bulletin).
- (tier2) Supplier: DL2-15017.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier'; first listed (Afton Chemical Asia Pte. Ltd.) recorded.
- (tier2) Only an SDS is in the archive for HiTEC 8799B; claims, SAE grades, treat rates, base oils, co-components and formulations are not printed (could be looked up later in an Afton product bulletin).
- (tier2) TBN, sulfated ash, all elements and pour point are not printed in DL2-15017.pdf.
- (tier2) DL2-15017.pdf p.2-3 Section 3 component shares (not element contents): two ZDDPs 3 - 5 % and 1 - 3 %, overbased calcium sulfurized phenate 3 - 5 %, calcium long-chain alkaryl sulfonate 1 - 3 %, base-oil distillates 25 - 35 % and 15 - 25 %. p.20 (Japan PRTR) 'Boron compounds 5 - 10' % (component share, B left Missing).
- (tier2) Density: old Product_JSON gives 956 kg/m3 (converted); sheet prints 0.956 g/cm³ at 15°C (p.7), relative density 0.958.

#### HiTEC_8766B
- (tier1) DL2-10367.pdf is shared with HiTEC 8767B (component #78). Per decision, only the HiTEC 8766B column of 'Typical Characteristics' is used here; the 8767B dose in the dosage table is recorded as a co-component of the 8766B SAE 10W-40 route.
- (tier1) Claims recorded as claim_type 'approval' from the table header 'Approvals' (DL2-10367.pdf p.2).
- (tier1) TBN booster required for some claims ('1 Requires TBN Boost') but product and dose are not printed.
- (tier1) Fleet bubble chart (p.2, 'Euro III and Euro IV Engines Dominate the Market') is market data; not recorded.
- (tier2) DL2-10367.pdf is shared with HiTEC 8767B (component #78). Per decision, only the HiTEC 8766B column of 'Typical Characteristics' is used here; the 8767B dose in the dosage table is recorded as a co-component of the 8766B SAE 10W-40 route.
- (tier2) KV40, sulfated ash, elements and pour point are not printed in DL2-10367.pdf. No SDS in the archive for HiTEC 8766B.

#### BRB_PETROLAD_8099
- (tier1) Claim types: API rows set to 'meets' (text p.1 'meet market standard API requirements'), 'MB 228.3 blanket approval' to 'approval', all other rows of the 'Performances' table to 'other' because the table has no wording beyond 'Performances'. Please confirm.
- (tier1) Viscotech 6540 VI improver is optional ('can be used in formulations combined with'); not entered as a required co-component. No SAE grades printed.
- (tier1) Only a TDS is in the archive; text says 'An MSDS is available upon request' (p.3).
- (tier2) Ca, P, N, Zn printed without a test method (DL2-11053.pdf p.3). KV40, sulfated ash, Mg, B, Mo, S and pour point are not printed.
- (tier2) Density: old Product_JSON gives 990 kg/m3 (converted); sheet prints 0.99 kg / L at 15.6 °C.

#### BETTCHEM_BT_3088
- (tier1) User decision 2026-10-17: the 4 entries from the 'Technical Judgement for BT 3088' (DL2-15620.pdf, document_type 'other') are recorded as Reported with evidence_class 'Predicted' and the note that the value is a prediction, not a measurement.
- (tier1) Claim type: the TDS (DL2-15551.pdf p.1) gives a 'RECOMMENDED DOSAGE' per specification and says the package 'covers API CI-4 /CH-4 performance levels'; recorded as 'recommended'.
- (tier1) No SAE grades, base oils, co-components or published formulation are printed in either document.
- (tier1) API SL at 8% appears only in the Technical Judgement (p.4); the TDS lists API CH-4/SJ at 7.0 and CF-4/SG at 6.0.
- (tier2) User decision 2026-10-17: element rows Ca, Zn, P, B, N, S and Sulphated Ash (DL2-15551.pdf p.1) print no unit; numbers stored as Reported with unit 'not printed'. Flagged: unit to be confirmed (likely mass %).
- (tier2) Density field holds the printed SPECIFIC GRAVITY at 15.6℃ (0.9881, ASTM D1298); no density in kg/m3 is printed.
- (tier2) Mg and Mo not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.9881 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY at 15.6℃ Report 0.9881 ASTM D1298', DL2-15551.pdf p.1), not a density in kg/m3; flagged for review.

#### BETTCHEM_BT_3089
- (tier1) Claim type 'recommended' from the 'RECOMMENDED DOSAGE' table (DL2-15552.pdf p.1); product is 'CUSTOMER SPECIFIC'.
- (tier1) No SAE grades, base oils, co-components or published formulation printed in DL2-15552.pdf; no SDS in the archive.
- (tier1) Mg, B and Mo are not printed in DL2-15552.pdf. Base number has a 'Minimum' (198) and a 'TYPICAL' (233) but no 'Maximum'.
- (tier2) Density field holds the printed SPECIFIC GRAVITY at 15.6℃ (ASTM D1298); no density in kg/m3 printed (DL2-15552.pdf p.1).
- (tier2) Mg, B and Mo are not printed in DL2-15552.pdf. Base number has a 'Minimum' (198) and a 'TYPICAL' (233) but no 'Maximum'.
- (tier2) User decision 2026-10-17: density field stores the number 1.09 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY at 15.6℃ Report 1.09 ASTM D1298', DL2-15552.pdf p.1), not a density in kg/m3; flagged for review.

#### BETTCHEM_BT_3093
- (tier1) Claim type 'recommended' from the 'RECOMMENDED DOSAGE' table (DL2-15550.pdf p.1); product is 'CUSTOMER SPECIFIC'.
- (tier1) No SAE grades, base oils, co-components or published formulation printed in DL2-15550.pdf; no SDS in the archive.
- (tier1) B and pour point are not printed in DL2-15550.pdf. Base number has 'Minimum' 100 and 'TYPICAL' 115, no 'Maximum'.
- (tier2) Density field holds the printed SPECIFIC GRAVITY at 15.6℃ (ASTM D1298); no density in kg/m3 printed (DL2-15550.pdf p.1).
- (tier2) B and pour point are not printed in DL2-15550.pdf. Base number has 'Minimum' 100 and 'TYPICAL' 115, no 'Maximum'.
- (tier2) User decision 2026-10-17: density field stores the number 0.99 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY at 15.6℃ 0.9 1.1 0.99 ASTM D1298', DL2-15550.pdf p.1), not a density in kg/m3; flagged for review.

#### ENI_MX_5212
- (tier1) Claim type 'recommended' from the text 'is recommended for blending ...' and the 'TREAT RATE & PERFORMANCE CLAIMS' table (DL2-14981.pdf p.1).
- (tier1) Treat rates are printed as '%' with no mass/volume basis. No SDS in the archive.
- (tier2) DL2-14981.pdf p.2 gives only min/max specification limits (value left null, min/max filled); density is a single value in a merged cell.
- (tier2) KV40, sulfated ash, B, Mo, S and pour point are not printed. Flash point method ASTM D 93 (PMCC).
- (tier2) Old Product_JSON left KV100/TBN/elements as observations without values; the sheet prints them as min/max limits.

#### ENI_MX_5217
- (tier1) Claim types: 'ACEA E4/E7-12' set to 'meets' (text 'meets ACEA E4/E7 levels'); other cells, many printed as '... level', set to 'other'. MB 228.5 is '(*) Official approval pending in group II/III formulation'.
- (tier1) No SDS in the archive.
- (tier2) DL2-12630.pdf p.2 gives only min/max specification limits (value left null, min/max filled); density is a single value in a merged cell.
- (tier2) KV40, sulfated ash, B, Mo, S and pour point are not printed. Flash point method ASTM D 93 (PMCC).

#### INFINEUM_D3320
- (tier1) Claim type 'other': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) No VM/co-components or SDS in the archive for D3320.
- (tier2) Typical Inspections (DL2-12025.pdf p.1) also print 'Mineral Oil 48 %(m) Calculated' (carrier share; no package field).
- (tier2) Ca, Mg, Zn, P, B, Mo, N and pour point are not printed.

#### INFINEUM_D3354
- (tier1) Claim type 'other': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) Row 2 level is printed as 'As below plus Volvo VDS-2' (DL2-10203.pdf p.1); the reference ('below' vs the row above) is unclear.
- (tier1) Booster rows: footnotes 3 and 4 give three alternative boosters 'tuned for different base stock qualities'; all recorded as co-components. SV261 VM dose not printed.
- (tier2) Typical Inspections p.1 also print 'Mineral Oil Content 49 mass % Calculated' (carrier share; no package field).
- (tier2) B, Mo, S and pour point are not printed.

#### INFINEUM_D3375
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) NEW product (no old Product_JSON file); image-only TDS read visually (DL2-10217.pdf p.1, 'Version: 10 March 2015 (4.0)').
- (tier1) Claim type 'meets' from the description wording 'oil meeting the performance requirements listed below'. MB entry printed as 'MB-Approval 228.5'.
- (tier1) Infineum SV261 VM dose not printed. No SDS in the archive.
- (tier2) NEW product, image-only TDS read visually. Typical Inspections also print 'Mineral Oil 51 %(m) Calculated' and handling viscosities 'Vis @ Min Load/Unload Temp: 1,470 cSt', 'Vis @ Max Load/Unload Temp: 835 cSt'.
- (tier2) Density, sulfated ash, B, Mo, S and pour point are not printed.

#### INFINEUM_D3384
- (tier1) Claim type 'other': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) DL2-10218.pdf (TDS, Version 10 May 2015 (5.0)) is image-only; read visually. Not listed in the old Product_JSON; added per decision (b).
- (tier1) TDS p.2 prints 'Min Load/Unload Temp: 80 °C' above 'Max Load/Unload Temp: 65 °C' (min > max); copied as printed. SDS p.7 gives loading/unloading 55 °C - 65 °C.
- (tier1) Product use (SDS DL2-15274.pdf p.1): 'Additive for heavy duty diesel engine lubricating oil'. VM not named.
- (tier2) SDS DL2-15274.pdf p.3 component share (not element content): zinc dialkyldithiophosphate (298-577-9) >=10 - <12,5 %; four base-oil distillates >=1 - <10 % each.
- (tier2) Sulfated ash, B, Mo, S and pour point not printed in the TDS; SDS p.13 'Pour point : not determined'.
- (tier2) SDS also prints relative density 0,974 at 15,6 °C.

#### INFINEUM_D3396
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) API SL is described as 'can also be used in gasoline engines requiring API SL category products'; recorded with the table claim type 'meets'.
- (tier1) No SDS in the archive.
- (tier2) Also printed: 'Density @ 60 F, lb/gal 8.08 lb/USG'. B, Mo, S and pour point not printed (DL2-13383.pdf).

#### INFINEUM_D3398
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) No SDS in the archive.
- (tier2) Also printed: 'Density @ 60 F, lb/gal 8.15 lb/USG'. B, Mo, S and pour point not printed (DL2-13348.pdf).

#### INFINEUM_D3416
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) Grades printed as 'MULTI' / 'MONO' (multigrade / monograde) for the lower API levels (DL2-15333.pdf p.1); recorded as printed.
- (tier1) Claim type 'meets' applied to all rows from the CI-4 description; the lower API levels have no separate wording.
- (tier1) No SDS in the archive.
- (tier2) Sulfated Ash method printed as 'Calculated' (supplier). B, Mo, S and pour point not printed.
- (tier2) Row label 'Flash Point Deg C' is visible on the page image but missing from the text layer. (DL2-15333.pdf p.1).

#### INFINEUM_D3417
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) DL2-15334.pdf is a customer specification ('CUSTOMER SPECIFICATION', customer 'Global - BRENNTAG GROUP', 'Printed On : 12-Feb-2024'), document_type PDS per decision (c).
- (tier1) No SDS in the archive.
- (tier2) Element fields use the newer customer specification DL2-15334.pdf (Min/Target/Max); targets equal the TDS typical values (Ca 1.26, Mg 1.19, N 0.79, P 1.37, Zn 1.51), so no conflict.
- (tier2) PDS lists Base Number and KV100 as 'Test and report results' (no limits). Sulfated ash, B, Mo, S and pour point not printed.
- (tier2) Row label 'Flash Point Deg C' is visible on the page image but missing from the text layer. (DL2-15335.pdf p.1).

#### INFINEUM_D3424
- (tier1) Claim type 'other': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) DL2-10204.pdf holds two documents: p.1 Infineum TDS (Version 9th November 2004 (3.1)) and p.2-8 a Safety Data Sheet issued by Multisol Limited (Revision Date 02Dec2008, Revision 4). Both listed in document_type/source_file.
- (tier1) Claim type 'other' ('developed to meet ...'); several rows say 'Quality' (e.g. 'MTU Type II Quality', 'VW501/5 Quality'). No VM or co-components printed.
- (tier2) Flash point: TDS 190 °C (PM) vs SDS '>110C'; recorded as a conflict, field holds the more recent SDS value.
- (tier2) TDS also prints 'Mineral Oil Content 49 mass % Calculated'. SDS p.2 Section 3 component shares: calcium long chain alkyl phenate sulphide 1.0 - 4.9%, tetrapropenylphenol 1.0 - 4.9%, zinc alkyl dithiophosphate 5.0 - 9.9% (not element contents).
- (tier2) B, Mo, S and pour point not printed.

#### INFINEUM_D3451
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) Fields use the newer TDS DL2-12029.pdf (2017). The 2012 TDS DL2-10219.pdf p.1 lists 'API SL/CI-4/CH-4' and 'ACEA E7-08' for SAE 15W-40 at 11.9 mass % ('~ 11.0 Volume %'); the 2017 sheet updates ACEA E7-08 to E7-12 and adds rows. Revision, not recorded as conflict.
- (tier1) 'can be downtreated to meet API CG-4 and CF-4' has no treat rate printed.
- (tier2) SDS DL2-13720.pdf p.3 component shares: ZDDP >=10 - <12,5 %; molybdenum polysulphide long chain alkyl dithiocarbamate complex >=0,25 - <1 % (not element contents). SDS p.12 'Pour point : not determined'.
- (tier2) Sulfated ash only in the 2012 TDS (8.6 %(m)); B and pour point not printed.

#### INFINEUM_D3453
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) NEW product (no old Product_JSON file); image-only TDS (Version: 9 December 2014 (3.0)) read visually.
- (tier1) No SDS in the archive.
- (tier2) NEW product, image-only TDS read visually. Also printed: 'Density @ 60 F, lb/gal 8.06 lb/USG', 'Vis @ Min Load/Unload Temp: 1,270 cSt', 'Vis @ Max Load/Unload Temp: 725 cSt'.
- (tier2) B and pour point not printed.

#### INFINEUM_D3463
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) No SDS in the archive.
- (tier2) Also printed: 'Density @ 60 F, lb/gal 8.02 lb/USG'. B, Mo, S and pour point not printed.
- (tier2) Row label 'Flash Point Deg C' is visible on the page image but missing from the text layer.

#### INFINEUM_D3503
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) 'applicable OEM performance specifications' are mentioned without names (DL2-11404.pdf p.1). No SDS in the archive.
- (tier2) Calcium is not printed in DL2-11404.pdf (checked on the page image); B and pour point not printed. Also printed: 'Density @ 60 F, lb/gal 8.00 lb/USG'.
- (tier2) Row label 'Flash Point Deg C' is visible on the page image but missing from the text layer.

#### INFINEUM_D3511
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) API FA-4 appears in the Performance table (13.2, 10W-30) but the description names only API CK-4; recorded with claim type 'meets' from the table context. No VM named. No SDS in the archive.
- (tier2) Flash point, KV40, KV100, Mo, B, S and pour point are not printed in DL2-15389.pdf (checked on the page image). Sulfated Ash method 'Calculated'. Also printed: 'Density @ 60 F, lb/gal 7.99 lb/USG'.

#### JINZHOU_DONGGONG_T3160
- (tier1) No revision date printed on DL2-11882.pdf.
- (tier1) Base Oil Type column read from the page image (Roman numerals are not in the text layer).
- (tier1) Claim types: CI-4/SL 'meets' (text 'Test data to meet ...'); other rows of the 'Dosage Reference' table 'other'. No VM/co-components, no SDS in the archive.
- (tier2) Density (20°C) and KV100 are printed as 'Report' with no value (DL2-11882.pdf p.1); left Missing.
- (tier2) Quality Index values are minimum limits ('≥'), not typical values. KV40, sulfated ash, Mg, P, B, Mo, S and pour point not printed.

#### JINZHOU_KANGTAI_KT31140
- (tier1) No revision date printed on DL2-12961.pdf. Supplier printed as 'KangTai . Lubricant Addtives' (WWW.JZKANGTAI.COM).
- (tier1) Claim type 'recommended' from 'DOSAGE RECOMMENDED'. No SAE grades, VM or SDS.
- (tier2) KV100 printed as 'Report' with no value (DL2-12961.pdf p.1).
- (tier2) Column header 'Typical Value' but each value printed with 'min'. Recorded as minimum specifications.
- (tier2) Density, KV40, sulfated ash, Mg, B, Mo, S and pour point not printed.

#### LUBRIZOL_16008
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) The 4.4 % by weight block lists 'API CF' and 'API SF' without an intro sentence; claim_type 'other'. Text: 'For full details of the specification cascade offered by LUBRIZOL® 16008 please refer to the Product Data Summary.' (not in archive).
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) TBN from text p.1: 'LUBRIZOL® 16008 has a TBN greater than 182.'
- (tier2) User decision 2026-10-17: density field stores the number 1.065 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 1.045 1.065 1.085', DL2-10871.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_3589C
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Footnote 1 ('Product at 6.15 % by weight provides 11 TBN (ASTM D2896)') is finished-oil TBN, not package TBN; kept in route limits only.
- (tier1) Footnote 2: Kolomna approval at 6.2 % by weight plus a 0.8 % by weight booster (booster not named).
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 1.069 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 1.049 1.069 1.089', DL2-10629.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_3700D
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) Zinc is on page 2, which is image-only (DL2-10633.pdf p.2); read visually: 1.11 / 1.23 / 1.35.
- (tier2) User decision 2026-10-17: density field stores the number 0.999 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.979 0.999 1.019', DL2-10633.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_3700
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.981 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.961 0.981 1.001', DL2-10632.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_4986D
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.973 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993', DL2-10654.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_4986E
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.973 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993', DL2-10655.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_4986F
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.974 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.954 0.974 0.994', DL2-10656.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_4986G
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.976 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.956 0.976 0.996', DL2-10657.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_4986
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.973 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993', DL2-10653.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_4987
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) DL2-10658.pdf and DL2-10659.pdf are byte-identical (same MD5); values cited from DL2-10658.pdf.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.973 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993', DL2-10658.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_CV1100
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Restriction printed in the claims list: 'API CK-4 / SN claim limited to SAE 15W-40 viscosity grade in select Group II base oils.' (route limits).
- (tier1) API FA-4 block requires 2.0 wt% LUBRIZOL® CV6320 top treat (component #79).
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.952 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.932 0.952 0.972', DL2-11503.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_CV1103
- (tier1) DL2-14978.pdf is a Lubrizol 'Product Data Sheet' (PDS). The credentials table has two '14.30% by weight' columns with no other header; the second column (only API FA-4, Cummins CES 20087, DDC 93K223) appears to be the CV6320 top-treat FA-4 route described in the text, but the table does not say so.
- (tier1) Claim codes: A -> 'approval', M -> 'meets', L ('Licensable against an active API category') -> kept as 'other', with the code recorded in the scope note (user decision 2026-10-17). Column 1 also marks API FA-4 'L' without mentioning CV6320; recorded as printed.
- (tier1) Treat rate printed '14.30% by weight' in the table vs '14.3wt%' in the text (same value). No SDS in the archive.
- (tier1) User decision 2026-10-17: 7 claims with Lubrizol code 'L' keep their claim_type; the code and its legend text are recorded in the scope note.
- (tier2) Density field holds SPECIFIC GRAVITY @ 15.6 C (0.953, ASTM D 4052); 'LBS PER GAL @ 15.6 C 7.94 lbs CALCULATED' also printed.
- (tier2) TBN, Mg, B and Mo not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.953 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 SPGRAV ASTM D 4052', DL2-14978.pdf p.2), not a density in kg/m3; flagged for review.

#### LUBRIZOL_CV2301
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Treat rate is printed per 'Recommended for use at' block (11.7, 10.7, 9.1, 8.2 % by weight); the 8.2 % block intro mentions a 'booster' that is not named.
- (tier1) SDS DL2-13713.pdf p.1 'Recommended use: Heavy Duty Diesel'.
- (tier2) Tables are on TDS page 2 (DL2-13065.pdf p.2). Density field holds SPECIFIC GRAVITY @ 15.6 C. Package TBN, Mg, B, Mo, S not printed.
- (tier2) SDS DL2-13713.pdf p.2 component shares (not element contents): Mineral oil 40 – 50%; Zinc alkyl dithiophosphate 5 – 10%; Calcium sulfonate 1 – 5%; Alkylated phenol 0.1 – 0.5%.
- (tier2) SDS p.5 Section 9 values agree with the TDS (no conflicts); SDS also prints viscosities at 25 °C (5753 mm2/s), 20 °C (8574 mm2/s) and 50 mPa.s at 122.4 °C.
- (tier2) User decision 2026-10-17: density field stores the number 0.982 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.962 0.982 1.002', DL2-13065.pdf p.2), not a density in kg/m3; flagged for review.

#### LUBRIZOL_CV2601
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER GAL also printed.
- (tier2) Physical values (p.1) in the 'Target' column; chemical values (p.2) in the 'Typical' column.
- (tier2) TBN, Mo and S are not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.955 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.935 0.955 0.975', DL2-11702.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_CV3515
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) 'Cummins CES 20078' is printed twice in the claims list (DL2-15722.pdf p.1); recorded twice as printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.972 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.952 0.972 0.992', DL2-15722.pdf p.1), not a density in kg/m3; flagged for review.

#### LUBRIZOL_CV7540
- (tier1) Two Product Data Sheets: DL2-14638.pdf (Published on 20 Jan, 2020) and DL2-15581.pdf (Published on 13 May, 2022). Fields use the 2022 sheet. 2022 adds ACEA E7-22 (2022) and CAT ECF-2; the 2020 sheet lists neither. Cummins CES 20076/77/78 changed from L to A (see conflicts).
- (tier1) SAE grades from the 2022 text: 'Viscosity grade coverage across SAE 20W-50 and 15W-40'. Claim codes: A -> approval, M -> meets, L -> other (code recorded in the scope note per user decision 2026-10-17). No SDS in the archive.
- (tier1) User decision 2026-10-17: 2 claims with Lubrizol code 'L' keep their claim_type; the code and its legend text are recorded in the scope note.
- (tier2) Typical characteristics identical in both sheets (DL2-14638.pdf p.2 and DL2-15581.pdf p.2). Density/specific gravity, TBN and Mo not printed.

#### MINGLAN_T3161A
- (tier1) No revision date and no supplier legal name printed on T3161A%20%20MULTIFUNCTIONAL%20ENGINE%20OIL%20ADDITIVE%20FOR%20CI.pdf; supplier recorded from the archive folder name 'MINGLAN CHEMICAL'.
- (tier1) Claim type 'other': 'The following performance levels can be achieved with oils formulated with T3161A'. No SAE grades, base oils, co-components or SDS.
- (tier1) CF-4/SJ dose '6.0/6.2' and CD/SF dose '4.6/4.8' (dosage column 'Dosage (m%)'): two values separated by '/', meaning not stated; value left null with printed text kept.
- (tier2) Kinematic Viscosity (100 °C) printed as 'report' (no value). Density, KV40, sulfated ash, S and pour point not printed.
- (tier2) Supplier-name note: 'MINGLAN CHEMICAL' is the archive folder name; the sheet prints no company name.
- (tier2) 2026-10-17: sulfated ash calculated (≥13.3 wt.%) from the TDS element minimums with ASTM D874 factors (NOT from the datasheet).

#### MINGLAN_T3161
- (tier1) No revision date and no supplier legal name printed on T3161%20%20MULTIFUNCTIONAL%20ENGINE%20OIL%20ADDITIVE%20FOR%20CI.pdf; supplier recorded from the archive folder name 'MINGLAN CHEMICAL'.
- (tier1) Claim type 'other': 'The following performance levels can be achieved with oils formulated with T3161'. No SAE grades, base oils, co-components or SDS.
- (tier1) 'Reference dosage' column 'Dosage' has no unit printed (T3161A prints 'm%'); unit left null.
- (tier2) Kinematic Viscosity (100 °C) printed as 'report' (no value). Density, KV40, sulfated ash, S and pour point not printed.
- (tier2) Supplier-name note: 'MINGLAN CHEMICAL' is the archive folder name; the sheet prints no company name.

#### MINGYUEKEJI_MY_P3168
- (tier1) No revision date printed on 'TDS of P3168.pdf'. Supplier from the archive folder 'MINGYUEKEJI' (sheet header prints only Chinese text '高品质润滑油添加剂生产商').
- (tier1) Grades printed only as 'Multi-grade' / 'Mono-grade'. Claims from the 'Dosage' table recorded as 'other'; API CF4 and CF also as 'meets' from the text 'exceeding ... engine testing requirements'.
- (tier2) KV40, sulfated ash, Mg, B, Mo, S and pour point not printed. Nitrogen method printed as ASTM D4951.

#### CHEVRON_N204
- (tier1) Image-only PDF (no text layer); all values read visually from 200 dpi page renders.
- (tier1) NEW product (no old Product_JSON file). Decision (a) said 'all properties missing and image-only noted', the later instruction says to read image-only PDFs like text PDFs; values were read and entered as Reported.
- (tier1) DL2-12494.pdf p.1: 'Company Identification: Indian Additives Ltd.' with Chevron Oronite logo and Oronite emergency contacts; supplier recorded as Indian Additives Ltd. (Revision Number: 0, MSDS : 46286).
- (tier1) DL2-12494.pdf p.1 Section 2 component shares (not element contents): Highly refined mineral oil (C15 - C50) 40 - 45 %weight; Zinc alkyl dithiophosphate (68649-42-3) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-69-7) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-68-6) 1 - 5 %weight.
- (tier1) Package vs component: MSDS only says 'Product Use: Automotive lubricant additive' (p.1); filed as a package per decision (a).
- (tier1) Only an MSDS is available; package type, claims, SAE grades, base oils and co-components are not printed.
- (tier2) Image-only PDF (no text layer); all values read visually from 200 dpi page renders.
- (tier2) NEW product (no old Product_JSON file). Decision (a) said 'all properties missing and image-only noted', the later instruction says to read image-only PDFs like text PDFs; values were read and entered as Reported.
- (tier2) DL2-12494.pdf p.1: 'Company Identification: Indian Additives Ltd.' with Chevron Oronite logo and Oronite emergency contacts; supplier recorded as Indian Additives Ltd. (Revision Number: 0, MSDS : 46286).
- (tier2) DL2-12494.pdf p.1 Section 2 component shares (not element contents): Highly refined mineral oil (C15 - C50) 40 - 45 %weight; Zinc alkyl dithiophosphate (68649-42-3) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-69-7) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-68-6) 1 - 5 %weight.
- (tier2) Package vs component: MSDS only says 'Product Use: Automotive lubricant additive' (p.1); filed as a package per decision (a).
- (tier2) TBN, sulfated ash, KV100, pour point and all elements are not printed. Section 5 lists combustion oxides of Calcium, Zinc, Molybdenum, Boron, Phosphorus, Nitrogen, Sulfur (qualitative only).
- (tier2) DL2-12494.pdf p.5 also prints 'Specific Gravity: 0.9850 @ 15.6°C (60°F)'; same value as density.

#### CHEVRON_N216
- (tier1) Image-only PDF (no text layer); all values read visually from 200 dpi page renders.
- (tier1) NEW product (no old Product_JSON file). Decision (a) said 'all properties missing and image-only noted', the later instruction says to read image-only PDFs like text PDFs; values were read and entered as Reported.
- (tier1) DL2-12493.pdf p.1: 'Company Identification: Indian Additives Ltd.' with Chevron Oronite logo and Oronite emergency contacts; supplier recorded as Indian Additives Ltd. (Revision Number: 3, MSDS : 44378).
- (tier1) DL2-12493.pdf p.1 Section 2 component shares (not element contents): Highly refined mineral oil (C15 - C50) 40 - 45 %weight; Zinc alkyl dithiophosphate (68649-42-3) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-69-7) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-68-6) 1 - 5 %weight.
- (tier1) Package vs component: MSDS only says 'Product Use: Automotive lubricant additive' (p.1); filed as a package per decision (a).
- (tier1) Only an MSDS is available; package type, claims, SAE grades, base oils and co-components are not printed.
- (tier2) Image-only PDF (no text layer); all values read visually from 200 dpi page renders.
- (tier2) NEW product (no old Product_JSON file). Decision (a) said 'all properties missing and image-only noted', the later instruction says to read image-only PDFs like text PDFs; values were read and entered as Reported.
- (tier2) DL2-12493.pdf p.1: 'Company Identification: Indian Additives Ltd.' with Chevron Oronite logo and Oronite emergency contacts; supplier recorded as Indian Additives Ltd. (Revision Number: 3, MSDS : 44378).
- (tier2) DL2-12493.pdf p.1 Section 2 component shares (not element contents): Highly refined mineral oil (C15 - C50) 40 - 45 %weight; Zinc alkyl dithiophosphate (68649-42-3) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-69-7) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-68-6) 1 - 5 %weight.
- (tier2) Package vs component: MSDS only says 'Product Use: Automotive lubricant additive' (p.1); filed as a package per decision (a).
- (tier2) TBN, sulfated ash, KV100, pour point and all elements are not printed. Section 5 lists combustion oxides of Calcium, Sulfur, Phosphorus, Nitrogen, Zinc, Boron (qualitative only).
- (tier2) DL2-12493.pdf p.4 also prints 'Coefficient of Therm. Expansion / °F: 0.000360' (no template field).
- (tier2) DL2-12493.pdf p.6 'REVISION STATEMENT: SECTION 09 - Physical/Chemical Properties information was deleted.'; the remaining Section 9 values on p.4 were recorded as printed.

#### CHEVRON_OLOA_59215
- (tier1) MB 228.3 and CES 20076/77 are printed as '(Approval in progress)' (DL2-13875.pdf p.1); recorded as claim_type 'other'.
- (tier1) PARATONE 24 SSI / 35 SSI VII doses are not printed.
- (tier1) No SDS in the archive for OLOA 59215.
- (tier2) Mg, flash point and pour point are not printed in DL2-13875.pdf (p.1 refers to the MSDS for handling).
- (tier2) Density: old Product_JSON gives 986.7 kg/m3 (converted); sheet prints 0.9867 g/cm³ (kg/l) at 15°C.

#### CHEVRON_OLOA_59230
- (tier1) Claim wording 'is developed to meet API CF-4 performance' (DL2-13876.pdf p.1) recorded as claim_type 'other'; please confirm whether this should count as 'meets'.
- (tier1) Composition text p.1: 'contains ashless dispersant, zinc dithiophosphate, metallic detergents and anti-oxidant' (no shares).
- (tier1) No SAE grades, base oils, co-components or formulation printed; no SDS in the archive.
- (tier2) Mg, B, Mo, S, flash point and pour point are not printed in DL2-13876.pdf.

#### CHEVRON_OLOA_59766
- (tier1) Only an SDS is in the archive for OLOA 59766 (Revision Number 14, SDS 23738); package type, claims, grades, base oils and co-components not printed. Supplier per Section 1.3: Chevron Oronite S.A.S.
- (tier1) 2026-10-17: package_type filled from the Chevron Oronite official web page https://www.oronite.com/products-technology/heavy-duty-motor-oils.html (NOT from the datasheet).
- (tier2) Only an SDS is in the archive for OLOA 59766 (Revision Number 14, SDS 23738); package type, claims, grades, base oils and co-components not printed. Supplier per Section 1.3: Chevron Oronite S.A.S.
- (tier2) TBN, sulfated ash, KV100, pour point and all elements not printed.
- (tier2) DL2-11731.pdf p.2-3 Section 3 component shares (not element contents): mineral oil 40 - 45 %weight; PIB succinimide-type amine reaction product (147880-09-9) 25 - 30 %weight; ZDDP (68784-31-6) 5 - 10 %weight; calcium alkylbenzene sulfonates 5 - 10, 5 - 10 and 1 - 5 %weight (722503-69-7 is listed twice).

#### CHEVRON_OLOA_61003
- (tier1) Claims are listed under 'performance claims can be made' (DL2-11032.pdf p.1); recorded as claim_type 'other'. Items with '*' are 'Approvals on going'.
- (tier1) VII PARATONE® 8006 named, dose not printed. No SAE grades or base oils printed. No SDS in the archive.
- (tier2) Calcium is printed as 'Calcium, as Sulfonate' (ASTM D 3712), which may not be total calcium.
- (tier2) Density field holds 'Specific Gravity, at 15°C' 0,968. Mg, B, Mo, S, flash point and pour point not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.968 (specific gravity (dimensionless)), which is reported as specific gravity ('Specific Gravity, at 15°C (ASTM D 4052) 0,968', DL2-11032.pdf p.1), not a density in kg/m3; flagged for review.

#### RICHFUL_RF6066
- (tier1) The two TDS (DL2-13819.pdf 'TDS OF RF6066' and DL2-15451.pdf) carry no date, so the order of revisions cannot be determined. Density, KV100, TBN, Zn and Ca differ between documents (see conflicts) and are left null. DL2-13819.pdf matches the 2020 SDS (density 990, TBN 106); DL2-15451.pdf matches the 2021 SDS (density 0.988, 185 mm²/s), which suggests DL2-15451.pdf is the later TDS, but no date is printed.
- (tier1) Supplier spelled 'Xinxiang Richuful Lube Additive Co. Ltd.' in SDS DL2-13820.pdf p.1 and 'Xinxiang Richful Lube Additive Co., Ltd.' in SDS DL2-15831.pdf p.1.
- (tier1) DL2-15831.pdf (SDS 2021): body text is image/vector graphics; read visually from page renders.
- (tier1) Old Product_JSON mixed values from DL2-15451.pdf and DL2-13819.pdf without flagging the differences.
- (tier1) Claim type 'recommended' from the 'Recommended Treat Rate' tables. Storage/blending limits differ between the two TDS (45/65 ℃ vs 50/60 ℃).
- (tier2) The two TDS (DL2-13819.pdf 'TDS OF RF6066' and DL2-15451.pdf) carry no date, so the order of revisions cannot be determined. Density, KV100, TBN, Zn and Ca differ between documents (see conflicts) and are left null. DL2-13819.pdf matches the 2020 SDS (density 990, TBN 106); DL2-15451.pdf matches the 2021 SDS (density 0.988, 185 mm²/s), which suggests DL2-15451.pdf is the later TDS, but no date is printed.
- (tier2) Supplier spelled 'Xinxiang Richuful Lube Additive Co. Ltd.' in SDS DL2-13820.pdf p.1 and 'Xinxiang Richful Lube Additive Co., Ltd.' in SDS DL2-15831.pdf p.1.
- (tier2) DL2-15831.pdf (SDS 2021): body text is image/vector graphics; read visually from page renders.
- (tier2) Old Product_JSON mixed values from DL2-15451.pdf and DL2-13819.pdf without flagging the differences.
- (tier2) Component shares (not element contents): SDS DL2-15831.pdf p.2: base-oil distillates 10 - 39.9 %; ZDDP (68649-42-3) 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 9.9 %; molybdenum dithiocarbamate 0.1 – 1.99 %. SDS DL2-13820.pdf p.2 lists ingredients without percentages.
- (tier2) Sulfated ash, KV40, Mg, B, S and pour point not printed.
- (tier2) 2026-10-17: TBN, KV100, density, Ca, Zn filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=112 (NOT from the datasheet); the page agrees with DL2-15451.pdf and with the file's existing P, Mo, N.

#### RICHFUL_RF6069
- (tier1) TDS DL2-15618.pdf has no date; SDS DL2-15619.pdf: Issue/Revision date 1/4/2022, version 2.0 (body image/vector graphics, read visually).
- (tier1) KV100 differs: TDS 118 mm2/s vs SDS 142 mm²/s; TDS undated, so the field is left null (see conflicts).
- (tier1) RF0206 (1.9% in the CF-4 route) is not described on the sheet.
- (tier2) TDS DL2-15618.pdf has no date; SDS DL2-15619.pdf: Issue/Revision date 1/4/2022, version 2.0 (body image/vector graphics, read visually).
- (tier2) KV100 differs: TDS 118 mm2/s vs SDS 142 mm²/s; TDS undated, so the field is left null (see conflicts).
- (tier2) SDS DL2-15619.pdf p.2 component shares (not element contents): base-oil distillates 10 - 59.9 %; ZDDP (68649-42-3) 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 4.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S and pour point not printed.
- (tier2) 2026-10-17: KV100 filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=32 (NOT from the datasheet).

#### RICHFUL_RF6071L
- (tier1) Only an undated TDS is in the archive for RF6071L (no SDS). The sheet prints no company name; supplier left null (archive folder: Richful Lube Additive).
- (tier2) Only an undated TDS is in the archive for RF6071L (no SDS). The sheet prints no company name; supplier left null (archive folder: Richful Lube Additive).
- (tier2) Column headers 'Requirement Limit' / 'Typical Value'. Sulfated ash, KV40, Mg, B, S and pour point not printed.

#### RICHFUL_RF6077
- (tier1) TDS DL2-15536.pdf has no date; SDS DL2-15542.pdf Issue/Revision date 11/16/2023.
- (tier1) KV100 (TDS 160 vs SDS 150 mm2/s) and density (TDS 998 kg/m3 at 20 ℃ vs SDS 0.991 g/cm3 at 15 °C) differ; TDS undated, fields left null (see conflicts). The density temperatures also differ.
- (tier1) Claim type 'meets' from 'is compliant to API CI-4 specification'. OCP VII required but not named and no dose.
- (tier2) TDS DL2-15536.pdf has no date; SDS DL2-15542.pdf Issue/Revision date 11/16/2023.
- (tier2) KV100 (TDS 160 vs SDS 150 mm2/s) and density (TDS 998 kg/m3 at 20 ℃ vs SDS 0.991 g/cm3 at 15 °C) differ; TDS undated, fields originally left null; filled 2026-10-18 by user decision (see conflicts). The density temperatures also differ.
- (tier2) SDS p.2 component shares (not element contents): base-oil distillates 10 - 59.9 %; ZDDP 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 2.9 %; molybdenum dithiocarbamate 0.1 – 0.99 %.
- (tier2) SDS also prints vapour pressure 28.7 mmHg at 65 °C and 15.9 mmHg at 45 °C (no template field). Sulfated ash, KV40, Mg, B, S, pour point not printed.

#### RICHFUL_RF6078
- (tier1) Both TDS (DL2-15832.pdf and 'RF6078 - TDS.pdf') are undated; SDS DL2-15833.pdf revision 9/2/2021 (issue date printed '9/022021'); SDS body is image/vector graphics, read visually.
- (tier1) Density: TDS 972 kg/m3 vs SDS 975 kg/m³ (both 20 ℃); TDS undated, field left null (see conflicts).
- (tier1) The two TDS give different rates for the 'ACEA E7/API CI-4' row; see conflicts.
- (tier2) Both TDS (DL2-15832.pdf and 'RF6078 - TDS.pdf') are undated; SDS DL2-15833.pdf revision 9/2/2021 (issue date printed '9/022021'); SDS body is image/vector graphics, read visually.
- (tier2) Density: TDS 972 kg/m3 vs SDS 975 kg/m³ (both 20 ℃); TDS undated, field left null (see conflicts).
- (tier2) SDS p.2 component shares (not element contents): base-oil distillates 10 - 39.9 %; ZDDP 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 9.9 %; molybdenum dithiocarbamate 0.1 – 1.99 %.
- (tier2) Sulfated ash, KV40, Mg, B, N, S, pour point not printed.
- (tier2) 2026-10-17: density filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=109 (NOT from the datasheet).

#### RICHFUL_RF6079
- (tier1) TDS DL2-15535.pdf undated; bulletin 'RF6079 Diesel Engine Oil Additive Package.pdf' prints only 'Version 1'; SDS DL2-15541.pdf Issue/Revision 3/18/2022 (body image/vector graphics, read visually). All three agree on the shared values.
- (tier1) API CI-4 Plus (11.0%) appears only in the bulletin. OCP VII not named.
- (tier2) TDS DL2-15535.pdf undated; bulletin 'RF6079 Diesel Engine Oil Additive Package.pdf' prints only 'Version 1'; SDS DL2-15541.pdf Issue/Revision 3/18/2022 (body image/vector graphics, read visually). All three agree on the shared values.
- (tier2) SDS p.2 component shares (not element contents): hydrotreated heavy paraffinic distillate 10 – 59.9 %; ZDDP 3 – 17.9 %; overbased calcium sulfurized phenate 1 – 14.9 %; bis(nonylphenyl)amine 0.5 – 9.9 %; hindered phenolic ester 0.5 – 9.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.
- (tier2) User decision 2026-10-17: density field stores the number 1.0 (g/cm³), which is reported as specific gravity (relative density) ('Relative density : 1.000 g/cm³@20℃', DL2-15541.pdf p.5), not a density in kg/m3; flagged for review.

#### RICHFUL_RF6080
- (tier1) TDS issue date 2025-05-09 (p.1-2); SDS issue date 2025-04-08.
- (tier1) Claim wording: 'meets all ... certification requirements' recorded as 'meets'. VII and PPD required but not named.
- (tier2) TDS issue date 2025-05-09 (p.1-2); SDS issue date 2025-04-08.
- (tier2) SDS p.2 component shares (not element contents): hydrotreated heavy paraffinic distillate 10 - 59.9 %; ZDDP 5 - 19.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; bis(nonylphenyl)amine 0.5 - 9.9 %; hindered phenolic ester 0.5 - 9.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.

#### RICHFUL_RF6081
- (tier1) TDS issue date 2025-05-13 (p.1-2); SDS issue date 2025-04-09.
- (tier1) Claim wording: 'meets all ... certification requirements' recorded as 'meets'. VII and PPD required but not named.
- (tier2) TDS issue date 2025-05-13 (p.1-2); SDS issue date 2025-04-09.
- (tier2) SDS p.2 component shares (not element contents): hydrotreated heavy paraffinic distillate 10 - 59.9 %; ZDDP 5 - 19.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; bis(nonylphenyl)amine 0.5 - 9.9 %; hindered phenolic ester 0.5 - 9.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.

#### RICHFUL_RF6088F
- (tier1) TDS DL2-15839.pdf undated; SDS DL2-15840.pdf issue date 17/10/2024.
- (tier1) KV100 (TDS 177 vs SDS 178.2 mm2/s) and density (TDS 963 kg/m3 vs SDS 0.958 g/cm3, both 20 ℃) differ; TDS undated, fields left null (see conflicts).
- (tier1) Claim type 'meets' from 'Greatly meet API CK-4 specification'.
- (tier2) TDS DL2-15839.pdf undated; SDS DL2-15840.pdf issue date 17/10/2024.
- (tier2) KV100 (TDS 177 vs SDS 178.2 mm2/s) and density (TDS 963 kg/m3 vs SDS 0.958 g/cm3, both 20 ℃) differ; TDS undated, fields originally left null; filled 2026-10-18 by user decision (see conflicts).
- (tier2) SDS p.2 component shares (not element contents): distillate 10 – 59.9 %; ZDDP 3 – 17.9 %; overbased calcium sulfurized phenate 1 – 14.9 %; hindered phenolic ester 1 – 14.9 %; bis(nonylphenyl)amine 1 – 9.9 %.
- (tier2) KV40, Mg, B, Mo, S, pour point not printed.

#### RICHFUL_RF6088
- (tier1) TDS DL2-15452.pdf undated; SDS DL2-15838.pdf Issue/Revision 2/25/2024. Shared values agree.
- (tier1) Claim type 'meets' from 'is compliant to API CK-4&ACEA E11 specification'. OCP VII not named.
- (tier2) TDS DL2-15452.pdf undated; SDS DL2-15838.pdf Issue/Revision 2/25/2024. Shared values agree.
- (tier2) SDS p.2 component shares (not element contents): distillate 10 – 59.9 %; ZDDP 3 – 17.9 %; overbased calcium sulfurized phenate 1 – 14.9 %; bis(nonylphenyl)amine 1 – 14.9 %; hindered phenolic ester 1 – 14.9 %. SDS also prints vapour pressure at 40 °C 16.2mmHg.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.955 (g/cm³), which is reported as specific gravity (relative density) ('Relative density : 0.955 g/cm3@20℃', DL2-15838.pdf p.5), not a density in kg/m3; flagged for review.

#### RICHFUL_RF6089
- (tier1) Only an SDS (DL2-15841 (1).pdf, issue/revision 07/25/2025) is in the archive for RF6089; no TDS. Supplier from Section 1.3 'Manufacturer' (rendered as graphics, read from the page image).
- (tier1) Package type, claims, grades, treat rates, base oils and co-components are not printed; could be looked up later in a Richful TDS.
- (tier2) Only an SDS (DL2-15841 (1).pdf, issue/revision 07/25/2025) is in the archive for RF6089; no TDS. Supplier from Section 1.3 'Manufacturer' (rendered as graphics, read from the page image).
- (tier2) Package type, claims, grades, treat rates, base oils and co-components are not printed; could be looked up later in a Richful TDS.
- (tier2) SDS p.2 component shares (not element contents): distillate 10 - 59.9 %; ZDDP 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; bis(nonylphenyl)amine 1 - 14.9 %; hindered phenolic ester 1 - 14.9 %.
- (tier2) TBN, sulfated ash, KV40, elements and pour point not printed.

#### RICHFUL_RF6400
- (tier1) Two undated TDS (DL2-15849.pdf, 'RF6400 TDS.pdf') with identical content; SDS 'RF6400 MSDS.pdf' (HCS-2012 format, 7/25/2022) and DL2-15850.pdf (REACH, rev. 6/7/2023). All shared values agree.
- (tier1) Document type: 'RF6400 MSDS.pdf' prints 'Safety Data Sheet' in the title; recorded as SDS.
- (tier1) Grades listed as '... 20W-50, 40, 50 and etc.' (open list).
- (tier2) Two undated TDS (DL2-15849.pdf, 'RF6400 TDS.pdf') with identical content; SDS 'RF6400 MSDS.pdf' (HCS-2012 format, 7/25/2022) and DL2-15850.pdf (REACH, rev. 6/7/2023). All shared values agree.
- (tier2) Document type: 'RF6400 MSDS.pdf' prints 'Safety Data Sheet' in the title; recorded as SDS.
- (tier2) SDS DL2-15850.pdf p.2 component shares (not element contents): distillate 10 - 59.9 %; PIB succinimide (84605-20-9) 8 - 44.9 %; unnamed component (CAS '-') 1 – 14.9 %; calcium sulfonate (70024-69-0) 1 - 24.9 %; ZDDP (4259-15-8) 3 - 17.9 %; alkylated diphenylamine 0.5 - 2.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.

#### RICHFUL_RF6406
- (tier1) Two undated TDS: DL2-14746.pdf ('TDS OF RF6406', prints minimum values only) and DL2-15456.pdf (index ranges + typicals); SDS RF6406.pdf issue 11/26/2021, revision 04/21/2025.
- (tier1) Supplier: neither TDS prints a company name and SDS Section 1.3 is blank (RF6406.pdf p.1); supplier left null.
- (tier1) TBN minimum differs (DL2-14746.pdf ≥180 vs DL2-15456.pdf index 168-198); CF/SF treat rate differs (3.7 vs 4.1 %); both TDS undated, see conflicts.
- (tier1) Grades printed only as 'Multi' / 'Mono'.
- (tier1) 2026-10-17: API CF/SF (Multi) treat rate filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=130 (NOT from the datasheet).
- (tier2) Two undated TDS: DL2-14746.pdf ('TDS OF RF6406', prints minimum values only) and DL2-15456.pdf (index ranges + typicals); SDS RF6406.pdf issue 11/26/2021, revision 04/21/2025.
- (tier2) Supplier: neither TDS prints a company name and SDS Section 1.3 is blank (RF6406.pdf p.1); supplier left null.
- (tier2) TBN minimum differs (DL2-14746.pdf ≥180 vs DL2-15456.pdf index 168-198); CF/SF treat rate differs (3.7 vs 4.1 %); both TDS undated, see conflicts.
- (tier2) SDS p.2 component shares (not element contents): base-oil distillates 10 - 59.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; ZDDP 3 - 29.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed. DL2-14746.pdf prints density and KV100 as 'Report' (no value).
- (tier2) 2026-10-17: TBN filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=130 (NOT from the datasheet).

#### RICHFUL_RF6408
- (tier1) Only an undated TDS (DL2-15534.pdf); no company name printed (supplier left null; archive folder 'Richful Lube Additive'). No SDS in the archive.
- (tier1) Claim type 'other': text says the oils 'passed Mack T-8A, Caterpillar 1K, Sequence VIII and Mack T-9 engine tests and all bench tests' (no 'meets' wording).
- (tier2) Only an undated TDS (DL2-15534.pdf); no company name printed (supplier left null; archive folder 'Richful Lube Additive'). No SDS in the archive.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.

#### SAMA_P2021A
- (tier1) DL2-12295.pdf prints no company name and no date; supplier left null (archive folder 'SAMA'). Only a product brochure, no SDS.
- (tier1) Claims are a bulleted 'Profile' list without approval/meets wording; recorded as claim_type 'other'.
- (tier1) No treat rate is printed (only 'has the lowest VII and DI treat-rates in the market'); treat_rate_matrix left Missing.
- (tier1) Bar chart p.2 ('% Performance Reserve - P2021A additive': Mack T12, OM 501LA, Mack T11 vs limits) has no formulation; not recorded.
- (tier2) DL2-12295.pdf prints no company name and no date; supplier left null (archive folder 'SAMA'). Only a product brochure, no SDS.
- (tier2) No test methods printed. KV40, elements and pour point not printed.

#### TIANHE_P_TEC_3232
- (tier1) No date printed on DL2-12939.pdf; supplier from the logo 'TIANHE CHEMICALS' (website ENGLISH.TIANHECHEM.COM). No SDS in the archive.
- (tier1) TREAT RATE table (p.2) has a 'Total base number, mg KOH/g' row with no values (checked on the page image).
- (tier1) Claim type 'meets' from 'surpasses the standard engine tests of API CF4/CF and the OEM requirements of MB 228.1'; table rows 'recommended'.
- (tier2) User decision 2026-10-17: density stored exactly as printed (1.0130, unit 'kg/m3', DL2-12939.pdf p.1) with the note 'suspected unit error — verify'. Flagged for review.
- (tier2) No date printed on DL2-12939.pdf; supplier from the logo 'TIANHE CHEMICALS' (website ENGLISH.TIANHECHEM.COM). No SDS in the archive.
- (tier2) Values are under the column 'Specification' without min/max; value_kind set to 'specification'. KV40, sulfated ash, Mg, B, Mo, N, S, pour point not printed.

#### TREE_TRADING_NT513
- (tier1) No date printed on DL2-14797.pdf; supplier from the footer 'Tree Trading FIZ LLC'. No SDS in the archive.
- (tier1) Claims listed in a table without approval wording, except 'MB 228.3 (Blanket Approval)'; others recorded as 'other' ('(Level)' kept where printed).
- (tier1) 'The typical finished oil BN is 10.1 mg KOH/g at the standard treat of 11.2 wt%' is finished-oil TBN, not package TBN (not entered).
- (tier2) Flash point, Mg, B, S and pour point not printed. Mo printed in ppm.
- (tier2) User decision 2026-10-17: density field stores the number 0.99 (specific gravity (dimensionless)), which is reported as specific gravity ('Specific Gravity, at 15°C ASTM D4052 0.99', DL2-14797.pdf p.1), not a density in kg/m3; flagged for review.

#### WUXI_WX3118
- (tier1) No company name or date printed on DL2-13534.pdf (website WWW.WXNFCN.CN/EN); supplier left null (archive folder 'Wuxi South Petroleum'). No SDS in the archive.
- (tier1) Claim type 'recommended' from the treat-rate table (no approval/meets wording).
- (tier1) Grades printed as '30,40,50,10W/30,15W/40,20W/40,' (trailing comma).
- (tier2) KV100 and Density at 20℃ printed as 'Report' (no value). Values are minimum limits (column 'Limit'), not typicals.
- (tier2) Element methods printed as 'ASTM D - 4628' / 'ASTM D - 3228' as on the sheet.

#### WUXI_WX3326
- (tier1) No company name or date printed on DL2-13538.pdf (website WWW.WXNFCN.CN/EN); supplier left null (archive folder 'Wuxi South Petroleum'). No SDS in the archive.
- (tier1) Claim type 'recommended' from the treat-rate table (no approval/meets wording).
- (tier1) Description: 'Its API CF-4/SL/SM engine oil has excellent high temperature detergency, antioxidation, antiwear and anticorrosion properties.'
- (tier2) KV100 and Density at 20℃ printed as 'Report' (no value). Values are minimum limits (column 'Limit'), not typicals.
- (tier2) Element methods printed as 'ASTM D - 4628' / 'ASTM D - 3228' as on the sheet.

### Additive components

#### AFTON_HITEC_8767B
- (tier1) DL2-10367.pdf is the HiTEC® 8766B bulletin; HiTEC® 8767B appears only as a second column of 'Typical Characteristics' and as a dose column in the 'Recommended Dosage' table (p.2). Per decision (b) only the 8767B column is used here.
- (tier1) Function / chemical family of HiTEC® 8767B are not stated anywhere in the archive; function, chemical_family, active content and carrier left Missing; component_subtype left null (no VM/PPD statement). Could be looked up later in an Afton bulletin for 8767B.
- (tier1) Physical properties printed for HiTEC® 8767B (no field in the component template; DL2-10367.pdf p.2, 'Typical Characteristics'): Density at 15°C, g/ml 0.918; Flash Point, °C (PMCC) 135 min.; Kinematic Viscosity at 100°c, mm2/s 187.
- (tier1) Treat rate: only one dose (3.3% in the 8766B SAE 10W-40 route) is printed; no min/max/typical range for 8767B on its own.
- (tier1) No old Product_JSON file exists for HiTEC 8767B; folder name AFTON_HITEC_8767B created per the naming rule.

#### LUBRIZOL_CV6320
- (tier1) CV6320 is filed under 'Additive packages/LUBRIZOL' but is a component ('Ashless Antiwear Performance Booster', DL2-12015.pdf p.1). Not a VM or PPD, so only general.json is created.
- (tier1) Chemical family is not named. SDS DL2-12016.pdf p.2 Section 3 lists 'Olefin sulfide 1 - 5%', 'Ethoxylated alcohol 0.5 - 1%' and '++ Aryl thiophosphate (597-82-0) 0.1 - 0.5%' (component shares); chemical_family and active_content left Missing.
- (tier1) Function-specific marker not in template: SULFUR 0.60 (% weight, Typical; DL2-12015.pdf p.1).
- (tier1) Physical properties (no field in the component template), DL2-12015.pdf p.1 (Target column): FLASH POINT, C, PMCC 181; POUR POINT, C -21; SPECIFIC GRAVITY @ 15.6 C 0.849 / 0.869 / 0.889 (min/target/max); VISCOSITY @ 100 C, CST 69; VISCOSITY @ 40 C, CST 787; LBS PER U.S. GAL @ 15.6 C 7.24. SDS DL2-12016.pdf p.4-5 prints the same: flash 181 °C (Pensky-Martens Closed Cup), relative density 0,849 - 0,889 (15,6 °C), 787 mm2/s (40 °C), 69 mm2/s (100 °C), pour point -21 °C.
- (tier1) SDS supplier block names LUBRIZOL FRANCE (Rouen); TDS is The Lubrizol Corporation. SDS Issue Date 21.12.2017, Version 1.1.
- (tier1) 2026-10-17: Ca, Mg, Zn, Mo markers set to N/A (ashless booster); P marker remains Missing.

#### RF6602
- (tier1 VM) TDS DL2-14874.pdf ('TDS OF RF6602') undated; SDS RF6602.pdf issue/revision 18/2/2022.
- (tier1 VM) Physical properties (no field in the component templates): TDS DL2-14874.pdf p.1 (Index / Typical, method): Kinematic Viscosity (100℃) 1100-1850 / 1360 mm2/s ASTM D445; Flash Point (COC) ≮180 / 210 ℃ ASTM D92; Density (20℃) 850-950 / 919 kg/m3 ASTM D4052; Color ＜0.5 ASTM D1500. SDS RF6602.pdf Section 9: Flash point 160 °C; Viscosity, kinematic 53691mm²/s (40℃); Density 0.9 g/cm³ (no temperature).
- (tier1 VM) Flash point differs: TDS index '≮180' / typical 210 ℃ (COC) vs SDS 'Flash point : 160 °C' (no method). No template field; recorded here, not resolved.
- (tier1 VM) Density: TDS 919 kg/m3 (20℃) vs SDS 0.9 g/cm³ - same value rounded to one decimal, not a conflict.
- (tier1 VM) Applications (TDS p.1): 'suitable for the blending of hydraulic oil (especially low temperature hydraulic oil), gear oil, shock absorber oil, transmission oil and other kinds of oil' - no compatibility restrictions printed (compatibility_restrictions left Missing; 150N / 500N / Group Ⅲ 6# are only the thickening-test oils).
- (tier1 VM) No recommended treat rate is printed (only test doses 1/3/5 % and 6/10 %); treat_rate left Missing. Secondary function not stated (text: 'can effectively increase the viscosity index and improve the low temperature performance of the oil').
- (tier1 VM) 2026-10-17: function-specific markers (TBN, Ca, Mg, P, Zn, Mo) set to N/A - not applicable to a PMA VII.
- (tier2 VM) TDS DL2-14874.pdf ('TDS OF RF6602') undated; SDS RF6602.pdf issue/revision 18/2/2022.
- (tier2 VM) Physical properties (no field in the component templates): TDS DL2-14874.pdf p.1 (Index / Typical, method): Kinematic Viscosity (100℃) 1100-1850 / 1360 mm2/s ASTM D445; Flash Point (COC) ≮180 / 210 ℃ ASTM D92; Density (20℃) 850-950 / 919 kg/m3 ASTM D4052; Color ＜0.5 ASTM D1500. SDS RF6602.pdf Section 9: Flash point 160 °C; Viscosity, kinematic 53691mm²/s (40℃); Density 0.9 g/cm³ (no temperature).
- (tier2 VM) Flash point differs: TDS index '≮180' / typical 210 ℃ (COC) vs SDS 'Flash point : 160 °C' (no method). No template field; recorded here, not resolved.
- (tier2 VM) Density: TDS 919 kg/m3 (20℃) vs SDS 0.9 g/cm³ - same value rounded to one decimal, not a conflict.
- (tier2 VM) Thickening table (TDS p.1): reference oils 150N, 500N, Group Ⅲ 6# at 0/1/3/5 % treat; ΔKV100 values are Calculated (difference from the 0 % row). No test method printed -> 'usable' false.
- (tier2 VM) Shear test 'The Shear of Diesel Injector Nozzle' (30 and 250 cycles) in 150N at 6 % and 10 %: no standard (e.g. ASTM D6278/D7109) and no SSI printed; percentage KV100 loss calculated. Units for KV100 not printed in that table.
- (tier2 VM) Polymer form (solid/concentrate) not stated; appearance 'Clear、bright、no sediment viscous liquid'. Treat range by SAE grade, HTHS, CCS/MRV impact, gelation and dissolution temperature not printed.
- (tier2 VM) Storage (TDS p.1): short-term storage/transport ≤ 75℃, long-term ≤ 45℃ (not a dissolution/blend temperature).
- (tier2 VM) Old Product_JSON uses record id 'RF6602' (no RICHFUL_ prefix); kept per decision (d).
