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
- **Conflict (tier1)** [edition difference] `tier1.performance_claims / tier1.treat_rate_matrix (MTU 2.0, row 10.3% + 5.0% HiTEC® 12255, SAE 15W-40, GP I)`: DL2-11412.PDF p.2 (05/18): dot in MTU 2.0 column; DL2-14639.pdf p.2 (08/18): no dot in MTU 2.0 column — 05/18 vs 08/18 bulletin. Newer (08/18) used in the fields; not resolved.
- **Conflict (tier1)** [edition difference] `tier1.performance_claims / tier1.treat_rate_matrix (DDC 93K215, row 11.7% + 0.9% HiTEC® 12260, SAE 10W-30, GP II)`: DL2-11412.PDF p.2 (05/18): no dot in DDC 93K215 column; DL2-14639.pdf p.2 (08/18): dot in DDC 93K215 column — 05/18 vs 08/18 bulletin. Newer (08/18) used in the fields; not resolved.
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
- (tier1) 2026-10-17: package_type filled from the Chevron Oronite official web page https://www.oronite.com/products-technology/heavy-duty-motor-oils.html (NOT from the datasheet).

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
- **Conflict (tier2)** [conflicting values between different documents] `tier2.flash_point`: DL2-10204.pdf p.1 (2004-11-09): Flash Point (PM) 190 °C ASTM D 93; DL2-10204.pdf p.6 (2008-12-02): Flash Point [Method]: >110C (230F) [ ASTM D-93] — TDS typical (2004, p.1) vs SDS lower bound (2008, p.6; also p.3 Section 5). Values are compatible (190 > 110) but printed differently; per rule the field holds the more recent SDS value. Not resolved.
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
- (tier2) Density holds 'LBS PER U.S. GAL @ 15.6 C 8.11' (Target), with 'LBS PER IMP GAL @ 15.6 C 9.74' as an alternate entry; 'SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993' is recorded in the optional specific_gravity property (2026-10-24 pilot).
- (tier2) Physical values are in the 'Target' column (target, not typical); chemical values in the 'Typical' column. KV40/flash/pour usually have no min/max.
- (tier2) Package TBN is printed only where the table has a 'BASE NUMBER (MGKOH/G)' row; otherwise left Missing.
- (tier2) [History] User decision 2026-10-17: the density field stored 0.973 (specific gravity, dimensionless) from 'SPECIFIC GRAVITY @ 15.6 C 0.953 0.973 0.993' (DL2-10653.pdf p.1). Superseded 2026-10-24 by the approved optional specific_gravity property: the specific gravity moved there and density now holds the printed 8.11 lbs/US gal @ 15.6 C.

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
- **Conflict (tier1)** [edition difference] `tier1.performance_claims (Cummins CES 20076 claim code)`: DL2-14638.pdf p.1 (2020-01-20): Cummins CES 20076 L; DL2-15581.pdf p.1 (2022-05-13): Cummins CES 20076 A — 2020 sheet: 'L - Licensable'; 2022 sheet: 'A - Approved'. Fields use the newer 2022 sheet. Not resolved.
- **Conflict (tier1)** [edition difference] `tier1.performance_claims (Cummins CES 20077 claim code)`: DL2-14638.pdf p.1 (2020-01-20): Cummins CES 20077 L; DL2-15581.pdf p.1 (2022-05-13): Cummins CES 20077 A — 2020 sheet: 'L - Licensable'; 2022 sheet: 'A - Approved'. Fields use the newer 2022 sheet. Not resolved.
- **Conflict (tier1)** [edition difference] `tier1.performance_claims (Cummins CES 20078 claim code)`: DL2-14638.pdf p.1 (2020-01-20): Cummins CES 20078 L; DL2-15581.pdf p.1 (2022-05-13): Cummins CES 20078 A — 2020 sheet: 'L - Licensable'; 2022 sheet: 'A - Approved'. Fields use the newer 2022 sheet. Not resolved.
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
- (tier2) 2026-10-17: sulfated ash calculated (≥13.3 wt.%) from the TDS element minimums with ASTM D874 factors (NOT from the datasheet).

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
- **Conflict (tier2)** [conflicting values between different documents] `tier2.density`: DL2-13819.pdf p.1 (undated): Density( 20℃), kg/m3 990 GB/T13377，ASTMD4052; DL2-15451.pdf p.1 (undated): Density (20℃), kg/m3 968-1008 988 SH/T 0604, ASTM D4052; DL2-13820.pdf p.5 (2020-07-06): Density 990 kg/m3; DL2-15831.pdf p.5 (2021-09-02): Density : 0.988 g/cm³ (20 °C) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.kv100`: DL2-13819.pdf p.1 (undated): Kinematic Viscosity, ( 100℃), mm2/s 227 GB/T265，ASTMD445; DL2-15451.pdf p.1 (undated): Kinematic Viscosity (100℃), mm2/s Report 185 GB/T 265, ASTM D445; DL2-13820.pdf p.5 (2020-07-06): Kinematic viscosity 200 mm2/s (100 °C); DL2-15831.pdf p.5 (2021-09-02): Viscosity, dynamic : 185 mm²/s (100 °C) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.tbn`: DL2-13819.pdf p.1 (undated): Total Base Number, mgKOH/g 106 SH/T0251，ASTMD2896; DL2-15451.pdf p.1 (undated): Total Base Number, mgKOH/g 97-119 108 SH/T 0251, ASTM D2896; DL2-13820.pdf p.5 (2020-07-06): Total base number 106 mgKOH/g — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.elements.Zn`: DL2-13819.pdf p.1 (undated): Zn Content, %（m/m） 1.3 GB/T17476，ASTM D4951; DL2-15451.pdf p.1 (undated): Zn Content, m% 1.13-1.38 1.24 GB/T 17476, ASTM D4951 — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.elements.Ca`: DL2-13819.pdf p.1 (undated): Ca Content,%（m/m） 3.0 GB/T17476，ASTM D4951; DL2-15451.pdf p.1 (undated): Ca Content, m% 2.82-3.44 3.15 GB/T 17476, ASTM D4951 — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) Component shares (not element contents): SDS DL2-15831.pdf p.2: base-oil distillates 10 - 39.9 %; ZDDP (68649-42-3) 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 9.9 %; molybdenum dithiocarbamate 0.1 – 1.99 %. SDS DL2-13820.pdf p.2 lists ingredients without percentages.
- (tier2) Sulfated ash, KV40, Mg, B, S and pour point not printed.
- (tier2) 2026-10-17: TBN, KV100, density, Ca, Zn filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=112 (NOT from the datasheet); the page agrees with DL2-15451.pdf and with the file's existing P, Mo, N.

