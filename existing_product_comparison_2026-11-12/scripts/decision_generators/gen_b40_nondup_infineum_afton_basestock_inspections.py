"""Nineteenth pass, batch 40: open non-duplicate (category D) base-oil links of five candidate data packages with
sample- or lot-numbered base-stock inspection tables: Afton HiTEC 12200 core datasets DL2-11706; Infineum CDP M418
(D3494, February 2017) DL2-11766; Infineum CDP 595 (D3503, June 2017) DL2-11768; Infineum INF-CDP-730 (P5807, API SN
PLUS RC) DL2-11763; Infineum CDP-659 (P6660, March 2018) DL2-11762.
Every name-hit page read in full on the text layer; the four inspection tables also viewed as page images.
The INFINEUM_D3503 link on DL2-11768 (the package's own data package) is NOT closed here: it needs a package review.
New rows: Chevron 100R / 220R KV100 (mandatory, Missing), SpectraSyn 4 saturates, Ultra-S 4 / 8 saturates notes.
Evidence for fields that already have open rows is added through field_overrides (EHC 45 / 110 KV40, YUBASE 4 / 6 and
Chevron 600R saturates). Writes decisions/zzzzzzzzzzzzzzzzzzz_b40_nondup_infineum_afton_basestock_inspections_nineteenth_pass.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nd_common import B, Batch, T, to_root
to_root()

FROZEN = [r for r in [
('DL2-11706.pdf', 'CHEVRON_GROUP_II_100R', 'D', '9,19,29', 'Chevron 100R', '35'),
('DL2-11706.pdf', 'CHEVRON_GROUP_II_220R', 'D', '16,19,22,26,29,32', 'Chevron 220R', '35'),
('DL2-11706.pdf', 'CHEVRON_GROUP_II_600R', 'D', '9,16,19,22,26,29,32', 'Chevron 600R', '35'),
('DL2-11706.pdf', 'EXXONMOBIL_APE_CORE_150', 'D', '3,9', 'AP/E Core 150', '35'),
('DL2-11706.pdf', 'EXXONMOBIL_APE_CORE_600', 'D', '3,9', 'AP/E Core 600', '35'),
('DL2-11706.pdf', 'EXXONMOBIL_EHC_110', 'D', '3,16,19,22,26,29,32', 'EHC 110', '35'),
('DL2-11706.pdf', 'EXXONMOBIL_EHC_50', 'D', '3,16,19,22,26,29,32', 'EHC 50', '35'),
('DL2-11766.pdf', 'CHEVRON_GROUP_II_100R', 'D', '4,15', 'CHEVRON 100R', '31'),
('DL2-11766.pdf', 'CHEVRON_GROUP_II_220R', 'D', '4,8,9,13,15', 'CHEVRON 220R', '31'),
('DL2-11766.pdf', 'CHEVRON_GROUP_II_600R', 'D', '4,8,9,13,15', 'CHEVRON 600R', '31'),
('DL2-11766.pdf', 'EXXONMOBIL_EHC_110', 'D', '4,15,19', 'EHC 110', '31'),
('DL2-11766.pdf', 'EXXONMOBIL_EHC_45', 'D', '4,15,19', 'EHC 45', '31'),
('DL2-11766.pdf', 'YUBASE_6', 'D', '4,15,19', 'Yubase 6', '31'),
('DL2-11768.pdf', 'CHEVRON_GROUP_II_100R', 'D', '4,10,13', 'CHEVRON 100R', '23'),
('DL2-11768.pdf', 'CHEVRON_GROUP_II_220R', 'D', '4,6,8,10,11,13,16', 'CHEVRON 220R', '23'),
('DL2-11768.pdf', 'CHEVRON_GROUP_II_600R', 'D', '6,11', 'CHEVRON 600R', '23'),
('DL2-11768.pdf', 'EXXONMOBIL_EHC_110', 'D', '4,10,13', 'EHC 110', '23'),
('DL2-11768.pdf', 'EXXONMOBIL_EHC_45', 'D', '4,10,13', 'EHC 45', '23'),
('DL2-11768.pdf', 'INFINEUM_D3503', 'D,E', '1,2,3,4,6,8,10,11,16', 'Infineum D3503', '23'),
('DL2-11763.pdf', 'EXXONMOBIL_EHC_45', 'D', '10', 'EHC45', '20'),
('DL2-11763.pdf', 'S_OIL_ULTRA_S_4', 'D', '3,8,9', 'ULTRA S4', '20'),
('DL2-11763.pdf', 'S_OIL_ULTRA_S_8', 'D', '3,8,9', 'ULTRA S8', '20'),
('DL2-11763.pdf', 'YUBASE_4', 'D', '3,5,6,8,9,10,17,18', 'YUBASE 4', '20'),
('DL2-11763.pdf', 'YUBASE_6', 'D', '3,5,6,8,9,10,17,18', 'YUBASE 6', '20'),
('DL2-11762.pdf', 'EXXONMOBIL_SPECTRASYN_4', 'D', '4,14', 'Spectrasyn 4', '16'),
('DL2-11762.pdf', 'YUBASE_4', 'D', '4,8,9,10,12,14', 'Yubase 4', '16'),
('DL2-11762.pdf', 'YUBASE_6', 'D', '4,8,9,10,12,14', 'Yubase 6', '16'),
] if r[1] != 'INFINEUM_D3503']   # package's own link: left open for a package review

Q = 'no package record; added to the new-product candidate queue in this batch'
b = Batch('non-duplicate review, batch 40: Afton HiTEC 12200 core datasets and four Infineum CDP base-stock inspection tables (nineteenth pass)')
A = lambda pages: f'assessed by reading (2026-11-14, nineteenth pass) for the name-hit pages {pages} only: '
BLEND = "the 'Base Oil Viscosity / Viscosity Index / Sulfur / Saturates' rows of the core datasets belong to each test oil's base-oil blend, not to a neat oil, and the text layer does not keep the column order (no column value used)"
b.doc('DL2-11706.pdf', 'Afton HiTEC 12200 typical formulations (p.3) and API CI-4 / SL / ACEA E7 core datasets (pp.9-32)', 'not printed on the pages read', FROZEN,
      f'a recipe share; {BLEND}', route='Afton HiTEC 12200 (record exists; its own links are reviewed separately) with HiTEC 9552, 672, 5748 / 5748A')

S220 = "samples 14021464 (6.479 / 41.283 / 107 / sat 96.5), 12015827 (6.47 / 41.518 / 107 / 97.7), 11012963 (6.61 / 43.51 / 103 / 96.2)"
cov66 = {
    'CHEVRON_GROUP_II_100R': A('4 and 15') + "pp.4, 15 recipe shares; the 'Base Stock Analysis' (p.19, not a name hit for this product: printed '100R') sample 10012866: KV100 4.07, KV40 19.89, VI 103, saturates 97.2 %, sulfur <0.001 -> the Chevron 100R KV100 row of this batch.",
    'CHEVRON_GROUP_II_220R': A('4, 8, 9, 13 and 15') + f"recipe shares (CJ-4 / SN programme); p.19 (printed '220R', producer Chevron) {S220}; a third '220R' column, sample 12015818, prints 11.91 / 103.05 and is named 'Chevron 600R' in DL2-11768.pdf p.13: label inconsistency of the source, that sample is used for neither product -> the Chevron 220R KV100 row of this batch.",
    'CHEVRON_GROUP_II_600R': A('4, 8, 9, 13 and 15') + "recipe shares; the 600R sample of p.19 is printed under '220R' (see the 220R link); only DL2-11768.pdf names it Chevron 600R (added to the batch 34 600R saturates row with the inconsistency stated).",
    'EXXONMOBIL_EHC_110': A('4, 15 and 19') + "recipe shares; p.19 sample 11014321: KV100 10.47, KV40 91.22, VI 96, saturates 92.6 % -> added to the batch 38 EHC 110 KV40 row (field override).",
    'EXXONMOBIL_EHC_45': A('4, 15 and 19') + "recipe shares; p.19 samples 09010520 (4.64 / 23.38 / 115 / 92.9) and 09010605 (4.63 / 23.3 / 115 / 92.8) -> added to the batch 38 EHC 45 KV40 row (field override).",
    'YUBASE_6': A('4, 15 and 19') + "recipe shares; p.19 'Yubase6' (producer 'Yukong', Group III) sample 11013747: KV100 6.56, KV40 37.22, VI 131, saturates 98.2 % -> added to the batch 38 YUBASE 6 saturates row (field override).",
}
b.doc('DL2-11766.pdf', "Infineum CDP M418 (Infineum D3494 API CJ-4 / SN candidate data package), 'Base Stock Analysis' p.19", "'February 2017'", FROZEN, 'a recipe share', cov=cov66,
      viewed='p.19 also viewed as a page image', route='Infineum D3494 (no package record; already in the candidate queue from DL2-13801.pdf, this document added as further evidence) with Paratone 68231, Infineum V385 / V387')
cov68 = {
    'CHEVRON_GROUP_II_100R': A('4, 10 and 13') + "recipe shares; p.13 'Chevron 100R' sample 12015817: KV40 19.63, KV100 4.04, VI 103, saturates 93.8 % -> the Chevron 100R KV100 row of this batch.",
    'CHEVRON_GROUP_II_220R': A('4, 6, 8, 10, 11, 13 and 16') + "recipe shares; p.13 'Chevron 220R' samples 12015827 (41.46 / 6.47 / 106 / 97.7), LN14015495 (41.43 / 6.47 / 106 / 98.2), LN14021464 (41.36 / 6.48 / 107 / 96.5) -> the Chevron 220R KV100 row of this batch.",
    'CHEVRON_GROUP_II_600R': A('6 and 11') + "recipe shares (p.13 is not a name hit for this product's alias but was read: 'Chevron 600R' sample LN12015818: KV40 102.85, KV100 11.90, VI 105, sulfur 0.001, saturates 97.3 %) -> added to the batch 34 600R saturates row (field override).",
    'EXXONMOBIL_EHC_110': A('4, 10 and 13') + "recipe shares; p.13 'EHC110' sample 11014321 (91.22 / 10.47 / 96 / 92.6), the same sample as DL2-11766.pdf p.19.",
    'EXXONMOBIL_EHC_45': A('4, 10 and 13') + "recipe shares; p.13 'EHC45' sample 14034439: KV40 22.69, KV100 4.56, VI 116, saturates 93.2 % -> added to the batch 38 EHC 45 KV40 row (field override).",
}
b.doc('DL2-11768.pdf', "Infineum CDP 595 (Infineum D3503 API CK-4 / SN candidate data package), 'Base stock Information' p.13", "'June 2017'", FROZEN, 'a recipe share', cov=cov68,
      viewed='p.13 also viewed as a page image',
      route='Infineum D3503 (record exists; its own link on this document stays OPEN for a package review: claims, route and treat rate are not assessed here) with Infineum SV261L, Paratone 68231, V385 / V387')
cov63 = {
    'EXXONMOBIL_EHC_45': A('10') + "p.10 'Level 2 Support for the Sequence IIIG' table only (EHC 45 named in it); no property of the neat base oil.",
    'S_OIL_ULTRA_S_4': A('3, 8 and 9') + "recipe shares; p.9 'Ultra S4' (manufacturer 'S Oil', API Group III) lot 12015322: VI 124, KV100 4.27, KV40 19.76, sulphur 0.001, saturates 97.5 % (ASTM D2007) -> note against the record '>99 wt%'; Infineum's group label is of the same kind as the batch 36 row and is not proposed again.",
    'S_OIL_ULTRA_S_8': A('3, 8 and 9') + "recipe shares; p.9 'Ultra S8' lot 12015242: VI 131, KV100 7.13, KV40 42.22, sulphur 0.001, saturates 96.53 % -> note against '>99 wt%'; group label as in the batch 39 row, not proposed again.",
    'YUBASE_4': A('3, 5, 6, 8, 9, 10, 17 and 18') + "recipe shares; p.9 lots 13102339 (98.5), 14011472 (98.6), 16027383 (98.0), LN12014855 (98.1) saturates % -> added to the batch 34 YUBASE 4 saturates row (field override).",
    'YUBASE_6': A('3, 5, 6, 8, 9, 10, 17 and 18') + "recipe shares; p.9 lots 12015695 (97.62), 16012596 (98.2), LN11013747 (98.15) saturates % -> added to the batch 38 YUBASE 6 saturates row (field override).",
}
b.doc('DL2-11763.pdf', "Infineum INF-CDP-730 (Infineum P5807 with Paratone 50 SSI, API SN PLUS RC), 'Basestock Inspections' p.9", 'not printed on the pages read', FROZEN, 'a recipe share', cov=cov63,
      viewed="p.9 also viewed as a page image (the Motiva 'Star 4' / 'Star 6' columns are visibly shifted in the source; not used)",
      route=f'Infineum P5807 ({Q}) with Paratone 50 SSI / 68530, Infineum SV265, V362, V387')
cov62 = {
    'EXXONMOBIL_SPECTRASYN_4': A('4 and 14') + "p.4 recipe share; p.14 'SPECTRASYN4' (ExxonMobil, Group IV) sample LN04001024: VI 124, sulfur 0.0003, saturates 96.9 %, KV100 4.08, KV40 18.28 -> SpectraSyn 4 saturates (Missing) open-question row.",
    'YUBASE_4': A('4, 8, 9, 10, 12 and 14') + "recipe shares; p.14 samples LN09009384 (98.1), LN11013660 (97.72), LN15012069 (98.2), LN11014322 (97.9), LN16022692 (99.4) saturates % -> added to the batch 34 YUBASE 4 saturates row.",
    'YUBASE_6': A('4, 8, 9, 10, 12 and 14') + "recipe shares; p.14 samples LN08008620 (98.2), LN16013666 (98.6), LN12015842 (97.8) saturates % -> added to the batch 38 YUBASE 6 saturates row.",
}
b.doc('DL2-11762.pdf', "Infineum CDP-659 (Infineum P6660 ACEA A3/B4-16 candidate data package), 'Basestock Information' p.14", "'March 2018'", FROZEN, 'a recipe share', cov=cov62,
      viewed='p.14 also viewed as a page image', route=f'Infineum P6660 ({Q}) with Infineum SV261 / SV603, V385')

OLD_CH = 're-read manually: DL2-10004.pdf p.1 (Group II/II+ specifications, 1/2018) read in full (text layer) (' + T + ')'
for pid, g, spec, txt in (
        ('CHEVRON_GROUP_II_100R', '100R', "KV40 '18.7 – 20.8', KV100 'Report', VI '95 (MIN)'",
         "DL2-11766.pdf p.19 '100R | Chevron | II | 10012866 | VI 103 | Sulfur <0.001 | Saturates 97.2 | KV@100C 4.07 | KV@40C 19.89'; DL2-11768.pdf p.13 'Chevron 100R | 12015817 | VI 103 | KV-40 19.63 | KV-100 4.04 | Sulfur <0.001 | Saturates 93.8'"),
        ('CHEVRON_GROUP_II_220R', '220R', "KV40 '40.0 – 46.0', KV100 'Report', VI '95 (MIN)'",
         f"DL2-11766.pdf p.19 '220R' {S220}; DL2-11768.pdf p.13 'Chevron 220R' 12015827 (KV-100 6.47), LN14015495 (6.47), LN14021464 (6.48) (ASTM D445)")):
    b.row(p=pid, tier=1, path='kv100', old=f"DL2-10004.pdf (Chevron Group II/II+ specifications, 1/2018) prints for {g}: {spec}. Record KV100 Missing (mandatory).",
          new_f='DL2-11768.pdf', new_p=13, new_text=txt, unit='cSt', form='batch measurement of the neat base oil by a third party (Infineum sample IDs)', method='ASTM D445', cond='100 °C; neat base oil, individual samples',
          outcome='additional', action='propose_open_question_update',
          reason=("Sample analyses by Infineum in its candidate data packages (2017), not manufacturer typicals or specifications: they cannot fill the mandatory KV100, for which Chevron prints 'Report'. "
                  "Record them in an open question as batch evidence with the sample IDs. The sample KV40 and VI lie inside or meet the record's limits (observation only). Sample 12015818, printed '220R' in DL2-11766.pdf "
                  "but 'Chevron 600R' in DL2-11768.pdf, is excluded from both products."),
          old_rev=OLD_CH, cmp_override='existing: KV100 Missing')
b.row(p='EXXONMOBIL_SPECTRASYN_4', tier=3, path='saturates', old="DL2-11332.pdf (SpectraSyn 4 product datasheet, 07/30/2015) prints typical SG, KV, VI, pour, flash, Noack, CCS, MRV and others, and no saturates row; record saturates Missing.",
      new_f='DL2-11762.pdf', new_p=14, new_text="'SPECTRASYN4 | EXXONMOBIL | IV | LN04001024 | OM 646LA | VI 124 | Sulfur 0.0003 | Saturates (%) 96.9 | KV@100C 4.08 | KV@40C 18.28' (ASTM D2007 for saturates)",
      unit='%', form='batch measurement of the neat base oil by a third party (Infineum sample ID LN04001024)', method='ASTM D2007', cond='neat base oil, one sample', basis='not stated (printed %)',
      outcome='additional', action='propose_open_question_update',
      reason="One Infineum sample analysis: it cannot fill saturates. Record it in an open question as batch evidence with the sample ID; the sample KV / VI are context only (typicals 4.1 / 19.0 / 126).",
      old_rev=f're-read manually: DL2-11332.pdf pp.1-2 read in full (old archive text layer) ({T})', cmp_override='existing: saturates Missing')
for pid, g, lot, sat, kv in (('S_OIL_ULTRA_S_4', '4', '12015322', '97.5', 'VI 124, KV100 4.27, KV40 19.76'), ('S_OIL_ULTRA_S_8', '8', '12015242', '96.53', 'VI 131, KV100 7.13, KV40 42.22')):
    b.row(p=pid, tier=3, path='saturates', old="DL2-11177.pdf (Ultra-S series sheet, typical properties) prints 'Saturates, wt% | D 2007 | >99 >99 >99 >99 >99'; record saturates '>99 wt%' (ASTM D2007).",
          new_f='DL2-11763.pdf', new_p=9, new_text=f"'Basestock Inspections' column 'Ultra S{g} | III | S Oil | Lot Number {lot}': Saturates, % {sat} (ASTM D2007); {kv}",
          unit='%', form=f'batch measurement of the neat base oil by a third party (lot {lot})', method='ASTM D2007', cond='neat base oil, one lot', basis='not stated (printed %)',
          outcome='not_comparable', action='propose_note',
          reason=(f"Comparability checked: same property and method (ASTM D2007), but a different value class (one Infineum lot vs S-OIL's typical bound '>99'); {sat} below '>99' is therefore NOT recorded as a "
                  "conflict and the typical is not questioned on one lot. Noted for the reviewer as batch evidence; no value changes."),
          old_rev=f're-read manually: DL2-11177.pdf p.1 (only page) read in full (text layer) ({T})', cmp_override="existing: saturates '>99 wt%'")

src = {n: json.load(open(f'{B}/decisions/{n}', encoding='utf-8'))['fields'] for n in (
    'zzzzzzzzzzzzzzzzzzz_b34_nondup_formulation_decks_1_nineteenth_pass.json', 'zzzzzzzzzzzzzzzzzzz_b38_nondup_afton_cdp_characterisations_nineteenth_pass.json')}
ovr = {(o['p'], o['path'], o['new_f']): o['new_text'] for o in json.load(open(f'{B}/decisions/zzzzzzzzzzzzzzzzzzz_b39_nondup_richful_afton_lubrizol_summaries_nineteenth_pass.json', encoding='utf-8')).get('field_overrides', [])}
def current(p, path, nf):
    if (p, path, nf) in ovr:
        return ovr[(p, path, nf)]
    hit = [r for rows in src.values() for r in rows if r['p'] == p and r['path'] == path and r['new_f'] == nf]
    assert len(hit) == 1, (p, path, nf, len(hit))
    return hit[0]['new_text']
F22 = 'HiTEC%2022300%20CDP_API%20SL%20AramcoPrima.pdf'
TAG = f'[Batch 40 ({T}): added Infineum sample / lot evidence from documents read in that batch; see new_source_printed.]'
def add(p, path, nf, more):
    b.overrides.append(dict(p=p, path=path, new_f=nf, new_text=current(p, path, nf) + '; ADDED in batch 40: ' + more, reason_append=TAG))
add('EXXONMOBIL_EHC_45', 'kv40', F22, "Infineum samples 09010520 'KV@40C 23.38', 09010605 '23.3' (DL2-11766.pdf p.19) and 14034439 'KV-40 22.69' (DL2-11768.pdf p.13), ASTM D445")
add('EXXONMOBIL_EHC_110', 'kv40', F22, "Infineum sample 11014321 'KV@40C 91.22' (DL2-11766.pdf p.19; the same sample in DL2-11768.pdf p.13), ASTM D445")
add('YUBASE_4', 'saturates', 'DL2-15799.pdf', "Infineum lots 13102339 98.5, 14011472 98.6, 16027383 98.0, LN12014855 98.1 (DL2-11763.pdf p.9) and samples LN09009384 98.1, LN11013660 97.72, LN15012069 98.2, LN11014322 97.9, LN16022692 99.4 (DL2-11762.pdf p.14), ASTM D2007")
add('YUBASE_6', 'saturates', F22, "Infineum sample 11013747 98.2 (DL2-11766.pdf p.19, producer 'Yukong'), lots 12015695 97.62, 16012596 98.2, LN11013747 98.15 (DL2-11763.pdf p.9), samples LN08008620 98.2, LN16013666 98.6, LN12015842 97.8 (DL2-11762.pdf p.14), ASTM D2007")
add('CHEVRON_GROUP_II_600R', 'saturates', 'DL2-15799.pdf', "Infineum sample LN12015818 'Chevron 600R' saturates 97.3 % (KV-40 102.85, KV-100 11.90, VI 105; DL2-11768.pdf p.13); the same sample is printed under '220R' (12015818, saturates 97.2) in DL2-11766.pdf p.19 (CDP M418): label inconsistency between the two Infineum documents")

b.visual += [
    dict(f='DL2-11766.pdf', page=19, checked="'Base Stock Analysis' tables", result='confirmed', detail="All columns as cited; the third '220R' column (sample 12015818) prints 11.91 / 103.05 (600R-like values)."),
    dict(f='DL2-11768.pdf', page=13, checked="'Base stock Information' tables", result='confirmed', detail="Columns as cited, including 'Chevron 600R | LN12015818' 102.85 / 11.90 / 105 / 0.001 / 97.3."),
    dict(f='DL2-11763.pdf', page=9, checked="'Basestock Inspections' table", result='confirmed', detail="Yubase, Ultra S4 / S8 columns as cited; the Motiva Star 4 / Star 6 columns are shifted in the source (KV100 0.001, saturates 20.4 / 41.8): not used."),
    dict(f='DL2-11762.pdf', page=14, checked="'Basestock Information' table", result='confirmed', detail='YUBASE 4 / 6 and SPECTRASYN4 columns as cited.'),
]
b.queue += [dict(name_as_printed=n, supplier='Infineum', file=f, page=pg, evidence=e) for n, f, pg, e in (
    ('Infineum D3494', 'DL2-11766.pdf', '1-31', 'CDP M418 API CJ-4 / SN candidate data package (February 2017), 13.200 mass %'),
    ('Infineum P5807', 'DL2-11763.pdf', '3-18', 'INF-CDP-730 API SN PLUS RC candidate package at 10.0 % with Paratone 50 SSI'),
    ('Infineum P6660', 'DL2-11762.pdf', '4-14', 'CDP-659 ACEA A3/B4-16 candidate data package (March 2018), 13.0-13.4 %'))]
b.write('zzzzzzzzzzzzzzzzzzz_b40_nondup_infineum_afton_basestock_inspections_nineteenth_pass.json')
