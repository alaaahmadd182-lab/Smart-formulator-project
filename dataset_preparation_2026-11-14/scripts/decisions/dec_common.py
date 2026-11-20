"""Shared helpers for the supplier-batch decision generators from S25 onward (S01-S24 are self-contained).
Selection is by the provisional supplier label of tables/document_identity_auto.csv; a document already decided in an earlier
batch file is never taken again (first decision stands; changes are made in the batch that owns the document).
Document fields added from S25: 'manufacturer', 'distributor', 'issuer' (kept apart; '' = not printed / not established)."""
import csv, glob, json, os, re, importlib.util
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
_spec = importlib.util.spec_from_file_location('ident', os.path.join(os.path.dirname(HERE), '02_identify.py'))
ident = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ident)
TEMPLATE = {'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ subtype as noted)', 'base_oil': 'base_oil tier1-3'}


def rows(label_test, own_file=None):
    """Automated-identity rows whose provisional supplier passes label_test and that no OTHER decision file already owns."""
    taken = set()
    for f in glob.glob(os.path.join(PKG, 'decisions', '*.json')):
        if own_file and os.path.basename(f) == own_file:
            continue
        taken |= set(json.load(open(f, encoding='utf-8')).get('documents', {}))
    out = []
    for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')):
        if label_test(r['supplier_provisional']) and not any(r['sha256'].startswith(p) for p in taken):
            out.append(r)
    return out


def page_text(sha, n=1):
    pg, _ = ident.pages_for(sha)
    return re.sub(r'\s+', ' ', ' '.join(pg[:n]) if pg else '')


def top(r):
    return [x.strip() for x in re.split(r'\n|\s\|\s', r['top_lines'])]


def doc(D, sha, doc_type, supplier, products, read, roles=None, relation=None, note='', next_action='', manufacturer='', distributor='', issuer='', **kw):
    D[sha[:12]] = dict(doc_type=doc_type, supplier=supplier, products=list(products), roles=roles or {k: 'subject' for k in products},
                       relation=relation or ('product' if products else 'unresolved_identity'), read=read, note=note, next_action=next_action,
                       manufacturer=manufacturer, distributor=distributor, issuer=issuer, **kw)


def prod(PK, key, name, supplier, material_class, notes, existing='', evidence='printed product name on the documents linked in this batch', status=None):
    if key in PK:
        return
    PK[key] = dict(name=name, supplier=supplier, material_class=material_class, existing_record=existing,
                   status=status or ('existing' if existing else 'out_of_scope' if material_class.startswith('out_of') else 'new_candidate'),
                   notes=notes, identity_evidence=evidence, template=TEMPLATE.get(material_class, 'none / not determined'))


PSEUDO = re.compile(r':(UNKNOWN_|CATALOG$)')
PRODUCT_STATUS = {'existing', 'new_candidate', 'new_confirmed', 'unresolved', 'out_of_scope'}
RELATIONS = {'product', 'non_product', 'unresolved_identity', 'unreadable'}


def _normalise(PK, D):
    """Integration review 2026-11-20: a document whose product is not identified is NOT a product. Pseudo-keys such as
    'ADNOC:UNKNOWN_DOC_DL2_14075' or 'SHENYANG_GW:CATALOG' are removed from the product list and from the documents; the
    document keeps its note and gets relation 'unresolved_identity' (or a multi-product disposition for a catalogue).
    Vocabularies are enforced so that a generator cannot introduce new status / relation values."""
    for k in [k for k in PK if PSEUDO.search(k)]:
        PK.pop(k)
    for s, v in D.items():
        gone = [k for k in v['products'] if PSEUDO.search(k)]
        if not gone:
            continue
        v['products'] = [k for k in v['products'] if k not in gone]
        v['roles'] = {k: r for k, r in v.get('roles', {}).items() if k not in gone}
        cat = any(k.endswith(':CATALOG') for k in gone)
        v['note'] = (v.get('note', '') + f" [integration review 2026-11-20: pseudo-product key {', '.join(gone)} removed; "
                     + ("catalogue kept as a multi-product document]" if cat else "identity not established, no product created]")).strip()
        if cat:
            v['relation'] = 'product'
            v['next_action'] = 'multi-product catalogue (finished lubricants, out of template): list products only if the scope changes'
        else:
            v['relation'] = 'unresolved_identity'
            v['next_action'] = v.get('next_action') or 'identify the product from the page image (name not legible in the text layer)'
    bad = [(k, p.get('status')) for k, p in PK.items() if p.get('status') not in PRODUCT_STATUS] + \
          [(s, v.get('relation')) for s, v in D.items() if v.get('relation') not in RELATIONS]
    if bad:
        raise SystemExit(f'vocabulary violation: {bad[:5]}')


def write(name, batch, scope, PK, D, reviewed_on='2026-11-15'):
    _normalise(PK, D)
    json.dump(dict(batch=batch, reviewed_on=reviewed_on, scope=scope, products=PK, documents=D),
              open(os.path.join(PKG, 'decisions', name), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(name, len(D), 'documents', len(PK), 'products', dict(Counter(v['relation'] for v in D.values())), dict(Counter(p['material_class'] for p in PK.values())))
