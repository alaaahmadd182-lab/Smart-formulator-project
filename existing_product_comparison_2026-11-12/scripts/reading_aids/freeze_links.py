"""Reading aid (read-only): for the given documents, print the open (content-review) non-duplicate links as Python literals
(file, product_id, hit pages, first printed name hit, page count) so that a decision generator can carry them frozen and
does not depend on the ledger state at run time. Usage: python freeze_links.py FILE [FILE ...]"""
import csv, gzip, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE))
INV = os.path.join(os.path.dirname(BASE), 'incoming_dataset_review_2026-11-12')
OPEN = ('content review LIMITED', 'NOT ASSESSED', 'hit lines only', 'additive lines only', 'page 1 only', 'no content comparison needed')


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    spec = importlib.util.spec_from_file_location('cand', os.path.join(BASE, 'scripts', '01_candidates.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    with open(os.path.join(BASE, 'tables', 'product_identities.csv'), encoding='utf-8') as fh:
        AL = {r['product_id']: r['search_aliases'].split(' | ') for r in csv.DictReader(fh)}
    with open(os.path.join(BASE, 'tables', 'progress_ledger.csv'), encoding='utf-8') as fh:
        L = list(csv.DictReader(fh))
    for f in sys.argv[1:]:
        rows = [r for r in L if r['file'] == f and not r['reviewed_categories'].startswith('A') and r['field_verification_status'].startswith(OPEN)]
        if not rows:
            print(f'# {f}: no open link'); continue
        with gzip.open(os.path.join(INV, '_cache', 'text', rows[0]['sha256'] + '.txt.gz'), 'rt', encoding='utf-8') as fh:
            pages = fh.read().split('\f')
        for r in rows:
            rxs = [m.alias_regex(a) for a in AL.get(r['product_id'], [])]
            hp, first = [], ''
            for i, t in enumerate(pages, 1):
                hs = [h for rx in rxs for h in rx.finditer(t)]
                if hs:
                    hp.append(i)
                    if not first:
                        first = re.sub(r'\s+', ' ', min(hs, key=lambda h: h.start()).group(0)).strip()
            print(repr((f, r['product_id'], r['reviewed_categories'], ','.join(map(str, hp)), first, r['pages'])) + ',')


if __name__ == '__main__':
    main()
