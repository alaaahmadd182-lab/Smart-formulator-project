# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
links, F = [], []


def L(p, f, cov, fs, idn, note='', cat='A'):
    links.append(dict(p=p, f=f, cat=cat, status='completed', fields_status=fs, coverage=cov, identity=idn, note=note))


def R(p, tier, path, old, nf, np_, nt, unit, form, act, reason, orv, cmp, outc, qual='', meth='', cond=''):
    F.append(dict(p=p, tier=tier, path=path, old=old, new_f=nf, new_p=np_, new_text=nt, unit=unit, form=form, qual=qual, method=meth, cond=cond, basis='', outcome=outc, action=act, reason=reason, old_rev=orv, cmp_override=cmp))


# S-OIL Ultra-S sheet distributed by Cosan (never cited)
U = 'DL2-11240.pdf'
NOF = "Saybolt colour 30; CCR < 0.01 wt% (D189); copper corrosion 1a; TAN < 0.01; ring analysis (D3238) CA / CN / CP; aniline point (D611); UV absorbance 260-350 nm < 0.1 (D2269) - no template field (ring-analysis CA is not the template's aromatics quantity)"
L('S_OIL_ULTRA_S_4', U, f"assessed by reading (2026-11-13, eleventh pass): 'Typical Properties Ultra-S Series' sheet with the footer 'Cosan Lubrificantes e Especialidades SA, Authorized Distributor of S-Oil Base Stocks' (undated); every Ultra-S 4 value equals the JSON (SG 15/4 C 0.834, KV40 19.62, KV100 4.247, VI 123, flash COC 228, pour -20.0, sulfur < 1.0 ppm, Noack 14.5, saturates > 99); also printed: {NOF}: aniline 115.8, CN 17.7, CP 82.1",
  'whole page read (text layer)', "exact: column 'Ultra-S 4'", 'Archive file never cited by the record; distributor-issued copy of S-OIL typicals.')
L('S_OIL_ULTRA_S_8', U, f"assessed by reading (2026-11-13, eleventh pass): Cosan-distributed S-OIL sheet (undated); every Ultra-S 8 value equals the JSON (0.847, 43.89, 7.234, VI 127, flash 256, pour -15.0, sulfur < 1.0, Noack 4.1, saturates > 99); also printed: {NOF}: aniline 124.0, CN 20.9, CP 78.9",
  'whole page read (text layer)', "exact: column 'Ultra-S 8'", 'As for Ultra-S 4.')
L('S_OIL_ULTRA_S_6', U, f"assessed by reading (2026-11-13, eleventh pass): Cosan-distributed S-OIL sheet (undated); the Ultra-S 6 column is a THIRD set of typicals, different from both the cited brochure DL2-11177.pdf and the S-OIL web page already in the JSON conflicts: SG 0.840, KV40 32.69, KV100 6.017, VI 132, flash 234, pour -17.5, Noack 7.9 (field rows); sulfur < 1.0 and saturates > 99 equal; also printed: {NOF}: aniline 123.5 (brochure 119.8), CN 17.3, CP 82.5",
  'whole page read (text layer)', "exact: column 'Ultra-S 6'", 'Values differ from both recorded editions; see conflict rows.')
ORU = 're-read manually: DL2-11177.pdf (cited brochure spread) - values as compared in the ninth pass (zzzzzzzzz_soil_brochure_ninth_pass.json)'
for path, t, br, web, cos, unit in (('kv40', 1, '33.32', '32.54', '32.69', 'cSt'), ('kv100', 1, '6.0', '6.04', '6.017', 'cSt'), ('viscosity_index', 1, '127', '134', '132', ''), ('flash_point', 2, '235', '240', '234', 'C'), ('pour_point', 2, '-20.0', '-16', '-17.5', 'C')):
    R('S_OIL_ULTRA_S_6', t, path, f"DL2-11177.pdf (cited): {br}; existing unresolved 'edition difference' conflict with the S-OIL web page: {web}.", U, 1, f"'Ultra-S 6' column: {cos} (Cosan-distributed S-OIL typical-properties sheet, undated)", unit,
      'typical (distributor copy of manufacturer typicals, undated)', 'propose_record_conflict',
      f'A third printed value ({cos}) for the same property; propose adding it to the existing conflict with its source and the distributor footer; no edition order is assumed (the sheet is undated); the JSON value stays.', ORU, f'existing: {br}; conflict with web {web}', 'changed_or_conflicting', qual='typical')
