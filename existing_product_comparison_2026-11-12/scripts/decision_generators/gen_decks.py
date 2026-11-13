# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json

D13, D15, D43, D67, D65, D68 = 'DL2-15813.pdf', 'DL2-15763.pdf', 'DL2-15543.pdf', 'DL2-15767.pdf', 'DL2-15765.pdf', 'DL2-15768.pdf'
links = []


def L(p, f, cat, fs, cov, idn, note=''):
    links.append(dict(p=p, f=f, cat=cat, status='completed', fields_status=fs, coverage=cov, identity=idn, note=note))


PORT = "portfolio slide only (product name, API level); read in full; NOT ASSESSED beyond that slide"
for f, pg in ((D15, 3), (D67, 4)):
    for p in ('RICHFUL_RF6066', 'RICHFUL_RF6078', 'RICHFUL_RF6400'):
        L(p, f, 'C', f'p.{pg} portfolio slide read (text layer); the deck has no other page on this product', PORT, f"printed '{p[8:]}' in the HDEO product portfolio")
for p in ('RICHFUL_RF6066', 'RICHFUL_RF6078'):
    L(p, D43, 'C', 'p.2 CVO product-line slide read (text layer)', PORT, f"printed '{p[8:]}'")
L('RICHFUL_RF6400', D43, 'E', 'pp.2-3 read (text layer)', "p.3 chart 'Recommended Treat Rate ... RF6400 RF6408 6.0% 5.88%' (CF-4): a further printing of RF6400 at 6.0 % (TDS 5.5 %); added to the treat-rate conflict", "printed 'RF6400'")
L('RICHFUL_RF6069', D43, 'C', 'p.12 read (text layer and chart labels)', "chart label 'HTCBT Pb Corrosion RF6069 CI-4 Limit' on an RF6079 performance slide; no RF6069 data; NOT ASSESSED further", "printed 'RF6069' as a chart label",
  'Probably a label error on an RF6079 slide; not used for RF6069.')
# RF6079
L('RICHFUL_RF6079', D15, 'E', 'pp.3, 7-9 read (text layer); pp.7 and 9 as images', "profile: API CI-4, ACEA E7-2022; '9.15% treat rate (Group II), 10.0% treat rate (Group I)'; 'RF6079@9.15% = RF6067@8.5 + RF0216@0.65%'; four licensable EHC formulations (RX210314340/353/350/351, all totals 100.0); credential table p.7 (TBC columns are other products)", "exact: 'RF6079'")
L('RICHFUL_RF6079', D67, 'E', 'pp.4, 10-11 read (text layer); p.11 as an image', "profile (November 2025): API CI-4, ACEA E7, 9.15 %; data-ready base oils incl. Group I (Aramco Dura, ExxonMobil A/P Core, Petrobas [sic]); '9.5% for 10W-XX, 9.15% for others'", "exact")
L('RICHFUL_RF6079', D43, 'E', 'pp.7-15 read (text layer; charts without numbers)', "Group II base-oil coverage (EHC, Handi Sunshine, Daesan, Sinopec HVIH), grades 15W-40/20W-50/15W-50/10W-30/10W-40, 'RF6067 8.5% + RF0216 0.65% = RF6079 9.15%', ACEA E7 cover; performance charts (no values in the text layer)", "exact")
L('RICHFUL_RF6079', D13, 'E', 'pp.4, 12, 17-21 read (text layer); p.12 as an image', "January 2026: claims API CI-4, API SL, ACEA E7 (E7: 15W-40 & 20W-50 in EHC); treat rates 9.15 % (15W-XX, 20W-50, Gr II), 9.5 % (10W-XX, Gr II), 10.0 % (15W-40 & 20W-50, Gr I); formulations EHC x4 (= DL2-15763.pdf p.9), Aramco Prima x4 (RX240020042-45), Aramco Dura x2 (RX210314352, RX230320022; PPD RF8233); p.21 specification equal to the TDS and the JSON except the N method (ASTM D5762; TDS SH/T 0656, ASTM D5291)", "exact")
L('RICHFUL_RF6079', D65, 'D', 'p.23 read (text layer)', "PPD study blend 'CI-4 15W-40': LZ7077 7.3, RF6079 9.15, PPD 0.05, EHC 50 47.5, EHC 110 36.0 (total 100.0); a different blend (PPD 0.05 % for evaluation) from the CDP final RX210314101; it does NOT resolve the CDP p.8 / p.11 swap", "printed 'RF6079, wt%'")
# RF6088
L('RICHFUL_RF6088', D15, 'E', 'pp.3-6 read (text layer); pp.4 and 6 as images', "profile: API CK-4, ACEA E11-2022, 13.8 %, OCP VM; base-oil coverage; p.6 EHC formulations 10W-30 / 10W-40 (with SK Yubase 4P 10.0) / 15W-40 and Aramco Prima 10W-30/40, 15W-40 (all printed TOTAL 100); the EHC 15W-40 column adds to 100.8", "exact")
L('RICHFUL_RF6088', D67, 'E', 'pp.4-6, 9 read (text layer); p.6 as an image', "November 2025: claims API CK-4, ACEA E11, GB D1; 'RF6088 has been D1 certified' with China D1 engine-test results (p.9); data-ready base oils incl. Kixx LUBO, Finas", "exact")
L('RICHFUL_RF6088', D43, 'E', 'pp.2, 23-35 read (text layer); pp.34-35 as images', "© 2023: '~13.8%', 'Grp. II base stock ... Less than 10% Grp. III is permitted'; next step ACEA E11; engine-test result tables (formulation codes RX-22001xx); 18 formulations pp.34-35 (EHC, Handi, Sinopec, Formosa, Chevron, CNOOC; Yubase 4 10.0 in three) all totalling 100.0; claim rows 'API CK-4' and 'China GB 11122-2006'", "exact")
L('RICHFUL_RF6088', D13, 'E', 'pp.4-5, 8-11, 54 read (text layer); pp.5 and 10 as images', "January 2026: claims API CK-4, ACEA E11 ('Cover EHC only'), GB D1 ('Cover SAE 15W-40 grade in EHC only'; but p.9 says 'GB D1 for 10W40'); p.9 = DL2-15763.pdf p.6; p.10 three more Prima formulations (RX220014001-3, PPD RF8236, ADNOC 4); p.11 specification equal to the TDS except N 0.83-1.11 / 0.97 by ASTM D5291 (TDS 0.81-1.11 / 0.96, SH/T0704, ASTM D5762); Ca 1.37-1.69 / 1.53 as the TDS", "exact")
# RF6089
L('RICHFUL_RF6089', D15, 'E', 'p.4 read (text layer and image)', "'Target' column: treat rate 'TBD', grades 15W-40, 10W-30, 10W-40, credential list (API CK-4, ACEA E11, OEM)", "exact")
L('RICHFUL_RF6089', D67, 'E', 'pp.4, 6-7 read (text layer and images)', "November 2025: 'RF6089 = RF6088+RF0219', 14.1 % (column under 'Target'); OEM approval status in EHC 15W-40: Obtained DTFR 15C100 (MB228.31), DQC III-18LA, CES 20086, M3775, DFS 93K222, VDS-4.5, EOS-4.5, RLD-3; Meets M3575, ECF-3", "exact")
L('RICHFUL_RF6089', D13, 'E', 'pp.4-7, 54 read (text layer; p.5 as an image)', "January 2026: claims API CK-4 (base oils of RF6088), ACEA E11 (EHC only), GB D1 (15W-40 in EHC only), OEM list (CES 20086 also 10W-30/40); 14.1 % = 13.8 % RF6088 + 0.3 % RF0219; specification p.7 (density 933-973 / 953, KV100 91, flash >=180 / 206, TBN 58-72 / 65, Ca, Zn, P, N, B); 'Both RF6088 and RF6089 have been GB D1 certified' (p.54)", "exact")
# RF6080 / RF6081
for p, rate, plus in (('RICHFUL_RF6080', '9.3', '0.15'), ('RICHFUL_RF6081', '9.6', '0.45')):
    L(p, D15, 'E', 'p.7 read (text layer and image)', f"earlier profile: treat rate 'TBC', 15W-40 / EHC, credential list; superseded in this archive by DL2-15767.pdf and DL2-15813.pdf ({rate} %)", 'exact')
    L(p, D67, 'E', 'pp.4, 11-12 read (text layer and images)', f"November 2025: {rate} % (equal to the TDS); 'RF6080/RF6081 = RF6079+RF0218'; OEM approval status in EHC 15W-40 (Obtained / Meets / 'Nov 2025' for Cummins)", 'exact')
    L(p, D13, 'E', 'pp.4, 12-16 read (text layer; p.12 as an image)', f"January 2026: claims API CI-4, API SL, ACEA E7 + OEM list; {rate} % = 9.15 % RF6079 + {plus} % RF0218; specification page equal to the TDS and the JSON (every limit and typical)", 'exact')
