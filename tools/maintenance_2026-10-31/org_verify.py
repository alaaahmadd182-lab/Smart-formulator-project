"""Read-only verification after the folder organisation (outputs go to a temporary folder)."""
import hashlib, io, json, os, re, shutil, subprocess, sys, tarfile, tempfile, zipfile
sys.stdout.reconfigure(encoding='utf-8')
REPO = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project'
LONG = '\\\\?\\'
os.chdir(REPO)
fails = []


def check(c, m):
    print(('PASS ' if c else 'FAIL ') + m)
    if not c:
        fails.append(m)


def git(*a, b=False):
    r = subprocess.run(['git', *a], capture_output=True)
    return r.stdout if b else r.stdout.decode('utf-8')


print('== 1. What changed relative to the committed HEAD ==')
changed = set(git('diff', 'HEAD', '--name-only').split()) | set(git('ls-files', '--others', '--exclude-standard').split())
check(changed == {'README.md', 'reconciliation/README.md', 'PROJECT_FILE_GUIDE.md'}, f'only documentation changed: {sorted(changed)}')
for p in ('Products_json', 'reconciliation/audit_evidence', 'Manual + Data to share.zip', 'json_templates', 'Coverage_Matrix.xlsx',
          'open_questions_and_conflicts.md', 'source_registry.json', 'reconciliation/comprehensive_conflicts_audit.md',
          'reconciliation/comprehensive_conflicts_audit.csv', 'reconciliation/comprehensive_conflicts_audit_corrections_2026-10-31.md',
          'build_coverage_matrix.py', 'integrate_products.py', 'build_conflicts_report.py'):
    check(git('diff', 'HEAD', '--stat', '--', p).strip() == '', f'unchanged: {p}')

print('\n== 2. Working-tree bytes equal committed blobs (product data, evidence, source archive) ==')
mism = []
n = 0
for line in git('ls-files', '-s', '--', 'Products_json', 'reconciliation/audit_evidence', 'Manual + Data to share.zip').splitlines():
    meta, path = line.split('\t', 1)
    data = open(LONG + os.path.normpath(os.path.join(REPO, path)), 'rb').read()
    lf = data.replace(b'\r\n', b'\n') if not path.startswith('reconciliation/audit_evidence') and not path.endswith('.zip') else data
    sha = hashlib.sha1(b'blob %d\0' % len(lf) + lf).hexdigest()
    n += 1
    if sha != meta.split()[1]:
        mism.append(path)
check(not mism, f'{n} files compared with their committed blobs (evidence and ZIP byte-exact; JSON modulo CRLF); mismatches {mism[:5]}')
man = open('reconciliation/audit_evidence/evidence_manifest.md', encoding='utf-8').read()
ev = [f for f in os.listdir('reconciliation/audit_evidence') if f not in ('evidence_manifest.md', '.gitattributes')]
bad = [f for f in ev if hashlib.sha256(open(os.path.join('reconciliation/audit_evidence', f), 'rb').read()).hexdigest() not in man]
check(len(ev) == 11 and not bad, f'evidence SHA-256 values match evidence_manifest.md for {len(ev)} files; mismatches {bad}')

print('\n== 3. Source references resolve ==')
Z = zipfile.ZipFile('Manual + Data to share.zip')
names = {os.path.basename(x).replace('\ufffd', '%') for x in Z.namelist()}
reg = json.load(open('source_registry.json', encoding='utf-8'))
reg_urls = set(re.findall(r'https?://[^"\s]+', json.dumps(reg, ensure_ascii=False)))
cited, missing, unreg = set(), set(), set()
for dp, _, fs in os.walk(LONG + os.path.join(REPO, 'Products_json')):
    for f in fs:
        d = json.load(open(os.path.join(dp, f), encoding='utf-8'))
        def rec(x):
            if isinstance(x, dict):
                s = x.get('source')
                if isinstance(s, dict) and s.get('file'):
                    v = s['file']
                    (unreg if v.startswith('http') and v not in reg_urls else cited).add(v) if v.startswith('http') else (cited.add(v), None if v in names else missing.add(v))
                for v in x.values(): rec(v)
            elif isinstance(x, list):
                for v in x: rec(v)
        rec(d)
        for sd in d.get('source_documents') or []:
            v = sd.get('file') if isinstance(sd, dict) else sd
            if isinstance(v, str) and not v.startswith('http'):
                cited.add(v)
                if v not in names: missing.add(v)
arch = {c for c in cited if not c.startswith('http')}
check(not missing, f'{len(arch)} distinct archive files cited by the JSON all exist in the source archive; missing {sorted(missing)[:5]}')
check(not unreg, f'cited URLs not in source_registry.json: {sorted(unreg)[:5]}')

