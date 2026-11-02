"""Extract and render the Afton performance-claim matrices (read-only on the archive).

The claims tables of the Afton HiTEC 12200 bulletins (DL2-11412.PDF 05/18, DL2-14639.pdf 08/18) and HiTEC 12210M bulletins
(DL2-11796.pdf 05/18, DL2-15568.pdf 04/22) are vector drawings: a claim is a small filled circle, an "MB package approval"
is a circled "P" icon, the column labels are rotated text and every row carries an SAE grade. For each page this script:

  1. reads the column labels (rotated text lines above the table) and the row labels (treat rate, booster, SAE grade,
     base-oil group, read from word positions);
  2. reads every mark inside the table (filled shapes up to 6 pt wide), classifies it as "dot" (a circle drawn from
     curves only) or "icon" (a shape that also contains straight segments: the circled P), and assigns it to the
     nearest row and column; a mark farther than the tolerance from every row or column is reported, never forced;
  3. writes the grid to docs/audit_review_2026-11-02/verification_results/afton/<doc>_matrix.csv;
  4. renders the table area at 220 dpi (and, with --crops, the regions the findings depend on) to the same folder
     for visual confirmation;
  5. prints the cells the Afton findings depend on (CF-001, CF-002, CF-166, CF-167) and the footnotes.

Usage: python tools/audit/review_2026-11-02/afton_matrices.py [--no-render]
Exit codes: 0 extraction complete and every mark assigned; 1 otherwise.
"""
import argparse, csv, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf
import review_lib as R

OUT = os.path.join(R.ROOT, 'docs', 'audit_review_2026-11-02', 'verification_results', 'afton')
DOCS = {'DL2-11412.PDF': 'HiTEC 12200 bulletin 05/18', 'DL2-14639.pdf': 'HiTEC 12200 bulletin 08/18',
        'DL2-11796.pdf': 'HiTEC 12210M bulletin 05/18', 'DL2-15568.pdf': 'HiTEC 12210M bulletin 04/22'}


def page_of(name):
    ar = R.Archive()
    m = ar.member(name)
    return pymupdf.open(stream=ar.z.read(m), filetype='pdf')[1]


