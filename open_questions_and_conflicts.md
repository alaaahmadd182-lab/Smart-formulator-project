# Open questions and conflicts (all products)

Generated from the open_questions and conflicts arrays of every output file, in work-list order.

## 1. AFTON_HITEC_12010
- (tier1) Supplier: Section 1 of DL2-15021.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier' (first: Afton Chemical Asia Pte. Ltd.; also Afton Chemical Corporation, Richmond, VA). Confirm which name to record.
- (tier1) Only an SDS is in the archive for HiTEC 12010 (DL2-15021.pdf). No TDS/product bulletin, so package type, claims, SAE grades, treat rates, co-components and published formulations are all missing; these could be looked up later in an Afton product bulletin.
- (tier1) package_type left Missing: the SDS (p.1) only says 'Lubricating Oil Additive'; it does not state PVL/CVL/HDDO etc. The old Product_JSON subclass 'performance additive package' is not printed on the sheet.
- (tier2) TBN, sulfated ash, all elements (Ca, Mg, Zn, P, B, Mo, N, S) and pour point are not printed in DL2-15021.pdf; Section 9 (p.6-7) has no pour point entry.
- (tier2) DL2-15021.pdf p.2 Section 3 lists 'Phosphorodithioic acid, mixed O,O-bis(2-ethylhexyl and iso-Bu and iso-Pr) esters, zinc salts' (CAS 85940-28-9) at 10 - 15 %. This is a ZDDP component share, not Zn or P element content, so Zn/P stay Missing.
- (tier2) DL2-15021.pdf p.2 Section 3 lists two base-oil carriers (hydrotreated heavy paraffinic 64742-54-7, 15 - 25 %; solvent-dewaxed heavy paraffinic 64742-65-0, 15 - 25 %) and p.15 (Korea ISHL) lists 'Mineral oil 35 - 45' %. The package templates have no carrier field.
- (tier2) Density: the old Product_JSON gives 1044 kg/m3 (converted); the sheet prints 1.044 g/cm³ at 15°C (p.6). Same value, kept in the printed unit.

## 2. AFTON_HITEC_12200
- **Conflict (tier1)** `tier1.performance_claims / tier1.treat_rate_matrix (MTU 2.0, row 10.3% + 5.0% HiTEC® 12255, SAE 15W-40, GP I)`: DL2-11412.PDF p.2 (05/18): dot in MTU 2.0 column; DL2-14639.pdf p.2 (08/18): no dot in MTU 2.0 column — 05/18 vs 08/18 bulletin. Newer (08/18) used in the fields; not resolved.
- **Conflict (tier1)** `tier1.performance_claims / tier1.treat_rate_matrix (DDC 93K215, row 11.7% + 0.9% HiTEC® 12260, SAE 10W-30, GP II)`: DL2-11412.PDF p.2 (05/18): no dot in DDC 93K215 column; DL2-14639.pdf p.2 (08/18): dot in DDC 93K215 column — 05/18 vs 08/18 bulletin. Newer (08/18) used in the fields; not resolved.
- (tier1) Product name differs between documents: bulletins DL2-11412.PDF p.1-2 and DL2-14639.pdf p.1-2 print 'HiTEC® 12200' / 'HiTEC® 12200 HDEO Additive Package'; SDS DL2-12074.pdf p.1 prints 'HiTEC® 12200 Performance Additive' (SDS no. H12200).
- (tier1) Supplier: bulletins (DL2-14639.pdf p.2) name Afton Chemical Corporation; SDS DL2-12074.pdf p.1 lists Afton Chemical Asia Pte. Ltd. and other Afton entities under 'Manufacturer / Supplier'.
- (tier1) revision_date: bulletins print only '05/18' (DL2-11412.PDF p.2) and '08/18' (DL2-14639.pdf p.2) in the copyright line; SDS DL2-12074.pdf p.1 'Date of issue/Date of revision: 7/16/2019'. product.revision_date is a list in source_file order.
- (tier1) Claim type: every matrix column sits under the printed header 'Approvals' (DL2-14639.pdf p.2), including API categories, so claim_type = 'approval'. Columns MB 228.1, MB 229.1 and MAN 3275 carry footnote 5 'Meets requirements of (MRO)' and are set to 'meets'. Please confirm this reading.
- (tier1) Treat rates and booster doses are printed as '%' with no mass/volume basis (DL2-14639.pdf p.2); only footnote 3 says '% wt'. Unit kept as '%'.
- (tier1) Rows and columns only in the 08/18 bulletin (DL2-14639.pdf p.2), absent from 05/18 (DL2-11412.PDF p.2): row '10.8% + 0.9% HiTEC® 12260, SAE 10W-30, GP II' (API CI-4, API SL); row '10.8% + 0.6% HiTEC® 9552, SAE 10W-40, GP II/III' (API SN, API SL, API SJ, ACEA A3/B4-16, MB 229.3, RN 0700); columns API SN, MB 229.3, RN 0700. Not treated as conflicts (additions, not disagreements).
- (tier1) Footnote 6 differs: 05/18 (DL2-11412.PDF p.2) '6 Formulations, available in Q2 2018' on the two SAE 10W-40 rows; 08/18 (DL2-14639.pdf p.2) '6 11.15% HiTEC® 12252 = 10.8% HiTEC® 12200 + 0.35% HiTEC® 9552' on the 10.8% SAE 15W-40 GP I row.
- (tier1) No complete published formulation (all ingredients summing to 100 wt.%) is printed; published_formulations left Missing. The bar charts on DL2-14639.pdf p.2 (Mack T-12, Cat 1K, Seq IIIF, T8E vs 'API CI-4 Limit'/'Reserve') have no numeric values and were not recorded.
- (tier1) Old Product_JSON has no claims, route matrix or co-components for this product although both bulletins print them; the new file fills them from DL2-14639.pdf p.2.
- (tier2) Sulfated ash, all elements (Ca, Mg, Zn, P, B, Mo, N, S) and pour point are not printed in any of the three documents.
- (tier2) SDS DL2-12074.pdf p.2 Section 3 component shares (not element contents, so element fields stay Missing): overbased calcium sulfurized tetrapropenyl phenate 5 - 10 %; two zinc dialkyldithiophosphates 3 - 5 % each; base-oil distillates 15 - 25 % (x2) and 1 - 3 % (x2).
- (tier2) SDS DL2-12074.pdf p.20 (Japan PRTR) lists 'Boron compounds 5 - 10' %. This is a component share, not boron content; B stays Missing.
- (tier2) Density: old Product_JSON gives 989 kg/m3 (converted); the sheet prints 0.989 g/ml at 15°C (DL2-14639.pdf p.2). Same value, kept in printed unit.

## 3. AFTON_HITEC_12208
- (tier1) Only a product bulletin is available for HiTEC 12208 (no SDS in the archive).
- (tier1) Claim wording: the table header says 'Approvals', the text (p.2) says 'can be formulated into premium lubricant meeting API CK-4', 'can also be formulated into API FA-4 lubricant' and 'It can also meet Cummins approvals'. claim_type set to 'approval' from the table header; please confirm.
- (tier1) Bar charts on DL2-15364.pdf p.2 (Mack T-12 wear, Volvo T-13 oxidation) give performance reserves (43%, 22%, 48%, 70%) vs API CK-4/FA-4 limits; candidate-oil test results, no formulation given, not recorded.
- (tier1) No co-components (VM/PPD/booster) and no published formulation are printed.
- (tier2) KV40, sulfated ash, all elements and pour point are not printed in DL2-15364.pdf.
- (tier2) Density: old Product_JSON gives 957.2 kg/m3 (converted); sheet prints 0.9572 g/ml at 15°C (p.2).

## 4. AFTON_HITEC_12210
- (tier1) Only a product bulletin is available for HiTEC 12210 (no SDS in the archive).
- (tier1) Required VM HiTEC® 5748A (OCP) is named (DL2-11418.pdf p.2) but its dose is not printed; dose left Missing.
- (tier1) Permitted base oils: the sheet only says 'in a range of market basestocks' and 'in appropriate grades and base stocks' (p.2); no API group named, field left Missing.
- (tier1) OEM claim is generic ('designed to meet ... including Caterpillar, Cummins, ...'), no specific OEM specification numbers; recorded as claim_type 'other'.
- (tier1) Radar chart 'Afton PC-11 vs. CJ-4 Performance Comparison' (p.2) has no numeric values; not recorded.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CK-4/FA-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Afton Chemical Corporation.
- (tier2) Density printed as 7.90 lbs/gal without a temperature (DL2-11418.pdf p.2); specific gravity 0.948 @ 15.6/15.6°C printed on the same page. Kept in printed unit; temperature for density left null.
- (tier2) KV40, sulfated ash, all elements and pour point are not printed in DL2-11418.pdf.

## 5. AFTON_HITEC_12210M
- (tier1) Product name differs: bulletins print 'HiTEC® 12210M' (DL2-11796.pdf, DL2-15568.pdf p.1-2); SDS prints 'HiTEC® 12210M Performance Additive' (DL2-15569.pdf p.1).
- (tier1) Supplier: bulletins name Afton Chemical Corporation; SDS DL2-15569.pdf p.1 lists Afton entities under 'Manufacturer / Supplier'.
- (tier1) Claims table changed between bulletins. 05/18 (DL2-11796.pdf p.2) columns not in 04/22: API CJ-4 (CK-4 15W-40 and 10W-30), Ford WSS-M2C214-B1 (FA-4 10W-30), ACEA E7-16, ACEA E9-16, MTU 2.1, Deutz DQC III-10LA. 04/22 (DL2-15568.pdf p.2) adds row API CK-4 10W-40 and columns ACEA E7-22, ACEA E11-22, MAN 3775, Deutz DQC III-18LA, Allison TES 439. For the columns present in both, the dots agree, so no conflict entries. Fields use the 04/22 table.
- (tier1) 05/18 text names only HiTEC® 5748A as the VM and only SAE 15W-40/10W-30 for CK-4; 04/22 adds HiTEC® 5748 and SAE 10W-40.
- (tier1) Required VM dose is not printed in either bulletin; left Missing.
- (tier1) Permitted base oils: only 'in a range of market basestocks' / 'in appropriate grades and base stocks' (DL2-15568.pdf p.2); left Missing.
- (tier1) Radar chart 'Afton CK-4 vs. CJ-4 Performance Comparison' (p.2) has no numeric values; not recorded.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CK-4/FA-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Afton Chemical Corporation.
- (tier2) Sulfated ash, all elements and pour point are not printed in any of the three documents.
- (tier2) SDS DL2-15569.pdf p.2-3 Section 3 component shares (not element contents): ZDDP (85940-28-9) ≥5 - ≤10 %, overbased calcium sulfurized phenate ≥3 - ≤5 %, base-oil distillates ≥15-≤25, ≥10-≤15, ≥5-≤10 %; p.22 (Korea) 'Mineral oil ≥35 - ≤45' and 'Molybdenum and its compounds ≥0.30 - ≤0.50' %. Mo/Zn/Ca left Missing.
- (tier2) KV40 is printed as 'Minimum' in the SDS (p.8); the old Product_JSON also records it as a minimum. Only source of KV40.

