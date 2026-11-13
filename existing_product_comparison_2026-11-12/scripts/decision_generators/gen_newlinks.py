# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
WD = "word by word and number by number (difflib) against the cited TDS"


def L(p, f, cat, fs, cov, idn, note=''):
    return dict(p=p, f=f, cat=cat, status='completed', fields_status=fs, coverage=cov, identity=idn, note=note)


links = [
    L('RICHFUL_RF6066', 'DL2-15743.pdf', 'B', 'p.7 read in full and compared ' + WD + ' DL2-15451.pdf', 'same content as DL2-15451.pdf (only the page number differs); every value already in the JSON', "exact: catalogue page 'RF6066 CH-4/CI-4 Diesel Engine Oil Package'"),
    L('RICHFUL_RF6066', 'DL2-15764.pdf', 'B', 'p.7 read in full and compared ' + WD + ' DL2-15451.pdf', "same content as DL2-15451.pdf (page number and column heading 'Requirement / Limit' only)", 'exact'),
    L('RICHFUL_RF6066', 'DL2-15546.pdf', 'B', 'p.6 read in full and compared ' + WD + ' DL2-15451.pdf', "same content as DL2-15451.pdf (only spacing in method codes, e.g. 'GB/T265', and the page number differ)", 'exact'),
    L('RICHFUL_RF6078', 'DL2-15764.pdf', 'B', 'p.12 read in full and compared word by word with RF6078%20-%20TDS.pdf (ratio 1.000)', "identical text to the cited TDS 'RF6078 - TDS.pdf' (ACEA E7/API CI-4 10.85 %; API CI-4 Plus 11.85 %); second printing of that version", 'exact'),
    L('RICHFUL_RF6078', 'DL2-15743.pdf', 'E', 'p.12 read in full and compared ' + WD + ' DL2-15832.pdf and RF6078%20-%20TDS.pdf', "values (density, KV100, flash, TBN, Ca, Zn, P, Mo) equal both TDS; treat-rate table differs from both: only 'CI-4 | 15W-40, 20W-50 | 10.85%' (no ACEA E7, no CI-4 Plus, no 10W grades); density method SH/T 0604", 'exact', 'A narrower edition; see the treat-rate field row.'),
    L('RICHFUL_RF6078', 'DL2-15546.pdf', 'E', 'p.9 read in full and compared ' + WD + ' DL2-15832.pdf', "as DL2-15743.pdf: values equal; treat rate 'CI-4 | 15W-40, 20W-50 | 10.85%' only; also lists the 8 API CI-4 engine tests passed by a 15W-40 Group II / OCP oil (Cat 1K, Cat 1R, Mack T-8E, IIIH70, EOAT, Cummins ISM, RFWT, Mack T-12)", 'exact'),
    L('RICHFUL_RF6079', 'DL2-15743.pdf', 'E', 'p.13 read in full and compared ' + WD + ' DL2-15535.pdf', "values equal the TDS and the JSON; this edition prints only 'API CI-4/ ACEA E7 | 15W-40/20W-50 | 9.15%' (no 10W-30/10W-40 9.50 % row, no 15W-50) and other method citations (density SH/T 0604; N SH/T 0704 / ASTM D5762 instead of SH/T 0656 / ASTM D5291)", 'exact', 'Narrower grade list; nothing proposed (no value differs; absence of a row is not a conflict).'),
    L('RICHFUL_RF6079', 'DL2-15764.pdf', 'B', 'p.13 read in full and compared ' + WD + ' DL2-15535.pdf', 'same values and treat-rate table as DL2-15535.pdf; only the column heading and the density method citation (SH/T 0604 vs GB/T 13377) differ', 'exact'),
    L('RICHFUL_RF6088', 'DL2-15743.pdf', 'E', 'p.14 read in full and compared ' + WD + ' DL2-15452.pdf', "all values equal the TDS except Ca 1.45-1.77 / 1.61 m% (TDS and JSON 1.37-1.69 / 1.53); claim is API CK-4 only ('required by ASTM D4485'), no ACEA E11; treat rate CK-4 10W-30, 10W-40, 15W-40 13.8 %", 'exact', 'See the Ca field row.'),
    L('RICHFUL_RF6088', 'DL2-15764.pdf', 'B', 'p.14 read in full and compared ' + WD + ' DL2-15452.pdf', "same content as DL2-15452.pdf (heading 'CK-4/E11'; column heading and density method SH/T 0604 differ); Ca 1.37-1.69 / 1.53", 'exact'),
    L('RICHFUL_RF6400', 'DL2-15764.pdf', 'B', 'p.5 read in full and compared ' + WD + ' DL2-15849.pdf', 'same content as DL2-15849.pdf (CF-4/SG 5.5 %; column heading only)', 'exact'),
    L('RICHFUL_RF6400', 'DL2-15743.pdf', 'E', 'p.5 read in full and compared ' + WD + ' DL2-15849.pdf', "identical to DL2-15849.pdf except the CF-4/SG treat rate '6%' (TDS 5.5%)", 'exact', 'See the treat-rate field row.'),
    L('RICHFUL_RF6400', 'DL2-15546.pdf', 'E', 'p.18 read in full and compared ' + WD + ' DL2-15849.pdf', "identical values except CF-4/SG '6%' (TDS 5.5%); wording differences only otherwise", 'exact'),
    L('RICHFUL_RF6400', 'DL2-12243.pdf', 'E,F', 'p.22 read in full (and p.1 contents) and compared with DL2-15849.pdf', "older-style catalogue page (typicals only, no limits, 'Treating Rate (mass%)'): CF-4/SG 6 %, other treat rates equal (2.80/4.20/2.70/3.50/2.50/2.6/1.60 %); typicals differ: density 1046 (TDS 1039), KV100 90 (109), TBN 162 (168), Ca 5.4 (5.94); Zn 1.9 equal; no P or N; storage 50/60 C (TDS 45/65 C)", "exact: 'RF6400 Universal Type Engine Oil Package'", 'Undated; different edition of the RF6400 data. See field rows.'),
    L('RF6602', 'DL2-15744.pdf', 'E', 'p.51 read in full and compared ' + WD + ' DL2-14874.pdf', 'all values equal the TDS (KV100 1100-1850 / 1360, flash >=180 / 210, colour < 0.5, density 850-950 / 919); performance tests omitted; storage differs: short-term max 60 C (TDS 75 C), shelf life 2 years (TDS 24 months)', "exact: 'RF6602 PMA Viscosity Index Improver'"),
    L('RF6602', 'DL2-15766.pdf', 'E', 'p.52 read in full and compared with DL2-14874.pdf and the JSON', 'new: PSSI (10 % in 150N) ultrasonic 6 (SH/T 0505), diesel nozzle 30 cycles 5 and 250 cycles 8 (DIN 51382), KRL 20 h 54 (CEC L-45-A-99); thickening table 0/1/5 % in 150N / 500N / Group III 6# (KV values equal the TDS rounded to 0.1; VIs differ, e.g. 150N 0 % 108 vs 110); typical flash 180 C (TDS typical 210, SDS 160); typicals only (no limits)', "exact: 'RF6602 Polymethacrylate Viscosity Index Improver'", 'See field rows.'),
    L('RF6602', 'RF5016-Booklet.pdf', 'D', 'p.14 recipe line read (text layer); other pages concern RF5016', "recipe share only ('RF6602 (VII), wt% 3 / 3.5' in an RF5016 hydraulic-oil formulation); not a property of RF6602; NOT ASSESSED beyond p.14", "printed 'RF6602（VII）' in a Richful booklet"),
    L('S_OIL_PREMIUM_P_31', 'DL2-12545.pdf', 'E', 'p.6 Premium table viewed as an image (ninth pass, zzzzzzzzz_soil_brochure_ninth_pass.json)', 'legible cells equal the JSON (cited DL2-11173.pdf): KV40 30.14, KV100 5.189, VI 101, flash 212; pour-point sign and some specific-gravity digits illegible, not compared', "exact: 'P-31 (Premium 150N)'", 'Link added in the tenth pass (missed by the same-page supplier rule).'),
]
F = []