## 60. RICHFUL_RF6069
- (tier1) TDS DL2-15618.pdf has no date; SDS DL2-15619.pdf: Issue/Revision date 1/4/2022, version 2.0 (body image/vector graphics, read visually).
- (tier1) KV100 differs: TDS 118 mm2/s vs SDS 142 mm²/s; TDS undated, so the field is left null (see conflicts).
- (tier1) RF0206 (1.9% in the CF-4 route) is not described on the sheet.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.kv100`: DL2-15618.pdf p.1 (undated): Kinematic Viscosity (100℃), mm2/s Report 118 GB/T 265, ASTM D445; DL2-15619.pdf p.5 (2022-01-04): Viscosity, kinematic : 142 mm²/s (100 °C, ASTM D445) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS DL2-15619.pdf p.2 component shares (not element contents): base-oil distillates 10 - 59.9 %; ZDDP (68649-42-3) 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 4.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S and pour point not printed.
- (tier2) 2026-10-17: KV100 filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=32 (NOT from the datasheet).

## 61. RICHFUL_RF6071L
- (tier1) Only an undated TDS is in the archive for RF6071L (no SDS). The sheet prints no company name; supplier left null (archive folder: Richful Lube Additive).
- (tier2) Column headers 'Requirement Limit' / 'Typical Value'. Sulfated ash, KV40, Mg, B, S and pour point not printed.

## 62. RICHFUL_RF6077
- (tier1) TDS DL2-15536.pdf has no date; SDS DL2-15542.pdf Issue/Revision date 11/16/2023.
- (tier1) KV100 (TDS 160 vs SDS 150 mm2/s) and density (TDS 998 kg/m3 at 20 ℃ vs SDS 0.991 g/cm3 at 15 °C) differ; TDS undated, fields left null (see conflicts). The density temperatures also differ.
- (tier1) Claim type 'meets' from 'is compliant to API CI-4 specification'. OCP VII required but not named and no dose.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.density`: DL2-15536.pdf p.1 (undated): Density (20℃), kg/m3 978-1018 998 GB/T 13377, ASTM D4052; DL2-15542.pdf p.5 (2023-11-16): Density : 0.991 g/cm3 (15 °C) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.kv100`: DL2-15536.pdf p.1 (undated): Kinematic Viscosity (100℃), mm2/s Report 160 GB/T 265, ASTM D445; DL2-15542.pdf p.5 (2023-11-16): Viscosity, kinematic : 150mm2/s (100 °C) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS p.2 component shares (not element contents): base-oil distillates 10 - 59.9 %; ZDDP 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 2.9 %; molybdenum dithiocarbamate 0.1 – 0.99 %.
- (tier2) SDS also prints vapour pressure 28.7 mmHg at 65 °C and 15.9 mmHg at 45 °C (no template field). Sulfated ash, KV40, Mg, B, S, pour point not printed.
- (tier2) KV100 (TDS 160 vs SDS 150 mm2/s) and density (TDS 998 kg/m3 at 20 ℃ vs SDS 0.991 g/cm3 at 15 °C) differ; TDS undated, fields originally left null; filled 2026-10-18 by user decision (see conflicts). The density temperatures also differ.

## 63. RICHFUL_RF6078
- **Conflict (tier1)** [conflicting values between different documents] `tier1.treat_rate_matrix (ACEA E7/API CI-4)`: DL2-15832.pdf p.1 (undated): ACEA E7/API CI-4 10W-30, 10W-40, 15W-40, 20W-50 11.85%; RF6078%20-%20TDS.pdf p.1 (undated): ACEA E7/API CI-4 10W-30, 10W-40, 15W-40, 20W-50 10.85% — Both TDS undated; DL2-15832.pdf lists API CI-4 alone at 10.85%, 'RF6078 - TDS.pdf' lists API CI-4 Plus at 11.85%. Not resolved.
- (tier1) Both TDS (DL2-15832.pdf and 'RF6078 - TDS.pdf') are undated; SDS DL2-15833.pdf revision 9/2/2021 (issue date printed '9/022021'); SDS body is image/vector graphics, read visually.
- (tier1) Density: TDS 972 kg/m3 vs SDS 975 kg/m³ (both 20 ℃); TDS undated, field left null (see conflicts).
- (tier1) The two TDS give different rates for the 'ACEA E7/API CI-4' row; see conflicts.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.density`: DL2-15832.pdf p.1 (undated): Density (20℃), kg/m3 952-992 972 GB/T 13377, ASTM D4052; RF6078%20-%20TDS.pdf p.1 (undated): Density (20℃), kg/m3 952-992 972 SH/T 0604, ASTM D4052; DL2-15833.pdf p.5 (2021-09-02): Density : 975 kg/m³ (20 °C, ASTM D4052) — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS p.2 component shares (not element contents): base-oil distillates 10 - 39.9 %; ZDDP 3 - 17.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; alkylated diphenylamine 0.5 - 9.9 %; molybdenum dithiocarbamate 0.1 – 1.99 %.
- (tier2) Sulfated ash, KV40, Mg, B, N, S, pour point not printed.
- (tier2) 2026-10-17: density filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=109 (NOT from the datasheet).

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
- **Conflict (tier2)** [conflicting values between different documents] `tier2.kv100`: DL2-15836.pdf p.2 (2025-05-13): Kinematic Viscosity (100℃), mm2/s Report 132 ASTM D445; DL2-15837.pdf p.5 (2025-04-09): Viscosity, kinematic : 130 mm2/s (100 °C) — All documents dated; field holds the most recent (DL2-15836.pdf). Not resolved.
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
- **Conflict (tier2)** [conflicting values between different documents] `tier2.density`: DL2-15839.pdf p.1 (undated): Density (20℃), kg/m3 943-983 963 SH/T 0604，ASTM D4052; DL2-15840.pdf p.5 (2024-10-17): Relative density : 0.958 g/cm3@20℃ — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.kv100`: DL2-15839.pdf p.1 (undated): Kinematic Viscosity (100℃), mm2/s Report 177 GB/T 265，ASTM D445; DL2-15840.pdf p.5 (2024-10-17): Viscosity, kinematic : 178.2 mm2/s @100℃ — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS p.2 component shares (not element contents): distillate 10 – 59.9 %; ZDDP 3 – 17.9 %; overbased calcium sulfurized phenate 1 – 14.9 %; hindered phenolic ester 1 – 14.9 %; bis(nonylphenyl)amine 1 – 9.9 %.
- (tier2) KV40, Mg, B, Mo, S, pour point not printed.
- (tier2) KV100 (TDS 177 vs SDS 178.2 mm2/s) and density (TDS 963 kg/m3 vs SDS 0.958 g/cm3, both 20 ℃) differ; TDS undated, fields originally left null; filled 2026-10-18 by user decision (see conflicts).

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
- **Conflict (tier1)** [conflicting values between different documents] `tier1.treat_rate_matrix (API CF/SF, Multi)`: DL2-15456.pdf p.1 (undated): CF/SF Multi 4.1%; DL2-14746.pdf p.1 (undated): CF/SF （Multi） 3.7 — Both TDS undated; not resolved.
- (tier1) Two undated TDS: DL2-14746.pdf ('TDS OF RF6406', prints minimum values only) and DL2-15456.pdf (index ranges + typicals); SDS RF6406.pdf issue 11/26/2021, revision 04/21/2025.
- (tier1) Supplier: neither TDS prints a company name and SDS Section 1.3 is blank (RF6406.pdf p.1); supplier left null.
- (tier1) TBN minimum differs (DL2-14746.pdf ≥180 vs DL2-15456.pdf index 168-198); CF/SF treat rate differs (3.7 vs 4.1 %); both TDS undated, see conflicts.
- (tier1) Grades printed only as 'Multi' / 'Mono'.
- (tier1) Permitted base oils (2026-10 audit): previously recorded as reported [Group I, Group II, Group III] with no source, from an industry rule of thumb based on the highest API claim (API CF-4), not from any supplier document; the field is now missing. Confirm permitted API groups with Richful.
- **Conflict (tier2)** [conflicting values between different documents] `tier2.tbn`: DL2-15456.pdf p.1 (undated): Total Base Number, mgKOH/g 168-198 185 SH/T0251, ASTM D2896; DL2-14746.pdf p.1 (undated): Total Base Number，mgKOH/g ≥180 SH/T0251，ASTMD2896 — At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.
- (tier2) SDS p.2 component shares (not element contents): base-oil distillates 10 - 59.9 %; overbased calcium sulfurized phenate 1 - 14.9 %; ZDDP 3 - 29.9 %.
- (tier2) Sulfated ash, KV40, Mg, B, Mo, S, pour point not printed. DL2-14746.pdf prints density and KV100 as 'Report' (no value).
- (tier1) 2026-10-17: API CF/SF (Multi) treat rate filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=130 (NOT from the datasheet).
- (tier2) 2026-10-17: TBN filled from the Richful official product page https://www.richful.com/catalogueDetail.html?id=130 (NOT from the datasheet).

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
- (general) [History] VM fields (polymer_chemistry, active_polymer, treat_range_by_sae_grade, thickening_response, shear_stability, post_shear_blend_behaviour, dissolution_blend_temperature) were 'Not Applicable' ('This product is not a viscosity modifier — field does not apply'). Changed to Missing (2026-10 audit): the function of HiTEC® 8767B is not stated in any reviewed source (DL2-10367.pdf only gives its typical characteristics and a 3.3% dose in the 8766B SAE 10W-40 route; no Afton 8767B bulletin was found), so it is not established that the product is not a viscosity modifier. Confirm the function of HiTEC® 8767B with Afton.

## 79. LUBRIZOL_CV6320
- (general) CV6320 is filed under 'Additive packages/LUBRIZOL' but is a component ('Ashless Antiwear Performance Booster', DL2-12015.pdf p.1). Not a VM or PPD, so only general.json is created.
- (general) Chemical family is not named. SDS DL2-12016.pdf p.2 Section 3 lists 'Olefin sulfide 1 - 5%', 'Ethoxylated alcohol 0.5 - 1%' and '++ Aryl thiophosphate (597-82-0) 0.1 - 0.5%' (component shares); chemical_family and active_content left Missing.
- (general) Function-specific marker not in template: SULFUR 0.60 (% weight, Typical; DL2-12015.pdf p.1).
- (general) Physical properties (no field in the component template), DL2-12015.pdf p.1 (Target column): FLASH POINT, C, PMCC 181; POUR POINT, C -21; SPECIFIC GRAVITY @ 15.6 C 0.849 / 0.869 / 0.889 (min/target/max); VISCOSITY @ 100 C, CST 69; VISCOSITY @ 40 C, CST 787; LBS PER U.S. GAL @ 15.6 C 7.24. SDS DL2-12016.pdf p.4-5 prints the same: flash 181 °C (Pensky-Martens Closed Cup), relative density 0,849 - 0,889 (15,6 °C), 787 mm2/s (40 °C), 69 mm2/s (100 °C), pour point -21 °C.
- (general) SDS supplier block names LUBRIZOL FRANCE (Rouen); TDS is The Lubrizol Corporation. SDS Issue Date 21.12.2017, Version 1.1.
- (general) [History] 2026-10-17: Ca, Mg, Zn, Mo markers set to N/A (ashless booster); P marker remains Missing. Changed back to Missing (2026-10 audit): the N/A status was inferred from the product type and SDS composition; the template does not exclude these markers and absent elements are not inferred. Confirm Ca, Mg, Zn, Mo and P contents with Lubrizol.

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
- (vm) Storage temperature differs between Richful documents (no template field; recorded here, not resolved): TDS DL2-14874.pdf p.1 (undated; PDF created 2021-05-16): 'For short-term storage and transportation, the temperature of the product shall not surpass 75℃; for long-term storage,it shall not surpass 45℃.' Richful product page https://www.richful.com/catalogueDetail.html?id=105 (English; Chinese id=104), page data feed productId=105, record created 2023-05-23, no revision date, retrieved 2026-10-23: 'The maximum storage and transportation temperature shall not exceed 60℃ in short term, and shall not exceed 45℃ in long term.' (Chinese page: '短期最高温度不应超过 60℃；长期储存最高温度不应超过 45℃'). Both state the same condition (short-term storage and transport) and the same 45℃ long-term limit, so the short-term limits genuinely differ (75℃ vs 60℃). The page is reachable directly but is not in Richful's public catalogue listing. Confirm the current short-term limit with Richful.
- (vm) Old Product_JSON uses record id 'RF6602' (no RICHFUL_ prefix); kept per decision (d).
- (general) [History] 2026-10-17: function-specific markers (TBN, Ca, Mg, P, Zn, Mo) set to N/A - not applicable to a PMA VII. Changed back to Missing (2026-10 audit): the N/A status was inferred from the product type and SDS composition; the template does not exclude these markers and absent elements are not inferred. Neither the TDS, the SDS nor Richful's product page states them. Confirm TBN, Ca, Mg, P, Zn and Mo contents with Richful.

## 81. ADNOC_ADBASE_2CST
- (tier1) CCS is printed as '-' for 2 cSt: ask whether a value exists and at which temperature. [fields: ccs]
- (tier1) No test method is printed for KV40, KV100, VI and density on the brochure. [fields: kv40, kv100, viscosity_index, density]
- (tier2) MRV viscosity and yield stress are not reported anywhere for this product. [fields: mrv]
- (tier2) Noack is printed as '-' (not reported) for 2 cSt. [fields: noack_volatility]
- (tier2) Flash point 170 deg C has no method (COC or PMCC): unusable until the method is confirmed. [fields: flash_point]
- (tier2) Pour point has no test method printed. [fields: pour_point]
- (tier3) Cloud point and wax content are not reported. [fields: cloud_point, wax_content]
- (tier3) Sulfur, saturates and aromatics have no test method printed. [fields: sulfur, saturates, aromatics]

## 82. ADNOC_ADBASE_3CST
- (tier1) CCS is printed as '-' for 3 cSt. [fields: ccs]
- (tier1) No test method printed on the brochure for KV40, KV100, VI and density. [fields: kv40, kv100, viscosity_index, density]
- (tier2) MRV viscosity and yield stress not reported anywhere. [fields: mrv]
- (tier2) Noack is printed as '-' for 3 cSt. [fields: noack_volatility]
- (tier2) Flash point 190 deg C has no method (COC/PMCC). [fields: flash_point]
- (tier2) Pour point has no test method printed. [fields: pour_point]
- (tier3) Cloud point and wax content not reported. [fields: cloud_point, wax_content]
- (tier3) Sulfur, saturates and aromatics have no test method printed. [fields: sulfur, saturates, aromatics]

## 83. ADNOC_ADBASE_4CST
- (tier1) No test method printed on the brochure for typical KV40, KV100, VI and density (spec sheet gives ASTM D445 / D2270 / D4052 for limits). [fields: kv40, kv100, viscosity_index, density]
- (tier1) OPEN - supplier confirmation needed. History: chemistry was first entered from general knowledge as 'Group III base oil (hydrocracked / hydroisomerised mineral oil)' (status Reported, no source; original question: 'Chemistry is general knowledge only (sheet says Group III / high-purity base oil, not hydrocracked/mineral).'). That claim is not printed on the 2016 sheets. It is now sourced from the official ADNOC ADbase brochure (2020, pp. 2, 4-5), which describes the product-family production process only and post-dates the 2016 spec sheet. Ask ADNOC to confirm that this process applies to ADbase 4 cSt. [fields: api_group_chemistry.chemistry]
- (tier2) MRV viscosity and yield stress are not reported anywhere. [fields: mrv]
- (tier2) Flash point 220 deg C (brochure typical) has no method printed; the spec sheet's limit is COC. Confirm the typical value is also COC (COC and PMCC differ). [fields: flash_point]
- (tier2) Noack typical value has no test temperature/duration printed (spec sheet cites ASTM 5800 Method B). [fields: noack_volatility]
- (tier3) Cloud point and wax content are not reported. [fields: cloud_point, wax_content]
- (tier3) Spec sheet gives sulfur only as a maximum limit (10 mg/kg); brochure typical is '<3' mg/kg. Saturates/aromatics 'Report' only on spec sheet: no method on the typical values. [fields: sulfur, saturates, aromatics]

## 84. ADNOC_ADBASE_6CST
- (tier1) No test method printed on the brochure for typical KV40, KV100, VI and density (spec sheet gives ASTM D445 / D2270 / D4052 for limits). [fields: kv40, kv100, viscosity_index, density]
- (tier1) OPEN - supplier confirmation needed. History: chemistry was first entered from general knowledge as 'Group III base oil (hydrocracked / hydroisomerised mineral oil)' (status Reported, no source; original question: 'Chemistry is general knowledge only (sheet says Group III / high-purity base oil, not hydrocracked/mineral).'). That claim is not printed on the 2016 sheets. It is now sourced from the official ADNOC ADbase brochure (2020, pp. 2, 4-5), which describes the product-family production process only and post-dates the 2016 spec sheet. Ask ADNOC to confirm that this process applies to ADbase 6 cSt. [fields: api_group_chemistry.chemistry]
- (tier2) MRV viscosity and yield stress are not reported anywhere. [fields: mrv]
- (tier2) Flash point 235 deg C (brochure typical) has no method printed; the spec sheet's limit is COC. Confirm the typical value is also COC (COC and PMCC differ). [fields: flash_point]
- (tier2) Noack typical value has no test temperature/duration printed (spec sheet cites ASTM 5800 Method B). [fields: noack_volatility]
- (tier3) Cloud point and wax content are not reported. [fields: cloud_point, wax_content]
- (tier3) Spec sheet gives sulfur only as a maximum limit (10 mg/kg); brochure typical is '<3' mg/kg. Saturates/aromatics 'Report' only on spec sheet: no method on the typical values. [fields: sulfur, saturates, aromatics]

## 85. ADNOC_ADBASE_8CST
- (tier1) No test method printed on the brochure for typical KV40, KV100, VI and density (spec sheet gives ASTM D445 / D2270 / D4052 for limits). [fields: kv40, kv100, viscosity_index, density]
- (tier1) OPEN - supplier confirmation needed. History: chemistry was first entered from general knowledge as 'Group III base oil (hydrocracked / hydroisomerised mineral oil)' (status Reported, no source; original question: 'Chemistry is general knowledge only (sheet says Group III / high-purity base oil, not hydrocracked/mineral).'). That claim is not printed on the 2016 sheets. It is now sourced from the official ADNOC ADbase brochure (2020, pp. 2, 4-5), which describes the product-family production process only and post-dates the 2016 spec sheet. Ask ADNOC to confirm that this process applies to ADbase 8 cSt. [fields: api_group_chemistry.chemistry]
- (tier2) MRV viscosity and yield stress are not reported anywhere. [fields: mrv]
- (tier2) Flash point 255 deg C (brochure typical) has no method printed; the spec sheet's limit is COC. Confirm the typical value is also COC (COC and PMCC differ). [fields: flash_point]
- (tier2) Noack typical value has no test temperature/duration printed (spec sheet cites ASTM 5800 Method B). [fields: noack_volatility]
- (tier3) Cloud point and wax content are not reported. [fields: cloud_point, wax_content]
- (tier3) Spec sheet gives sulfur only as a maximum limit (10 mg/kg); brochure typical is '<3' mg/kg. Saturates/aromatics 'Report' only on spec sheet: no method on the typical values. [fields: sulfur, saturates, aromatics]

## 86. ARAMCO_LUBEREF_DURA_150_JEDDAH
- (tier1) KV100, density and CCS are not reported in the reviewed source specifications. [fields: kv100, density, ccs[]]
- (tier2) Not reported in reviewed source specifications; preserve as missing. [fields: mrv[].mrv_viscosity, mrv[].yield_stress, noack_volatility]
- (tier3) Not reported in reviewed source specifications; preserve as missing. [fields: saturates, aromatics, cloud_point, wax_content]

## 87. ARAMCO_LUBEREF_DURA_500_JEDDAH
- (tier1) KV100, density and CCS are not reported in the reviewed source specifications. [fields: kv100, density, ccs[]]
- (tier2) Not reported in reviewed source specifications; preserve as missing. [fields: mrv[].mrv_viscosity, mrv[].yield_stress, noack_volatility]
- (tier3) Not reported in reviewed source specifications; preserve as missing. [fields: saturates, aromatics, cloud_point, wax_content]

## 88. ARAMCO_LUBEREF_DURA_BS150_YANBU
- **Conflict (tier1)** [unit or test-condition discrepancy] `density`: {"note": "The 0.894 kg/L typical density is at 15.6°C (DL2-13944), not 15°C; do not treat it as a 15°C measurement."}
- (tier1) KV40 and CCS are not reported in the reviewed source specifications. [fields: kv40, ccs[]]
- (tier2) Not reported in reviewed source specifications; preserve as missing. [fields: mrv[].mrv_viscosity, mrv[].yield_stress, noack_volatility]
- **Conflict (tier3)** [unit or test-condition discrepancy] `sulfur`: {"sources": [{"file": "DL2-13944.pdf", "page": 1, "printed_text": "Sulfur Content ppm 1.3‡ (‡ D2622)"}, {"file": "DL2-12173.pdf", "page": 1, "printed_text": "Sulfur Content Max WT% 1.3"}], "note": "Conflicting units (ppm vs wt.%). 1.3 wt.% retained from guaranteed specification; verify before use."}
- (tier3) Not reported in reviewed source specifications; preserve as missing. [fields: saturates, aromatics, cloud_point, wax_content]

## 89. ARAMCO_LUBEREF_PRIMA_110
- (tier1) KV100 and CCS are not reported in the reviewed specifications. [fields: kv100, ccs[]]
- (tier2) Not reported in reviewed source specifications; preserve as missing. [fields: mrv[].mrv_viscosity, mrv[].yield_stress]
- (tier3) Not reported in reviewed source specifications; preserve as missing. [fields: aromatics, cloud_point, wax_content]

## 90. ARAMCO_LUBEREF_PRIMA_230
- (tier2) Not reported in reviewed source specifications; preserve as missing. [fields: mrv[].mrv_viscosity, mrv[].yield_stress]
- (tier3) Not reported in reviewed source specifications; preserve as missing. [fields: aromatics, cloud_point, wax_content]

## 91. ARAMCO_LUBEREF_PRIMA_500
- (tier1) KV40 and CCS are not confirmed for the specific Luberef PRIMA 500 product represented by DL2-12172.pdf. [fields: kv40, ccs[]]
- (tier2) Not reported in reviewed source specifications; preserve as missing. [fields: mrv[].mrv_viscosity, mrv[].yield_stress]
- (tier3) Not reported in reviewed source specifications; preserve as missing. [fields: aromatics, cloud_point, wax_content]

## 92. ARAMCO_LUBEREF_PRIMA_70
- (tier1) KV40, density and CCS are not reported in the reviewed source specifications. [fields: kv40, density, ccs[]]
- (tier2) Not reported in reviewed source specifications; preserve as missing. [fields: mrv[].mrv_viscosity, mrv[].yield_stress, noack_volatility]
- (tier3) Not reported in reviewed source specifications; preserve as missing. [fields: aromatics, cloud_point, wax_content]

## 93. BAPCO_BAPBASE_4
- (tier1) Exact grade-specific chemistry and CAS number have not been verified from a BAPbase 4 SDS. [fields: api_group_chemistry.chemistry]
- (tier1) Original Bapco specification says 'To be reported'. An external Ergon catalog gives specific gravity 0.834 at 15/4°C, but no directly reported density in kg/m3 has been entered. [fields: density]
- (tier3) Document says To be reported; no value. [fields: cloud_point]

## 94. BAPCO_BAPBASE_6
- (tier1) Exact grade-specific chemistry and CAS number have not been verified from a BAPbase 6 SDS. [fields: api_group_chemistry.chemistry]
- (tier1) Original Bapco specification provides no numerical density. External Ergon/MOGO 2025 catalog reports specific gravity 0.839 at 15/4°C, but no directly reported density in kg/m3 has been entered. [fields: density]

## 95. BAPCO_BAPBASE_8
- (tier1) Exact grade-specific chemistry and CAS number have not been verified from a BAPbase 8 SDS. [fields: api_group_chemistry.chemistry]
- (tier1) Original Bapco specification says 'To be reported'. External Ergon/MOGO catalog reports specific gravity 0.847 at 15/4°C, but no directly reported density in kg/m3 has been entered. [fields: density]

## 96. GS_CALTEX_150BS
- (tier1) SDS not provided among the two supplier files; reconciliation pending.
- (tier1) No density, sulfur, saturates, CCS or MRV values stated in product specification.

## 97. GS_CALTEX_150N
- (tier1) SDS not supplied in the GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV and cloud point not stated in supplied specification.

## 98. GS_CALTEX_220N
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV and cloud point not stated in supplied specification.

## 99. GS_CALTEX_2CST_H
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.

## 100. GS_CALTEX_2CST_L
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.

## 101. GS_CALTEX_600N
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.

## 102. GS_CALTEX_60N
- (tier1) SDS not supplied in GS Caltex source folder; reconciliation pending.
- (tier1) Density, sulfur, saturates, CCS, MRV, Noack and cloud point not stated in supplied specification.

## 103. CHEVRON_GROUP_II_100R
- (tier1) Not reported in supplier specification. [fields: density]
- (tier3) Supplier says Report, without a numerical sulfur value. [fields: sulfur]

## 104. CHEVRON_GROUP_II_110RLV
- (tier1) Not reported in supplier specification. [fields: density]
- (tier3) Supplier says Report, without a numerical sulfur value. [fields: sulfur]

## 105. CHEVRON_GROUP_II_150R
- (tier1) Not reported in supplier specification. [fields: density]
- (tier3) Supplier says Report, without a numerical sulfur value. [fields: sulfur]

## 106. CHEVRON_GROUP_II_220R
- (tier1) Not reported in supplier specification. [fields: density]
- (tier3) Supplier says Report, without a numerical sulfur value. [fields: sulfur]

## 107. CHEVRON_GROUP_II_600R
- (tier1) Not reported in supplier specification. [fields: density]
- (tier3) Supplier says Report, without a numerical sulfur value. [fields: sulfur]

## 108. CHEVRON_GROUP_II_60R
- (tier1) 60R API group cell is blank in supplied table; heading alone is not an explicit classification. [fields: api_group_chemistry.api_group]
- (tier1) Not reported in supplier specification. [fields: density]
- (tier3) Supplier says Report, without a numerical sulfur value. [fields: sulfur]

## 109. CHEVRON_SYNFLUID_DIMER_C10
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 110. CHEVRON_SYNFLUID_DIMER_C12
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 111. CHEVRON_SYNFLUID_MPAO_100
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 112. CHEVRON_SYNFLUID_MPAO_150
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 113. CHEVRON_SYNFLUID_MPAO_40
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 114. CHEVRON_SYNFLUID_MPAO_50
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 115. CHEVRON_SYNFLUID_MPAO_65
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 116. CHEVRON_SYNFLUID_PAO_2
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 117. CHEVRON_SYNFLUID_PAO_2_5
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 118. CHEVRON_SYNFLUID_PAO_4
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 119. CHEVRON_SYNFLUID_PAO_40
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 120. CHEVRON_SYNFLUID_PAO_5
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 121. CHEVRON_SYNFLUID_PAO_6
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 122. CHEVRON_SYNFLUID_PAO_6_HVI
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 123. CHEVRON_SYNFLUID_PAO_7
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 124. CHEVRON_SYNFLUID_PAO_8
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 125. CHEVRON_SYNFLUID_PAO_8_BLEND
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 126. CHEVRON_SYNFLUID_PAO_9
- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]

## 127. ERGON_HYGOLD_100
- (tier1) API group not stated in supplier specification; independent classification not yet verified.
- (tier1) SDS DL2-10029.pdf requires field-by-field reconciliation before final audit.

## 128. ERGON_HYGOLD_100E
- (tier1) API group is not explicitly stated in supplier specification; independent classification not yet verified.
- (tier1) Corresponding SDS needs product-matched review before final audit.

## 129. ERGON_HYGOLD_5000BS
- (tier1) API group not explicitly stated.
- (tier1) SDS not yet reconciled.

## 130. ERGON_HYGOLD_60
- (tier1) API group not explicitly stated; do not infer from naphthenic description.
- (tier1) SDS DL2-10027.pdf requires full cross-check.

## 131. ERGON_HYGOLD_70E
- (tier1) API group not explicitly stated; do not infer from naphthenic description.
- (tier1) SDS not yet reconciled.

## 132. ERGON_HYGOLD_L1200
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS DL2-10032.pdf requires cross-check.

## 133. ERGON_HYGOLD_L150
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.

## 134. ERGON_HYGOLD_L200
- (tier1) API group not explicitly stated.
- (tier1) SDS reconciliation pending.

## 135. ERGON_HYGOLD_L2000
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.

## 136. ERGON_HYGOLD_L250E
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.

## 137. ERGON_HYGOLD_L350E
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.

## 138. ERGON_HYGOLD_L500
- (tier1) API group not explicitly stated; leave missing.
- (tier1) SDS reconciliation pending.

## 139. ERGON_HYGOLD_L750
- **Conflict (tier1)** [inconsistency within one document] `density_at_15_6_c`: {"description": "TDS reports density at 15.6°C = 0.854 g/cm3 but specific gravity at 15.6°C = 0.9183; these appear inconsistent. Neither has been silently corrected.", "sources": [{"file": "DL2-10414.pdf", "page": 1}]}
- (tier1) API group not explicitly stated.
- (tier1) SDS reconciliation pending.
- (tier1) Density and specific gravity conflict in supplier TDS; verify with supplier.

## 140. ERGON_HYGOLD_OLYMPUS_L500
- (tier1) API group not explicitly stated.
- (tier1) SDS DL2-10026.pdf reconciliation pending.

## 141. ERGON_HYGOLD_P150BS
- (tier1) API group not explicitly stated.
- (tier1) SDS cross-check pending.
- (tier1) Specific gravity 0.8931 at 15.6°C and density 7.437 lb/gal at 15.6°C are supplier-reported; no conversion into canonical density field.

## 142. ERGON_HYGOLD_P40
- (tier1) API group not explicitly stated.
- (tier1) SDS cross-check pending.

## 143. ERGON_HYGOLD_P70N
- (tier1) API group not explicitly stated.
- (tier1) SDS cross-check pending.
- (tier1) Supplier specific gravity 0.8559 and density 0.8552 g/cm3 at 15.6°C differ slightly; retained separately without equating.

## 144. ERGON_HY_40
- (tier1) API group not explicitly stated.
- (tier1) SDS cross-check pending.
- (tier1) Specific gravity reported at 15.6°C; density not directly reported.
- (tier1) PMCC flash point and water content specification retained in ingestion log because template does not offer dedicated fields.

## 145. FORMOSA_150N_GII_PLUS
- (tier1) Supplier group II+ is a commercial subclass, not a separate API group.
- (tier1) Density reported as relative density, not mass density; preserve original units.
- (tier1) KV40 reported only in SDS, not specification.
- **Conflict (tier2)** [conflicting values between different documents] `flash_point`: {"source_a": {"file": "DL2-10001.pdf", "page": 1, "value": "minimum 210 C"}, "source_b": {"file": "DL2-10011.pdf", "page": 3, "value": ">230 C"}, "note": "SDS and specification use different threshold statements; preserve both without assuming equivalence."}
- (tier2) SDS flash point >230 C and specification minimum 210 C differ in stated thresholds; not necessarily contradictory.

## 146. FORMOSA_500N_GII
- (tier1) Density reported as relative density, not mass density; preserve original units.
- (tier1) KV40 reported only in SDS, not specification.

## 147. NESTE_NEXBASE_3020
- (tier1) No product TDS supplied for NEXBASE 3020; only two matching SDS files.
- (tier1) API group, KV100, VI, mass density, sulfur and other absent properties remain missing.
- (tier1) Relative density 0.82 at 15°C must not be treated as mass density.

## 148. NESTE_NEXBASE_3043
- (tier1) TDS edition 5.2 has no calendar revision date; no date inferred.
- (tier1) SDS DL2-15010.pdf reports KV40 typical 20 mm²/s, flash point >220°C, pour point ≤−12°C and relative density 0.82–0.84 at 15°C; these are consistent with TDS values/limits, but SDS density is relative density, not directly substituted for TDS mass density.

## 149. NESTE_NEXBASE_3050
- (tier1) TDS edition 4.2 does not provide a calendar revision date.
- (tier1) No independently identified NEXBASE 3050 SDS among the text-searchable supplier PDFs; SDS reconciliation pending.

## 150. NESTE_NEXBASE_3060
- (tier1) TDS edition 6.2 has no calendar revision date.
- (tier1) SDS DL2-12735.pdf checked; its pour-point and flash-point limits are compatible with TDS specifications.

## 151. NESTE_NEXBASE_3080
- (tier1) TDS edition 2.2 does not specify a calendar revision date.
- (tier1) SDS specific to NEXBASE 3080 not independently verified.

## 152. NYNAS_BASE_STOCK_20
- (tier1) API group not explicitly stated in supplier PDS.
- (tier1) SDS reconciliation pending.

## 153. NYNAS_BNS_5
- (tier1) API group and base-oil chemistry not explicitly stated in this PDS.
- (tier1) SDS reconciliation pending.

## 154. NYNAS_NS_3
- **Conflict (tier1)** [edition difference] `kv40`: {"primary": {"value": 2.92, "source_file": "DL2-15474.pdf", "page": 2}, "alternate": {"value": 2.84, "source_file": "DL2-12382.pdf", "page": 2}, "note": "Different typical values in 2024 and 2016 editions; newer edition selected."}
- **Conflict (tier1)** [edition difference] `density`: {"primary": {"value": 0.863, "source_file": "DL2-15474.pdf", "page": 2}, "alternate": {"value": 0.86, "source_file": "DL2-12382.pdf", "page": 2}, "note": "Different typical values in 2024 and 2016 editions."}
- **Conflict (tier1)** [edition difference] `flash_point`: {"primary": {"value": 95, "source_file": "DL2-15474.pdf", "page": 2}, "alternate": {"value": 94, "source_file": "DL2-12382.pdf", "page": 2}, "note": "Different typical PM flash points in two editions."}
- **Conflict (tier1)** [edition difference] `sulfur`: {"primary": {"value": "<10 ppm", "source_file": "DL2-15474.pdf", "page": 2}, "alternate": {"value": "30 ppm", "source_file": "DL2-12382.pdf", "page": 2}, "note": "Older typical 30 ppm versus newer upper-bound <10 ppm; not interchangeable."}
- (tier1) SDS reconciliation pending.
- (tier1) Older PDS DL2-12382.pdf (2016-11-01) has different typical values; confirm appropriate commercial revision.

## 155. NYNAS_NYBASE_70
- (tier1) API group not explicitly stated: marketed for Group I replacement, not classified as Group I.
- (tier1) SDS reconciliation pending.

## 156. NYNAS_NYFROST_100
- (tier1) Grade-specific SDS reconciliation pending.

## 157. NYNAS_NYFROST_32
- **Conflict (tier1)** [conflicting values between different documents] `kv40`: {"source_a": "DL2-11510.pdf p.2 (2016-11-01)", "value_a": "32 cSt (typical)", "source_b": "DL2-13444.pdf p.6 (2020-05-23)", "value_b": "31 cSt (SDS)", "resolution": "Retained supplier PDS typical value; SDS discrepancy flagged."}
- **Conflict (tier1)** [conflicting values between different documents] `flash_point`: {"source_a": "DL2-11510.pdf p.2 (2016-11-01)", "value_a": "176°C typical, Pensky-Martens (ASTM D93)", "source_b": "DL2-13444.pdf p.6 (2020-05-23)", "value_b": ">180°C closed cup Pensky-Martens", "resolution": "Not numerically compatible; PDS typical retained and SDS limit flagged for review."}
- (tier1) Resolve SDS KV40 31 cSt versus PDS 32 cSt and SDS PM flash >180°C versus PDS PM typical 176°C.
- (tier1) Check whether differing document dates or test conditions explain discrepancy.

## 158. NYNAS_NYFROST_68
- (tier1) API group not explicitly stated in supplied PDS.
- (tier1) Grade-specific SDS reconciliation pending.

## 159. NYNAS_S_3B
- (tier1) SDS DL2-13379.pdf has rounded KV40 3 cSt vs PDS 3.20 cSt; no definitive contradiction (SDS rounded).
- (tier1) SDS flash >100°C consistent with PDS 107°C; SDS density 0.86 g/cm3 rounded vs PDS 0.859 g/cm3.

## 160. NYNAS_T_3
- (tier1) Grade-specific SDS not reconciled.

## 161. NYNAS_T_4
- (tier1) Grade-specific SDS not reconciled.

## 162. NYNAS_T_600
- (tier1) Grade-specific SDS not reconciled.

## 163. NYNAS_T_9
- (tier1) Grade-specific SDS not reconciled.

## 164. PETRONAS_EQUINAS_4
- (tier1) No grade-specific TDS in supplied product source; only SDS available.
- (tier1) API base oil group not explicitly stated in SDS.
- (tier1) Pour point, sulfur, viscosity index and CCS not reported.

## 165. PETRONAS_EQUINAS_6
- (tier1) No separate grade-specific TDS found in supplied inventory.
- (tier1) API group, sulfur, viscosity index and CCS not explicitly reported.

## 166. PETRONAS_EQUINAS_8
- (tier1) No separately verified grade-specific SDS for EQUINAS 8; reconciliation pending.

## 167. PETRONAS_ETRO_3
- (tier1) No grade-specific SDS independently verified for ETRO 3.
- (tier1) No calendar revision date stated on product data sheet.

## 168. PETRONAS_ETRO_4
- (tier1) Supplementary DL2-12475.pdf is image-only and has not been independently reconciled.
- (tier1) No grade-specific SDS independently verified for ETRO 4.
- (tier1) No calendar revision date stated on PDS.
- (tier1) Density measurement temperature is not stated in the PDS; do not infer it.

## 169. PETRONAS_ETRO_4_PLUS
- (tier1) No grade-specific SDS independently verified for ETRO 4+.
- (tier1) No calendar revision date stated on PDS.
- (tier1) Density temperature is not specified; density remains Missing in temperature-dependent template field.

## 170. PETRONAS_ETRO_6
- (tier1) No separate grade-specific SDS verified for ETRO 6.
- (tier1) KV40 and density not reported in supplied TDS.
- (tier1) No dated revision on TDS.
- (tier1) Flash specification is printed as >220°C; no conversion to >=220°C.

## 171. PETRONAS_ETRO_6_PLUS
- **Conflict (tier1)** [conflicting values between different documents] `kv40`: {"primary_source": "DL2-10234.pdf", "primary_value": "32.55 cSt at 40°C (ASTM D445)", "comparison_source": "DL2-14610.pdf", "comparison_value": "34.79 mm²/s at 40°C (ASTM D445), page 4", "assessment": "Different reported values; retain TDS typical value, flag for review."}
- **Conflict (tier1)** [conflicting values between different documents] `flash_point`: {"primary_source": "DL2-10234.pdf", "primary_value": "240°C ASTM D92 (COC)", "comparison_source": "DL2-14610.pdf", "comparison_value": "228°C ASTM D93 (PMCC), page 3", "assessment": "Different methods, not directly comparable; both values retained."}
- **Conflict (tier1)** [conflicting values between different documents] `noack_volatility`: {"primary_source": "DL2-10234.pdf", "primary_value": "5.7 mass% ASTM D5800-B", "comparison_source": "DL2-14610.pdf", "comparison_value": "5.3 mass% ASTM D5800 B, page 4", "assessment": "Different reported values; retain TDS typical value, flag for review."}
- **Conflict (tier1)** [conflicting values between different documents] `density`: {"primary_source": "DL2-10234.pdf", "primary_value": "0.8429 kg/L (temperature not stated)", "comparison_source": "DL2-14610.pdf", "comparison_value": "0.8486 g/cm³ at 15°C ASTM D4052, page 4", "assessment": "TDS lacks measurement temperature; SDS has a stated temperature and is used in the density field, with its own source."}
- (tier1) TDS lacks calendar revision date.
- (tier1) KV40 and Noack differences between TDS and SDS require source-level review.
- (tier1) Flash values are method-specific (D92 vs D93); not interchangeable.
- (tier1) TDS density 0.8429 kg/L has no stated test temperature; SDS density at 15°C used instead.

## 172. PETRONAS_M500
- (tier1) No independently verified grade-specific SDS for M500.
- (tier1) TDS has no stated calendar revision date.

## 173. PETRO_CANADA_PURITY_1003
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 21.5 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 21.7 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 21.7 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 4.4 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 4.45 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 4.45 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-10020.pdf p.2 (2015-07): 115; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity Index: 117 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 117 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Individual API group not explicitly assigned in the supplier family brochure (Group II and Group II+ are described collectively).
- (tier1) Grade-specific SDS reconciliation pending.
- (tier1) Additional Petro-Canada documents not yet reconciled against this brochure.
- **Conflict (tier2)** [edition difference] `tier2.noack_volatility`: DL2-10020.pdf p.2 (2015-07): 15.5 wt%; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): NOACK Volatility, % wt: 16 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 16 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-10020.pdf p.2 (2015-07): −18°C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Pour Point, °C: -24 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints -24 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): COC 210°C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 226 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 226 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).

## 174. PETRO_CANADA_PURITY_1017
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 4.3 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 4.33 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 4.33 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-10020.pdf p.2 (2015-07): 107; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity Index: 109 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 109 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.ccs[-20 C]`: DL2-10020.pdf p.2 (2015-07): @ -20°C: 741 cP; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Cold Crank Simulator, cP @ -20°C: 861 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 861 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.ccs[-25 C]`: DL2-10020.pdf p.2 (2015-07): @ -25°C: 1321 cP; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Cold Crank Simulator, cP @ -25°C: 1330 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 1330 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Individual API group not explicitly assigned in supplier family brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- **Conflict (tier2)** [edition difference] `tier2.noack_volatility`: DL2-10020.pdf p.2 (2015-07): 22.4 wt%; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): NOACK Volatility, % wt: 22 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 22 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-10020.pdf p.2 (2015-07): −24°C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Pour Point, °C: -21 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints -21 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): COC 225°C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 217 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 217 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).

## 175. PETRO_CANADA_PURITY_1020
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 22.3 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 21.3 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 21.3 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 4.4 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 4.16 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 4.16 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-10020.pdf p.2 (2015-07): 94; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity Index: 93 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 93 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Individual API group not explicitly assigned in supplier family brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- **Conflict (tier2)** [edition difference] `tier2.noack_volatility`: DL2-10020.pdf p.2 (2015-07): 33.6 wt%; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): NOACK Volatility, % wt: 27 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 27 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-10020.pdf p.2 (2015-07): -18 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Pour Point, °C: -21 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints -21 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): 210 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 207 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 207 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).

## 176. PETRO_CANADA_PURITY_2204
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 41.5 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 40.2 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 40.2 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 6.3 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 6.27 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 6.27 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-10020.pdf p.2 (2015-07): 102; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity Index: 103 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 103 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.density`: DL2-10020.pdf p.2 (2015-07): 0.87 kg/L; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Density @ 15°C, kg/L: 0.86 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 0.86 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.ccs[-20 C]`: DL2-10020.pdf p.2 (2015-07): @ -20°C: 3400 cP; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Cold Crank Simulator, cP @ -20°C: 2708 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 2708 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.ccs[-25 C]`: DL2-10020.pdf p.2 (2015-07): @ -25°C: 7000 cP; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Cold Crank Simulator, cP @ -25°C: 5361 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 5361 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Individual API group not explicitly assigned in supplier family brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): 240 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 233 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 233 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).

