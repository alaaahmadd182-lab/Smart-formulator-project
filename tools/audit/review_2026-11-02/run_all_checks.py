"""Run every automated check of the 2026-11-02 audit review and save the output.

Writes one text file per check to docs/audit_review_2026-11-02/verification_results/ and prints two separate results:

  EXECUTION              whether every required check ran and passed (the version-4 report check is informational: it
                         documents the inconsistencies that version 5 corrects, so it is expected to fail);
  VERIFICATION COMPLETE  whether every source in the citation ledger is fully verified. A run can succeed while the
                         verification is incomplete; the unresolved sources are then listed.

Usage: python tools/audit/review_2026-11-02/run_all_checks.py
Exit codes: 0 every required check passed and the verification is complete;
            3 every required check passed but the verification is incomplete (unresolved sources listed);
            1 a required check failed.
"""
import json, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import review_lib as R

T = os.path.join('tools', 'audit', 'review_2026-11-02')
OUT = os.path.join(R.ROOT, 'docs', 'audit_review_2026-11-02', 'verification_results')
V5 = os.path.join(T, 'output', 'findings_v5.json')


def run(name, args, required=True, ok_codes=(0,)):
    r = subprocess.run([sys.executable] + args, cwd=R.ROOT, capture_output=True, text=True, encoding='utf-8')
    text = f'$ python {" ".join(args)}\nexit code: {r.returncode}\n\n{r.stdout}{r.stderr}'
    open(os.path.join(OUT, name + '.txt'), 'w', encoding='utf-8', newline='\n').write(text)
    good = r.returncode in ok_codes
    if good:
        status = 'PASS' if r.returncode == 0 else f'RAN (exit {r.returncode})'
    else:
        status = 'FAIL' if required else 'FAIL (informational, expected)'
    print(f'{status:32s} {name}')
    return good or not required


def main():
    os.makedirs(OUT, exist_ok=True)
    ok = True
    ok &= run('01_revise_findings', [os.path.join(T, 'revise_findings.py')])
    # the citation-level verification feeds section 4 of the report, so it runs before the report is generated
    ok &= run('02_check_sources_v5', [os.path.join(T, 'check_sources.py'), '--findings', V5, '--out', os.path.join(OUT, 'source_checks_v5.csv')])
    ok &= run('03_check_columns_v5', [os.path.join(T, 'check_columns.py'), '--findings', V5,
                                      '--out', os.path.join(OUT, 'column_checked_citations.json')])
    ok &= run('04_afton_matrices', [os.path.join(T, 'afton_matrices.py')])
    ok &= run('05_build_association_review', [os.path.join(T, 'build_association_review.py')])
    # exit 3 = the ledger ran and found sources that are not fully verified: execution succeeded, verification incomplete
    ok &= run('06_verification_ledger', [os.path.join(T, 'verification_ledger.py')], ok_codes=(0, 3))
    with tempfile.TemporaryDirectory() as tmp:
        ok &= run('07_generate_report_v5', [os.path.join(T, 'gen_report_v5.py'), '--outdir', tmp])
        same = all(open(os.path.join(tmp, f), encoding='utf-8-sig').read() ==
                   open(os.path.join(R.ROOT, 'reconciliation', f), encoding='utf-8-sig').read().replace('\r\n', '\n')
                   for f in ('comprehensive_conflicts_audit.md', 'comprehensive_conflicts_audit.csv'))
        open(os.path.join(OUT, '08_regeneration_identical.txt'), 'w', encoding='utf-8', newline='\n').write(
            'Regenerated version-5 report and CSV equal the files in reconciliation/ (line endings normalised): ' + str(same) + '\n')
        print(f'{"PASS" if same else "FAIL":32s} 08_regeneration_identical')
        ok &= same
    ok &= run('09_check_report_v5', [os.path.join(T, 'check_report.py')])
    v4 = tempfile.mkdtemp()
    for f in ('comprehensive_conflicts_audit.md', 'comprehensive_conflicts_audit.csv'):
        open(os.path.join(v4, f), 'w', encoding='utf-8', newline='').write(R.git_show(R.SNAPSHOT_COMMIT, 'reconciliation/' + f))
    run('10_check_report_v4_snapshot', [os.path.join(T, 'check_report.py'), '--md', os.path.join(v4, 'comprehensive_conflicts_audit.md'),
                                        '--csv', os.path.join(v4, 'comprehensive_conflicts_audit.csv')], required=False)
    ok &= run('11_verify_revision_and_protected_files', [os.path.join(T, 'verify_revision.py')])
    ok &= run('12_regression_tests', ['-m', 'unittest', 'discover', '-s', os.path.join(T, 'tests'), '-v'])
    S = json.load(open(os.path.join(OUT, 'ledger_summary.json'), encoding='utf-8'))
    print()
    print('EXECUTION:', 'ALL REQUIRED CHECKS RAN SUCCESSFULLY' if ok else 'A REQUIRED CHECK FAILED')
    if S['complete']:
        print(f"VERIFICATION COMPLETE: YES (all {S['total']} sources fully verified or not used as evidence)")
    else:
        print(f"VERIFICATION COMPLETE: NO, INCOMPLETE: {S['E']} unresolved and {S['D']} text-presence-only of {S['total']} sources")
        for u in S['unresolved']:
            print(f"  unresolved: {u['id']} {u['source']}")
    return 1 if not ok else (0 if S['complete'] else 3)


if __name__ == '__main__':
    sys.exit(main())
