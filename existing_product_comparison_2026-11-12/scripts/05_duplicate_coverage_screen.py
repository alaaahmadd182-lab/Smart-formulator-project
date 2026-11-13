"""Old-versus-new comparison, step 5 (tenth pass): AUTOMATED coverage screen of the byte-duplicate (category A) links.
Read-only. For each A link it lists the numbers printed near a property word in the document's text layer and checks
whether the same number occurs anywhere in that product's JSON (values or printed_text). A number that is not found is
an AUTOMATED LEAD for information that may not have been captured; it is NOT a reading and NOT a finding. The ledger's
source-to-JSON coverage of A links stays 'not assessed' until a reviewer reads the document.

Usage: python existing_product_comparison_2026-11-12/scripts/05_duplicate_coverage_screen.py
Output: tables/duplicate_source_coverage_screen.csv
"""
import collections, csv, glob, gzip, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(BASE)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
PROPERTY = re.compile(r'(?i)typical|specification|density|viscosity|flash ?point|pour ?point|base number|\btbn\b|sulph?ated ash|calcium|phosphorus|zinc|nitrogen|'
                      r'sulph?ur|saturates|aromatic|noack|volatility|cold[- ]cranking|\bccs\b|\bmrv\b|treat(?:ing)? rate|dosage|kv ?\d{2,3}|viscosity index|\bvi\b')
NUMRX = re.compile(r'(?<![\w.,/])[-+−–]?\d+(?:[.,]\d+)?(?![\w])')
# noise filters (documented): CAS registry numbers, test-method codes, and Fahrenheit temperatures are not values
CAS = re.compile(r'\d{2,7}-\d{2}-\d')
METHOD_BEFORE = re.compile(r'(?i)(?:ASTM|D|ISO|IP|EN|DIN|GB/T|SH/T|CEC|NB/SH/T|L-)\s?-?$')
FAHRENHEIT_AFTER = re.compile(r'\s?°\s?F')
STATUS = 'AUTOMATED SCREEN ONLY - not a reading; source-to-JSON coverage remains NOT ASSESSED'


def norm(tok):
    t = tok.replace('−', '-').replace('–', '-').replace('+', '').replace(',', '.')
    try:
        return f'{float(t):g}'
    except ValueError:
        return None


def json_numbers(pid):
    out = set()
    for f in glob.glob(os.path.join(ROOT, 'Products_json', '**', pid, '*.json'), recursive=True):
        with open(f, encoding='utf-8') as fh:
            s = fh.read()
        for m in NUMRX.finditer(s):
            n = norm(m.group())
            if n is not None:
                out.add(n)
                out.add(n.lstrip('-'))
    return out


def main():
    with open(os.path.join(BASE, 'tables', 'progress_ledger.csv'), encoding='utf-8') as fh:
        led = [r for r in csv.DictReader(fh) if r['reviewed_categories'] == 'A']
    share = collections.Counter(r['sha256'] for r in led)
    rows = []
    for r in sorted(led, key=lambda x: (x['product_id'], x['file'])):
        p = os.path.join(INV, '_cache', 'text', r['sha256'] + '.txt.gz')
        base = dict(product_id=r['product_id'], file=r['file'], sha256=r['sha256'], products_sharing_document=share[r['sha256']])
        if not os.path.exists(p):
            rows.append(dict(base, text_available='no (no text layer cached)', numbers_in_property_context=0, found_in_product_json=0, not_found_count='', not_found_examples='', screen_status=STATUS))
            continue
        with gzip.open(p, 'rt', encoding='utf-8') as fh:
            pages = fh.read().split('\f')
        seen = {}
        for i, t in enumerate(pages, 1):
            flat = re.sub(r'\s+', ' ', t)
            for m in PROPERTY.finditer(flat):
                win = flat[m.start(): m.end() + 140]
                cas = [c.span() for c in CAS.finditer(win)]
                for n in NUMRX.finditer(win):
                    v = norm(n.group())
                    if v is None or re.fullmatch(r'(19|20)\d\d', v):
                        continue
                    if any(a <= n.start() < b for a, b in cas) or METHOD_BEFORE.search(win[:n.start()]) or FAHRENHEIT_AFTER.match(win[n.end():]):
                        continue
                    seen.setdefault(v, f'p.{i}: ' + win[:110])
        have = json_numbers(r['product_id'])
        miss = [(v, c) for v, c in seen.items() if v not in have and v.lstrip('-') not in have]
        rows.append(dict(base, text_available='yes', numbers_in_property_context=len(seen), found_in_product_json=len(seen) - len(miss), not_found_count=len(miss),
                         not_found_examples=' || '.join(f'{v} @ {c}' for v, c in miss[:12]), screen_status=STATUS +
                         ('; multi-product document: unmatched numbers may belong to other products' if share[r['sha256']] > 1 else '')))
    out = os.path.join(BASE, 'tables', 'duplicate_source_coverage_screen.csv')
    with open(out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    c = collections.Counter('no text' if r['text_available'] != 'yes' else ('all found' if r['not_found_count'] == 0 else 'leads') for r in rows)
    print(out, len(rows), dict(c))


if __name__ == '__main__':
    main()
