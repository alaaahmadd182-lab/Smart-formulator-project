"""Nineteenth pass, batch 39: open non-duplicate (category D) links of 14 short additive-supplier documents with base-oil
characterisation tables or labelled recipes: Richful RF6190 API SQ data summaries (DL2-15649, 15651-15656), Richful
RF6189 / RF6123 / RF6125 booklets, Lubrizol 21303A formulation summary DL2-11732 (2011), Afton HiTEC 11180 dexos1 Gen 2
formulations (DL2-13230, DL2-12085) and the Afton HiTEC 34321 ATF bulletin DL2-12593.
Every name-hit page read in full on the text layer; the pages behind the evidence also viewed as images (stated per
document). One new row (Ultra-S 8 API-group label). To avoid duplicate proposals, the new third-party evidence for fields
that already have an open-question row (EHC KV40, YUBASE 4 / 6 density and saturates) is ADDED to those rows through
field_overrides (new_text extended, reason appended with the batch and date); the original rows stay as written.
Writes decisions/zzzzzzzzzzzzzzzzzzz_b39_nondup_richful_afton_lubrizol_summaries_nineteenth_pass.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nd_common import B, Batch, T, to_root
to_root()

FROZEN = [
('DL2-15649.pdf', 'EXXONMOBIL_EHC_110', 'D', '1,5', 'EHC 110', '5'),
('DL2-15649.pdf', 'EXXONMOBIL_EHC_50', 'D', '1,5', 'EHC 50', '5'),
('DL2-15651.pdf', 'YUBASE_4', 'D', '1,4', 'Yubase 4', '4'),
('DL2-15652.pdf', 'YUBASE_4', 'D', '1,4', 'Yubase 4', '4'),
('DL2-15653.pdf', 'EXXONMOBIL_EHC_50', 'D', '1,4', 'EHC 50', '4'),
('DL2-15653.pdf', 'YUBASE_4', 'D', '1,4', 'Yubase 4', '4'),
('DL2-15654.pdf', 'EXXONMOBIL_EHC_45', 'D', '1,4', 'EHC 45', '4'),
('DL2-15654.pdf', 'EXXONMOBIL_EHC_65', 'D', '1,4', 'EHC 65', '4'),
('DL2-15655.pdf', 'EXXONMOBIL_EHC_50', 'D', '1,4', 'EHC 50', '4'),
('DL2-15656.pdf', 'EXXONMOBIL_EHC_50', 'D', '1,4', 'EHC 50', '4'),
('RF6189%20booklet.pdf', 'EXXONMOBIL_EHC_110', 'D', '1,3', 'EHC 110', '3'),
('RF6189%20booklet.pdf', 'EXXONMOBIL_EHC_50', 'D', '1,3', 'EHC 50', '3'),
('RF6123%20%20booklet.pdf', 'YUBASE_4', 'D', '3,7', 'Yubase 4', '7'),
('RF6123%20%20booklet.pdf', 'YUBASE_6', 'D', '3,7', 'Yubase 6', '7'),
('RF6125%20booklet.pdf', 'YUBASE_4', 'D', '3,5', 'Yubase 4', '5'),
('DL2-11732.PDF', 'YUBASE_4', 'D', '4,5', 'YUBASE 4', '5'),
('DL2-11732.PDF', 'YUBASE_6', 'D', '4,5', 'YUBASE 6', '5'),
('DL2-13230.pdf', 'S_OIL_ULTRA_S_4', 'D', '4', 'Ultra-S 4', '8'),
('DL2-13230.pdf', 'S_OIL_ULTRA_S_8', 'D', '4', 'Ultra-S 8', '8'),
('DL2-13230.pdf', 'YUBASE_4', 'D', '6', 'Yubase 4', '8'),
('DL2-13230.pdf', 'YUBASE_6', 'D', '6', 'Yubase 6', '8'),
('DL2-12085.pdf', 'YUBASE_4', 'D', '8', 'Yubase 4', '11'),
('DL2-12085.pdf', 'YUBASE_6', 'D', '8', 'Yubase 6', '11'),
('DL2-12593.pdf', 'CHEVRON_GROUP_II_100R', 'D', '2', 'Chevron 100R', '2'),
('DL2-12593.pdf', 'CHEVRON_GROUP_II_220R', 'D', '2', 'Chevron 220R', '2'),
]
Q = 'no package record; added to the new-product candidate queue in this batch'
b = Batch('non-duplicate review, batch 39: Richful RF6190 / RF6189 / RF6123 / RF6125 summaries, Lubrizol 21303A, Afton HiTEC 11180 / 34321 (nineteenth pass)')
A = lambda pages: f'assessed by reading (2026-11-14, nineteenth pass) for the name-hit pages {pages} only: '
RCH = "Richful 'Base Oil Characterization' table (no lot number, no date of analysis)"

# Richful RF6190 data summaries: p.1 formulation + engine tests, last page characterisation table
EHC = {'EXXONMOBIL_EHC_45': ('4.68', '23.42', '118', '14.7'), 'EXXONMOBIL_EHC_50': ('5.50', '31.09', '115', '13.8'),
       'EXXONMOBIL_EHC_65': ('6.44', '41.90', '103', '10.3'), 'EXXONMOBIL_EHC_110': ('10.60', '95.00', '95', '5.9')}
def ehc_cov(pid, pages, f):
    kv, k4, vi, nk = EHC[pid]
    return (A(pages) + f"p.1 recipe share in an RF6190 / RF6189 finished-oil formulation; {RCH}: KV100 {kv}, KV40 {k4} mm2/s (ASTM D445), VI {vi}, Noack {nk} wt.%, S '<0.0003' wt.%. "
            "The KV40 is added to the batch 38 KV40 open-question row (field override, not a second proposal); the KV100 and VI lie inside the record's specification ranges (observation only).")
Y4R = "Yubase 4: KV100 4.20, KV40 19.30, VI 123, Noack 11.0"
for f, prods, pages, title in (
        ('DL2-15649.pdf', ('EXXONMOBIL_EHC_50', 'EXXONMOBIL_EHC_110'), '1 and 5', 'RF6190 API SQ 15W-40'),
        ('DL2-15653.pdf', ('EXXONMOBIL_EHC_50',), '1 and 4', 'RF6190 API SQ / ILSAC GF-7 5W-20'),
        ('DL2-15654.pdf', ('EXXONMOBIL_EHC_45', 'EXXONMOBIL_EHC_65'), '1 and 4', 'RF6190 API SQ / ILSAC GF-7 5W-30'),
        ('DL2-15655.pdf', ('EXXONMOBIL_EHC_50',), '1 and 4', 'RF6190 API SQ / ILSAC GF-7 5W-30 (with ADNOC 4)'),
        ('DL2-15656.pdf', ('EXXONMOBIL_EHC_50',), '1 and 4', 'RF6190 API SQ / ILSAC GF-7 5W-30 (with CTL 4)'),
        ('RF6189%20booklet.pdf', ('EXXONMOBIL_EHC_50', 'EXXONMOBIL_EHC_110'), '1 and 3', 'RF6189 API SP 10W-40')):
    cov = {p: ehc_cov(p, pages, f) for p in prods}
    if f == 'DL2-15653.pdf':
        cov['YUBASE_4'] = A(pages) + f"p.1 recipe share; {RCH}: {Y4R}, S '<0.0003' wt.%; no Missing field of the record is informed (KV / VI / Noack recorded from DL2-11304.pdf). No row."
    b.doc(f, f'Richful {title} gasoline engine oil data summary (formulation, engine and bench results, base-oil characterization)', 'not printed', FROZEN, 'a recipe share', cov=cov,
          viewed='p.5 also viewed as a page image' if f == 'DL2-15649.pdf' else '',
          route=f"Richful {'RF6189' if 'RF6189' in f else 'RF6190'} ({Q}) with Lubrizol LZ 7077 (VM; not assessed by these links)")
for f, pages, title in (('DL2-15651.pdf', '1 and 4', 'RF6190 API SQ / ILSAC GF-7 0W-20'), ('DL2-15652.pdf', '1 and 4', 'RF6190 API SQ / ILSAC GF-7 0W-30')):
    extra = (" The sulfur row prints 'S, wt.% | <3 | <3' (checked on the page image), where the other RF6190 summaries print '<0.0003' wt.%: a unit or value anomaly of the source, kept as printed and not used."
             if f == 'DL2-15652.pdf' else " S '<0.0003' wt.%.")
    b.doc(f, f'Richful {title} gasoline engine oil data summary', 'not printed', FROZEN, 'a recipe share',
          cov={'YUBASE_4': A(pages) + f"p.1 recipe share; {RCH}: {Y4R}.{extra} No Missing field of the record is informed. No row."},
          viewed='p.4 also viewed as a page image' if f == 'DL2-15652.pdf' else '',
          route=f'Richful RF6190 ({Q}) with Lubrizol LZ 7077 (VM; not assessed by these links)')
b.doc('RF6123%20%20booklet.pdf', 'Richful RF6123 ACEA-2023 C3 5W-30 passenger car engine oil data summary', 'not printed', FROZEN, 'a recipe share',
      cov={'YUBASE_4': A('3 and 7') + f"p.3 recipe share; p.7 {RCH}: {Y4R}, 'Saturate, wt.% | 93.0' (ASTM D2007), S '＜0.001'. The saturates value is added to the batch 34 YUBASE 4 saturates open-question row (field override).",
           'YUBASE_6': A('3 and 7') + f"p.3 recipe share; p.7 {RCH}: Yubase 6 KV100 6.33, KV40 34.99, VI 133, Noack 5.2, 'Saturate, wt.% | 97.9' (ASTM D2007), S '＜0.001'. The saturates value is added to the batch 38 YUBASE 6 saturates open-question row (field override)."},
      viewed='p.7 also viewed as a page image', route=f'Richful RF6123 ({Q}) with Lubrizol LZ 7077 and RF8248 (not assessed by these links)')
b.doc('RF6125%20booklet.pdf', 'Richful RF6125 ACEA-2023 C5 0W-20 passenger car engine oil data summary', 'not printed', FROZEN, 'a recipe share',
      cov={'YUBASE_4': A('3 and 5') + f"p.3 recipe share; p.5 {RCH}: {Y4R}, 'Saturate, wt.% | 93.0' (ASTM D2007), S '＜0.001' (the same figures as RF6123; named in the saturates override, not proposed again)."},
      route=f'Richful RF6125 ({Q}) with RF6661 and RF8248B (not assessed by these links)')
b.doc('DL2-11732.PDF', "Lubrizol 21303A API SN formulation summary ('Formulations tested to support the final formulation', 'C-12479 HLWH Jan 2011')", "'Jan 2011' (page footer)", FROZEN,
      "a recipe share labelled '[Gp III]' by Lubrizol (Yubase 4 and Yubase 6 records already carry Group III from SK)",
      route=f'Lubrizol 21303A DI with Lubrizol 7418 / 7418A VM and 7749B PPD ({Q})')
cov13230 = {
    'S_OIL_ULTRA_S_8': A('4') + "p.4 recipe share in 'dexos1TM Gen 2 Ultra-S Final Formulations' with the label 'Ultra-S 8, Group III' and '7.06' lbs/gal ('* Properties from Base Oil Specification Sheet', no temperature). The record's API group is Missing -> one open-question row (third-party label). The 'Base Oil Properties' (98.5 / 0.000 / 4.435 / 129 and 98.2 / 0.000 / 4.871 / 130) belong to the formulations' base-oil blends, not to a neat oil.",
    'S_OIL_ULTRA_S_4': A('4') + "p.4 recipe share labelled 'Ultra-S 4, Group III' (the batch 36 API-group open-question row already carries Afton's label; not proposed again) and '6.96' lbs/gal (no temperature; record density recorded from S-OIL, not compared).",
    'YUBASE_4': A('6') + "p.6 recipe share labelled 'Yubase 4, Group III' with '6.95' lbs/gal ('* Properties from Base Oil Specification Sheet', no temperature): added to the batch 38 YUBASE 4 density open-question row (field override); not converted.",
    'YUBASE_6': A('6') + "p.6 recipe share labelled 'Yubase 6, Group III' with '7.01' lbs/gal (no temperature): added to the batch 38 YUBASE 6 density open-question row (field override); not converted.",
}
b.doc('DL2-13230.pdf', 'Afton HiTEC 11180 dexos1 Gen 2 / ILSAC GF-6 final formulations (Ultra-S p.4, Yubase p.6)', 'not printed on the pages read', FROZEN, 'a recipe share', cov=cov13230,
      viewed='p.4 also viewed as a page image', route=f'Afton HiTEC 11180 with HiTEC 5754A VM ({Q})')
b.doc('DL2-12085.pdf', 'Afton HiTEC 11180 dexos1 Gen 2 Yubase final formulations (p.8; the same table as DL2-13230.pdf p.6)', 'not printed on the pages read', FROZEN, 'a recipe share',
      cov={p: A('8') + f"p.8 recipe share with the lbs/gal value already listed from DL2-13230.pdf p.6 ({'6.95' if p == 'YUBASE_4' else '7.01'}); nothing new; no row." for p in ('YUBASE_4', 'YUBASE_6')},
      route=f'Afton HiTEC 11180 with HiTEC 5754A VM ({Q})')
b.doc('DL2-12593.pdf', "Afton HiTEC 34321 multi-vehicle ATF additive package bulletin ('11/18'), typical formulations GM IIIH / IID / TASA", "'11/18'", FROZEN,
      'a recipe share (% wt.) in the typical formulations; KV100, Brookfield and KRL figures are properties of the blends', route=f'Afton HiTEC 34321 ({Q})')

b.row(p='S_OIL_ULTRA_S_8', tier=1, path='api_group_chemistry.api_group',
      old="DL2-11177.pdf (Ultra-S series sheet) prints no API group (only use 'in combination with conventional Group I or Group II base oils'); record API group Missing since the 2026-10 audit, with an open question listing indirect evidence only.",
      new_f='DL2-13230.pdf', new_p=4, new_text="'dexos1TM Gen 2 Ultra-S Final Formulations | Components | lbs/gal *' row 'Ultra-S 8, Group III | 7.06 | 7.00 | 7.00 | 20.50 | 20.59'", unit='(classification label)',
      form='third-party classification label (additive supplier formulation table)', outcome='additional', action='propose_open_question_update',
      reason=("An additive supplier's label in its own formulation table: not a manufacturer classification, so it cannot fill the mandatory API group. Record it in the existing API-group open question "
              "as third-party evidence only. It does not change the audit conclusion that no S-OIL document classifies Ultra-S 8 directly, and it does not bear on ID-01 (aramcoULTRA 8 vs Ultra-S 8), which stays open."),
      old_rev=f're-read manually: DL2-11177.pdf p.1 (only page) read in full (text layer) ({T})', cmp_override='existing: API group Missing')

# Add the new evidence to the existing open-question rows (no second proposal for the same field)
src = {n: json.load(open(f'{B}/decisions/{n}', encoding='utf-8'))['fields'] for n in (
    'zzzzzzzzzzzzzzzzzzz_b34_nondup_formulation_decks_1_nineteenth_pass.json', 'zzzzzzzzzzzzzzzzzzz_b38_nondup_afton_cdp_characterisations_nineteenth_pass.json')}
def orig(p, path, nf):
    hit = [r for rows in src.values() for r in rows if r['p'] == p and r['path'] == path and r['new_f'] == nf]
    assert len(hit) == 1, (p, path, nf, len(hit))
    return hit[0]['new_text']
F22 = 'HiTEC%2022300%20CDP_API%20SL%20AramcoPrima.pdf'
TAG = f' [Batch 39 ({T}): added third-party evidence from documents read in that batch; see new_source_printed.]'
def add(p, path, nf, more):
    b.overrides.append(dict(p=p, path=path, new_f=nf, new_text=orig(p, path, nf) + '; ADDED in batch 39: ' + more, reason_append=TAG.strip()))
for p, files in (('EXXONMOBIL_EHC_45', 'DL2-15654.pdf p.4'), ('EXXONMOBIL_EHC_50', 'DL2-15649.pdf p.5, DL2-15653 / 15655 / 15656.pdf p.4, RF6189 booklet p.3'),
                 ('EXXONMOBIL_EHC_65', 'DL2-15654.pdf p.4'), ('EXXONMOBIL_EHC_110', 'DL2-15649.pdf p.5, RF6189 booklet p.3')):
    add(p, 'kv40', F22, f"{RCH} 'Kinematic Viscosity (40℃), mm2/s | {EHC[p][1]} | ASTM D445' ({files}; Richful RF6190 / RF6189 summaries)")
add('YUBASE_4', 'density', F22, "'Yubase 4, Group III | 6.95' under 'lbs/gal *' with '* Properties from Base Oil Specification Sheet' (Afton HiTEC 11180, DL2-13230.pdf p.6; also DL2-12085.pdf p.8); no temperature; not converted")
add('YUBASE_6', 'density', F22, "'Yubase 6, Group III | 7.01' under 'lbs/gal *' ('* Properties from Base Oil Specification Sheet'; DL2-13230.pdf p.6, DL2-12085.pdf p.8); no temperature; not converted")
add('YUBASE_4', 'saturates', 'DL2-15799.pdf', f"{RCH} 'Saturate, wt.% | 93.0 | ASTM D2007' (RF6123 booklet p.7; same in RF6125 booklet p.5) and (read in batch 38, named there in coverage only) Afton lots RIC22-02745 96.5, RIC23-08617 98.6 (HiTEC 22300 book p.14), B18-138 96.3 (DL2-15777.pdf p.12)")
add('YUBASE_6', 'saturates', F22, f"{RCH} 'Saturate, wt.% | 97.9 | ASTM D2007' (RF6123 booklet p.7)")

b.visual += [
    dict(f='DL2-13230.pdf', page=4, checked="'dexos1TM Gen 2 Ultra-S Final Formulations' component table", result='confirmed',
         detail="'Ultra-S 4, Group III | 6.96', 'Ultra-S 8, Group III | 7.06', 'Yubase 4PLUS, Group III | 6.88' under 'lbs/gal *' ('* Properties from Base Oil Specification Sheet'); Base Oil Properties 98.5 / 0.000 / 4.435 / 129 and 98.2 / 0.000 / 4.871 / 130 (blends)."),
    dict(f='DL2-15649.pdf', page=5, checked="Richful 'Table 6 Base Oil Characterization'", result='confirmed', detail='EHC 50 5.50 / 31.09 / 115 / 13.8 / <0.0003; EHC 110 10.60 / 95.00 / 95 / 5.9 / <0.0003, as cited.'),
    dict(f='DL2-15652.pdf', page=4, checked="Richful 'Table 5 Base Oil Characterization' sulfur row", result='confirmed', detail="'S, wt.% | <3 | <3 | ASTM D2622' printed for Yubase 4 and Yubase 4P (the other summaries print <0.0003 wt.%): source anomaly, kept as printed."),
    dict(f='RF6123%20%20booklet.pdf', page=7, checked="Richful 'Table 5 Base Oil Characterization'", result='confirmed', detail="Yubase 4 4.20 / 19.30 / 123 / 11.0 / Saturate 93.0 / ＜0.001; Yubase 6 6.33 / 34.99 / 133 / 5.2 / 97.9 / ＜0.001 (ASTM D445, D2270, D5800, D2007, D2622)."),
]
b.queue += [dict(name_as_printed=n, supplier=s, file=f, page=pg, evidence=e) for n, s, f, pg, e in (
    ('Richful RF6190', 'Richful', 'DL2-15649.pdf', '1-5', 'API SQ / ILSAC GF-7 data summaries at 8.3 wt.% with LZ 7077 (DL2-15649, 15651-15656): engine tests, elastomers, base-oil characterization'),
    ('Richful RF6189', 'Richful', 'RF6189%20booklet.pdf', '1-3', 'API SP 10W-40 data summary at 7.68 wt.%'),
    ('Richful RF6123', 'Richful', 'RF6123%20%20booklet.pdf', '3-7', 'ACEA-2023 C3 5W-30 data summary at 10.4 wt.%'),
    ('Richful RF6125', 'Richful', 'RF6125%20booklet.pdf', '3-5', 'ACEA-2023 C5 0W-20 data summary at 10.4 wt.%'),
    ('Lubrizol 21303A', 'Lubrizol', 'DL2-11732.PDF', '4-5', 'API SN formulations at 10.90 / 11.30 mass % with Lubrizol 7418 / 7418A VM and 7749B PPD (Jan 2011)'),
    ('HiTEC 11180', 'Afton', 'DL2-13230.pdf', '4, 6', 'dexos1 Gen 2 / GF-6 final formulations at 10.10 wt.% with HiTEC 5754A (also DL2-12085.pdf p.8)'),
    ('HiTEC 34321', 'Afton', 'DL2-12593.pdf', '2', 'multi-vehicle ATF package: 8.2 % wt. IIIH, 6.0 % IID, 4.1 % TASA; density 0.912 g/ml at 15 °C, KV100 277 cSt (11/18)'))]
b.write('zzzzzzzzzzzzzzzzzzz_b39_nondup_richful_afton_lubrizol_summaries_nineteenth_pass.json')
