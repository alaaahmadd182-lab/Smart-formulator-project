"""Build the review package of the 2026-11-02 audit review (outside the repository).

Contents: the version-5 report and CSV, the 2026-10-31 correction log, tools/, docs/audit_review_2026-11-02/ and the three
documentation files that point readers to version 5 (README.md, reconciliation/README.md, PROJECT_FILE_GUIDE.md), plus
REVIEW_PACKAGE_MANIFEST.txt with the SHA-256 of every file. Never included: .git, the source archive
"Manual + Data to share.zip", product data, evidence files, __pycache__.

Usage: python tools/audit/review_2026-11-02/make_review_zip.py OUTPUT.zip
Exit codes: 0 written; 1 the output exists or a forbidden file would be included.
"""
import hashlib, os, subprocess, sys, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import review_lib as R

FILES = ['reconciliation/comprehensive_conflicts_audit.md', 'reconciliation/comprehensive_conflicts_audit.csv',
         'reconciliation/comprehensive_conflicts_audit_corrections_2026-10-31.md', 'README.md', 'reconciliation/README.md',
         'PROJECT_FILE_GUIDE.md']
TREES = ['tools', 'docs/audit_review_2026-11-02']


def main():
    out = os.path.abspath(sys.argv[1])
    if os.path.exists(out):
        print('output exists:', out); return 1
    paths = list(FILES)
    for t in TREES:
        for dp, dns, fns in os.walk(os.path.join(R.ROOT, t)):
            dns[:] = [d for d in dns if d != '__pycache__']
            paths += [os.path.relpath(os.path.join(dp, f), R.ROOT).replace(os.sep, '/') for f in fns]
    paths = sorted(set(paths))
    bad = [p for p in paths if p.startswith(('.git', 'Products_json', 'reconciliation/audit_evidence')) or p.endswith('Manual + Data to share.zip')]
    if bad:
        print('forbidden files:', bad); return 1
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=R.ROOT, capture_output=True, text=True).stdout.strip()
    br = subprocess.run(['git', 'branch', '--show-current'], cwd=R.ROOT, capture_output=True, text=True).stdout.strip()
    lines = ['Smart Formulator: review package of the conflicts-audit documentation review (2026-11-02), version 5 of the report',
             f'Working tree of branch {br} on top of HEAD {head}; uncommitted. Excludes .git, the source archive, product data and evidence files.',
             'Start with docs/audit_review_2026-11-02/README.md. To re-run the checks, copy these files into the repository and run',
             'python tools/audit/review_2026-11-02/run_all_checks.py (needs the source archive and the repository).', '',
             'SHA-256  size  path']
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in paths:
            data = open(R.lp(os.path.join(R.ROOT, p)), 'rb').read()
            z.writestr(p, data)
            lines.append(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {p}')
        z.writestr('REVIEW_PACKAGE_MANIFEST.txt', '\n'.join(lines) + '\n')
    print(f'written {out}: {len(paths)} files + manifest, {os.path.getsize(out)} bytes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