## 6. AFTON_HITEC_12360
- (tier1) Only a product bulletin is available for HiTEC 12360 (no SDS in the archive).
- (tier1) MAN 3677 and Scania LDF-4 are marked '*' = 'Approvals pending ...' (DL2-13692.pdf p.2); recorded as claim_type 'other', not 'approval'.
- (tier1) Required VM HiTEC® 5748 (25SSI OCP) named but dose not printed.
- (tier1) Bar charts p.2 (ISB cam lobe wear, Mack T13 IR peak height, CAT C13 oil consumption vs CK-4 limit, reserves 78%/45%/36%/37%/35%) are candidate-oil results without formulations; not recorded.
- (tier2) Text p.2: 'HiTEC® 12360 contains 1% ash content so it is compatible with after treatment devices'. It is not clear whether this is the package or the finished oil sulfated ash; sulfated_ash left Missing.
- (tier2) KV40, all elements and pour point are not printed in DL2-13692.pdf.

## 7. AFTON_HITEC_12400
- (tier1) User decision 2026-10-17: 13 claims marked with a filled dot (DL2-15365.pdf p.2) are recorded as Reported with claim_type left unspecified (null), because the legend does not define the filled dot; flagged for review. Claims with only '○ Pending completion of Field Trial' or '◉ Approval pending' marks keep claim_type 'other'.
- (tier1) Only a product bulletin is available for HiTEC 12400 (no SDS in the archive).
- (tier1) DL2-15365.pdf p.2: the table has 22 symbol columns but only 21 header labels; row 'ACEA E4 SAE 10W-40 + HiTEC® 611' has an '◉ Approval pending' mark in column 22, which has no header. Recorded as '(column 22, no header printed)'.
- (tier1) Table headers are vector graphics (not text); column assignment was read from a 400 dpi image and the symbol positions from the text layer (Wingdings glyphs).
- (tier1) HiTEC® 611 booster dose and the OCP VM identity/dose are not printed.
- (tier1) Bar charts p.2 (Caterpillar C13, Cummins ISM, Volvo T-13, OM501LA, OM646LA, Mack T-12 vs industry limit; OM501LA fuel economy '19 % better') have no formulation; not recorded.
- (tier2) KV40, sulfated ash, all elements and pour point are not printed in DL2-15365.pdf.
- (tier2) The typical characteristics (0.951 g/ml, 150 °C, 133 mm2/s, TBN 61) are identical to HiTEC 12360 (DL2-13692.pdf); copied as printed.

## 8. AFTON_HITEC_8712
- (tier1) Supplier: DL2-15020.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier'; first listed (Afton Chemical Asia Pte. Ltd.) recorded.
- (tier1) Only an SDS is in the archive for HiTEC 8712. Package type, claims, grades, treat rates, base oils, co-components and formulations are not printed; could be looked up later in an Afton bulletin.
- (tier1) Product name printed as 'HiTEC® 8712 Performance Additive' (p.1); old Product_JSON uses 'HiTEC 8712'.
- (tier1) The SDS does not say this is a package; composition (p.2) shows mineral oil 30 - 60 %, calcium long-chain alkylphenate sulfide 10 - 19.9 % and ZDDP 10 - 19.9 %. Old Product_JSON classifies it as 'performance additive package'; please confirm package vs component.
- (tier2) Density 1.033 g/cm³ printed without temperature; relative density 1.036 also printed (DL2-15020.pdf p.6). Temperature left null.
- (tier2) TBN, sulfated ash, elements and pour point not printed. Section 3 (p.2) component shares: calcium alkylphenate sulfide 10 - 19.9 %, ZDDP 10 - 19.9 %, mineral oil 30 - 60 % (also p.10 ISHL 'Mineral Oil 30 - 60'); not element contents.

## 9. HiTEC_8766B
- (tier1) DL2-10367.pdf is shared with HiTEC 8767B (component #78). Per decision, only the HiTEC 8766B column of 'Typical Characteristics' is used here; the 8767B dose in the dosage table is recorded as a co-component of the 8766B SAE 10W-40 route.
- (tier1) Claims recorded as claim_type 'approval' from the table header 'Approvals' (DL2-10367.pdf p.2).
- (tier1) TBN booster required for some claims ('1 Requires TBN Boost') but product and dose are not printed.
- (tier1) Fleet bubble chart (p.2, 'Euro III and Euro IV Engines Dominate the Market') is market data; not recorded.
- (tier2) KV40, sulfated ash, elements and pour point are not printed in DL2-10367.pdf. No SDS in the archive for HiTEC 8766B.

## 10. AFTON_HITEC_8788B
- (tier1) Supplier: DL2-15016.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier'; first listed (Afton Chemical Asia Pte. Ltd.) recorded.
- (tier1) Only an SDS is in the archive for HiTEC 8788B; claims, SAE grades, treat rates, base oils, co-components and formulations are not printed (could be looked up later in an Afton product bulletin).
- (tier2) TBN, sulfated ash, all elements and pour point are not printed in DL2-15016.pdf.
- (tier2) DL2-15016.pdf p.2-3 Section 3 component shares (not element contents): overbased calcium sulfurized phenate 5 - 10 %, alkyl esters of alkyl phenate alkanoic acid 3 - 5 %, two ZDDPs 1 - 3 % each, base-oil distillates 15 - 25 % (x2) and 1 - 3 % (x2). p.21 (Japan PRTR) 'Boron compounds 5 - 10' % (component share, B left Missing).
- (tier2) Density: old Product_JSON gives 958 kg/m3 (converted); sheet prints 0.958 g/cm³ at 15°C (p.7).

## 11. AFTON_HITEC_8799B
- (tier1) Supplier: DL2-15017.pdf p.1 lists several Afton entities under 'Manufacturer / Supplier'; first listed (Afton Chemical Asia Pte. Ltd.) recorded.
- (tier1) Only an SDS is in the archive for HiTEC 8799B; claims, SAE grades, treat rates, base oils, co-components and formulations are not printed (could be looked up later in an Afton product bulletin).
- (tier2) TBN, sulfated ash, all elements and pour point are not printed in DL2-15017.pdf.
- (tier2) DL2-15017.pdf p.2-3 Section 3 component shares (not element contents): two ZDDPs 3 - 5 % and 1 - 3 %, overbased calcium sulfurized phenate 3 - 5 %, calcium long-chain alkaryl sulfonate 1 - 3 %, base-oil distillates 25 - 35 % and 15 - 25 %. p.20 (Japan PRTR) 'Boron compounds 5 - 10' % (component share, B left Missing).
- (tier2) Density: old Product_JSON gives 956 kg/m3 (converted); sheet prints 0.956 g/cm³ at 15°C (p.7), relative density 0.958.

## 12. BETTCHEM_BT_3088
- (tier1) User decision 2026-10-17: the 4 entries from the 'Technical Judgement for BT 3088' (DL2-15620.pdf, document_type 'other') are recorded as Reported with evidence_class 'Predicted' and the note that the value is a prediction, not a measurement.
- (tier1) Claim type: the TDS (DL2-15551.pdf p.1) gives a 'RECOMMENDED DOSAGE' per specification and says the package 'covers API CI-4 /CH-4 performance levels'; recorded as 'recommended'.
- (tier1) No SAE grades, base oils, co-components or published formulation are printed in either document.
- (tier1) API SL at 8% appears only in the Technical Judgement (p.4); the TDS lists API CH-4/SJ at 7.0 and CF-4/SG at 6.0.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Bettchem.
- (tier2) User decision 2026-10-17: element rows Ca, Zn, P, B, N, S and Sulphated Ash (DL2-15551.pdf p.1) print no unit; numbers stored as Reported with unit 'not printed'. Flagged: unit to be confirmed (likely mass %).
- (tier2) Density field holds the printed SPECIFIC GRAVITY at 15.6℃ (0.9881, ASTM D1298); no density in kg/m3 is printed.
- (tier2) Mg and Mo not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.9881 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY at 15.6℃ Report 0.9881 ASTM D1298', DL2-15551.pdf p.1), not a density in kg/m3; flagged for review.

## 13. BETTCHEM_BT_3089
- (tier1) Claim type 'recommended' from the 'RECOMMENDED DOSAGE' table (DL2-15552.pdf p.1); product is 'CUSTOMER SPECIFIC'.
- (tier1) No SAE grades, base oils, co-components or published formulation printed in DL2-15552.pdf; no SDS in the archive.
- (tier1) Mg, B and Mo are not printed in DL2-15552.pdf. Base number has a 'Minimum' (198) and a 'TYPICAL' (233) but no 'Maximum'.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Bettchem.
- (tier2) Density field holds the printed SPECIFIC GRAVITY at 15.6℃ (ASTM D1298); no density in kg/m3 printed (DL2-15552.pdf p.1).
- (tier2) User decision 2026-10-17: density field stores the number 1.09 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY at 15.6℃ Report 1.09 ASTM D1298', DL2-15552.pdf p.1), not a density in kg/m3; flagged for review.

## 14. BETTCHEM_BT_3093
- (tier1) Claim type 'recommended' from the 'RECOMMENDED DOSAGE' table (DL2-15550.pdf p.1); product is 'CUSTOMER SPECIFIC'.
- (tier1) No SAE grades, base oils, co-components or published formulation printed in DL2-15550.pdf; no SDS in the archive.
- (tier1) B and pour point are not printed in DL2-15550.pdf. Base number has 'Minimum' 100 and 'TYPICAL' 115, no 'Maximum'.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Bettchem.
- (tier2) Density field holds the printed SPECIFIC GRAVITY at 15.6℃ (ASTM D1298); no density in kg/m3 printed (DL2-15550.pdf p.1).
- (tier2) User decision 2026-10-17: density field stores the number 0.99 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY at 15.6℃ 0.9 1.1 0.99 ASTM D1298', DL2-15550.pdf p.1), not a density in kg/m3; flagged for review.

## 15. BRB_PETROLAD_8099
- (tier1) Claim types: API rows set to 'meets' (text p.1 'meet market standard API requirements'), 'MB 228.3 blanket approval' to 'approval', all other rows of the 'Performances' table to 'other' because the table has no wording beyond 'Performances'. Please confirm.
- (tier1) Viscotech 6540 VI improver is optional ('can be used in formulations combined with'); not entered as a required co-component. No SAE grades printed.
- (tier1) Only a TDS is in the archive; text says 'An MSDS is available upon request' (p.3).
- (tier2) Ca, P, N, Zn printed without a test method (DL2-11053.pdf p.3). KV40, sulfated ash, Mg, B, Mo, S and pour point are not printed.
- (tier2) Density: old Product_JSON gives 990 kg/m3 (converted); sheet prints 0.99 kg / L at 15.6 °C.

## 16. CHEVRON_N204
- (tier1) Image-only PDF (no text layer); all values read visually from 200 dpi page renders.
- (tier1) NEW product (no old Product_JSON file). Decision (a) said 'all properties missing and image-only noted', the later instruction says to read image-only PDFs like text PDFs; values were read and entered as Reported.
- (tier1) DL2-12494.pdf p.1: 'Company Identification: Indian Additives Ltd.' with Chevron Oronite logo and Oronite emergency contacts; supplier recorded as Indian Additives Ltd. (Revision Number: 0, MSDS : 46286).
- (tier1) DL2-12494.pdf p.1 Section 2 component shares (not element contents): Highly refined mineral oil (C15 - C50) 40 - 45 %weight; Zinc alkyl dithiophosphate (68649-42-3) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-69-7) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-68-6) 1 - 5 %weight.
- (tier1) Package vs component: MSDS only says 'Product Use: Automotive lubricant additive' (p.1); filed as a package per decision (a).
- (tier1) Only an MSDS is available; package type, claims, SAE grades, base oils and co-components are not printed.
- (tier2) TBN, sulfated ash, KV100, pour point and all elements are not printed. Section 5 lists combustion oxides of Calcium, Zinc, Molybdenum, Boron, Phosphorus, Nitrogen, Sulfur (qualitative only).
- (tier2) DL2-12494.pdf p.5 also prints 'Specific Gravity: 0.9850 @ 15.6°C (60°F)'; same value as density.