def R(p, tier, path, old, nf, np_, nt, unit, form, qual, meth, outc, act, reason, orv, cmp, cond='', basis=''):
    F.append(dict(p=p, tier=tier, path=path, old=old, new_f=nf, new_p=np_, new_text=nt, unit=unit, form=form, qual=qual, method=meth, cond=cond, basis=basis,
                  outcome=outc, action=act, reason=reason, old_rev=orv, cmp_override=cmp))


R('RICHFUL_RF6088', 2, 'elements.Ca', "DL2-15452.pdf (TDS, undated) read: 'Ca Content, m% | 1.37-1.69 | 1.53 | GB/T 17476, ASTM D4951'. JSON Ca 1.53 (1.37-1.69).", 'DL2-15743.pdf', 14,
  "'Ca Content, m% | 1.45-1.77 | 1.61 | GB/T 17476, ASTM D4951' (catalogue, undated). DL2-15764.pdf p.14 prints 1.37-1.69 / 1.53.", 'm%', 'specification limits and typical (manufacturer catalogue, undated)', 'limits + typical',
  'GB/T 17476, ASTM D4951', 'changed_or_conflicting', 'propose_record_conflict',
  'Two manufacturer printings differ (1.45-1.77 / 1.61 vs 1.37-1.69 / 1.53); none is dated. Propose recording a conflict with DL2-15743.pdf on one side and DL2-15452.pdf + DL2-15764.pdf on the other; the JSON value stays; not averaged; no edition order assumed.',
  're-read manually: DL2-15452.pdf whole page (text layer)', 'existing: Ca 1.53 (1.37-1.69) from DL2-15452.pdf')