L('RICHFUL_RF6069', D13, 'E', 'p.29 read (text layer)', "'Meet requirement Products - RF6069': specification equal to DL2-15618.pdf (KV100 typical 118) with ASTM-only methods; treat rates equal (CI-4 8.5 %, CH-4 7.8 %, CF-4 4.1 % + 1.9 % RF0206, 'wt%'); shelf life 24 months", 'exact')
L('RICHFUL_RF6069', 'DL2-15546.pdf', 'E', 'p.7 read in full and compared word by word with DL2-15618.pdf', 'identical to DL2-15618.pdf except KV100 typical 142 (TDS 118) and method citations (density GB/T 13377; N SH/T 0656 / ASTM D5291)', 'exact', 'Added to the RF6069 KV100 conflict.')
L('RICHFUL_RF6071L', 'DL2-15546.pdf', 'B', 'p.8 read in full and compared word by word with RF6071L.pdf', 'same content as RF6071L.pdf (page number and column heading only)', 'exact')
# RF6077
L('RICHFUL_RF6077', D15, 'E', 'pp.3, 10-11 read (text layer)', "profile: API CI-4, 8.76 %, OCP (Paratone) VM, 15W-40 / 20W-50, data ready EHC, Formosa, Handi; two licensable EHC formulations with 'Paratone 8900E Premix' (RX230332602 / RX230332601, totals 100.0)", 'exact')
L('RICHFUL_RF6077', D67, 'E', 'pp.4, 14 read (text layer)', 'November 2025 profile identical to DL2-15763.pdf p.10 (8.76 %, OCP (Paratone) VM)', 'exact')
L('RICHFUL_RF6077', D43, 'E', 'pp.2, 16-22 read (text layer; charts without numbers)', "engine-test matrix in EHC with Paratone VM (15W-40: 1K, 1P, T-8E, ISM, T-12, EOAT, IIIH-70, RFWT; 20W-50: EOAT, ISM, T-8E) against CH-4 and CI-4 limits; 'Suitable for use with Paratone OCP'; 8.76 %", 'exact')
L('RICHFUL_RF6077', D65, 'D', 'p.24 read (text layer)', "VM / PPD study blends CI-4 15W-40: Paratone 24EX 7.8, PPD 0.3 or 0.1, RF6077 8.76, EHC 50 39.14, EHC 110 44 / 44.2 (totals 100); VM named 'Paratone 24EX' here (DL2-15763.pdf: 'Paratone 8900E Premix')", "printed 'RF6077, wt%'")
L('RF6602', D65, 'C', 'p.65 read (text layer)', "product list 'Summary on Richful's PMA products' only; NOT ASSESSED further", "printed 'RF6602'")
L('RF6602', D68, 'D', 'pp.26, 28 read (text layer)', "recipe shares: tractor fluid 'RF6602, % 1.5' (EHC 50/110) and 8# hydraulic transmission fluid 'RF6602, % 3.0' (Formosa 150N/500N); not properties of RF6602", "printed 'RF6602'")
L('NYNAS_T_3', D65, 'D', 'p.56 read (text layer)', "shock-absorber fluid recipe 'Nynas T3, wt% 32' with RF8750; a recipe share", "printed 'Nynas T3'")
L('S_OIL_SUPER_S_8', D65, 'G', 'p.61 hit read (text layer)', 'not applicable', "FALSE MATCH: the generic alias matched 'mm2/s 8.64' on a page that names 'S-oil' (Ultra S-oil base oil); S-8 is not printed")
L('S_OIL_SUPER_S_8', 'DL2-12881.pdf', 'G', 'p.7 and p.11 hits read (text layer)', 'not applicable', "FALSE MATCH: the alias matched 'mm2/s 8.0' on pages that print 'S-Oil 4/8' (Ultra grades); S-8 is not printed")