## 17. CHEVRON_N216
- (tier1) Image-only PDF (no text layer); all values read visually from 200 dpi page renders.
- (tier1) NEW product (no old Product_JSON file). Decision (a) said 'all properties missing and image-only noted', the later instruction says to read image-only PDFs like text PDFs; values were read and entered as Reported.
- (tier1) DL2-12493.pdf p.1: 'Company Identification: Indian Additives Ltd.' with Chevron Oronite logo and Oronite emergency contacts; supplier recorded as Indian Additives Ltd. (Revision Number: 3, MSDS : 44378).
- (tier1) DL2-12493.pdf p.1 Section 2 component shares (not element contents): Highly refined mineral oil (C15 - C50) 40 - 45 %weight; Zinc alkyl dithiophosphate (68649-42-3) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-69-7) 5 - 10 %weight; Calcium long chain alkaryl sulfonate (722503-68-6) 1 - 5 %weight.
- (tier1) Package vs component: MSDS only says 'Product Use: Automotive lubricant additive' (p.1); filed as a package per decision (a).
- (tier1) Only an MSDS is available; package type, claims, SAE grades, base oils and co-components are not printed.
- (tier2) TBN, sulfated ash, KV100, pour point and all elements are not printed. Section 5 lists combustion oxides of Calcium, Sulfur, Phosphorus, Nitrogen, Zinc, Boron (qualitative only).
- (tier2) DL2-12493.pdf p.4 also prints 'Coefficient of Therm. Expansion / °F: 0.000360' (no template field).
- (tier2) DL2-12493.pdf p.6 'REVISION STATEMENT: SECTION 09 - Physical/Chemical Properties information was deleted.'; the remaining Section 9 values on p.4 were recorded as printed.

## 18. CHEVRON_OLOA_59215
- (tier1) MB 228.3 and CES 20076/77 are printed as '(Approval in progress)' (DL2-13875.pdf p.1); recorded as claim_type 'other'.
- (tier1) PARATONE 24 SSI / 35 SSI VII doses are not printed.
- (tier1) No SDS in the archive for OLOA 59215.
- (tier2) Mg, flash point and pour point are not printed in DL2-13875.pdf (p.1 refers to the MSDS for handling).
- (tier2) Density: old Product_JSON gives 986.7 kg/m3 (converted); sheet prints 0.9867 g/cm³ (kg/l) at 15°C.

## 19. CHEVRON_OLOA_59230
- (tier1) Claim wording 'is developed to meet API CF-4 performance' (DL2-13876.pdf p.1) recorded as claim_type 'other'; please confirm whether this should count as 'meets'.
- (tier1) Composition text p.1: 'contains ashless dispersant, zinc dithiophosphate, metallic detergents and anti-oxidant' (no shares).
- (tier1) No SAE grades, base oils, co-components or formulation printed; no SDS in the archive.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Chevron Oronite Company LLC.
- (tier2) Mg, B, Mo, S, flash point and pour point are not printed in DL2-13876.pdf.

## 20. CHEVRON_OLOA_59766
- (tier1) Only an SDS is in the archive for OLOA 59766 (Revision Number 14, SDS 23738); package type, claims, grades, base oils and co-components not printed. Supplier per Section 1.3: Chevron Oronite S.A.S.
- (tier2) TBN, sulfated ash, KV100, pour point and all elements not printed.
- (tier2) DL2-11731.pdf p.2-3 Section 3 component shares (not element contents): mineral oil 40 - 45 %weight; PIB succinimide-type amine reaction product (147880-09-9) 25 - 30 %weight; ZDDP (68784-31-6) 5 - 10 %weight; calcium alkylbenzene sulfonates 5 - 10, 5 - 10 and 1 - 5 %weight (722503-69-7 is listed twice).

## 21. CHEVRON_OLOA_61003
- (tier1) Claims are listed under 'performance claims can be made' (DL2-11032.pdf p.1); recorded as claim_type 'other'. Items with '*' are 'Approvals on going'.
- (tier1) VII PARATONE® 8006 named, dose not printed. No SAE grades or base oils printed. No SDS in the archive.
- (tier2) Calcium is printed as 'Calcium, as Sulfonate' (ASTM D 3712), which may not be total calcium.
- (tier2) Density field holds 'Specific Gravity, at 15°C' 0,968. Mg, B, Mo, S, flash point and pour point not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.968 (specific gravity (dimensionless)), which is reported as specific gravity ('Specific Gravity, at 15°C (ASTM D 4052) 0,968', DL2-11032.pdf p.1), not a density in kg/m3; flagged for review.

## 22. ENI_MX_5212
- (tier1) Claim type 'recommended' from the text 'is recommended for blending ...' and the 'TREAT RATE & PERFORMANCE CLAIMS' table (DL2-14981.pdf p.1).
- (tier1) Treat rates are printed as '%' with no mass/volume basis. No SDS in the archive.
- (tier2) DL2-14981.pdf p.2 gives only min/max specification limits (value left null, min/max filled); density is a single value in a merged cell.
- (tier2) KV40, sulfated ash, B, Mo, S and pour point are not printed. Flash point method ASTM D 93 (PMCC).
- (tier2) Old Product_JSON left KV100/TBN/elements as observations without values; the sheet prints them as min/max limits.

## 23. ENI_MX_5217
- (tier1) Claim types: 'ACEA E4/E7-12' set to 'meets' (text 'meets ACEA E4/E7 levels'); other cells, many printed as '... level', set to 'other'. MB 228.5 is '(*) Official approval pending in group II/III formulation'.
- (tier1) No SDS in the archive.
- (tier2) DL2-12630.pdf p.2 gives only min/max specification limits (value left null, min/max filled); density is a single value in a merged cell.
- (tier2) KV40, sulfated ash, B, Mo, S and pour point are not printed. Flash point method ASTM D 93 (PMCC).

## 24. INFINEUM_D3320
- (tier1) Claim type 'other': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) No VM/co-components or SDS in the archive for D3320.
- (tier2) Typical Inspections (DL2-12025.pdf p.1) also print 'Mineral Oil 48 %(m) Calculated' (carrier share; no package field).
- (tier2) Ca, Mg, Zn, P, B, Mo, N and pour point are not printed.

## 25. INFINEUM_D3354
- (tier1) Claim type 'other': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) Row 2 level is printed as 'As below plus Volvo VDS-2' (DL2-10203.pdf p.1); the reference ('below' vs the row above) is unclear.
- (tier1) Booster rows: footnotes 3 and 4 give three alternative boosters 'tuned for different base stock qualities'; all recorded as co-components. SV261 VM dose not printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) Typical Inspections p.1 also print 'Mineral Oil Content 49 mass % Calculated' (carrier share; no package field).
- (tier2) B, Mo, S and pour point are not printed.

## 26. INFINEUM_D3375
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) NEW product (no old Product_JSON file); image-only TDS read visually (DL2-10217.pdf p.1, 'Version: 10 March 2015 (4.0)').
- (tier1) Claim type 'meets' from the description wording 'oil meeting the performance requirements listed below'. MB entry printed as 'MB-Approval 228.5'.
- (tier1) Infineum SV261 VM dose not printed. No SDS in the archive.
- (tier2) NEW product, image-only TDS read visually. Typical Inspections also print 'Mineral Oil 51 %(m) Calculated' and handling viscosities 'Vis @ Min Load/Unload Temp: 1,470 cSt', 'Vis @ Max Load/Unload Temp: 835 cSt'.
- (tier2) Density, sulfated ash, B, Mo, S and pour point are not printed.

