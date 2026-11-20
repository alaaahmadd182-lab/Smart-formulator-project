"""Automated audit of the field evidence (field_evidence/*.csv) against the cached page text. Read-only on evidence.

This is an AUTOMATED check. It is not a source review and never makes a product conversion-ready by itself.
For every row:
  Reported rows   'number found on cited page'   every number in value / min / max occurs as a number on the cited page
                  'number NOT found on cited page' at least one does not (extraction error, wrong page, or a reformatted value)
                  'text row (no number)'          nothing numeric to compare; printed_text words compared instead
                  'page not available'            the cached text has no such page (or no cache for the document)
                  + 'OCR page: visual check required' when the cited page text came from OCR (01_ocr.py)
  flags           'SDS source in an element / marker field' (an SDS component share must never be an element content)
                  'value form inconsistent' (bound without qualifier/bound, range without min+max, typical without value)
                  'numeric Reported row without unit'; 'percentage basis unspecified' (unit '%' on a dose / treat-rate row)
  Missing rows    'Missing, inspection recorded'  the note says what was inspected (e.g. 'not printed on the sheet (all pages read)')
                  'Missing, no inspection note'   no such note: a parser that found nothing does NOT prove the value is absent
Discovery: every field_evidence/*.csv is read; field_evidence/MANIFEST.json lists the expected files, row counts and SHA-256.
The audit FAILS (exit 1) when a file is unreadable, lacks required columns, is not in the manifest, is listed but absent, or
its row count / hash differs (run with --update-manifest only after a reviewed evidence change).
Outputs: tables/evidence_audit_rows.csv, tables/evidence_audit_products.csv, tables/evidence_audit_summary.json.
Usage: python 09_audit_evidence.py [--update-manifest]   (cache locations: see scripts/paths.py)"""
import csv, glob, gzip, hashlib, json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths import PKG, TEXT_CACHE, OCR_CACHE, describe

T = os.path.join(PKG, 'tables')
FE = os.path.join(PKG, 'field_evidence')
REQ = ['product_key', 'template', 'field', 'value', 'qualifier', 'min', 'max', 'value_kind', 'printed_text', 'unit', 'status', 'source_file', 'sha256', 'page', 'notes', 'review']
NUM = re.compile(r'(?<![\w.])-?\d+(?:[.,]\d+)?')
INSPECTED = re.compile(r'(?i)not printed|not stated|not found|all pages read|no .{0,40}printed|not given|no dosage|no restriction|listed .{0,30}Report|no value printed|not on the sheet|absent from|sheet (?:gives|prints) no|no formulation|no co-component|no base-oil|not reported on|none printed|not provided')
ELEMENT = re.compile(r'^(elements\.|function_specific_markers\.(ca|mg|p|zn|mo)$)')


def pages(sha):
    out, src = [], []
    p = os.path.join(TEXT_CACHE, sha + '.txt.gz')
    if os.path.exists(p):
        out = gzip.open(p, 'rt', encoding='utf-8').read().split('\f')
        src = ['text_layer'] * len(out)
    o = os.path.join(OCR_CACHE, sha + '.json.gz')
    if os.path.exists(o):
        for pg in json.load(gzip.open(o, 'rt', encoding='utf-8'))['pages']:
            i = pg['page'] - 1
            while len(out) <= i:
                out.append(''); src.append('none')
            if len(re.sub(r'\s', '', out[i])) < 20 and pg.get('text'):
                out[i], src[i] = pg['text'], pg['source']
    return out, src


