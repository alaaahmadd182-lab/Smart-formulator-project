"""Verify the version-5 revision and the protected files (read-only).

1. Every CSV cell that differs between version 4 (commit e6617ca) and the working-tree CSV is explained by a row of
   docs/audit_review_2026-11-02/finding_changes.csv (or is one of the two new columns); every declared change shows up.
2. The version-4 Markdown is preserved in Git history at e6617ca and differs from the working tree.
3. Protected files are byte-identical to HEAD of main at the start of the review (545fd3d): product JSON, templates,
   Coverage_Matrix.xlsx, the source ZIP, source_registry.json, scripts, the curated log and audit_evidence/.
4. The 11 saved evidence files match the SHA-256 hashes in evidence_manifest.md.

Usage: python tools/audit/review_2026-11-02/verify_revision.py [--base 545fd3d]
Exit codes: 0 all checks passed; 1 a check failed.
"""
import argparse, collections, csv, hashlib, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import review_lib as R

FIELD_COLS = {
    'group': {'finding_type', 'finding_type_definition'}, 'comparability': {'comparability'}, 'nature': {'nature'},
    'explanation': {'explanation'}, 'follow_up_category': {'follow_up_category'}, 'follow_up_reason': {'follow_up_reason'},
    'next_step': {'recommended_next_step'}, 'verification': {'verification_status', 'verification_level'},
    'verification_priority': {'verification_priority'}, 'values': {'source_documents_and_pages', 'units_and_conditions'},
}
PROTECTED = ['Products_json', 'json_templates', 'Coverage_Matrix.xlsx', 'Manual + Data to share.zip', 'source_registry.json',
             'open_questions_and_conflicts.md', 'reconciliation/audit_evidence', 'build_coverage_matrix.py', 'integrate_products.py',
             'build_conflicts_report.py', 'Property_Glossary.docx', 'Raw_Material_Missing_Properties_2026-10-13.xlsx', 'requirements.txt']


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--base', default='545fd3d'); a = ap.parse_args()
    fails = []
    def check(ok, msg):
        print(('PASS ' if ok else 'FAIL ') + msg)
        if not ok: fails.append(msg)

    old = {r['conflict_id']: r for r in R.read_csv(text=R.git_show(R.SNAPSHOT_COMMIT, 'reconciliation/comprehensive_conflicts_audit.csv'))}
    new = {r['conflict_id']: r for r in R.read_csv()}
    chg = list(csv.DictReader(open(os.path.join(R.ROOT, 'docs', 'audit_review_2026-11-02', 'finding_changes.csv'), encoding='utf-8-sig')))
    allowed = collections.defaultdict(set)
    for c in chg:
        allowed[c['id']] |= FIELD_COLS.get(c['field'].split('[')[0], set())
    check(list(old) == list(new), 'same 180 IDs in the same order')
    newcols = set(next(iter(new.values()))) - set(next(iter(old.values())))
    check(newcols == {'changed_in_v5', 'later_state_2026_10_31'}, f'new CSV columns are exactly {sorted(newcols)}')
    unexplained, seen = [], collections.defaultdict(set)
    for i in old:
        for col in old[i]:
            if old[i][col] != new[i][col]:
                seen[i].add(col)
                if col not in allowed[i]:
                    unexplained.append((i, col))
    check(not unexplained, f'every changed CSV cell is a declared change ({sum(len(v) for v in seen.values())} cells in {len(seen)} findings); unexplained: {unexplained[:5]}')
    missing = [(c['id'], c['field']) for c in chg if c['field'] != 'later_state' and not (FIELD_COLS[c['field'].split('[')[0]] & seen[c['id']])]
    check(not missing, f'every declared change appears in the CSV; missing: {missing[:5]}')
    check(all(new[i]['later_state_2026_10_31'] for i in ('CF-136', 'CF-142', 'CF-143', 'CF-144', 'CF-159', 'CF-180'))
          and sum(1 for r in new.values() if r['later_state_2026_10_31']) == 6, 'later-state column filled for exactly CF-136, 142, 143, 144, 159, 180')

    md_old = R.git_show(R.SNAPSHOT_COMMIT, 'reconciliation/comprehensive_conflicts_audit.md')
    md_new = open(R.REPORT_MD, encoding='utf-8').read().replace('\r\n', '\n')
    check('source-verification review and reporting corrections 2026-10-30 (this version)' in md_old and md_old != md_new
          and md_new.startswith('# Comprehensive conflicts audit') and '**Version 5 — revision of 2026-11-02 (current version).**' in md_new,
          'version 4 preserved at e6617ca; the working tree carries the dated version-5 header')

    # 2026-10-31 correction log: the ASTM D 5950 statement (CF-136)
    t13200 = R.Archive().pages('DL2-13200.pdf')[0]
    L = [l.strip() for l in t13200.splitlines()]
    i = L.index('Pour Point, °C (°F)')
    check(L[i + 1] == '-53 (-63)' and L[i + 6] == 'ASTM D 5950',
          'DL2-13200.pdf p.1: the pour-point row (C12 Dimer column -53 (-63)) prints ASTM D 5950 as its method')
    log = open(os.path.join(R.ROOT, 'reconciliation', 'comprehensive_conflicts_audit_corrections_2026-10-31.md'), encoding='utf-8').read()
    details = log.split('## Errata (2026-11-02)')[0]
    check('appears only in the 2012 sheet' not in details and 'ASTM D 5950 is printed for the pour-point row' in details
          and '## Errata (2026-11-02)' in log, 'correction log: the "only in the 2012 sheet" claim is corrected, with an errata entry')

    r = subprocess.run(['git', 'diff', '--name-only', a.base, '--'] + PROTECTED, cwd=R.ROOT, capture_output=True, text=True)
    r2 = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=all', '--'] + PROTECTED, cwd=R.ROOT, capture_output=True, text=True)
    check(r.returncode == 0 and not r.stdout.strip() and not r2.stdout.strip(),
          f'protected files unchanged against {a.base} (product JSON, templates, workbook, source ZIP, registry, curated log, evidence, scripts)'
          + (f': {r.stdout.split()[:5]} {r2.stdout.split()[:5]}' if r.stdout.strip() or r2.stdout.strip() else ''))
    man = open(os.path.join(R.EVIDENCE, 'evidence_manifest.md'), encoding='utf-8').read()
    saved = man.split('## Archive documents checked visually')[0]
    rows = {m.group(1): m.group(2) for m in re.finditer(r'^\| `([^`]+)` \|.*?\| `([0-9a-f]{64})` \|', saved, re.M)}
    ev = sorted(f for f in os.listdir(R.EVIDENCE) if f not in ('evidence_manifest.md', '.gitattributes'))
    check(len(ev) == 11 and set(ev) == set(rows), f'11 evidence files = the manifest rows ({len(ev)} files, {len(rows)} rows)')
    for f in ev:
        h = hashlib.sha256(open(os.path.join(R.EVIDENCE, f), 'rb').read()).hexdigest()
        check(h == rows.get(f), f'SHA-256 matches manifest: {f}')
    print('\nOVERALL:', 'PASS' if not fails else f'{len(fails)} FAILED')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
