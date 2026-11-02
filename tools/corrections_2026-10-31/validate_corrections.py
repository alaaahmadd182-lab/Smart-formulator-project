#!/usr/bin/env python3
"""Read-only validation of the 2026-10-31 source-backed corrections (CF-136, CF-142, CF-143, CF-159, CF-180).

Usage:
  python validate_corrections.py --repo <repository> --archive <"Manual + Data to share.zip"> [--base e6617ca]

Checks the working tree of --repo against --base: the five product JSON edits, the curated log, the correction log,
the regenerated coverage workbook and the unchanged audit snapshot and evidence. Writes nothing to the repository
(temporary files go to the system temp folder). Exit codes: 0 all checks passed; 1 a check failed; 2 a prerequisite
is missing. Checks that need a person (image-only pages) are listed separately under MANUAL and do not affect the
exit code.
"""
import argparse, copy, hashlib, importlib.util, io, json, os, subprocess, sys, tempfile, zipfile

sys.stdout.reconfigure(encoding='utf-8')
FAILS = []
JSON_EDITS = {
    'Products_json/Base_oils_json/CHEVRON/CHEVRON_SYNFLUID_DIMER_C12/CHEVRON_SYNFLUID_DIMER_C12__base_oil_tier2_verification.json': {'.fields.pour_point'},
    'Products_json/Additive_packages_json/Lubrizol/LUBRIZOL_CV1100/tier2_numeric_contribution.json': {'.fields.sulfated_ash', '.fields.elements.Zn', '.fields.elements.S'},
    'Products_json/Additive_packages_json/Lubrizol/LUBRIZOL_CV3515/tier2_numeric_contribution.json': {'.fields.sulfated_ash', '.fields.elements.Zn', '.fields.elements.S'},
    'Products_json/Additive_packages_json/Richful/RICHFUL_RF6066/tier2_numeric_contribution.json': {'.conflicts[1].note'},
    'Products_json/Additive_packages_json/Richful/RICHFUL_RF6078/tier1_route_defining.json': {'.conflicts[0].final_resolution'},
}
LOG = 'reconciliation/comprehensive_conflicts_audit_corrections_2026-10-31.md'
SUPPORT = {'open_questions_and_conflicts.md', 'Coverage_Matrix.xlsx', LOG}
UNCHANGED = ['reconciliation/comprehensive_conflicts_audit.md', 'reconciliation/comprehensive_conflicts_audit.csv',
             'reconciliation/audit_evidence', 'json_templates', 'integrate_products.py', 'build_coverage_matrix.py',
             'build_conflicts_report.py', 'source_registry.json']
ALLOWED = {'Reported', 'Calculated', 'Missing', 'Not Required', 'N/A', 'Not Applicable'}
EXPECTED_CELLS = {('LUBRIZOL_CV1100', c, 'calculated' if c == 'sulfated_ash' else 'missing', 'reported') for c in ('sulfated_ash', 'elements.Zn', 'elements.S')} | \
                 {('LUBRIZOL_CV3515', c, 'calculated' if c == 'sulfated_ash' else 'missing', 'reported') for c in ('sulfated_ash', 'elements.Zn', 'elements.S')}
