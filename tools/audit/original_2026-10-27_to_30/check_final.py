"""Consistency checks between the final Markdown and CSV audit reports (read-only)."""
import collections, csv, glob, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
REPO = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project'
os.chdir(REPO)
C = collections.Counter
rows = list(csv.DictReader(open('reconciliation/comprehensive_conflicts_audit.csv', encoding='utf-8-sig'))); R = {r['conflict_id']: r for r in rows}
ids = [r['conflict_id'] for r in rows]
print('CSV rows', len(rows), '| unique', len(set(ids)) == 180, '| contiguous', ids == [f'CF-{i:03d}' for i in range(1, 181)])
md = open('reconciliation/comprehensive_conflicts_audit.md', encoding='utf-8').read()
PIPE = '\x00'
sec5 = md.split('## 5. Findings by type')[1].split('## 6.')[0]; cur = None; mt, mf, mv, heads = {}, {}, {}, {}
for line in sec5.splitlines():
    m = re.match(r'^### 5\.\d (.+) \((\d+)\)$', line)
    if m: cur = m.group(1); heads[cur] = int(m.group(2)); continue
    m = re.match(r'^\| (CF-\d{3}) \|', line)
    if m:
        cells = [c.strip() for c in line.replace('\\|', PIPE).split('|')[1:-1]]
        mt[m.group(1)] = cur; mv[m.group(1)] = cells[7].split(':')[0]; mf[m.group(1)] = cells[9].split(':')[0]
bad = lambda d, k: [i for i in ids if d.get(i) != R[i][k]]
print('section-5 IDs', len(mt), '| mismatches: type', bad(mt, 'finding_type')[:5], 'verification', bad(mv, 'verification_level')[:5], 'follow-up', bad(mf, 'follow_up_category')[:5])
ct = C(r['finding_type'] for r in rows); print('section-5 heading counts == CSV:', heads == dict(ct))
for label, key in (('type', 'finding_type'), ('follow-up', 'follow_up_category'), ('verification level', 'verification_level'), ('resolution', 'resolution_status')):
    for k, n in C(r[key] for r in rows).items():
        m = re.search(r'^\| ' + re.escape(k) + r' \| (\d+) \|', md, re.M)
        assert m and int(m.group(1)) == n, (label, k, n, m and m.group(1))
    print(f'{label} table matches CSV:', dict(C(r[key] for r in rows)))
sec4 = md.split('## 4. Verification')[1].split('## 5.')[0]
pt = re.findall(r'^\| (High|Medium|Low) \| (CF-\d{3}) \|', sec4, re.M)
print('pending table == CSV:', {i for _, i in pt} == {r['conflict_id'] for r in rows if r['verification_priority']}, '| priorities agree:',
      all(R[i]['verification_priority'].split(':')[0] == lv for lv, i in pt), sorted(i for _, i in pt))
s1 = md.split('## 1. Summary tables')[1].split('## 2.')[0]
print('class totals MD', re.search(r'\| \*\*Total\*\* \| (\d+) \| (\d+) \| (\d+) \| \*\*(\d+)\*\*', s1).groups(), 'CSV', [sum(1 for r in rows if r['material_class'] == k) for k in ('Base oil', 'Additive package', 'Additive component')])
for title in ('Category', 'Follow-up'):
    tab = [l for l in s1.split('\n| ' + title + ' |')[1].split('\n\n')[0].splitlines()[1:] if l.startswith('| ') and not l.startswith('|---')]
    print(f'{title} x type table sums to', sum(int(l.split('|')[-2]) for l in tab))
soil = [r for r in rows if 'S-OIL web table' in r['verification_status']]; pc = [r for r in rows if 'IM-1809E' in r['verification_status']]
print('S-OIL', len(soil), dict(C(r['finding_type'] for r in soil)), [r['conflict_id'] for r in soil if r['finding_type'] != 'Edition difference'])
print('Petro-Canada', len(pc), 'records,', len(pc) - sum(1 for r in pc if r['duplicate_of']), 'distinct | duplicates', [(r['conflict_id'], r['duplicate_of']) for r in rows if r['duplicate_of']])
print('distinct issues', 180 - sum(1 for r in rows if r['duplicate_of']))
blob = md + ' '.join(' '.join(r.values()) for r in rows)
print('superseded wording present:', {p: p in blob for p in ('can only be settled by the supplier', 'can only be settled by suppliers', 'all 24 S-OIL edition', 'All 62 Petro-Canada', 'Genuine contradiction')})
print('CF-144:', R['CF-144']['finding_type'], '|', R['CF-144']['verification_level'], '|', R['CF-144']['nature'])
paths = set(p.strip() for r in rows for p in r['json_paths'].split(' ; ')); n = miss = 0
for f in glob.glob('Products_json/**/*.json', recursive=True):
    d = json.load(open(f, encoding='utf-8')); rel = f.replace(os.sep, '/')
    for i, _ in enumerate(d.get('conflicts', [])):
        n += 1; miss += f'{rel}#conflicts[{i}]' not in paths
print('JSON conflict entries', n, 'missing', miss, '| documented rows', sum(1 for r in rows if r['provenance'].startswith('Previously documented (JSON')))
print('user decisions recorded', [r['conflict_id'] for r in rows if r['recorded_decision'].startswith('User decision')])
print('supplier-clarification rows without a reason', [r['conflict_id'] for r in rows if r['follow_up_category'] == 'Supplier clarification' and len(r['follow_up_reason']) < 40])
