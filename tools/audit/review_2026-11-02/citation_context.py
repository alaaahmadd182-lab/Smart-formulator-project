"""Print the on-page context of every citation that the number check accepted only by text presence (read-only).

For each such citation (result "on cited page" in check_sources.py, outside the column-checked Petro-Canada and S-OIL
groups) it prints what the finding claims (value, unit, conditions, printed text, document type, property, product)
and, for every occurrence of the number on the cited page:
  - the words on the same row (same baseline, by word position), which carry the row label, unit and method;
  - the column header above the number, when the page is a multi-column table (words directly above, same x);
  - the three text-layer lines before and after.
The output is the material for the association review (association_review.json): the reviewer records for each
citation whether the number is tied to the right product, property, unit, qualifier and conditions.

Usage: python tools/audit/review_2026-11-02/citation_context.py [--findings PATH] [--ids CF-001,CF-002] > context.txt
"""
import argparse, csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf
import review_lib as R


def column_checked(F):
    pc = {i for i, f in F.items() if f['record_id'].startswith('PETRO_CANADA_PURITY_') and i != 'CF-147'}
    so = {i for i, f in F.items() if f['supplier'] == 'S-OIL' and any(str(v.get('file')) == 'DL2-11177.pdf' for v in f['values'])
          and any(str(v.get('file', '')).startswith('http') for v in f['values'])}
    return pc | so


def presence_only(rows, F):
    cc = column_checked(F)
    return [r for r in rows if r['result'] == 'on cited page' and r['id'] not in cc]


def page_obj(ar, name, page):
    m = ar.member(name)
    if m is not None:
        return pymupdf.open(stream=ar.z.read(m), filetype='pdf')[page - 1]
    return pymupdf.open(os.path.join(R.EVIDENCE, os.path.basename(name)))[page - 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--findings', default=os.path.join(R.HERE, 'output', 'findings_v5.json'))
    ap.add_argument('--checks', default=os.path.join(R.ROOT, 'docs', 'audit_review_2026-11-02', 'verification_results', 'source_checks_v5.csv'))
    ap.add_argument('--ids')
    a = ap.parse_args()
    F = {f['id']: f for f in json.load(open(a.findings, encoding='utf-8'))}
    rows = presence_only(list(csv.DictReader(open(a.checks, encoding='utf-8'))), F)
    if a.ids:
        rows = [r for r in rows if r['id'] in a.ids.split(',')]
    ar = R.Archive()
    for r in rows:
        f = F[r['id']]; v = f['values'][int(r['value_index'])]
        page = int(re.findall(r'\d+', str(r['page']))[0])
        p = page_obj(ar, r['file'], page)
        words = p.get_text('words')
        print(f"\n##### {r['id']}#{r['value_index']}#{r['file']} p.{page} | {f['product']} | {f['property']}")
        print(f"   claim: value={v.get('value')!r} unit={v.get('unit')!r} cond={v.get('conditions')!r} temp={v.get('temperature_c')!r} "
              f"printed={v.get('printed_text')!r} doc={v.get('doc_type')!r} date={v.get('revision_date')!r}")
        nums = re.findall(r'-?\d+(?:[.,]\d+)?', str(v.get('value')))
        lines = [l for l in p.get_text().splitlines()]
        for n in nums[:3]:
            hits = [w for w in words if R.on_page(n, w[4]) and re.sub(r'[^\d.,-]', '', w[4]).strip('.,') not in ('',)]
            for w in hits[:3]:
                yc = (w[1] + w[3]) / 2
                row = ' '.join(x[4] for x in sorted((x for x in words if abs((x[1] + x[3]) / 2 - yc) < 3), key=lambda x: x[0]))
                above = ' '.join(x[4] for x in sorted((x for x in words if x[3] < w[1] and abs((x[0] + x[2]) / 2 - (w[0] + w[2]) / 2) < 14),
                                                     key=lambda x: -x[1])[:3])
                print(f"   [{n}] at x={w[0]:.0f} y={w[1]:.0f}: ROW: {row[:200]}")
                print(f"        ABOVE (nearest first): {above[:120]}")
        if not any(R.on_page(n, w[4]) for n in nums for w in words):
            for i, l in enumerate(lines):
                if any(R.on_page(n, l) for n in nums):
                    print('   LINES:', ' | '.join(x.strip() for x in lines[max(0, i - 3):i + 4])[:300])
                    break


if __name__ == '__main__':
    main()
