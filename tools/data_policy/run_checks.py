"""Run the Workstream A pipeline and every required check; save each command's real return code and full output.

Each step runs as its own subprocess (no shell, no pipes), so the recorded return code is the command's own. For every
step the runner writes docs/data_policy_mandatory_review/test_results/NN_<name>.txt (command, return code, duration,
full stdout and stderr) and, at the end, summary.md and summary.json.

Expectations per step:
  zero              passes only with return code 0 (and the required text, if any, in its output)
  by_design_nonzero a documented, expected failure (verify_revision.py compares with the v5 commit 545fd3d, whose
                    protected files have since changed); reported as "expected failure", never as a pass
The overall result is PASS only if every required step met its expectation and no step failed to run.
Expected-incomplete verification (unavailable evidence, pending decisions) is reported by the review tools in their
output; it is not an execution failure.

Usage: python tools/data_policy/run_checks.py [--out-dir docs/data_policy_mandatory_review/test_results]
"""
import argparse, datetime, json, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = sys.executable
BASELINE = 'f4d97e71f72598df601b72403775581c34061ad1'
PROTECTED = ['Manual + Data to share.zip', 'json_templates', 'Property_Glossary.docx', 'reconciliation', 'source_registry.json',
             'tools/audit', 'tools/corrections_2026-10-31', 'tools/integration_2026-10-24', 'tools/maintenance_2026-10-31',
             'docs/audit_review_2026-11-02', 'analysis/association_mining']
NO_CACHE = ':(exclude,glob)**/__pycache__/**'  # bytecode caches written by test runs are not content
ALLOWED_STATUS = {'Reported', 'Calculated', 'Missing', 'Not Required', 'N/A', 'Not Applicable'}

STEPS = [  # (name, argv or builtin, expectation, required text in the output)
    ('document_classes', ['tools/data_policy/document_classes.py'], 'zero', None),
    ('source_selection_dry_run', ['tools/data_policy/source_selection.py'], 'zero', r'0 to apply; files to write \(selections, notes, open questions, product blocks\): 0'),
    ('tds_sds_inventory', ['tools/data_policy/tds_sds_inventory.py'], 'zero', None),
    ('source_coverage_ledger', ['tools/data_policy/source_coverage_ledger.py'], 'zero', None),
    ('association_review', ['tools/data_policy/association_review.py'], 'zero', None),
    ('lead_review', ['tools/data_policy/lead_review.py'], 'zero', None),
    ('external_review', ['tools/data_policy/external_review.py'], 'zero', None),
    ('source_review_status', ['tools/data_policy/source_review_status.py'], 'zero', None),
    ('treat_rate_basis_scan', ['tools/mandatory_properties/treat_rate_basis_scan.py'], 'zero', None),
    ('co_component_evidence_scan', ['tools/mandatory_properties/co_component_evidence_scan.py'], 'zero', None),
    ('build_eligibility', ['tools/mandatory_properties/build_eligibility.py'], 'zero', None),
    ('build_eligibility_check', ['tools/mandatory_properties/build_eligibility.py', '--check'], 'zero', None),
    ('coverage_matrix', ['build_coverage_matrix.py', '--output', 'Coverage_Matrix.xlsx', '--overwrite'], 'zero', None),
    ('integrate_products_dry_run', ['integrate_products.py'], 'zero', None),
    ('integration_diff_changed', ['tools/data_policy/integration_diff.py', '--changed', '--against', BASELINE], 'zero', r'NEW \(absent at '),
    ('verify_preserved', ['tools/data_policy/verify_preserved.py', '--out', 'docs/data_policy_mandatory_review/test_results/preserved_and_evidence.csv'], 'zero', None),
    ('protected_paths', 'builtin_protected', 'zero', None),
    ('product_json_valid', 'builtin_json', 'zero', None),
    ('tests_mandatory_properties', ['-m', 'unittest', 'discover', '-s', 'tools/mandatory_properties/tests', '-v'], 'zero', r'\nOK'),
    ('tests_data_policy', ['-m', 'unittest', 'discover', '-s', 'tools/data_policy/tests', '-v'], 'zero', r'\nOK'),
    ('tests_audit_v5', ['-m', 'unittest', 'discover', '-s', 'tools/audit/review_2026-11-02/tests', '-v'], 'zero', r'\nOK'),
    ('verify_revision_v5', ['tools/audit/review_2026-11-02/verify_revision.py'], 'by_design_nonzero', None),
]