def extract(page):
    d = page.get_text('dict')
    cols = []
    for b in d['blocks']:
        for l in b.get('lines', []):
            if abs(l['dir'][0] - 1.0) > 1e-3:  # rotated text: a candidate column label
                t = re.sub(r'\s+', ' ', ''.join(sp['text'] for sp in l['spans'])).strip()
                ox, oy = l['spans'][0]['origin']  # baseline start = the bottom of the label, which sits on its column
                cols.append({'label': t, 'x0': l['bbox'][0], 'y1': l['bbox'][3], 'ox': ox, 'oy': oy})
    # the table header: labels whose baselines start at the same height (rotated text elsewhere on the page is dropped)
    oys = sorted(round(c['oy']) for c in cols)
    mode = max(set(oys), key=oys.count)
    cols = sorted([c for c in cols if abs(c['oy'] - mode) <= 3], key=lambda c: c['ox'])
    # keep the longest run spaced like table columns (< 20 pt): rotated row-header labels ("HiTEC® 12200", "Boosters") stand apart
    runs, cur = [], [cols[0]]
    for c in cols[1:]:
        if c['ox'] - cur[-1]['ox'] < 20:
            cur.append(c)
        else:
            runs.append(cur); cur = [c]
    runs.append(cur)
    cols = max(runs, key=len)
    header_y = max(c['y1'] for c in cols)
    words = page.get_text('words')
    left = cols[0]['x0'] - 2  # row labels lie left of the first column
    lines = {}
    for w in sorted((w for w in words if w[1] > header_y and w[2] <= left + 4 and w[1] < header_y + 220), key=lambda w: (w[1] + w[3]) / 2):
        yc = (w[1] + w[3]) / 2
        near = [k for k in lines if abs(k - yc) < 3]  # words of one row may sit on slightly different baselines
        lines.setdefault(near[0] if near else yc, []).append(w)
    rows = []
    for yc in sorted(lines):
        ws = sorted(lines[yc], key=lambda x: x[0])
        text = ' '.join(x[4] for x in ws)
        # a matrix row: an SAE grade (HiTEC 12200 tables) or an API category with a grade (HiTEC 12210M tables)
        if re.search(r'\bSAE \d+W-\d+|^API (CK|FA|CJ)-4 \d+W-\d+', text) and not (rows and yc - rows[-1]['y'] > 25):
            rows.append({'y': yc, 'label': text})
    bottom = rows[-1]['y'] + 6
    marks = []
    for dr in page.get_drawings():
        r = dr['rect']
        if (r.width <= 8.5 and r.height <= 8.5 and header_y < r.y0 and r.y1 < bottom and dr.get('fill') is not None
                and dr['fill'] != (1.0, 1.0, 1.0) and r.width > 1.5):
            kinds = {i[0] for i in dr['items']}
            marks.append({'x': (r.x0 + r.x1) / 2, 'y': (r.y0 + r.y1) / 2, 'kind': 'dot' if kinds == {'c'} else 'icon',
                          'w': r.width, 'fill': tuple(round(c, 2) for c in dr['fill'])})
    # columns = intervals between the table's vertical cell separators (thin filled bars in the table band); each label's
    # baseline origin must fall in its own interval, and a mark belongs to the interval that contains its centre
    seps = sorted({round(dr['rect'].x0, 1) for dr in page.get_drawings()
                   if dr['rect'].width < 1.5 and dr['rect'].height > 5 and header_y - 5 < dr['rect'].y0 < bottom})
    def interval(x):
        for a_, b_ in zip(seps, seps[1:]):
            if a_ <= x < b_:
                return (a_, b_)
        return None
    for c in cols:
        c['iv'] = interval(c['ox'])
    ivs = [c['iv'] for c in cols]
    bad_labels = [c['label'] for c in cols if c['iv'] is None] + [c['label'] for c in cols if ivs.count(c['iv']) > 1]
    by_iv = {c['iv']: c for c in cols if c['iv'] is not None}
    unassigned, grid = [(f'label without its own column: {x}',) for x in sorted(set(bad_labels))], {}
    for m in marks:
        c = by_iv.get(interval(m['x']))
        rw = min(rows, key=lambda r: abs(r['y'] - m['y']))
        dy = abs(rw['y'] - m['y'])
        if c is None or dy > 4:
            unassigned.append((round(m['x'], 1), round(m['y'], 1), m['kind'], 'no labelled column' if c is None else f'dy {dy:.1f}'))
            continue
        grid.setdefault((rw['label'], c['label']), set()).add(m['kind'])
    off = len(seps)
    for r in rows:
        r['seps'] = seps
    return cols, rows, grid, unassigned, off, header_y, bottom


def highlight(name, row_re, col_label, tag):
    """Render the table with the cell (row_re, col_label) outlined in red; the page is changed in memory only."""
    p = page_of(name)
    cols, rows, grid, un, off, hy, bottom = extract(p)
    c = next(c for c in cols if c['label'] == col_label)
    r = next(r for r in rows if re.search(row_re, r['label']))
    cell = pymupdf.Rect(c['iv'][0], r['y'] - 5.5, c['iv'][1], r['y'] + 5.5)
    p.draw_rect(cell, color=(1, 0, 0), width=0.8)
    p.draw_rect(pymupdf.Rect(15, r['y'] - 5.5, c['iv'][1], r['y'] + 5.5), color=(1, 0, 0), width=0.3)
    clip = pymupdf.Rect(10, hy - 45, p.rect.width - 10, bottom + 4)
    out = os.path.join(OUT, f'{os.path.splitext(name)[0]}_p2_{tag}_cell_300dpi.png')
    p.get_pixmap(dpi=300, clip=clip).save(out)
    return out


