"""Supplier batch S18: Eni (Eni S.p.A. additives 'Eni MX', and Versalis 'Dutral'; 37 documents with provisional supplier 'Eni').
Read: compact listing; every 'Eni MX nnnn' code on page 1 with the descriptor following the first one.
Rules: subject = the Eni MX code printed in the title (first code in the top lines, else the first on page 1); other MX codes on
the same page are linked with role 'mentioned (other grade named on page 1)' and become products of their own (class unresolved
when only mentioned). 'Eni Triple Tech' brochure is multi-product (grades it names linked as 'mentioned'). Versalis 'DUTRAL EP(D)M'
range sheet is multi-product; 'Dutral OCP 2550' (name from the TDS file name 'TDS Dutral OCP 2550 2107' and the EP(D)M sheet) is a
component (VM use not printed on page 1). Existing records: ENI_MX_5212, ENI_MX_5217.
Identity only. Writes decisions/s18_eni.json."""
import csv, json, os, re, importlib.util
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location('ident', os.path.join(os.path.dirname(HERE), '02_identify.py'))
ident = importlib.util.module_from_spec(spec); spec.loader.exec_module(ident)
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'] == 'Eni']
SUP = 'Eni S.p.A.'
EXIST = {'ENI MX 5212': 'ENI_MX_5212', 'ENI MX 5217': 'ENI_MX_5217'}
CODE = re.compile(r'Eni MX \d{4}[A-Z]?')
D, PK, DESC = {}, {}, {}
for r in A:
    sha, p10 = r['sha256'], r['sha256'][:10]
    pg, _ = ident.pages_for(sha)
    t = re.sub(r'\s+', ' ', pg[0] if pg else '')
    if p10 == 'a93468cdb7':
        D[sha[:12]] = dict(doc_type='product range sheet (multi-product)', supplier='Versalis (Eni)', products=[], roles={}, relation='product', read='page-1 listing',
                           note="Versalis 'DUTRAL EP(D)M' main-properties range sheet", next_action='list the products inside (multi-product)')
        continue
    if p10 == 'bc18ca1da1':
        k = 'VERSALIS:DUTRAL OCP 2550'
        D[sha[:12]] = dict(doc_type='product data sheet (TDS/PDS)', supplier='Versalis (Eni)', products=[k], roles={k: 'subject'}, relation='product', read='page-1 listing; file name',
                           note="name from the file name 'TDS Dutral OCP 2550 2107' and the 'DUTRAL EP(D)M' header", next_action='confirm the grade name on the page image')
        PK[k] = dict(name='Dutral OCP 2550', supplier='Versalis (Eni)', material_class='additive_component', existing_record='', status='new_candidate',
                     notes='ethylene-propylene copolymer (EP(D)M header); VM use not printed on page 1', identity_evidence='file name + page header', template='additive_component general (VM subtype to confirm)')
        continue
    codes = list(dict.fromkeys(CODE.findall(t)))
    top = CODE.findall(r['top_lines'])
    multi = p10 == '6431b25a4a'
    subj = None if multi else (top[0] if top else codes[0])
    keys, roles = [], {}
    for c in ([subj] if subj else []) + [c for c in codes if c != subj]:
        k = 'ENI:' + c.upper()
        keys.append(k)
        roles[k] = 'subject' if c == subj else 'mentioned (other grade named on page 1)'
    if subj:
        m = re.search(re.escape(subj) + r'\s+(?:is an? |additives? package is |additive package is )?(.{0,80})', t)
        d0 = re.split(r'\s(?:Eni\.spa|\d{2}/2017|Via Laurentina|Safety Data Sheet)', m.group(1))[0] if m else ''
        if 'Safety Data Sheet' not in t[:300] or subj.upper() not in DESC:
            DESC[subj.upper()] = d0 if 'Safety Data Sheet' not in t[:300] else ''
    typ = 'SDS' if 'Safety Data Sheet' in t[:300] else ('brochure (multi-product)' if multi else 'product data sheet (TDS/PDS)')
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=keys, roles=roles, relation='product', read='page-1 text (MX codes and descriptor)',
                       note="'Eni Triple Tech - Multipurpose Additives Packages Technology' brochure" if multi else '', next_action='list the products inside (multi-product)' if multi else '')
for k in dict.fromkeys(p for v in D.values() for p in v['products'] if p.startswith('ENI:')):
    c = k[4:]
    d = DESC.get(c)
    if d is None:
        mc, n = 'unresolved', 'named only on other grades\' sheets / the Triple Tech brochure (class not printed for this grade)'
    elif re.search(r'(?i)package', d):
        mc, n = 'additive_package', d
    elif re.search(r'(?i)Olefin Copolymer|Viscosity Index', d):
        mc, n = 'additive_component', d + ' (VM subtype)'
    elif re.search(r'(?i)Pour Point', d):
        mc, n = 'additive_component', d + ' (PPD subtype)'
    else:
        mc, n = 'additive_component', d
    PK[k] = dict(name=c.replace('ENI', 'Eni'), supplier=SUP, material_class=mc, existing_record=EXIST.get(c, ''), status='existing' if c in EXIST else 'new_candidate',
                 notes=('printed: ' + n) if d is not None else n, identity_evidence='printed product code on the documents linked in this batch',
                 template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ subtype as noted)'}.get(mc, 'not determined'))
PK['ENI:ENI MX 4016']['notes'] = "printed once on the Eni MX 4106 sheet (sha 318f8bc615); may be a separate grade or a misprint of 4106 - not resolved"
out = dict(batch='S18 Eni / Versalis (identity)', reviewed_on='2026-11-14', scope='37 documents with provisional supplier Eni', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's18_eni.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(p['material_class'] for p in PK.values()), Counter(p['status'] for p in PK.values()))
for k, v in sorted(PK.items()): print(k.ljust(24), v['material_class'].ljust(18), v['notes'][:70])