for path, t, br, cos, unit, meth in (('noack_volatility', 2, '8.0 wt%', '7.9', 'wt%', 'D 5800'), ('specific_gravity', 1, '0.843 (15/4 C, D 1298)', '0.840', '', 'D 1298')):
    R('S_OIL_ULTRA_S_6', t, path, f'DL2-11177.pdf (cited): {br}; no conflict recorded.', U, 1, f"'Ultra-S 6' column: {cos} ({meth}; Cosan-distributed S-OIL sheet, undated)", unit, 'typical (distributor copy of manufacturer typicals, undated)', 'propose_record_conflict',
      f'Different printed typical ({cos} vs {br}); propose recording a conflict with both sources; no preference.', ORU, f'existing: {br}', 'changed_or_conflicting', qual='typical', meth=meth)
# SpectraSyn 10 later edition
L('EXXONMOBIL_SPECTRASYN_10', 'DL2-15428.pdf', "assessed by reading (2026-11-13, eleventh pass): later edition (Revision Date 07/01/2019, (c)2024) of the cited DL2-11336.pdf (07/30/2015); word-level comparison: identical except the dates and the added 'Additional Information: Technical White Mineral Oil, 21 CFR 178.3620(b); NSF White book category code H1, lubricants with incidental food contact' (no template field; preserved here). Every value equals the JSON. Not captured from either edition (no template field): KV -40 C 39000 cSt (2), water < 50 ppm, refractive index 1.4615 (2), TAN < 0.05, Brookfield -40 C 36650 cP (2), density correction factor 6.32E-4 (2), fire point 296 C (2), evaporation loss 0.7 wt% (150 C, 22 h, 2), dielectric strength 35.6 kV (2), aniline point 134.6 C (2), Kauri-Butanol 5.0 (2); the captured CCS -30 C 8840 cP carries footnote 2 (single sample or two sample average).",
  'both pages read in full and compared word by word with DL2-11336.pdf', "exact: 'SpectraSyn 10'", 'Never cited by the record; later edition with no value change.', cat='A')
# SpectraSyn 2 SDS
S2 = 'DL2-13913.pdf'
L('EXXONMOBIL_SPECTRASYN_2', S2, "assessed by reading (2026-11-13, eleventh pass): ExxonMobil MATERIAL SAFETY DATA SHEET SPECTRASYN 2 (Revision Date 14 Nov 2011, product code 6016513-05), never cited by the record. Section 9 (for safety purposes; 'may not fully represent product specifications'): relative density 0.8 at 15 C [in-house] (data sheet SG 0.798 at 15.6 C: consistent at the printed precision); flash 145 C [ASTM D-93] (data sheet 157 C is the COC value: different method, alternate-entry row); KV40 5.2 cSt and KV100 1.7 cSt [in-house] (data sheet 5.0 / 1.7: KV40 conflict row); pour -66 C [in-house] (equal); boiling point 310 C; vapour pressure < 0.013 kPa at 20 C. Section 2: 'Dec-1-ene, dimers, hydrogenated' CAS 68649-11-6 > 90 % (chemistry note row). Section 3: 'considered to be hazardous ... Toxic by inhalation. If swallowed, may be aspirated and cause lung damage' (no template field; preserved in the note row). Sections 1-3 and 9 read in full; sections 4-8 and 10-16 read for product data (none beyond hazard / toxicology statements).",
  'all 10 pages (text layer); sections 1-3 and 9 read in full', "exact: 'SPECTRASYN 2'")
