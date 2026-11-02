"""Report-level consistency checks of the comprehensive conflicts audit (read-only).

Checks the Markdown report and CSV against each other and against the product JSON:
  A  IDs: CF-001..CF-180 once each in the CSV and once each in the section-5 tables of the Markdown, in the table of
     the finding's own type and material class; duplicate_of / related_ids name existing findings.
  B  Counts: every summary table and every count stated in the Markdown text is recomputed from the CSV.
  C  JSON paths: every cited file exists (in the working tree and at the snapshot commit) and every anchor
     (conflicts[i], fields.x.y, open_questions) resolves; "Open question (verbatim)" quotations occur verbatim in the
     JSON of the snapshot commit.
  D  Classification rules: the comparability text agrees with the finding type, no explanation calls a confirmed
     contradiction "not a confirmed ... contradiction", the follow-up category agrees with the recommended next
     step and the verification priority, and a "Verified" level is not paired with text saying the value was not
     re-read.
Rule D results are review leads: a rule can be waived for one finding only with a reason in WAIVERS.

Usage:
    python tools/audit/review_2026-11-02/check_report.py [--md PATH] [--csv PATH] [--rev COMMIT]
Exit codes: 0 all checks passed; 1 at least one check failed.
"""
import argparse, collections, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import review_lib as R

CLS = [('Base oil', 'Base oils'), ('Additive package', 'Additive packages'), ('Additive component', 'Additive components')]
COMPARABILITY_PREFIX = {
    R.CONF: ('Confirmed',),
    R.POT: ('Uncertain', 'Partly uncertain'),
    'Edition difference': ('Confirmed: same document series', 'Confirmed: same grade column', 'Edition change',
                           'Same document series', 'Not applicable'),
    'Explainable difference': ('Not comparable',),
    'Data-quality issue': ('Not applicable',),
}
WAIVERS = {  # (rule, id) -> reason; reviewed 2026-11-02
    ('D1', 'CF-024'): 'data-quality record (suspected unit misprint) whose comparability text accurately describes the typical-vs-maximum '
                      'comparison and the 10,000-fold unit gap; the uncertainty is the point of the finding',
    ('D1', 'CF-159'): 'data-quality record inside the CF-009 comparison; it repeats CF-009\'s comparability statement, which is accurate',
}


class Checks:
    def __init__(self):
        self.fails, self.n = [], 0

    def check(self, ok, msg):
        self.n += 1
        if not ok:
            self.fails.append(msg)
            print('FAIL', msg)


def md_tables(md):
    """{id: (type heading, class heading)} for every row of the section-5 tables."""
    out, t, c = collections.defaultdict(list), None, None
    in5 = False
    for line in md.splitlines():
        if line.startswith('## '):
            in5 = line.startswith('## 5.')
        if not in5:
            continue
        m = re.match(r'### 5\.\d+ (.+?) \((\d+)\)$', line)
        if m:
            t = m.group(1); continue
        m = re.match(r'#### (.+?) \((\d+)\)$', line)
        if m:
            c = m.group(1); continue
        m = re.match(r'\| (CF-\d{3}) \|', line)
        if m:
            out[m.group(1)].append((t, c))
    return out


def table_after(md, header_start):
    """Rows (lists of cells) of the first Markdown table whose header line starts with header_start."""
    lines = md.splitlines()
    for i, l in enumerate(lines):
        if l.startswith(header_start):
            rows = []
            for l2 in lines[i + 2:]:
                if not l2.startswith('|'):
                    break
                rows.append([x.strip() for x in l2.strip('|').split(' | ')])
            return rows
    return None