def footnotes(page, bottom):
    return [re.sub(r'\s+', ' ', b[4]).strip() for b in page.get_text('blocks') if b[1] > bottom - 4 and b[1] < bottom + 60]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--no-render', action='store_true'); a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    ok = True; M = {}
    for name, label in DOCS.items():
        p = page_of(name)
        cols, rows, grid, un, off, hy, bottom = extract(p)
        M[name] = (cols, rows, grid)
        base = os.path.splitext(name)[0]
        with open(os.path.join(OUT, f'{base}_p2_matrix.csv'), 'w', encoding='utf-8-sig', newline='') as fh:
            w = csv.writer(fh, lineterminator='\r\n'); w.writerow(['row (treat rate, booster, SAE grade, group)'] + [c['label'] for c in cols])
            for r in rows:
                w.writerow([r['label']] + ['/'.join(sorted(grid.get((r['label'], c['label']), ''))) for c in cols])
        n = sum(len(v) for v in grid.values())
        print(f'== {name} p.2 ({label}): {len(cols)} columns, {len(rows)} rows, {n} marked cells; {off} cell separators; '
              f'unassigned marks {len(un)} {un[:4]}')
        ok &= not un
        for f in footnotes(p, bottom):
            print('   footnote/legend:', f[:160])
        if not a.no_render:
            clip = pymupdf.Rect(10, hy - 45, p.rect.width - 10, bottom + 60)
            p.get_pixmap(dpi=220, clip=clip).save(os.path.join(OUT, f'{base}_p2_matrix_220dpi.png'))
    # ---- cells the findings depend on
    def cell(name, row_re, col):
        cols, rows, grid = M[name]
        rr = [r['label'] for r in rows if re.search(row_re, r['label'])]
        if len(rr) != 1:
            return f'row {row_re!r}: {len(rr)} matching rows {rr}'
        if col not in [c['label'] for c in cols]:
            return f'column {col!r} not in table'
        return '/'.join(sorted(grid.get((rr[0], col), ''))) or 'empty'
    print('\nCF-001 MTU 2.0, row 10.3% + 5.0% HiTEC 12255 SAE 15W-40 GP I:')
    for n in ('DL2-11412.PDF', 'DL2-14639.pdf'):
        print(f'   {n}:', cell(n, r'5\.0% HiTEC® 12255 SAE 15W-40 GP I$', 'MTU 2.0'))
    print('CF-002 DDC 93K215, row 11.7% + 0.9% HiTEC 12260 SAE 10W-30 GP II:')
    for n in ('DL2-11412.PDF', 'DL2-14639.pdf'):
        print(f'   {n}:', cell(n, r'^11\.7% 0\.9% HiTEC® 12260 SAE 10W-30 GP II$', 'DDC 93K215'))
    print('CF-167 rows/columns only in 08/18:')
    for n in ('DL2-11412.PDF', 'DL2-14639.pdf'):
        cols, rows, grid = M[n]
        print(f'   {n}: columns API SN / MB 229.3 / RN 0700 present:', [x in [c["label"] for c in cols] for x in ('API SN', 'MB 229.3', 'RN 0700')],
              '| rows with 10.8% + 0.9% HiTEC 12260 SAE 10W-30:', [r['label'] for r in rows if re.search(r'^10\.8% 0\.9% HiTEC® 12260 SAE 10W-30', r['label'])],
              '| rows with 10.8% + 0.6% HiTEC 9552 SAE 10W-40:', [r['label'] for r in rows if re.search(r'^10\.8% 0\.6% HiTEC® 9552', r['label'])])
    for n in ('DL2-14639.pdf',):
        cols, rows, grid = M[n]
        for r in rows:
            if re.search(r'^10\.8% (0\.9% HiTEC® 12260 SAE 10W-30|0\.6% HiTEC® 9552)', r['label']):
                print(f'   {n} row "{r["label"]}" marked columns:', [c['label'] for c in cols if (r['label'], c['label']) in grid])
    print('CF-166 columns of the HiTEC 12210M tables:')
    c05 = [c['label'] for c in M['DL2-11796.pdf'][0]]; c22 = [c['label'] for c in M['DL2-15568.pdf'][0]]
    print('   only in 05/18:', [c for c in c05 if c not in c22]); print('   only in 04/22:', [c for c in c22 if c not in c05])
    r05 = [r['label'] for r in M['DL2-11796.pdf'][1]]; r22 = [r['label'] for r in M['DL2-15568.pdf'][1]]
    print('   rows 05/18:', r05); print('   rows 04/22:', r22)
    diff = []
    for r in set(r05) & set(r22):
        for c in set(c05) & set(c22):
            a5 = (r, c) in M['DL2-11796.pdf'][2]; a2 = (r, c) in M['DL2-15568.pdf'][2]
            if a5 != a2:
                diff.append((r, c, a5, a2))
    print(f'   shared rows x shared columns compared: {len(set(r05) & set(r22)) * len(set(c05) & set(c22))}; cells that differ: {diff}')
    if not a.no_render:
        for n in ('DL2-11412.PDF', 'DL2-14639.pdf'):
            highlight(n, r'5\.0% HiTEC® 12255 SAE 15W-40 GP I$', 'MTU 2.0', 'CF-001')
            highlight(n, r'^11\.7% 0\.9% HiTEC® 12260 SAE 10W-30 GP II$', 'DDC 93K215', 'CF-002')
    print('\nOVERALL:', 'PASS (every mark assigned)' if ok else 'FAIL (unassigned marks)')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