## 177. PETRO_CANADA_PURITY_2305
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 45.4 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 44.8 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 44.8 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 7.0 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 6.97 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 6.97 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-10020.pdf p.2 (2015-07): 110; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity Index: 113 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 113 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.ccs[-25 C]`: DL2-10020.pdf p.2 (2015-07): @ -25°C: 6200 cP; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Cold Crank Simulator, cP @ -25°C: 5660 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 5660 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Individual API group not explicitly assigned in supplier family brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-10020.pdf p.2 (2015-07): -15 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Pour Point, °C: -18 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints -18 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): 230 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 242 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 242 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).

## 178. PETRO_CANADA_PURITY_L35
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 3.7 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 3.83 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 3.83 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.density`: DL2-10020.pdf p.2 (2015-07): 0.82 kg/L; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Density @ 15°C, kg/L: 0.83 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 0.83 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Viscosity index, sulfur and CCS are not reported for L35 in the cited brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group II' (Reported) citing Petro-Canada's ILMA Engage base-oils brochure (https://petrocanadalubricants.com/-/media/pdfs/brochures/base-oils/ilma-engage-sponsorship-base-oils-brochure.ashx, no page), printed_text 'GROUP II - PURITY L35', basis 'External manufacturer brochure - grade-specific Group II table'. That brochure could not be retrieved (Petro-Canada blocks automated access; no Wayback Machine copy; the distributor-hosted 'World-Class Base Oils' copy is also blocked), so no grade-level classification of PURITY L35 could be inspected. Petro-Canada's LUB3213E editions (2015.07 = DL2-10020.pdf p.1; 2023.03 p.1) describe PURITY only as 'Group II and Group II+ base oils' at brand level, which does not classify an individual grade; the field is now Missing. Obtain the brochure or a grade-specific Petro-Canada document to confirm.
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): 135 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 134 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 134 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier2) Individual API group not explicitly assigned in supplier family brochure.

