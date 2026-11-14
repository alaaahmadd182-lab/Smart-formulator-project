"""Supplier batch S21: Jinzhou Mingyue Keji (锦州名悦科技有限公司, 'MINGYUEKEJI'; 30 documents).
Read: compact listing; longer cards for DL2-15087 and the T154A certificate. The 6 certificates have a garbled (font-mapped)
Chinese text layer; the Latin product codes are legible ('T115B(TBN 250)', 'T154A', 'T161', 'T202', 'T204', 'T106A(TBN 300)').
Rules: subject = printed code. Certificates print codes WITHOUT the 'MY-' prefix used on the TDS / SDS (e.g. 'T106A(TBN 300)' vs
'MY-T106A (TBN300)'): they are kept as separate product keys with a note 'probably the same grade (prefix absent) - not merged;
confirm' (the match would rest on the name pattern only; values are not used). Classes from the printed descriptor; 'MY-T2007A'
(PIBSA) is a component / process intermediate (schema gap); MY-P3065 'Additive Package For Car & Motorcycle Oil' is a package.
Identity only. Writes decisions/s21_mingyue.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Mingyue')]
SUP = 'Jinzhou Mingyue Keji Co., Ltd.'
COA = {'43eb3aa1be': ('T115B', "printed 'T115B(TBN 250)'"), '0594f234eb': ('T154A', ''), 'fe5013d3c3': ('T161', ''), 'e6e4bef768': ('T202', ''),
       'b136ac2322': ('T204', ''), 'db689f6610': ('T106A', "printed 'T106A(TBN 300}'")}
D, PK = {}, {}
for r in A:
    sha, p10 = r['sha256'], r['sha256'][:10]
    t = r['top_lines'].replace('\n', ' | ')
    if p10 in COA:
        code, n = COA[p10]
        desc, typ = '', 'certificate of analysis (batch)'
        note = (n + '; ' if n else '') + 'garbled Chinese text layer; Latin code legible'
    elif p10 == '241204262a':
        code, desc, typ, note = 'MY-P3065', 'Additive Package For Car & Motorcycle Oil', 'product data sheet (TDS/PDS)', ''
    else:
        m = re.search(r'(MY-[A-Z]\d{3,4}[A-Z]?)\s*(?:\(TBN\s?\d+\))?\s*(.{0,80}?)\s*(?:\||DESCRIPTION|SAFETY)', t)
        code, desc = m.group(1), m.group(2).strip(' |')
        if code == 'MY-T168M':  # glued title 'MY-T168Multi-fonction ...'
            code, desc = 'MY-T168', 'M' + desc
        typ = 'SDS' if 'SAFETY DATA SHEET' in t else 'product data sheet (TDS/PDS)'
        note = ''
    k = 'MINGYUE:' + code
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=[k], roles={k: 'subject'}, relation='product', read='page-1 listing' + ('; longer card' if p10 in ('241204262a', '0594f234eb') else ''),
                       note=note, next_action='')
    if k not in PK or (desc and not PK[k]['notes'].startswith('printed')):
        if code.startswith('MY-P') or re.search(r'(?i)package', desc): mc, n2 = 'additive_package', desc
        elif 'MY-T2007A' == code: mc, n2 = 'additive_component', 'PIBSA (process intermediate: schema gap)'
        elif desc: mc, n2 = 'additive_component', desc
        else: mc, n2 = 'unresolved', ''
        PK[k] = dict(name=code, supplier=SUP, material_class=mc, existing_record='', status='new_candidate', notes=('printed: ' + n2) if n2 else 'certificate only; descriptor not printed',
                     identity_evidence='printed product code on the documents linked in this batch',
                     template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general'}.get(mc, 'not determined'))
for code, _ in COA.values():
    if 'MINGYUE:MY-' + code in PK:
        PK['MINGYUE:' + code]['notes'] += f"; probably the same grade as MY-{code} (prefix 'MY-' absent on the certificate) - not merged; confirm"
out = dict(batch='S21 Mingyue (identity)', reviewed_on='2026-11-14', scope='30 documents with provisional supplier Mingyue', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's21_mingyue.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(p['material_class'] for p in PK.values()))
for k, v in sorted(PK.items()): print(k.ljust(22), v['material_class'].ljust(18), v['notes'][:80])
