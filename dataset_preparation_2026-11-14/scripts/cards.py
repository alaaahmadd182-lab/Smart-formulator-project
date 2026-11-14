"""Reading aid (read-only): one compact identity card per unique document of a supplier group, for reviewing identity.
Each card shows the page-1 text (first N characters, text layer or OCR), the labelled product fields, code tokens and
company lines found by 02_identify.py. Cards are sorted by the automated primary key so product families sit together.
Usage: python cards.py "<supplier_provisional label | (none)>" [chars=260] [--auto-supplier]  ->  stdout
       python cards.py --sha <prefix,prefix,...> [chars]
A card is a reading of page 1 only (or the first characters of it); the decision files must say so.
"""
import csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location('ident', os.path.join(HERE, '02_identify.py'))
ident = importlib.util.module_from_spec(spec); spec.loader.exec_module(ident)


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    args = sys.argv[1:]
    with open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8') as fh:
        A = list(csv.DictReader(fh))
    if args[0] == '--sha':
        pres = args[1].split(',')
        rows = [r for r in A if any(r['sha256'].startswith(p) for p in pres)]
        n = int(args[2]) if len(args) > 2 else 600
    else:
        sup = args[0]
        n = int(args[1]) if len(args) > 1 and args[1].isdigit() else 260
        rows = [r for r in A if (r['supplier_provisional'] or '(none)') == sup]
    rows.sort(key=lambda r: (r['primary_key'] or 'ZZZ' + r['first_path'], r['first_path']))
    print(f'# {len(rows)} documents')
    for r in rows:
        pages, src = ident.pages_for(r['sha256'])
        p1 = re.sub(r'\s+', ' ', pages[0] if pages else '').strip()
        if len(p1) < 60 and len(pages) > 1:
            p1 = (p1 + ' || p2: ' + re.sub(r'\s+', ' ', pages[1]).strip())
        print(f"[{r['sha256'][:10]}] {r['first_path'][:44]} | {r['document_type_provisional']}/{r['document_subtype_provisional'][:12]} | {r['pages']}pp | "
              f"x{r['copies_in_batch']} | auto: {r['primary_identity'][:50]} ({r['identity_confidence']})"
              + (f" | dupOLD" if r['byte_duplicate_of_existing'] else ''))
        print('   ', p1[:n] if p1 else f'(no text: {src})')


if __name__ == '__main__':
    main()
