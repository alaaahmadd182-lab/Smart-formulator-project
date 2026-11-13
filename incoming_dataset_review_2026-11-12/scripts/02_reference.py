"""Incoming dataset inventory, pass 2: the reference side (read-only).

Collects what the new files are compared with:
  - every member of the existing source archive 'Manual + Data to share.zip': SHA-256, normalised-text SHA-256, pages;
  - locally available evidence copies (reconciliation/audit_evidence, reports/data_policy/external_evidence) and the
    SHA-256 values recorded in source_registry.json;
  - the product identities of Products_json (product_id, material class, supplier, product name) and which source
    files each product cites.
Writes _cache/reference.json. Usage: python incoming_dataset_review_2026-11-12/scripts/02_reference.py
"""
import collections, gzip, hashlib, json, os, re, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(BASE)
CACHE = os.path.join(BASE, '_cache')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'data_policy'))
import policy_lib as P  # noqa: E402


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def main():
    import pymupdf
    pymupdf.TOOLS.mupdf_display_errors(False)
    os.makedirs(os.path.join(CACHE, 'ref_text'), exist_ok=True)
    arch = os.path.join(ROOT, 'Manual + Data to share.zip')
    members = []
    with zipfile.ZipFile(arch) as z:
        for i in z.infolist():
            if i.is_dir():
                continue
            data = z.read(i.filename)
            sha = hashlib.sha256(data).hexdigest()
            rec = dict(path=i.filename, name=i.filename.rsplit('/', 1)[-1], size=i.file_size, sha256=sha, pages=None, text_sha256='', text_chars=0)
            if data[:4] == b'%PDF' or b'%PDF' in data[:1024]:
                try:
                    d = pymupdf.open(stream=data, filetype='pdf')
                    full = '\f'.join(p.get_text() for p in d)
                    n = norm(full)
                    rec.update(pages=d.page_count, text_chars=len(n), text_sha256=hashlib.sha256(n.encode('utf-8')).hexdigest() if n else '')
                    if n:
                        with gzip.open(os.path.join(CACHE, 'ref_text', sha + '.txt.gz'), 'wt', encoding='utf-8') as fh:
                            fh.write(full)
                except Exception as e:
                    rec['error'] = repr(e)[:120]
            members.append(rec)
    local = []
    for folder in ('reconciliation/audit_evidence', 'reports/data_policy/external_evidence'):
        for f in sorted(os.listdir(os.path.join(ROOT, folder))):
            p = os.path.join(ROOT, folder, f)
            if os.path.isfile(p):
                with open(p, 'rb') as fh:
                    local.append(dict(path=f'{folder}/{f}', sha256=hashlib.sha256(fh.read()).hexdigest()))
    with open(os.path.join(ROOT, 'source_registry.json'), encoding='utf-8') as fh:
        registry = [dict(url=s['url'], title=s.get('title'), sha256=s.get('sha256')) for s in json.load(fh)['sources'] if s.get('sha256')]
    prods = P.load_products()
    products, cites = [], collections.defaultdict(set)
    for pid, p in sorted(prods.items()):
        head = next(iter(p['files'].values()))
        pr = head.get('product') or {}
        for d in p['files'].values():
            for _, n in P.value_objects(d.get('fields', {})):
                f = (n.get('source') or {}).get('file')
                if f and not str(f).lower().startswith('http'):
                    cites[f].add(pid)
        products.append(dict(product_id=pid, material_class=p['class'], supplier=pr.get('supplier'), product_name=pr.get('product_name')))
    out = dict(archive=dict(path='Manual + Data to share.zip', size=os.path.getsize(arch), members=members), local_evidence=local,
               registry=registry, products=products, cited_files={k: sorted(v) for k, v in sorted(cites.items())})
    with open(os.path.join(CACHE, 'reference.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False)
    print(f'existing archive members: {len(members)} (unique hashes {len({m["sha256"] for m in members})}); local evidence files: {len(local)}; '
          f'registry hashes: {len(registry)}; products: {len(products)}; cited archive files: {len(cites)}')


if __name__ == '__main__':
    sys.exit(main())