def resolve_anchor(doc, anchor):
    if anchor in ('', None):
        return True
    if anchor == 'open_questions':
        return bool(doc.get('open_questions'))
    m = re.fullmatch(r'conflicts\[(\d+)\]', anchor)
    if m:
        return int(m.group(1)) < len(doc.get('conflicts') or [])
    if anchor.startswith('fields.'):
        node = doc.get('fields')
        for part in anchor.split('.')[1:]:
            if not isinstance(node, dict) or part not in node:
                return False
            node = node[part]
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--md', default=R.REPORT_MD)
    ap.add_argument('--csv', default=R.REPORT_CSV)
    ap.add_argument('--rev', default=R.SNAPSHOT_COMMIT, help='commit whose product JSON the findings describe')
    a = ap.parse_args()
    md = open(a.md, encoding='utf-8').read().replace('\r\n', '\n')
    rows = R.read_csv(a.csv)
    by = {r['conflict_id']: r for r in rows}
    K = Checks()

    # ---- A: IDs and placement
    ids = [r['conflict_id'] for r in rows]
    K.check(ids == [f'CF-{i:03d}' for i in range(1, 181)], 'CSV holds CF-001..CF-180 once each, in order')
    tab = md_tables(md)
    K.check(set(tab) == set(ids) and all(len(v) == 1 for v in tab.values()), 'every ID appears exactly once in the section-5 tables')
    label = dict(CLS)
    for r in rows:
        place = tab.get(r['conflict_id'], [(None, None)])[0]
        K.check(place == (r['finding_type'], label[r['material_class']]),
                f"{r['conflict_id']}: Markdown table {place} matches CSV type/class ({r['finding_type']}, {r['material_class']})")
        for x in [r['duplicate_of']] + [y.strip() for y in r['related_ids'].split(',')]:
            if x:
                K.check(x in by, f"{r['conflict_id']}: referenced finding {x} exists")
        K.check(r['finding_type'] in R.TYPES and r['follow_up_category'] in R.FU, f"{r['conflict_id']}: type and follow-up are from the defined lists")

    # ---- B: counts
    C = collections.Counter
    types = C(r['finding_type'] for r in rows); fu = C(r['follow_up_category'] for r in rows)
    res = C(r['resolution_status'] for r in rows); lv = C(r['verification_level'] for r in rows)
    t1 = table_after(md, '| Type | Records | Meaning |')
    K.check(t1 is not None and all(int(c[1].strip('*')) == (types[c[0]] if c[0] in types else len(rows)) for c in t1 if c[0] != '**Total**')
            and t1[-1][1] == f'**{len(rows)}**', 'supervisor type table matches the CSV')
    t2 = table_after(md, '| Follow-up | Records | Meaning |')
    K.check(t2 is not None and all(int(c[1]) == fu[c[0]] for c in t2), 'supervisor follow-up table matches the CSV')
    t3 = table_after(md, '| Type | Base oils |')
    ok = t3 is not None
    for c in t3 or []:
        if c[0] == '**Total**':
            exp = [sum(1 for r in rows if r['material_class'] == k) for k, _ in CLS]
            ok &= [int(x) for x in c[1:4]] == exp and c[4] == f'**{len(rows)}**'
        else:
            exp = [sum(1 for r in rows if r['finding_type'] == c[0] and r['material_class'] == k) for k, _ in CLS]
            ok &= [int(x) for x in c[1:4]] == exp and int(c[4]) == sum(exp)
    K.check(ok, 'type x class table matches the CSV')
    t4 = table_after(md, '| Category |')
    ok = t4 is not None
    for c in t4 or []:
        exp = [sum(1 for r in rows if r['conflict_category'] == c[0] and r['finding_type'] == t) for t in R.TYPES]
        ok &= [int(x) for x in c[1:6]] == exp and int(c[6]) == sum(exp)
    K.check(ok and sum(int(c[6]) for c in t4 or []) == len(rows), 'category x type table matches the CSV')
    t5 = table_after(md, '| Follow-up | Confirmed')
    ok = t5 is not None
    for c in t5 or []:
        exp = [sum(1 for r in rows if r['follow_up_category'] == c[0] and r['finding_type'] == t) for t in R.TYPES]
        ok &= [int(x) for x in c[1:6]] == exp and int(c[6]) == sum(exp)
    K.check(ok, 'follow-up x type table matches the CSV')
    t6 = table_after(md, '| Resolution status | Records |')
    K.check(t6 is not None and {c[0]: int(c[1]) for c in t6} == dict(res), 'resolution-status table matches the CSV')
    t7 = table_after(md, '| Verification level | Records |')
    K.check(t7 is not None and {c[0]: int(c[1]) for c in t7} == dict(lv), 'verification-level table matches the CSV')
    for t in R.TYPES:
        K.check(f'### 5.{R.TYPES.index(t) + 1} {t} ({types[t]})' in md, f'section heading count for {t}')
    m = re.search(r'(\d+) records are verified, (\d+) partially verified and (\d+) pending', md)
    K.check(bool(m) and (int(m.group(1)), int(m.group(2)), int(m.group(3))) ==
            (lv['Verified'], lv['Partially verified'], lv['Pending']), 'verification counts in the summary text')
    pend = [r for r in rows if r['verification_priority']]
    t8 = table_after(md, '| Priority | ID |')
    K.check(t8 is not None and sorted(c[1] for c in t8) == sorted(r['conflict_id'] for r in pend), 'pending-items table lists exactly the findings with a verification priority')
    m = re.search(r'(\d+) items still need evidence that could not be obtained \(High (\d+), Medium (\d+), Low (\d+)', md)
    pr = C(r['verification_priority'].split(':')[0] for r in pend)
    K.check(bool(m) and tuple(map(int, m.groups())) == (len(pend), pr['High'], pr['Medium'], pr['Low']), 'pending-item counts in the summary text')
    n_dup = sum(1 for r in rows if r['duplicate_of'])
    K.check(f'so there are {len(rows) - n_dup} distinct issues' in md, 'distinct-issue count')
    for r in rows:
        for c in t8 or []:
            if c[1] == r['conflict_id']:
                K.check(c[5] == r['follow_up_category'], f"{r['conflict_id']}: follow-up in the pending table matches the CSV")

    # ---- C: JSON paths and verbatim quotations
    cache = {}
    def doc(rev, rel):
        k = (rev, rel)
        if k not in cache:
            try:
                cache[k] = R.load_json_at(rev, rel)
            except Exception:
                cache[k] = None
        return cache[k]
    for r in rows:
        for p in [x.strip() for x in r['json_paths'].split(' ; ') if x.strip()]:
            rel, _, anchor = p.partition('#')
            d_now, d_snap = doc(None, rel), doc(a.rev, rel)
            K.check(d_now is not None and d_snap is not None, f"{r['conflict_id']}: JSON file exists now and at {a.rev}: {rel}")
            if d_snap is not None:
                K.check(resolve_anchor(d_snap, anchor), f"{r['conflict_id']}: anchor #{anchor} resolves in {rel}")
        m = re.match(r'Open question \(verbatim\): (.*?)(?: AUDIT CHECK:| \[\'|$)', r['explanation'])
        if m:
            quote = m.group(1).strip()
            texts = []
            for p in r['json_paths'].split(' ; '):
                d = doc(a.rev, p.split('#')[0].strip())
                if d:
                    texts.append(json.dumps(d.get('open_questions'), ensure_ascii=False))
            found = any(quote in json.loads(json.dumps(t)) for t in texts) or any(quote in json.loads(t).__str__() for t in texts)
            if not found:
                found = any(quote in q.get('question', '') for t in texts for q in json.loads(t) or [] if isinstance(q, dict))
            K.check(found, f"{r['conflict_id']}: verbatim open-question quotation occurs in the JSON at {a.rev}")

    # ---- C2: conflict entries -> distinct conflicts -> finding records (the "147 / 125" statements)
    files = subprocess.run(['git', 'ls-tree', '-r', '--name-only', a.rev, 'Products_json'], cwd=R.ROOT, capture_output=True,
                           text=True, encoding='utf-8').stdout.split('\n')
    raw = []
    for f in files:
        if f.endswith('.json'):
            d = doc(a.rev, f)
            raw += [(f, i) for i in range(len((d or {}).get('conflicts') or []))]
    cited = {}
    for r in rows:
        for p in r['json_paths'].split(' ; '):
            m = re.search(r'^(.*?)#conflicts\[(\d+)\]$', p.strip())
            if m:
                cited.setdefault((m.group(1), int(m.group(2))), set()).add(r['conflict_id'])
    recs = {i for v in cited.values() for i in v}
    n_doc = sum(1 for r in rows if r['provenance'].startswith('Previously documented (JSON conflicts[]'))
    K.check(len(raw) == 147 and set(cited) == set(raw) and all(len(v) == 1 for v in cited.values()),
            f'all {len(raw)} raw JSON conflict entries at {a.rev} are cited, each by exactly one finding record')
    K.check(len(recs) == 125 == n_doc, f'the 147 entries form {len(recs)} distinct conflicts = {n_doc} finding records marked "Previously documented (JSON conflicts[])"')
    K.check('The 147 conflict entries already recorded in the JSON (125 distinct conflicts)' in md and '125 records were already recorded as conflicts' in md,
            'the report states 147 raw entries / 125 distinct conflicts / 125 finding records')
    K.check(not re.search(r'147 (conflict-entry )?findings|147 finding', md), 'the report never calls the 147 entries "findings"')

    # ---- C3: every quoted final_resolution equals the JSON conflict entry it comes from
    n_fr = 0
    for r in rows:
        m = re.search(r'final_resolution: (.*)$', r['explanation'])
        anchors = [p.strip() for p in r['json_paths'].split(' ; ') if '#conflicts[' in p]
        if not m or not anchors:
            continue
        q = m.group(1).strip()
        for p in anchors:
            rel, _, anc = p.partition('#')
            d = doc(a.rev, rel)
            fr = (d or {}).get('conflicts', [{}])[int(re.search(r'\[(\d+)\]', anc).group(1))].get('final_resolution')
            n_fr += 1
            # exact quotation, or the exact quotation followed by the audit's own "NOTE: ..." (CF-024, CF-025)
            ok = fr is not None and (q == fr or (q.startswith(fr) and q[len(fr):].strip().startswith('NOTE:')))
            K.check(ok, f"{r['conflict_id']}: quoted final_resolution equals the JSON entry {rel.split('/')[-1]}#{anc}")
    K.check(n_fr > 0, f'final_resolution quotations compared: {n_fr}')

    # ---- D: classification and follow-up rules
    def rule(name, fid, ok, msg):
        if not ok and (name, fid) in WAIVERS:
            print(f'WAIVED {name} {fid}: {WAIVERS[(name, fid)]}')
            ok = True
        K.check(ok, f'{fid}: [{name}] {msg}')
    for r in rows:
        fid, t, comp = r['conflict_id'], r['finding_type'], r['comparability']
        rule('D1', fid, comp.startswith(COMPARABILITY_PREFIX[t]), f'comparability "{comp[:70]}" fits the type "{t}"')
        rule('D2', fid, not (t == R.CONF and re.search(r'not a confirmed (numerical )?contradiction', r['explanation'] + r['nature'], re.I)),
             'a confirmed contradiction is not described as "not a confirmed contradiction"')
        ns, fu_c = r['recommended_next_step'].lower(), r['follow_up_category']
        rule('D3', fid, not (re.search(r'\bask the supplier|confirm with (the supplier|s-oil|afton)', ns) and fu_c not in ('Supplier clarification',)
                             and 'optional' not in ns), f'next step "{r["recommended_next_step"][:60]}" agrees with follow-up "{fu_c}"')
        rule('D4', fid, not (fu_c == 'No follow-up needed beyond documentation' and r['verification_priority']),
             'a finding needing no follow-up has no open verification item')
        rule('D5', fid, not (r['verification_level'] == 'Verified' and re.search(r'not re-read|quoted from the JSON', r['verification_status'])),
             'a "Verified" level is not paired with "not re-read" evidence')
        rule('D6', fid, not (t == 'Edition difference' and 'dated editions' in comp and re.search(r'\(not printed\)', r['source_documents_and_pages'])
                             and len(re.findall(r'\(not printed\)', r['source_documents_and_pages'])) >= 2),
             'an edition difference said to be between dated editions cites dated documents')
        rule('D7', fid, not (fu_c == 'Supplier clarification' and 'supplier contact is not required' in r['follow_up_reason'].lower()),
             'supplier-clarification follow-up does not say supplier contact is not required')

    print(f'\nchecks run: {K.n}; failed: {len(K.fails)}')
    print('OVERALL:', 'PASS' if not K.fails else 'FAIL')
    return 1 if K.fails else 0


if __name__ == '__main__':
    sys.exit(main())
