"""Nineteenth pass, batch 38: open non-duplicate (category D) links of three Afton API programme books (CDPs) that carry
lot-numbered 'Program Base Stock Characterization' tables and formulation component densities: HiTEC 22300 (API SL, Aramco
Prima), HiTEC 11356 (API SQ, 'Version 1_20260525_updated') and HiTEC 11500 (DL2-15777, API SQ). Chosen first because the
records lack mandatory KV40 / density (EHC series), density (YUBASE 4 / 6) or API group (Purity 1003 / 2204).
Every name-hit page read in full on the text layer; the table pages behind the rows also viewed as page images (watermark
noted where it covers digits). Third-party lot and component values are batch / formulation evidence: open questions or
notes only, never values. Writes decisions/zzzzzzzzzzzzzzzzzzz_b38_nondup_afton_cdp_characterisations_nineteenth_pass.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nd_common import Batch, T, to_root
to_root()

F22 = 'HiTEC%2022300%20CDP_API%20SL%20AramcoPrima.pdf'
F13 = 'HiTEC%2011356_API%20SQ%20CDP%20-%20Version%201_20260525_updated.pdf'
F15 = 'DL2-15777.pdf'
FROZEN = [
(F22, 'EXXONMOBIL_EHC_110', 'D', '12,14,16,17', 'EHC 110', '40'),
(F22, 'EXXONMOBIL_EHC_45', 'D', '12,14', 'EHC 45', '40'),
(F22, 'EXXONMOBIL_EHC_50', 'D', '12,14,16,17', 'EHC 50', '40'),
(F22, 'EXXONMOBIL_EHC_65', 'D', '12,14', 'EHC 65', '40'),
(F22, 'YUBASE_4', 'D', '12,14,15,16,17', 'Yubase 4', '40'),
(F22, 'YUBASE_6', 'D', '12,14,15', 'Yubase 6', '40'),
(F13, 'CHEVRON_GROUP_II_600R', 'D', '14,16', 'Chevron 600R', '35'),
(F13, 'PETRO_CANADA_PURITY_1003', 'D', '14,16,17,18', 'PURITY 1003', '35'),
(F13, 'PETRO_CANADA_PURITY_2204', 'D', '14,16,17,18', 'PURITY 2204', '35'),
(F13, 'YUBASE_4', 'D', '14,16,23,24', 'Yubase 4', '35'),
(F13, 'YUBASE_6', 'D', '14,16,23,24', 'Yubase 6', '35'),
(F15, 'NESTE_NEXBASE_3043', 'D', '10,12', 'NEXBASE 3043', '18'),
(F15, 'NESTE_NEXBASE_3050', 'D', '10,12', 'NEXBASE 3050', '18'),
(F15, 'YUBASE_4', 'D', '10,12,13,14', 'YUBASE 4', '18'),
(F15, 'YUBASE_6', 'D', '10,12,13,14', 'YUBASE 6', '18'),
]

b = Batch('non-duplicate review, batch 38: Afton CDP base-stock characterisations (HiTEC 22300, 11356, 11500) (nineteenth pass)')
LOT = 'batch measurement of the neat base oil by a third party (inventory number{})'
CD = 'component value used in a formulation calculation (third party)'
A = lambda pages: f'assessed by reading (2026-11-14, nineteenth pass) for the name-hit pages {pages} only: '

cov22 = {
    'EXXONMOBIL_EHC_45': A('12 and 14') + "p.12 recipe shares (Level 1 support matrix); p.14 lot RIC22-08507: KV100 4.663, KV40 23.8, VI 113, saturates 97.8 %, sulfur <0.0002 % (Afton label II). Record: KV100 4.4-4.7, VI 113-119 (specification, DL2-11785.pdf), KV40 Missing -> open-question row (lot evidence).",
    'EXXONMOBIL_EHC_50': A('12, 14, 16 and 17') + "p.14 lots TSU23-00050 (5.478 / 30.75 / 115 / 98.5) and RIC22-13237 (5.375 / 29.77 / 115 / 98.2); pp.16-17 component 'Density @ 15.6ºC' 0.8513 (no unit). Record: KV100 5.2-5.6, VI 110-119 (specification), KV40 and density Missing -> two open-question rows.",
    'EXXONMOBIL_EHC_65': A('12 and 14') + "p.14 lots TSU21-00145 (6.490 / 41.65 / 106 / 96.1) and RIC23-10730 (6.486 / 41.85 / 105 / 98.3). Record: KV100 6.3-6.6, VI 103-109 (specification), KV40 Missing -> open-question row.",
    'EXXONMOBIL_EHC_110': A('12, 14, 16 and 17') + "p.14 lots RIC23-02722 (10.58 / 93.41 / 95 / 98.5) and TSU23-00051 (10.64 / 92.76 / 97 / 97.1); pp.16-17 component density 0.8762 at 15.6 ºC (no unit). Record: KV100 10.0-12.0, VI 95-119 (specification), KV40 and density Missing -> two open-question rows.",
    'YUBASE_4': A('12 and 14-17') + "p.14 lots RIC22-02745 (4.189 / 19.22 / 123 / saturates 96.5) and RIC23-08617 (4.145 / 18.77 / 125 / 98.6); pp.15-16 component density 0.8322 at 15.6 ºC (no unit). Density -> one open-question row for the three component densities seen in this batch; the lot saturates are of the same kind as the batch 34 saturates row and are not proposed again.",
    'YUBASE_6': A('12, 14 and 15') + "p.14 lots TSU22-00437 (6.411 / 35.83 / 132 / 97.9) and RIC23-08382 (6.374 / 35.23 / 133 / 98.6); p.15 component density 0.8407 at 15.6 ºC (no unit) and the 'Base Oil Properties' of LBT-029748-A / -029749-A, whose only base oil is Yubase 6 (saturates 97.9 mass %, KV100 6.410, VI 132). Density and saturates Missing -> two open-question rows.",
}
cov13 = {
    'CHEVRON_GROUP_II_600R': A('14 and 16') + "p.14 recipe shares; p.16 the same lots RIC23-04540 / RIC24-08339 as DL2-15799.pdf p.20 (already in the batch 34 open-question row); no new row.",
    'PETRO_CANADA_PURITY_1003': A('14, 16, 17 and 18') + "p.16 lot R16-13774 (4.448 / 21.530 / 119 / saturates 99.1 / sulfur 0.0002) labelled 'II' by Afton; pp.17-18 component density 0.836 at 15.6 ºC (no unit; record density 0.84 kg/L at 15 °C, not compared). Record API group Missing -> one open-question row (third-party label).",
    'PETRO_CANADA_PURITY_2204': A('14, 16, 17 and 18') + "p.16 lot R19-15467 (6.334 / 39.620 / 108 / saturates 94.3 / sulfur 0.0002) labelled 'II' by Afton; pp.17-18 component density 0.856 at 15.6 ºC (no unit; record 0.87 kg/L at 15 °C, not compared). Record API group Missing -> one open-question row; lot saturates vs record typical -> one note.",
    'YUBASE_4': A('14, 16, 23 and 24') + "p.16 the same lot R20-12589 as DL2-15799.pdf p.20 (batch 34 saturates row); pp.23-24 component density 0.8334 at 15.6 ºC (no unit; 'Apr 2, 2024'), listed in this batch's density row.",
    'YUBASE_6': A('14, 16, 23 and 24') + "p.16 lot RIC25-02290 (6.524 / 36.42 / 134 / saturates 95.8 / 0.0002); pp.23-24 component density 0.8417 at 15.6 ºC (no unit), both listed in this batch's Yubase 6 rows.",
}
cov15 = {
    'NESTE_NEXBASE_3043': A('10 and 12') + "p.10 recipe share; p.12 lot B17-19563 (4.294 / 19.89 / 125 / saturates 94.5 / sulfur 0.000). Record saturates Missing -> open-question row.",
    'NESTE_NEXBASE_3050': A('10 and 12') + "p.10 recipe share; p.12 lot B17-2777 (5.105 / 26.32 / 125 / saturates 98.9 / sulfur 0.000). Record saturates Missing -> open-question row.",
    'YUBASE_4': A('10, 12, 13 and 14') + "p.12 lot B18-138 (4.230 / 19.33 / 125 / saturates 96.3); pp.13-14 'Typical Density' 0.834 (no unit, no temperature; 'Sep, 2025'), listed in this batch's density row; lot saturates not proposed again.",
    'YUBASE_6': A('10, 12, 13 and 14') + "p.12 lot B17-15748 (6.360 / 34.62 / 137 / saturates 95.8); pp.13-14 'Typical Density' 0.842 (no unit, no temperature), both listed in this batch's Yubase 6 rows.",
}
b.doc(F22, 'Afton HiTEC 22300 API SL programme book in Aramco Prima (Level 1 support matrix p.12, Program Base Stock Characterization p.14, final formulations pp.15-17)', 'not printed on the pages read', FROZEN,
      'a recipe share', cov=cov22, viewed='pp.14, 15 and 16 also viewed as page images (some p.14 cells partly covered by the CONFIDENTIAL watermark; the text-layer values agree with the visible digits)',
      route='Afton HiTEC 22300 (no package record; already in the candidate queue) with HiTEC 672 and HiTEC 5748 (record exists; not assessed by these links)')
b.doc(F13, "Afton HiTEC 11356 API SQ programme book ('Version 1_20260525_updated'; support matrix p.14, characterization p.16, final formulations pp.17-18 'Apr, 2025' and pp.23-24 'Apr 2, 2024')", 'file name 20260525; pages Apr 2025 / Apr 2, 2024', FROZEN,
      'a recipe share', cov=cov13, viewed='pp.16 and 23 also viewed as page images',
      route='Afton HiTEC 11356 (no package record; already in the candidate queue) with HiTEC 672 and HiTEC 5748 (record exists; not assessed by these links)')
b.doc(F15, "Afton HiTEC 11500 API SQ programme book (support matrix p.10, characterization p.12, final formulations pp.13-14 'Sep, 2025')", "'Sep, 2025' (final formulations)", FROZEN,
      'a recipe share', cov=cov15, viewed='pp.12 and 13 also viewed as page images',
      route='Afton HiTEC 11500 (no package record; already in the candidate queue) with HiTEC 672 and HiTEC 5748 (record exists; not assessed by these links)')

OLD_EHC = 're-read manually: DL2-11785.pdf pp.1-3 (EHC Series specifications, 4/29/2019) read in full (old archive text layer) (' + T + ')'
EHC_OLD = "DL2-11785.pdf (EHC Series, 4/29/2019) prints only specification limits: KV100 '{kv}', VI '{vi}', flash, pour, Noack, colour{ccs}; no KV40 and no density row. Record KV40 and density Missing (mandatory)."
for pid, g, kv, vi, ccs, lots, txt in (
        ('EXXONMOBIL_EHC_45', '45', '4.4- 4.7', '113- 119', ', CCS -25 °C max 1,550', 'RIC22-08507', "'EHC45 | RIC22-08507 | 4.663 | 23.8 | 113 | 97.8 | <0.0002 | II'"),
        ('EXXONMOBIL_EHC_50', '50', '5.2- 5.6', '110- 119', ', CCS -20 °C max 1,700', 'TSU23-00050, RIC22-13237', "'EHC 50 | TSU23-00050 | 5.478 | 30.75 | 115 | 98.5 | <0.0002 | II' and 'EHC 50 | RIC22-13237 | 5.375 | 29.77 | 115 | 98.2 | <0.0002 | II'"),
        ('EXXONMOBIL_EHC_65', '65', '6.3- 6.6', '103- 109', ', CCS -20 °C max 3,100', 'TSU21-00145, RIC23-10730', "'EHC65 | TSU21-00145 | 6.490 | 41.65 | 106 | 96.1 | <0.0002 | II' and 'EHC65 | RIC23-10730 | 6.486 | 41.85 | 105 | 98.3 | <0.0002 | II'"),
        ('EXXONMOBIL_EHC_110', '110', '10.0- 12.0', '95- 119', '', 'RIC23-02722, TSU23-00051', "'EHC 110 | RIC23-02722 | 10.58 | 93.41 | 95 | 98.5 | <0.0002 | II' and 'EHC 110 | TSU23-00051 | 10.64 | 92.76 | 97 | 97.1 | <0.0002 | II'")):
    b.row(p=pid, tier=1, path='kv40', old=EHC_OLD.format(kv=kv, vi=vi, ccs=ccs), new_f=F22, new_p=14,
          new_text=f"'Program Base Stock Characterization / Matrix Core Engine Tested Base Stocks' (columns KV100 cSt D445, KV40 cSt D445, VI D2270, Saturates % D2007, Sulfur % D2622, API 1509 group): {txt}",
          unit='cSt', form=LOT.format(f's {lots}' if ',' in lots else f' {lots}'), method='ASTM D445 (as printed)', cond='40 °C; neat base oil, single lot(s)', outcome='additional', action='propose_open_question_update',
          reason=("Afton's measured properties of the lot(s) used in its matrix core engine tests ('reported in accordance with ACC CoP, Appendix E, Guideline 2.c)'). A lot result is not a manufacturer typical or "
                  "specification and cannot fill the mandatory KV40; record it in an open question as batch evidence with the inventory number(s). The lot KV100 and VI lie inside the record's specification "
                  "ranges (observation only). Some p.14 cells are partly covered by the watermark on the page image; the text-layer values agree with the visible digits."),
          old_rev=OLD_EHC, cmp_override='existing: KV40 Missing')
for pid, d, pages in (('EXXONMOBIL_EHC_50', '0.8513', '16-17'), ('EXXONMOBIL_EHC_110', '0.8762', '16-17')):
    b.row(p=pid, tier=1, path='density',
          old=("DL2-11785.pdf (EHC Series, 4/29/2019) prints specification limits only (KV100, VI, flash, pour, Noack, colour and, for some grades, CCS maxima); it has no density row. "
               "Record density Missing (mandatory)."),
          new_f=F22, new_p=16, new_text=f"'Formulation Composition | Type | Density @ 15.6ºC' row '{'EHC 50' if d == '0.8513' else 'EHC 110'} | Group II | {d}' (pp.{pages}; the column prints no unit)",
          unit='not printed', form=CD, method='not printed', cond='15.6 °C', outcome='additional', action='propose_open_question_update',
          reason=("A formulator's component density used to convert weight % to volume %; the temperature is printed (15.6 ºC) but no unit and no method, and it is a third-party figure without a lot. "
                  "It cannot fill the mandatory density (unit not printed; not a manufacturer value); add it to an open question as unverified evidence. No unit is assumed and no value is converted to 15 °C."),
          old_rev=OLD_EHC, cmp_override='existing: density Missing')

b.row(p='YUBASE_4', tier=1, path='density', old="DL2-11304.pdf (NARMAK TRADE sheet) prints 'Specific gravity at 15 °C | g/m3 | 0,8338 | ASTM D1298' and no density row; record density Missing (mandatory). Batch 34 already proposes the DL2-15799.pdf 'Typical Density' 0.834 (no unit, no temperature).",
      new_f=F22, new_p=15, new_text="'Density @ 15.6ºC' row 'Yubase 4 | Group III | 0.8322' (HiTEC 22300 book pp.15-16); also HiTEC 11356 book pp.23-24 'Yubase 4 | 0.8334' (Density @ 15.6ºC, 'Apr 2, 2024') and DL2-15777.pdf pp.13-14 'Yubase 4 | 0.834' ('Typical Density', 'Sep, 2025'); no unit in any of them",
      unit='not printed', form=CD, method='not printed', cond='15.6 °C (DL2-15777.pdf: no temperature)', outcome='additional', action='propose_open_question_update',
      reason=("Three more third-party component densities (0.8322, 0.8334 at 15.6 ºC; 0.834 without temperature), none with a unit, method or lot. They cannot fill the mandatory density; add them to the "
              "existing density question beside the batch 34 entry. They are not averaged, rounded or converted to 15 °C."),
      old_rev='re-read manually: DL2-11304.pdf p.1 (only page) read in full (text layer) (' + T + ')', cmp_override='existing: density Missing')
OLD_Y6 = 're-read manually: DL2-11306.pdf p.1 (only page) read in full (text layer) (' + T + ')'
Y6_OLD = "DL2-11306.pdf (NARMAK TRADE sheet) prints 'Specific gravity at 15 °C | g/m3 | 0,8423 | ASTM D1298', KV40 36,82, KV100 6,52, VI 131, sulfur '< 10 ppm' and no density or saturates row; record density (mandatory) and saturates Missing."
b.row(p='YUBASE_6', tier=1, path='density', old=Y6_OLD, new_f=F22, new_p=15,
      new_text="'Density @ 15.6ºC' row 'Yubase 6 | Group III | 0.8407' (HiTEC 22300 book p.15); also HiTEC 11356 book pp.23-24 'Yubase 6 | 0.8417' (Density @ 15.6ºC) and DL2-15777.pdf pp.13-14 'Yubase 6 | 0.842' ('Typical Density'); no unit in any of them",
      unit='not printed', form=CD, method='not printed', cond='15.6 °C (DL2-15777.pdf: no temperature)', outcome='additional', action='propose_open_question_update',
      reason=("Third-party component densities without unit, method or lot; they cannot fill the mandatory density. Record them in an open question as unverified evidence; no unit is assumed, "
              "nothing is averaged or converted, and the NARMAK 'g/m3' specific gravity question stays as it is."),
      old_rev=OLD_Y6, cmp_override='existing: density Missing')
b.row(p='YUBASE_6', tier=3, path='saturates', old=Y6_OLD, new_f=F22, new_p=14,
      new_text="'Yubase 6 | TSU22-00437 | 6.411 | 35.83 | 132 | 97.9 | <0.0002 | III' and 'Yubase 6 | RIC23-08382 | 6.374 | 35.23 | 133 | 98.6 | <0.0002 | III' (HiTEC 22300 p.14); 'Yubase 6 | RIC25-02290 | III | 6.524 | 36.42 | 134 | 95.8 | 0.0002' (HiTEC 11356 p.16); 'YUBASE 6 | B17-15748 | III | 6.360 | 34.62 | 137 | 95.8 | 0.001' (DL2-15777.pdf p.12)",
      unit='% / wt%', form=LOT.format('s TSU22-00437, RIC23-08382, RIC25-02290, B17-15748'), method='ASTM D2007', cond='neat base oil, four lots', basis='mass (printed % / wt%)',
      outcome='additional', action='propose_open_question_update',
      reason=("Four lots analysed by Afton (saturates 97.9, 98.6, 95.8, 95.8): lot results cannot fill saturates; record them in an open question as batch evidence with the inventory numbers. "
              "The HiTEC 22300 p.15 'Base Oil Properties' (saturates 97.9 mass %, KV100 6.410, VI 132) of formulations whose only base oil is Yubase 6 are kept as printed, with no lot. Lot KV / VI values "
              "are shown beside the NARMAK typicals for context, not as conflicts (different value class)."),
      old_rev=OLD_Y6, cmp_override='existing: saturates Missing')

OLD_PC = 're-read manually: DL2-10020.pdf pp.1-2 (PURITY base oils brochure LUB3213E (2015.07)) read in full (old archive text layer) (' + T + ')'
for pid, g, lot, row in (('PETRO_CANADA_PURITY_1003', '1003', 'R16-13774', "'PURITY1003 | R16-13774 | II | 4.448 | 21.530 | 119 | 99.1 | 0.0002'"),
                         ('PETRO_CANADA_PURITY_2204', '2204', 'R19-15467', "'PURITY2204 | R19-15467 | II | 6.334 | 39.620 | 108 | 94.3 | 0.0002'")):
    b.row(p=pid, tier=1, path='api_group_chemistry.api_group',
          old=f"DL2-10020.pdf prints a typical-properties table for PURITY {g} without a per-grade API group; p.1 text speaks of 'Group II and Group II+ base oils' and a benchmarking chart whose labels the record treats as ambiguous. Record API group Missing.",
          new_f=F13, new_p=16, new_text=f"'Program Base Stock Characterization HiTEC® 11356' row {row} (column 'Base Stock Group')", unit='(classification label)',
          form='third-party classification label (additive supplier characterization table)', outcome='additional', action='propose_open_question_update',
          reason=("Afton's group label beside its own lot analysis: not a manufacturer classification, so it cannot fill the mandatory API group. Record it in an open question as third-party evidence "
                  "(document, page, printed text, lot). It does not resolve the reading of Petro-Canada's own brochure."),
          old_rev=OLD_PC, cmp_override='existing: API group Missing')
b.row(p='PETRO_CANADA_PURITY_2204', tier=3, path='saturates', old="DL2-10020.pdf typical table: '% Saturates | PCM435 | ... 2204 ... 99.9' (Petro-Canada method PCM435). Record saturates 99.9 %.",
      new_f=F13, new_p=16, new_text="'PURITY2204 | R19-15467 | II | 6.334 | 39.620 | 108 | 94.3 | 0.0002' (Saturates (wt%) D2007)", unit='wt%',
      form=LOT.format(' R19-15467'), method='ASTM D2007', cond='neat base oil, one lot', basis='mass (printed wt%)', outcome='not_comparable', action='propose_note',
      reason=("Comparability checked: same property, but a different method (ASTM D2007 vs Petro-Canada PCM435) and value class (one third-party lot vs a manufacturer typical); 94.3 vs 99.9 is therefore "
              "NOT recorded as a conflict. Noted for the reviewer as batch evidence; no value changes. (PURITY 1003's lot gives 99.1 vs the typical 99.9; not noted separately.)"),
      old_rev=OLD_PC, cmp_override='existing: saturates 99.9 % (typical, PCM435)')
for pid, g, ed, lot, row in (('NESTE_NEXBASE_3043', '3043', 'Edition 5.2', 'B17-19563', "'NEXBASE 3043 | B17-19563 | III | 4.294 | 19.89 | 125 | 94.5 | 0.000'"),
                             ('NESTE_NEXBASE_3050', '3050', 'Edition 4.2', 'B17-2777', "'NEXBASE 3050 | B17-2777 | III | 5.105 | 26.32 | 125 | 98.9 | 0.000'")):
    f = 'DL2-10037.pdf' if g == '3043' else 'DL2-10038.pdf'
    b.row(p=pid, tier=3, path='saturates', old=f"{f} (NEXBASE {g} TDS, {ed}) prints viscosity, VI, pour, flash, colour, Noack and density and no saturates row; record saturates Missing.",
          new_f=F15, new_p=12, new_text=f"'Program Base Stock Characterization HiTEC® 11500' row {row} (Saturates (wt%) D2007)", unit='wt%',
          form=LOT.format(f' {lot}'), method='ASTM D2007', cond='neat base oil, one lot', basis='mass (printed wt%)', outcome='additional', action='propose_open_question_update',
          reason="A single lot analysed by Afton: it cannot fill saturates. Record it in an open question as batch evidence with the inventory number; the lot KV / VI are context only.",
          old_rev=f're-read manually: {f} pp.1-2 read in full (old archive text layer) ({T})', cmp_override='existing: saturates Missing')

b.visual += [
    dict(f=F22, page=14, checked="'Program Base Stock Characterization' table", result='confirmed',
         detail="EHC 45 / 50 / 65 / 110 and Yubase 4 / 6 lot rows as cited; some cells (EHC 50 KV40, EHC 65 KV100 / KV40, AP/E Core VI and saturates) partly covered by the CONFIDENTIAL watermark, the text-layer values agree with the visible digits."),
    dict(f=F22, page='15, 16', checked="'Engine Oil Final Formulation' component tables", result='confirmed',
         detail="Column 'Density @ 15.6ºC' (no unit): Yubase 4 0.8322, Yubase 6 0.8407 (p.15), EHC 50 0.8513, EHC 110 0.8762, Yubase 4 0.8322 (p.16). p.15 LBT-029748-A / -029749-A: Yubase 6 is the only base oil; Base Oil Properties 97.9 / 0.000 / 6.410 / 132."),
    dict(f=F13, page=16, checked="'Program Base Stock Characterization HiTEC® 11356' table", result='confirmed', detail='Rows for Yubase 4 / 6, Chevron 600R, PURITY1003 / 2204 as cited (group column II for the PURITY rows).'),
    dict(f=F13, page=23, checked="'Final Formulations' component table (Apr 2, 2024)", result='confirmed', detail="'Density @ 15.6ºC' column (no unit): Yubase 4 0.8334, Yubase 6 0.8417."),
    dict(f=F15, page=12, checked="'Program Base Stock Characterization HiTEC® 11500' table", result='confirmed', detail='NEXBASE 3043 B17-19563, NEXBASE 3050 B17-2777, YUBASE 4 B18-138, YUBASE 6 B17-15748 rows as cited.'),
    dict(f=F15, page=13, checked="'Final Formulations' component table (Sep, 2025)", result='confirmed', detail="'Typical Density' column (no unit, no temperature): Yubase 4 0.834, Yubase 6 0.842 (both listed without a share in the four formulations shown)."),
]
b.write('zzzzzzzzzzzzzzzzzzz_b38_nondup_afton_cdp_characterisations_nineteenth_pass.json')
