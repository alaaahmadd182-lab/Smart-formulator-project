# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json, csv
B = 'existing_product_comparison_2026-11-12'
links, F = [], []


def L(p, f, cat, fs, cov, idn, note=''):
    links.append(dict(p=p, f=f, cat=cat, status='completed', fields_status=fs, coverage=cov, identity=idn, note=note))


def R(p, tier, path, old, nf, np_, nt, unit, form, act, reason, orv, cmp, outc='additional', qual='', meth='', cond='', basis=''):
    F.append(dict(p=p, tier=tier, path=path, old=old, new_f=nf, new_p=np_, new_text=nt, unit=unit, form=form, qual=qual, method=meth, cond=cond, basis=basis, outcome=outc, action=act, reason=reason, old_rev=orv, cmp_override=cmp))


led = list(csv.DictReader(open(f'{B}/tables/progress_ledger.csv', encoding='utf-8')))
open_ = {(r['product_id'], r['file']) for r in led if r['relationship_status'] == 'not yet assessed'}
# Eni
L('ENI_MX_5212', 'DL2-11130.PDF', 'E', 'both pages read (text layer); p.1 table as an image',
  "Eni Triple Tech brochure (02/2017): 'CF-4/SJ: Eni MX 5612B 5.42% + Eni MX 5612C 1.53% = 6.95% / Eni MX 5212'; CF-4/SM 1.20 + 5.42 + 1.53 = 8.15 % and CF-4/SL 0.50 + 5.42 + 1.53 = 7.45 % agree with the JSON rows '6.95% + 1.20% / + 0.50% Eni MX 5612A'; part-package data p.2 belong to MX 5612A/B/C",
  "printed 'Eni MX 5212' as the single-package equivalent", 'See the composition note row.')
R('ENI_MX_5212', 1, 'route_selector_restrictions', "DL2-14981.pdf (02/2017): 'Eni MX 5212 can be used alone or with a specific booster (Eni MX 5612 A) to have a cascade system.'", 'DL2-11130.PDF', 1,
  "Table 2 (image checked): 'CF-4/SJ | Eni MX 5612A - | 5612B 5.42% | 5612C 1.53% | 6.95% | Eni MX 5212'; 'CF-4/SM | 1.20% / 5.42% / 1.53% | 8.15%'; 'CF-4/SL | 0.50% / 5.42% / 1.53% | 7.45%'",
  '%', 'manufacturer brochure (02/2017)', 'propose_note',
  'Propose a note that the brochure presents Eni MX 5212 at 6.95 % as equivalent to the part-packages 5612B 5.42 % + 5612C 1.53 %; the booster rows reproduce the JSON treat rates (8.15 and 7.45 % in total). Nothing is derived from the equivalence.',
  're-read manually: DL2-14981.pdf as quoted in the JSON (treat-rate rows with Eni MX 5612A)', 'existing: cascade with 5612A only')
L('ENI_MX_5217', 'DL2-11127.pdf', 'F', 'both pages read and compared word by word with the cited DL2-12630.pdf (03/2017); p.1 as an image',
  "earlier edition (02/2017, EN 5030-01): two treat-rate columns only (13.6 %: CH-4 / CI-4 level, E4/E7-12, MB 228.5, M 3277, MTU Type 3 level, VDS-2, Renault RVI RD, CES 20078; 9.6 %: CG-4/SJ, E3-96, MB 228.3, M 3275, MTU Type 2 level, Renault RVI RD); the 03/2017 edition adds the 11.6 % column; p.2 technical data identical to the cited edition and the JSON; footnote '(*) Official approval pending in SAE 10W-40 formulation'",
  "exact: 'Eni MX 5217'", 'Earlier edition; nothing proposed (the JSON follows the later 03/2017 edition).')
# ExxonMobil spreadsheet
XL = {'SPECTRASYN_40': 39, 'SPECTRASYN_100': 100, 'SPECTRASYN_10': 10, 'SPECTRASYN_2': 1.7, 'SPECTRASYN_2B': 1.8, 'SPECTRASYN_2C': 2, 'SPECTRASYN_4': 4.1, 'SPECTRASYN_5': 5.1, 'SPECTRASYN_6': 5.8, 'SPECTRASYN_8': 8,
      'SPECTRASYN_ELITE_150': 156, 'SPECTRASYN_ELITE_300': 303, 'SPECTRASYN_ELITE_65': 65, 'SPECTRASYN_PLUS_4': 3.9, 'SPECTRASYN_PLUS_6': 5.9, 'SYNESSTIC_12': 12.4, 'SYNESSTIC_5': 4.7,
      'ESTEREX_A32': 2.8, 'ESTEREX_A34': 3.2, 'ESTEREX_A41': 3.6, 'ESTEREX_A51': 5.4, 'ESTEREX_NP343': 4.3, 'ESTEREX_NP451': 5, 'ESTEREX_P61': 5.4, 'ESTEREX_P81': 8.3, 'ESTEREX_TM111': 11.9}