F = []


def R(p, tier, path, old, nf, np_, nt, unit, form, act, reason, orv, cmp, outc='additional', qual='', meth='', cond='', basis='', ov=''):
    d = dict(p=p, tier=tier, path=path, old=old, new_f=nf, new_p=np_, new_text=nt, unit=unit, form=form, qual=qual, method=meth, cond=cond, basis=basis,
             outcome=outc, action=act, reason=reason, old_rev=orv, cmp_override=cmp)
    if ov:
        d['overlap_reviewed'] = ov
    if path == 'published_formulations':
        d['new_text'] = 'Identity per formulation column (oil code where printed, else the base-oil / grade column): ' + d['new_text']
        d['basis'] = d['basis'] or ("printed 'Treat rate %' (basis not stated)" if 'Treat rate %' in d['new_text'] else 'mass (printed wt%)')
    if path == 'required_co_components' and not d['cond']:
        d['cond'] = 'API CI-4 licensable formulations 15W-40 (RX230332602) and 20W-50 (RX230332601) in ExxonMobil EHC'
    F.append(d)


OR79 = 're-read manually: DL2-15535.pdf whole page (text layer)'
OR88 = 're-read manually: DL2-15452.pdf whole page (text layer)'
OR89 = 're-read manually: DL2-15841 (1).pdf (SDS, 07/25/2025) as quoted in the JSON printed_text; the JSON open question states no TDS exists'
OR80 = 're-read manually: DL2-15834.pdf (TDS 2025-05-09) as quoted in the JSON; claims and treat rate'
OR81 = 're-read manually: DL2-15836.pdf (TDS 2025-05-13) as quoted in the JSON; claims and treat rate'
OR77 = 're-read manually: DL2-15536.pdf whole page (text layer)'
DECK = 'manufacturer presentation (Richful)'
# RF6079
R('RICHFUL_RF6079', 1, 'treat_rate_matrix', "DL2-15535.pdf: treat rates for API CI-4 / ACEA E7 in 'Group II base oil' only (9.15 % / 9.50 %). JSON: four rows, all Group II; no Group I row.", D13, 12,
  "'10.0% for 15W-40 & 20W-50 in Gr I' (DL2-15813.pdf p.12; p.17 '10.0% treat rate in Gp I base oil'); DL2-15763.pdf p.8 '10.0% treat rate(Group I)'", 'wt% (p.29 heading of the same deck uses wt%; this table prints %)',
  'recommended treat rate (manufacturer presentation, January 2026)', 'propose_add_route_bound',
  'A Group I route is stated by the manufacturer in two presentations (2025, January 2026) with Group I base oils named (AP/E Core, Aramco Dura, Petrobras) and two Dura formulations at 10.00 wt%. Propose adding a treat-rate row bound to 15W-40 and 20W-50 in Group I; the existing Group II rows are unchanged; basis kept as printed (%).',
  OR79, 'existing: Group II rows only', cond='15W-40 & 20W-50, Group I')
R('RICHFUL_RF6079', 1, 'performance_claims', "DL2-15535.pdf: API CI-4 / ACEA E7 (bulletin: CI-4 Plus at 11.0 %). JSON claims API CI-4, ACEA E7, API CI-4 Plus; no API SL.", D13, 12,
  "Performance Level & OEM Claim: 'API CH-4 API SL' (RF6067), 'API CI-4 API SL ACEA E7(2)' (RF6079); footnote 2 'Cover 15W-40 & 20W-50 grades in EHC.'; p.17 'API CI-4, API SL, ACEA E7'", '', 'claim (manufacturer presentation, January 2026)', 'propose_add',
  "Propose adding API SL as a claim from the January 2026 presentation (no TDS prints it), and a scope note for ACEA E7 ('Cover 15W-40 & 20W-50 grades in EHC'). Claims in a presentation are recorded with that evidence class.", OR79, 'existing: API CI-4, ACEA E7, API CI-4 Plus')
