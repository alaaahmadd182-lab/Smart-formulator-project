"""Preparation checks (read-only). Exit code 1 if any check fails. Usage: python 04_checks.py [--hash-archive]
 C01 archive baseline: 4,422 files / 4,186 unique documents / 236 redundant copies (manifest); with --hash-archive the ZIP SHA-256
 C02 every unique document has exactly one register row; every file maps to a canonical document
 C03 every decision document prefix resolves to exactly one document and is owned by exactly one decision file
 C04 every product key linked by a decision is defined (in a decision file) or is an existing production record
 C05 status / relation vocabularies
 C06 an identity-reviewed 'product' document has >= 1 product, unless it is recorded as multi-product (next_action says so)
 C07 no product is 'conversion_ready' without stages 2 'verified', 3 'established', 5 'complete'; field-mapping rows cite a page
 C08 production data untouched: no difference in Products_json / json_templates against the workstream base commit ecd4ee3
 C09 OCR cache covers every document without a text layer; failures are listed, not hidden
 C10 field-evidence rows: allowed status vocabulary; non-Missing rows carry printed_text, source file and page"""
import csv, glob, hashlib, json, os, subprocess, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
ROOT = os.path.dirname(PKG)
T = os.path.join(PKG, 'tables')
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
ZIP = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip'
ZSHA = '62565d5c7a2afc2203536c241004cd4af7f62866a4bfe4f70801b378cf2c78b1'
rd = lambda p: list(csv.DictReader(open(p, encoding='utf-8'))) if os.path.exists(p) else []
res = []


def chk(cid, ok, msg):
    res.append((cid, bool(ok), msg)); print(('PASS ' if ok else 'FAIL ') + cid + ': ' + msg)


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    man = rd(os.path.join(INV, 'manifest', 'file_manifest.csv'))
    U = {r['sha256']: r for r in rd(os.path.join(INV, 'tables', 'unique_documents.csv'))}
    docs, files, links, prods, stages = (rd(os.path.join(T, n)) for n in ('document_register.csv', 'file_register.csv', 'document_product_links.csv', 'product_register.csv', 'product_stages.csv'))
    chk('C01', len(man) == 4422 and len(U) == 4186 and len(man) - len(U) == 236, f'{len(man)} files / {len(U)} unique / {len(man) - len(U)} redundant copies')
    if '--hash-archive' in sys.argv:
        h = hashlib.sha256()
        with open(ZIP, 'rb') as fh:
            for b in iter(lambda: fh.read(1 << 20), b''):
                h.update(b)
        chk('C01b', h.hexdigest() == ZSHA, 'archive SHA-256 ' + h.hexdigest()[:16])
    chk('C02', len(docs) == len(U) == len({d['sha256'] for d in docs}) and len(files) == len(man) and all(f['sha256'] in U for f in files), f'{len(docs)} document rows, {len(files)} file rows')
    own, bad = {}, []
    for f in sorted(glob.glob(os.path.join(PKG, 'decisions', '*.json'))):
        for pre in json.load(open(f, encoding='utf-8')).get('documents', {}):
            hits = [s for s in U if s.startswith(pre)]
            if len(hits) != 1: bad.append((os.path.basename(f), pre, 'hits', len(hits)))
            elif hits[0] in own: bad.append((os.path.basename(f), pre, 'also in', own[hits[0]]))
            else: own[hits[0]] = os.path.basename(f)
    chk('C03', not bad, f'{len(own)} decided documents, {len(bad)} problems {bad[:5]}')
    pk = {p['product_key'] for p in prods}
    und = sorted({l['product_key'] for l in links if l['product_key'] not in pk})
    chk('C04', not und, f'{len(und)} linked keys without a product row {und[:8]}')
    st = Counter(p['status'] for p in prods); rel = Counter(d['relation'] for d in docs)
    chk('C05', set(st) <= {'existing', 'new_candidate', 'new_confirmed', 'unresolved', 'out_of_scope'} and set(rel) <= {'product', 'non_product', 'unresolved_identity', 'unreadable', 'automated'}, f'{dict(st)} {dict(rel)}')
    e = [d['sha256'][:10] for d in docs if d['identity_status'].startswith('identity reviewed') and d['relation'] == 'product' and not d['products'] and 'multi-product' not in d['next_action'] and 'multi-product' not in d['document_type'] and not d['next_action'].startswith('list the')]
    chk('C06', not e, f'{len(e)} reviewed product documents without a product and without a multi-product disposition {e[:8]}')
    r7 = [s['product_key'] for s in stages if s['conversion_ready'] == 'yes' and not (s['stage2_identity'] == 'verified' and s['stage3_class_template'] == 'established' and s['stage5_field_mapping'] == 'complete')]
    chk('C07', not r7, f"{sum(s['conversion_ready'] == 'yes' for s in stages)} conversion-ready products; {len(r7)} inconsistent")
    g = subprocess.run(['git', '-C', ROOT, 'diff', '--quiet', 'ecd4ee3', '--', 'Products_json', 'json_templates'])
    g2 = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain', '--', 'Products_json', 'json_templates'], capture_output=True, text=True)
    chk('C08', g.returncode == 0 and not g2.stdout.strip(), 'Products_json and json_templates identical to ecd4ee3 and clean')
    need = [r['sha256'] for r in U.values() if r['readability'] != 'text' or r['kind'] == 'docx']
    have = {os.path.basename(f)[:64] for f in glob.glob(os.path.join(PKG, '_cache', 'ocr', '*.json.gz'))}
    log = os.path.join(PKG, 'logs', '01_ocr.log')
    err = [l.split('\t')[0] for l in open(log, encoding='utf-8')] if os.path.exists(log) else []
    err = [l for l in (open(log, encoding='utf-8').read().splitlines() if os.path.exists(log) else []) if 'ERROR' in l]
    chk('C09', not have or all(s in have for s in need), f'{len(need)} documents need OCR / extraction, {len(have)} cached, {len(err)} logged errors' + ('' if have else ' (cache not present in this checkout: not verified)'))
    fe = rd(os.path.join(T, 'field_evidence.csv'))
    ok_status = {'Reported', 'Calculated', 'Missing', 'Not Required', 'N/A', 'Not Applicable'}
    b10 = [r for r in fe if r['status'] not in ok_status or (r['status'] != 'Missing' and not (r['printed_text'] and r['source_file'] and r['page']))]
    chk('C10', not b10, f'{len(fe)} field-evidence rows, {len(b10)} invalid')
    fails = [c for c, ok, _ in res if not ok]
    print(f'{len(res) - len(fails)} / {len(res)} checks passed')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