for k, v in XL.items():
    p = 'EXXONMOBIL_' + k
    if (p, 'DL2-12146.xlsx') in open_:
        L(p, 'DL2-12146.xlsx', 'E', "all cells of the single sheet 'EXXON MOBIL' read (openpyxl, read-only)",
          f"compiled product / application matrix (no issuer, date or method): 'Kinematic Viscosity @ 100 C (cSt)' {v} - equal to the JSON kv100; application flags 'P' are set per product-type group (first row of each group), not per grade, and have no template field",
          'product name in the sheet', 'Corroborates the KV100 only; issuer unidentified; nothing proposed.')
if ('EXXONMOBIL_APE_SN_500', 'DL2-12146.xlsx') in open_:
    L('EXXONMOBIL_APE_SN_500', 'DL2-12146.xlsx', 'C', 'all cells read', "name only in the 'Group I basestocks' list (no value, no flag)", "printed 'AP/E SN 500'")
for k in ('SPECTRASYN_100', 'SPECTRASYN_40', 'SPECTRASYN_6', 'SPECTRASYN_ELITE_150', 'SPECTRASYN_ELITE_65'):
    if ('EXXONMOBIL_' + k, 'DL2-11911.pdf') in open_:
        L('EXXONMOBIL_' + k, 'DL2-11911.pdf', 'D', 'both pages read (text layer)', "'Blending Study: KV at 40 C, HiVis component % / SpectraSyn 6 (Source: ExxonMobil data)': charts without numeric data in the text layer; blend behaviour, not a property of the neat product", 'product name as a chart legend')
# BRB
L('BRB_PETROLAD_8099', 'DL2-11052.pdf', 'D,E', 'all 3 pages read (text layer)',
  "Petrolad 8003B booster TDS (issue date May 8, 2015): 'Performances of Petrolad 8099' at 11.2 % wt (CH-4, CF-4/SJ; E7-04/08; JASO DH-1; Global DHD-1; VDS-3; Mack EO-M +; MB 228.2/3; MAN 3275; Cummins CES 20076/71/72) - an earlier list than the cited 8099 TDS (2016-05-31: E7-12, MB 228.3 blanket approval, MAN 3275-1, CI-4 in Group II, CES 20078, DDC 93K215, Allison C4); booster route 8099 + 8003B; VII Viscotech 6540",
  "printed 'Petrolad 8099' in the BRB 8003B data sheet", 'See the route row.')
R('BRB_PETROLAD_8099', 1, 'route_selector_restrictions', "DL2-11053.pdf (8099 TDS, 2016-05-31): 'It can be used in formulations combined with our Viscotech 6540 VI improver.'; claims at 11.2 % wt alone (CI-4 in a Group II formulation).", 'DL2-11052.pdf', 2,
  "'Performances Petrolad 8099 (11.2 % wt.) boosted with Petrolad 8003B (1.7 % wt.)': CI-4/SL 11.2 + 1.7; CG-4 9.3 + 1.4; Cummins 20077/78 11.2 + 1.7; MTU Type 2 11.2 + 1.7; Renault Truck RLD-2 11.2 + 1.7; p.1 'Petrolad 8099 with Petrolad 8003B is formulated for use with Viscotech 6540 VI improver.'",
  '% wt', 'manufacturer data sheet of the booster (May 2015)', 'propose_add_route_bound',
  'Propose recording the booster route (8099 + 8003B doses per claim) as a separate route; the 2016 claims of 8099 alone are unchanged; the 2015 list of 8099-alone claims is older wording and is not proposed.',
  're-read manually: DL2-11053.pdf as quoted in the JSON (claims table, VII statement)', 'existing: 8099 alone at 11.2 % wt; VII Viscotech 6540', basis='mass (printed % wt)')
