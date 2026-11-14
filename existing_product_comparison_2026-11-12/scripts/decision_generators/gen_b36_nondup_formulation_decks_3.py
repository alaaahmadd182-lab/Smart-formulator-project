"""Nineteenth pass, batch 36: open non-duplicate (category D) links of six additive-supplier documents (Lubrizol CV1100
MB 228.31 read-across matrix DL2-12610; Infineum T4294 ATF formulations DL2-13089; Afton HiTEC 3460 DCTF bulletin
DL2-13296; Oronite OLOA 55603 GF-7 / dexos1 Gen 3 deck (pptx); Afton HiTEC 12210M HDEO formulations DL2-12485 and
DL2-12486). Every name-hit page read in full on the text layer (the pptx text layer has no slide breaks and was read
whole); other pages not read. One open-question row: Afton's 'API Group III' label for Ultra-S 4 (API group Missing).
Writes decisions/zzzzzzzzzzzzzzzzzzz_b36_nondup_formulation_decks_3_nineteenth_pass.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nd_common import Batch, T, to_root
to_root()

PPTX = 'OLOA%2055603%20ILSAC%20GF-7%20and%20Gen%203%20MG%20Customer%20Deck%20-%20AMR%20APR%20EAME%20Jul26%20.pptx'
FROZEN = [
('DL2-12610.pdf', 'CHEVRON_GROUP_II_110RLV', 'D', '4', 'CHEVRON 110RLV', '5'),
('DL2-12610.pdf', 'CHEVRON_GROUP_II_220R', 'D', '4', 'CHEVRON 220R', '5'),
('DL2-12610.pdf', 'CHEVRON_GROUP_II_600R', 'D', '4', 'CHEVRON 600R', '5'),
('DL2-12610.pdf', 'EXXONMOBIL_EHC_110', 'D', '4', 'EHC 110', '5'),
('DL2-12610.pdf', 'EXXONMOBIL_EHC_45', 'D', '4', 'EHC 45', '5'),
('DL2-12610.pdf', 'EXXONMOBIL_EHC_50', 'D', '4', 'EHC 50', '5'),
('DL2-12610.pdf', 'EXXONMOBIL_EHC_65', 'D', '4', 'EHC 65', '5'),
('DL2-12610.pdf', 'NESTE_NEXBASE_3060', 'D', '4', 'NEXBASE 3060', '5'),
('DL2-13089.pdf', 'NESTE_NEXBASE_3030', 'D', '8', 'Nexbase 3030', '13'),
('DL2-13089.pdf', 'NESTE_NEXBASE_3043', 'D', '8', 'Nexbase 3043', '13'),
('DL2-13089.pdf', 'NESTE_NEXBASE_3080', 'D', '8', 'Nexbase 3080', '13'),
('DL2-13089.pdf', 'S_OIL_ULTRA_S_3', 'D', '9', 'Ultra S3', '13'),
('DL2-13089.pdf', 'S_OIL_ULTRA_S_4', 'D', '9', 'Ultra S4', '13'),
('DL2-13089.pdf', 'S_OIL_ULTRA_S_8', 'D', '9', 'Ultra S8', '13'),
('DL2-13089.pdf', 'YUBASE_3', 'D', '7', 'Yubase 3', '13'),
('DL2-13089.pdf', 'YUBASE_6', 'D', '7', 'Yubase 6', '13'),
('DL2-13296.pdf', 'NESTE_NEXBASE_3030', 'D', '6', 'Nexbase 3030', '24'),
('DL2-13296.pdf', 'NESTE_NEXBASE_3060', 'D', '6', 'Nexbase 3060', '24'),
('DL2-13296.pdf', 'NESTE_NEXBASE_3080', 'D', '6', 'Nexbase 3080', '24'),
('DL2-13296.pdf', 'S_OIL_ULTRA_S_3', 'D', '6', 'Ultra S 3', '24'),
('DL2-13296.pdf', 'S_OIL_ULTRA_S_6', 'D', '6', 'Ultra S 6', '24'),
('DL2-13296.pdf', 'S_OIL_ULTRA_S_8', 'D', '6', 'Ultra S 8', '24'),
('DL2-13296.pdf', 'YUBASE_3', 'D', '6', 'Yubase 3', '24'),
('DL2-13296.pdf', 'YUBASE_6', 'D', '6', 'Yubase 6', '24'),
(PPTX, 'BAPCO_BAPBASE_4', 'D', '1', 'BAPBase 4', '8'),
(PPTX, 'BAPCO_BAPBASE_8', 'D', '1', 'BAPBase 8', '8'),
(PPTX, 'CHEVRON_GROUP_II_100R', 'D', '1', 'Chevron 100R', '8'),
(PPTX, 'CHEVRON_GROUP_II_220R', 'D', '1', 'Chevron 220R', '8'),
(PPTX, 'NESTE_NEXBASE_3080', 'D', '1', 'NEXBASE 3080', '8'),
(PPTX, 'PETRO_CANADA_PURITY_VHVI_4', 'D', '1', 'Purity VHVI-4', '8'),
(PPTX, 'PETRO_CANADA_PURITY_VHVI_8', 'D', '1', 'Purity VHVI-8', '8'),
('DL2-12485.pdf', 'CHEVRON_GROUP_II_110RLV', 'D', '5,6', 'Chevron 110RLV', '32'),
('DL2-12485.pdf', 'CHEVRON_GROUP_II_220R', 'D', '5,6,7', 'Chevron 220R', '32'),
('DL2-12485.pdf', 'EXXONMOBIL_EHC_45', 'D', '9,10,11', 'EHC 45', '32'),
('DL2-12485.pdf', 'EXXONMOBIL_EHC_65', 'D', '9,10,11', 'EHC 65', '32'),
('DL2-12485.pdf', 'S_OIL_ULTRA_S_4', 'D', '12,13,15,16,17,24,25,26', 'Ultra-S 4', '32'),
('DL2-12485.pdf', 'YUBASE_4', 'D', '8', 'Yubase 4', '32'),
('DL2-12485.pdf', 'YUBASE_6', 'D', '21,22,23,30,31,32', 'Yubase 6', '32'),
('DL2-12486.pdf', 'CHEVRON_GROUP_II_110RLV', 'D', '5,6', 'Chevron 110RLV', '32'),
('DL2-12486.pdf', 'CHEVRON_GROUP_II_220R', 'D', '5,6,7', 'Chevron 220R', '32'),
('DL2-12486.pdf', 'EXXONMOBIL_EHC_45', 'D', '9,10,11', 'EHC 45', '32'),
('DL2-12486.pdf', 'EXXONMOBIL_EHC_65', 'D', '9,10,11', 'EHC 65', '32'),
('DL2-12486.pdf', 'S_OIL_ULTRA_S_4', 'D', '12,13,15,16,17,24,25,26', 'Ultra-S 4', '32'),
('DL2-12486.pdf', 'YUBASE_4', 'D', '8', 'Yubase 4', '32'),
('DL2-12486.pdf', 'YUBASE_6', 'D', '21,22,23,30,31,32', 'Yubase 6', '32'),
]

b = Batch('non-duplicate review, batch 36: Lubrizol CV1100 matrix, Infineum T4294, Afton HiTEC 3460 / 12210M, Oronite OLOA 55603 deck (nineteenth pass)')
RECIPE = 'a recipe share (wt.% / m%) in finished-oil formulation tables; the KV, KRL, Brookfield, CCS, MRV, HTHS, Noack, TBN and ash figures are properties of the blends'
LABEL = "; Afton prints an 'API Group II' / 'API Group III' label beside each base oil (third-party label, not a manufacturer classification)"
b.doc('DL2-12610.pdf', 'Lubrizol CV1100 MB 228.31 read-across matrix (basic candidate formulations, oil codes OS...)', "'1/1/2020' (page footer)", FROZEN, RECIPE)
b.doc('DL2-13089.pdf', 'Infineum T4294 multi-vehicle ATF formulations with Yubase, Nexbase and S-Oil Ultra base stocks', '© 2019 Infineum International Limited', FROZEN, RECIPE,
      ident={p: f"printed '{n}' under 'Formulations with S-Oil Ultra® Base Stocks'" for p, n in (('S_OIL_ULTRA_S_3', 'Ultra S3'), ('S_OIL_ULTRA_S_4', 'Ultra S4'), ('S_OIL_ULTRA_S_8', 'Ultra S8'))})
b.doc('DL2-13296.pdf', "Afton HiTEC 3460 DCTF bulletin, 'HiTEC® 3460 Typical Formulations' page", '2018 © Afton Chemical Corporation', FROZEN,
      RECIPE + "; the page says only '12.8% weight HiTEC® 3460 in Group III base stock' for the ATF-499-RX-01 blend (no per-oil classification)")
b.doc(PPTX, 'Chevron Oronite OLOA 55603 dexos1 Gen 3 and ILSAC GF-7 customer deck (AMR / APR / EAME)', "'July 2026' (title slide)", FROZEN,
      "a recipe share in the 'Base oil Coverage' formulation tables (Purity VHVI-4 / VHVI-8 carry Oronite's '(Gp3)' label); the deck's 'Base oil properties' ranges (saturates 93 - 99 %, KV100 4.8 - 6.2, VI 109 - 140) are route requirements of OLOA 55603, not properties of a named base oil",
      scope='whole extracted text layer read in full (the pptx text has no slide breaks: one block of 7,184 characters covering the text of all 8 slides); slide images, charts and notes not viewed')
for f in ('DL2-12485.pdf', 'DL2-12486.pdf'):
    other = 'DL2-12486.pdf' if f == 'DL2-12485.pdf' else 'DL2-12485.pdf'
    cov = {}
    if f == 'DL2-12486.pdf':
        cov['S_OIL_ULTRA_S_4'] = ("not applicable for property values: another product's document (Afton HiTEC 12210M HDEO formulations); on the name-hit pages read Ultra-S 4 appears only as a recipe share "
                                  "with Afton's label 'API Group III'; the same text is in DL2-12485.pdf, whose p.12 is cited in the single API-group open-question row of this batch (not proposed twice). "
                                  "No property of the neat base oil is printed on those pages (pages without the name not read)")
    else:
        cov['S_OIL_ULTRA_S_4'] = ("not applicable for property values: another product's document (Afton HiTEC 12210M HDEO formulations); on the name-hit pages read Ultra-S 4 appears only as a recipe share "
                                  "with Afton's label 'API Group III'; the record's API group is Missing -> one open-question row (third-party label). No property of the neat base oil is printed on those pages "
                                  "(pages without the name not read)")
    b.doc(f, f'Afton HiTEC 12210M HDEO formulation sheets (API CK-4 / FA-4) by base-oil slate (the text of every name-hit page is identical to {other}, a different file)',
          '2019 © Afton Chemical Corporation', FROZEN, RECIPE + LABEL, cov=cov)

b.row(p='S_OIL_ULTRA_S_4', tier=1, path='api_group_chemistry.api_group',
      old="DL2-11177.pdf (Ultra-S series sheet) prints no API group (only use 'in combination with conventional Group I or Group II base oils'); record API group Missing since the 2026-10 audit, with an open question listing indirect evidence only.",
      new_f='DL2-12485.pdf', new_p=12, new_text="'Formulation (%) wt | HiTEC® 12210M | DI | 18.0 | HiTEC® 5748A | ND-OCP | 1.0 | Ergon P 100N | API Group II | 35.0 | Ergon P 300N | API Group II | 36.0 | Ultra-S 4 | API Group III | 10.0' (same label on pp.13, 15-17, 24-26 and in DL2-12486.pdf)",
      unit='(classification label)', form='third-party classification label (additive supplier formulation table)', outcome='additional', action='propose_open_question_update',
      reason=("An additive supplier's label beside the base oil in its own formulation tables: not a manufacturer classification, so it cannot fill the mandatory API group. Record it in the existing API-group "
              "open question as third-party evidence only (document, page, printed text). It does not change the audit conclusion that no S-OIL document classifies Ultra-S 4 directly, and it does not bear on "
              "ID-01 (aramcoULTRA 8 vs Ultra-S 8), which stays open."),
      old_rev=f're-read manually: DL2-11177.pdf p.1 (only page) read in full (text layer) ({T})', cmp_override='existing: API group Missing')
b.write('zzzzzzzzzzzzzzzzzzz_b36_nondup_formulation_decks_3_nineteenth_pass.json')
