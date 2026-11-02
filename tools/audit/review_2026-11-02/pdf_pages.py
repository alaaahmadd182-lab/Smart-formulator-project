"""Print the text layer of archive documents, page by page, read in memory from the source ZIP (no extraction).

Used in the 2026-11-02 documentation review to read cited pages. Read-only.

Usage:
    python tools/audit/review_2026-11-02/pdf_pages.py DL2-13444.pdf [--pages 6,7] [--grep REGEX] [--words]
        [--zip "Manual + Data to share.zip"] [--render OUTDIR --dpi 110]

--grep prints only matching lines (with page numbers); --words prints each word with its x/y position (for reading
table columns); --render writes PNG renders of the selected pages to OUTDIR (for pages without a text layer).
"""
import argparse, os, re, sys, zipfile

import pymupdf

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def key(name):
    # same rule as review_lib.Archive.key: some member names carry '%20' or a U+FFFD where '%' was
    n = str(name).replace('�', '%').replace('%20', ' ').replace('%', '').lower().strip()
    return re.sub(r'\s+', ' ', n)


def member(z, name):
    want = key(os.path.basename(name))
    hits = [n for n in z.namelist() if not n.endswith('/') and key(os.path.basename(n)) == want]
    if len(hits) != 1:
        sys.exit(f'{name}: {len(hits)} matching archive members {hits[:5]}')
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('doc')
    ap.add_argument('--zip', default=os.path.join(ROOT, 'Manual + Data to share.zip'))
    ap.add_argument('--pages', help='comma-separated 1-based pages (default: all)')
    ap.add_argument('--grep')
    ap.add_argument('--words', action='store_true')
    ap.add_argument('--render')
    ap.add_argument('--dpi', type=int, default=110)
    a = ap.parse_args()
    z = zipfile.ZipFile(a.zip)
    m = member(z, a.doc)
    doc = pymupdf.open(stream=z.read(m), filetype=os.path.splitext(m)[1].lstrip('.').lower() or 'pdf')
    pages = [int(p) for p in a.pages.split(',')] if a.pages else range(1, len(doc) + 1)
    print(f'# {m} ({len(doc)} pages)')
    for p in pages:
        pg = doc[p - 1]
        if a.render:
            os.makedirs(a.render, exist_ok=True)
            out = os.path.join(a.render, f'{os.path.splitext(os.path.basename(m))[0]}_p{p}.png')
            pg.get_pixmap(dpi=a.dpi).save(out)
            print(f'rendered p.{p} -> {out}')
            continue
        if a.words:
            for w in pg.get_text('words'):
                print(f'p.{p} x={w[0]:.0f} y={w[1]:.0f} {w[4]}')
            continue
        text = pg.get_text()
        if a.grep:
            for line in text.splitlines():
                if re.search(a.grep, line, re.I):
                    print(f'p.{p}: {line}')
        else:
            print(f'--- p.{p} ---\n{text}')


if __name__ == '__main__':
    main()