R('RICHFUL_RF6079', 1, 'published_formulations', "DL2-15535.pdf: none. JSON: Missing (the CDP final formulation is proposed separately, with its unresolved EHC 50 / EHC 110 swap).", D13, 18,
  "p.18 EHC (oil codes RX210314340 / 353 / 350 / 351; same as DL2-15763.pdf p.9): 10W-30 9.50 / LZ7077 5.3 / Viscoplex 1-248 0.2 / EHC 50 70.0 / EHC 110 15.0; 10W-40 9.5 / 9.8 / 0.2 / 70.4 / 10.1; 15W-40 9.15 / 7.0 / 0.2 / 42.00 / 41.65; 20W-50 9.15 / 6.5 / 0.2 / 3.0 / 81.15. p.19 Aramco Prima (RX240020042-45): 10W-30 9.5 / 6.00 / 0.2 / Prima 110N 32.30 / 230N 52.00; 10W-40 9.5 / 10.10 / 0.2 / 110N 37.70 / 230N 42.50; 15W-40 9.15 / 6.95 / 0.2 / 230N 69.90 / 500N 13.80; 20W-50 9.15 / 6.65 / 0.2 / 230N 10.00 / 500N 74.00. p.20 Aramco Dura (RX210314352, RX230320022): 15W-40 10.00 / 8.40 / PPD RF8233 0.30 / Dura 150SN 57.90 / 500SN 23.40; 20W-50 10.00 / 7.30 / 0.30 / 13.90 / 68.40. Nine columns add to 100.0; the Dura 20W-50 column RX230320022 adds to 99.90 against a printed TOTAL of 100.00 (image checked).",
  'wt%', 'manufacturer licensable formulations (presentation, January 2026)', 'propose_add_route_bound',
  'Propose adding the ten formulations, each bound to its column (oil code, grade, base-oil slate, VM, PPD), as printed; the Dura 20W-50 column is flagged (parts 99.90 vs printed total 100.00) and not corrected. They are different oil codes from the CDP final RX210314101 and do not bear on its unresolved EHC 50 / EHC 110 swap, which stays unresolved with both printings.',
  OR79, 'existing: published_formulations Missing', ov='different oil codes from the CDP row (RX210314101); both kept; the CDP swap is not resolved by these')
R('RICHFUL_RF6079', 1, 'permitted_base_oils_restrictions', "DL2-15535.pdf: 'blended with OCP VII in Group II base oil'. JSON permitted_api_groups ['Group II'].", D13, 17,
  "'Base Oil Coverage - Data ready: Gp II: EHC, Sinopec, Handi, HSB, Finas, Kixx LUBO, CNOOC, Aramco Prima; Gp I: AP/E Core, Aramco Dura, Patrobras [sic]; In progress/plan: Chevron, Formosa'", '', 'manufacturer statement (presentation, January 2026)', 'propose_note',
  "The TDS names Group II only; the manufacturer's later presentations add Group I stocks with their own treat rate. Propose a note listing the data-ready base oils by group with the source; the permitted groups are left for the reviewer (the TDS wording does not exclude Group I, so this is not recorded as a conflict).",
  OR79, "existing: permitted_api_groups ['Group II']")
# RF6088
R('RICHFUL_RF6088', 1, 'performance_claims', "DL2-15452.pdf: 'API CK-4/ACEA E11' for 10W-30, 10W-40, 15W-40 in Group II and Group III. JSON: API CK-4/ACEA E11; no GB D1.", D13, 5,
  "p.5 'API CK-4 / ACEA E11(2) / GB D1(3)'; footnotes '2: Cover EHC only.' '3: Cover SAE 15W-40 grade in EHC only.'; p.9 'GB D1 for 10W40'; p.54 'Both RF6088 and RF6089 have been GB D1 certified'; DL2-15767.pdf p.9 'RF6088 has been D1 certified' with CA6DM3 / DCI11 / 2.0CTI / WP13 results",
  '', 'claim (manufacturer presentations, November 2025 and January 2026)', 'propose_add_route_bound',
  "Propose adding GB D1 (China GB 11122-2025 D1) bound to EHC; the grade scope is inconsistent inside DL2-15813.pdf (p.5 footnote: 15W-40 only; p.9: 10W-40) and is recorded as such, not resolved. Also propose a scope note on the existing ACEA E11 claim: the January 2026 presentation limits E11 to EHC ('Cover EHC only'), while the TDS states Group II and Group III base oils.",
  OR88, 'existing: API CK-4/ACEA E11 (TDS scope)')
R('RICHFUL_RF6088', 1, 'permitted_base_oils_restrictions', "DL2-15452.pdf: 'blended with OCP VII in Group II and Group III base oils'. JSON permitted_api_groups ['Group II', 'Group III'], no limit.", D43, 23,
  "'Grp. II base stock EHC, Chevron, Formosa, Sinopec HVI, CNOOC, Handi Sunshine, Daesan... Less than 10% Grp. III is permitted.' (© 2023); formulations pp.34-35 and DL2-15813.pdf pp.9-10 use Group III (Yubase 4 / Yubase 4P / ADNOC 4) at 10.0 % or less",
  '%', 'manufacturer statement (presentation, 2023)', 'propose_add',
  "Propose adding the printed limit '< 10 % Group III' to the restrictions with its source and date (© 2023 presentation). The undated TDS does not print a limit; the later formulations are consistent with it. Not converted into any other rule.",
  OR88, 'existing: Group II and Group III, no limit')