## 179. PETRO_CANADA_PURITY_L40
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 3.4 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 3.62 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 3.62 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 1.3 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 1.37 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 1.37 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.density`: DL2-10020.pdf p.2 (2015-07): 0.85 kg/L; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Density @ 15°C, kg/L: 0.84 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 0.84 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Not verified (2026-10 audit): the grade-level brochure cited for API Group II could not be retrieved; the field is Missing (see the API Group question). Previous note: 'API Group II confirmed from an additional official Petro-Canada manufacturer brochure; the original DL2-10020.pdf did not explicitly assign a grade-specific group.'
- (tier1) Viscosity index, sulfur and CCS are not reported for L40 in the cited brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier1) CCS (2026-10 audit): the 3 CCS values previously recorded here - 1300 mPa.s at -25 °C, 1876 mPa.s at -30 °C, 2390 mPa.s at -35 °C (Reported, Typical, ASTM D5293; cited to https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx, revision 2023-03, no page) - are the PURITY 1003 column of Petro-Canada's 'Typical Properties of PURITY Base Oils' table in LUB3213E / IM-1809E (2023.03) p.2, not PURITY L40. The same values appear under PURITY 1003 in LUB3213E (2015.07) = DL2-10020.pdf p.2. The L35-L65 table in both editions has no Cold Crank Simulator row, so no CCS value is published for PURITY L40; ccs is now Missing. The values were not copied to any other record. Confirm with Petro-Canada whether a CCS value exists for PURITY L40.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group II' (Reported) citing Petro-Canada's ILMA Engage base-oils brochure (https://petrocanadalubricants.com/-/media/pdfs/brochures/base-oils/ilma-engage-sponsorship-base-oils-brochure.ashx, no page), printed_text 'PURITY L40 listed in GROUP II TYPICAL PROPERTIES table', basis 'External manufacturer brochure - grade-specific Group II table'. That brochure could not be retrieved (Petro-Canada blocks automated access; no Wayback Machine copy; the distributor-hosted 'World-Class Base Oils' copy is also blocked), so no grade-level classification of PURITY L40 could be inspected. Petro-Canada's LUB3213E editions (2015.07 = DL2-10020.pdf p.1; 2023.03 p.1) describe PURITY only as 'Group II and Group II+ base oils' at brand level, which does not classify an individual grade; the field is now Missing. Obtain the brochure or a grade-specific Petro-Canada document to confirm.
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-10020.pdf p.2 (2015-07): -33 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Pour Point, °C: -27 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints -27 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): 126 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 127 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 127 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- **Conflict (tier3)** [edition difference] `tier3.saturates`: DL2-10020.pdf p.2 (2015-07): 97.8%; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): % Saturates: 96.4 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 96.4 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier3)** [edition difference] `tier3.aromatics`: DL2-10020.pdf p.2 (2015-07): 2.2%; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): % Aromatics: 3.6 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 3.6 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).

## 180. PETRO_CANADA_PURITY_L45
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 6.3 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 6.31 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 6.31 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 1.9 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 1.94 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 1.94 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Not verified (2026-10 audit): the grade-level brochure cited for API Group II could not be retrieved; the field is Missing (see the API Group question). Previous note: 'API Group II confirmed from an additional official Petro-Canada manufacturer brochure; the original DL2-10020.pdf did not explicitly assign a grade-specific group.'
- (tier1) Viscosity index remains unreported for PURITY L45. Grade-specific CCS remains Missing: the CCS values previously recorded here at -20°C, -25°C, -30°C and -35°C belong to PURITY 1020, not L45; the manufacturer's March 2023 brochure prints no CCS for L45 (see the 'CCS (2026-10 audit)' note).
- (tier1) Grade-specific SDS and differences between brochure editions require reconciliation.
- (tier1) CCS (2026-10 audit): the 4 CCS values previously recorded here - 935 mPa.s at -20 °C, 1716 mPa.s at -25 °C, 3438 mPa.s at -30 °C, 7415 mPa.s at -35 °C (Reported, Typical, ASTM D5293; cited to https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx, revision 2023-03, no page) - are the PURITY 1020 column of Petro-Canada's 'Typical Properties of PURITY Base Oils' table in LUB3213E / IM-1809E (2023.03) p.2, not PURITY L45. The same values appear under PURITY 1020 in LUB3213E (2015.07) = DL2-10020.pdf p.2. The L35-L65 table in both editions has no Cold Crank Simulator row, so no CCS value is published for PURITY L45; ccs is now Missing. The values were not copied to any other record. Confirm with Petro-Canada whether a CCS value exists for PURITY L45.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group II' (Reported) citing Petro-Canada's ILMA Engage base-oils brochure (https://petrocanadalubricants.com/-/media/pdfs/brochures/base-oils/ilma-engage-sponsorship-base-oils-brochure.ashx, no page), printed_text 'PURITY L45 listed in GROUP II TYPICAL PROPERTIES table'. That brochure could not be retrieved (Petro-Canada blocks automated access; no Wayback Machine copy; the distributor-hosted 'World-Class Base Oils' copy is also blocked), so no grade-level classification of PURITY L45 could be inspected. Petro-Canada's LUB3213E editions (2015.07 = DL2-10020.pdf p.1; 2023.03 p.1) describe PURITY only as 'Group II and Group II+ base oils' at brand level, which does not classify an individual grade; the field is now Missing. Obtain the brochure or a grade-specific Petro-Canada document to confirm.
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Viscosity index, sulfur, Noack, saturates, aromatics and CCS are not reported for L45 in the cited brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.

## 181. PETRO_CANADA_PURITY_L50
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 5.2 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 5.51 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 5.51 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 1.7 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 1.78 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 1.78 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Not verified (2026-10 audit): the grade-level brochure cited for API Group II could not be retrieved; the field is Missing (see the API Group question). Previous note: 'API Group II confirmed from Petro-Canada's official Group II typical-properties table; the original DL2-10020.pdf did not explicitly assign a grade-specific group.'
- (tier1) Viscosity index remains unreported for PURITY L50.
- (tier1) Grade-specific CCS remains Missing: the CCS values previously recorded here at -20°C and -25°C belong to PURITY 2204, not L50; no CCS value for PURITY L50 has been found in Petro-Canada documentation (see the 'CCS (2026-10 audit)' note).
- (tier1) Grade-specific SDS and differences between the original 2015 brochure and newer manufacturer documentation require reconciliation.
- (tier1) CCS (2026-10 audit): the 2 CCS values previously recorded here - 2708 mPa.s at -20 °C, 5361 mPa.s at -25 °C (Reported, Typical, ASTM D5293; cited to https://petrocanadalubricants.com/en-us/brand/purity-base-oils/compare, no page) - are the PURITY 2204 column of Petro-Canada's 'Typical Properties of PURITY Base Oils' table in LUB3213E / IM-1809E (2023.03) p.2, not PURITY L50. The 2015.07 edition (DL2-10020.pdf p.2) prints 3400 cP at -20 °C and 7000 cP at -25 °C for PURITY 2204 and no CCS for L50; the PURITY L50 product data sheet DL2-13351.pdf (last reviewed May 2020) prints no CCS; the cited compare page could not be retrieved (bot protection). The L35-L65 table in both editions has no Cold Crank Simulator row, so no CCS value is published for PURITY L50; ccs is now Missing. The values were not copied to any other record. Confirm with Petro-Canada whether a CCS value exists for PURITY L50.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group II' (Reported) citing Petro-Canada's ILMA Engage base-oils brochure (https://petrocanadalubricants.com/-/media/pdfs/brochures/base-oils/ilma-engage-sponsorship-base-oils-brochure.ashx, no page), printed_text 'PURITY L50 listed under GROUP II TYPICAL PROPERTIES'. That brochure could not be retrieved (Petro-Canada blocks automated access; no Wayback Machine copy; the distributor-hosted 'World-Class Base Oils' copy is also blocked), so no grade-level classification of PURITY L50 could be inspected. Petro-Canada's LUB3213E editions (2015.07 = DL2-10020.pdf p.1; 2023.03 p.1) describe PURITY only as 'Group II and Group II+ base oils' at brand level, which does not classify an individual grade; the field is now Missing. Obtain the brochure or a grade-specific Petro-Canada document to confirm.
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-10020.pdf p.2 (2015-07): -6 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Pour Point, °C: -12 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints -12 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): 151 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 152 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 152 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Viscosity index, sulfur, Noack and CCS are not reported for L50 in the cited brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.
- **Conflict (tier3)** [edition difference] `tier3.saturates`: DL2-10020.pdf p.2 (2015-07): 98.5%; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): % Saturates: 97.7 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 97.7 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier3)** [edition difference] `tier3.aromatics`: DL2-10020.pdf p.2 (2015-07): 1.5%; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): % Aromatics: 2.3 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 2.3 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).

## 182. PETRO_CANADA_PURITY_L60
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 10.2 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 9.61 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 9.61 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 2.4 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 2.51 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 2.51 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-10020.pdf p.2 (2015-07): 87; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity Index: 80 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 80 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.density`: DL2-10020.pdf p.2 (2015-07): 0.85 kg/L; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Density @ 15°C, kg/L: 0.86 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 0.86 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Not verified (2026-10 audit): the grade-level brochure cited for API Group II could not be retrieved; the field is Missing (see the API Group question). Previous note: 'API Group II verified from Petro-Canada's official World-Class Base Oils brochure; the original 2015 brochure did not explicitly classify L60.'
- (tier1) Sulfur, Noack, saturates, aromatics and CCS are not reported for L60 in the cited brochure.
- (tier1) Grade-specific SDS and other brochure editions require reconciliation.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group II' (Reported) citing Petro-Canada's ILMA Engage base-oils brochure (https://petrocanadalubricants.com/-/media/pdfs/brochures/base-oils/ilma-engage-sponsorship-base-oils-brochure.ashx, no page), printed_text 'PURITY L60 listed in GROUP II TYPICAL PROPERTIES table'. That brochure could not be retrieved (Petro-Canada blocks automated access; no Wayback Machine copy; the distributor-hosted 'World-Class Base Oils' copy is also blocked), so no grade-level classification of PURITY L60 could be inspected. Petro-Canada's LUB3213E editions (2015.07 = DL2-10020.pdf p.1; 2023.03 p.1) describe PURITY only as 'Group II and Group II+ base oils' at brand level, which does not classify an individual grade; the field is now Missing. Obtain the brochure or a grade-specific Petro-Canada document to confirm.
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-10020.pdf p.2 (2015-07): -27 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Pour Point, °C: -21 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints -21 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): 171 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 178 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 178 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier2) Individual API group not explicitly assigned in supplier family brochure.