# BAPCO certificates
for p, f, date, cert, vals, dens in (('BAPCO_BAPBASE_6', 'DL2-14114.pdf', '5-JUN-2020 sampled, 7-JUN-2020 certified, issued 15-JUL-2020', '849968',
                                      'CCS -30 C 3826; colour L 0.5; Saybolt +29; density 15 C 0.8398 kg/liter; flash COC 236; flash PMCC 227; pour (D5950) -16; Noack 7.8; UV 280-350 nm 0.185 / 0.117 / 0.077 / 0.054; KV100 6.046; KV40 32.55; VI 134; water 27 mg/kg; SG 60/60 F 0.8402; saturates (D7419) 99.4; sulfur (D5453) 2.1 mg/kg', '0.8398'),
                                     ('BAPCO_BAPBASE_8', 'DL2-14119.pdf', '17-JUN-2020 sampled, 18-JUN-2020 certified, issued 15-JUL-2020', '700476',
                                      'CCS -30 C 8365; colour L 0.5; Saybolt +29; density 15 C 0.8443; flash COC 260; pour -14; Noack 2.5; UV 0.088 / 0.080 / 0.090 / 0.030; KV100 7.906; KV40 48.32; VI 133; water 14; SG 0.8447; saturates 99.4; sulfur 1.0', '0.8443')):
    L(p, f, 'E', 'whole page read (text layer)', f'Bapco laboratory report / test certificate (form BP0209 (04/16)), {date}, Certified By {cert}: {vals}; every batch value conforms to the specification limits in the JSON (2017 specification images); density is not in the JSON',
      f"printed '{p.split('_')[-1]} cst' (BAPBASE), www.bapco.net", 'Batch evidence only.')
    R(p, 1, 'density', f"Specification image cited by the JSON (2017-08-17): no density row. JSON density Missing.", f, 1, f"'Density@ 15 deg C, kg/liter | ASTM D4052 | {dens}' (Bapco test certificate, {date.split(',')[1].strip()})", 'kg/liter',
      'batch measurement (single manufacturer test certificate)', 'propose_open_question_update',
      'A single batch result cannot fill the mandatory density; propose recording it in an open question as batch evidence with the certificate identifiers.', 're-read manually: the JSON printed_text of the 2017 specification image (no density row)', 'existing: density Missing', meth='ASTM D4052', cond='15 C')
for f, date in (('DL2-14773.pdf', '08-December-2020, batch TRAF4-201208, ref N2020-17163'), ('DL2-14775.pdf', 'February-2021, batch TRAF1-210219, ref N2021-02889')):
    L('NYNAS_NYFROST_32', f, 'E', 'whole page read (text layer)',
      f"certificate of analysis ({date}): density 15 C, KV40, flash PM (D93A), colour, TAN, refractive index, carbon-type composition (D2140 C_A / C_N / C_P), breakdown voltage, water; batch values inside the JSON specification limits (KV40 28.8-35.2, density 0.896-0.916, flash PM min 174); D2140 %C_A is not the template's aromatics quantity; nothing proposed",
      "printed 'Nyfrost 32'", 'Batch evidence only; no Missing field that a batch value could inform except through ring analysis, which is a different quantity.')
# AP/E Core 2500 (same table as Core 150 / 600 in the ninth pass)
L('EXXONMOBIL_APE_CORE_2500', 'RF6508%20Booklet.pdf', 'D,E', 'p.7 base-stock table read in full (text layer); pp.8, 11 recipe tables',
  "p.7 row 'ExxonMobil AP/E Core 2500 | I | 31.92 | 480.5 | 97 | 41.9 | 1.12' (KV100, KV40, VI, saturates %, sulfur wt.%): KV100 inside the JSON 30.6-32.7; VI 97 >= 95; KV40, saturates and sulfur are Missing in the JSON", "printed 'ExxonMobil AP/E Core 2500', Group I", 'Third-party characterisation without lot number.')
R('EXXONMOBIL_APE_CORE_2500', 3, 'saturates', "DL2-13265.pdf (05-2020) read: CORE 2500 limits only (KV100 30.6-32.7, VI 95 min, flash 294 min, pour -6 max, colour 6 max); no KV40, saturates or sulfur. JSON those Missing.", 'RF6508%20Booklet.pdf', 7,
  "'ExxonMobil AP/E Core 2500 | I | 31.92 | 480.5 | 97 | 41.9 | 1.12' under 'Base Stock Information' (KV100 D445, KV40 D445, VI D2270, Saturates % D2007, Sulfur wt.% D2622)", '%; wt.%; mm2/s',
  'third-party characterisation (additive supplier booklet, no lot number)', 'propose_open_question_update',
  'As for AP/E Core 150 / 600 (ninth pass): not a manufacturer value; propose an open-question note citing it.', 're-read manually: DL2-13265.pdf p.1 whole text layer (AP/E CORE specifications, 05-2020)', 'existing: saturates, sulfur, KV40 Missing')