OR2 = 're-read manually: DL2-11328.pdf (cited data sheet, 07/30/2015) as quoted in the JSON printed values'
R('EXXONMOBIL_SPECTRASYN_2', 1, 'kv40', 'DL2-11328.pdf (cited, 07/30/2015): KV40 5.0 (ASTM D445). JSON 5.0.', S2, 5, "'Viscosity: 5.2 cSt (5.2 mm2/sec) at 40 C | 1.7 cSt (1.7 mm2/sec) at 100 C [In-house method]' (SDS 14 Nov 2011)", 'cSt',
  'SDS physical property, typical value as printed (in-house method; for safety purposes, may not represent specifications)', 'propose_record_conflict', 'SDS (2011, in-house) 5.2 vs data sheet (2015, D445) 5.0; propose recording the conflict with both sources and methods; no preference; JSON unchanged.', OR2, 'existing: 5.0', 'changed_or_conflicting', qual='typical (SDS)', meth='in-house method')
R('EXXONMOBIL_SPECTRASYN_2', 2, 'flash_point', 'DL2-11328.pdf (cited): flash point COC 157 C. JSON 157 (COC).', S2, 3, "'Flash Point [Method]: 145 C (293 F) [ASTM D-93]' (SDS sections 5 and 9)", 'C', 'SDS physical property, typical value as printed (closed cup; for safety purposes)', 'propose_alternate_entry',
  'A closed-cup (D93) value for the same property; propose an alternate entry with method and source beside the COC value, which stays selected; different methods are not compared as a conflict.', OR2, 'existing: 157 (COC)', 'additional', qual='typical (SDS)', meth='ASTM D-93')
R('EXXONMOBIL_SPECTRASYN_2', 1, 'api_group_chemistry.chemistry', "JSON chemistry 'Polyalphaolefin (PAO)'.", S2, 2, "'Dec-1-ene, dimers, hydrogenated | 68649-11-6 | > 90 %' (SDS Section 2)", '', 'SDS composition', 'propose_note',
  "Propose adding the substance name, CAS number and the printed share (> 90 %) to the chemistry entry, and the hazard statement (toxic by inhalation; aspiration) to a note, because no template field holds hazard classification. Nothing else is derived.", OR2, "existing: 'Polyalphaolefin (PAO)'", 'additional')
# SpectraSyn Elite 150 SDS
E = 'DL2-11849.pdf'
L('EXXONMOBIL_SPECTRASYN_ELITE_150', E, "assessed by reading (2026-11-13, eleventh pass): ExxonMobil MATERIAL SAFETY DATA SHEET SPECTRASYN ELITE 150 (Revision Date 26 Sep 2012, product code 6026192-01), never cited by the record. Section 9 (for safety purposes): relative density 0.85 at 15 C [in-house] (data sheet SG 0.849 at 15.6 C: consistent at the printed precision); flash 246 C [ASTM D-92] (data sheet 277 C, also D92: conflict row); KV40 1731 cSt and KV100 157 cSt [in-house] (data sheet 1649 / 156: conflict rows); pour -33 C [in-house] (equal); vapour pressure < 0.013 kPa at 20 C. Section 2: no reportable hazardous substance; not hazardous. Sections 1-3 and 9 read in full; other sections read for product data (none).",
  'all 9 pages (text layer); sections 1-3 and 9 read in full', "exact: 'SPECTRASYN ELITE 150'")
