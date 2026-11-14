"""Build the dataset-preparation registers from the archive inventory, the automated identities (02_identify.py), the
existing-product comparison ledger and the reviewed identity decisions (decisions/*.json, applied in sorted order).

Outputs (tables/):
  file_register.csv            every archive file (4,422) -> canonical unique document (SHA-256), duplicate role
  document_register.csv        every unique document (4,186): type, supplier, products, relation, identity status, review
                               status, limitations and next action (one row per document)
  document_product_links.csv   one row per (document, product) with role and evidence
  product_register.csv         one row per product (existing record or new / unresolved candidate) with documents and status
  supplier_register.csv        per supplier: aliases seen, existing records, documents, products, review coverage
  register_summary.json        counts used by the checkpoints
Decision file format (decisions/<name>.json):
  {"batch": str, "reviewed_on": str, "scope": str,
   "products": {KEY: {"name", "supplier", "material_class", "existing_record" (product_id or ''), "status"
                      ('existing' | 'new_confirmed' | 'new_candidate' | 'unresolved'), "identity_evidence", "template", "notes"}},
   "documents": {sha256-prefix (>=10 chars): {"doc_type", "supplier", "products": [KEY, ...], "roles": {KEY: role},
                 "relation" ('product' | 'non_product' | 'unresolved_identity' | 'unreadable'), "read": what was read,
                 "date", "region", "revision", "note", "next_action"}}}
Statuses never claim more than was read: a document without a decision keeps 'automated identity only (not reviewed)'.
"""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
EPC = os.path.join(ROOT, 'existing_product_comparison_2026-11-12')
T = os.path.join(PKG, 'tables')


