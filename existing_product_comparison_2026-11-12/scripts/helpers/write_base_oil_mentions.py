"""One-off helper (kept for the record): writes a decision file that classifies the remaining NOT-YET-ASSESSED ledger
links of given base-oil products as recipe / component mentions, after the reviewer has read the text around every
name hit (scripts/hits.py output) and set aside the product-specific documents, which get their own decision rows.

Each link gets: category D (formulation / compatibility evidence of ANOTHER product), relationship completed,
content review = 'name-hit lines read (text layer)', coverage = not applicable. No field rows are produced: recipe shares
and formulators' component values are not properties of the base oil.

Usage: python write_base_oil_mentions.py <decision file name> <product_id> [<product_id> ...] --skip <file> [<file> ...]
"""
import csv, gzip, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE))
INV = os.path.join(os.path.dirname(BASE), 'incoming_dataset_review_2026-11-12')


def main():
    args = sys.argv[1:]
    out = args[0]
    pids = args[1:args.index('--skip')] if '--skip' in args else args[1:]
    skip = set(args[args.index('--skip') + 1:]) if '--skip' in args else set()
    spec = importlib.util.spec_from_file_location('cand', os.path.join(BASE, 'scripts', '01_candidates.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    with open(os.path.join(BASE, 'tables', 'product_identities.csv'), encoding='utf-8') as fh:
        ali = {r['product_id']: r['search_aliases'].split(' | ') for r in csv.DictReader(fh)}
    with open(os.path.join(BASE, 'tables', 'progress_ledger.csv'), encoding='utf-8') as fh:
        rows = [r for r in csv.DictReader(fh) if r['product_id'] in pids and r['relationship_status'] == 'not yet assessed' and r['file'] not in skip]
    links = []
    for r in rows:
        p = os.path.join(INV, '_cache', 'text', r['sha256'] + '.txt.gz')
        ctx = ''
        if os.path.exists(p):
            with gzip.open(p, 'rt', encoding='utf-8') as fh:
                pages = fh.read().split('\f')
            for i, t in enumerate(pages, 1):
                for a in ali[r['product_id']]:
                    h = m.alias_regex(a).search(t)
                    if h:
                        ctx = f'p.{i}: ' + re.sub(r'\s+', ' ', t[max(0, h.start() - 60): h.end() + 90]).strip()
                        break
                if ctx:
                    break
        links.append(dict(p=r['product_id'], f=r['file'], cat='D', status='completed',
                          fields_status='content review LIMITED to the name-hit passages (text layer); outstanding: tables and the rest of the document',
                          coverage=('NOT ASSESSED: only the passages around the name hits were inspected (text layer); tables, other pages and the rest of '
                                    'the document were not reviewed for this product, so absence of a property near the name hit says nothing about the document'),
                          identity='exact name in the text; document by another supplier',
                          note='Recipe share, component value or test-oil use in another product\'s document. First hit: ' + ctx[:260]))
    d = dict(batch='other suppliers: base-oil mentions', reviewed_on='2026-11-13 (sixth pass)',
             note='Classified with scripts/helpers/write_base_oil_mentions.py after reading the name-hit lines of every listed document; product-specific documents were excluded and reviewed separately.',
             documents={}, links=links, fields=[])
    target = os.path.join(BASE, 'decisions', out)
    if os.path.exists(target):
        with open(target, encoding='utf-8') as fh:
            old_n = len(json.load(fh).get('links', []))
        if len(links) < old_n:
            sys.exit(f'refusing to overwrite {out}: {old_n} links would shrink to {len(links)} (rebuild without this file first)')
    with open(target, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
    print(out, len(links), 'links')


if __name__ == '__main__':
    main()