## 27. INFINEUM_D3384
- (tier1) Claim type 'other': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) DL2-10218.pdf (TDS, Version 10 May 2015 (5.0)) is image-only; read visually. Not listed in the old Product_JSON; added per decision (b).
- (tier1) TDS p.2 prints 'Min Load/Unload Temp: 80 °C' above 'Max Load/Unload Temp: 65 °C' (min > max); copied as printed. SDS p.7 gives loading/unloading 55 °C - 65 °C.
- (tier1) Product use (SDS DL2-15274.pdf p.1): 'Additive for heavy duty diesel engine lubricating oil'. VM not named.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) SDS DL2-15274.pdf p.3 component share (not element content): zinc dialkyldithiophosphate (298-577-9) >=10 - <12,5 %; four base-oil distillates >=1 - <10 % each.
- (tier2) Sulfated ash, B, Mo, S and pour point not printed in the TDS; SDS p.13 'Pour point : not determined'.
- (tier2) SDS also prints relative density 0,974 at 15,6 °C.

## 28. INFINEUM_D3396
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) API SL is described as 'can also be used in gasoline engines requiring API SL category products'; recorded with the table claim type 'meets'.
- (tier1) No SDS in the archive.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) Also printed: 'Density @ 60 F, lb/gal 8.08 lb/USG'. B, Mo, S and pour point not printed (DL2-13383.pdf).

## 29. INFINEUM_D3398
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) No SDS in the archive.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) Also printed: 'Density @ 60 F, lb/gal 8.15 lb/USG'. B, Mo, S and pour point not printed (DL2-13348.pdf).

## 30. INFINEUM_D3416
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) Grades printed as 'MULTI' / 'MONO' (multigrade / monograde) for the lower API levels (DL2-15333.pdf p.1); recorded as printed.
- (tier1) Claim type 'meets' applied to all rows from the CI-4 description; the lower API levels have no separate wording.
- (tier1) No SDS in the archive.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) Sulfated Ash method printed as 'Calculated' (supplier). B, Mo, S and pour point not printed.
- (tier2) Row label 'Flash Point Deg C' is visible on the page image but missing from the text layer. (DL2-15333.pdf p.1).

## 31. INFINEUM_D3417
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) DL2-15334.pdf is a customer specification ('CUSTOMER SPECIFICATION', customer 'Global - BRENNTAG GROUP', 'Printed On : 12-Feb-2024'), document_type PDS per decision (c).
- (tier1) No SDS in the archive.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) Element fields use the newer customer specification DL2-15334.pdf (Min/Target/Max); targets equal the TDS typical values (Ca 1.26, Mg 1.19, N 0.79, P 1.37, Zn 1.51), so no conflict.
- (tier2) PDS lists Base Number and KV100 as 'Test and report results' (no limits). Sulfated ash, B, Mo, S and pour point not printed.
- (tier2) Row label 'Flash Point Deg C' is visible on the page image but missing from the text layer. (DL2-15335.pdf p.1).

## 32. INFINEUM_D3424
- (tier1) Claim type 'other': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) DL2-10204.pdf holds two documents: p.1 Infineum TDS (Version 9th November 2004 (3.1)) and p.2-8 a Safety Data Sheet issued by Multisol Limited (Revision Date 02Dec2008, Revision 4). Both listed in document_type/source_file.
- (tier1) Claim type 'other' ('developed to meet ...'); several rows say 'Quality' (e.g. 'MTU Type II Quality', 'VW501/5 Quality'). No VM or co-components printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- **Conflict (tier2)** `tier2.flash_point`: DL2-10204.pdf p.1 (2004-11-09): Flash Point (PM) 190 °C ASTM D 93; DL2-10204.pdf p.6 (2008-12-02): Flash Point [Method]: >110C (230F) [ ASTM D-93] — TDS typical (2004, p.1) vs SDS lower bound (2008, p.6; also p.3 Section 5). Values are compatible (190 > 110) but printed differently; per rule the field holds the more recent SDS value. Not resolved.
- (tier2) Flash point: TDS 190 °C (PM) vs SDS '>110C'; recorded as a conflict, field holds the more recent SDS value.
- (tier2) TDS also prints 'Mineral Oil Content 49 mass % Calculated'. SDS p.2 Section 3 component shares: calcium long chain alkyl phenate sulphide 1.0 - 4.9%, tetrapropenylphenol 1.0 - 4.9%, zinc alkyl dithiophosphate 5.0 - 9.9% (not element contents).
- (tier2) B, Mo, S and pour point not printed.

## 33. INFINEUM_D3451
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) Fields use the newer TDS DL2-12029.pdf (2017). The 2012 TDS DL2-10219.pdf p.1 lists 'API SL/CI-4/CH-4' and 'ACEA E7-08' for SAE 15W-40 at 11.9 mass % ('~ 11.0 Volume %'); the 2017 sheet updates ACEA E7-08 to E7-12 and adds rows. Revision, not recorded as conflict.
- (tier1) 'can be downtreated to meet API CG-4 and CF-4' has no treat rate printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) SDS DL2-13720.pdf p.3 component shares: ZDDP >=10 - <12,5 %; molybdenum polysulphide long chain alkyl dithiocarbamate complex >=0,25 - <1 % (not element contents). SDS p.12 'Pour point : not determined'.
- (tier2) Sulfated ash only in the 2012 TDS (8.6 %(m)); B and pour point not printed.

## 34. INFINEUM_D3453
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) NEW product (no old Product_JSON file); image-only TDS (Version: 9 December 2014 (3.0)) read visually.
- (tier1) No SDS in the archive.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) NEW product, image-only TDS read visually. Also printed: 'Density @ 60 F, lb/gal 8.06 lb/USG', 'Vis @ Min Load/Unload Temp: 1,270 cSt', 'Vis @ Max Load/Unload Temp: 725 cSt'.
- (tier2) B and pour point not printed.

## 35. INFINEUM_D3463
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) No SDS in the archive.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4 Plus), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) Also printed: 'Density @ 60 F, lb/gal 8.02 lb/USG'. B, Mo, S and pour point not printed.
- (tier2) Row label 'Flash Point Deg C' is visible on the page image but missing from the text layer.

## 36. INFINEUM_D3503
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) 'applicable OEM performance specifications' are mentioned without names (DL2-11404.pdf p.1). No SDS in the archive.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CK-4/FA-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) Calcium is not printed in DL2-11404.pdf (checked on the page image); B and pour point not printed. Also printed: 'Density @ 60 F, lb/gal 8.00 lb/USG'.
- (tier2) Row label 'Flash Point Deg C' is visible on the page image but missing from the text layer.

## 37. INFINEUM_D3511
- (tier1) Claim type 'meets': Infineum performance tables list 'Performance Level' per grade and mass % without approval/meets wording beyond the description.
- (tier1) API FA-4 appears in the Performance table (13.2, 10W-30) but the description names only API CK-4; recorded with claim type 'meets' from the table context. No VM named. No SDS in the archive.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CK-4/FA-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Infineum.
- (tier2) Flash point, KV40, KV100, Mo, B, S and pour point are not printed in DL2-15389.pdf (checked on the page image). Sulfated Ash method 'Calculated'. Also printed: 'Density @ 60 F, lb/gal 7.99 lb/USG'.

## 38. JINZHOU_DONGGONG_T3160
- (tier1) No revision date printed on DL2-11882.pdf.
- (tier1) Base Oil Type column read from the page image (Roman numerals are not in the text layer).
- (tier1) Claim types: CI-4/SL 'meets' (text 'Test data to meet ...'); other rows of the 'Dosage Reference' table 'other'. No VM/co-components, no SDS in the archive.
- (tier2) Density (20°C) and KV100 are printed as 'Report' with no value (DL2-11882.pdf p.1); left Missing.
- (tier2) Quality Index values are minimum limits ('≥'), not typical values. KV40, sulfated ash, Mg, P, B, Mo, S and pour point not printed.

## 39. JINZHOU_KANGTAI_KT31140
- (tier1) No revision date printed on DL2-12961.pdf. Supplier printed as 'KangTai . Lubricant Addtives' (WWW.JZKANGTAI.COM).
- (tier1) Claim type 'recommended' from 'DOSAGE RECOMMENDED'. No SAE grades, VM or SDS.
- (tier2) KV100 printed as 'Report' with no value (DL2-12961.pdf p.1).
- (tier2) Column header 'Typical Value' but each value printed with 'min'. Recorded as minimum specifications.
- (tier2) Density, KV40, sulfated ash, Mg, B, Mo, S and pour point not printed.

## 40. LUBRIZOL_16008
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) The 4.4 % by weight block lists 'API CF' and 'API SF' without an intro sentence; claim_type 'other'. Text: 'For full details of the specification cascade offered by LUBRIZOL® 16008 please refer to the Product Data Summary.' (not in archive).
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) TBN from text p.1: 'LUBRIZOL® 16008 has a TBN greater than 182.'
- (tier2) User decision 2026-10-17: density field stores the number 1.065 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 1.045 1.065 1.085', DL2-10871.pdf p.1), not a density in kg/m3; flagged for review.

## 41. LUBRIZOL_3589C
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Footnote 1 ('Product at 6.15 % by weight provides 11 TBN (ASTM D2896)') is finished-oil TBN, not package TBN; kept in route limits only.
- (tier1) Footnote 2: Kolomna approval at 6.2 % by weight plus a 0.8 % by weight booster (booster not named).
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF-2), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 1.069 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 1.049 1.069 1.089', DL2-10629.pdf p.1), not a density in kg/m3; flagged for review.

## 42. LUBRIZOL_3700
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.981 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.961 0.981 1.001', DL2-10632.pdf p.1), not a density in kg/m3; flagged for review.

## 43. LUBRIZOL_3700D
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) Zinc is on page 2, which is image-only (DL2-10633.pdf p.2); read visually: 1.11 / 1.23 / 1.35.
- (tier2) User decision 2026-10-17: density field stores the number 0.999 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.979 0.999 1.019', DL2-10633.pdf p.1), not a density in kg/m3; flagged for review.

## 44. LUBRIZOL_4986
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.973 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993', DL2-10653.pdf p.1), not a density in kg/m3; flagged for review.

## 45. LUBRIZOL_4986D
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.973 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993', DL2-10654.pdf p.1), not a density in kg/m3; flagged for review.

## 46. LUBRIZOL_4986E
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.973 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993', DL2-10655.pdf p.1), not a density in kg/m3; flagged for review.

## 47. LUBRIZOL_4986F
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.974 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.954 0.974 0.994', DL2-10656.pdf p.1), not a density in kg/m3; flagged for review.

## 48. LUBRIZOL_4986G
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.976 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.956 0.976 0.996', DL2-10657.pdf p.1), not a density in kg/m3; flagged for review.

## 49. LUBRIZOL_4987
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) DL2-10658.pdf and DL2-10659.pdf are byte-identical (same MD5); values cited from DL2-10658.pdf.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.973 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993', DL2-10658.pdf p.1), not a density in kg/m3; flagged for review.