def rd(p):
    with open(p, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def wr(name, rows, cols=None):
    cols = cols or (list(rows[0].keys()) if rows else ['empty'])
    with open(os.path.join(T, name), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows)


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    man = rd(os.path.join(INV, 'manifest', 'file_manifest.csv'))
    U = {r['sha256']: r for r in rd(os.path.join(INV, 'tables', 'unique_documents.csv'))}
    A = {r['sha256']: r for r in rd(os.path.join(T, 'document_identity_auto.csv'))}
    ident = {r['product_id']: r for r in rd(os.path.join(EPC, 'tables', 'product_identities.csv'))}
    led = rd(os.path.join(EPC, 'tables', 'progress_ledger.csv'))
    epc_docs = {r['sha256'] for r in rd(os.path.join(EPC, 'tables', 'reviewed_documents.csv')) if r.get('sha256')}
    scope = {r['sha256']: r['read_scope'] for r in rd(os.path.join(EPC, 'tables', 'document_read_scope.csv'))}
    OPEN = ('content review LIMITED', 'NOT ASSESSED', 'hit lines only', 'additive lines only', 'page 1 only', 'no content comparison needed')
    epc_links = defaultdict(list)
    for r in led:
        if r['relationship_status'] in ('completed',) and not r['reviewed_categories'].startswith(('G',)):
            epc_links[r['sha256']].append(r)
    # decisions
    P, D = {}, {}
    for f in sorted(glob.glob(os.path.join(PKG, 'decisions', '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        for k, v in d.get('products', {}).items():
            P[k] = dict(P.get(k, {}), **v, decision_file=os.path.basename(f))
        for pre, v in d.get('documents', {}).items():
            hits = [s for s in U if s.startswith(pre)] if len(pre) >= 10 else [s for s in U if U[s]['first_path'] == pre or pre in U[s]['paths'].split(' | ')]
            assert len(hits) == 1, (f, pre, len(hits))
            D[hits[0]] = dict(v, decision_file=os.path.basename(f), batch=d.get('batch', ''))
    canon = {k: ('EXISTING:' + v['existing_record'] if v.get('existing_record') else k) for k, v in P.items()}
    # file register
    files = []
    for m in man:
        u = U[m['sha256']]
        files.append(dict(path=m['filename'], sha256=m['sha256'], size=m['size_bytes'], canonical_file=u['first_path'], copies_of_this_document=u['copies_in_batch'],
                          role='canonical' if m['filename'] == u['first_path'] else 'byte duplicate of the canonical file',
                          byte_duplicate_of_existing_archive=u['byte_duplicate_of_existing'] or ''))
    # documents + links
    docs, links = [], []
    for sha, u in U.items():
        a, dec = A[sha], D.get(sha)
        epc = epc_links.get(sha, [])
        epc_products = sorted({r['product_id'] for r in epc})
        if dec:
            prods = dec.get('products', [])
            rel = dec.get('relation', 'product' if prods else 'unresolved_identity')
            status = f"identity reviewed ({dec['batch']}): {dec.get('read', '')}"
            dtype, sup = dec.get('doc_type', u['document_type'] + ' (provisional)'), dec.get('supplier', u['supplier_provisional'] + ' (provisional)')
            nxt = dec.get('next_action', '')
        else:
            prods, rel = [], ('unreadable' if a['text_source'] == 'none' else 'unresolved_identity' if a['identity_confidence'] in ('none', 'low') else 'automated')
            status = 'automated identity only (not reviewed)'
            dtype, sup = u['document_type'] + ' (provisional)', (u['supplier_provisional'] or '(none)') + ' (provisional)'
            nxt = ('read the page images / OCR text to identify the product' if rel in ('unreadable', 'unresolved_identity') else
                   'confirm the automated identity in the supplier batch')
        for k in prods:
            links.append(dict(sha256=sha, file=u['first_path'], product_key=canon.get(k, k), printed_identity=P.get(k, {}).get('name', k), role=(dec.get('roles', {}) or {}).get(k, 'subject'), source='identity decision',
                              existing_record=P.get(k, {}).get('existing_record', ''), decision_file=dec['decision_file']))
        for r in epc:
            links.append(dict(sha256=sha, file=u['first_path'], product_key='EXISTING:' + r['product_id'], role='existing-product comparison link (' + r['reviewed_categories'] + ')',
                              source='existing_product_comparison ledger', existing_record=r['product_id'], decision_file=r['batch'][:60]))
        epc_open = sum(1 for r in epc if r['field_verification_status'].startswith(OPEN))
        docs.append(dict(sha256=sha, canonical_file=u['first_path'], all_paths=u['paths'], copies=u['copies_in_batch'], kind=u['kind'], pages=u['pages'],
                         readability=u['readability'], text_source=a['text_source'], document_type=dtype, supplier=sup,
                         products=' | '.join(canon.get(k, k) for k in prods), relation=rel, identity_status=status,
                         auto_identity=a['primary_identity'], auto_confidence=a['identity_confidence'], auto_basis=a['identity_basis'],
                         existing_comparison_products=' | '.join(epc_products), existing_comparison_open_links=epc_open,
                         existing_comparison_read_scope=scope.get(sha, ''), byte_duplicate_of_existing_archive=u['byte_duplicate_of_existing'],
                         printed_dates=dec.get('date', u['printed_dates']) if dec else u['printed_dates'], region=(dec or {}).get('region', ''),
                         revision=(dec or {}).get('revision', ''), note=(dec or {}).get('note', ''), next_action=nxt))
    # products
    prodrows = {}
    for k, v in P.items():
        if canon[k] != k:
            continue
        prodrows[k] = dict(product_key=k, name=v.get('name', ''), supplier=v.get('supplier', ''), material_class=v.get('material_class', ''),
                           existing_record=v.get('existing_record', ''), status=v.get('status', ''), template=v.get('template', ''),
                           identity_evidence=v.get('identity_evidence', ''), notes=v.get('notes', ''), decision_file=v.get('decision_file', ''))
    for pid, v in ident.items():
        prodrows.setdefault('EXISTING:' + pid, dict(product_key='EXISTING:' + pid, name=v['product_name'], supplier=v['supplier'], material_class=v['material_class'],
                                                     existing_record=pid, status='existing', template=v['material_class'], identity_evidence='existing production record',
                                                     notes='', decision_file='product_identities.csv'))
    alias = defaultdict(list)
    for k, c in canon.items():
        if c != k:
            alias[c].append(P[k].get('name', k))
    cnt = Counter(l['product_key'] for l in links)
    for k, r in prodrows.items():
        r['documents_linked'] = cnt.get(k, 0)
        r['aliases_from_batches'] = ' | '.join(sorted(set(alias.get(k, []))))
    # suppliers
    sup = defaultdict(lambda: Counter())
    for d in docs:
        s = re.sub(r' \(provisional\)$', '', d['supplier']) or '(none)'
        sup[s]['documents'] += 1
        sup[s]['identity_reviewed'] += d['identity_status'].startswith('identity reviewed')
        sup[s]['unreadable'] += d['relation'] == 'unreadable'
        sup[s]['unresolved'] += d['relation'] == 'unresolved_identity'
    recs = Counter(v['supplier'] for v in ident.values())
    suprows = [dict(supplier=s, documents=c['documents'], identity_reviewed=c['identity_reviewed'], unresolved_identity=c['unresolved'], unreadable=c['unreadable'],
                    existing_records_same_label=recs.get(s, 0)) for s, c in sorted(sup.items(), key=lambda x: -x[1]['documents'])]
    wr('file_register.csv', files)
    wr('document_register.csv', docs)
    wr('document_product_links.csv', links)
    wr('product_register.csv', sorted(prodrows.values(), key=lambda r: (r['supplier'], r['product_key'])))
    wr('supplier_register.csv', suprows)
    summ = dict(files=len(files), unique_documents=len(docs), canonical_files=sum(1 for f in files if f['role'] == 'canonical'),
                relation=dict(Counter(d['relation'] for d in docs)), identity_reviewed=sum(1 for d in docs if d['identity_status'].startswith('identity reviewed')),
                products=dict(Counter(r['status'] for r in prodrows.values())), links=len(links))
    json.dump(summ, open(os.path.join(T, 'register_summary.json'), 'w', encoding='utf-8'), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == '__main__':
    main()