R('RICHFUL_RF6088', 1, 'published_formulations', "DL2-15452.pdf: none. JSON: Missing (CDP final 15W-40 proposed separately).", D43, 34,
  "pp.34-35 'Oil formulation', 'Treat rate %' (API CK-4; China GB 11122-2006): RF6088 13.8 in all 18 columns; LZ7077 / Viscoplex 1-248 / base oils: EHC 10W-30 5.7/0.3/EHC 50 77.2/EHC 110 3.0; 10W-40 10.0/0.3/75.9; 15W-40 6.6/0.3/51.3/28.0; Handi 10W-30 5.6/0.3/150N 72.3/500N 8.0; 10W-40 9.2/0.3/72.0/4.7; 15W-40 5.6/0.3/41.3/39.0; Sinopec 10W-30 4.8/0.3/HVI 6 76.1/HVI 10 5.0; 10W-40 8.5/0.3/77.4; 15W-40 6.0/0.3/47.9/32.0; Formosa 10W-30 5.8/0.3/150N 76.1/500N 4.0; 10W-40 9.2/0.3/60.3/6.4/Yubase 4 10.0; 15W-40 6.8/0.3/51.1/28.0; Chevron 10W-30 5.5/0.3/150R 73.0/600R 7.4; 10W-40 9.3/0.3/57.1/9.5/Yubase 4 10.0; 15W-40 6.3/0.3/49.6/30.0; CNOOC 10W-30 5.4/0.3/150N 80.5; 10W-40 9.6/0.3/66.3/Yubase 4 10.0; 15W-40 5.4/0.3/44.5/500N 36.0. Every column totals 100.0 (checked).",
  'printed "Treat rate %"', 'manufacturer formulations (presentation, © 2023)', 'propose_add_route_bound',
  'Propose adding the 18 formulations, each bound to its column (grade, base-oil slate, VM LZ7077, PPD Viscoplex 1-248). No oil codes are printed; the column (base-oil pair and grade) is the identity. Basis kept as printed.',
  OR88, 'existing: published_formulations Missing', ov='a different document and set of columns from the CDP row; the EHC 15W-40 column agrees with the CDP (EHC 110 28.0)')
R('RICHFUL_RF6088', 1, 'published_formulations', "DL2-15452.pdf: none. JSON: Missing.", D13, 9,
  "p.9 (= DL2-15763.pdf p.6) EHC: 10W-30 RX220013800 13.8 / LZ7077 5.7 / Viscoplex-1-248 0.3 / EHC 50 77.2 / EHC 110 3.0 (100.0); 10W-40 RX220013802 13.8 / 10.0 / 0.3 / 61.9 / 4.0 / SK Yubase 4P 10.0 (100.00); Aramco Prima: 10W-30 RX220013936 13.8 / 5.8 / 0.3 / Prima 110N 64.1 / 230N 16.0; 10W-40 RX220013937 13.8 / 9.5 / 0.3 / 110N 51.4 / 500N 15.0 / Yubase 4P 10.0; 15W-40 RX220013938 13.8 / 6.4 / 0.3 / 110N 42.5 / 500N 37.0. p.10 Prima with PPD RF8236: 10W-30 RX220014001 13.8 / 5.7 / 0.3 / 110N 42.2 / 230N 38.0; 10W-40 RX220014002 13.8 / 9.5 / 0.3 / 31.4 / 35.0 / ADNOC 4 10; 15W-40 RX220014003 13.8 / 6.5 / 0.3 / 230N 79.4. All these columns total 100.0 (checked). The EHC 15W-40 column is in the separate conflict row.",
  'wt%', 'manufacturer licensable formulations (presentations, 2025 and January 2026)', 'propose_add_route_bound',
  'Propose adding these eight formulations by oil code. The EHC 10W-40 here (with Yubase 4P) differs from the 2023 EHC 10W-40 column of DL2-15543.pdf (EHC 50 75.9, no Group III): different formulations, both kept by their identity.',
  OR88, 'existing: published_formulations Missing', ov='identified by oil codes; distinct from the CDP final and the 2023 columns')
R('RICHFUL_RF6088', 1, 'published_formulations', "CDP C-H-2405 p.11 (proposed in the ninth pass): RX220013803 RF6088 13.8 / LZ7077 6.6 / Viscoplex 1-248 0.3 / EHC 50 51.3 / EHC 110 28.0 = 100.0. DL2-15543.pdf p.34 EHC 15W-40 column: the same 28.0.", D13, 9,
  "DL2-15813.pdf p.9 and DL2-15763.pdf p.6, 15W-40 'Oil Code: RX2200133803': RF6088 13.8 / Lubrizol 7077 6.6 / Viscoplex-1-248 0.3 / ExxonMobil EHC 50 51.3 / ExxonMobil EHC 110 28.8 / TOTAL 100.00 (the printed parts add to 100.8; image checked)",
  'wt%', 'manufacturer licensable formulation (presentation printing)', 'propose_record_conflict',
  "The presentation printing of the EHC 15W-40 formulation (EHC 110 28.8, parts adding to 100.8 against a printed total of 100.00, oil code printed 'RX2200133803') differs from the CDP final RX220013803 (28.0, total 100.0) and from the 2023 deck (28.0). Propose recording the discrepancy with all three citations; the oil-code identity is not assumed (one extra digit); nothing is corrected or averaged.",
  OR88, 'existing: Missing; CDP 15W-40 row proposed (28.0)', outc='changed_or_conflicting', ov='discrepancy row for one column; the other rows exclude this column')
R('RICHFUL_RF6088', 2, 'elements.N', "DL2-15452.pdf: 'N Content, m% | 0.81-1.11 | 0.96 | SH/T0704, ASTM D5762'. JSON N 0.96 (0.81-1.11).", D13, 11,
  "'N Content, m% | 0.83-1.11 | 0.97 | ASTM D5291' (RF6088 specification page, presentation January 2026)", 'm%', 'specification limits and typical (manufacturer presentation, January 2026)', 'propose_record_conflict',
  'The January 2026 specification page prints a different lower limit and typical for N and another method (D5291, combustion; TDS D5762, chemiluminescence). Propose recording a conflict with both sources and methods; the JSON keeps the TDS values; no date-based preference.',
  OR88, 'existing: N 0.96 (0.81-1.11), SH/T0704, ASTM D5762', outc='changed_or_conflicting', qual='limits + typical', meth='ASTM D5291')
