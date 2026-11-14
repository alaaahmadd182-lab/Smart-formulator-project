"""Supplier batch S17: Jinzhou KangTai Lubricant Additives (40 documents with provisional supplier 'KangTai').
Read: compact page-1 listing: every product sheet prints 'KangTai . Lubricant Addtives | WWW.JZKANGTAI.COM | <code> | <descriptor>'.
Rules: subject = printed code; keys drop internal spaces so that the same code printed with and without a space is one product
('KT D1354' here = 'KTD1354' on the S13 bulletin DL2-15761; 'BD C010' -> BDC010); the printed spelling is kept as the name.
'KT D1354', 'KT D1354B', 'KT D1354E' and 'KT33070' / 'KT33070A', 'KT33303' / 'KT33303A', 'KT33160A' are separate products.
'J-0010' (ethylene-propylene copolymer, solid) is printed by KangTai; the same code appears under PetroChina Jilin in earlier
batches (LUBRIZOL:JILIN J0010) - NOT merged here: cross-supplier consolidation question.
Classes from the printed descriptor ('... ADDITIVE PACKAGE' / 'ENGINE OIL ADDITIVE' -> package; chemistry names -> component; KR
1300 PIBSA -> component, process intermediate (schema gap)). Existing record: JINZHOU_KANGTAI_KT31140.
Identity only. Writes decisions/s17_kangtai.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('KangTai')]
SUP = 'Jinzhou KangTai Lubricant Additives Co., Ltd.'
EXIST = {'KT31140': 'JINZHOU_KANGTAI_KT31140'}
D, PK = {}, {}
for r in A:
    sha = r['sha256']
    f = [x.strip() for x in re.split(r'\n|\s\|\s', r['top_lines'])]
    if sha.startswith('15e9e889cd'):
        D[sha[:12]] = dict(doc_type='company catalogue (multi-product)', supplier=SUP, products=[], roles={}, relation='product', read='page-1 listing',
                           note="'Additive Expert KANGTAI' catalogue (31 pp)", next_action='list the products inside (multi-product)')
        continue
    i = f.index('WWW.JZKANGTAI.COM')
    printed, desc = f[i + 1], f[i + 2]
    code = printed.replace(' ', '').upper()
    key = 'KANGTAI:' + code
    D[sha[:12]] = dict(doc_type='product data sheet (TDS/PDS)', supplier=SUP, products=[key], roles={key: 'subject'}, relation='product', read='page-1 listing (code + printed descriptor)',
                       note=f"printed code '{printed}'", next_action='')
    if re.search(r'PACKAGE|ENGINE OIL ADDITIVE', desc):
        mc, n = 'additive_package', desc
    elif 'SUCCINIC ANHYDRIDE' in desc:
        mc, n = 'additive_component', desc + ' (process intermediate: schema gap)'
    elif re.search(r'COPOLYMER|Viscosity Index', desc, re.I):
        mc, n = 'additive_component', desc + ' (VM subtype)'
    else:
        mc, n = 'additive_component', desc
    if code == 'J-0010':
        n += "; same code as PetroChina Jilin J0010 linked in an earlier batch (LUBRIZOL:JILIN J0010): not merged, consolidation question"
    PK[key] = dict(name=printed, supplier=SUP, material_class=mc, existing_record=EXIST.get(code, ''), status='existing' if code in EXIST else 'new_candidate',
                   notes='printed: ' + n, identity_evidence='printed code on the documents linked in this batch',
                   template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ subtype as noted)'}[mc])
out = dict(batch='S17 KangTai (identity)', reviewed_on='2026-11-14', scope='40 documents with provisional supplier KangTai', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's17_kangtai.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(p['material_class'] for p in PK.values()), Counter(p['status'] for p in PK.values()))
print(sorted(PK))