ORE = 're-read manually: DL2-11378.pdf (cited data sheet, 01/07/2015) as quoted in the JSON printed values'
for path, t, sds, tds, unit, meth in (('kv40', 1, '1731 cSt (1731 mm2/sec) at 40 C [In-house method]', '1649 (D445)', 'cSt', 'in-house method'), ('kv100', 1, '157 cSt (157 mm2/sec) at 100 C [In-house method]', '156 (D445)', 'cSt', 'in-house method'),
                                      ('flash_point', 2, 'Flash Point [Method]: 246 C (475 F) [ASTM D-92]', '277 (COC, D92)', 'C', 'ASTM D-92')):
    R('EXXONMOBIL_SPECTRASYN_ELITE_150', t, path, f'DL2-11378.pdf (cited, 01/07/2015): {tds}. JSON equals the data sheet.', E, 5, f"'{sds}' (SDS section 9, 26 Sep 2012)", unit, 'SDS physical property, typical value as printed (for safety purposes, may not represent specifications)', 'propose_record_conflict',
      'SDS (2012) and data sheet (2015) print different values' + (' by the same method (D92): a real disagreement between the two documents' if path == 'flash_point' else '') + '; propose recording the conflict with both sources, methods and dates; no preference; JSON unchanged.',
      ORE, f'existing: {tds}', 'changed_or_conflicting', qual='typical (SDS)', meth=meth)
# Ultra-S 3 third-party MSDS
L('S_OIL_ULTRA_S_3', 'DL2-13823.pdf', "assessed by reading (2026-11-13, eleventh pass): MATERIAL SAFETY DATA SHEET 'BASE OIL ULTRA S3' (product name printed 'BASE OIL S3'), issued by TEXOL Lubritech FZC, Hamriyah Free Zone, Sharjah (Date Prepared 16May2021, Revision Date 29 January 2023), never cited by the record; not an S-OIL document. Content: 'Mixture of Paraffin Oil - 100%', HC code 27101997, specific gravity 0.83 (JSON SG 0.827 at 15/4 C: consistent at the printed precision), clear amber liquid, not hazardous (OSHA), LD50 > 5000 mg/kg, transport not regulated. Nothing proposed: a third party's MSDS adds no product property beyond a rounded SG.",
  'all 6 pages (text layer)', "printed 'BASE OIL ULTRA S3' by TEXOL Lubritech FZC (third party; identity with S-OIL Ultra-S 3 not stated)", 'Third-party document.')
# EHC
L('EXXONMOBIL_EHC_50', 'DL2-11786.pdf', 'not assessed', "all 3 pages compared word by word with the cited DL2-11785.pdf: identical text (ratio 1.000; web print 4/29/2019). Its coverage equals that of the cited source, which was not re-assessed field by field in this pass.", "exact: 'EHC Series'", 'Identical text to the cited source.')
for p in ('EXXONMOBIL_EHC_45', 'EXXONMOBIL_EHC_65', 'EXXONMOBIL_EHC_110', 'EXXONMOBIL_EHC_120'):
    L(p, 'DL2-11786.pdf', 'not assessed', 'identical text to the cited DL2-11785.pdf (word-level ratio 1.000)', "exact: 'EHC Series'")