# RF6089
R('RICHFUL_RF6089', 1, 'performance_claims', "DL2-15841 (1).pdf (SDS): no claims. JSON performance_claims Missing (open question: no TDS).", D13, 5,
  "p.5 RF6089 column: 'API CK-4(1) / ACEA E11(2) / GB D1(3) / Caterpillar ECF-3 / Cummins CES 20086(4) / Daimler Truck DTFR 15C100 (MB228.31) / Detroit Diesel DFS 93K222 / Deutz DQC III-18LA / Mack EO-4.5 / MAN M3775 / MTU Cat 2.1 / Renault RLD-3 / Volvo VDS-4.5 / International (meet)'; footnotes 1 base oils, 2 EHC only, 3 15W-40 in EHC only, 4 also 10W-30 & 10W-40. p.6: 'Approved for: DTFR 15C100 ..., MTU Cat 2.1' and 'Meet : CAT ECF-3, MAN M3575'. DL2-15767.pdf p.7 table (EHC 15W-40): Obtained ... 'EOS-4.5' (Mack), 'Meets' M3575 and ECF-3.",
  '', 'claims and OEM approval status (manufacturer presentations, November 2025 and January 2026)', 'propose_add_route_bound',
  "Propose adding the claims bound to SAE 15W-40 in ExxonMobil EHC (with the footnoted exceptions), keeping 'approved / obtained' separate from 'meets'. The Mack specification is printed 'EOS-4.5' (November 2025) and 'EO-4.5' (January 2026): both printings kept. Evidence class: manufacturer presentation; not checked against OEM approval lists.",
  OR89, 'existing: performance_claims Missing')
R('RICHFUL_RF6089', 1, 'treat_rate_matrix', 'SDS: none. JSON treat_rate_matrix Missing.', D13, 5,
  "'Treat Rate 14.1% (13.8% RF6088 + 0.3% RF0219)'; 'Viscosity Grade SAE 15W-40'; 'Base Oil EHC'. DL2-15767.pdf p.6: 14.1 % (column under 'Target'); DL2-15763.pdf p.4: 'TBD'.", '%', 'recommended treat rate (manufacturer presentation, January 2026)', 'propose_add_route_bound',
  "Propose a treat-rate row 14.1 % bound to API CK-4 SAE 15W-40 in EHC, citing the earlier 'TBD' (2025) and the 'Target' label of November 2025 as history. Basis kept as printed '%'.",
  OR89, 'existing: Missing', cond='SAE 15W-40, ExxonMobil EHC')
R('RICHFUL_RF6089', 1, 'package_type_application.package_type', 'SDS: product name only. JSON package_type Missing.', D13, 5,
  "'14.1% (13.8% RF6088 + 0.3% RF0219)'; DL2-15767.pdf p.6 'RF6089 = RF6088+RF0219'; p.4 'RF6089 API CK-4, ACEA E11 ready GB D1, OEM'", '', 'manufacturer statement (presentation)', 'propose_note',
  'Propose a note that RF6089 is RF6088 (13.8 %) plus booster RF0219 (0.3 %), as printed; RF0219 is not in the database; nothing is derived from the relation.', OR89, 'existing: Missing')
R('RICHFUL_RF6089', 1, 'permitted_base_oils_restrictions', 'SDS: none. JSON Missing.', D13, 6,
  "p.5 'Base Oil EHC'; p.6 'Base oils to be covered: ARAMCO Prima, CNOOC, Sinopec, Formosa, HDS, HSB, Chevron, Kixx LUBO, Finas'; 'Viscosity grades to be covered: 10W-30, 10W-40'", '', 'manufacturer statement (presentation, January 2026)', 'propose_add_route_bound',
  "Propose recording EHC as the covered base oil, with the 'to be covered' lists kept as plans (not permissions).", OR89, 'existing: Missing')
SPEC = [('tbn', 'mg KOH/g', "'Total Base Number, mg KOH/g | 58-72 | 65 | ASTM D2896'", 'ASTM D2896'),
        ('elements.Ca', 'm%', "'Ca Content, m% | 1.32-1.62 | 1.47 | ASTM D4951'", 'ASTM D4951'),
        ('elements.Zn', 'm%', "'Zn Content, m% | 0.77-0.95 | 0.86 | ASTM D4951'", 'ASTM D4951'),
        ('elements.P', 'm%', "'P Content, m% | 0.69-0.85 | 0.77 | ASTM D4951'", 'ASTM D4951'),
        ('elements.N', 'm%', "'N Content, m% | 0.86-1.16 | 1.01 | ASTM D5762'", 'ASTM D5762'),
        ('elements.B', 'm%', "'B Content,m% | 0.09-0.15 | 0.12 | ASTM D4951'", 'ASTM D4951')]
for path, unit, txt, meth in SPEC:
    R('RICHFUL_RF6089', 2, path, f'DL2-15841 (1).pdf (SDS): {path} not printed (component shares only). JSON {path} Missing.', D13, 7, txt + ' (RF6089 specification page, Requirement Limit / Typical Value)',
      unit, 'specification limits and typical (manufacturer presentation, January 2026)', 'propose_add',
      'The only printing of this value; a manufacturer specification page (limits and typical) in a dated presentation. Propose adding with that source; no TDS exists in the archive.', OR89, f'existing: {path} Missing', qual='limits + typical', meth=meth)
R('RICHFUL_RF6089', 2, 'kv100', "DL2-15841 (1).pdf p.5: 'Viscosity, kinematic : 92 mm2/s (100 C)'. JSON kv100 92.", D13, 7, "'Kinematic Viscosity (100 C), mm2/s | Report | 91 | ASTM D445'", 'mm2/s',
  'typical (manufacturer specification page, January 2026)', 'propose_record_conflict', 'SDS 92 vs specification-page typical 91 mm2/s: different documents, different values. Propose recording a conflict with both sources; the JSON keeps 92; not averaged; no preference by document type.',
  OR89, 'existing: kv100 92 (SDS)', outc='changed_or_conflicting', qual='typical', meth='ASTM D445')