## 183. PETRO_CANADA_PURITY_L65
- **Conflict (tier1)** Viscosity index differs between manufacturer documents: DL2-10020.pdf (2015-07), page 2, reports 92; Petro-Canada's World-Class Base Oils brochure reports 104. The original value of 92 is retained pending reconciliation.
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-10020.pdf p.2 (2015-07): 9.5 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 40°C, cSt: 9.33 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 9.33 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-10020.pdf p.2 (2015-07): 2.6 cSt; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity @ 100°C, cSt: 2.57 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 2.57 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-10020.pdf p.2 (2015-07): 92; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Viscosity Index: 104 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 104 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Not verified (2026-10 audit): the grade-level brochure cited for API Group II could not be retrieved; the field is Missing (see the API Group question). Previous note: 'API Group II confirmed for PURITY L65 using Petro-Canada's official World-Class Base Oils brochure.'
- (tier1) No grade-specific CCS measurement has been verified for PURITY L65.
- (tier1) Noack volatility and grade-specific SDS require further verification.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group II' (Reported) citing Petro-Canada's ILMA Engage base-oils brochure (https://petrocanadalubricants.com/-/media/pdfs/brochures/base-oils/ilma-engage-sponsorship-base-oils-brochure.ashx, no page), printed_text 'PURITY L65 listed in GROUP II TYPICAL PROPERTIES table'. That brochure could not be retrieved (Petro-Canada blocks automated access; no Wayback Machine copy; the distributor-hosted 'World-Class Base Oils' copy is also blocked), so no grade-level classification of PURITY L65 could be inspected. Petro-Canada's LUB3213E editions (2015.07 = DL2-10020.pdf p.1; 2023.03 p.1) describe PURITY only as 'Group II and Group II+ base oils' at brand level, which does not classify an individual grade; the field is now Missing. Obtain the brochure or a grade-specific Petro-Canada document to confirm.
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-10020.pdf p.2 (2015-07): -30 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Pour Point, °C: -42 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints -42 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-10020.pdf p.2 (2015-07): 177 °C; https://petrocanadalubricants.com/-/media/pdfs/brochures/purity/purity-base-oil_lub3213e.ashx p.2 (2023-03): Flash Point, COC, °C: 185 — Document editions differ: the recorded value comes from the cited document; Petro-Canada LUB3213E / IM-1809E (2023.03) p.2 prints 185 (copy read from the distributor-hosted mirror https://mascherpa.it/wp-content/uploads/2025/06/Purity-Base-oil_LUB3213E.pdf, because the Petro-Canada server blocks automated retrieval). The recorded value is kept; not resolved (2026-10 audit).
- (tier2) Individual API group not explicitly assigned in supplier family brochure.
- (tier2) Noack and CCS are not reported for L65 in the cited brochure.
- (tier2) Grade-specific SDS and other brochure editions require reconciliation.

## 184. PETRO_CANADA_PURITY_VHVI_2
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Cross-check duplicate supplier brochure files DL2-11262.pdf through DL2-11265.pdf and any grade-specific SDS during final audit.

## 185. PETRO_CANADA_PURITY_VHVI_3
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Confirm against grade-specific SDS and other brochure editions during final audit.

## 186. PETRO_CANADA_PURITY_VHVI_4
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Confirm against grade-specific SDS and other brochure editions during final audit.

## 187. PETRO_CANADA_PURITY_VHVI_6
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Confirm against grade-specific SDS and other brochure editions during final audit.

## 188. PETRO_CANADA_PURITY_VHVI_8
- (tier1) Group III classification and chemistry are supplier family-level descriptions, not individual grade assay.
- (tier1) Confirm against grade-specific SDS and other brochure editions during final audit.

## 189. SHELL_RISELLA_X_415
- **Conflict (tier1)** [conflicting values between different documents] `density`: {"tds": {"value": 806, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13728.pdf", "page": 1}, "sds": {"value": 803.5, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13729.pdf", "page": 8, "revision_date": "2018-10-26"}, "note": "Different reported values at same temperature; TDS selected as primary, SDS retained for reconciliation."}
- (tier1) [History] Shell identifies Risella X 415 as a GTL-derived technical white/process oil, but no explicit grade-specific API base-oil Group classification has been verified. API Group remains Missing. Superseded: the api_group status in this record is 'Not Required' (TDS DL2-13728.pdf p.1 prints 'GtL Technical White Oil' and 'Purity Requirements for Technical White Oil FDA 178.3620 (b) Pass'), the same treatment as tier 2 and Risella X 420/430; the sentence 'API Group remains Missing' contradicted it (2026-10 audit). No grade-specific API Group is printed; the Not Required classification still awaits confirmation of the project applicability rule.
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

## 190. SHELL_RISELLA_X_420
- **Conflict (tier1)** [conflicting values between different documents] `density`: {"tds": {"value": 816, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13726.pdf", "page": 1, "revision_date": "2014-06-02"}, "sds": {"value": 813.8, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13730.pdf", "page": 8, "revision_date": "2018-10-26"}, "note": "Different supplier-reported values at same temperature; TDS retained as primary, SDS separately documented."}
- (tier1) Shell Risella X 420 is described as a GTL-derived process oil. API lubricant base-oil Group classification is treated as Not Required under the proposed project applicability rule; confirm this interpretation is accepted by the professor's template.
- (tier1) Chemistry is recorded from TDS DL2-13726.pdf, page 1, dated 2014-06-02: GTL-derived hydrocarbon fluid, highly saturated with a high degree of iso-paraffinic structures.
- (tier1) CCS viscosity is treated as Not Required for the documented process-oil application. No grade-specific CCS viscosity or test temperature is reported in the supplied TDS.
- (tier1) TDS DL2-13726.pdf reports density of 816 kg/m3 at 15°C, whereas SDS DL2-13730.pdf reports 813.8 kg/m3 at 15°C. The discrepancy requires reconciliation.
- (tier1) The historical TDS is dated 2014-06-02 and the cited SDS was revised 2018-10-26. Confirm applicable document revisions before final approval.
- (tier2) Shell Risella X 420 is marketed as a GTL-derived process oil. API lubricant base-oil Group classification is treated as Not Required under the proposed project applicability rule; confirm this interpretation is accepted by the professor's template.
- (tier2) MRV low-temperature pumpability testing is treated as Not Required for the documented process-oil application. No grade-specific MRV apparent viscosity, yield stress, or test temperature is reported in the supplied TDS.
- (tier2) Noack volatility is reported as 12 mass% at 250°C for 1 hour, ASTM D5800, in TDS DL2-13726.pdf.
- (tier3) API group not explicitly stated; GTL origin is not a supplier API group declaration.
- (tier3) TDS density 816 kg/m3 at 15 C versus SDS DL2-13730.pdf p.8 813.8 kg/m3 at 15 C; verify revisions and reconcile.
- (tier3) Confirm latest TDS/SDS editions before final approval.

## 191. SHELL_RISELLA_X_430
- **Conflict (tier1)** [conflicting values between different documents] `density`: {"tds": {"value": 828, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13727.pdf", "page": 1, "revision_date": "2014-06-02"}, "sds": {"value": 824.8, "unit": "kg/m3", "temperature_c": 15, "source_file": "DL2-13731.pdf", "page": 7, "revision_date": "2020-01-13"}, "note": "Different supplier-reported values at same temperature; TDS retained as primary, SDS separately documented."}
- (tier1) Shell Risella X 430 is described as a GTL-derived process oil. API lubricant base-oil Group classification is treated as Not Required under the proposed project applicability rule; confirm acceptance of this classification with the professor.
- (tier1) Chemistry is recorded from TDS DL2-13727.pdf, page 1, dated 2014-06-02: GTL-derived hydrocarbon fluid, highly saturated with a high degree of iso-paraffinic structures.
- (tier1) CCS cold-cranking viscosity is treated as Not Required for the documented process-oil application. No grade-specific CCS viscosity, test method, or test temperature is provided in the supplied TDS.
- (tier1) TDS DL2-13727.pdf reports density of 828 kg/m3 at 15°C, whereas SDS DL2-13731.pdf reports 824.8 kg/m3 at 15°C. The discrepancy requires reconciliation.
- (tier1) The historical TDS is dated 2014-06-02 and the cited SDS was revised 2020-01-13. Confirm applicable document revisions before final approval.
- (tier2) Shell Risella X 430 is described as a GTL-derived process oil. API lubricant base-oil Group classification is treated as Not Required under the proposed project applicability rule; confirm acceptance of this interpretation with the professor.
- (tier2) MRV low-temperature pumpability testing is treated as Not Required for the documented process-oil application. No grade-specific MRV apparent viscosity, yield stress, or test temperature is reported in the supplied TDS.
- (tier2) Noack volatility is reported as 2.0 mass% at 250°C for 1 hour, ASTM D5800, in TDS DL2-13727.pdf.
- (tier3) API group not explicitly stated; GTL origin is not a supplier API group declaration.
- (tier3) TDS density 828 kg/m3 at 15 C versus SDS DL2-13731.pdf p.7 824.8 kg/m3 at 15 C; verify revisions and reconcile.
- (tier3) Confirm latest TDS/SDS editions before final approval.

## 192. S_OIL_ARAMCO_ULTRA_8
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-14611.pdf p.2 (2018-09-07): 42.0 - 55.0 cSt @ 40°C (ASTM D 445); https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 40℃, cSt (D445): 41.1 — Document editions differ for aramcoULTRA 8: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 41.1. The recorded value is kept; not resolved (2026-10 audit).
- (tier1) API group not explicitly specified in the original 2018 SDS.
- (tier1) The original SDS reports viscosity ranges; S-OIL's official technical specifications provide additional typical properties.
- (tier1) Verify whether the SDS relative density 0.847 at 15°C is dimensionless relative density rather than absolute mass density; do not silently convert.
- (tier1) CCS viscosity of 6,300 mPa.s at -30°C (ASTM D5293) was obtained from S-OIL's official technical specifications, not the original SDS.
- (tier1) Final source-level audit and alternate document reconciliation pending.
- (tier2) API group not explicitly specified in the original SDS.
- (tier2) The original SDS reports viscosity ranges; additional typical properties are available in Aramco's grade-specific technical datasheet.
- (tier2) MRV viscosity and its test temperature are not reported in the reviewed manufacturer technical specifications.
- (tier3) API group not explicitly specified in the source SDS.
- (tier3) A grade-specific TDS with typical values should be located; the SDS reports ranges only.

## 193. S_OIL_PREMIUM_P_20
- (tier1) API Group and chemistry (2026-10 audit): both Tier 1 values were attributed to sources for a different product, aramcoULTRA 8, and are now Missing. Former API Group: 'Group III' (Reported), cited to the Aramco base-oil catalog 2024 p.25, which is the aramcoULTRA slate table for grades 4/6/8 and does not list P-20 or any Premium-series grade; former note: 'Group III explicitly confirmed for aramcoULTRA 8 in Aramco's official 2024 base-oil catalog. The original 2018 SDS did not state the API Group.' Former chemistry: 'Distillates (petroleum), hydrotreated heavy paraffinic' (Reported; printed text 'Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7; purity 100%'), cited to DL2-14611.pdf p.1, the SDS for 'Base Oil aramcoULTRA 8 (250 Neutral)' revised 2018-09-07. Former open question: 'API Group III confirmed for aramcoULTRA 8 using Aramco's official 2024 base-oil catalog; classification was not explicitly stated in the original 2018 SDS.' No reviewed document states the API Group or chemistry of P-20; the Premium Series sheet DL2-11173.pdf names neither. Confirm both with S-OIL.
- (tier1) S-OIL's official Premium Series catalog reports specific gravity 0.8520 at 15/4°C (ASTM D1298), but absolute density remains unverified.
- (tier1) No grade-specific CCS viscosity or test temperature was verified for P-20.
- (tier1) Grade-specific SDS and additional technical documentation require reconciliation.
- (tier2) API group not explicitly specified in reviewed Premium Series datasheets.
- (tier2) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics not reported in the reviewed product sheets.
- (tier2) Final source-level audit and grade-specific SDS reconciliation pending.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for S-OIL P-20 (Premium 100N); no test temperature or ASTM D4684 measurement is available in the reviewed documentation.

## 194. S_OIL_PREMIUM_P_31
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

## 195. S_OIL_PREMIUM_P_480
- (tier1) Historical P-480 (150BS) API Group has not been explicitly verified in the reviewed manufacturer documents.
- (tier1) Chemistry confirmed using S-OIL Premium-480 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic, CAS 64742-57-0, purity 100%.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed as absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature was verified.
- (tier1) Noack volatility, saturates and aromatics remain unverified.
- (tier1) Final source-level reconciliation between the original product datasheet and grade-specific SDS pending.
- (tier2) Historical P-480 (150BS) API Group remains unverified.
- (tier2) Chemistry identified in S-OIL's Premium-480 SDS revised 2015-06-10; grade-specific composition should be reconciled with the original product datasheet.
- (tier2) MRV viscosity and MRV yield stress have not been verified for P-480; no grade-specific test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier2) Final source-level audit and SDS reconciliation pending.
- (tier3) API group not explicitly specified in reviewed Premium Series datasheet.
- (tier3) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier3) Noack volatility, CCS viscosity, saturates and aromatics not reported in the reviewed product sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

## 196. S_OIL_PREMIUM_P_8
- (tier1) API Group classification for historical S-OIL P-8 (Premium 60N) has not been explicitly verified.
- (tier1) Chemistry confirmed in S-OIL Premium-8 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8; purity 100%.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed as absolute density.
- (tier1) No grade-specific CCS viscosity or test temperature has been verified for P-8.
- (tier1) Noack volatility, saturates and aromatics remain unverified.
- (tier1) Final source-level reconciliation between the original product datasheet and grade-specific SDS pending.
- (tier2) API Group for historical S-OIL P-8 (Premium 60N) remains unverified.
- (tier2) Chemistry identified in S-OIL Premium-8 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8.
- (tier2) MRV viscosity and MRV yield stress have not been verified for P-8; no grade-specific test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier3) API group and chemistry not explicitly specified in reviewed Premium Series datasheet.
- (tier3) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier3) Noack volatility, CCS viscosity, saturates and aromatics not reported in reviewed product sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

## 197. S_OIL_PREMIUM_P_96
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
- (tier3) API group and chemistry not explicitly specified in reviewed Premium Series datasheet.
- (tier3) Specific gravity (15/4°C) is dimensionless and must not be transcribed as absolute density.
- (tier3) Noack volatility, CCS viscosity, saturates and aromatics not reported in reviewed product sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

## 198. S_OIL_SUPER_S_31
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
- (tier3) API group is not explicitly specified in the reviewed Super Series brochure.
- (tier3) Specific gravity at 15/4 °C is dimensionless and is not an absolute density measurement.
- (tier3) Noack volatility, CCS, saturates, and aromatics are not numerically reported in the reviewed sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

## 199. S_OIL_SUPER_S_8
- (tier1) API Group for historical S-OIL S-8 (Super 60N) has not been explicitly verified.
- (tier1) S-OIL lists a grade-specific Super 8 SDS, but its Section 3 chemical composition and CAS number require direct verification.
- (tier1) Specific gravity 0.8719 at 15/4°C (ASTM D1298) is dimensionless and must not be transcribed as absolute density.
- (tier1) The original datasheet prints L-40.0 for pour point; the notation requires source-level verification before assigning a numeric value.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified.
- (tier1) Noack volatility, saturates and aromatics remain unverified.
- (tier1) Final reconciliation between DL2-12392.pdf and the grade-specific Super 8 SDS pending.
- (tier2) API Group for historical S-OIL S-8 (Super 60N) remains unverified.
- (tier2) Grade-specific Super 8 SDS composition and CAS number require direct verification.
- (tier2) Pour point is printed as L-40.0 °C (ASTM D5950); qualifier or encoding remains ambiguous. Numeric value deliberately left null. No S-OIL legend defining the 'L' prefix was found in the archived sheets, the S-OIL catalog or the S-OIL web page (2026-10 audit); confirm with S-OIL whether 'L-40.0' means 'below -40.0 °C'.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for S-8; no MRV test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier2) Final reconciliation between DL2-12392.pdf and grade-specific Super 8 SDS pending.
- (tier3) API group not explicitly specified in Super Series brochure.
- (tier3) Specific gravity 15/4°C 0.8719 (ASTM D1298) is dimensionless, not density.
- (tier3) Pour point cell prints L-40.0 (ASTM D5950); unclear if this is a qualifier or character encoding. Numeric pour point deliberately not assigned pending supplier verification.
- (tier3) Noack volatility, CCS, saturates and aromatics not numerically reported.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

## 200. S_OIL_SUPER_S_96
- (tier1) API Group for historical S-OIL S-96 (Super 500N) has not been explicitly verified.
- (tier1) Chemistry confirmed in S-OIL Super-96 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7; purity 100%.
- (tier1) Historical S-OIL catalog reports specific gravity 0.8762 at 15/4°C (ASTM D1298), not an absolute density measurement.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for historical S-96; modern aramcoPRIMA 500 measurements must not be substituted.
- (tier1) Noack volatility, saturates and aromatics remain unverified.
- (tier1) Final source-level reconciliation between DL2-12392.pdf and the grade-specific SDS pending.
- (tier2) Chemistry identified in S-OIL Super-96 SDS revised 2015-06-10: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7.
- (tier2) Historical S-OIL catalog reports specific gravity 0.8762 at 15/4°C (ASTM D1298), which must not be transcribed directly as absolute density.
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for historical S-96; no grade-specific test temperature is available.
- (tier2) Noack volatility, CCS viscosity, saturates and aromatics remain unverified.
- (tier3) API group is not explicitly specified in the reviewed Super Series brochure.
- (tier3) Specific gravity at 15/4 °C is dimensionless and is not an absolute density measurement.
- (tier3) Noack volatility, CCS, saturates, and aromatics are not numerically reported in the reviewed sheet.
- (tier3) Final source-level audit and grade-specific SDS reconciliation pending.

