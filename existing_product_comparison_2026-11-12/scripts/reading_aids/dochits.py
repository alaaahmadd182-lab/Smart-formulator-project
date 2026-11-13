"""Reading aid (read-only): for one document (archive file name or SHA-256 prefix), print every page that carries a name hit of
any product whose link to it is still open for content review, as the whole page text (whitespace collapsed), with the
products hit on each page. Usage: python dochits.py <file|sha-prefix> [extra pages, comma-separated]
It prints whole pages, not hit windows; it does not decide anything. Pages without a hit are not printed unless listed.
"""
import csv, gzip, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE))
INV = os.path.join(os.path.dirname(BASE), 'incoming_dataset_review_2026-11-12')
OPEN = ('content review LIMITED', 'NOT ASSESSED', 'hit lines only', 'additive lines only', 'page 1 only', 'no content comparison needed')


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    key = sys.argv[1]
    extra = {int(x) for x in sys.argv[2].split(',')} if len(sys.argv) > 2 and sys.argv[2] else set()
    spec = importlib.util.spec_from_file_location('cand', os.path.join(BASE, 'scripts', '01_candidates.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    with open(os.path.join(BASE, 'tables', 'product_identities.csv'), encoding='utf-8') as fh:
        AL = {r['product_id']: r['search_aliases'].split(' | ') for r in csv.DictReader(fh)}
    with open(os.path.join(BASE, 'tables', 'progress_ledger.csv'), encoding='utf-8') as fh:
        L = list(csv.DictReader(fh))
    rows = [r for r in L if (r['file'] == key or r['sha256'].startswith(key)) and not r['reviewed_categories'].startswith('A')
            and r['field_verification_status'].startswith(OPEN)]
    if not rows:
        print('no open link'); return
    sha = rows[0]['sha256']
    print(f"## {rows[0]['file']} | {rows[0]['document_type']} | {rows[0]['pages']} pp | sha {sha[:12]}")
    for r in rows:
        print(f"   open: {r['product_id']} [{r['reviewed_categories']}] hits p.{r['hit_pages']}")
    with gzip.open(os.path.join(INV, '_cache', 'text', sha + '.txt.gz'), 'rt', encoding='utf-8') as fh:
        pages = fh.read().split('\f')
    hitp = {}
    for r in rows:
        rxs = [m.alias_regex(a) for a in AL.get(r['product_id'], [])]
        for i, t in enumerate(pages, 1):
            if any(rx.search(t) for rx in rxs):
                hitp.setdefault(i, []).append(r['product_id'])
    for i in sorted(set(hitp) | extra):
        t = re.sub(r'[ \t]+', ' ', pages[i - 1])
        t = re.sub(r'\n\s*\n+', '\n', t).strip()
        print(f"\n=== p.{i} ({len(t)} chars) products: {', '.join(hitp.get(i, ['(listed)']))}\n{t}")


if __name__ == '__main__':
    main()
