"""Nineteenth pass, batch 34: open non-duplicate (category D) links of five additive-supplier formulation documents
(Infineum 2019 driveline / motorcycle / gas-engine deck DL2-12999; Oronite OLOA 54xxx formulation deck DL2-13852; Afton
HiTEC 11455 GF-7 / SQ support document DL2-15799; Infineum D341X typical formulations DL2-15564 and DL2-15332).
Every name-hit page of each document was read in full on the text layer (all open products together); other pages were
not read. Writes decisions/zzzzzzzzzzzzzzzzzzz_b34_nondup_formulation_decks_1_nineteenth_pass.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nd_common import Batch, T, to_root
to_root()

FROZEN = [
('DL2-12999.pdf', 'CHEVRON_GROUP_II_100R', 'D', '8,14,16,26', 'Chevron 100R', '44'),
('DL2-12999.pdf', 'CHEVRON_GROUP_II_220R', 'D', '14,26,41', 'Chevron 220R', '44'),
('DL2-12999.pdf', 'CHEVRON_GROUP_II_600R', 'D', '26,41', 'Chevron 600R', '44'),
('DL2-12999.pdf', 'EXXONMOBIL_EHC_120', 'D', '23', 'EHC 120', '44'),
('DL2-12999.pdf', 'EXXONMOBIL_EHC_50', 'D', '23', 'EHC 50', '44'),
('DL2-12999.pdf', 'NESTE_NEXBASE_3030', 'D', '6,9,10,13,14', 'Nexbase 3030', '44'),
('DL2-12999.pdf', 'NESTE_NEXBASE_3043', 'D', '6,8', 'Nexbase 3043', '44'),
('DL2-12999.pdf', 'NESTE_NEXBASE_3060', 'D', '9,10', 'Nexbase 3060', '44'),
('DL2-12999.pdf', 'NESTE_NEXBASE_3080', 'D', '6,11,13', 'Nexbase 3080', '44'),
('DL2-12999.pdf', 'YUBASE_3', 'D', '6,8,9,13', 'Yubase 3', '44'),
('DL2-12999.pdf', 'YUBASE_4', 'D', '8,11,14,16', 'Yubase 4', '44'),
('DL2-12999.pdf', 'YUBASE_6', 'D', '6,8,9,14,16', 'Yubase 6', '44'),
('DL2-13852.pdf', 'CHEVRON_GROUP_II_100R', 'D', '19,20', 'CHEVRON 100R', '47'),
('DL2-13852.pdf', 'CHEVRON_GROUP_II_220R', 'D', '17,18,19,20', 'Chevron 220R', '47'),
('DL2-13852.pdf', 'CHEVRON_GROUP_II_600R', 'D', '19,20', 'CHEVRON 600R', '47'),
('DL2-13852.pdf', 'EXXONMOBIL_EHC_110', 'D', '22,23', 'EHC 110', '47'),
('DL2-13852.pdf', 'EXXONMOBIL_EHC_120', 'D', '22,23', 'EHC 120', '47'),
('DL2-13852.pdf', 'EXXONMOBIL_EHC_50', 'D', '17,18,22,23', 'EHC 50', '47'),
('DL2-13852.pdf', 'NESTE_NEXBASE_3043', 'D', '9,11,19,20,21,32,42,43', 'Nexbase 3043', '47'),
('DL2-13852.pdf', 'NESTE_NEXBASE_3050', 'D', '9,11,18,19,20,21,32,35,36,42,45', 'Nexbase 3050', '47'),
('DL2-13852.pdf', 'NESTE_NEXBASE_3060', 'D', '35', 'Nexbase 3060', '47'),
('DL2-13852.pdf', 'NESTE_NEXBASE_3080', 'D', '9,18,21,32,35', 'Nexbase 3080', '47'),
('DL2-13852.pdf', 'YUBASE_4', 'D', '17,19,20,21,30,35,44', 'Yubase 4', '47'),
('DL2-13852.pdf', 'YUBASE_6', 'D', '17,19,30,35', 'Yubase 6', '47'),
('DL2-15799.pdf', 'ADNOC_ADBASE_4CST', 'D', '17,20,23', 'ADbase 4', '36'),
('DL2-15799.pdf', 'ADNOC_ADBASE_6CST', 'D', '17,20,23', 'ADbase 6', '36'),
('DL2-15799.pdf', 'ARAMCO_LUBEREF_PRIMA_100', 'D', '17', 'aramcoPRIMA 100', '36'),
('DL2-15799.pdf', 'ARAMCO_LUBEREF_PRIMA_600', 'D', '17', 'aramcoPRIMA 600', '36'),
('DL2-15799.pdf', 'CHEVRON_GROUP_II_600R', 'D', '17,20', 'Chevron 600R', '36'),
('DL2-15799.pdf', 'EXXONMOBIL_EHC_120', 'D', '17', 'EHC 120', '36'),
('DL2-15799.pdf', 'EXXONMOBIL_EHC_45', 'D', '17', 'EHC 45', '36'),
('DL2-15799.pdf', 'GS_CALTEX_150N', 'D', '17', '150N', '36'),
('DL2-15799.pdf', 'YUBASE_4', 'D', '17,20,21', 'Yubase 4', '36'),
('DL2-15799.pdf', 'YUBASE_6', 'D', '17', 'Yubase 6', '36'),
('DL2-15564.pdf', 'ARAMCO_LUBEREF_PRIMA_150', 'D', '27', 'AramcoPRIMA150', '31'),
('DL2-15564.pdf', 'ARAMCO_LUBEREF_PRIMA_220', 'D', '29', 'AramcoPRIMA220', '31'),
('DL2-15564.pdf', 'ARAMCO_LUBEREF_PRIMA_500', 'D', '27', 'AramcoPRIMA500', '31'),
('DL2-15564.pdf', 'ARAMCO_LUBEREF_PRIMA_600', 'D', '29', 'AramcoPRIMA600', '31'),
('DL2-15564.pdf', 'EXXONMOBIL_EHC_110', 'D', '13', 'EHC 110', '31'),
('DL2-15564.pdf', 'EXXONMOBIL_EHC_50', 'D', '13', 'EHC 50', '31'),
('DL2-15564.pdf', 'EXXONMOBIL_EHC_65', 'D', '30', 'EHC 65', '31'),
('DL2-15564.pdf', 'GS_CALTEX_600N', 'D', '26', '600N', '31'),
('DL2-15564.pdf', 'NESTE_NEXBASE_3043', 'D', '14', 'Nexbase 3043', '31'),
('DL2-15564.pdf', 'YUBASE_4', 'D', '26', 'YUBASE 4', '31'),
('DL2-15332.pdf', 'ARAMCO_LUBEREF_PRIMA_150', 'D', '27', 'AramcoPRIMA150', '31'),
('DL2-15332.pdf', 'ARAMCO_LUBEREF_PRIMA_220', 'D', '29', 'AramcoPRIMA220', '31'),
('DL2-15332.pdf', 'ARAMCO_LUBEREF_PRIMA_500', 'D', '27', 'AramcoPRIMA500', '31'),
('DL2-15332.pdf', 'ARAMCO_LUBEREF_PRIMA_600', 'D', '29', 'AramcoPRIMA600', '31'),
('DL2-15332.pdf', 'EXXONMOBIL_EHC_110', 'D', '13', 'EHC 110', '31'),
('DL2-15332.pdf', 'EXXONMOBIL_EHC_50', 'D', '13', 'EHC 50', '31'),
('DL2-15332.pdf', 'EXXONMOBIL_EHC_65', 'D', '30', 'EHC 65', '31'),
('DL2-15332.pdf', 'GS_CALTEX_600N', 'D', '26', '600N', '31'),
('DL2-15332.pdf', 'NESTE_NEXBASE_3043', 'D', '14', 'Nexbase 3043', '31'),
('DL2-15332.pdf', 'YUBASE_4', 'D', '26', 'YUBASE 4', '31'),
]

b = Batch('non-duplicate review, batch 34: formulation decks (Infineum 2019 / D341X, Oronite OLOA 54xxx, Afton HiTEC 11455) (nineteenth pass)')
RECIPE = 'a recipe share (wt.% / %m) in finished-oil formulation tables; the KV, CCS, MRV, HTHS, Noack, VI and BN figures on those pages are properties of the blends'
KIXX = ("name-only partial match: the hit is '{0}' in a formulation table; the record names the product '{1}' from GS Caltex and does not mention Kixx Lubo, "
        "so the identity is NOT established from the document or the record; nothing from this page is used")

b.doc('DL2-12999.pdf', 'Infineum Additive Packages presentation: ATF, CVT, HD ATF, motorcycle, outboard and gas-engine example formulations', '01/01/2019 (page header)', FROZEN, RECIPE)
b.doc('DL2-13852.pdf', 'Chevron Oronite OLOA 54xxx finished oil formulations and claims deck (Client Confidential)', '© 2018 Chevron (no other date)', FROZEN, RECIPE)
for f in ('DL2-15564.pdf', 'DL2-15332.pdf'):
    other = 'DL2-15332.pdf' if f == 'DL2-15564.pdf' else 'DL2-15564.pdf'
    b.doc(f, f'Infineum D341X typical formulations presentation (the text of every name-hit page is identical to {other}, a different file)', '© Infineum International Limited 2023',
          FROZEN, RECIPE + "; each base stock row carries a 'Group II Basestock' / 'Group III Basestock' description written by Infineum (not a manufacturer statement)",
          ident={'GS_CALTEX_600N': KIXX.format('KIXX LUBO 600N, %m', '600N')})

# DL2-15799: Afton HiTEC 11455 support document; p.20 'Program Base Stock Characterization' (lot-numbered), pp.21 / 23 component 'Typical Density'
W = 'Afton HiTEC 11455 + HiTEC 7133 ILSAC GF-7 / API SQ support document (Level 1 support matrix p.17, base stock characterization p.20, final formulations pp.21-23)'
F15799 = 'DL2-15799.pdf'
cov = {
    'YUBASE_4': ("assessed by reading (2026-11-14, nineteenth pass) for the name-hit pages 17, 20 and 21 only: p.17 recipe share; p.20 'Program Base Stock Characterization' lot R20-12589 "
                 "(KV100 4.150 cSt D445, KV40 19.320 cSt D445, VI 122 D2270, saturates 98.3 wt% D2007, sulfur 0.0000 wt% D2622); p.21 component 'Typical Density' 0.834 "
                 "(no unit, no temperature) and the formulation's 'Base Oil Properties' (saturates 99.2 %m, sulfur 0.000 %m, KV100 4.225 cSt, VI 126). Record: KV100 4.23, KV40 19.57, VI 122 "
                 "(typicals, DL2-11304.pdf); density and saturates Missing -> two open-question rows (third-party evidence, not values)."),
    'ADNOC_ADBASE_4CST': ("assessed by reading (2026-11-14, nineteenth pass) for the name-hit pages 17, 20 and 23 only: p.17 recipe share; p.20 lot R20-7853 (KV100 4.322, KV40 19.71, VI 129, "
                          "saturates 96.8 wt% D2007, sulfur 0.0002 wt%); p.23 component 'Typical Density' 0.831 (no unit, no temperature). Record (DL2-12221.pdf, table headed 'PRODUCT SPECIFICATIONS'): KV100 4.35, KV40 20, VI 130, "
                          "density 0.832 g/ml, saturates 99.8 mass% -> one note (saturates; value classes differ)."),
    'ADNOC_ADBASE_6CST': ("assessed by reading (2026-11-14, nineteenth pass) for the name-hit pages 17, 20 and 23 only: p.17 recipe share; p.20 lot R19-5555 (KV100 6.008, KV40 31.72, VI 138, "
                          "saturates 95.5 wt% D2007, sulfur 0.0000 wt%); p.23 component 'Typical Density' 0.837 (no unit, no temperature). Record (DL2-12221.pdf, table headed 'PRODUCT SPECIFICATIONS'): KV100 6.18, KV40 34, VI 137, "
                          "density 0.844 g/ml, saturates 99.8 mass% -> one note (saturates; value classes differ)."),
    'CHEVRON_GROUP_II_600R': ("assessed by reading (2026-11-14, nineteenth pass) for the name-hit pages 17 and 20 only: p.17 recipe share; p.20 two lots RIC23-04540 / RIC24-08339 (KV100 12.010 / 12.030, "
                              "KV40 102.100 / 102.300, VI 108 / 108, saturates 97.6 / 97.2 wt% D2007, sulfur 0.0002 / 0.0002 wt% D2622); the lot KV100 values lie inside the record's 11.7-12.9, KV40 and VI meet "
                              "'100 (MIN)' and '95 (MIN)'; record saturates and sulfur Missing -> one open-question row. No density is printed for 600R on the pages read."),
}
b.doc(F15799, W, "'Last updated: June 9, 2025' (final formulation pages)", FROZEN,
      'a recipe share in the Level 1 support matrix (p.17), whose KV, CCS, HTHS, MRV and element data are properties of the blends', cov=cov,
      ident={'GS_CALTEX_150N': KIXX.format('Kixxlubo 150N', '150N'),
             'YUBASE_4': "printed 'Yubase 4' (p.20 inventory number R20-12589); 'Yubase 4 plus' lots on p.20 are a different product and were not used",
             'CHEVRON_GROUP_II_600R': "printed 'Chevron 600R' with inventory numbers RIC23-04540 and RIC24-08339, Group II",
             'ADNOC_ADBASE_4CST': "printed 'ADbase 4' (inventory number R20-7853, Group III)", 'ADNOC_ADBASE_6CST': "printed 'ADbase 6' (inventory number R19-5555, Group III)"})

OLD = {'YUBASE_4': 're-read manually: DL2-11304.pdf p.1 (only page) read in full (text layer) (' + T + ')',
       'ADNOC': 're-read manually: DL2-12221.pdf p.1 (only page) read in full (text layer) (' + T + ')',
       'CHEVRON_GROUP_II_600R': 're-read manually: DL2-10004.pdf p.1 (Group II/II+ specifications, 1/2018) read in full (text layer) (' + T + ')'}
b.row(p='YUBASE_4', tier=1, path='density', old="DL2-11304.pdf (NARMAK TRADE property sheet) prints 'Specific gravity at 15 °C | g/m3 | 0,8338 | ASTM D1298' and no density row; record density Missing (mandatory) with an open question on that unit.",
      new_f=F15799, new_p=21, new_text="'Final Formulations ... Components | Typical Density | % wt. | % vol.' row 'Yubase 4 | 0.834 | 87.15 | 88.26'", unit='not printed',
      form='component value used in a formulation calculation (third party)', cond='temperature not printed', method='not printed', outcome='additional', action='propose_open_question_update',
      reason=("A formulator's component density used to convert % wt. to % vol.; no unit, no temperature and no method are printed, and it is a third-party figure. A density without its reference "
              "temperature cannot fill the mandatory density; add it to the existing density / specific-gravity question as unverified evidence only. No value is derived or converted."),
      old_rev=OLD['YUBASE_4'], cmp_override='existing: density Missing')
b.row(p='YUBASE_4', tier=3, path='saturates', old="DL2-11304.pdf prints KV40 19,57 / KV100 4,23 mm2/s (ASTM D445), VI 122 (ASTM D2270), sulfur '< 10 ppm' (ASTM D2622) and no saturates row; record saturates Missing.",
      new_f=F15799, new_p=20, new_text="'Program Base Stock Characterization' row 'Yubase 4 | R20-12589 | III | 4.150 | 19.320 | 122 | 98.3 | 0.0000' (KV100 cSt D445, KV40 cSt D445, VI D2270, Saturates (wt%) D2007, Sulfur (wt%) D2622)",
      unit='wt%; cSt', form='batch measurement of the neat base oil by a third party (inventory number R20-12589)', method='ASTM D2007 (saturates), as printed per column', cond='neat base oil, one lot',
      basis='mass (printed wt%)', outcome='additional', action='propose_open_question_update',
      reason=("A single lot analysed by Afton, not a manufacturer typical or specification: it cannot fill saturates. Record it in an open question as batch evidence with the inventory number. "
              "The lot KV100 4.150 / KV40 19.320 / VI 122 are shown for context beside the typicals 4.23 / 19.57 / 122 and are not treated as a conflict (different value class). "
              "p.21 also prints the formulation's 'Base Oil Properties' (saturates 99.2 %m, KV100 4.225 cSt, VI 126; Yubase 4 is the only base oil in that formulation; no lot printed), kept as printed."),
      old_rev=OLD['YUBASE_4'], cmp_override='existing: saturates Missing')
for pid, lot, sat, s, kv, rec in (('ADNOC_ADBASE_4CST', 'R20-7853', '96.8', '0.0002', 'KV100 4.322 / KV40 19.71 / VI 129', 'KV100 4.35 / KV40 20 / VI 130'),
                                  ('ADNOC_ADBASE_6CST', 'R19-5555', '95.5', '0.0000', 'KV100 6.008 / KV40 31.72 / VI 138', 'KV100 6.18 / KV40 34 / VI 137')):
    g = pid[-4]
    b.row(p=pid, tier=3, path='saturates', old=f"DL2-12221.pdf prints 'Saturates | mass% | 99.8' for every ADbase grade in a table headed 'PRODUCT SPECIFICATIONS' with single values (no min / max, no method); {rec}. Record saturates 99.8 mass%.",
          new_f=F15799, new_p=20, new_text=f"'Program Base Stock Characterization' row 'ADbase {g} | {lot} | III | ...' saturates {sat} wt% (D2007), sulfur {s} wt% (D2622), {kv}",
          unit='wt%', form=f'batch measurement of the neat base oil by a third party (inventory number {lot})', method='ASTM D2007', cond='neat base oil, one lot', basis='mass (printed wt%)',
          outcome='not_comparable', action='propose_note',
          reason=(f"Comparability checked: same property and unit basis, but a different value class (one lot measured by Afton vs a manufacturer table value whose kind - limit or typical - is not stated) and the manufacturer's method is not printed; "
                  f"so {sat} vs 99.8 is NOT recorded as a conflict. Noted for the reviewer as batch evidence; no value changes. p.23 also prints a component 'Typical Density' "
                  f"{'0.831' if g == '4' else '0.837'} with no unit or temperature (record 0.832 / 0.844 g/ml), not compared."),
          old_rev=OLD['ADNOC'], cmp_override='existing: saturates 99.8 mass%')
b.row(p='CHEVRON_GROUP_II_600R', tier=3, path='saturates', old="DL2-10004.pdf (1/2018) prints for 600R: API category 'Group II+', KV40 '100 (MIN)', KV100 '11.7 – 12.9', VI '95 (MIN)', 'Sulpur, ppm ASTM D5453 Report', no saturates row. Record saturates and sulfur Missing.",
      new_f=F15799, new_p=20, new_text="'Chevron 600R | RIC23-04540 | II | 12.010 | 102.100 | 108 | 97.6 | 0.0002' and 'Chevron 600R | RIC24-08339 | II | 12.030 | 102.300 | 108 | 97.2 | 0.0002' (KV100, KV40, VI, Saturates wt% D2007, Sulfur wt% D2622)",
      unit='wt%; cSt', form='batch measurement of the neat base oil by a third party (inventory numbers RIC23-04540, RIC24-08339)', method='ASTM D2007 / D2622 as printed', cond='neat base oil, two lots',
      basis='mass (printed wt%)', outcome='additional', action='propose_open_question_update',
      reason=("Two lots analysed by Afton: they cannot fill saturates or sulfur (not manufacturer values). Record them in the open questions as batch evidence with the inventory numbers; "
              "the lot KV100 / KV40 / VI lie inside or meet the record's specification limits (observation only). Afton labels the lots 'II'; Chevron's sheet prints 'Group II+' (labels as printed, not compared)."),
      old_rev=OLD['CHEVRON_GROUP_II_600R'], cmp_override='existing: saturates, sulfur Missing')
b.write('zzzzzzzzzzzzzzzzzzz_b34_nondup_formulation_decks_1_nineteenth_pass.json')