R('RICHFUL_RF6089', 2, 'flash_point', "DL2-15841 (1).pdf p.5: 'Flash point : 213 C (COC)'. JSON flash_point 213.", D13, 7, "'Flash Point (COC), C | >=180 | 206 | ASTM D92'", 'C',
  'specification limit and typical (manufacturer specification page, January 2026)', 'propose_record_conflict', 'SDS 213 C vs specification-page typical 206 C (both COC); the page adds the limit >= 180. Propose recording a conflict for the typical and adding the limit with its source; JSON value unchanged.',
  OR89, 'existing: flash_point 213 (SDS)', outc='changed_or_conflicting', qual='minimum + typical', meth='ASTM D92')
R('RICHFUL_RF6089', 2, 'density', "DL2-15841 (1).pdf p.6: 'Density : 0.953 g/cm3(20 C)'. JSON density 0.953 g/cm3.", D13, 7, "'Density (20 C), kg/m3 | 933-973 | 953 | ASTM D4052'", 'kg/m3',
  'specification limits and typical (manufacturer specification page, January 2026)', 'propose_alternate_entry',
  'Same typical: 0.953 g/cm3 = 953 kg/m3 exactly (1 g/cm3 = 1,000 kg/m3), both at 20 C. The page adds limits 933-973 kg/m3 and the method; propose them as an alternate entry with this source; the stored value is unchanged.',
  OR89, 'existing: density 0.953 g/cm3 (SDS)', outc='already_captured', qual='limits + typical', meth='ASTM D4052')
# RF6080 / RF6081
for p, orv, rate, plus, extra in (('RICHFUL_RF6080', OR80, '9.3', '0.15', "p.12 RF6080 column: 'API CI-4(1) / API SL(1) / ACEA E7(2) / - / Caterpillar ECF-1a / Cummins CES 20077 / - / Daimler Truck DTFR 15B110 (MB228.3) / Detroit Diesel DFS 93K215 / Deutz DQC III-18 / MTU Cat 2 / Volvo VDS-3 / Mack EO-N / Renault RLD-2 / MAN M3275-1 (meet)' (dashes where RF6081 lists JASO DH-1 and CES 20078); p.15 RF6080 profile however lists 'OEM Approvals: JASO DH-1, Cummins CES 20077/20078, ...'. DL2-15767.pdf p.12 (EHC 15W-40): Obtained DTFR 15B110, DQC III-18, DFS 93K215, VDS-3, EO-N, RLD-2; Meets M3275-1, ECF-1a; CES 20077 'Nov 2025'; CES 20078 cell greyed."),
                                     ('RICHFUL_RF6081', OR81, '9.6', '0.45', "p.12 RF6081 column: 'API CI-4 / API SL / ACEA E7 / JASO DH-1 / Caterpillar ECF-1a / Cummins CES 20077 / Cummins CES 20078 / Daimler Truck DTFR 15B110 (MB228.3) / Detroit Diesel DFS 93K215 / Deutz DQC III-18 / MTU Cat 2 / Volvo VDS-3 / Mack EO-N / Renault RLD-2 / MAN M3275-1 (meet)'; p.13 profile: same, 'Meet Performance: Caterpillar ECF-1a, MAN M3275-1'. DL2-15767.pdf p.12: Obtained as for RF6080; CES 20077 and CES 20078 'Nov 2025'.")):
    R(p, 1, 'performance_claims', f'TDS ({rate} %): API CI-4 and ACEA E7' + (' and JASO DH-1' if p.endswith('81') else '') + '; no API SL, no OEM approvals. JSON accordingly.', D13, 12, extra, '',
      'claims and OEM approval status (manufacturer presentations, November 2025 and January 2026)', 'propose_add_route_bound',
      "Propose adding API SL and the OEM approvals bound to SAE 15W-40 in ExxonMobil EHC, keeping 'approved / obtained' and 'meets' separate and leaving Cummins items dated 'Nov 2025' in the November 2025 deck as stated." + (" For RF6080 the January 2026 presentation is internally inconsistent (p.12 dashes vs p.15 'JASO DH-1, CES 20077/20078'): both are recorded; JASO DH-1 and CES 20078 are NOT proposed as RF6080 claims." if p.endswith('80') else ''),
      orv, 'existing: API CI-4, ACEA E7' + (', JASO DH-1' if p.endswith('81') else ''))
    R(p, 1, 'package_type_application.package_type', 'TDS: package description only. JSON: no composition relation.', D13, 13 if p.endswith('81') else 15,
      f"'{rate}% {p[8:]}= 9.15% RF6079 + {plus}% RF0218'; DL2-15767.pdf p.11 'RF6080/RF6081 = RF6079+RF0218'", '', 'manufacturer statement (presentation)', 'propose_note',
      f'Propose a note that {p[8:]} is RF6079 (9.15 %) plus booster RF0218 ({plus} %), as printed; nothing is derived from it.', orv, 'existing: no composition relation')
# RF6077
R('RICHFUL_RF6077', 1, 'required_co_components', "DL2-15536.pdf: 'blended with OCP VII in Group II base oil'; VII not named. JSON: role 'VII (OCP)', name null, dose Missing.", D15, 11,
  "DL2-15763.pdf p.11 'Paratone 8900E Premix 7.8 (15W-40) / 8.0 (20W-50)'; p.10 'OCP (Paratone) VM'; DL2-15543.pdf p.17 'Suitable for use with Paratone OCP'; DL2-15765.pdf p.24 study blends with 'Paratone 24EX 7.8'", 'wt%', 'component of licensable formulations (manufacturer presentations)', 'propose_add_route_bound',
  "Propose naming 'Paratone 8900E Premix' with its doses for the two licensable CI-4 formulations only; the VM-study blends of DL2-15765.pdf use 'Paratone 24EX' and are recorded as a separate route, not merged. Not a universal co-component.",
  OR77, 'existing: VII (OCP), name null')