SRC = [  # (archive file, page, printed text that must appear, whitespace collapsed)
    ('DL2-13202.pdf', 1, ['Pour Point, °F, °C', '-53 (-63)', 'Revision Date April 2011', '362 (183)', '396 (202)']),
    ('DL2-13200.pdf', 1, ['Pour Point, °C (°F)', '-53 (-63)']),
    ('DL2-11503.pdf', 1, ['Minimum % Weight Typical Maximum % Weight', 'PHOSPHORUS']),
    ('DL2-11503.pdf', 2, ['SULFATED ASH 7', 'SULFUR 2.35', 'ZINC 0.700 0.778 0.856']),
    ('DL2-11503.pdf', 3, ['Effective: 11/8/2017']),
    ('DL2-15722.pdf', 1, ['Minimum % Weight Typical Maximum % Weight', 'PHOSPHORUS']),
    ('DL2-15722.pdf', 2, ['SULFATED ASH 10', 'SULFUR 2.4', 'ZINC 0.695 0.772 0.850']),
    ('DL2-15722.pdf', 3, ['Effective: 10/9/2017']),
    ('DL2-15832.pdf', 1, ['ACEA E7/API CI-4 10W-30, 10W-40, 15W-40, 20W-50 11.85% API CI-4 10W-30, 10W-40, 15W-40, 20W-50 10.85%']),
    ('RF6078%20-%20TDS.pdf', 1, ['ACEA E7/API CI-4 10W-30, 10W-40, 15W-40, 20W-50 10.85% API CI-4 Plus 10W-30, 10W-40, 15W-40, 20W-50 11.85%']),
]
MANUAL = [
    'DL2-15831.pdf p.5 (RF6066 SDS, image/vector text, nothing extractable): confirm "Viscosity, kinematic : Not available" '
    'and "Viscosity, dynamic : 185 mm²/s (100 °C)" from the page image (CF-159).',
    'DL2-11503.pdf / DL2-15722.pdf: the p.2 values sit in the Typical column. Word x-coordinates were checked during '
    'review (Typical x=347, Minimum x=236, Maximum x=442); this script checks the row text and the p.1 header only.',
    'Chevron Phillips Synfluid Dimer C12 sheet (revision June 2012) in reconciliation/audit_evidence: "Pour Point, °C (°F) '
    'ASTM D5950 -53 (-63)" (hash recorded in evidence_manifest.md; byte identity checked here, content not).',
]


def check(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg)
    if not cond:
        FAILS.append(msg)


def need(cond, msg):
    if not cond:
        print('PREREQUISITE MISSING: ' + msg)
        sys.exit(2)


def git(*args, binary=False):
    r = subprocess.run(['git', '-C', REPO, *args], capture_output=True)
    need(r.returncode == 0, f'git {" ".join(args)} failed: {r.stderr.decode(errors="replace").strip()}')
    return r.stdout if binary else r.stdout.decode('utf-8')


def long(p):
    p = os.path.normpath(os.path.abspath(p))
    return '\\\\?\\' + p if os.name == 'nt' and not p.startswith('\\\\?\\') else p


def rd(rel, mode='r'):
    with open(long(os.path.join(REPO, rel)), 'rb' if mode == 'rb' else 'r', **({} if mode == 'rb' else {'encoding': 'utf-8', 'newline': ''})) as f:
        return f.read()


def leaves(n, p=''):
    if isinstance(n, dict):
        for k, v in n.items(): yield from leaves(v, f'{p}.{k}')
    elif isinstance(n, list):
        for i, v in enumerate(n): yield from leaves(v, f'{p}[{i}]')
    else:
        yield p, n


def value_objects(n, p=''):
    if isinstance(n, dict):
        if 'status' in n and 'value' in n and not isinstance(n['status'], dict):
            yield p, n
        for k, v in n.items(): yield from value_objects(v, f'{p}.{k}')
    elif isinstance(n, list):
        for i, v in enumerate(n): yield from value_objects(v, f'{p}[{i}]')


def ash_counts(docs):
    sel = alt = rep = 0
    for d in docs:
        sa = d.get('fields', {}).get('sulfated_ash')
        if isinstance(sa, dict):
            sel += sa.get('status') == 'Calculated'; rep += sa.get('status') == 'Reported'
            alt += sum(a.get('status') == 'Calculated' for a in sa.get('alternate_entries') or [])
    return sel, alt, rep