def nums(s):
    v = set()
    for m in NUM.findall(s.replace('−', '-').replace('–', '-')):
        for x in {m, m.replace(',', '.')}:
            try:
                v.add(round(float(x), 6))
            except ValueError:
                pass
    return v


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    files = sorted(glob.glob(os.path.join(FE, '*.csv')))
    mpath = os.path.join(FE, 'MANIFEST.json')
    man = json.load(open(mpath, encoding='utf-8')) if os.path.exists(mpath) else {'files': {}}
    problems, rows, seen = [], [], {}
    for f in files:
        b = os.path.basename(f)
        try:
            R = list(csv.DictReader(open(f, encoding='utf-8')))
        except Exception as e:
            problems.append(f'{b}: unreadable ({e})'); continue
        cols = set(R[0].keys()) if R else set()
        miss = [c for c in REQ if c not in cols]
        if not R or miss:
            problems.append(f'{b}: {len(R)} rows, missing columns {miss}')
        seen[b] = dict(rows=len(R), sha256=hashlib.sha256(open(f, 'rb').read()).hexdigest())
        for i, r in enumerate(R, 2):
            r['_file'], r['_line'] = b, i
            rows.append(r)
    if '--update-manifest' in sys.argv:
        man = {'note': 'Expected field-evidence files (written by --update-manifest after a reviewed evidence change).', 'files': seen}
        json.dump(man, open(mpath, 'w', encoding='utf-8'), indent=1)
    for b, m in man['files'].items():
        if b not in seen:
            problems.append(f'{b}: listed in MANIFEST.json but absent')
        elif seen[b] != m:
            problems.append(f"{b}: rows/hash differ from MANIFEST.json ({seen[b]['rows']} vs {m['rows']} rows)")
    for b in seen:
        if b not in man['files']:
            problems.append(f'{b}: present but not in MANIFEST.json (would be skipped silently by a fixed list)')
    # document types and readiness inputs
    doct = {d['sha256']: d['document_type'] for d in csv.DictReader(open(os.path.join(T, 'document_register.csv'), encoding='utf-8'))}
    fm = {r['product_key']: r for r in csv.DictReader(open(os.path.join(T, 'field_mapping_status.csv'), encoding='utf-8'))}
    cache = {}
    out = []
    for r in rows:
        sha, res, flags = r.get('sha256', ''), '', []
        if r['status'] == 'Reported' or r['status'] == 'Calculated':
            if sha not in cache:
                cache[sha] = pages(sha) if sha else ([], [])
            pg, src = cache[sha]
            try:
                pn = int(float(r['page']))
            except ValueError:
                pn = 0
            vals = [x for x in (r['value'], r['min'], r['max']) if x.strip()]
            if not (1 <= pn <= len(pg)) or not pg[pn - 1].strip():
                res = 'page not available'
            elif vals:
                pv = nums(pg[pn - 1])
                ok = all(nums(v) and nums(v) <= pv for v in vals)
                res = 'number found on cited page' if ok else 'number NOT found on cited page'
            else:
                words = [w for w in re.findall(r'[A-Za-z]{4,}', r['printed_text'])][:12]
                low = pg[pn - 1].lower()
                hit = sum(w.lower() in low for w in words)
                res = 'text row (no number): words found' if words and hit >= 0.7 * len(words) else 'text row (no number): words NOT found'
            if 1 <= pn <= len(src) and src[pn - 1] == 'ocr':
                flags.append('OCR page: visual check required')
            if ELEMENT.match(r['field']) and 'SDS' in doct.get(sha, '').upper():
                flags.append('SDS source in an element / marker field')
            k = r['value_kind']
            if (k == 'bound' and not (r['qualifier'] and (r['min'] or r['max']))) or (k == 'range' and not (r['min'] and r['max'])) or (k == 'typical' and not r['value']):
                flags.append('value form inconsistent')
            if vals and not r['unit'].strip():
                flags.append('numeric Reported row without unit')
            if r['unit'].strip() == '%' and re.search(r'(?i)treat|dos', r['field'] + ' ' + r.get('value_class', '')):
                flags.append('percentage basis unspecified')
        elif r['status'] == 'Missing':
            res = 'Missing, inspection recorded' if INSPECTED.search(r['notes']) else 'Missing, no inspection note'
        else:
            res = r['status']
        out.append(dict(file=r['_file'], line=r['_line'], product_key=r['product_key'], template=r['template'], field=r['field'], status=r['status'], page=r['page'],
                        result=res, flags=' | '.join(flags), extraction='programmatic' if 'programmatic' in fm.get(r['product_key'], {}).get('evidence_review', '') else 'read'))
    with open(os.path.join(T, 'evidence_audit_rows.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    P = defaultdict(Counter)
    for o in out:
        c = P[o['product_key']]
        c['rows'] += 1; c[o['status']] += 1; c[o['result']] += 1
        for fl in filter(None, o['flags'].split(' | ')):
            c[fl] += 1
        c['_extraction_' + o['extraction']] += 1
    prow = []
    for k, c in sorted(P.items()):
        fail = c['number NOT found on cited page'] + c['page not available'] + c['text row (no number): words NOT found']
        issues = []
        if fail: issues.append(f'{fail} Reported rows not matched on the cited page')
        if c['OCR page: visual check required']: issues.append(f"{c['OCR page: visual check required']} OCR-derived rows need a visual check")
        if c['SDS source in an element / marker field']: issues.append(f"{c['SDS source in an element / marker field']} SDS rows in element fields")
        if c['value form inconsistent']: issues.append(f"{c['value form inconsistent']} value-form inconsistencies")
        if c['numeric Reported row without unit']: issues.append(f"{c['numeric Reported row without unit']} numeric rows without unit")
        if c['percentage basis unspecified']: issues.append(f"{c['percentage basis unspecified']} dose rows with unspecified % basis")
        if c['Missing, no inspection note']: issues.append(f"{c['Missing, no inspection note']} Missing rows without an inspection note")
        if c['Reported'] == 0: issues.append('no Reported row at all')
        if c['_extraction_programmatic']: issues.append('programmatic extraction (not a reading review)')
        prow.append(dict(product_key=k, rows=c['rows'], reported=c['Reported'], missing=c['Missing'], reported_matched=c['number found on cited page'] + c['text row (no number): words found'],
                         reported_not_matched=fail, ocr_visual_needed=c['OCR page: visual check required'], sds_element_flags=c['SDS source in an element / marker field'],
                         missing_inspected=c['Missing, inspection recorded'], missing_no_note=c['Missing, no inspection note'],
                         extraction='programmatic' if c['_extraction_programmatic'] else 'read',
                         auto_check='pass' if not issues else 'issues', auto_issues='; '.join(issues)))
    with open(os.path.join(T, 'evidence_audit_products.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(prow[0].keys())); w.writeheader(); w.writerows(prow)
    rc = Counter(o['result'] for o in out)
    fc = Counter(fl for o in out for fl in filter(None, o['flags'].split(' | ')))
    summ = dict(caches=describe(), files_checked={b: v['rows'] for b, v in seen.items()}, files=len(seen), rows=len(out), products=len(prow),
                status=dict(Counter(o['status'] for o in out)), row_results=dict(rc), row_flags=dict(fc),
                products_auto_pass=sum(p['auto_check'] == 'pass' for p in prow), products_with_issues=sum(p['auto_check'] != 'pass' for p in prow),
                discovery_problems=problems)
    json.dump(summ, open(os.path.join(T, 'evidence_audit_summary.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in summ.items() if k != 'files_checked'}, indent=1, ensure_ascii=False))
    for b, v in seen.items():
        print(f'  checked {b}: {v["rows"]} rows')
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
