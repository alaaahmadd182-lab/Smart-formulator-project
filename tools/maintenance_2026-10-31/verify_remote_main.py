"""Verify a fresh clone of origin/main. Usage: verify_remote_main.py <clone dir>. Outputs go to a temp folder."""
import hashlib, json, os, re, subprocess, sys, tempfile
sys.stdout.reconfigure(encoding='utf-8')
C = os.path.abspath(sys.argv[1]); os.chdir(C)
LONG = '\\\\?\\'
fails = []


def check(c, m):
    print(('PASS ' if c else 'FAIL ') + m)
    if not c: fails.append(m)


print('clone HEAD', subprocess.run(['git', 'log', '-1', '--format=%H %s'], capture_output=True, text=True).stdout.strip())
REQ = ['reconciliation/comprehensive_conflicts_audit.md', 'reconciliation/comprehensive_conflicts_audit.csv',
       'reconciliation/audit_evidence/evidence_manifest.md', 'reconciliation/audit_evidence/.gitattributes',
       'reconciliation/comprehensive_conflicts_audit_corrections_2026-10-31.md', 'Coverage_Matrix.xlsx', 'PROJECT_FILE_GUIDE.md',
       'README.md', 'reconciliation/README.md', 'open_questions_and_conflicts.md', 'Manual + Data to share.zip',
       'Products_json/Base_oils_json/CHEVRON/CHEVRON_SYNFLUID_DIMER_C12/CHEVRON_SYNFLUID_DIMER_C12__base_oil_tier2_verification.json',
       'Products_json/Additive_packages_json/Lubrizol/LUBRIZOL_CV1100/tier2_numeric_contribution.json',
       'Products_json/Additive_packages_json/Lubrizol/LUBRIZOL_CV3515/tier2_numeric_contribution.json',
       'Products_json/Additive_packages_json/Richful/RICHFUL_RF6066/tier2_numeric_contribution.json',
       'Products_json/Additive_packages_json/Richful/RICHFUL_RF6078/tier1_route_defining.json']
for p in REQ:
    check(os.path.exists(LONG + os.path.normpath(os.path.join(C, p))), f'present: {p}')

man = open('reconciliation/audit_evidence/evidence_manifest.md', encoding='utf-8').read()
saved, archived = man.split('## Archive documents checked visually')[0], man.split('## Archive documents checked visually')[1].split('## Sources that could not')[0]
pat = r'^\| `([^`]+)` \|.*?\| `([0-9a-f]{64})` \|'
rows = {m.group(1): m.group(2) for m in re.finditer(pat, saved, re.M)}
ev = sorted(f for f in os.listdir('reconciliation/audit_evidence') if f not in ('evidence_manifest.md', '.gitattributes'))
check(len(ev) == 11 and set(ev) == set(rows), f'11 evidence files, exactly the files in the manifest section "saved in this folder" ({len(ev)} files, {len(rows)} rows)')
for f in ev:
    h = hashlib.sha256(open(os.path.join('reconciliation/audit_evidence', f), 'rb').read()).hexdigest()
    check(h == rows.get(f), f'SHA-256 matches manifest: {f}')
import zipfile
Z = zipfile.ZipFile('Manual + Data to share.zip')
arows = {m.group(1): m.group(2) for m in re.finditer(pat, archived, re.M)}
names = {n.replace('�', '%'): n for n in Z.namelist()}
ok = [p for p, h in arows.items() if p in names and hashlib.sha256(Z.read(names[p])).hexdigest() == h]
check(len(arows) == 9 and len(ok) == 9, f'archive documents listed in the manifest: {len(ok)}/{len(arows)} SHA-256 match the source ZIP in the clone')

ALLOWED = {'Reported', 'Calculated', 'Missing', 'Not Required', 'N/A', 'Not Applicable'}
n = bad_json = 0; bad_status = []; classes = {}
for dp, _, fs in os.walk(LONG + os.path.join(C, 'Products_json')):
    for f in fs:
        if not f.endswith('.json'): continue
        n += 1
        try:
            d = json.load(open(os.path.join(dp, f), encoding='utf-8'))
        except Exception:
            bad_json += 1; continue
        classes[d.get('material_class')] = classes.get(d.get('material_class'), 0) + 1
        def rec(x, p=''):
            if isinstance(x, dict):
                if 'status' in x and 'value' in x and not isinstance(x['status'], dict) and x['status'] not in ALLOWED:
                    bad_status.append((f, p, x['status']))
                for k, v in x.items(): rec(v, p + '.' + k)
            elif isinstance(x, list):
                for i, v in enumerate(x): rec(v, f'{p}[{i}]')
        rec(d.get('fields', {}))
check(n == 706 and bad_json == 0 and not bad_status, f'{n} product JSON files parse; invalid {bad_json}; statuses outside the allowed list {bad_status[:3]}; per class {classes}')

d = json.load(open(LONG + os.path.normpath(os.path.join(C, REQ[11])), encoding='utf-8'))
check(d['fields']['pour_point']['value'] == -53, 'Dimer C12 pour point is -53 °C')
for prod, ash, zn, s in (('CV1100', 7, 0.778, 2.35), ('CV3515', 10, 0.772, 2.4)):
    F = json.load(open(f'Products_json/Additive_packages_json/Lubrizol/LUBRIZOL_{prod}/tier2_numeric_contribution.json', encoding='utf-8'))['fields']
    check((F['sulfated_ash']['value'], F['sulfated_ash']['status'], F['elements']['Zn']['value'], F['elements']['S']['value']) == (ash, 'Reported', zn, s),
          f'{prod}: sulfated ash {ash} Reported, Zn {zn}, S {s}')

with tempfile.TemporaryDirectory() as tmp:
    out = os.path.join(tmp, 'cm.xlsx')
    r = subprocess.run([sys.executable, 'build_coverage_matrix.py', '--output', out], capture_output=True, text=True, encoding='utf-8')
    check(r.returncode == 0, 'coverage rebuild ran: ' + (r.stdout.splitlines() or [''])[0][:220])
    from openpyxl import load_workbook
    def rows_of(p):
        wb = load_workbook(p, read_only=True)
        try:
            return {s: [tuple(x) for x in wb[s].iter_rows(values_only=True)] for s in wb.sheetnames}
        finally:
            wb.close()
    check(rows_of(out) == rows_of('Coverage_Matrix.xlsx'), 'coverage rebuild equals the committed Coverage_Matrix.xlsx (all sheets, all cells)')
print('\nOVERALL:', 'ALL CHECKS PASSED' if not fails else f'{len(fails)} FAILED')
sys.exit(1 if fails else 0)
