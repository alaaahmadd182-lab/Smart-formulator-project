"""Compare two coverage workbooks sheet by sheet: cell diffs for keyed sheets, row multiset diffs otherwise."""
import collections, sys
from openpyxl import load_workbook
sys.stdout.reconfigure(encoding='utf-8')
a, b = load_workbook(sys.argv[1], read_only=True), load_workbook(sys.argv[2], read_only=True)
print('sheets A', a.sheetnames); print('sheets B', b.sheetnames)
total = 0
for name in a.sheetnames:
    if name not in b.sheetnames:
        print('only in A:', name); continue
    ra = [tuple(r) for r in a[name].iter_rows(values_only=True)]
    rb = [tuple(r) for r in b[name].iter_rows(values_only=True)]
    if ra == rb:
        print(f'[{name}] identical ({len(ra)} rows)'); continue
    if len(ra) == len(rb) and all(len(x) == len(y) for x, y in zip(ra, rb)):
        diffs = [(i + 1, j + 1, x[j], y[j]) for i, (x, y) in enumerate(zip(ra, rb)) for j in range(len(x)) if x[j] != y[j]]
        print(f'[{name}] same shape, {len(diffs)} cells differ')
        hdr = ra[0]
        for i, j, va, vb in diffs[:60]:
            print(f'   row {i} ({ra[i-1][0]} | {ra[i-1][1]}) col {hdr[j-1]!r}: {va!r} -> {vb!r}')
        total += len(diffs)
    else:
        ca, cb = collections.Counter(ra), collections.Counter(rb)
        only_a, only_b = ca - cb, cb - ca
        print(f'[{name}] rows {len(ra)} -> {len(rb)}; removed {sum(only_a.values())}, added {sum(only_b.values())}')
        for r in only_a: print('   -', r)
        for r in only_b: print('   +', r)
        total += sum(only_a.values()) + sum(only_b.values())
print('TOTAL differences', total)