R('RICHFUL_RF6400', 1, 'treat_rate_matrix[0].treat_rate_wt_pct', "DL2-15849.pdf (TDS, undated) read: 'CF-4/SG 5.5%'. JSON 5.5 '%' (basis not stated). The field-test report (RF6400 booklet p.2) also uses 'the dosage of 5.5%'.", 'DL2-15743.pdf', 5,
  "'CF-4/SG 6%' in DL2-15743.pdf p.5 and DL2-15546.pdf p.18; DL2-12243.pdf p.22 'API Performance Level | Treating Rate (mass%) | CF-4/SG 6%'. DL2-15764.pdf p.5 prints 5.5%.", '%', 'recommended treat rate (manufacturer documents, undated)', '', '',
  'changed_or_conflicting', 'propose_record_conflict',
  "Richful documents print 6 % (three catalogue printings) and 5.5 % (two TDS, one catalogue, the field-test report) for CF-4/SG. None is dated; propose recording the conflict with all citations; the JSON row stays at 5.5 %. The 'mass%' heading of DL2-12243.pdf belongs to the 6 % edition and is NOT transferred to the 5.5 % row (route-matched basis policy).",
  're-read manually: DL2-15849.pdf whole page (text layer)', "existing: CF-4/SG 5.5 '%' from DL2-15849.pdf")
for path, unit, old_v, typ, new_v, lab in [('density', 'kg/m3', '1019-1059 / 1039 (SH/T 0604, ASTM D4052)', '1039', '1046 (ASTM D4052)', 'Density (20 C), kg/m3'),
                                           ('kv100', 'mm2/s', 'Report / 109', '109', '90', 'Kinematic Viscosity (100 C), mm2/s'),
                                           ('tbn', 'mgKOH/g', '155-181 / 168', '168', '162', 'Total Base Number, mgKOH/g'),
                                           ('elements.Ca', 'm%', '5.35-6.53 / 5.94', '5.94', '5.4', 'Ca Content, m%')]:
    R('RICHFUL_RF6400', 2, path, f"DL2-15849.pdf (TDS, undated) read: '{lab} | {old_v}'. JSON equals the TDS.", 'DL2-12243.pdf', 22,
      f"'{lab} | {new_v}' (typical only; 'Product Quality Characteristics & Test Method', older-style Richful catalogue, undated)", unit,
      'typical (older-style manufacturer catalogue, undated; no limits)', 'typical', 'as printed', 'changed_or_conflicting', 'propose_record_conflict',
      f'An older-style Richful catalogue prints a different typical ({new_v} vs {typ}). Neither document is dated; propose recording a conflict with both sources; the JSON keeps the TDS value; no edition order assumed (the older layout is not a date).',
      're-read manually: DL2-15849.pdf whole page (text layer)', f'existing: {old_v} from DL2-15849.pdf')
R('RICHFUL_RF6078', 1, 'treat_rate_matrix[0].treat_rate_wt_pct',
  "DL2-15832.pdf read: 'ACEA E7/API CI-4 | 10W-30, 10W-40, 15W-40, 20W-50 | 11.85%' and 'API CI-4 | ... | 10.85%'; RF6078%20-%20TDS.pdf: 'ACEA E7/API CI-4 ... 10.85%' and 'API CI-4 Plus ... 11.85%'. JSON: row [0] ACEA E7/API CI-4 value null with an unresolved conflict 11.85 vs 10.85.",
  'DL2-15764.pdf', 12, "DL2-15764.pdf p.12 (identical to RF6078 - TDS.pdf): 'ACEA E7/API CI-4 ... 10.85%; API CI-4 Plus ... 11.85%'. DL2-15743.pdf p.12 and DL2-15546.pdf p.9: 'CI-4 | 15W-40, 20W-50 | 10.85%' only.",
  '%', 'recommended treat rate (manufacturer documents, undated)', '', '', 'changed_or_conflicting', 'propose_record_conflict',
  'Add DL2-15764.pdf as a second printing of the 10.85 % / CI-4 Plus 11.85 % version to the existing conflict; DL2-15743.pdf and DL2-15546.pdf state only CI-4 15W-40/20W-50 at 10.85 % (they do not address ACEA E7). The conflict stays unresolved; no edition order assumed.',
  're-read manually: DL2-15832.pdf whole page (text layer) and RF6078%20-%20TDS.pdf p.1', 'existing: row [0] null; conflict 11.85 (DL2-15832.pdf) vs 10.85 (RF6078 - TDS.pdf)')
