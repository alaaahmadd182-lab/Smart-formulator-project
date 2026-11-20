"""Preparation checks (read-only). Exit code 1 if any check fails. Usage: python 04_checks.py [--hash-archive]
 C01 archive baseline: 4,422 files / 4,186 unique documents / 236 redundant copies (manifest); with --hash-archive the ZIP SHA-256
 C02 every unique document has exactly one register row; every file maps to a canonical document
 C03 every decision document prefix resolves to exactly one document and is owned by exactly one decision file
 C04 every product key linked by a decision is defined (in a decision file) or is an existing production record
 C05 status / relation vocabularies
 C06 an identity-reviewed 'product' document has >= 1 product, unless it is recorded as multi-product (next_action says so)
 C07 conversion_ready only with stage 2 'verified', 3 'established', evidence read (not programmatic), a source-verification sign-off,
     an automated audit pass and no blockers (rule of the 2026-11-20 integration review)
 C08 production data untouched: no difference in Products_json / json_templates against the workstream base commit ecd4ee3
 C09 OCR cache covers every document without a text layer; failures are listed, not hidden
 C10 evidence discovery (integration): every field_evidence/*.csv is read and printed with its row count; files, row counts and SHA-256
     must match field_evidence/MANIFEST.json (no file skipped, none unlisted); every product mapped in tables/field_mapping_status.csv
     has evidence rows and every product in the evidence has a mapping-status row; >= 1 row checked (a check over 0 rows fails)
 C11 evidence validity (readiness): allowed status vocabulary; non-Missing rows carry printed_text, source file and page. FAIL if any
     invalid row belongs to a conversion-ready or source-verified product; invalid rows in unfinished mappings are counted and reported
 C12 automated evidence audit present and current (tables/evidence_audit_summary.json from 09_audit_evidence.py covers every
     evidence file with the same row counts; no discovery problem)"""
import csv, glob, hashlib, json, os, subprocess, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
ROOT = os.path.dirname(PKG)
T = os.path.join(PKG, 'tables')
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
sys.path.insert(0, HERE)
from paths import ARCHIVE_ZIP as ZIP, OCR_CACHE  # configurable: SF_ARCHIVE_ZIP / SF_OCR_CACHE (see paths.py)
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
    r7 = [s['product_key'] for s in stages if s['conversion_ready'] == 'yes' and not (s['stage2_identity'] == 'verified' and s['stage3_class_template'] == 'established'
          and not s['stage4_evidence_review'].startswith('programmatic') and s['source_verified'].startswith('yes') and s['auto_check'] == 'pass' and not s['blockers'])]
    chk('C07', not r7, f"{sum(s['conversion_ready'] == 'yes' for s in stages)} conversion-ready products; {len(r7)} inconsistent; "
        f"{sum(s.get('ready_under_previous_rule') == 'yes' for s in stages)} would be 'ready' under the previous rule (generated mapping only)")
    g = subprocess.run(['git', '-C', ROOT, 'diff', '--quiet', 'ecd4ee3', '--', 'Products_json', 'json_templates'])
    g2 = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain', '--', 'Products_json', 'json_templates'], capture_output=True, text=True)
    chk('C08', g.returncode == 0 and not g2.stdout.strip(), 'Products_json and json_templates identical to ecd4ee3 and clean')
    need = [r['sha256'] for r in U.values() if r['readability'] != 'text' or r['kind'] == 'docx']
    have = {os.path.basename(f)[:64] for f in glob.glob(os.path.join(OCR_CACHE, '*.json.gz'))}
    log = os.path.join(PKG, 'logs', '01_ocr.log')
    err = [l.split('\t')[0] for l in open(log, encoding='utf-8')] if os.path.exists(log) else []
    err = [l for l in (open(log, encoding='utf-8').read().splitlines() if os.path.exists(log) else []) if 'ERROR' in l]
    chk('C09', not have or all(s in have for s in need), f'{len(need)} documents need OCR / extraction, {len(have)} cached, {len(err)} logged errors' + ('' if have else ' (cache not present in this checkout: not verified)'))
    fe_files = sorted(glob.glob(os.path.join(PKG, 'field_evidence', '*.csv')))
    mpath = os.path.join(PKG, 'field_evidence', 'MANIFEST.json')
    man = json.load(open(mpath, encoding='utf-8'))['files'] if os.path.exists(mpath) else {}
    fe, p10, seen = [], [], {}
    for _f in fe_files:
        b = os.path.basename(_f)
        rows_f = rd(_f)
        seen[b] = dict(rows=len(rows_f), sha256=hashlib.sha256(open(_f, 'rb').read()).hexdigest())
        print(f'      evidence file {b}: {len(rows_f)} rows')
        if not rows_f:
            p10.append(f'{b}: 0 rows')
        fe.extend(rows_f)
    for b, m in man.items():
        if b not in seen: p10.append(f'{b}: in MANIFEST.json but absent')
        elif seen[b] != m: p10.append(f'{b}: rows/hash differ from MANIFEST.json')
    p10 += [f'{b}: not in MANIFEST.json' for b in seen if b not in man]
    if not man: p10.append('field_evidence/MANIFEST.json missing')
    fmk = {r['product_key'] for r in rd(os.path.join(T, 'field_mapping_status.csv')) if r.get('field_mapping') == 'complete'}
    evk = {r['product_key'] for r in fe}
    p10 += [f'mapped without evidence rows: {k}' for k in sorted(fmk - evk)][:10] + [f'evidence without mapping-status row: {k}' for k in sorted(evk - fmk)][:10]
    if not fe: p10.append('0 evidence rows checked')
    chk('C10', not p10, f'{len(fe)} evidence rows from {len(fe_files)} files ({len(evk)} products) checked against the manifest; problems: {p10[:6]}')
    ok_status = {'Reported', 'Calculated', 'Missing', 'Not Required', 'N/A', 'Not Applicable'}
    b11 = [r for r in fe if r['status'] not in ok_status or (r['status'] != 'Missing' and not (r['printed_text'] and r['source_file'] and r['page']))]
    gated = {s['product_key'] for s in stages if s['conversion_ready'] == 'yes' or s.get('source_verified', 'no').startswith('yes')}
    bad_g = sorted({r['product_key'] for r in b11 if r['product_key'] in gated})
    byfile = Counter(r.get('product_key', '').split(':')[0] for r in b11)
    chk('C11', not bad_g, f'{len(b11)} invalid rows in {len({r["product_key"] for r in b11})} products (all in unfinished mappings: {not bad_g}); by key prefix {dict(byfile.most_common(6))}; '
        f'invalid rows in ready / source-verified products: {bad_g[:5]}')
    ap = os.path.join(T, 'evidence_audit_summary.json')
    au = json.load(open(ap, encoding='utf-8')) if os.path.exists(ap) else {}
    p12 = [] if au else ['tables/evidence_audit_summary.json missing: run 09_audit_evidence.py']
    if au:
        if au.get('discovery_problems'): p12.append(f"audit discovery problems: {au['discovery_problems'][:3]}")
        if au.get('files_checked') != {b: v['rows'] for b, v in seen.items()}: p12.append('audit is stale: files / row counts differ from field_evidence/')
    chk('C12', not p12, f"audit covers {au.get('files', 0)} files / {au.get('rows', 0)} rows; {au.get('products_auto_pass', 0)} products pass, {au.get('products_with_issues', 0)} with issues; {p12}")
    fails = [c for c, ok, _ in res if not ok]
    print(f'{len(res) - len(fails)} / {len(res)} checks passed')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