## 50. LUBRIZOL_CV1100
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) Restriction printed in the claims list: 'API CK-4 / SN claim limited to SAE 15W-40 viscosity grade in select Group II base oils.' (route limits).
- (tier1) API FA-4 block requires 2.0 wt% LUBRIZOL® CV6320 top treat (component #79).
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.952 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.932 0.952 0.972', DL2-11503.pdf p.1), not a density in kg/m3; flagged for review.

## 51. LUBRIZOL_CV1103
- (tier1) DL2-14978.pdf is a Lubrizol 'Product Data Sheet' (PDS). The credentials table has two '14.30% by weight' columns with no other header; the second column (only API FA-4, Cummins CES 20087, DDC 93K223) appears to be the CV6320 top-treat FA-4 route described in the text, but the table does not say so.
- (tier1) Claim codes: A -> 'approval', M -> 'meets', L ('Licensable against an active API category') -> kept as 'other', with the code recorded in the scope note (user decision 2026-10-17). Column 1 also marks API FA-4 'L' without mentioning CV6320; recorded as printed.
- (tier1) Treat rate printed '14.30% by weight' in the table vs '14.3wt%' in the text (same value). No SDS in the archive.
- (tier1) User decision 2026-10-17: 7 claims with Lubrizol code 'L' keep their claim_type; the code and its legend text are recorded in the scope note.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CK-4/FA-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Density field holds SPECIFIC GRAVITY @ 15.6 C (0.953, ASTM D 4052); 'LBS PER GAL @ 15.6 C 7.94 lbs CALCULATED' also printed.
- (tier2) TBN, Mg, B and Mo not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.953 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.953 SPGRAV ASTM D 4052', DL2-14978.pdf p.2), not a density in kg/m3; flagged for review.

## 52. LUBRIZOL_CV2301
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Treat rate is printed per 'Recommended for use at' block (11.7, 10.7, 9.1, 8.2 % by weight); the 8.2 % block intro mentions a 'booster' that is not named.
- (tier1) SDS DL2-13713.pdf p.1 'Recommended use: Heavy Duty Diesel'.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with The Lubrizol Corporation.
- (tier2) Tables are on TDS page 2 (DL2-13065.pdf p.2). Density field holds SPECIFIC GRAVITY @ 15.6 C. Package TBN, Mg, B, Mo, S not printed.
- (tier2) SDS DL2-13713.pdf p.2 component shares (not element contents): Mineral oil 40 – 50%; Zinc alkyl dithiophosphate 5 – 10%; Calcium sulfonate 1 – 5%; Alkylated phenol 0.1 – 0.5%.
- (tier2) SDS p.5 Section 9 values agree with the TDS (no conflicts); SDS also prints viscosities at 25 °C (5753 mm2/s), 20 °C (8574 mm2/s) and 50 mPa.s at 122.4 °C.
- (tier2) User decision 2026-10-17: density field stores the number 0.982 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.962 0.982 1.002', DL2-13065.pdf p.2), not a density in kg/m3; flagged for review.

## 53. LUBRIZOL_CV2601
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER GAL also printed.
- (tier2) Physical values (p.1) in the 'Target' column; chemical values (p.2) in the 'Typical' column.
- (tier2) TBN, Mo and S are not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.955 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.935 0.955 0.975', DL2-11702.pdf p.1), not a density in kg/m3; flagged for review.

## 54. LUBRIZOL_CV3515
- (tier1) Claim type from the intro line of each 'Recommended for use at' block (e.g. 'the lubricant meets the following performance specifications').
- (tier1) Only a TDS is in the archive for this product (no SDS).
- (tier1) Treat rate is printed per 'Recommended for use at' block; SAE grade taken from the block intro where printed.
- (tier1) 'Cummins CES 20078' is printed twice in the claims list (DL2-15722.pdf p.1); recorded twice as printed.
- (tier2) Density field holds 'SPECIFIC GRAVITY @ 15.6 C' (dimensionless); LBS PER U.S./IMP GAL @ 15.6 C also printed.
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) User decision 2026-10-17: density field stores the number 0.972 (specific gravity (dimensionless)), which is reported as specific gravity ('SPECIFIC GRAVITY @ 15.6 C 0.952 0.972 0.992', DL2-15722.pdf p.1), not a density in kg/m3; flagged for review.

## 55. LUBRIZOL_CV7540
- **Conflict (tier1)** `tier1.performance_claims (Cummins CES 20076 claim code)`: DL2-14638.pdf p.1 (2020-01-20): Cummins CES 20076 L; DL2-15581.pdf p.1 (2022-05-13): Cummins CES 20076 A — 2020 sheet: 'L - Licensable'; 2022 sheet: 'A - Approved'. Fields use the newer 2022 sheet. Not resolved.
- **Conflict (tier1)** `tier1.performance_claims (Cummins CES 20077 claim code)`: DL2-14638.pdf p.1 (2020-01-20): Cummins CES 20077 L; DL2-15581.pdf p.1 (2022-05-13): Cummins CES 20077 A — 2020 sheet: 'L - Licensable'; 2022 sheet: 'A - Approved'. Fields use the newer 2022 sheet. Not resolved.
- **Conflict (tier1)** `tier1.performance_claims (Cummins CES 20078 claim code)`: DL2-14638.pdf p.1 (2020-01-20): Cummins CES 20078 L; DL2-15581.pdf p.1 (2022-05-13): Cummins CES 20078 A — 2020 sheet: 'L - Licensable'; 2022 sheet: 'A - Approved'. Fields use the newer 2022 sheet. Not resolved.
- (tier1) Two Product Data Sheets: DL2-14638.pdf (Published on 20 Jan, 2020) and DL2-15581.pdf (Published on 13 May, 2022). Fields use the 2022 sheet. 2022 adds ACEA E7-22 (2022) and CAT ECF-2; the 2020 sheet lists neither. Cummins CES 20076/77/78 changed from L to A (see conflicts).
- (tier1) SAE grades from the 2022 text: 'Viscosity grade coverage across SAE 20W-50 and 15W-40'. Claim codes: A -> approval, M -> meets, L -> other (code recorded in the scope note per user decision 2026-10-17). No SDS in the archive.
- (tier1) User decision 2026-10-17: 2 claims with Lubrizol code 'L' keep their claim_type; the code and its legend text are recorded in the scope note.
- (tier2) Typical characteristics identical in both sheets (DL2-14638.pdf p.2 and DL2-15581.pdf p.2). Density/specific gravity, TBN and Mo not printed.

## 56. MINGLAN_T3161
- (tier1) No revision date and no supplier legal name printed on T3161%20%20MULTIFUNCTIONAL%20ENGINE%20OIL%20ADDITIVE%20FOR%20CI.pdf; supplier recorded from the archive folder name 'MINGLAN CHEMICAL'.
- (tier1) Claim type 'other': 'The following performance levels can be achieved with oils formulated with T3161'. No SAE grades, base oils, co-components or SDS.
- (tier1) 'Reference dosage' column 'Dosage' has no unit printed (T3161A prints 'm%'); unit left null.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with MINGLAN CHEMICAL.
- (tier2) Kinematic Viscosity (100 °C) printed as 'report' (no value). Density, KV40, sulfated ash, S and pour point not printed.
- (tier2) Supplier-name note: 'MINGLAN CHEMICAL' is the archive folder name; the sheet prints no company name.

## 57. MINGLAN_T3161A
- (tier1) No revision date and no supplier legal name printed on T3161A%20%20MULTIFUNCTIONAL%20ENGINE%20OIL%20ADDITIVE%20FOR%20CI.pdf; supplier recorded from the archive folder name 'MINGLAN CHEMICAL'.
- (tier1) Claim type 'other': 'The following performance levels can be achieved with oils formulated with T3161A'. No SAE grades, base oils, co-components or SDS.
- (tier1) CF-4/SJ dose '6.0/6.2' and CD/SF dose '4.6/4.8' (dosage column 'Dosage (m%)'): two values separated by '/', meaning not stated; value left null with printed text kept.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with MINGLAN CHEMICAL.
- (tier2) Kinematic Viscosity (100 °C) printed as 'report' (no value). Density, KV40, sulfated ash, S and pour point not printed.
- (tier2) Supplier-name note: 'MINGLAN CHEMICAL' is the archive folder name; the sheet prints no company name.

## 58. MINGYUEKEJI_MY_P3168
- (tier1) No revision date printed on 'TDS of P3168.pdf'. Supplier from the archive folder 'MINGYUEKEJI' (sheet header prints only Chinese text '高品质润滑油添加剂生产商').
- (tier1) Grades printed only as 'Multi-grade' / 'Mono-grade'. Claims from the 'Dosage' table recorded as 'other'; API CF4 and CF also as 'meets' from the text 'exceeding ... engine testing requirements'.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF4), not from any supplier document; the field is now missing. Confirm permitted API groups with MINGYUEKEJI.
- (tier2) KV40, sulfated ash, Mg, B, Mo, S and pour point not printed. Nitrogen method printed as ASTM D4951.

