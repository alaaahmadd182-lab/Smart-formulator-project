"""Print every column of one or more findings from the audit CSV (read-only).

Usage:
    python tools/audit/review_2026-11-02/show_finding.py CF-031 CF-032 [--csv reconciliation/comprehensive_conflicts_audit.csv]
    python tools/audit/review_2026-11-02/show_finding.py --grep "DL2-13200"   (findings whose row contains the text)
"""
import argparse, csv, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

ap = argparse.ArgumentParser()
ap.add_argument('ids', nargs='*')
ap.add_argument('--csv', default=os.path.join(ROOT, 'reconciliation', 'comprehensive_conflicts_audit.csv'))
ap.add_argument('--grep')
ap.add_argument('--cols', help='comma-separated columns to print (default: all)')
a = ap.parse_args()
rows = list(csv.DictReader(open(a.csv, encoding='utf-8-sig', newline='')))
cols = a.cols.split(',') if a.cols else None
for r in rows:
    if r['conflict_id'] in a.ids or (a.grep and re.search(a.grep, ' '.join(r.values()), re.I)):
        print(f"===== {r['conflict_id']}")
        for k, v in r.items():
            if cols is None or k in cols:
                print(f'{k}: {v}')
