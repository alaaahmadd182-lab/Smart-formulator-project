import json
R = 'C:\\Users\\windo\\sf-wsA\\'


def load(rel):
    return open(R + rel, encoding='utf-8').read()


def save(rel, s):
    open(R + rel, 'w', encoding='utf-8', newline='\n').write(s)


def sub(s, a, b):
    assert s.count(a) == 1, (a[:80], s.count(a))
    return s.replace(a, b)


# ---------------------------------------------------------------- evidence items get their registry URL
p = 'tools\\data_policy\\external_review_decisions.json'
d = json.loads(load(p))
reg = {s['url']: s for s in json.loads(load('source_registry.json'))['sources']}
URLS = {
    'aramco_prima230_sheet': 'https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramcoprima/aramcoprima_2021_december/aramcoprima-230_yanbu_ar.pdf?hash=35009BCB03F8661F4C2220E5BC82ED39EAFE713F&la=ar',
    'luberef_prima230_sds': 'https://luberefapp.s3-accelerate.amazonaws.com/documents/prima230-1664376579.pdf',
    'mogo_flyer_2025': 'https://specs.ergonspecialtyoils.com/mogoil/MOGO-2025_Base%20Oils_Flyer_a4_Digital.pdf',
    'aramco_catalog_2024': 'https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramco-base-oil-catalog-2024.pdf',
    'richful_feed_109': 'https://www.richful.com/catalogueDetail.html?id=109',
    'richful_feed_130': 'https://www.richful.com/catalogueDetail.html?id=130',
    'soil_page_wayback': 'https://www.s-oil.com/en/energy/LubeBaseOil.aspx',
    'soil_page_live': 'https://www.s-oil.com/en/energy/LubeBaseOil.aspx',
    'afton_12204l_pds': 'https://web.archive.org/web/20201023085523id_/https://www.aftonchemical.com/Afton/media/AftonSBU/Engine/PDS/HiTEC-12204L/HiTEC-12204L_PDS.pdf?ext=.pdf',
    'afton_8788b_pds': 'https://web.archive.org/web/20221204124252/https://www.aftonchemical.com/Afton/media/AftonSBU/Engine/PDS/HiTEC-8788B/HiTEC-8788B_PDS.pdf?ext=.pdf',
}
assert set(URLS) == set(d['evidence'])
for k, u in URLS.items():
    assert u in reg, k
    d['evidence'][k]['registry_url'] = u
save(p, json.dumps(d, ensure_ascii=False, indent=1) + '\n')