## 59. RICHFUL_RF6066
- (tier1) The two TDS (DL2-13819.pdf 'TDS OF RF6066' and DL2-15451.pdf) carry no date, so the order of revisions cannot be determined. Density, KV100, TBN, Zn and Ca differ between documents (see conflicts) and are left null. DL2-13819.pdf matches the 2020 SDS (density 990, TBN 106); DL2-15451.pdf matches the 2021 SDS (density 0.988, 185 mm²/s), which suggests DL2-15451.pdf is the later TDS, but no date is printed.
- (tier1) Supplier spelled 'Xinxiang Richuful Lube Additive Co. Ltd.' in SDS DL2-13820.pdf p.1 and 'Xinxiang Richful Lube Additive Co., Ltd.' in SDS DL2-15831.pdf p.1.
- (tier1) DL2-15831.pdf (SDS 2021): body text is image/vector graphics; read visually from page renders.
- (tier1) Old Product_JSON mixed values from DL2-15451.pdf and DL2-13819.pdf without flagging the differences.
- (tier1) Claim type 'recommended' from the 'Recommended Treat Rate' tables. Storage/blending limits differ between the two TDS (45/65 ℃ vs 50/60 ℃).
- **Conflict (tier2)** `tier2.density`: DL2-13819.pdf p.1 (undated): Density( 20℃), kg/m3 990 GB/T13377，ASTMD4052; DL2-15451.pdf p.1 (undated): Density (20℃), kg/m3 968-1008 988 SH/T 0604, ASTM D4052; DL2-13820.pdf p.5 (2020-07-06): Density 990 kg/m3; DL2-15831.pdf p.5 (2021-09-02): Density : 0.988 g/cm³ (20 °C) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** `tier2.kv100`: DL2-13819.pdf p.1 (undated): Kinematic Viscosity, ( 100℃), mm2/s 227 GB/T265，ASTMD445; DL2-15451.pdf p.1 (undated): Kinematic Viscosity (100℃), mm2/s Report 185 GB/T 265, ASTM D445; DL2-13820.pdf p.5 (2020-07-06): Kinematic viscosity 200 mm2/s (100 °C); DL2-15831.pdf p.5 (2021-09-02): Viscosity, dynamic : 185 mm²/s (100 °C) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** `tier2.tbn`: DL2-13819.pdf p.1 (undated): Total Base Number, mgKOH/g 106 SH/T0251，ASTMD2896; DL2-15451.pdf p.1 (undated): Total Base Number, mgKOH/g 97-119 108 SH/T 0251, ASTM D2896; DL2-13820.pdf p.5 (2020-07-06): Total base number 106 mgKOH/g — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** `tier2.elements.Zn`: DL2-13819.pdf p.1 (undated): Zn Content, %（m/m） 1.3 GB/T17476，ASTM D4951; DL2-15451.pdf p.1 (undated): Zn Content, m% 1.13-1.38 1.24 GB/T 17476, ASTM D4951 — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** `tier2.elements.Ca`: DL2-13819.pdf p.1 (undated): Ca Content,%（m/m） 3.0 GB/T17476，ASTM D4951; DL2-15451.pdf p.1 (undated): Ca Content, m% 2.82-3.44 3.15 GB/T 17476, ASTM D4951 — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) Component shares (not element contents): SDS DL2-15831.pdf p.2: base-oil distillates 10 - 39.9 %; ZDDP (68649-42-3) 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 9.9 %; molybdenum dithiocarbamate 0.1 – 1.99 %. SDS DL2-13820.pdf p.2 lists ingredients without percentages.
- (tier2) Sulfated ash, KV40, Mg, B, S and pour point not printed.

## 60. RICHFUL_RF6069
- (tier1) TDS DL2-15618.pdf has no date; SDS DL2-15619.pdf: Issue/Revision date 1/4/2022, version 2.0 (body image/vector graphics, read visually).
- (tier1) KV100 differs: TDS 118 mm2/s vs SDS 142 mm²/s; TDS undated, so the field is left null (see conflicts).
- (tier1) RF0206 (1.9% in the CF-4 route) is not described on the sheet.
- **Conflict (tier2)** `tier2.kv100`: DL2-15618.pdf p.1 (undated): Kinematic Viscosity (100℃), mm2/s Report 118 GB/T 265, ASTM D445; DL2-15619.pdf p.5 (2022-01-04): Viscosity, kinematic : 142 mm²/s (100 °C, ASTM D445) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS DL2-15619.pdf p.2 component shares (not element contents): base-oil distillates 10 - 59.9 %; ZDDP (68649-42-3) 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 4.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S and pour point not printed.

## 61. RICHFUL_RF6071L
- (tier1) Only an undated TDS is in the archive for RF6071L (no SDS). The sheet prints no company name; supplier left null (archive folder: Richful Lube Additive).
- (tier2) Column headers 'Requirement Limit' / 'Typical Value'. Sulfated ash, KV40, Mg, B, S and pour point not printed.

## 62. RICHFUL_RF6077
- (tier1) TDS DL2-15536.pdf has no date; SDS DL2-15542.pdf Issue/Revision date 11/16/2023.
- (tier1) KV100 (TDS 160 vs SDS 150 mm2/s) and density (TDS 998 kg/m3 at 20 ℃ vs SDS 0.991 g/cm3 at 15 °C) differ; TDS undated, fields left null (see conflicts). The density temperatures also differ.
- (tier1) Claim type 'meets' from 'is compliant to API CI-4 specification'. OCP VII required but not named and no dose.
- **Conflict (tier2)** `tier2.density`: DL2-15536.pdf p.1 (undated): Density (20℃), kg/m3 978-1018 998 GB/T 13377, ASTM D4052; DL2-15542.pdf p.5 (2023-11-16): Density : 0.991 g/cm3 (15 °C) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** `tier2.kv100`: DL2-15536.pdf p.1 (undated): Kinematic Viscosity (100℃), mm2/s Report 160 GB/T 265, ASTM D445; DL2-15542.pdf p.5 (2023-11-16): Viscosity, kinematic : 150mm2/s (100 °C) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS p.2 component shares (not element contents): base-oil distillates 10 - 59.9 %; ZDDP 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 2.9 %; molybdenum dithiocarbamate 0.1 – 0.99 %.
- (tier2) SDS also prints vapour pressure 28.7 mmHg at 65 °C and 15.9 mmHg at 45 °C (no template field). Sulfated ash, KV40, Mg, B, S, pour point not printed.

## 63. RICHFUL_RF6078
- **Conflict (tier1)** `tier1.treat_rate_matrix (ACEA E7/API CI-4)`: DL2-15832.pdf p.1 (undated): ACEA E7/API CI-4 10W-30, 10W-40, 15W-40, 20W-50 11.85%; RF6078%20-%20TDS.pdf p.1 (undated): ACEA E7/API CI-4 10W-30, 10W-40, 15W-40, 20W-50 10.85% — Both TDS undated; DL2-15832.pdf lists API CI-4 alone at 10.85%, 'RF6078 - TDS.pdf' lists API CI-4 Plus at 11.85%. Not resolved.
- (tier1) Both TDS (DL2-15832.pdf and 'RF6078 - TDS.pdf') are undated; SDS DL2-15833.pdf revision 9/2/2021 (issue date printed '9/022021'); SDS body is image/vector graphics, read visually.
- (tier1) Density: TDS 972 kg/m3 vs SDS 975 kg/m³ (both 20 ℃); TDS undated, field left null (see conflicts).
- (tier1) The two TDS give different rates for the 'ACEA E7/API CI-4' row; see conflicts.
- **Conflict (tier2)** `tier2.density`: DL2-15832.pdf p.1 (undated): Density (20℃), kg/m3 952-992 972 GB/T 13377, ASTM D4052; RF6078%20-%20TDS.pdf p.1 (undated): Density (20℃), kg/m3 952-992 972 SH/T 0604, ASTM D4052; DL2-15833.pdf p.5 (2021-09-02): Density : 975 kg/m³ (20 °C, ASTM D4052) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS p.2 component shares (not element contents): base-oil distillates 10 - 39.9 %; ZDDP 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 9.9 %; molybdenum dithiocarbamate 0.1 – 1.99 %.
- (tier2) Sulfated ash, KV40, Mg, B, N, S, pour point not printed.

## 64. RICHFUL_RF6079
- (tier1) TDS DL2-15535.pdf undated; bulletin 'RF6079 Diesel Engine Oil Additive Package.pdf' prints only 'Version 1'; SDS DL2-15541.pdf Issue/Revision 3/18/2022 (body image/vector graphics, read visually). All three agree on the shared values.
- (tier1) API CI-4 Plus (11.0%) appears only in the bulletin. OCP VII not named.
- (tier2) SDS p.2 component shares (not element contents): hydrotreated heavy paraffinic distillate 10 – 59.9 %; ZDDP 3 – 17.9 %; overbased calcium sulfurized phenate 1 – 14.9 %; bis(nonylphenyl)amine 0.5 – 9.9 %; hindered phenolic ester 0.5 – 9.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.
- (tier2) User decision 2026-10-17: density field stores the number 1.0 (g/cm³), which is reported as specific gravity (relative density) ('Relative density : 1.000 g/cm³@20℃', DL2-15541.pdf p.5), not a density in kg/m3; flagged for review.

## 65. RICHFUL_RF6080
- (tier1) TDS issue date 2025-05-09 (p.1-2); SDS issue date 2025-04-08.
- (tier1) Claim wording: 'meets all ... certification requirements' recorded as 'meets'. VII and PPD required but not named.
- (tier2) SDS p.2 component shares (not element contents): hydrotreated heavy paraffinic distillate 10 - 59.9 %; ZDDP 5 - 19.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; bis(nonylphenyl)amine 0.5 - 9.9 %; hindered phenolic ester 0.5 - 9.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.

## 66. RICHFUL_RF6081
- (tier1) TDS issue date 2025-05-13 (p.1-2); SDS issue date 2025-04-09.
- (tier1) Claim wording: 'meets all ... certification requirements' recorded as 'meets'. VII and PPD required but not named.
- **Conflict (tier2)** `tier2.kv100`: DL2-15836.pdf p.2 (2025-05-13): Kinematic Viscosity (100℃), mm2/s Report 132 ASTM D445; DL2-15837.pdf p.5 (2025-04-09): Viscosity, kinematic : 130 mm2/s (100 °C) — All documents dated; field holds the most recent (DL2-15836.pdf). Not resolved.
- (tier2) SDS p.2 component shares (not element contents): hydrotreated heavy paraffinic distillate 10 - 59.9 %; ZDDP 5 - 19.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; bis(nonylphenyl)amine 0.5 - 9.9 %; hindered phenolic ester 0.5 - 9.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.

## 67. RICHFUL_RF6088
- (tier1) TDS DL2-15452.pdf undated; SDS DL2-15838.pdf Issue/Revision 2/25/2024. Shared values agree.
- (tier1) Claim type 'meets' from 'is compliant to API CK-4&ACEA E11 specification'. OCP VII not named.
- (tier2) SDS p.2 component shares (not element contents): distillate 10 – 59.9 %; ZDDP 3 – 17.9 %; overbased calcium sulfurized phenate 1 – 14.9 %; bis(nonylphenyl)amine 1 – 14.9 %; hindered phenolic ester 1 – 14.9 %. SDS also prints vapour pressure at 40 °C 16.2mmHg.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.
- (tier2) User decision 2026-10-17: density field stores the number 0.955 (g/cm³), which is reported as specific gravity (relative density) ('Relative density : 0.955 g/cm3@20℃', DL2-15838.pdf p.5), not a density in kg/m3; flagged for review.