## 201. S_OIL_ULTRA_S_2
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-11177.pdf p.1: 7.117 cSt @40°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 40℃, cSt (D445): 7.62 — Document editions differ for Ultra-S 2: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 7.62. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-11177.pdf p.1: 2.174 cSt @100°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 100℃, cSt (D445): 2.25 — Document editions differ for Ultra-S 2: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 2.25. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-11177.pdf p.1: 109; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Viscosity Index (D2270): 103 — Document editions differ for Ultra-S 2: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 103. The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Chemistry is recorded from SDS DL2-15235.pdf, Section 3: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 2.
- (tier1) Noack volatility is marked with a dash in the Ultra-S 2 column and must remain Missing.
- (tier1) Final source-level reconciliation between DL2-11177.pdf and DL2-15235.pdf remains pending.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); S-OIL states Ultra-S and aramcoULTRA have the same properties'; note 'Classification supported by manufacturer-published Ultra-S/aramcoULTRA equivalence; not directly stated in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 2 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 2 and aramcoULTRA 2 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.24 lists aramcoULTRA 2 as API Base Oil Category Group II, and p.23 states 'These grades of aramcoULTRA are not classified as API Group III' for aramcoULTRA 2 and 3 (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Documentation discrepancy, not a conflict between Ultra-S specifications: the S-OIL page labels the aramcoULTRA brand as a whole 'aramcoULTRA (Group Ⅲ)', whereas the Aramco catalog classifies the aramcoULTRA 2 grade as Group II. Neither document classifies Ultra-S 2. Confirm the API Group of Ultra-S 2 with S-OIL.
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-11177.pdf p.1: -37.5 °C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Pour Point, ℃ (D5950/6749): -36 — Document editions differ for Ultra-S 2: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints -36. The recorded value is kept; not resolved (2026-10 audit).
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for Ultra-S 2; no grade-specific MRV test temperature is available.
- (tier2) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15235.pdf remains pending.
- (tier3) API group not explicitly specified in the reviewed Ultra-S series brochure.
- (tier3) Specific gravity 15/4 °C is dimensionless and is not absolute density.
- (tier3) Noack volatility is marked with a dash in the Ultra-S 2 column, and must remain Missing.
- (tier3) SDS DL2-15235.pdf revised June 10, 2015; final source-level audit pending.

## 202. S_OIL_ULTRA_S_3
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-11177.pdf p.1: 13.47 cSt @40°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 40℃, cSt (D445): 14.0 — Document editions differ for Ultra-S 3: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 14.0. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-11177.pdf p.1: 3.315 cSt @100°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 100℃, cSt (D445): 3.38 — Document editions differ for Ultra-S 3: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 3.38. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-11177.pdf p.1: 117; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Viscosity Index (D2270): 115 — Document editions differ for Ultra-S 3: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 115. The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Chemistry is recorded from SDS DL2-15236.pdf, Section 3: Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-55-8. Final source-level verification remains pending.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) No grade-specific CCS viscosity or CCS test temperature has been verified for Ultra-S 3.
- (tier1) Noack volatility is marked with a dash in the Ultra-S 3 column and must remain Missing.
- (tier1) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15236.pdf remains pending.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); S-OIL states Ultra-S and aramcoULTRA have the same properties'; note 'Classification supported by manufacturer-published Ultra-S/aramcoULTRA equivalence; not directly stated in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 3 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 3 and aramcoULTRA 3 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.24 lists aramcoULTRA 3 as API Base Oil Category Group II, and p.23 states 'These grades of aramcoULTRA are not classified as API Group III' for aramcoULTRA 2 and 3 (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Documentation discrepancy, not a conflict between Ultra-S specifications: the S-OIL page labels the aramcoULTRA brand as a whole 'aramcoULTRA (Group Ⅲ)', whereas the Aramco catalog classifies the aramcoULTRA 3 grade as Group II. Neither document classifies Ultra-S 3. Confirm the API Group of Ultra-S 3 with S-OIL.
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-11177.pdf p.1: 204 °C (COC); https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Flash Point, COC, ℃ (D92): 202 — Document editions differ for Ultra-S 3: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 202. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-11177.pdf p.1: -25.0 °C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Pour Point, ℃ (D5950/6749): -27 — Document editions differ for Ultra-S 3: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints -27. The recorded value is kept; not resolved (2026-10 audit).
- (tier2) MRV apparent viscosity and MRV yield stress have not been verified for Ultra-S 3; no grade-specific MRV test temperature is available.
- (tier3) API group not explicitly specified in the reviewed Ultra-S series brochure.
- (tier3) Specific gravity 15/4 °C is dimensionless and is not absolute density.
- (tier3) Noack volatility is marked with a dash in the Ultra-S 3 column and remains Missing.
- (tier3) SDS DL2-15236.pdf revised June 10, 2015; final source-level audit pending.

## 203. S_OIL_ULTRA_S_4
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-11177.pdf p.1: 19.62 cSt @40°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 40℃, cSt (D445): 19.7 — Document editions differ for Ultra-S 4: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 19.7. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-11177.pdf p.1: 4.247 cSt @100°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 100℃, cSt (D445): 4.27 — Document editions differ for Ultra-S 4: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 4.27. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-11177.pdf p.1: 123; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Viscosity Index (D2270): 124 — Document editions differ for Ultra-S 4: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 124. The recorded value is kept; not resolved (2026-10 audit).
- (tier1) S-OIL Ultra-S 4 SDS revised 2015-06-10 reports Distillates (petroleum), hydrotreated light paraffinic; CAS 64742-54-7; purity 100%. The printed description and CAS number appear inconsistent and require supplier clarification.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) CCS for Ultra-S 4 is recorded in Tier 1 as 1,500 mPa.s at -30 °C (ASTM D5293) from the current S-OIL Lube Base Oil web page; the archived 2009 sheet DL2-11177.pdf prints no CCS (2026-10 audit).
- (tier1) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15139.pdf remains pending.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); S-OIL states Ultra-S and aramcoULTRA have the same properties'; note 'Classification supported by manufacturer-published Ultra-S/aramcoULTRA equivalence; not directly stated in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 4 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 4 and aramcoULTRA 4 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.25 lists aramcoULTRA 4 as API Base Oil Category Group III (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Confirm the API Group of Ultra-S 4 with S-OIL.
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-11177.pdf p.1: 228 °C (COC); https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Flash Point, COC, ℃ (D92): 220 — Document editions differ for Ultra-S 4: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 220. The recorded value is kept; not resolved (2026-10 audit).
- (tier2) SDS DL2-15139.pdf, revised 2015-06-10, reports 'Distillates (petroleum), hydrotreated light paraffinic' with CAS 64742-54-7. The printed description and CAS number appear inconsistent and require supplier clarification.
- (tier2) MRV apparent viscosity, MRV yield stress, and MRV test temperature have not been verified for Ultra-S 4.
- (tier3) API group not explicitly specified in reviewed supplier documents.
- (tier3) Specific gravity 15/4 °C is dimensionless and is not absolute density.
- (tier3) SDS DL2-15139.pdf revised June 10, 2015; final source-level audit pending.

## 204. S_OIL_ULTRA_S_6
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-11177.pdf p.1: 33.32 cSt @40°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 40℃, cSt (D445): 32.54 — Document editions differ for Ultra-S 6: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 32.54. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-11177.pdf p.1: 6.0 cSt @100°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 100℃, cSt (D445): 6.04 — Document editions differ for Ultra-S 6: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 6.04. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-11177.pdf p.1: 127; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Viscosity Index (D2270): 134 — Document editions differ for Ultra-S 6: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 134. The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Chemistry is recorded from SDS DL2-15237.pdf, Section 3: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7. Final source-level verification remains pending.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) CCS for Ultra-S 6 is recorded in Tier 1 as 3,850 mPa.s at -30 °C (ASTM D5293) from the current S-OIL Lube Base Oil web page; the archived 2009 sheet DL2-11177.pdf prints no CCS (2026-10 audit).
- (tier1) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15237.pdf remains pending.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); S-OIL states Ultra-S and aramcoULTRA have the same properties'; note 'Classification supported by manufacturer-published Ultra-S/aramcoULTRA equivalence; not directly stated in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 6 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 6 and aramcoULTRA 6 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.25 lists aramcoULTRA 6 as API Base Oil Category Group III (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Confirm the API Group of Ultra-S 6 with S-OIL.
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-11177.pdf p.1: 235 °C (COC); https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Flash Point, COC, ℃ (D92): 240 — Document editions differ for Ultra-S 6: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 240. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-11177.pdf p.1: -20.0 °C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Pour Point, ℃ (D5950/6749): -16 — Document editions differ for Ultra-S 6: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints -16. The recorded value is kept; not resolved (2026-10 audit).
- (tier2) MRV apparent viscosity, MRV yield stress, and MRV test temperature have not been verified for Ultra-S 6.
- (tier3) API group not explicitly specified in reviewed supplier documents.
- (tier3) Specific gravity 15/4 °C is dimensionless and is not absolute density.
- (tier3) SDS DL2-15237.pdf revised June 10, 2015; final source-level audit pending.

## 205. S_OIL_ULTRA_S_8
- **Conflict (tier1)** [edition difference] `tier1.kv40`: DL2-11177.pdf p.1: 43.89 cSt @40°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 40℃, cSt (D445): 41.1 — Document editions differ for Ultra-S 8: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 41.1. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.kv100`: DL2-11177.pdf p.1: 7.234 cSt @100°C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Kinematic Viscosity @ 100℃, cSt (D445): 7.1 — Document editions differ for Ultra-S 8: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 7.1. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier1)** [edition difference] `tier1.viscosity_index`: DL2-11177.pdf p.1: 127; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Viscosity Index (D2270): 134 — Document editions differ for Ultra-S 8: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 134. The recorded value is kept; not resolved (2026-10 audit).
- (tier1) Chemistry is recorded from SDS DL2-15238.pdf, Section 3: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7. The SDS revision date is recorded as 2015-06-10.
- (tier1) Specific gravity at 15/4°C is dimensionless and must not be transcribed directly as absolute density.
- (tier1) CCS for Ultra-S 8 is recorded in Tier 1 as 6,300 mPa.s at -30 °C (ASTM D5293) from the current S-OIL Lube Base Oil web page; the archived 2009 sheet DL2-11177.pdf prints no CCS (2026-10 audit).
- (tier1) Final source-level reconciliation between DL2-11177.pdf and SDS DL2-15238.pdf remains pending.
- (tier1) API Group (2026-10 audit): previously recorded as 'Group III' (Reported, no source; printed_text 'aramcoULTRA (Group III); Ultra-S and aramcoULTRA are stated by S-OIL to have the same quality'; note 'API Group III supported by official manufacturer product-family classification and equivalence; not directly printed in the historical grade-specific SDS.'). No archived or public S-OIL document classifies Ultra-S 8 directly, so the field is now Missing. Indirect evidence only, not a classification of Ultra-S: (1) S-OIL states 'Ultra-S base oil is S-OIL's own brand product and has the same properties with armcoULTRA base oil' and lists identical typical properties for Ultra-S 8 and aramcoULTRA 8 (https://www.s-oil.com/en/energy/LubeBaseOil.aspx, undated, retrieved 2026-10-21); (2) the Aramco base-oil catalog 2024 p.25 lists aramcoULTRA 8 as API Base Oil Category Group III (https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf). Confirm the API Group of Ultra-S 8 with S-OIL.
- **Conflict (tier2)** [edition difference] `tier2.flash_point`: DL2-11177.pdf p.1: 256 °C (COC); https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Flash Point, COC, ℃ (D92): 250 — Document editions differ for Ultra-S 8: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints 250. The recorded value is kept; not resolved (2026-10 audit).
- **Conflict (tier2)** [edition difference] `tier2.pour_point`: DL2-11177.pdf p.1: -15.0 °C; https://www.s-oil.com/en/energy/LubeBaseOil.aspx: Pour Point, ℃ (D5950/6749): -14 — Document editions differ for Ultra-S 8: the recorded value comes from the cited archive/older document; the current S-OIL Lube Base Oil web page (typical properties, undated, retrieved 2026-10-21) prints -14. The recorded value is kept; not resolved (2026-10 audit).
- (tier2) API Group is not printed in any reviewed S-OIL document for Ultra-S 8; the Tier 1 API Group is Missing (2026-10 audit). S-OIL's published Ultra-S/aramcoULTRA equivalence and the Aramco catalog classification of aramcoULTRA 8 are indirect evidence only; see the Tier 1 open questions.
- (tier2) Chemistry is recorded from SDS DL2-15238.pdf, Section 3: Distillates (petroleum), hydrotreated heavy paraffinic; CAS 64742-54-7; revision date 2015-06-10.
- (tier2) No grade-specific MRV apparent viscosity, MRV yield stress, or MRV test temperature has been verified for Ultra-S 8.
- (tier2) CCS (6,300 mPa.s at -30 °C) and density (0.8425 kg/L at 15.6 °C) for Ultra-S 8 are recorded in Tier 1 from the current S-OIL Lube Base Oil web page, with that source stated; differences between that table and the archived sheets are listed as conflicts (2026-10 audit).
- (tier2) Final reconciliation between historical product data sheet DL2-11177.pdf, SDS DL2-15238.pdf, and current manufacturer product information remains pending.
- (tier3) API group not explicitly specified in reviewed supplier documents.
- (tier3) Specific gravity (15/4 °C) is dimensionless and not absolute density.
- (tier3) Grade-specific SDS DL2-15238.pdf revised June 10, 2015; final source-level audit pending.

## 206. YUBASE_3
- (tier1) [Resolved] Resolved (2026-10 audit): SK's official YUBASE site states that YUBASE-3 and YUBASE-L3 are Group II because their VI is below 120 (archived 'Performance' page, 2010 and 2019 snapshots), consistent with SK's 2000 paper and the January 2021 offering circular (p.52). SK Enmove's current page groups YUBASE under 'Group III/III+' only at brand level. Previous note: 'Resolve the YUBASE 3 API Group discrepancy between the current SK Enmove manufacturer webpage (Group III product range) and the January 2021 SK corporate offering circular, page 52 (YUBASE 3 explicitly listed as Group II).'
- (tier1) Document is headed NARMAK TRADE S.R.O.; confirm manufacturer/supplier relationship with YUBASE-SK.
- (tier1) API group and chemistry are not explicitly stated in this document.
- (tier1) Specific gravity row is printed with unit g/m3, which is inconsistent with the stated value 0,8299; do not interpret as verified density or specific gravity without clarification.
- (tier1) [Resolved] Resolved (2026-10 audit): SK's official YUBASE site states that YUBASE-3 and YUBASE-L3 are Group II because their VI is below 120 (archived 'Performance' page, 2010 and 2019 snapshots), consistent with SK's 2000 paper and the January 2021 offering circular (p.52). SK Enmove's current page groups YUBASE under 'Group III/III+' only at brand level. Previous note: 'API Group (2026-10 audit): recorded as Group II from SK's grade-level statements (2000 conference paper, slide 10; 2021 offering circular, p.52). SK Enmove's current web page groups YUBASE under 'Group III/III+' at brand level. Confirm with SK Enmove that the current YUBASE 3 is still API Group II.'
- (tier2) Confirm the manufacturer and distributor relationship between SK and NARMAK TRADE S.R.O. for archived YUBASE 3.
- (tier2) [Resolved] Resolved (2026-10 audit): Tier 1 records Group II from SK's official YUBASE site, which names YUBASE-3 as Group II (VI below 120). Previous note: 'Resolve the API Group classification of archived YUBASE 3. Current SK Enmove product information presents YUBASE 3 within its Group III range, while a January 2021 SK corporate offering circular explicitly lists YUBASE 3 as Group II.'
- (tier2) The archived property sheet does not explicitly state the product chemistry. Obtain grade-specific manufacturer documentation before assigning a chemistry description.
- (tier2) The specific-gravity entry reports 0.8299 with the questionable unit g/m3. Verify the original units and measurement conditions before recording a density value.
- (tier2) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in DL2-11303.pdf.
- (tier2) Noack volatility is reported as 40 wt% using DIN 51581. The source transcription does not specify a test temperature; do not assume one.
- (tier2) Confirm the archived property sheet's issue date and applicable product revision.

## 207. YUBASE_4
- (tier1) Confirm the manufacturer and distributor relationship between SK Corporation/SK Enmove and NARMAK TRADE S.R.O. for archived YUBASE 4.
- (tier1) API Group III for YUBASE 4 is now sourced to SK's official YUBASE site (archived 'Performance' page: all YUBASE except YUBASE-3/L3 are Group III); SK's 2000 paper agrees. Not stated in the archived NARMAK TRADE sheet. Confirm that the current YUBASE 4 is unchanged (2026-10 audit).
- (tier1) [History] Chemistry is now sourced to SK Lubricants' 2009 YUBASE 4 MSDS (YUB400, archived from yubase.com), which agrees with the 1999 SK Corporation MSDS (2026-10 audit). Previous note: 'Historical SK Corporation YUBASE 4 MSDS No. 739-YU4-02, dated 1999-02-12, identifies the chemistry as hydrotreated heavy paraffinic petroleum distillate (CAS 64742-54-7). Confirm that this historical composition applies to the archived NARMAK TRADE product grade.'
- (tier1) The specific-gravity entry at 15°C is printed as 0.8338 with the inconsistent unit g/m3. Verify the original unit and measurement conditions before assigning a density value.
- (tier1) No grade-specific CCS cold-cranking viscosity, test temperature, or test method is reported in archived property sheet DL2-11304.pdf.
- (tier1) Confirm the issue date of the archived NARMAK TRADE property sheet and whether newer applicable TDS/SDS revisions are available.
- (tier2) Historical SK Corporation YUBASE 4 MSDS No. 739-YU4-02, dated 1999-02-12, identifies hydrotreated heavy paraffinic petroleum distillate (CAS 64742-54-7). Confirm that this composition applies to the archived grade.
- (tier2) The specific-gravity entry at 15°C is printed as 0.8338 with the inconsistent unit g/m3. Verify the original unit and measurement conditions before assigning density.
- (tier2) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in archived property sheet DL2-11304.pdf.
- (tier2) Noack volatility is reported as 15 wt% using DIN 51581. The source transcription does not specify a test temperature; do not assume one.
- (tier2) Confirm the archived property sheet's issue date and applicable product revision.
- (tier3) Document is headed NARMAK TRADE S.R.O.; confirm manufacturer/supplier relationship with YUBASE-SK.
- (tier3) API group and chemistry are not explicitly stated in this document.
- (tier3) Specific gravity at 15 °C is printed as 0,8338 with unit g/m3, an inconsistent unit; do not infer density or specific gravity without clarification.

## 208. YUBASE_5
- (tier1) [Open - history included] API Group (2026-10 audit): first recorded as 'III' from a brand-level ZIC statement, then set to Missing because no grade-level evidence was found; now Reported as Group III from SK's official YUBASE site (archived 'Performance' page: all YUBASE except YUBASE-3/L3 are Group III), which also lists YUBASE 5 as an SK grade. Confirm that the archived DL2-11305.pdf grade is the current SK YUBASE 5. Previous note: 'API Group (2026-10 audit): previously recorded as 'III' (Reported) from SK Lubricants' brand-level statement in 'Business with ZIC' (https://www.zic-europe.com/Business_with_ZIC.pdf, p.3: YUBASE is 'a synthetic new generation base oil classified as group III by API'), which does not name YUBASE 5. The brand statement is not used on its own because SK's own 2000 conference paper classes YUBASE-3 as API Group II, so not every YUBASE grade is Group III. No grade-level classification of YUBASE 5 was found, and YUBASE 5 is not in SK Enmove's current YUBASE line-up; the field is now Missing. Confirm the API Group of YUBASE 5 with SK Enmove.'
- (tier1) The API Group is not stated in the archived NARMAK TRADE property sheet DL2-11305.pdf (the earlier note named DL2-11304.pdf, which is the YUBASE 4 sheet) (2026-10 audit).
- (tier1) Historical SK Corporation YUBASE 4 MSDS No. 739-YU4-02, dated 1999-02-12, identifies hydrotreated heavy paraffinic petroleum distillate (CAS 64742-54-7). Confirm that this composition applies to the archived grade.
- (tier1) The specific-gravity entry at 15°C is printed as 0.8363 with the inconsistent unit g/m3. Verify the original unit and measurement conditions before assigning density.
- (tier1) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in archived property sheet DL2-11304.pdf.
- (tier1) Noack volatility is reported as 15 wt% using DIN 51581. The source transcription does not specify a test temperature; do not assume one.
- (tier1) Confirm the archived property sheet's issue date and applicable product revision.
- (tier2) Confirm the manufacturer and distributor relationship between SK Lubricants/SK Enmove and NARMAK TRADE S.R.O. for archived YUBASE 5.
- (tier2) [History] API Group for YUBASE 5 is now Group III in Tier 1 from SK's official YUBASE site (all YUBASE except YUBASE-3/L3 are Group III; YUBASE 5 listed as an SK grade) (2026-10 audit). Previous note: 'API Group for YUBASE 5 is Missing in Tier 1 (2026-10 audit): only brand-level YUBASE statements were found, and SK's own 2000 paper classes YUBASE-3 as Group II, so the brand statement does not establish the grade. Confirm the API Group of archived product DL2-11305.pdf with SK Enmove.'
- (tier2) The archived property sheet does not explicitly report chemical composition. Obtain grade-specific manufacturer SDS documentation before assigning chemistry or a CAS number.
- (tier2) The specific-gravity entry at 15°C is printed as 0.8363 with the inconsistent unit g/m3. Verify the original units and measurement conditions before assigning a density value.
- (tier2) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in archived property sheet DL2-11305.pdf.
- (tier2) Noack volatility is reported as 12 wt% using DIN 51581. The supplied transcription does not specify a test temperature; do not assume one.
- (tier3) Document issued by NARMAK TRADE S.R.O.; confirm manufacturer/supplier relationship with YUBASE-SK.
- (tier3) API group and chemistry are not explicitly stated.
- (tier3) Specific gravity at 15 °C printed as 0,8363 with inconsistent unit g/m3; do not infer density or specific gravity without clarification.

## 209. YUBASE_6
- (tier1) Confirm the manufacturer and distributor relationship between SK Lubricants/SK Enmove and NARMAK TRADE S.R.O. for archived YUBASE 6.
- (tier1) API Group III for YUBASE 6 is now sourced to SK's official YUBASE site (archived 'Performance' page: all YUBASE except YUBASE-3/L3 are Group III); SK's 2000 paper agrees. Not stated in the archived NARMAK TRADE sheet. Confirm that the current YUBASE 6 is unchanged (2026-10 audit).
- (tier1) Chemistry provenance (2026-10 audit): earlier cited to a Scribd upload (https://ru.scribd.com/document/799055322/Global-English-YUBASE-6, uploaded by an unrelated user) described as an SK Lubricants YUBASE 6 SDS dated 2020-01-01 giving 100% distillates (petroleum), hydrotreated heavy paraffinic, CAS 64742-54-7. The Scribd page shows no document content, so that claim could not be verified and is not used. Chemistry is now sourced to the Hilditch Pty Ltd SDS HIL0045 (2021-09-28), which gives the same composition. Obtain SK Enmove's own YUBASE 6 SDS to confirm. Previous note: 'SK Lubricants YUBASE 6 SDS dated 2020-01-01 identifies the chemistry as distillates (petroleum), hydrotreated heavy paraffinic, CAS 64742-54-7, at 100%. Confirm that this SDS applies to the undated archived NARMAK TRADE grade.'
- (tier1) The specific-gravity entry at 15°C is printed as 0.8423 with the inconsistent unit g/m3. Verify the original units and measurement conditions before assigning density.
- (tier1) No grade-specific CCS viscosity, test temperature, or test method is reported in archived property sheet DL2-11306.pdf.
- (tier1) Confirm the archived property sheet's issue date and applicable product revision.
- (tier2) Chemistry provenance (2026-10 audit): earlier cited to a Scribd upload (https://ru.scribd.com/document/799055322/Global-English-YUBASE-6, uploaded by an unrelated user) described as an SK Lubricants YUBASE 6 SDS dated 2020-01-01 giving 100% distillates (petroleum), hydrotreated heavy paraffinic, CAS 64742-54-7. The Scribd page shows no document content, so that claim could not be verified and is not used. Chemistry is now sourced to the Hilditch Pty Ltd SDS HIL0045 (2021-09-28), which gives the same composition. Obtain SK Enmove's own YUBASE 6 SDS to confirm. Previous note: 'A historical SK Lubricants YUBASE 6 SDS dated 2020-01-01 identifies the chemistry as distillates (petroleum), hydrotreated heavy paraffinic, CAS 64742-54-7. Confirm that this SDS applies to the undated archived grade.'
- (tier2) No MRV apparent viscosity, yield stress, test temperature, or test method is reported in archived property sheet DL2-11306.pdf.
- (tier2) Noack volatility is reported as 7 wt% using DIN 51581. The supplied transcription does not specify a test temperature; do not assume one.
- (tier3) Document issued by NARMAK TRADE S.R.O.; confirm manufacturer/supplier relationship with YUBASE-SK.
- (tier3) API group and chemistry are not explicitly stated.
- (tier3) Specific gravity at 15 °C printed as 0,8423 with inconsistent unit g/m3; do not infer density or specific gravity without clarification.

## 210. NYNAS_T_22
- (tier1) API Group is not printed on DL2-12371.pdf (Nynas PDS, issuing date 2012-08-10); left Missing and not inferred from the naphthenic chemistry. Confirm with Nynas.
- (tier1) Viscosity index is not printed; left Missing (not calculated from KV40 22.3 / KV100 3.7 cSt).
- (tier1) No CCS value is printed.
- (tier1) Only one T 22 document is in the archive (DL2-12371.pdf, 2012-08-10); no grade-specific SDS to reconcile. Confirm that this is the current revision.
- (tier1) Printed properties with no template field (DL2-12371.pdf p.1, Min / Max / Typical): Viscosity, 100°F, SUS, D 2161: typical 118; Copper Strip, 3 hrs, D 130: max 1, typical 1; Aniline Point, °C, D 611: 68 / 78 / 75; Refractive Index, 20 °C, D 1747: typical 1.494; Colour, D 1500: max 1.0, typical <0.5; Total Acid Number, mg KOH/g, D 974: max 0.03, typical <0.01; Appearance at 15°C, D 4176: Clear and bright / Clear and bright; DMSO extractible compounds, Wt %, IP 346: max 3.0, typical 2.0.
- (tier2) No Noack volatility or MRV value is printed on DL2-12371.pdf.
- (tier3) Aromatics left Missing: DL2-12371.pdf prints carbon-type data (IR-method C % typical 15; D 2140 C % 10, C_N % 43, C_P % 47), which are not aromatics in wt.%. The subscript of the two 'C' rows is not legible in the scan.
- (tier3) Saturates, cloud point and wax content are not printed.

## 211. NYNAS_T_110
- (tier1) API Group is not printed on DL2-12370.pdf (Nynas PDS for T 110); left Missing and not inferred from the naphthenic chemistry. Confirm with Nynas.
- (tier1) Viscosity index is not printed; left Missing (not calculated from KV40 114 / KV100 8,5 cSt).
- (tier1) No CCS value is printed.
- (tier1) DL2-12370.pdf prints no issuing or revision date, footer or Nynas logo on its single page (the archive register also gives no revision); source revision_date left null. Confirm the document revision with Nynas. No grade-specific SDS is in the archive.
- (tier1) Printed properties with no template field (DL2-12370.pdf p.1, guaranteed Min / Max / Typical, decimal commas as printed): Viscosity, 100°F, SUS, D 2161: typical 612; Copper Strip, 3 hrs, D 130: max 1, typical 1; Aniline Point, °C, D 611: 82 / 90 / 85; Refractive Index, 20 °C, D 1747: typical 1,504; Colour, D 1500: max 1,5, typical <1,0; Total Acid Number, mg KOH/g, D 974: max 0,03, typical <0,01; Appearance at 15°C, D 4176: Clear and bright / Clear and bright; DMSO extractible compounds, Wt %, IP 346: max 3,0, typical 2,0.
- (tier2) No Noack volatility or MRV value is printed on DL2-12370.pdf.
- (tier3) Aromatics left Missing: DL2-12370.pdf prints carbon-type data (IR-method C_A % typical 15; D 2140 C_A % 12, C_N % 40, C_P % 48), which are not aromatics in wt.%.
- (tier3) Saturates, cloud point and wax content are not printed.

## 212. ARAMCO_LUBEREF_PRIMA_150
- (tier1) API Group 'Group II' is taken from the brochure table heading over all eight aramcoPRIMA columns; no grade-specific statement is printed. Confirm with Saudi Aramco / Luberef. [fields: api_group_chemistry.api_group]
- (tier1) Chemistry is not printed on DL2-11773.pdf, and no aramcoPRIMA 150 SDS is in the archive. [fields: api_group_chemistry.chemistry]
- (tier1) All values are brochure typicals; no guaranteed specification for aramcoPRIMA 150 is in the archive (the specification sheet DL2-12172.pdf covers aramcoPRIMA 70, 110, 230 and 500 only). No issuing date is printed; the PDF metadata title 'Base oils Dubai Catalog 27Sep2018 FINALout-LOW' is not a printed date. The issuing company is not named on the page. [fields: kv40, kv100, viscosity_index, density, ccs[]]
- (tier1) Inventory identity notes kept unresolved: the inventory matched this grade to the legacy name 'Aramco Prima 150N' by product name (to confirm with the supplier), and the S-OIL Super S-31 record notes an unverified mapping to aramcoPRIMA 150. No grade is merged. [fields: product]
- (tier1) Printed properties with no template field (DL2-11773.pdf, column 'aramcoPRIMA 150 / Typical'): Appearance, Visual: C&B; Brookfield @ -40°C, D 2983: blank; Saybolt Color, D 156: +30; Color ASTM, D 1500: L 0.5; Copper Corrosion 100°C 3hrs, D 130: 1b; Tan mgKOH/gm, D 974: < 0.01. [fields: (no template field)]
- (tier2) No MRV value is printed on DL2-11773.pdf. [fields: mrv[].mrv_viscosity, mrv[].yield_stress]
- (tier3) Cloud point and wax content are not printed on DL2-11773.pdf. [fields: cloud_point, wax_content]

## 213. ARAMCO_LUBEREF_PRIMA_100
- (tier1) API Group 'Group II' is taken from the brochure table heading over all eight aramcoPRIMA columns (family-level evidence); no grade-specific statement is printed. Confirm with Saudi Aramco / Luberef. [fields: api_group_chemistry.api_group]
- (tier1) Chemistry is not printed on DL2-11773.pdf, and no aramcoPRIMA 100 SDS is in the archive. [fields: api_group_chemistry.chemistry]
- (tier1) All values are brochure typicals; no guaranteed specification for aramcoPRIMA 100 is in the archive (the specification sheet DL2-12172.pdf covers aramcoPRIMA 70, 110, 230 and 500 only). The aramcoPRIMA 100 column carries no '*', so the footnote '*Typicals are subject to confirmation upon startup of the new Group II plant.' does not apply to it. No issuing date is printed; the PDF metadata title 'Base oils Dubai Catalog 27Sep2018 FINALout-LOW' is not a printed date. The issuing company is not named on the page. [fields: kv40, kv100, viscosity_index, density, ccs[]]
- (tier1) The 'Cranking Viscosity @ -20°C' cell of the aramcoPRIMA 100 column is blank; only the -25 °C value (1,300 mPa-s) is printed. [fields: ccs[]]
- (tier1) Printed properties with no template field (DL2-11773.pdf, column 'aramcoPRIMA 100 / Typical'): Appearance, Visual: C&B; Brookfield @ -40°C, D 2983: 12,500 (no unit printed); Saybolt Color, D 156: blank; Color ASTM, D 1500: L 0.5; Copper Corrosion 100°C 3hrs, D 130: 1a; Tan mgKOH/gm, D 974: 0.01. [fields: (no template field)]
- (tier2) No MRV value is printed on DL2-11773.pdf. [fields: mrv[].mrv_viscosity, mrv[].yield_stress]
- (tier2) The Noack volatility cell of the aramcoPRIMA 100 column is blank (neighbouring grades have values); left Missing. [fields: noack_volatility]
- (tier3) Cloud point and wax content are not printed on DL2-11773.pdf. [fields: cloud_point, wax_content]

## 214. ARAMCO_LUBEREF_PRIMA_220
- (tier1) API Group 'Group II' is taken from the brochure table heading, printed at the top left of the pp. 8-9 table and covering all eight aramcoPRIMA columns including aramcoPRIMA 220 on page 9 (family-level evidence); no grade-specific statement is printed. Confirm with Saudi Aramco / Luberef. [fields: api_group_chemistry.api_group]
- (tier1) Chemistry is not printed on DL2-11773.pdf, and no aramcoPRIMA 220 SDS is in the archive. [fields: api_group_chemistry.chemistry]
- (tier1) All values are brochure typicals; no guaranteed specification for aramcoPRIMA 220 is in the archive (the specification sheet DL2-12172.pdf covers aramcoPRIMA 70, 110, 230 and 500 only). The aramcoPRIMA 220 column carries no '*', so the footnote '*Typicals are subject to confirmation upon startup of the new Group II plant.' does not apply to it. No issuing date is printed; the PDF metadata title 'Base oils Dubai Catalog 27Sep2018 FINALout-LOW' is not a printed date. The issuing company is not named on the page. [fields: kv40, kv100, viscosity_index, density, ccs[]]
- (tier1) The 'Cranking Viscosity @ -25°C' cell of the aramcoPRIMA 220 column is blank; only the -20 °C value (3,000 mPa-s) is printed. [fields: ccs[]]
- (tier1) Printed properties with no template field (DL2-11773.pdf, column 'aramcoPRIMA 220 / Typical'): Appearance, Visual: C&B; Color ASTM, D 1500: L 0.5. Blank cells in this column: Brookfield @ -40°C (D 2983), Saybolt Color (D 156), Copper Corrosion 100°C 3hrs (D 130), Tan mgKOH/gm (D 974). [fields: (no template field)]
- (tier2) No MRV value is printed on DL2-11773.pdf. [fields: mrv[].mrv_viscosity, mrv[].yield_stress]
- (tier3) The saturates cell of the aramcoPRIMA 220 column is blank (neighbouring grades have values); left Missing and not derived from the printed aromatics. [fields: saturates]
- (tier3) Cloud point and wax content are not printed on DL2-11773.pdf. [fields: cloud_point, wax_content]

## 215. ARAMCO_LUBEREF_PRIMA_600
- (tier1) API Group 'Group II' is taken from the brochure table heading, printed at the top left of the pp. 8-9 table and covering all eight aramcoPRIMA columns through aramcoPRIMA 600 on page 9 (family-level evidence); no grade-specific statement is printed. Confirm with Saudi Aramco / Luberef. [fields: api_group_chemistry.api_group]
- (tier1) Chemistry is not printed on DL2-11773.pdf, and no aramcoPRIMA 600 SDS is in the archive. [fields: api_group_chemistry.chemistry]
- (tier1) All values are brochure typicals; no guaranteed specification for aramcoPRIMA 600 is in the archive (the specification sheet DL2-12172.pdf covers aramcoPRIMA 70, 110, 230 and 500 only). The aramcoPRIMA 600 column carries no '*' (the adjacent 'aramcoPRIMA 500L*' does), so the footnote '*Typicals are subject to confirmation upon startup of the new Group II plant.' does not apply to it. No issuing date is printed; the PDF metadata title 'Base oils Dubai Catalog 27Sep2018 FINALout-LOW' is not a printed date. The issuing company is not named on the page. [fields: kv40, kv100, viscosity_index, density, ccs[]]
- (tier1) Printed properties with no template field (DL2-11773.pdf, column 'aramcoPRIMA 600 / Typical'): Appearance, Visual: C&B; Color ASTM, D 1500: L 0.5; Copper Corrosion 100°C 3hrs, D 130: 1b; Tan mgKOH/gm, D 974: 0.02. Blank cells in this column: Brookfield @ -40°C (D 2983), Saybolt Color (D 156). [fields: (no template field)]
- (tier2) No MRV value is printed on DL2-11773.pdf. [fields: mrv[].mrv_viscosity, mrv[].yield_stress]
- (tier2) The Noack volatility cell of the aramcoPRIMA 600 column is blank (neighbouring grades have values); left Missing. [fields: noack_volatility]
- (tier3) Cloud point and wax content are not printed on DL2-11773.pdf. [fields: cloud_point, wax_content]

## 216. ARAMCO_LUBEREF_PRIMA_500L
- (tier1) Provisional values: the column heading is printed 'aramcoPRIMA® 500L*', and the '*' refers to the footnote '*Typicals are subject to confirmation upon startup of the new Group II plant.' All aramcoPRIMA 500L values are provisional brochure typicals, not guaranteed specifications or confirmed production values. Obtain confirmed typicals or a specification from Saudi Aramco / Luberef. [fields: kv40, kv100, viscosity_index, density, ccs[], noack_volatility, pour_point, flash_point, sulfur, saturates, aromatics]
- (tier1) API Group 'Group II' is taken from the brochure table heading, printed at the top left of the pp. 8-9 table and covering all eight aramcoPRIMA columns including aramcoPRIMA 500L* on page 9 (family-level evidence); no grade-specific statement is printed. Confirm with Saudi Aramco / Luberef. [fields: api_group_chemistry.api_group]
- (tier1) Chemistry is not printed on DL2-11773.pdf, and no aramcoPRIMA 500L SDS is in the archive. [fields: api_group_chemistry.chemistry]
- (tier1) No guaranteed specification for aramcoPRIMA 500L is in the archive (the specification sheet DL2-12172.pdf covers aramcoPRIMA 70, 110, 230 and 500 only). No issuing date is printed; the PDF metadata title 'Base oils Dubai Catalog 27Sep2018 FINALout-LOW' is not a printed date. The issuing company is not named on the page. [fields: product]
- (tier1) Printed properties with no template field (DL2-11773.pdf, column 'aramcoPRIMA 500L* / Typical', provisional): Appearance, Visual: C&B; Color ASTM, D 1500: L 0.5; Copper Corrosion 100°C 3hrs, D 130: 1b; Tan mgKOH/gm, D 974: 0.02. Blank cells in this column: Brookfield @ -40°C (D 2983), Saybolt Color (D 156). [fields: (no template field)]
- (tier2) Noack, pour point and flash point are provisional typicals under the footnote '*Typicals are subject to confirmation upon startup of the new Group II plant.' [fields: noack_volatility, pour_point, flash_point]
- (tier2) No MRV value is printed on DL2-11773.pdf. [fields: mrv[].mrv_viscosity, mrv[].yield_stress]
- (tier3) Sulfur, saturates and aromatics are provisional typicals under the footnote '*Typicals are subject to confirmation upon startup of the new Group II plant.' [fields: sulfur, saturates, aromatics]
- (tier3) Cloud point and wax content are not printed on DL2-11773.pdf. [fields: cloud_point, wax_content]

## 217. NESTE_NEXBASE_3030
- (tier1) DL2-10962.pdf is a Neste Oil NEXBASE family technical data sheet ('Edition 8') with no calendar revision date; no date inferred. Only the 'NESTE OIL' logo identifies the issuer; no legal entity is printed.
- (tier1) API Group is not printed for NEXBASE 3030: the sheet attributes 'ACEA Group III' only to 'the other grades' (not 3020 and 3030). Left Missing; confirm with Neste.
- (tier1) Chemistry is family-level evidence (the NEXBASE description), not a grade-specific statement.
- (tier1) No test methods are printed in the DL2-10962.pdf table; method left null for every value. No NEXBASE 3030 SDS or grade-specific TDS is in the archive.
- (tier1) Viscosity at 40 °C and density at 15 °C have typical values only (spec printed as '_'). No CCS value is printed; the 'Viscosity at -20 °C' row (kinematic) is '–' for NEXBASE 3030.
- (tier1) Printed properties with no template field (DL2-10962.pdf, column 'Nexbase 3030', Spec / Typ): Appearance: pass / (1), footnote '1) Clear and bright liquid on visual observance'; Colour: ≤ 0.5 / < 0.5 (no scale or method printed); Viscosity at -20 °C, mm²/s: – / –.
- (tier2) Noack volatility is printed as '–' for NEXBASE 3030 (values are given only for 3043-3080); left Missing.
- (tier2) No MRV value is printed on DL2-10962.pdf.
- (tier2) The flash-point method (open or closed cup) is not printed; flash_method left null.
- (tier3) Sulfur, saturates, aromatics, cloud point and wax content are not printed on DL2-10962.pdf.

## 218. FORMOSA_FPCC_70N_GII
- (tier1) Source identity: DL2-12108.jpeg, DL2-12109.jpeg and DL2-12111.jpeg are pixel-identical copies of one image (bytes differ only in embedded EXIF titles 'FORMOSA 500N', '150N' and 'FORMOSA 70N', which are not printed); they count as one source, cited as DL2-12108.jpeg.
- (tier1) The image prints 'FPCC' only (title 'Specification of FPCC API GII Base Oil'); the supplier is recorded as Formosa Petrochemical Corporation per the archive folder and inventory. Confirm with the supplier.
- (tier1) No document revision or issue date is printed. '2017 AUG' appears only in the column heading 'Typical (2017 AUG)' and dates the typical data; revision_date left null.
- (tier1) API Group II is taken from the title covering all three grades (family-level evidence). The typical viscosity index of 70N is 88 and its VI specification is 'Report'.
- (tier1) Chemistry is not printed, and no FPCC 70N SDS is in the archive. No CCS value is printed.
- (tier1) Printed properties with no template field (DL2-12108.jpeg, 70N): Color, max, ASTM D-1500: Specification +0.5, Typical <0.5; Water Content, ppmw, max, ASTM D-6304: Specification 50, Typical 32.60; Appearance, Visual: B & C / B & C ('* B&C - Bright and Clear @ ambient air temperature').
- (tier2) Noack volatility is printed '-' for 70N (specification and typical); left Missing.
- (tier2) No MRV value is printed on DL2-12108.jpeg.
- (tier3) Saturates and aromatics typicals are printed as exactly '100' and '0' wt% (ASTM D-7419), without the '>'/'<' qualifiers used for 150N and 500N ('>99.80', '<0.20'); recorded as printed, not normalized. Confirm with the supplier.
- (tier3) Cloud point and wax content are not printed on DL2-12108.jpeg.

## 219. AFTON_HITEC_12250
- (general) Source: no HiTEC 12250 data sheet is in the archive or was found. All values come from Afton's HiTEC 12204L PDS (printed edition '06/17', © 2017 Afton Chemical Corporation), retrieved as the Internet Archive original-bytes copy captured 2020-10-23 (SHA-256 7a1e57d81d66b52b83215da261732256867d89b651c75334068022362a74183e), p.2 'Typical Characteristics' column 'HiTEC® 12250'. Afton's live site blocks automated access. The archived HiTEC 12200 leaflet DL2-14639.pdf gives only the dose.
- (general) Printed properties with no field in the component template (HiTEC 12204L PDS 06/17, p.2, column 'HiTEC® 12250', typical characteristics): Density, lbs/gal. 7.67; Specific Gravity @ 15.6/15.6°C 0.920; Viscosity @ 100°C, cSt 175; Flash Point, °C (PMCC) 135 min.
- (general) Handling information printed for 'HiTEC® 12204L and HiTEC® 12250' (p.2), no template field: Max Handling Temp: 70˚C; Shelf Life: 3 months @ 45°C, 36 months @ ambient (10-40°C).
- (general) Treat rate: the only dose is 4.2% with 10.3% HiTEC® 12200 to reach HiTEC® 12204L performance (12204L itself: 14.2% wt). The basis of the 4.2% is not printed, and 10.3% + 4.2% = 14.5% differs from the 14.2% 12204L rate; recorded as printed, not reconciled. Confirm with Afton.
- (general) Chemical family, active content, carrier identity/share, compatibility restrictions and Ca, Mg, P, Zn, Mo contents are not printed; left Missing and not inferred from HiTEC 12204L or HiTEC 12200. component_subtype left null (booster, not VM or PPD). Confirm with Afton.

## 220. AFTON_HITEC_5748
- (general) Source: Afton HiTEC 5748 PDS 'HiTEC® 5748 Non-Dispersant Olefin Copolymer Viscosity Modifier', printed edition '05/23' (© 2023 Afton Chemical Corporation; PDF created 2023-07-28), retrieved as the Internet Archive original-bytes copy captured 2024-10-05 (SHA-256 18edefceb198a43701b7eb17544599a71c6137199f6e3967800cf3f6ff0cee3b), p.2. Afton's live site blocks automated access. The archive only names HiTEC 5748 inside other bulletins (DL2-13692.pdf HiTEC 12360, 07/20; DL2-15568.pdf HiTEC 12210M, 04/22).
- (general) Printed typical characteristics with no field in the component templates (PDS 05/23, p.2): Appearance: Clear to slightly hazy greenish tan viscous liquid; Specific Gravity @ 15.6/15.6°C: 0.855; Flash Point, °C (PMCC): 135 min.; Color, ASTM D1500: 3.0 max.; Kinematic Viscosity @ 100˚C, cSt: 1100; Dilute Viscosity @ 100°C, cSt: 11.55 (dilution, reference oil and dose not stated). Handling Information: Max Handling Temp: 250°F (120°C); Shelf Life: 36 months @ 10 – 40 °C.
- (general) Application (PDS 05/23, p.2): 'recommended for use in various Engine Oils, selected Off Road, and Grease applications'; listed uses: licensable PCMO applications from API SL to OEM applications such as MB 229.5, licensable HDEO applications from API CH-4 to OEM applications such as MB 228.51, JASO compliant for MCO applications from API SG to API SN quality, selected off-road applications, and grease applications 'to provide structural stability and reduce soap content'. Recorded here, not as compatibility restrictions; secondary function left Missing.
- (general) Active content, carrier identity/share, compatibility restrictions and TBN/Ca/Mg/P/Zn/Mo are not printed; left Missing and not inferred. The 03/18 edition says the product is based on a solid polymer, but gives no polymer content.
- (general) Older Afton editions retrieved from the Internet Archive (original bytes, not cited as sources): PDS 07/11 (http://www.aftonchemical.com/ProductDataSheets/Engine%20Oil/HiTEC-5748_PDS.pdf, snapshot 2012-05-03, SHA-256 ee8581a8...); PDS 03/18 (HiTEC-5748_PDS_1.pdf, snapshot 2023-02-02, identical to the 2019-07-13 capture, SHA-256 3bfb7f0d...); PDS 04/21 (HiTEC-5748_PDS_2.pdf, snapshot 2023-01-28, SHA-256 f291807c...). Typical characteristics differ between editions (edition differences on properties without a template field): 07/11 Specific Gravity 0.865, Flash Point (PMCC) 155 min., Viscosity @ 40°C 15000 cSt, Viscosity @ 100°C 1140 cSt, Color 5.0 max.; 03/18 0.855, 135 min., 1100 cSt @ 100°C, Color 5.0 max., Thickening Power @ 100°C 6.55; 04/21 and 05/23 0.855, 135 min., 1100 cSt @ 100°C, Color 3.0 max., Dilute Viscosity @ 100°C 11.55 cSt. The recommended dosage table is identical in all four editions. The record uses the 05/23 edition.
- (general) Identity: HiTEC 5748A is a separate Afton grade with its own PDS (HiTEC-5748A_PDS.pdf); it has no inventory row (identity review ID-08). No 5748A data is used here.
- (vm) SSI discrepancy, not reconciled: Afton's HiTEC 5748 PDS prints 'Shear Stability Index %: 22' (05/23 and 04/21) and 'a typical Shear Stability Index (SSI) of 22' (03/18); the 07/11 edition says 'It is based on 23 SSI polymer' (base-polymer basis); Afton's HiTEC 12360 bulletin DL2-13692.pdf (07/20, p.2) describes 'HiTEC® 5748 25SSI OCP' / '25SSI viscosity modifier'. None of these documents prints the SSI test method, cycle count or base oil, so comparability is not established and no conflict entry is recorded. Confirm the SSI and its method with Afton.
- (vm) Treat range: the PDS gives one dosage per SAE grade in vol.% only (10 hour L-38 stay-in-grade, with CMCC DIN 51382 values in parentheses: 5W-30 8.0 (8.0), 10W-30 5.7 (5.8), 10W-40 11.6 (11.8), 15W-40 5.4 (5.5), 20W-50 5.4 (5.5) vol.%). No wt.% dosage and no min/max range are published, so treat_range_wt_pct stays Missing; the vol.% recommendations are kept in external_fill_notes and must not be used as wt.% inputs. Ask Afton for wt.% dosages.
- (vm) Thickening response, post-shear KV100, HTHS, CCS/MRV impact, low-temperature gelation, active polymer content, carrier and dissolution/blend temperature are not printed; left Missing. The printed 'Dilute Viscosity @ 100°C, cSt: 11.55' has no stated reference oil or dose, so it is not entered as a thickening response.

## 221. AFTON_HITEC_12204L
- (tier1) Source: Afton's own HiTEC 12204L PDS 'HiTEC® 12204L HDEO Additive Package', printed edition '06/17' (© 2017 Afton Chemical Corporation; PDF created 2017-06-16), retrieved as the Internet Archive original-bytes copy captured 2020-10-23 (SHA-256 7a1e57d81d66b52b83215da261732256867d89b651c75334068022362a74183e), p.2 (p.1 is the cover). Afton's live site blocks automated access. The same document is the source of AFTON_HITEC_12250. The archive's HiTEC 12200 bulletin DL2-14639.pdf (08/18) prints no HiTEC 12204L properties; it is used only for the premix formula and route context (see below).
- (tier1) Identity (ID-13): the inventory and identity review describe HiTEC 12204L as a premix defined in DL2-14639.pdf. Afton's own PDS presents it as 'HiTEC® 12204L HDEO Additive Package', 'part of the HiTEC 12200 family of products', with its own Typical Characteristics column and treat rate, so it is recorded as a product in its own right. HiTEC 12204Y and HiTEC 12252 are separate inventory materials; nothing from them is used.
- (tier1) Premix formula, not a treat rate: DL2-14639.pdf p.2 (08/18) footnote 1 '14.2% HiTEC® 12204L = 10.3% HiTEC® 12200 + 4.2% HiTEC® 12250', attached to the approvals row '10.3%¹ | 4.2% HiTEC® 12250 | SAE 15W-40 | GP II' (the 05/18 bulletin DL2-11412.PDF p.2 prints the same footnote). The PDS (06/17, p.2) says 'The performance level of HiTEC® 12204L can also be achieved through the use of HiTEC® 12250 booster package at 4.2% in combination with HiTEC® 12200 at 10.3%'. This is an alternative two-product route for SAE 15W-40 (GP II in DL2-14639), equivalent to 14.2% HiTEC® 12204L; it is not a general treat rate or a required co-component of HiTEC® 12204L, so it is recorded here only. 10.3% + 4.2% = 14.5%, not the printed 14.2% (also noted in AFTON_HITEC_12250); recorded as printed, not reconciled. Confirm with Afton.
- (tier1) Claims printed for the equivalent route only: DL2-14639.pdf p.2 (08/18) marks API SL, API SJ and DDC 93K214 in the row '10.3%¹ | 4.2% HiTEC® 12250 | SAE 15W-40 | GP II'. These columns do not exist in the 06/17 PDS approvals band, so they are not added to HiTEC® 12204L's claims and not treated as conflicts (columns absent, not contradicted). Confirm with Afton whether they apply to HiTEC® 12204L.
- (tier1) MAN 3275: the PDS footnote reads '*:Equivalent performance. MAN 3275 now obsolete' (claim_type 'other'); DL2-14639.pdf footnote 5 for the equivalent route reads 'Meets requirements of (MRO)'. The wordings differ but do not contradict each other; not recorded as a conflict.
- (tier1) Deutz labels are recorded as printed in the PDS: 'Deutz DDQ-III' and 'Deutz DCQ-II'. DL2-14639.pdf prints 'Deutz DQC- III' and 'Deutz DQC- II'. Probably the same specifications; not confirmed, not normalized.
- (tier1) Claim type: all 20 columns sit under the printed header 'Approvals', including API CI-4 Plus, API CI-4, API CH-4 and ACEA E7-16, so claim_type = 'approval' (same reading as AFTON_HITEC_12200); MAN 3275 is 'other' (equivalent performance). These are Afton-listed claims (evidence_class 'Supplier claim'): the PDS prints no approval, licence or certificate numbers and no third-party confirmation, so no independent certification is implied. The qualifiers 'p: MB package approval' (MB 228.3) and '*:Equivalent performance. MAN 3275 now obsolete' have no schema field and are kept in each claim's scope. For API CI-4 Plus the text says 'meets the requirements of'. Please confirm this reading.
- (tier1) MB 228.3 approval scope is route-specific (not recorded as a conflict): the PDS (06/17, p.2) marks MB 228.3 'p' ('p: MB package approval') in the row 'API CI-4 Plus | SAE 15W40 | HiTEC® 12204L @ 14.2%', i.e. for HiTEC® 12204L used alone. DL2-14639.pdf (08/18, p.2) shows a plain dot, without 'P' ('MB Package Approval', used in other rows), in the MB 228.3 column of the row '10.3%¹ | 4.2% HiTEC® 12250 | SAE 15W-40 | GP II', i.e. for the two-product combination HiTEC® 12200 + HiTEC® 12250. Footnote 1 ('14.2% HiTEC® 12204L = 10.3% HiTEC® 12200 + 4.2% HiTEC® 12250') and the PDS sentence ('The performance level of HiTEC® 12204L can also be achieved...') state equivalent composition or performance, not identical approval status; the two markings describe different formulation routes and are not shown to contradict each other. Confirm with Afton whether the MB package approval also covers the HiTEC 12200 + 12250 route.
- (tier1) Intended service, permitted base oils, route restrictions, required co-components and published formulations are not printed; left Missing. The bar charts on p.2 (Mack T-12, Cat 1K, Seq IIIF, Mack T-11 '*Based on % Soot at 12 cSt' vs 'API CI-4 Plus Limit' / 'Reserve') have no numeric values, and the field-test text ('field tested in harsh conditions to 50,000km/31,000 miles') refers to the HiTEC 12200 family; neither is recorded.
- (tier2) Handling information printed for 'HiTEC® 12204L and HiTEC® 12250' (p.2), no template field: Max Handling Temp: 70˚C; Shelf Life: 3 months @ 45°C, 36 months @ ambient (10-40°C). Also printed, no template field: Specific Gravity @ 15.6/15.6°C 0.972.
- (tier2) KV40, sulfated ash, all elements (Ca, Mg, Zn, P, B, Mo, N, S) and pour point are not printed in the PDS; left Missing. Nothing is inferred from HiTEC 12200 (DL2-14639.pdf) or HiTEC 12250, including the premix formula; HiTEC 12200 also prints KV100 190 mm2/s, but that value is not used here.

## Task 3 data-quality audit (2026-10): summary

Every product with open questions or conflicts has a section above; entries repeated identically in several tiers are listed once. Conflict lines carry their type in square brackets. Open questions labelled [Resolved] or [History] record audit history, not unresolved questions.

### Conflicts by type (JSON conflict entries, all tiers)
- [conflicting values between different documents]: 38
- [edition difference]: 102
- [inconsistency within one document]: 3
- [unit or test-condition discrepancy]: 2
- [untyped]: 1
- Edition differences: 85 recorded in this audit (24 S-OIL Ultra-S / aramcoULTRA 8 vs the current S-OIL tables; 61 Petro-Canada PURITY LUB3213E 2015.07 vs 2023.03) and 17 earlier ones (Afton HiTEC 12200 bulletins 05/18 vs 08/18; Lubrizol CV7540 2020 vs 2022; Nynas NS 3 2016 vs 2024, repeated in three tiers). The recorded value is kept in each case.
- Conflicting values between different documents (for example TDS vs SDS) are genuine disagreements; the PURITY L65 viscosity-index entry is stored as text and counted here as [untyped].

### Documentation uncertainties and corrections
- Open questions tagged '(2026-10 audit)' record corrected or re-sourced values with their previous text, including: ADNOC ADbase 4/6/8 chemistry; S-OIL Ultra-S 2-8 and P-20; YUBASE 3/4/5/6 API Group and YUBASE 4/6 chemistry; PURITY L35-L65 API Group (now Missing: the grade-level brochure could not be inspected) and L40/L45/L50 CCS; the 37 additive-package permitted-base-oil fields; Lubrizol CV6320 element markers (now Missing); Richful RF6602 function-specific markers (now Missing); Afton HiTEC 8767B VM fields (now Missing); S-OIL Super S-8 pour point.
- Sources outside the archive are listed, with their verification status, in source_registry.json.
- Mixed nested statuses (2026-10 audit): the 19 Coverage Matrix cells flagged 'Mixed nested statuses (review)' were each checked. All are partially reported properties (e.g. a reported primary function with a missing secondary function, a reported TBN with missing element markers, one co-component dose not printed, a reported intended service with a missing package type); every Reported subfield has a value and a source file with page, and every Missing subfield is empty. They are not structural or aggregation errors, and the nested statuses are left as recorded.
- Archive file names: seven archive PDFs are stored in the zip with U+FFFD in place of '%' (e.g. 'RF6078<U+FFFD>20-<U+FFFD>20TDS.pdf'); the JSON cites them with '%' restored (e.g. RF6078%20-%20TDS.pdf). All 250 cited archive files resolve to an archive entry.