R('RICHFUL_RF6077', 1, 'published_formulations', 'DL2-15536.pdf: none. JSON Missing.', D15, 11,
  "'CI-4 Licensable formulations, Formulation, wt%': 15W-40 Oil Code RX230332602: RF6077 8.76 / Paratone 8900E Premix 7.8 / Viscoplex-1-248 0.3 / ExxonMobil EHC 50 39.14 / EHC 110 44.0 / TOTAL 100.0; 20W-50 RX230332601: 8.76 / 8.0 / 0.3 / 4.0 / 78.94 / 100.0 (both add to 100.0)",
  'wt%', 'manufacturer licensable formulations (presentation, 2025)', 'propose_add_route_bound', 'Propose adding both formulations by oil code, route-bound (API CI-4, EHC, Paratone 8900E Premix).', OR77, 'existing: Missing')
overrides = [
    dict(p='RICHFUL_RF6069', path='kv100', new_f='DL2-15743.pdf', reason_append="Further printings found in the tenth pass: DL2-15546.pdf p.7 (catalogue, undated) prints 142 (methods GB/T 13377 / SH/T 0656 / ASTM D5291, as DL2-15743.pdf); DL2-15813.pdf p.29 (presentation, January 2026) prints 118 (ASTM methods). Both sides now have three manufacturer printings; still unresolved."),
    dict(p='RICHFUL_RF6400', path='treat_rate_matrix[0].treat_rate_wt_pct', new_f='DL2-15743.pdf', reason_append="Further printing (tenth pass): DL2-15543.pdf p.3 chart 'Recommended Treat Rate ... RF6400 6.0%' (CF-4)."),
    dict(p='RICHFUL_RF6088', path='elements.Ca', new_f='DL2-15743.pdf', reason_append="Further printing (tenth pass): DL2-15813.pdf p.11 (January 2026) prints 1.37-1.69 / 1.53 (ASTM D4951), as the TDS."),
    dict(p='RICHFUL_RF6079', path='package_type_application.package_type', new_f='RF6079%20Booklet.pdf', reason_append="Same relation in the presentations: DL2-15763.pdf p.9 and DL2-15813.pdf p.18 'RF6079@9.15% = RF6067@8.5 (API CH4) + RF0216@0.65%'; DL2-15543.pdf p.8 'RF6067 8.5% + RF0216 0.65% = RF6079 9.15%' (0.25 + 0.2 + 0.2 = 0.65 in the CDP)."),
]
docs = {
    D15: dict(what="Richful 'HDEO Additive Richful Solution' presentation (17 slides)", printed_date='© Richful 2025 (no month)', kind='manufacturer presentation', read='all 17 slides (text layer); slides 4, 6, 7, 9 as images', limits='performance charts carry no values in the text layer'),
    D67: dict(what="Richful 'Engine Oil Additive Solution' presentation (26 slides; HDEO and PCMO)", printed_date='November 2025', kind='manufacturer presentation', read='all 26 slides (text layer); slides 6, 7, 11, 12 as images', limits='PCMO slides 17-25 concern other products'),
    D43: dict(what="Richful 'Engine Commercial Vehicle Oil Additive Product' presentation (36 slides)", printed_date='© Richful 2023', kind='manufacturer presentation', read='all 36 slides (text layer); slides 34-35 as images', limits='charts carry no values'),
    D13: dict(what="Richful 'Automotive Engine Oil Additive Solutions' presentation (54 slides)", printed_date='January 2026', kind='manufacturer presentation', read='slides 1-21, 29 and 54 (text layer); slides 5, 10, 12 as images', limits='slides 22-28 and 30-53 (other products, PCMO) not reviewed'),
    D65: dict(what="Richful 'Building Your Flow with Richful's VIIs & PPDs' presentation (74 slides)", printed_date='Nov. 25th, 2025', kind='manufacturer presentation (VII / PPD)', read='slides 1, 23, 24, 56, 61, 65 (text layer)', limits='other slides concern VII / PPD products not in the database'),
    D68: dict(what="Richful 'Driveline Solutions' presentation (62 slides)", printed_date='2025-11', kind='manufacturer presentation (driveline)', read='slides 1, 26, 28 (text layer)', limits='other slides not reviewed'),
}
d = dict(batch='Richful: presentations DL2-15763 / 15767 / 15543 / 15813 / 15765 / 15768 and remaining catalogue links (tenth pass)', reviewed_on='2026-11-13 (tenth pass)',
         note="All Richful presentation links of the queue were read on the pages listed per document (text layer; key tables also as images). Dates: 2023 (DL2-15543), 2025 (DL2-15763), November 2025 (DL2-15767, DL2-15765, DL2-15768), January 2026 (DL2-15813). Claims and approvals from presentations carry that evidence class; 'Target', 'TBC', 'TBD' and 'to be covered' are kept as plans, not claims. Formulation totals were checked by addition; one printing does not add up (RF6088 EHC 15W-40, 100.8). The RF6079 CDP EHC 50 / EHC 110 swap stays unresolved: no presentation prints the CDP oil code RX210314101.",
         documents=docs, links=links, fields=F, field_overrides=overrides)
json.dump(d, open('existing_product_comparison_2026-11-12/decisions/zzzzzzzzzz_richful_decks_tenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F), len(overrides))
