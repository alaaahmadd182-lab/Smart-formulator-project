"""Nineteenth pass, batch 37: visual verification and route-evidence revision of batches 34-36 (no new link reviewed).

What changed, kept apart from new reading:
  1. NEW READING (visual): page images of the table pages behind batch 34-36 rows (DL2-15799 pp.20, 21, 23; DL2-15608
     pp.5, 9; DL2-12485 p.12) and of every name-hit page that carries a sizeable embedded image (DL2-12999 pp.6, 8;
     DL2-15564 / DL2-15332 pp.13, 14, 26, 27, 29, 30; DL2-13364 pp.3-5, 10, 11; DL2-13089 pp.7-9; DL2-13296 p.6;
     DL2-12906 p.1; DL2-12485 pp.5, 21; DL2-12486 pp.12, 30; DL2-15608 pp.3, 7) were viewed; claim-dot matrices of
     DL2-13364 pp.10-11 and the CVT graphic of DL2-15608 p.3 read at 200-220 dpi. The OLOA 55603 pptx was re-read from its
     slide XML (8 slides: text frames and table cells by row) with slide 2's images viewed; no slide renderer is
     available, so slides were not viewed as rendered images.
  2. WORDING / CLASSIFICATION (no new reading): every batch 34-36 link's coverage now states that 'not applicable' is
     limited to neat base-oil properties, names the packages the document is formulation / route evidence for and where
     that evidence stands, and that absence on the pages read is not proof of absence in the document.
  3. Packages without a record are added to the new-product candidate queue (route evidence preserved, nothing captured).
Reads the batch 34-36 decision files and writes
decisions/zzzzzzzzzzzzzzzzzzz_b37_visual_and_route_revision_nineteenth_pass.json (sorted after them, so its links replace
theirs)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nd_common import B, T, to_root
to_root()

SRC = ['zzzzzzzzzzzzzzzzzzz_b34_nondup_formulation_decks_1_nineteenth_pass.json',
       'zzzzzzzzzzzzzzzzzzz_b35_nondup_formulation_decks_2_nineteenth_pass.json',
       'zzzzzzzzzzzzzzzzzzz_b36_nondup_formulation_decks_3_nineteenth_pass.json']
PPTX = 'OLOA%2055603%20ILSAC%20GF-7%20and%20Gen%203%20MG%20Customer%20Deck%20-%20AMR%20APR%20EAME%20Jul26%20.pptx'
Q = 'no package record; added to the new-product candidate queue in this batch'

ROUTE = {
    'DL2-12999.pdf': f'Infineum T4294, T4714, T4920, T4535, T4579, T4537, T4580, S1875, S956 and M8220 ({Q}); p.6 also states that Ultra S, PetroCanada base oils or PAOs are suitable for T4294',
    'DL2-13852.pdf': f'Oronite OLOA 54100, 54120, 54050, 54000 / 54000B, 54013 and 58833 ({Q})',
    'DL2-12412.pdf': f'Oronite OLOA 54000 / 54000B, 54050, 54013 and 58833 ({Q})',
    'DL2-12906.pdf': f'Oronite OLOA 61105, 61106, 61005, 61107, 59094, 59211, 59110, 59770, 54050, 55501 and 59940 ({Q}); p.12 note c names the approved Group III base oils for OLOA 55501 (SK and S-Oil)',
    'DL2-15799.pdf': 'Afton HiTEC 11455 (no package record; already in the candidate queue) and HiTEC 5748 (record exists; its link on this document was reviewed in the sixteenth pass)',
    'DL2-15608.pdf': f"Afton HiTEC 34006 ({Q}); each page's CVT claims graphic is not in the text layer (p.3 read as an image in this batch)",
    'DL2-13364.pdf': 'Afton HiTEC 9490 (no package record; already in the candidate queue), HiTEC 12200, 12204L, 12250, 8788B and 5748 (records exist; their links on this document are reviewed separately; the claim dots of pp.10-11 were read as images in this batch)',
    'DL2-13089.pdf': f'Infineum T4294 ({Q})',
    'DL2-13296.pdf': f'Afton HiTEC 3460 with HiTEC 5739 ({Q})',
    PPTX: f'Oronite OLOA 55603 / 55600 ({Q}): base-oil coverage tables (slides 5, 6), base-oil interchange ranges (slide 8), claims (slides 3, 4, 7)',
    'DL2-12610.pdf': 'Lubrizol CV1100 (record exists; its p.4 column 14 was read as an image in an earlier pass)',
    'DL2-15564.pdf': 'Infineum D3416 and D3417 (records exist; their links reviewed in earlier passes) and D3418 (no record; already in the candidate queue)',
    'DL2-15332.pdf': 'Infineum D3416 and D3417 (records exist; their links reviewed in earlier passes) and D3418 (no record; already in the candidate queue)',
    'DL2-12485.pdf': "Afton HiTEC 12210M (record exists; its 31 formulations are proposed; the per-formulation claim-dot matrices on every page are NOT in the text layer and have NOT been read: outstanding visual check registered on DL2-12486.pdf, pixel-identical)",
    'DL2-12486.pdf': "Afton HiTEC 12210M (record exists; its 31 formulations are proposed; the per-formulation claim-dot matrices on every page are NOT in the text layer and have NOT been read: outstanding visual check registered on this file)",
}
VIEWED = {
    'DL2-12999.pdf': 'pp.6 and 8 also viewed as page images (embedded images; p.6 shows a column layout that the text layer does not preserve)',
    'DL2-15564.pdf': 'pp.13, 14, 26, 27, 29 and 30 also viewed as page images',
    'DL2-15332.pdf': 'pp.13, 14, 26, 27, 29 and 30 also viewed as page images',
    'DL2-13364.pdf': 'pp.3, 4, 5, 10 and 11 also viewed as page images (pp.10-11 claim dots at 220 dpi)',
    'DL2-13089.pdf': 'pp.7, 8 and 9 also viewed as page images',
    'DL2-13296.pdf': 'p.6 also viewed as a page image',
    'DL2-12906.pdf': 'p.1 (cover photograph) also viewed as a page image',
    'DL2-15799.pdf': 'pp.20, 21 and 23 also viewed as page images (lot table and component densities confirmed)',
    'DL2-15608.pdf': 'pp.3, 5, 7 and 9 also viewed as page images (labels confirmed; p.3 CVT graphic at 200 dpi)',
    'DL2-12485.pdf': 'pp.5, 12 and 21 also viewed as page images (p.12 label confirmed; claim-dot matrices not read)',
    'DL2-12486.pdf': 'pp.12 and 30 also viewed as page images (claim-dot matrices not read)',
}
PPTX_SCOPE = ("slide XML of all 8 slides read in full (text frames and table cells row by row; recipe tables on slides 5 and 6, base-oil interchange ranges on slide 8); "
              "slide 2 images viewed (world map, Chevron Oronite logo, dexos1 Gen 3 logo; one JPEG XR image not viewable); slides not viewed as rendered images (no renderer available)")
PPTX_COV = {
    'BAPCO_BAPBASE_4': "slide 5, column group 'Bapbase' (OR-F 93511M-A 0W-20 and 91394Q-A 5W-30): 'BAPBase 4' 61.12 / 52.63 wt% with BAPBase 8 and GTL4 trim fluid",
    'BAPCO_BAPBASE_8': "slide 5, column group 'Bapbase': 'BAPBase 8' 4.19 / 29.6 wt%",
    'CHEVRON_GROUP_II_100R': "slide 5, column group 'NEXBASE', OR-F 85742Q-A 5W-30: 'Chevron 100R' 8.17 wt% with Chevron 220R 30.24 and NEXBASE 3043R 43.32",
    'CHEVRON_GROUP_II_220R': "slide 5, column group 'NEXBASE', OR-F 85742Q-A 5W-30: 'Chevron 220R' 30.24 wt%",
    'NESTE_NEXBASE_3080': "slide 5: 'NEXBASE 3080' 3.31 / 5.74 wt% (group 'NEXBASE/CPChem PAO', OR-F 87372M-A, 87106M-A) and 20.38 wt% (group 'NEXBASE', 84516Q-A); the companion 'NEXBASE 3043R' is a different name from NEXBASE 3043 and is not linked",
    'PETRO_CANADA_PURITY_VHVI_4': "slide 6, column group 'PetroCanada': 'Purity VHVI-4 (Gp3), wt%' 62.93 / 83.58 (Oronite's '(Gp3)' label, third-party)",
    'PETRO_CANADA_PURITY_VHVI_8': "slide 6, column group 'PetroCanada': 'Purity VHVI-8 (Gp3), wt %' 18.80 (Oronite's '(Gp3)' label, third-party)",
}
NOT_PROOF = 'absence of a neat property on the pages read is not proof that the document contains none'

links, docs = [], {}
for s in SRC:
    d = json.load(open(f'{B}/decisions/{s}', encoding='utf-8'))
    for f, v in d['documents'].items():
        v = dict(v)
        if f == PPTX:
            v.update(read=PPTX_SCOPE, limits='slide XML read; slide images not rendered')
        elif f in VIEWED:
            v['read'] += '; ' + VIEWED[f]
        v['route_evidence_for'] = ROUTE[f]
        docs[f] = v
    for l in d['links']:
        l = dict(l)
        f, cov = l['f'], l['coverage']
        if f == PPTX:
            l['fields_status'] = f'{PPTX_SCOPE} ({T}; slide-numbered re-read in batch 37)'
            cov = (f"not applicable: another product's document (Oronite OLOA 55603 dexos1 Gen 3 / ILSAC GF-7 deck, July 2026); {PPTX_COV[l['p']]}; "
                   "recipe share only, no property of the neat base oil is printed in the slide text or tables read")
        elif f in VIEWED:
            l['fields_status'] = l['fields_status'].replace(f' ({T})', f'; {VIEWED[f]} ({T}; images viewed in batch 37)')
        if cov.startswith('not applicable'):
            rest = cov[len('not applicable'):].lstrip(' :')
            if rest.startswith('for property values:'):
                rest = rest[len('for property values:'):].strip()
            cov = (f'not applicable to neat base-oil properties only (limited meaning): {rest}. The document remains formulation / route evidence '
                   f'(recipes using this base oil, package claims, co-component doses) for {ROUTE[f]}; that evidence is not assessed by this link; {NOT_PROOF}')
        else:
            cov = (f'{cov} Limited meaning: assessed for neat base-oil properties on the pages read only; the document remains formulation / route evidence for {ROUTE[f]}; {NOT_PROOF}')
        l['coverage'] = cov
        l['note'] = l['note'] + ' Batch 37: coverage wording limited to neat base-oil properties and route evidence named; images viewed where stated (no change of the reading of the text).'
        links.append(l)

visual = [
    dict(f='DL2-15799.pdf', page=20, checked="'Program Base Stock Characterization' table (column alignment behind the batch 34 rows)", result='confirmed',
         detail="Rows read on the image: 'Yubase 4 | R20-12589 | III | 4.150 | 19.320 | 122 | 98.3 | 0.0000'; 'ADbase 4 | R20-7853 | III | 4.322 | 19.71 | 129 | 96.8 | 0.0002'; 'ADbase 6 | R19-5555 | III | 6.008 | 31.72 | 138 | 95.5 | 0.0000'; "
                "'Chevron 600R | RIC23-04540 | II | 12.010 | 102.100 | 108 | 97.6 | 0.0002' and '| RIC24-08339 | II | 12.030 | 102.300 | 108 | 97.2 | 0.0002', as recorded."),
    dict(f='DL2-15799.pdf', page=21, checked="'Final Formulations' component table", result='confirmed',
         detail="'Yubase 4' 0.834 under the column 'Typical Density' (no unit, no temperature), 87.15 % wt. / 88.26 % vol.; Yubase 4 is the only base oil of LBT-032205-A; 'Base Oil Properties' 99.2 / 0.000 / 4.225 / 126."),
    dict(f='DL2-15799.pdf', page=23, checked="'Final Formulations' component table", result='confirmed', detail="'ADbase 4' 0.831 and 'ADbase 6' 0.837 under 'Typical Density' (no unit, no temperature)."),
    dict(f='DL2-15608.pdf', page='5, 9', checked="formulation tables with Afton's base-oil labels", result='confirmed',
         detail="p.5 'Ultra S3 | API Group III | 54.4', 'Ultra S6 | API Group III | 34.0'; p.9 'Nexbase 3030 | API Group III | 41.2', 'Nexbase 3060 | API Group III | 47.2', as cited."),
    dict(f='DL2-15608.pdf', page=3, checked='CVT claims graphic (not in the text layer), 200 dpi crop', result='confirmed',
         detail="Columns 'CVT Belt and Chain', 'Toyota FE', 'Nissan NS3' beside 'CVT HiTEC® 34006 @ 11.6%': a light-blue marker in each; Toyota FE and Nissan NS3 markers carry '2'. Legend: 'Specification Status 1. Formal Approval 2. Self Certifying 3. Obsolete'; "
                "'Product Status' black = Approvable, grey = Meets Requirements, light blue = Suitable. Read by marker colour (an interpretation of the colour, not printed text). HiTEC 34006 has no record."),
    dict(f='DL2-12485.pdf', page=12, checked='formulation table LBR-018154-B', result='confirmed',
         detail="'Ultra-S 4 | API Group III | 10.0' as cited. The claim-dot matrix below the table is graphical and was NOT read; the slide title glyphs render as boxes."),
    dict(f='DL2-13364.pdf', page=10, checked='HiTEC 12200 LBB-018043-A claim-dot matrix (220 dpi crop)', result='confirmed',
         detail="'API SL SAE 10W-40 HiTEC® 12200 @ 10.8%': dots under API SL, API SJ, ACEA A3/B4-16, MB 228.3, MB 229.1, MAN 3275, MTU 2.0, JASO DH-1 (23 rotated column labels API CI-4 Plus ... DDC 93K215; column assignment by position). Not proposed in this batch; route evidence for the HiTEC 12200 record."),
    dict(f='DL2-13364.pdf', page=11, checked='HiTEC 12200 LBB-019625-A claim-dot matrix (220 dpi crop)', result='confirmed',
         detail="'API CI-4/SL SAE 10W-40 HiTEC® 12200 @ 10.8% & HiTEC® 12260 @ 0.9%': dots in every column except API CI-4 Plus, MB 228.1 and MB 229.1 (column assignment by position). Not proposed in this batch; route evidence for the HiTEC 12200 record."),
    dict(f='DL2-12999.pdf', page=6, checked='T4294 example formulations (embedded image page)', result='confirmed',
         detail="The image shows three blocks (Low, High, Mid) whose column pairing differs from the text-layer order: e.g. Low: 3030 51.0 + 3080 37.0 | 3043 80.0 + 3080 8.0 | 3043 88.0. Only the recipe-share role was used; no column value was taken from the text layer."),
]
pending = [dict(f='DL2-12486.pdf', page='2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32',
                why=("HiTEC 12210M per-formulation claim-dot matrices (graphical; not in the text layer) on every formulation page; not read. Same pixels as DL2-12485.pdf (earlier check), whose "
                     "'all' visual confirmation covers pixel identity and formulation totals only, not these claims."))]

QUEUE = [
    ('Infineum T4294', 'Infineum', 'DL2-12999.pdf', '6', 'ATF example formulations at 12.0 % (01/01/2019); also DL2-13089.pdf pp.7-9 (© 2019)'),
    ('Infineum T4714', 'Infineum', 'DL2-12999.pdf', '8', 'multi-vehicle ATF formulations at 20.0 %'),
    ('Infineum T4920', 'Infineum', 'DL2-12999.pdf', '9', 'CVT DI package 8.0 % with Infineum T4163 6.0 %, OEM CVT list'),
    ('Infineum T4535', 'Infineum', 'DL2-12999.pdf', '10', 'HD extended-drain ATF 16.0 %w, ZF / Voith / MAN / MB claims'),
    ('Infineum T4579', 'Infineum', 'DL2-12999.pdf', '11', 'HD ATF DI 10.2 %w with PAO 4 40 %w'),
    ('Infineum T4537', 'Infineum', 'DL2-12999.pdf', '13-14', 'main-tier ATF 11.2 %, D-IID / D-IIIG / D-IIIH formulations and claims'),
    ('Infineum T4580', 'Infineum', 'DL2-12999.pdf', '16', 'main / low-tier ATF 8.4 %, Dexron III-H / II-D formulations'),
    ('Infineum S1875', 'Infineum', 'DL2-12999.pdf', '23', 'motorcycle 4.0 % with Infineum SV261 / V385, JASO MA / MA2 claims'),
    ('Infineum S956', 'Infineum', 'DL2-12999.pdf', '26', 'four-stroke outboard 9.0 %, NMMA FC-W certification numbers'),
    ('Infineum M8220', 'Infineum', 'DL2-12999.pdf', '41', 'gas engine oil 12.5 %, Jenbacher series 6H approval'),
    ('OLOA 54100', 'Chevron Oronite', 'DL2-13852.pdf', '9', 'ACEA A3/B4-16 finished-oil formulations at 13.50 %'),
    ('OLOA 54120', 'Chevron Oronite', 'DL2-13852.pdf', '11', 'ACEA A3/B4-16 formulations at 15.1 %'),
    ('OLOA 54050', 'Chevron Oronite', 'DL2-13852.pdf', '17-23', 'formulations and claims at 11.30 % / 10.80 %; also DL2-12412.pdf pp.35-49 and DL2-12906.pdf p.11'),
    ('OLOA 54000 / OLOA 54000B', 'Chevron Oronite', 'DL2-13852.pdf', '30-36', 'formulations at 12-13 % (+ OLOA 249SX), equivalency letter 54000B; also DL2-12412.pdf pp.10-30'),
    ('OLOA 54013', 'Chevron Oronite', 'DL2-13852.pdf', '42-45', 'formulations at 9.9 % (+ OLOA 249SX / OLOA 58833); also DL2-12412.pdf pp.13, 54-57'),
    ('OLOA 58833', 'Chevron Oronite', 'DL2-13852.pdf', '44', 'component used at 3.33 % with OLOA 54013 (full 5W-40 profile)'),
    ('OLOA 61105', 'Chevron Oronite', 'DL2-12906.pdf', '2, 6', 'low SAPS HDMO base package 19.0 %, CK-4 / FA-4 formulations (December 2019 APAC summary)'),
    ('OLOA 61106', 'Chevron Oronite', 'DL2-12906.pdf', '3', 'high-TBN HDMO package 19.6 %'),
    ('OLOA 61005', 'Chevron Oronite', 'DL2-12906.pdf', '4', 'UHPD package 12.60 %, European type qualifications'),
    ('OLOA 61107', 'Chevron Oronite', 'DL2-12906.pdf', '5', 'mid SAPS HDMO package 19.3 %'),
    ('OLOA 59094', 'Chevron Oronite', 'DL2-12906.pdf', '7', 'SHPD package 14.69 %'),
    ('OLOA 59211', 'Chevron Oronite', 'DL2-12906.pdf', '8', 'HDMO package 11.95 % (+ OLOA 65751 booster 0.95 %)'),
    ('OLOA 59110', 'Chevron Oronite', 'DL2-12906.pdf', '9', 'HDMO package 14.90 %'),
    ('OLOA 59770', 'Chevron Oronite', 'DL2-12906.pdf', '10', 'SHPD package 12.9 %'),
    ('OLOA 55501', 'Chevron Oronite', 'DL2-12906.pdf', '12', 'PCMO top-tier package 7.56 %; note c: approved Group III base oils SK and S-Oil'),
    ('OLOA 59940', 'Chevron Oronite', 'DL2-12906.pdf', '13', 'PCMO main-tier package 7.58 % (SJ 6.82 %, SG 6.14 %)'),
    ('OLOA 55603', 'Chevron Oronite', PPTX, 'slides 3-8', 'dexos1 Gen 3 / ILSAC GF-7 package 9.77 wt% (PPD-embedded 8.30 wt%; = OLOA 55600 @ 7.9 wt%), base-oil coverage tables slides 5-6, interchange ranges slide 8 (July 2026)'),
    ('HiTEC 34006', 'Afton', 'DL2-15608.pdf', '3-9', 'CVT package 11.6 % in Group III base oils, CVT claims graphic (2024)'),
    ('HiTEC 3460', 'Afton', 'DL2-13296.pdf', '6', 'DCTF additive 12.8 % weight with HiTEC 5739 4.50 (2018)'),
]
d = dict(batch='batch 37: visual verification and route-evidence wording for batches 34-36 (nineteenth pass)', reviewed_on='2026-11-14 (nineteenth pass)',
         note='No new link reviewed: images viewed for batch 34-36 pages, pptx re-read by slide, coverage wording limited to neat base-oil properties, packages queued.',
         documents=docs, links=links, fields=[], visual=visual, not_yet_verified_visually=pending,
         new_product_candidates=[dict(name_as_printed=n, supplier=s, file=f, page=p, evidence=e) for n, s, f, p, e in QUEUE])
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzzzz_b37_visual_and_route_revision_nineteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(visual), len(pending), len(QUEUE))