R('RF6602', 2, 'shear_stability', "DL2-14874.pdf (TDS, undated) read: only 'The Shear of Diesel Injector Nozzle' KV100 before/after (6 % and 10 % in 150N), no SSI. JSON shear_stability: 'KV100 viscosity loss, % (calculated; no SSI printed)'.",
  'DL2-15766.pdf', 52, "'PSSI (10% treat rate in 150N) | Ultrasonic shear 6 | SH/T 0505; Diesel nozzle 30 cycles 5 | DIN51382; Diesel nozzle 250 cycles 8 | DIN51382; KRL 20h 54 | CEC L-45-A-99' (column 'Typical Value')",
  'PSSI', 'typical (manufacturer catalogue, undated)', 'typical', 'SH/T 0505; DIN 51382; CEC L-45-A-99', 'additional', 'propose_add',
  "Printed PSSI values with methods and test conditions (10 % in 150N) fill the gap noted in the JSON ('no SSI printed'). Propose adding them as four shear-stability entries with their methods; the calculated KV100 losses stay as they are.",
  're-read manually: DL2-14874.pdf whole page (text layer)', 'existing: calculated KV100 loss only; no SSI', cond='10 % RF6602 in 150N')
R('RF6602', 1, 'open_questions', "DL2-14874.pdf: flash point (COC) index '≮180', typical 210 C (ASTM D92); thickening table VIs 150N 0/1/3/5 %: 110/123/138/157; storage short-term <= 75 C. JSON open questions record TDS 210 vs SDS 160 C and the storage difference.",
  'DL2-15766.pdf', 52, "'Flash Point (COC), C | 180 | GB/T 3536' (typical column; no limit); thickening VIs 150N 0/1/5 %: 108/124/155, 500N 100/104/126, Group III 6# 137/148/176. DL2-15744.pdf p.51: storage short-term max 60 C, long-term 45 C.",
  'C', 'typical (manufacturer catalogue, undated)', 'typical', 'GB/T 3536', 'changed_or_conflicting', 'propose_open_question_update',
  'No template field holds flash point or VI of the thickening blends. Propose adding to the existing open questions: a third flash value (catalogue typical 180 C vs TDS typical 210 C vs SDS 160 C), VIs that differ from the TDS for the same blends (KV values agree to 0.1), and the 60 C short-term storage limit of DL2-15744.pdf (TDS 75 C). Not resolved.',
  're-read manually: DL2-14874.pdf whole page (text layer)', 'existing: open questions on flash (210 vs 160) and storage')
d = {"batch": "Richful + S-OIL: the 18 links added by the reviewed generic-alias mapping (tenth pass)", "reviewed_on": "2026-11-13 (tenth pass)",
     "note": "The 18 pairs admitted by scripts/reviewed_generic_alias_pairs.json were reviewed: each product page read in full and compared word by word and number by number (scratchpad helper wdiff.py, difflib) with the cited TDS; old TDS re-read in full (DL2-15451, DL2-15832, RF6078 - TDS.pdf, DL2-15535, DL2-15452, DL2-15849, DL2-14874). Catalogue editions are undated: no edition order is assumed and no value is preferred by layout.",
     "documents": {"DL2-15546.pdf": {"what": "Richful catalogue (Company Profile; 36 pp.), another undated edition", "printed_date": "not printed", "kind": "manufacturer product catalogue", "read": "pp.1-2 and product pages 6 (RF6066), 9 (RF6078), 18 (RF6400) in full", "limits": "other pages not reviewed"},
                   "DL2-12243.pdf": {"what": "Richful catalogue, older layout (contents p.1; RF6400 on p.22)", "printed_date": "not printed", "kind": "manufacturer product catalogue", "read": "p.1 contents and p.22 in full", "limits": "other pages not reviewed"},
                   "DL2-15744.pdf": {"what": "Richful catalogue (Company Profile; 83 pp.)", "printed_date": "not printed", "kind": "manufacturer product catalogue", "read": "pp.1, 3 and 51 (RF6602) in full", "limits": "other pages not reviewed"},
                   "DL2-15766.pdf": {"what": "Richful catalogue (Company Profile; 85 pp.)", "printed_date": "not printed", "kind": "manufacturer product catalogue", "read": "pp.1, 3 and 52 (RF6602) in full", "limits": "other pages not reviewed"},
                   "RF5016-Booklet.pdf": {"what": "Richful RF5016 hydraulic-oil compound booklet (Issue Date 2025/2/20)", "printed_date": "2025/2/20", "kind": "manufacturer booklet (another product)", "read": "p.1 and p.14 recipe table", "limits": "RF5016 content not reviewed"}},
     "links": links, "fields": F}
json.dump(d, open('existing_product_comparison_2026-11-12/decisions/zzzzzzzzzz_richful_new_links_tenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