X = 'DL2-11327.pdf'
for p, col, lim in (('EXXONMOBIL_EHC_45', 'EHC 45', 'KV100 4.4-4.7, VI 113-119, flash min 204, Noack max 15, pour max -18, CCS -25 C max 1550, colour max L0.5'), ('EXXONMOBIL_EHC_50', 'EHC 50', 'KV100 5.2-5.6, VI 110-119, flash min 210, Noack max 15, pour max -15, CCS -20 C max 1700, colour max 0.5'),
                    ('EXXONMOBIL_EHC_65', 'EHC 65', 'KV100 6.3-6.6, VI 103-109, flash min 214, Noack max 10, pour max -18, CCS -20 C max 3100, colour max L0.5'), ('EXXONMOBIL_EHC_110', 'EHC 110', 'KV100 10.0-12.0, VI 95-119, flash min 230, pour max -12, colour max 0.5 (no Noack, no CCS)')):
    L(p, X, f"assessed by reading (2026-11-13, eleventh pass): EHC Series 'Sales Specifications', edition 06-2018 (printed 27.10.2018), an earlier edition than the cited DL2-11785.pdf (03-2019); column '{col}' (image checked): {lim} - every limit equals the JSON. Representation issue found: the JSON stores the KV100 range as a list in 'value' with min / max empty and printed_text '[a, b]' instead of the printed text, and stores the flash minimum and pour maximum as 'value' with only value_kind marking the limit (note row).",
      'both pages read in full (text layer; p.1 as an image)', f"exact: column '{col}'", 'Earlier edition, never cited; same limits.')
    R(p, 1, 'kv100', f"DL2-11785.pdf (cited, 03-2019) and DL2-11327.pdf (06-2018) print 'Kinematic Viscosity @ 100 C ... Min-Max {lim.split(',')[0].split(' ')[1]}'. JSON kv100: range stored as a list in 'value', min / max null, printed_text '[..]'; flash / pour limits stored in 'value' with value_kind minimum / maximum.", X, 1,
      f"'Kinematic Viscosity@ 100 C mm2/sec | ASTM D 445 | Min-Max | {lim.split(',')[0].split(' ')[1]}'; 'Flash Point,COC Deg C | ASTM D 92 | Min | ..'; 'Pour Point, Deg C | ASTM D 97 | Max | ..' (column '{col}')", 'mm2/s',
      'specification limits (manufacturer sales specification)', 'propose_note',
      "The values are captured but not in the agreed form: ranges belong in min / max (kept as a range, not a point), limits need their printed qualifier ('Min', 'Max', 'Min-Max') and printed_text should hold the printed text. Propose a representation correction note; no value changes.",
      're-read manually: DL2-11327.pdf both pages (this pass); DL2-11785.pdf as quoted in the JSON', 'existing: range as a list in value', 'already_captured', qual='specification range', meth='ASTM D 445')
d = dict(batch='duplicate-source coverage: never-cited archive files, first set (eleventh pass)', reviewed_on='2026-11-13 (eleventh pass)',
         note='Never-cited byte duplicates read in full: S-OIL Ultra-S sheet (Cosan), SpectraSyn 10 later edition, SpectraSyn 2 and Elite 150 SDS, a third-party Ultra S3 MSDS, the EHC 2018 sales specification and a web print identical to the cited EHC sheet. The inventory labels DL2-11327.pdf and DL2-11786.pdf as SDS; both are EHC product data sheets.',
         documents={U: dict(what="S-OIL 'Typical Properties Ultra-S Series' (Ultra-S 4 / 6 / 8), footer 'Cosan Lubrificantes e Especialidades SA, Authorized Distributor of S-Oil Base Stocks'", printed_date='not printed', kind='distributor-issued copy of manufacturer typicals', read='whole page', limits=''),
                    'DL2-15428.pdf': dict(what='ExxonMobil Product Datasheet SpectraSyn 10', printed_date='Revision Date 07/01/2019', kind='manufacturer data sheet (later edition)', read='both pages', limits=''),
                    S2: dict(what='ExxonMobil MSDS SPECTRASYN 2', printed_date='14 Nov 2011', kind='manufacturer SDS', read='all 10 pages; sections 1-3, 9 in full', limits='in-house methods'),
                    E: dict(what='ExxonMobil MSDS SPECTRASYN ELITE 150', printed_date='26 Sep 2012', kind='manufacturer SDS', read='all 9 pages; sections 1-3, 9 in full', limits='in-house methods'),
                    'DL2-13823.pdf': dict(what="TEXOL Lubritech FZC MSDS 'BASE OIL ULTRA S3'", printed_date='Revision Date 29 January 2023', kind='third-party MSDS', read='all 6 pages', limits='not an S-OIL document'),
                    X: dict(what="ExxonMobil 'EHC Series' sales specifications (EHC 45 / 50 / 65 / 110)", printed_date='06-2018 (printed 27.10.2018)', kind='manufacturer data sheet (earlier edition)', read='both pages; p.1 as an image', limits='labelled SDS in the inventory'),
                    'DL2-11786.pdf': dict(what="ExxonMobil 'EHC Series' web print", printed_date='4/29/2019', kind='manufacturer data sheet (identical text to the cited DL2-11785.pdf)', read='all 3 pages compared word by word', limits='labelled SDS in the inventory')},
         links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzz_dup_nevercited_1_eleventh_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