# ---------------------------------------------------------------- inventory
p = 'tools\\data_policy\\tds_sds_inventory.py'
s = load(p)
s = sub(s, """Document class per (file, page) comes from reports/data_policy/document_classes.csv.
""", """  4. reviewed SDS values from the lead review, paired with the record's selected technical value.
Document class per (file, page) comes from reports/data_policy/document_classes.csv.

External (URL) sources. A URL registered in source_registry.json takes part in the pairing like an archive document:
its class is TECHNICAL, or SDS when its registry title names a safety data sheet. An unregistered URL is never paired.
One URL is one source however many saved copies of it exist, so identical copies cannot produce duplicate pairs, and a
pair found both in conflicts[] and through an alternate entry is one row (the origins are joined). For an external
side the row carries the evidence state from the external review (external_review_decisions.json): if no copy of the
source could be obtained, the value was not re-read and the pair is 'comparability unknown', whatever the numbers.
The inventory records relations between documents; it never selects a source and never resolves a disagreement.
""")
s = sub(s, """FINDINGS = os.path.join(P.ROOT, 'tools', 'audit', 'review_2026-11-02', 'output', 'findings_v5.json')
""", """FINDINGS = os.path.join(P.ROOT, 'tools', 'audit', 'review_2026-11-02', 'output', 'findings_v5.json')
REGISTRY = os.path.join(P.ROOT, 'source_registry.json')
EXTERNAL_DECISIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'external_review_decisions.json')
NOT_OBTAINED = 'external source not obtained: value not re-read'


def is_url(f):
    return str(f or '').lower().startswith(('http://', 'https://'))


def load_external():
    \"\"\"(registry by URL, evidence state by URL). State: 'not_obtained' if no copy of the source could be obtained in the
    external review, 'copy_read' if a copy was read there, otherwise the registry status (not re-read in that review).\"\"\"
    with open(REGISTRY, encoding='utf-8') as fh:
        reg = {x['url']: x for x in json.load(fh)['sources']}
    with open(EXTERNAL_DECISIONS, encoding='utf-8') as fh:
        ev = json.load(fh)['evidence']
    state = {}
    for e in ev.values():
        u = e.get('registry_url')
        if u:
            got = e.get('authenticity') != 'not_obtained'
            state[u] = 'copy_read' if got or state.get(u) == 'copy_read' else 'not_obtained'
    return reg, state


def external_class(f, reg):
    \"\"\"TECHNICAL or SDS for a registered URL (by its registry title); None for an unregistered URL.\"\"\"
    e = reg.get(str(f))
    if not e:
        return None
    return 'SDS' if re.search(r'safety data sheet|\\bmsds\\b', e.get('title') or '', re.I) else 'TECHNICAL'


def external_state(f, reg, state):
    if not is_url(f):
        return ''
    if state.get(str(f)) == 'not_obtained':
        return NOT_OBTAINED
    if state.get(str(f)) == 'copy_read':
        return 'copy read in the external review'
    e = reg.get(str(f)) or {}
    return f"registry status {e.get('status')} (checked {e.get('checked')}); not re-read in the external review"


def apply_evidence_state(r, states):
    \"\"\"A pair with an external side that could not be obtained is never screened: the value was not verified.\"\"\"
    if NOT_OBTAINED in states:
        r = dict(r, comparability='comparability unknown', reason=NOT_OBTAINED + ('; ' + r['reason'] if r.get('reason') else ''))
        for k in ('bound_satisfied', 'abs_diff', 'rel_diff_pct', 'within_rounding', 'tds_canonical', 'sds_canonical', 'rounding_tolerance'):
            r.pop(k, None)
    return r


def rev_date(v):
    s2 = v.get('source') if isinstance(v.get('source'), dict) else {}
    return v.get('revision_date') or s2.get('revision_date') or ''
""")
s = sub(s, """    def c_of(f, pg):
        pgs = re.findall(r'\\d+', str(pg)) if pg not in (None, '') else []
        return cls.get((str(f), pgs[0] if pgs else ''))
""", """    reg, ext_state = load_external()

    def c_of(f, pg):
        if is_url(f):
            return external_class(f, reg)
        pgs = re.findall(r'\\d+', str(pg)) if pg not in (None, '') else []
        return cls.get((str(f), pgs[0] if pgs else ''))
""")
s = sub(s, """        if key in pairs:
            pairs[key]['origin'] += '; ' + origin
        else:""", """        if key in pairs:
            pairs[key]['origin'] += '; ' + origin
            if origin.startswith('alternate entry') and (is_url(tds.get('file')) or is_url(sds.get('file'))):
                # the same pair as a conflicts[] entry: one row; the value objects carry unit, temperature, method and kind
                pairs[key].update(tds=tds, sds=sds)
        else:""")
s = sub(s, """        r = compare(x['property'], x['tds'], x['sds'])
        grp""", """        states = [external_state(x[k].get('file'), reg, ext_state) for k in ('tds', 'sds')]
        r = apply_evidence_state(compare(x['property'], x['tds'], x['sds']), states)
        r.update(tds_source='external' if is_url(x['tds'].get('file')) else 'archive', sds_source='external' if is_url(x['sds'].get('file')) else 'archive',
                 tds_revision_date=rev_date(x['tds']), sds_revision_date=rev_date(x['sds']), external_evidence='; '.join(y for y in states if y))
        grp""")
s = sub(s, "'proposed_screen', 'thresholds_version', 'origin']", "'proposed_screen', 'thresholds_version', 'origin',\n            'tds_source', 'sds_source', 'tds_revision_date', 'sds_revision_date', 'external_evidence']")
s = sub(s, """    print(f'TDS-SDS comparisons: {len(rows)}')""", """    print(f'TDS-SDS comparisons: {len(rows)} (with an external side: {sum(1 for r in rows if "external" in (r["tds_source"], r["sds_source"]))})')""")
save(p, s)
print('ok')