## 68. RICHFUL_RF6088F
- (tier1) TDS DL2-15839.pdf undated; SDS DL2-15840.pdf issue date 17/10/2024.
- (tier1) KV100 (TDS 177 vs SDS 178.2 mm2/s) and density (TDS 963 kg/m3 vs SDS 0.958 g/cm3, both 20 ℃) differ; TDS undated, fields left null (see conflicts).
- (tier1) Claim type 'meets' from 'Greatly meet API CK-4 specification'.
- **Conflict (tier2)** `tier2.density`: DL2-15839.pdf p.1 (undated): Density (20℃), kg/m3 943-983 963 SH/T 0604，ASTM D4052; DL2-15840.pdf p.5 (2024-10-17): Relative density : 0.958 g/cm3@20℃ — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** `tier2.kv100`: DL2-15839.pdf p.1 (undated): Kinematic Viscosity (100℃), mm2/s Report 177 GB/T 265，ASTM D445; DL2-15840.pdf p.5 (2024-10-17): Viscosity, kinematic : 178.2 mm2/s @100℃ — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS p.2 component shares (not element contents): distillate 10 – 59.9 %; ZDDP 3 – 17.9 %; overbased calcium sulfurized phenate 1 – 14.9 %; hindered phenolic ester 1 – 14.9 %; bis(nonylphenyl)amine 1 – 9.9 %.
- (tier2) KV40, Mg, B, Mo, S, pour point not printed.

## 69. RICHFUL_RF6089
- (tier1) Only an SDS (DL2-15841 (1).pdf, issue/revision 07/25/2025) is in the archive for RF6089; no TDS. Supplier from Section 1.3 'Manufacturer' (rendered as graphics, read from the page image).
- (tier1) Package type, claims, grades, treat rates, base oils and co-components are not printed; could be looked up later in a Richful TDS.
- (tier2) SDS p.2 component shares (not element contents): distillate 10 - 59.9 %; ZDDP 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; bis(nonylphenyl)amine 1 - 14.9 %; hindered phenolic ester 1 - 14.9 %.
- (tier2) TBN, sulfated ash, KV40, elements and pour point not printed.

## 70. RICHFUL_RF6400
- (tier1) Two undated TDS (DL2-15849.pdf, 'RF6400 TDS.pdf') with identical content; SDS 'RF6400 MSDS.pdf' (HCS-2012 format, 7/25/2022) and DL2-15850.pdf (REACH, rev. 6/7/2023). All shared values agree.
- (tier1) Document type: 'RF6400 MSDS.pdf' prints 'Safety Data Sheet' in the title; recorded as SDS.
- (tier1) Grades listed as '... 20W-50, 40, 50 and etc.' (open list).
- (tier2) SDS DL2-15850.pdf p.2 component shares (not element contents): distillate 10 - 59.9 %; PIB succinimide (84605-20-9) 8 - 44.9 %; unnamed component (CAS '-') 1 – 14.9 %; calcium sulfonate (70024-69-0) 1 - 24.9 %; ZDDP (4259-15-8) 3 - 17.9 %; alkylated diphenylamine 0.5 - 2.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.

## 71. RICHFUL_RF6406
- **Conflict (tier1)** `tier1.treat_rate_matrix (API CF/SF, Multi)`: DL2-15456.pdf p.1 (undated): CF/SF Multi 4.1%; DL2-14746.pdf p.1 (undated): CF/SF （Multi） 3.7 — Both TDS undated; not resolved.
- (tier1) Two undated TDS: DL2-14746.pdf ('TDS OF RF6406', prints minimum values only) and DL2-15456.pdf (index ranges + typicals); SDS RF6406.pdf issue 11/26/2021, revision 04/21/2025.
- (tier1) Supplier: neither TDS prints a company name and SDS Section 1.3 is blank (RF6406.pdf p.1); supplier left null.
- (tier1) TBN minimum differs (DL2-14746.pdf ≥180 vs DL2-15456.pdf index 168-198); CF/SF treat rate differs (3.7 vs 4.1 %); both TDS undated, see conflicts.
- (tier1) Grades printed only as 'Multi' / 'Mono'.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Richful.
- **Conflict (tier2)** `tier2.tbn`: DL2-15456.pdf p.1 (undated): Total Base Number, mgKOH/g 168-198 185 SH/T0251, ASTM D2896; DL2-14746.pdf p.1 (undated): Total Base Number，mgKOH/g ≥180 SH/T0251，ASTMD2896 — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS p.2 component shares (not element contents): base-oil distillates 10 - 59.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; ZDDP 3 - 29.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed. DL2-14746.pdf prints density and KV100 as 'Report' (no value).

## 72. RICHFUL_RF6408
- (tier1) Only an undated TDS (DL2-15534.pdf); no company name printed (supplier left null; archive folder 'Richful Lube Additive'). No SDS in the archive.
- (tier1) Claim type 'other': text says the oils 'passed Mack T-8A, Caterpillar 1K, Sequence VIII and Mack T-9 engine tests and all bench tests' (no 'meets' wording).
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed.

## 73. SAMA_P2021A
- (tier1) DL2-12295.pdf prints no company name and no date; supplier left null (archive folder 'SAMA'). Only a product brochure, no SDS.
- (tier1) Claims are a bulleted 'Profile' list without approval/meets wording; recorded as claim_type 'other'.
- (tier1) No treat rate is printed (only 'has the lowest VII and DI treat-rates in the market'); treat_rate_matrix left Missing.
- (tier1) Bar chart p.2 ('% Performance Reserve - P2021A additive': Mack T12, OM 501LA, Mack T11 vs limits) has no formulation; not recorded.
- (tier2) No test methods printed. KV40, elements and pour point not printed.

## 74. TIANHE_P_TEC_3232
- (tier1) No date printed on DL2-12939.pdf; supplier from the logo 'TIANHE CHEMICALS' (website ENGLISH.TIANHECHEM.COM). No SDS in the archive.
- (tier1) TREAT RATE table (p.2) has a 'Total base number, mg KOH/g' row with no values (checked on the page image).
- (tier1) Claim type 'meets' from 'surpasses the standard engine tests of API CF4/CF and the OEM requirements of MB 228.1'; table rows 'recommended'.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF4), not from any supplier document; the field is now missing. Confirm permitted API groups with TIANHE CHEMICALS.
- (tier2) User decision 2026-10-17: density stored exactly as printed (1.0130, unit 'kg/m3', DL2-12939.pdf p.1) with the note 'suspected unit error — verify'. Flagged for review.
- (tier2) Values are under the column 'Specification' without min/max; value_kind set to 'specification'. KV40, sulfated ash, Mg, B, Mo, N, S, pour point not printed.

## 75. TREE_TRADING_NT513
- (tier1) No date printed on DL2-14797.pdf; supplier from the footer 'Tree Trading FIZ LLC'. No SDS in the archive.
- (tier1) Claims listed in a table without approval wording, except 'MB 228.3 (Blanket Approval)'; others recorded as 'other' ('(Level)' kept where printed).
- (tier1) 'The typical finished oil BN is 10.1 mg KOH/g at the standard treat of 11.2 wt%' is finished-oil TBN, not package TBN (not entered).
- (tier2) Flash point, Mg, B, S and pour point not printed. Mo printed in ppm.
- (tier2) User decision 2026-10-17: density field stores the number 0.99 (specific gravity (dimensionless)), which is reported as specific gravity ('Specific Gravity, at 15°C ASTM D4052 0.99', DL2-14797.pdf p.1), not a density in kg/m3; flagged for review.

## 76. WUXI_WX3118
- (tier1) No company name or date printed on DL2-13534.pdf (website WWW.WXNFCN.CN/EN); supplier left null (archive folder 'Wuxi South Petroleum'). No SDS in the archive.
- (tier1) Claim type 'recommended' from the treat-rate table (no approval/meets wording).
- (tier1) Grades printed as '30,40,50,10W/30,15W/40,20W/40,' (trailing comma).
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CI-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Wuxi South Petroleum.
- (tier2) KV100 and Density at 20℃ printed as 'Report' (no value). Values are minimum limits (column 'Limit'), not typicals.
- (tier2) Element methods printed as 'ASTM D - 4628' / 'ASTM D - 3228' as on the sheet.

## 77. WUXI_WX3326
- (tier1) No company name or date printed on DL2-13538.pdf (website WWW.WXNFCN.CN/EN); supplier left null (archive folder 'Wuxi South Petroleum'). No SDS in the archive.
- (tier1) Claim type 'recommended' from the treat-rate table (no approval/meets wording).
- (tier1) Description: 'Its API CF-4/SL/SM engine oil has excellent high temperature detergency, antioxidation, antiwear and anticorrosion properties.'
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Wuxi South Petroleum.
- (tier2) KV100 and Density at 20℃ printed as 'Report' (no value). Values are minimum limits (column 'Limit'), not typicals.
- (tier2) Element methods printed as 'ASTM D - 4628' / 'ASTM D - 3228' as on the sheet.

## 78. AFTON_HITEC_8767B
- (general) DL2-10367.pdf is the HiTEC® 8766B bulletin; HiTEC® 8767B appears only as a second column of 'Typical Characteristics' and as a dose column in the 'Recommended Dosage' table (p.2). Per decision (b) only the 8767B column is used here.
- (general) Function / chemical family of HiTEC® 8767B are not stated anywhere in the archive; function, chemical_family, active content and carrier left Missing; component_subtype left null (no VM/PPD statement). Could be looked up later in an Afton bulletin for 8767B.
- (general) Physical properties printed for HiTEC® 8767B (no field in the component template; DL2-10367.pdf p.2, 'Typical Characteristics'): Density at 15°C, g/ml 0.918; Flash Point, °C (PMCC) 135 min.; Kinematic Viscosity at 100°c, mm2/s 187.
- (general) Treat rate: only one dose (3.3% in the 8766B SAE 10W-40 route) is printed; no min/max/typical range for 8767B on its own.
- (general) No old Product_JSON file exists for HiTEC 8767B; folder name AFTON_HITEC_8767B created per the naming rule.

