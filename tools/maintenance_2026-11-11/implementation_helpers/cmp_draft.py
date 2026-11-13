"""Scratch: draft structured 'other side' values for the open comparison gaps (to be reviewed by hand)."""
import csv, json, re, sys, os
sys.path.insert(0, r'C:\Users\windo\sf-wsA\tools\data_policy')
os.chdir(r'C:\Users\windo\sf-wsA')
sys.stdout.reconfigure(encoding='utf-8')
import policy_lib as P
import source_coverage_ledger as L
A = P.Archive()
pr = P.load_products()
led = list(csv.DictReader(open('reports/data_policy/source_coverage_ledger.csv', encoding='utf-8')))
NUM = r'(-?\d+(?:[.,]\d+)?)'
out = []
for r in led:
    if not r['comparison_status'].startswith('gap'):
        continue
    sel = r['selected_class']
    other = r['sds_pages_with_label'] if sel == 'TECHNICAL' else r['technical_pages_with_label']
    if sel not in ('TECHNICAL', 'SDS'):  # Missing record: the comparison is between the two classes' printed values
        other = r['sds_pages_with_label']
    for f, pg, how in re.findall(r'([^;]+?\.(?:pdf|PDF)) p\.(\d+) \(([^)]*)\)', other):
        f = f.strip()
        t = A.pages(f)[int(pg) - 1]
        flat = re.sub(r'\s+', ' ', t)
        m = re.search(L.LABELS[r['property']], flat, re.I)
        if not m:
            continue
        win = flat[m.start(): m.start() + 170]
        q = re.search(r'(>=|≥|≦|≤|>|<)\s*' + NUM, win)
        n = re.search(NUM + r'\s*(?:°\s*C|℃|g/cm|kg/m|cSt|mm)', win) or re.search(r':\s*' + NUM, win)
        temp = re.search(r'(?:\(|@\s*|at\s+|\[)\s*(\d+(?:[.,]\d+)?)\s*°?\s*C', win[10:])
        meth = re.findall(r'ASTM\s*D-?\s*\d+|ISO\s*\d+|Pensky-Martens|Cleveland open cup|COC|PMCC|In-house method', win, re.I)
        out.append(dict(product=r['product'], property=r['property'], selected=f"{r['selected_class']} {r['selected_file']} p{r['selected_page']}",
                        file=f, page=int(pg), how=how, window=win[:150],
                        qualifier=q.group(1) if q else None, value=(q.group(2) if q else (n.group(1) if n else None)),
                        temp=temp.group(1) if temp else None, method=meth[:2]))
json.dump(out, open(r'C:\Users\windo\AppData\Local\Temp\claude\c--Users-windo-OneDrive-Desktop-Smart-formulator-project\3f66f328-3708-42fd-ad6b-a350bfb79529\scratchpad\wsA\cmp_draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out:
    print(f"{o['product'][:26]:26} {o['property'][:10]:10} {o['file'][:13]:13} p{o['page']} q={o['qualifier']} v={o['value']} t={o['temp']} m={o['method']} | {o['window'][:95]}")
print(len(out))
