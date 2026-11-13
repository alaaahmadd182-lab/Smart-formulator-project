"""Nineteenth pass, batch 35: open non-duplicate (category D) links of four additive-supplier formulation documents
(Afton HiTEC 34006 CVT DL2-15608; Oronite OLOA 54000 / 54050 / 54013 deck DL2-12412; Oronite APAC product summary
DL2-12906; Afton HiTEC 9490 / 12200 / 8788B formulations DL2-13364). Every name-hit page read in full on the text layer;
other pages not read. Three open-question rows: Afton's 'API Group III' label for three records whose API group is
Missing (third-party label, not a classification). Writes decisions/zzzzzzzzzzzzzzzzzzz_b35_nondup_formulation_decks_2_nineteenth_pass.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nd_common import Batch, T, to_root
to_root()

FROZEN = [
('DL2-15608.pdf', 'NESTE_NEXBASE_3030', 'D', '9', 'Nexbase 3030', '10'),
('DL2-15608.pdf', 'NESTE_NEXBASE_3060', 'D', '9', 'Nexbase 3060', '10'),
('DL2-15608.pdf', 'PETRONAS_ETRO_3', 'D', '6', 'Etro 3', '10'),
('DL2-15608.pdf', 'PETRONAS_ETRO_4', 'D', '7', 'Etro 4', '10'),
('DL2-15608.pdf', 'PETRONAS_ETRO_6', 'D', '6', 'Etro 6', '10'),
('DL2-15608.pdf', 'S_OIL_ULTRA_S_3', 'D', '5', 'Ultra S3', '10'),
('DL2-15608.pdf', 'S_OIL_ULTRA_S_6', 'D', '5', 'Ultra S6', '10'),
('DL2-15608.pdf', 'YUBASE_3', 'D', '3', 'Yubase 3', '10'),
('DL2-15608.pdf', 'YUBASE_4', 'D', '4', 'Yubase 4', '10'),
('DL2-15608.pdf', 'YUBASE_6', 'D', '3', 'Yubase 6', '10'),
('DL2-12412.pdf', 'CHEVRON_GROUP_II_100R', 'D', '35,42', 'CHEVRON 100R', '59'),
('DL2-12412.pdf', 'CHEVRON_GROUP_II_220R', 'D', '35,36,37,42,43,44,45', 'CHEVRON 220R', '59'),
('DL2-12412.pdf', 'CHEVRON_GROUP_II_600R', 'D', '36,37,43,44,45', 'CHEVRON 600R', '59'),
('DL2-12412.pdf', 'NESTE_NEXBASE_3043', 'D', '28,29,35,37,38,42,45,46,54,55', 'Nexbase 3043', '59'),
('DL2-12412.pdf', 'NESTE_NEXBASE_3050', 'D', '16,17,18,19,21,30,36,39,44,47,48,49,54,57', 'Nexbase 3050', '59'),
('DL2-12412.pdf', 'NESTE_NEXBASE_3080', 'D', '40', 'NEXBASE 3080', '59'),
('DL2-12412.pdf', 'PETRONAS_ETRO_4', 'D', '42,45', 'ETRO 4', '59'),
('DL2-12412.pdf', 'S_OIL_ULTRA_S_4', 'D', '42,45', 'ULTRA S4', '59'),
('DL2-12412.pdf', 'YUBASE_4', 'D', '10,11,12,13,22,23,24,25,26,27,30,35,42,45,46,56', 'Yubase 4', '59'),
('DL2-12412.pdf', 'YUBASE_6', 'D', '36,44,47,48', 'YUBASE 6', '59'),
('DL2-12906.pdf', 'CHEVRON_GROUP_II_100R', 'D', '11', 'Chevron 100R', '14'),
('DL2-12906.pdf', 'CHEVRON_GROUP_II_110RLV', 'D', '2', 'Chevron 110RLV', '14'),
('DL2-12906.pdf', 'CHEVRON_GROUP_II_150R', 'D', '1,8,9,12,13', 'Chevron 150R', '14'),
('DL2-12906.pdf', 'CHEVRON_GROUP_II_220R', 'D', '2,3,4,5,6,7,8,9,10,11,12,13', 'Chevron 220R', '14'),
('DL2-12906.pdf', 'CHEVRON_GROUP_II_600R', 'D', '2,3,7,8,9,10,11,12,13', 'Chevron 600R', '14'),
('DL2-12906.pdf', 'NESTE_NEXBASE_3043', 'D', '2,3,4,5,6,11', 'Nexbase 3043', '14'),
('DL2-12906.pdf', 'NESTE_NEXBASE_3080', 'D', '4', 'Nexbase 3080', '14'),
('DL2-12906.pdf', 'PETRONAS_ETRO_4', 'D', '11', 'Etro 4', '14'),
('DL2-12906.pdf', 'YUBASE_4', 'D', '8,11,13', 'Yubase 4', '14'),
('DL2-13364.pdf', 'CHEVRON_GROUP_II_100R', 'D', '5', 'Chevron 100R', '18'),
('DL2-13364.pdf', 'CHEVRON_GROUP_II_220R', 'D', '5,10,11,12', 'Chevron 220R', '18'),
('DL2-13364.pdf', 'CHEVRON_GROUP_II_600R', 'D', '12', 'Chevron 600R', '18'),
('DL2-13364.pdf', 'EXXONMOBIL_APE_CORE_600', 'D', '17', 'AP/E Core 600', '18'),
('DL2-13364.pdf', 'NESTE_NEXBASE_3043', 'D', '3,5,10,11,12', 'Nexbase 3043', '18'),
('DL2-13364.pdf', 'NESTE_NEXBASE_3050', 'D', '3', 'Nexbase 3050', '18'),
('DL2-13364.pdf', 'NESTE_NEXBASE_3060', 'D', '3', 'Nexbase 3060', '18'),
('DL2-13364.pdf', 'YUBASE_4', 'D', '4,5,17,18', 'Yubase 4', '18'),
('DL2-13364.pdf', 'YUBASE_6', 'D', '4,17,18', 'Yubase 6', '18'),
]

b = Batch('non-duplicate review, batch 35: formulation decks (Afton HiTEC 34006 / 9490 / 12200 / 8788B, Oronite OLOA 54xxx, Oronite APAC summary) (nineteenth pass)')
RECIPE = 'a recipe share (wt.%) in finished-oil formulation tables; the KV, VI, CCS, MRV, HTHS, Noack, pour, BN and Brookfield figures on those pages are properties of the blends'
LABEL = "; Afton prints an 'API Group II' / 'API Group III' label beside each base oil (third-party label, not a manufacturer classification)"
F15608 = 'DL2-15608.pdf'
cov15608 = {pid: (f"not applicable for property values: another product's document (Afton HiTEC 34006 CVT formulations, 2024); on p.{pg} the product appears only as a recipe share with Afton's label "
                  f"'API Group III'; the record's API group is Missing -> one open-question row (third-party label). No property of the neat base oil is printed (pages without the name not read)")
            for pid, pg in (('NESTE_NEXBASE_3030', 9), ('S_OIL_ULTRA_S_3', 5), ('S_OIL_ULTRA_S_6', 5))}
b.doc(F15608, 'Afton HiTEC 34006 CVT formulations (one formulation per page with blend physical properties)', '2024 © Afton Chemical Corporation', FROZEN, RECIPE + LABEL, cov=cov15608)
b.doc('DL2-12412.pdf', 'Chevron Oronite OLOA 54000 series / OLOA 54050 / OLOA 54013 formulations and claims deck', '© 2017 Chevron (no other date)', FROZEN, RECIPE,
      ident={'S_OIL_ULTRA_S_4': "printed 'ULTRA S4' / 'Ultra S4' (no supplier name on the page); probable S-OIL Ultra-S 4, not verified; nothing used",
             'PETRONAS_ETRO_4': "printed 'ETRO 4' / 'Etro 4' (no supplier name on the page)"})
b.doc('DL2-12906.pdf', "Chevron Oronite Technology - Automotive 'Product Summary (Asia Pacific)' including Chevron 150R formulations",
      "'December 2019' (cover; slides marked © 2016)", FROZEN,
      "a 'Base Oils Ratio Only' share or a wt.% recipe share in package formulation tables with performance claims; p.12 note c 'Approved Group III base oils are SK and S-Oil' concerns OLOA 55501 routes, not a base-oil property")
cov13364 = {'EXXONMOBIL_APE_CORE_600': ("not applicable: another product's document (Afton HiTEC 9490 / 12200 / 8788B formulations); on p.17 the product appears only as a recipe share (18.0 %); the slide title reads "
                                        "'ExxonMobil AP/E Core Grp I & SK Yubase Grp III' while the row prints 'ExxonMobil AP/E Core 600 | API Group III'. That inconsistency was already raised for HiTEC 8788B in an earlier pass; "
                                        "the record's API group is 'Group I' (ExxonMobil web source). Third-party labels as printed; no row, nothing compared. No neat base-oil property printed (pages without the name not read)")}
b.doc('DL2-13364.pdf', 'Afton HiTEC 9490 (Nexbase / Yubase / Chevron), HiTEC 12200 and HiTEC 8788B formulation sheets', '2018-2020 © Afton Chemical Corporation (per slide)', FROZEN, RECIPE + LABEL, cov=cov13364)

TXT = {5: "'Formulation (%) wt. | HiTEC® 34006 | Additive Pack | 11.6 | Ultra S3 | API Group III | 54.4 | Ultra S6 | API Group III | 34.0' (p.5)",
       9: "'Formulation (%) wt. | HiTEC® 34006 | Additive Pack | 11.6 | Nexbase 3030 | API Group III | 41.2 | Nexbase 3060 | API Group III | 47.2' (p.9)"}
for pid, pg, old, orv in (
        ('S_OIL_ULTRA_S_3', 5, "DL2-11177.pdf (Ultra-S series sheet) prints no API group (only use 'in combination with conventional Group I or Group II base oils'); record API group Missing since the 2026-10 audit, with an open question listing indirect evidence only.",
         're-read manually: DL2-11177.pdf p.1 (only page) read in full (text layer)'),
        ('S_OIL_ULTRA_S_6', 5, "DL2-11177.pdf (Ultra-S series sheet) prints no API group (only use 'in combination with conventional Group I or Group II base oils'); record API group Missing since the 2026-10 audit, with an open question listing indirect evidence only.",
         're-read manually: DL2-11177.pdf p.1 (only page) read in full (text layer)'),
        ('NESTE_NEXBASE_3030', 9, "DL2-10962.pdf (Neste NEXBASE TDS, Edition 8): 'NEXBASE 3020 and NEXBASE 3030 are used in hydraulic and transmission oil formulations. The other grades ... conform to ACEA Group III'; no API group is printed for 3030 (VI spec '≥ 100', typ 111). Record API group Missing.",
         're-read manually: DL2-10962.pdf p.1 (only page; no text layer) viewed as a page image from the old archive')):
    b.row(p=pid, tier=1, path='api_group_chemistry.api_group', old=old, new_f=F15608, new_p=pg, new_text=TXT[pg], unit='(classification label)',
          form='third-party classification label (additive supplier formulation table)', outcome='additional', action='propose_open_question_update',
          reason=("An additive supplier's label beside the base oil in its own formulation table: it is not a manufacturer classification and cannot fill the mandatory API group. "
                  "Record it in the existing API-group open question as third-party evidence only (document, page, printed text). Other formulation documents that print the same kind of label "
                  "are not proposed again; they are named in their link coverage." + (" The label is not assessed here against Neste's printed VI or any group definition." if pid == 'NESTE_NEXBASE_3030' else
                  " It does not change the audit conclusion that no S-OIL document classifies the grade directly.")),
          old_rev=f'{orv} ({T})', cmp_override='existing: API group Missing')
b.write('zzzzzzzzzzzzzzzzzzz_b35_nondup_formulation_decks_2_nineteenth_pass.json')
