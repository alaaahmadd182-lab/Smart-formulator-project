"""Supplier batch S20: Chevron Phillips Chemical (Synfluid PAO / mPAO; 33 documents).
Read: compact listing; product links of every document checked against the existing-comparison ledger
(existing_product_comparison_2026-11-12), which already assessed these documents for the existing CHEVRON_SYNFLUID_* records.
Rules: one linked record -> 'subject'; several -> 'series / multi-grade sheet (grade listed)'. DL2 'C12 Based PAOs' table (sha
7c4871c0a1: C12 Dimer, 2.5 / 5 / 7 / 9 cSt) has no ledger link: multi-product, grades printed by viscosity only - NOT mapped to
existing records by viscosity (identity is never inferred from values). Identity only. Writes decisions/s20_cpchem.json."""
import csv, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = {r['sha256']: r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Chevron Phillips')}
REG = {d['sha256']: d for d in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_register.csv'), encoding='utf-8')) if d['sha256'] in A}
SUP = 'Chevron Phillips Chemical Company LP'
D = {}
for sha, a in A.items():
    prods = [p.strip() for p in REG[sha]['existing_comparison_products'].split('|') if p.strip()]
    t = a['top_lines']
    if sha.startswith('7c4871c0a1'):
        D[sha[:12]] = dict(doc_type='product table (multi-product)', supplier=SUP, products=[], roles={}, relation='product', read='page-1 listing',
                           note="'C12 Based PAOs' table: C12 Dimer, 2.5 / 5 / 7 / 9 cSt (grades named by viscosity only; not mapped to records by value)", next_action='list the products inside (multi-product)')
        continue
    keys = ['EXISTING:' + p for p in prods]
    typ = 'SDS' if 'SAFETY DATA SHEET' in t else ('sales specification' if 'Sales Specification' in t else ('presentation' if a['pages'] and int(a['pages']) > 20 and 'SAFETY' not in t else 'product data sheet (TDS/PDS)'))
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=keys, roles={k: ('subject' if len(keys) == 1 else 'series / multi-grade sheet (grade listed)') for k in keys},
                       relation='product', read='page-1 listing; existing-comparison ledger links', note='links as in the existing-comparison ledger', next_action='')
out = dict(batch='S20 Chevron Phillips Chemical (identity)', reviewed_on='2026-11-14', scope='33 documents with provisional supplier Chevron Phillips Chemical', products={}, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's20_cpchem.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', Counter(v['doc_type'] for v in D.values()), len({k for v in D.values() for k in v['products']}), 'existing records linked')