## 79. LUBRIZOL_CV6320
- (general) CV6320 is filed under 'Additive packages/LUBRIZOL' but is a component ('Ashless Antiwear Performance Booster', DL2-12015.pdf p.1). Not a VM or PPD, so only general.json is created.
- (general) Chemical family is not named. SDS DL2-12016.pdf p.2 Section 3 lists 'Olefin sulfide 1 - 5%', 'Ethoxylated alcohol 0.5 - 1%' and '++ Aryl thiophosphate (597-82-0) 0.1 - 0.5%' (component shares); chemical_family and active_content left Missing.
- (general) Function-specific marker not in template: SULFUR 0.60 (% weight, Typical; DL2-12015.pdf p.1).
- (general) Physical properties (no field in the component template), DL2-12015.pdf p.1 (Target column): FLASH POINT, C, PMCC 181; POUR POINT, C -21; SPECIFIC GRAVITY @ 15.6 C 0.849 / 0.869 / 0.889 (min/target/max); VISCOSITY @ 100 C, CST 69; VISCOSITY @ 40 C, CST 787; LBS PER U.S. GAL @ 15.6 C 7.24. SDS DL2-12016.pdf p.4-5 prints the same: flash 181 °C (Pensky-Martens Closed Cup), relative density 0,849 - 0,889 (15,6 °C), 787 mm2/s (40 °C), 69 mm2/s (100 °C), pour point -21 °C.
- (general) SDS supplier block names LUBRIZOL FRANCE (Rouen); TDS is The Lubrizol Corporation. SDS Issue Date 21.12.2017, Version 1.1.

## 80. RF6602
- (general) TDS DL2-14874.pdf ('TDS OF RF6602') undated; SDS RF6602.pdf issue/revision 18/2/2022.
- (general) Physical properties (no field in the component templates): TDS DL2-14874.pdf p.1 (Index / Typical, method): Kinematic Viscosity (100℃) 1100-1850 / 1360 mm2/s ASTM D445; Flash Point (COC) ≮180 / 210 ℃ ASTM D92; Density (20℃) 850-950 / 919 kg/m3 ASTM D4052; Color ＜0.5 ASTM D1500. SDS RF6602.pdf Section 9: Flash point 160 °C; Viscosity, kinematic 53691mm²/s (40℃); Density 0.9 g/cm³ (no temperature).
- (general) Flash point differs: TDS index '≮180' / typical 210 ℃ (COC) vs SDS 'Flash point : 160 °C' (no method). No template field; recorded here, not resolved.
- (general) Density: TDS 919 kg/m3 (20℃) vs SDS 0.9 g/cm³ - same value rounded to one decimal, not a conflict.
- (general) Applications (TDS p.1): 'suitable for the blending of hydraulic oil (especially low temperature hydraulic oil), gear oil, shock absorber oil, transmission oil and other kinds of oil' - no compatibility restrictions printed (compatibility_restrictions left Missing; 150N / 500N / Group Ⅲ 6# are only the thickening-test oils).
- (general) No recommended treat rate is printed (only test doses 1/3/5 % and 6/10 %); treat_rate left Missing. Secondary function not stated (text: 'can effectively increase the viscosity index and improve the low temperature performance of the oil').
- (vm) Thickening table (TDS p.1): reference oils 150N, 500N, Group Ⅲ 6# at 0/1/3/5 % treat; ΔKV100 values are Calculated (difference from the 0 % row). No test method printed -> 'usable' false.
- (vm) Shear test 'The Shear of Diesel Injector Nozzle' (30 and 250 cycles) in 150N at 6 % and 10 %: no standard (e.g. ASTM D6278/D7109) and no SSI printed; percentage KV100 loss calculated. Units for KV100 not printed in that table.
- (vm) Polymer form (solid/concentrate) not stated; appearance 'Clear、bright、no sediment viscous liquid'. Treat range by SAE grade, HTHS, CCS/MRV impact, gelation and dissolution temperature not printed.
- (vm) Storage (TDS p.1): short-term storage/transport ≤ 75℃, long-term ≤ 45℃ (not a dissolution/blend temperature).
- (vm) Old Product_JSON uses record id 'RF6602' (no RICHFUL_ prefix); kept per decision (d).

## Task 3 data-quality audit (2026-10): base-oil corrections

Base oils have no sections above. This section lists the base-oil open questions added or changed on branch `fix/task3-data-quality`. The additive-package corrections from the same audit appear in each package section above as '(tier1) Permitted base oils (2026-10 audit)'.

### Factual conflicts
- None added. The Ultra-S 2/3 Group II vs Group III difference is a documentation discrepancy between a brand-level label and a grade-level classification of aramcoULTRA, not a conflict between two Ultra-S specifications; it is recorded below as a documentation uncertainty.

### Documentation uncertainties and corrections
- ADNOC_ADBASE_4CST (tier1) OPEN - supplier confirmation needed. History: chemistry was first entered from general knowledge as 'Group III base oil (hydrocracked / hydroisomerised mineral oil)' (status Reported, no source; original question: 'Chemistry is general knowledge only (sheet says Group III / high-purity base oil, not hydrocracked/mineral).'). That claim is not printed on the 2016 sheets. It is now sourced from the official ADNOC ADbase brochure (2020, pp. 2, 4-5), which describes the product-family production process only and post-dates the 2016 spec sheet. Ask ADNOC to confirm that this process applies to ADbase 4 cSt.
- ADNOC_ADBASE_6CST (tier1) OPEN - supplier confirmation needed. History: chemistry was first entered from general knowledge as 'Group III base oil (hydrocracked / hydroisomerised mineral oil)' (status Reported, no source; original question: 'Chemistry is general knowledge only (sheet says Group III / high-purity base oil, not hydrocracked/mineral).'). That claim is not printed on the 2016 sheets. It is now sourced from the official ADNOC ADbase brochure (2020, pp. 2, 4-5), which describes the product-family production process only and post-dates the 2016 spec sheet. Ask ADNOC to confirm that this process applies to ADbase 6 cSt.
- ADNOC_ADBASE_8CST (tier1) OPEN - supplier confirmation needed. History: chemistry was first entered from general knowledge as 'Group III base oil (hydrocracked / hydroisomerised mineral oil)' (status Reported, no source; original question: 'Chemistry is general knowledge only (sheet says Group III / high-purity base oil, not hydrocracked/mineral).'). That claim is not printed on the 2016 sheets. It is now sourced from the official ADNOC ADbase brochure (2020, pp. 2, 4-5), which describes the product-family production process only and post-dates the 2016 spec sheet. Ask ADNOC to confirm that this process applies to ADbase 8 cSt.
- S_OIL_ULTRA_S_2 (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); S-OIL states Ultra-S and aramcoULTRA have the same properties'; note 'Classification supported by manufacturer-published Ultra-S/aramcoULTRA equivalence; not directly stated in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 2 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 2 and aramcoULTRA 2 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.24 lists aramcoULTRA 2 as API Base Oil Category Group II, and p.23 states 'These grades of aramcoULTRA are not classified as API Group III' for aramcoULTRA 2 and 3 (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Documentation discrepancy, not a conflict between Ultra-S specifications: the S-OIL page labels the aramcoULTRA brand as a whole 'aramcoULTRA (Group Ⅲ)', whereas the Aramco catalog classifies the aramcoULTRA 2 grade as Group II. Neither document classifies Ultra-S 2. Confirm the API Group of Ultra-S 2 with S-OIL.
- S_OIL_ULTRA_S_3 (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); S-OIL states Ultra-S and aramcoULTRA have the same properties'; note 'Classification supported by manufacturer-published Ultra-S/aramcoULTRA equivalence; not directly stated in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 3 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 3 and aramcoULTRA 3 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.24 lists aramcoULTRA 3 as API Base Oil Category Group II, and p.23 states 'These grades of aramcoULTRA are not classified as API Group III' for aramcoULTRA 2 and 3 (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Documentation discrepancy, not a conflict between Ultra-S specifications: the S-OIL page labels the aramcoULTRA brand as a whole 'aramcoULTRA (Group Ⅲ)', whereas the Aramco catalog classifies the aramcoULTRA 3 grade as Group II. Neither document classifies Ultra-S 3. Confirm the API Group of Ultra-S 3 with S-OIL.
- S_OIL_ULTRA_S_4 (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); S-OIL states Ultra-S and aramcoULTRA have the same properties'; note 'Classification supported by manufacturer-published Ultra-S/aramcoULTRA equivalence; not directly stated in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 4 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 4 and aramcoULTRA 4 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.25 lists aramcoULTRA 4 as API Base Oil Category Group III (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Confirm the API Group of Ultra-S 4 with S-OIL.
- S_OIL_ULTRA_S_6 (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); S-OIL states Ultra-S and aramcoULTRA have the same properties'; note 'Classification supported by manufacturer-published Ultra-S/aramcoULTRA equivalence; not directly stated in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 6 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 6 and aramcoULTRA 6 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.25 lists aramcoULTRA 6 as API Base Oil Category Group III (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Confirm the API Group of Ultra-S 6 with S-OIL.
- S_OIL_ULTRA_S_8 (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); Ultra-S and aramcoULTRA are stated by S-OIL to have the same quality'; note 'API Group III supported by official manufacturer product-family classification and equivalence; not directly printed in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 8 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 8 and aramcoULTRA 8 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.25 lists aramcoULTRA 8 as API Base Oil Category Group III (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Confirm the API Group of Ultra-S 8 with S-OIL.
- S_OIL_ULTRA_S_8 (tier2) API Group is not printed in any reviewed S-OIL document for Ultra-S 8; the Tier 1 API Group is Missing (2026-10 audit). S-OIL's published Ultra-S/aramcoULTRA equivalence and the Aramco catalog classification of aramcoULTRA 8 are indirect evidence only; see the Tier 1 open questions.
- S_OIL_PREMIUM_P_20 (tier1) API Group and chemistry (2026-10 audit): both Tier 1 values were attributed to sources for a different product, aramcoULTRA 8, and are now Missing. Former API Group: 'Group III' (Reported), cited to the Aramco base-oil catalog 2024 p.25, which is the aramcoULTRA slate table for grades 4/6/8 and does not list P-20 or any Premium-series grade; former note: 'Group III explicitly confirmed for aramcoULTRA 8 in Aramco's official 2024 base-oil catalog. The original 2018 SDS did not state the API Group.' Former chemistry: 'Distillates (petroleum), hydrotreated heavy paraffinic' (Reported; printed text 'Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7; purity 100%'), cited to DL2-14611.pdf p.1, the SDS for 'Base Oil aramcoULTRA 8 (250 Neutral)' revised 2018-09-07. Former open question: 'API Group III confirmed for aramcoULTRA 8 using Aramco's official 2024 base-oil catalog; classification was not explicitly stated in the original 2018 SDS.' No reviewed document states the API Group or chemistry of P-20; the Premium Series sheet DL2-11173.pdf names neither. Confirm both with S-OIL.