print('\n== 4. Paths named in PROJECT_FILE_GUIDE.md exist ==')
guide = open('PROJECT_FILE_GUIDE.md', encoding='utf-8').read()
paths = set(re.findall(r'`((?:reconciliation/|json_templates/|Products_json/)?[A-Za-z0-9_ .+()/-]+\.(?:md|csv|json|py|xlsx|docx|zip|txt))`', guide))
skip = {'conflicts_report_generated.md', 'Coverage_Matrix_new.xlsx', 'general.json', 'vm.json', 'tier1_route_defining.json',
        'tier2_numeric_contribution.json', 'Smart formulator project.zip', 'Smart formulator project (2).zip',
        'SmartFormulator_conflicts_audit_review_2026-10-30.zip', 'SmartFormulator_source_corrections_review_2026-10-31.zip',
        'SmartFormulator_source_corrections_review_v2_2026-10-31.zip', 'AGG WEBSITE.zip', 'tools/validate_corrections.py',
        'comprehensive_conflicts_audit.md', 'comprehensive_conflicts_audit.csv', 'comprehensive_conflicts_audit_corrections_2026-10-31.md',
        'identity_review.md', 'inventory_reconciliation.csv', 'deferred_products.csv', 'deferred_products.md', 'base_oil_ingestion_queue.md',
        'richful_feed_leads.csv', 'evidence_manifest.md', 'audit_evidence/evidence_manifest.md', 'base_oil_tier1_blocking.json',
        'base_oil_tier2_verification.json', 'base_oil_tier3_substitution.json', 'additive_package_tier1_route_defining.json',
        'additive_package_tier2_numeric_contribution.json', 'additive_component_all_general.json', 'additive_component_vm.json',
        'additive_component_ppd.json', 'package_company_mapping.csv',
        '_tier2.json', '_tier3.json', 'python build_coverage_matrix.py --output Coverage_Matrix_new.xlsx'}  # naming patterns / a command
loc = {'comprehensive_conflicts_audit.md': 'reconciliation/', 'comprehensive_conflicts_audit.csv': 'reconciliation/',
       'comprehensive_conflicts_audit_corrections_2026-10-31.md': 'reconciliation/', 'identity_review.md': 'reconciliation/',
       'inventory_reconciliation.csv': 'reconciliation/', 'deferred_products.csv': 'reconciliation/', 'deferred_products.md': 'reconciliation/',
       'base_oil_ingestion_queue.md': 'reconciliation/', 'richful_feed_leads.csv': 'reconciliation/', 'evidence_manifest.md': 'reconciliation/audit_evidence/',
       'audit_evidence/evidence_manifest.md': 'reconciliation/', **{t: 'json_templates/' for t in os.listdir('json_templates')}}
miss = [p for p in sorted(paths) if not os.path.exists(loc.get(p, '') + p) and p not in skip - set(loc)]
check(not miss, f'{len(paths)} file paths named in the guide resolve (bare names resolved in their folder); missing {miss}')
for d in ('Products_json/Base_oils_json', 'Products_json/Additive_packages_json', 'Products_json/Additive_components_json', 'json_templates', 'reconciliation/audit_evidence'):
    check(os.path.isdir(d), f'folder exists: {d}')

print('\n== 5. Scripts still run (outputs to a temporary folder) ==')
with tempfile.TemporaryDirectory() as tmp:
    out = os.path.join(tmp, 'cm.xlsx')
    r = subprocess.run([sys.executable, 'build_coverage_matrix.py', '--output', out], capture_output=True, text=True, encoding='utf-8')
    check(r.returncode == 0, 'build_coverage_matrix.py exit 0: ' + (r.stdout.splitlines() or [''])[0][:200])
    from openpyxl import load_workbook
    def rows(p):
        wb = load_workbook(p, read_only=True)
        try:
            return {s: [tuple(x) for x in wb[s].iter_rows(values_only=True)] for s in wb.sheetnames}
        finally:
            wb.close()
    check(rows(out) == rows('Coverage_Matrix.xlsx'), 'fresh coverage workbook equals Coverage_Matrix.xlsx in every sheet and cell')
    rep = os.path.join(tmp, 'conflicts_report_generated.md')
    r = subprocess.run([sys.executable, 'build_conflicts_report.py', '--output', rep], capture_output=True, text=True, encoding='utf-8')
    check(r.returncode == 0 and os.path.getsize(rep) > 1000, f'build_conflicts_report.py exit {r.returncode}, report {os.path.getsize(rep) if os.path.exists(rep) else 0} bytes (temporary)')
    # integration dry run on a temporary copy of the committed Products_json
    copy = os.path.join(tmp, 'pj')
    data = subprocess.run(['git', 'archive', '--format=tar', 'HEAD', 'Products_json'], capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        for m in t.getmembers():
            if m.isfile():
                p = LONG + os.path.normpath(os.path.join(copy, m.name))
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, 'wb').write(t.extractfile(m).read())
    r = subprocess.run([sys.executable, 'integrate_products.py', '--input', os.path.join(copy, 'Products_json')], capture_output=True, text=True, encoding='utf-8')
    first = (r.stdout.splitlines() or [''])[0]
    check(first.startswith('DRY RUN (nothing written)') and r.returncode == 0, f'integrate_products.py dry run on a temporary copy, exit {r.returncode}: {first[:220]}')
    shutil.rmtree(copy, ignore_errors=True)
print('\nOVERALL:', 'ALL CHECKS PASSED' if not fails else f'{len(fails)} FAILED')
sys.exit(1 if fails else 0)