# GS Caltex in the NeoFlex sheet
L('GS_CALTEX_600N', 'DL2-15627.pdf', 'D,E', 'p.2 read in full (text layer)', "Dowpol NeoFlex 680 PPD data (Revision Date April, 2018): neat pour point of 'GS-Caltex 600N' -12 C (0.2 % PPD -31 C); method not printed; the JSON typical is -14 C with specification max -12 C: observation only",
  "printed '600N | GS-Caltex'")
L('GS_CALTEX_150N', 'DL2-15627.pdf', 'G', 'p.2 read in full', 'not applicable', "FALSE MATCH: the 150N columns are SinoPec-Shanghai, Formosa, CNCOOC, SinoPec-Maoming and HDS; 'GS-Caltex' is named only for the 600N column")
# NEXBASE: identifier observation
nx = json.load(open(f'{B}/decisions/zzzzzzzzzz_nexbase_tds_full_read_tenth_pass.json', encoding='utf-8'))
for l in nx['links']:
    if l['f'] == 'DL2-14397.pdf':
        l = dict(l)
        l['note'] += (" Observation (tenth pass): the Bapco test certificate DL2-14119.pdf (BAPBASE 8, form BP0209) is also 'Certified By 700476' and uses the same fields (Tank Number, Date Sampled, Date Certified, Certified By); "
                      "this suggests the same laboratory issued DL2-14397.pdf, but the issuer is still not printed on DL2-14397.pdf, so it remains unidentified. It does not change the independence assessment (independence unverified).")
        links.append(l)
d = dict(batch='Eni, ExxonMobil spreadsheet and blending study, BRB, BAPCO and Nyfrost certificates, AP/E Core 2500, GS Caltex in a PPD sheet (tenth pass)', reviewed_on='2026-11-13 (tenth pass)',
         note='Single-document batches; each document read in full on the pages stated.', documents={
             'DL2-11130.PDF': dict(what='Eni Triple Tech multipurpose additive packages brochure', printed_date='02/2017', kind='manufacturer brochure', read='both pages; p.1 as an image', limits=''),
             'DL2-11127.pdf': dict(what='Eni MX 5217 data sheet, EN 5030-01', printed_date='02/2017', kind='manufacturer data sheet (earlier edition)', read='both pages; p.1 as an image', limits=''),
             'DL2-12146.xlsx': dict(what="spreadsheet 'EXXON MOBIL': products, KV100, application flags", printed_date='not printed', kind='compiled product list (issuer not identified)', read='all cells (openpyxl, read-only)', limits='no issuer, date or methods'),
             'DL2-11052.pdf': dict(what='BRB Petrolad 8003B diesel engine oil performance booster data sheet', printed_date='May 8, 2015', kind='manufacturer data sheet (booster)', read='all 3 pages', limits=''),
             'DL2-14114.pdf': dict(what='Bapco laboratory report / test certificate BAPBASE 6 cst', printed_date='issued 15-JUL-2020', kind='manufacturer batch certificate', read='whole page', limits='tank number not legible in the text layer'),
             'DL2-14119.pdf': dict(what='Bapco laboratory report / test certificate BAPBASE 8 cst', printed_date='issued 15-JUL-2020', kind='manufacturer batch certificate', read='whole page', limits=''),
             'DL2-14773.pdf': dict(what='Certificate of analysis Nyfrost 32, batch TRAF4-201208', printed_date='08-December-2020', kind='batch certificate', read='whole page', limits='issuer partly illegible'),
             'DL2-14775.pdf': dict(what='Certificate of analysis Nyfrost 32, batch TRAF1-210219 (Inspectorate Antwerp)', printed_date='February-2021', kind='batch certificate', read='whole page', limits=''),
             'DL2-15627.pdf': dict(what='Dowpol NeoFlex 680 pour point depressant data', printed_date='April 2018', kind='additive supplier data sheet', read='p.2', limits='')},
         links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzz_singles_tenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
