"""Scratch reading aid: for given archive files, print the cases (ledger rows) that cite them as leads, the current
record values, and the page text (compact)."""
import csv, re, sys, os
sys.path.insert(0, r'C:\Users\windo\sf-wsA\tools\data_policy')
os.chdir(r'C:\Users\windo\sf-wsA')
sys.stdout.reconfigure(encoding='utf-8')
import policy_lib as P

files = sys.argv[1:]
full = '--full' in files
files = [f for f in files if not f.startswith('--')]
R = list(csv.DictReader(open('reports/data_policy/source_coverage_ledger.csv', encoding='utf-8')))
pr = P.load_products()
A = P.Archive()
for f in files:
    cases = [r for r in R if f in r['technical_pages_with_label'] + r['sds_pages_with_label'] + r['unsearchable_documents']
             and (r['selection_status'] in ('missing_label_found', 'missing_not_searchable') or r['comparison_status'].startswith('gap'))]
    print('=' * 20, f, len(cases), 'cases')
    for r in cases:
        n = None
        for d in pr[r['product']]['files'].values():
            if r['property'] in d['fields']:
                n = d['fields'][r['property']]; n = n[0] if isinstance(n, list) else n
        print(f"  {r['product']:32} {r['property']:16} {r['selection_status']:22} sel={r['selected_file']} p{r['selected_page']} "
              f"val={n.get('value') if n else None} min={n.get('min') if n else None} max={n.get('max') if n else None} q={n.get('qualifier') if n else None} | {r['comparison_status'][:40]}")
    pages = A.pages(f) or []
    for i, t in enumerate(pages):
        flat = re.sub(r'[ \t]+', ' ', t)
        flat = re.sub(r'\n\s*\n+', '\n', flat)
        print(f'--- {f} p.{i + 1} ({len(flat)} chars)')
        print(flat if full else flat[:3500])
