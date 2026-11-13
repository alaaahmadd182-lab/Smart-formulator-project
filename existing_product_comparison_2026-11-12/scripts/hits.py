"""Reading aid: for one product, print every not-yet-assessed ledger link with the document title and the text right
after each hit of the product name (read-only). Usage: python hits.py <product_id> [chars after hit] [max hits per doc]
"""
import csv, gzip, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
INV = os.path.join(os.path.dirname(BASE), 'incoming_dataset_review_2026-11-12')


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    pid = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 90
    mx = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    spec = importlib.util.spec_from_file_location('cand', os.path.join(HERE, '01_candidates.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    with open(os.path.join(BASE, 'tables', 'product_identities.csv'), encoding='utf-8') as fh:
        al = next(r for r in csv.DictReader(fh) if r['product_id'] == pid)['search_aliases'].split(' | ')
    rxs = [m.alias_regex(a) for a in al]
    with open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8') as fh:
        U = {r['sha256']: r for r in csv.DictReader(fh)}
    with open(os.path.join(BASE, 'tables', 'progress_ledger.csv'), encoding='utf-8') as fh:
        rows = [r for r in csv.DictReader(fh) if r['product_id'] == pid and r['relationship_status'] == 'not yet assessed']
    for r in rows:
        u = U.get(r['sha256'], {})
        p = os.path.join(INV, '_cache', 'text', r['sha256'] + '.txt.gz')
        print(f'## {r["file"]} | {r["document_type"]} | pp {r["pages"]} | hits p.{r["hit_pages"]} | {u.get("title_lines", "")[:110]}')
        if not os.path.exists(p):
            print('   (no text)')
            continue
        with gzip.open(p, 'rt', encoding='utf-8') as fh:
            pages = fh.read().split('\f')
        k = 0
        for i, t in enumerate(pages, 1):
            for rx in rxs:
                for h in rx.finditer(t):
                    if k < mx:
                        print(f'   p{i}: ' + re.sub(r'\s+', ' ', t[max(0, h.start() - 25): h.end() + n]).strip())
                    k += 1


if __name__ == '__main__':
    main()