def main():
    global REPO
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--repo', required=True, help='repository root (working tree to validate)')
    ap.add_argument('--archive', required=True, help='path to "Manual + Data to share.zip"')
    ap.add_argument('--base', default='e6617ca', help='base commit (default: e6617ca)')
    a = ap.parse_args()
    REPO = os.path.abspath(a.repo)
    need(os.path.isdir(os.path.join(REPO, '.git')) or os.path.isfile(os.path.join(REPO, '.git')), f'not a git repository: {REPO}')
    need(os.path.isfile(a.archive), f'source archive not found: {a.archive}')
    for mod in ('pymupdf', 'openpyxl'):
        need(importlib.util.find_spec(mod) is not None, f'Python package {mod} is not installed')
    for f in ('integrate_products.py', 'build_coverage_matrix.py', 'source_registry.json'):
        need(os.path.isfile(os.path.join(REPO, f)), f'{f} not found in the repository')
    need(subprocess.run(['git', '-C', REPO, 'cat-file', '-e', a.base + '^{commit}'], capture_output=True).returncode == 0, f'base commit {a.base} not found')
    import pymupdf
    from openpyxl import load_workbook
    sys.path.insert(0, REPO)
    import integrate_products as I
    base = a.base
    head = lambda f: json.loads(git('show', f'{base}:{f}'))

    print(f'Repository {REPO}\nBranch {git("branch", "--show-current").strip()}; HEAD {git("rev-parse", "--short", "HEAD").strip()}; base {base}')

    print('\n== 1. Changed files ==')
    changed = set(git('diff', base, '--name-only').split('\n')) - {''}
    untracked = set(git('ls-files', '--others', '--exclude-standard').split('\n')) - {''}
    check(changed | untracked == set(JSON_EDITS) | SUPPORT,
          f'changed + untracked = expected 5 JSON + 3 supporting files; unexpected {sorted((changed | untracked) - set(JSON_EDITS) - SUPPORT)}, missing {sorted(set(JSON_EDITS) | SUPPORT - changed - untracked)}')
    for p in UNCHANGED:
        check(git('diff', base, '--stat', '--', p).strip() == '' and not any(u.startswith(p) for u in untracked), f'unchanged vs {base}: {p}')

    print('\n== 2. Product JSON: validity, statuses, sources, ranges, formatting, scope of change ==')
    for f, scope in JSON_EDITS.items():
        prod = f.split('/')[-2]; raw = rd(f); d = json.loads(raw)
        vos = list(value_objects(d.get('fields', {})))
        bad = [p for p, n in vos if n['status'] not in ALLOWED]
        nosrc = [p for p, n in vos if n['status'] == 'Reported' and not ((n.get('source') or {}).get('file') if isinstance(n.get('source'), dict) else n.get('source'))]
        rng = [p for p, n in vos if all(isinstance(n.get(k), (int, float)) for k in ('min', 'max', 'value')) and not n['min'] <= n['value'] <= n['max']]
        check(not (bad or nosrc or rng), f'{prod}: valid JSON, {len(vos)} value objects; bad status {bad}; Reported without source {nosrc}; out of range {rng}')
        tail = '\n' if raw.endswith('\n') else ''
        check((json.dumps(d, ensure_ascii=False, indent=2) + tail).replace('\n', '\r\n' if '\r\n' in raw else '\n') == raw, f'{prod}: formatting preserved (indent 2, line endings, final newline as before)')
        A, B = dict(leaves(head(f))), dict(leaves(d))
        diff = {k for k in set(A) | set(B) if A.get(k, '<absent>') != B.get(k, '<absent>')}
        out = sorted(k for k in diff if not any(k == e or k.startswith(e + '.') or k.startswith(e + '[') for e in scope))
        check(diff and not out, f'{prod}: {len(diff)} changed leaves, all inside {sorted(scope)}; outside {out}')

    print('\n== 3. Derived *_final keys match integrate_products.normalise; no new integration gaps ==')
    for f, scope in JSON_EDITS.items():
        prod = f.split('/')[-2]; d = json.loads(rd(f))
        for p, n in value_objects(d.get('fields', {})):
            if '.fields' + p not in scope:
                continue
            m = copy.deepcopy(n); I.normalise(m, p.lstrip('.'))
            mine, theirs = ({k: x[k] for k in I.OWN_KEYS if k in x} for x in (n, m))
            check(mine == theirs, f'{prod}{p}: {mine}')
            for alt in n.get('alternate_entries') or []:
                check(not any(k in alt for k in I.OWN_KEYS), f'{prod}{p}: historical alternate {alt["value"]} has no *_final keys')
        gaps = []
        for doc in (head(f), d):
            n = copy.deepcopy(doc); I.walk(n.get('fields', {}), '', {})
            gaps.append(sorted(set(dict(leaves(n))) ^ set(dict(leaves(doc)))))
        check(gaps[0] == gaps[1], f'{prod}: integration dry-run gaps identical before and after ({len(gaps[1])}, pre-existing)')

    print('\n== 4. Printed text in the source PDFs ==')
    Z = zipfile.ZipFile(a.archive)
    names = {os.path.basename(n).replace('�', '%'): n for n in Z.namelist()}
    for file, page, needles in SRC:
        if file not in names:
            check(False, f'{file} not found in the archive'); continue
        text = ' '.join(pymupdf.open(stream=Z.read(names[file]), filetype='pdf')[page - 1].get_text().split())
        for s in needles:
            check(s in text, f'{file} p.{page}: "{s}"')

    print('\n== 5. Conflict history ==')
    for f, i, key in (('Products_json/Additive_packages_json/Richful/RICHFUL_RF6066/tier2_numeric_contribution.json', 1, 'note'),
                      ('Products_json/Additive_packages_json/Richful/RICHFUL_RF6078/tier1_route_defining.json', 0, 'final_resolution')):
        old, new = head(f)['conflicts'][i], json.loads(rd(f))['conflicts'][i]
        check(new[key].startswith(old[key] + ' [Review 2026-10-31') and new['resolved'] is False and old['values'] == new['values'] and
              {k: v for k, v in old.items() if k != key} == {k: v for k, v in new.items() if k != key},
              f'{f.split("/")[-2]} conflicts[{i}]: original {key} kept as prefix, review note appended, values and other keys unchanged, resolved=false')

    print('\n== 6. Curated log (open_questions_and_conflicts.md) ==')
    old = git('show', f'{base}:open_questions_and_conflicts.md').replace('\r\n', '\n').split('\n')
    new = rd('open_questions_and_conflicts.md').replace('\r\n', '\n').split('\n')
    new_set = set(new)
    lost = [l for l in old if l not in new_set and not any(n.startswith(l.rstrip()) for n in new)]
    check(not lost, f'every original line kept verbatim or as the prefix of an extended line; lost {len(lost)}')
    note66 = json.loads(rd('Products_json/Additive_packages_json/Richful/RICHFUL_RF6066/tier2_numeric_contribution.json'))['conflicts'][1]['note']
    check(any(l.startswith('- **Conflict (tier2)**') and '`tier2.kv100`' in l and l.endswith(note66) for l in new), 'RF6066 kv100 conflict line mirrors the JSON note')
    for tag in ('audit CF-136', 'audit CF-142', 'audit CF-143', 'audit CF-180', 'Checked 2026-10-31 (audit CF-180)', LOG.split('/')[-1]):
        check(any(tag in l for l in new), f'curated log mentions "{tag}"')
    check(sum(l.count('Not resolved.') for l in new) == sum(l.count('Not resolved.') for l in old), 'number of "Not resolved." conflict statements unchanged')

    print('\n== 7. Correction log ==')
    log = rd(LOG)
    for cf in ('CF-136', 'CF-142', 'CF-143', 'CF-159', 'CF-180', 'CF-144'):
        check(cf in log, f'{LOG} references {cf}')

    print('\n== 8. CF-144 count: selected estimates vs historical alternates ==')
    base_docs = [json.loads(git('show', f'{base}:{n}')) for n in git('ls-tree', '-r', '--name-only', base, 'Products_json').split('\n') if n.endswith('.json')]
    now_docs = []
    for dp, _, fs in os.walk(long(os.path.join(REPO, 'Products_json'))):
        now_docs += [json.load(open(os.path.join(dp, x), encoding='utf-8')) for x in fs if x.endswith('.json')]
    cb, cn = ash_counts(base_docs), ash_counts(now_docs)
    print(f'INFO {base}: selected Calculated {cb[0]}, historical alternates {cb[1]}, Reported {cb[2]}; now: {cn[0]}, {cn[1]}, {cn[2]}')
    check(cb == (26, 0, 34) and cn == (24, 2, 36), 'CF-144: 26 -> 24 selected estimates; 0 -> 2 historical alternates; 34 -> 36 Reported')
    check(len(base_docs) == len(now_docs), f'JSON file count unchanged ({len(now_docs)})')

    print('\n== 9. Coverage workbook ==')
    src = open(os.path.join(REPO, 'build_coverage_matrix.py'), encoding='utf-8').read()
    check("return str(node.get('status')).strip()" in src and src.count("get('status_final')") == 0, 'build_coverage_matrix.py reads status, never status_final')
    check(not any('status_final' in dict(leaves(d)) or any(k.endswith('.status_final') for k in dict(leaves(d))) for d in now_docs), 'no product JSON carries status_final')
    with tempfile.TemporaryDirectory() as tmp:
        fresh = os.path.join(tmp, 'fresh.xlsx'); basewb = os.path.join(tmp, 'base.xlsx')
        r = subprocess.run([sys.executable, 'build_coverage_matrix.py', '--output', fresh], cwd=REPO, capture_output=True, text=True, encoding='utf-8')
        check(r.returncode == 0, 'coverage rebuild from the working tree ran')
        open(basewb, 'wb').write(git('show', f'{base}:Coverage_Matrix.xlsx', binary=True))
        def rows(p):
            wb = load_workbook(p, read_only=True)
            try:
                return {s: [tuple(x) for x in wb[s].iter_rows(values_only=True)] for s in wb.sheetnames}
            finally:
                wb.close()
        W, F, Bw = rows(os.path.join(REPO, 'Coverage_Matrix.xlsx')), rows(fresh), rows(basewb)
        check(W == F, 'repository Coverage_Matrix.xlsx equals a fresh rebuild from the working tree (all sheets, all cells)')
        check(W['Overview'][1][1:3] == Bw['Overview'][1][1:3] == (264, 706), f'products and JSON files unchanged: {W["Overview"][1][1:3]}')
        check([r[:2] for r in W['Overview'][4:7]] == [r[:2] for r in Bw['Overview'][4:7]], f'class product counts unchanged: {[r[:2] for r in W["Overview"][4:7]]}')
        for s in ('Base Oils', 'Additive Components', 'Validation Issues', 'Traceability Audit'):
            check(W[s] == Bw[s], f'sheet unchanged: {s}')
        hdr = W['Additive Packages'][0]
        cells = {(w[0], hdr[j], b[j], w[j]) for w, b in zip(W['Additive Packages'], Bw['Additive Packages']) for j in range(len(w)) if w[j] != b[j]}
        check(len(W['Additive Packages']) == len(Bw['Additive Packages']) and cells == EXPECTED_CELLS,
              f'Additive Packages: exactly 6 cells changed: {sorted(cells)}')
        ov = {r[0]: r for r in W['Overview']}; ob = {r[0]: r for r in Bw['Overview']}
        check((ob['Additive Packages'][2:5], ov['Additive Packages'][2:5]) == ((1004, 26, 764), (1010, 24, 760)), 'Overview Additive Packages: Reported 1004->1010, Calculated 26->24, Missing/N.A. 764->760')
        check((ob['Status Detail rows'][1], ov['Status Detail rows'][1]) == (6318, 6320), 'Overview Status Detail rows 6318 -> 6320 (two nested historical alternates)')
        sd_b, sd_w = set(Bw['Status Detail']), set(W['Status Detail'])
        added, removed = sd_w - sd_b, sd_b - sd_w
        check(len(added) == 9 and len(removed) == 7 and {r[1] for r in added | removed} == {'LUBRIZOL_CV1100', 'LUBRIZOL_CV3515', 'CHEVRON_SYNFLUID_DIMER_C12'},
              f'Status Detail: {len(removed)} rows replaced by {len(added)}, only CV1100, CV3515 and Dimer C12')

    print('\n== 10. SHA-256 of changed files ==')
    for f in sorted(set(JSON_EDITS) | SUPPORT):
        print(hashlib.sha256(rd(f, 'rb')).hexdigest(), f)

    print('\n== MANUAL (not checked by this script; do not affect the exit code) ==')
    for m in MANUAL:
        print('MANUAL ' + m)
    print(f'\nOVERALL: {"ALL AUTOMATED CHECKS PASSED" if not FAILS else f"{len(FAILS)} CHECK(S) FAILED"}')
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