def builtin_protected():
    out, rc = [], 0
    r = subprocess.run(['git', 'diff', '--name-only', BASELINE, '--', *PROTECTED, NO_CACHE], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    out.append(f'$ git diff --name-only {BASELINE} -- <protected paths>  (return code {r.returncode})')
    out.append(r.stdout.strip() or '(no differences)')
    if r.returncode != 0 or r.stdout.strip():
        rc = 1
    u = subprocess.run(['git', 'status', '--porcelain', '--', *PROTECTED, NO_CACHE], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    out.append(f'$ git status --porcelain -- <protected paths>  (return code {u.returncode})')
    out.append(u.stdout.strip() or '(clean)')
    if u.returncode != 0 or u.stdout.strip():
        rc = 1
    exists = os.path.exists(os.path.join(ROOT, 'analysis', 'association_mining'))
    out.append(f'analysis/association_mining exists on this branch: {exists}')
    return rc, '\n'.join(out), ''


def builtin_json():
    bad, n = [], 0
    for dp, _, fs in os.walk(os.path.join(ROOT, 'Products_json')):
        for f in fs:
            if not f.endswith('.json'):
                continue
            n += 1
            p = os.path.join(dp, f)
            try:
                with open(p, encoding='utf-8') as fh:
                    d = json.load(fh)
            except Exception as e:  # noqa: BLE001 - every parse failure is reported
                bad.append(f'{os.path.relpath(p, ROOT)}: invalid JSON ({e})'); continue

            def walk(x, path):
                if isinstance(x, dict):
                    if 'status' in x and isinstance(x['status'], str) and ('value' in x or 'source' in x) and x['status'] not in ALLOWED_STATUS:
                        bad.append(f'{os.path.relpath(p, ROOT)}: {path}.status = {x["status"]!r}')
                    for k, v in x.items():
                        walk(v, f'{path}.{k}')
                elif isinstance(x, list):
                    for i, v in enumerate(x):
                        walk(v, f'{path}[{i}]')
            walk(d.get('fields', {}), 'fields')
    return (1 if bad else 0), f'{n} product JSON files parsed; status values outside {sorted(ALLOWED_STATUS)}: {len(bad)}\n' + '\n'.join(bad), ''


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', default=os.path.join(ROOT, 'docs', 'data_policy_mandatory_review', 'test_results'))
    a = ap.parse_args(argv)
    os.makedirs(a.out_dir, exist_ok=True)
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    results = []
    for i, (name, cmd, expect, need) in enumerate(STEPS, 1):
        t0 = time.time()
        try:
            if cmd == 'builtin_protected':
                rc, so, se = builtin_protected(); shown = 'builtin: git diff of protected paths against the baseline'
            elif cmd == 'builtin_json':
                rc, so, se = builtin_json(); shown = 'builtin: parse every product JSON and check status values'
            else:
                full = [PY, *cmd]
                shown = ' '.join(full)
                r = subprocess.run(full, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env, timeout=1800)
                rc, so, se = r.returncode, r.stdout, r.stderr
            ran = True
        except Exception as e:  # noqa: BLE001 - a step that cannot run is an execution failure
            rc, so, se, ran = None, '', f'could not run: {e!r}', False
        dt = time.time() - t0
        text_ok = need is None or bool(re.search(need, so + se))
        if not ran:
            verdict = 'NOT RUN (execution failure)'
        elif expect == 'zero':
            verdict = 'pass' if rc == 0 and text_ok else ('FAIL' if rc != 0 else 'FAIL (required output not found)')
        else:
            verdict = 'expected failure (by design)' if rc not in (0, None) else 'UNEXPECTED PASS (review the by-design note)'
        fn = f'{i:02d}_{name}.txt'
        with open(os.path.join(a.out_dir, fn), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(f'command: {shown}\ncwd: {ROOT}\nHEAD: {head}\nreturn code: {rc}\nexpectation: {expect}'
                     f'{" + output matches " + repr(need) if need else ""}\nverdict: {verdict}\nduration: {dt:.1f} s\n\n'
                     f'===== stdout =====\n{so}\n===== stderr =====\n{se}\n')
        results.append(dict(step=i, name=name, command=shown, expectation=expect, return_code=rc, verdict=verdict, file=fn, seconds=round(dt, 1)))
        print(f'{i:02d} {name}: rc={rc} {verdict}', flush=True)
    ok = all(r['verdict'] in ('pass', 'expected failure (by design)') for r in results)
    overall = 'PASS' if ok else 'FAIL'
    stamp = datetime.datetime.now().isoformat(timespec='seconds')
    with open(os.path.join(a.out_dir, 'summary.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(dict(run_at=stamp, head=head, overall=overall, steps=results), fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    lines = [f'# Check run summary', '', f'Run {stamp} at HEAD `{head}` (plus the uncommitted working tree), Python {sys.version.split()[0]}.',
             f'Generated by `python tools/data_policy/run_checks.py`; each step is a separate subprocess and its return code is its own.', '',
             f'**Overall: {overall}** (every required step met its expectation)' if ok else f'**Overall: {overall}**', '',
             '| # | Step | Return code | Expectation | Verdict | Output |', '|---:|---|---:|---|---|---|']
    lines += [f'| {r["step"]} | {r["name"]} | {r["return_code"]} | {r["expectation"]} | {r["verdict"]} | [{r["file"]}]({r["file"]}) |' for r in results]
    lines += ['', 'Expected-incomplete verification is not an execution failure: unavailable external sources, insufficient archive '
              'evidence and pending decisions are reported inside the review steps (external_review, lead_review, '
              'source_review_status) while those steps return 0. `verify_revision_v5` fails by design: it compares the protected '
              'files with the v5 commit `545fd3d`, and product JSON and the workbook have changed since.', '']
    with open(os.path.join(a.out_dir, 'summary.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines))
    print(f'overall: {overall}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
