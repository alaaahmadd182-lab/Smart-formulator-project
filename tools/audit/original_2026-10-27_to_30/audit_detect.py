"""Independent detectors over the current dataset (read-only). Writes audit/candidates.json for triage."""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

P = A.load_products(); ar = A.Archive()
REG = {e['url']: e for e in json.load(open(os.path.join(A.REPO, 'source_registry.json'), encoding='utf-8'))['sources']}
C = collections.defaultdict(list)
COMMON = re.compile(r'(?i)\b(the|and|of|for|with|product|data|value|density|viscosity|point|test|method|typical)\b')


def leaf(path):
    ks = [k for k in re.split(r'[.\[\]]', path) if k and not k.isdigit()]
    return ks[-1] if ks else path


def page_state(f, pg):
    if not f: return 'no source'
    if str(f).startswith('http'): return 'external'
    e = ar.get(f)
    if e is None: return 'not in archive'
    if not e.get('chars'): return 'image-only'
    if not isinstance(pg, int): return 'no page'
    t = ar.page_text(f, pg)
    if t is None: return 'page out of range'
    if len(t.strip()) < 40: return 'page has no text'
    if len(COMMON.findall(t)) < 2 and len(t) > 200: return 'text layer unreadable'
    return 'readable'


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def add(det, p, tk, path, **kw):
    t = p['tiers'][tk]
    C[det].append(dict(record_id=p['record_id'], folder=p['folder'], material_class=p['class'], tier=tk, file=t['file'], path=path, **kw))


TEMP_RE = re.compile(r'(?<![\w.])(-?\d+(?:[.,]\d+)?)\s*(?:°|º|˚)?\s*(?:C\b|℃|deg\s*C)', re.I)
F_RE = re.compile(r'(-?\d+(?:[.,]\d+)?)\s*(?:°|º)?\s*F\b')
TEMP_PROPS = {'kv40', 'kv100', 'density', 'ccs', 'ccs_viscosity', 'mrv', 'mrv_viscosity', 'hths', 'specific_gravity'}

for folder, p in P.items():
    vals = {}  # property leaf -> list of (tk, path, node)
    for tk, t in p['tiers'].items():
        d = t['doc']
        for path, n, parent in A.value_objects(d.get('fields', {})):
            vals.setdefault(leaf(path), []).append((tk, path, n))
            st = str(n.get('status')); v = n.get('value'); f, pg, rev = A.src_of(n)
            lo, hi = num(n.get('min')), num(n.get('max'))
            # --- status vs evidence
            if st == 'Missing' and (v not in (None, '', []) or lo is not None or hi is not None):
                add('status_missing_with_value', p, tk, path, value=v, min=lo, max=hi, status=st)
            if st in ('Reported', 'Calculated') and v in (None, '', []) and lo is None and hi is None:
                add('status_reported_without_value', p, tk, path, status=st, printed_text=n.get('printed_text'))
            if st == 'Calculated' and not n.get('calculation_note'):
                add('calculated_without_note', p, tk, path, value=v)
            if st in ('Not Applicable', 'Not Required', 'N/A') and not (n.get('notes') or n.get('calculation_note')):
                add('na_without_reason', p, tk, path, status=st)
            if st == 'Reported':
                if n.get('basis') == 'general_knowledge': add('reported_general_knowledge', p, tk, path, value=v, notes=n.get('notes'))
                if not f: add('reported_without_source', p, tk, path, value=v)
                elif str(f).startswith('http'):
                    r = REG.get(f)
                    if not r or r.get('status') != 'verified': add('reported_unverified_url', p, tk, path, url=f, reg=(r or {}).get('status'))
                    elif r.get('issuer') == 'third-party': add('reported_third_party', p, tk, path, url=f)
                elif pg in (None, ''): add('reported_archive_no_page', p, tk, path, src_file=f)
                # number on cited page?
                state = page_state(f, pg)
                nv = num(v) if num(v) is not None else (lo if lo is not None else hi)
                if state == 'readable' and nv is not None:
                    page_nums = A.numbers(ar.page_text(f, pg))
                    pt_nums = A.numbers(n.get('printed_text'))
                    ok = any(abs(nv - x) < 1e-9 for x in page_nums)
                    if not ok:
                        # value may be printed in another unit/format (e.g. 0,31 cm2/s (31 cSt)); try printed_text numbers
                        ok_pt = any(any(abs(a - b) < 1e-9 for b in page_nums) for a in pt_nums)
                        add('reported_value_not_on_page', p, tk, path, value=nv, unit=n.get('unit'), src_file=f, page=pg,
                            printed_text=n.get('printed_text'), printed_numbers_on_page=ok_pt)
                elif state not in ('readable', 'external', 'no page'):
                    C['_page_state'].append(state)
            # --- value vs printed text
            pt = n.get('printed_text'); nv = num(v)
            if pt and nv is not None and st in ('Reported', 'Calculated'):
                pn = A.numbers(pt)
                if pn and not any(abs(nv - x) < 1e-9 for x in pn) and st == 'Reported':
                    add('value_not_in_printed_text', p, tk, path, value=nv, unit=n.get('unit'), printed_text=pt, src_file=f, page=pg)
            # --- limits
            if nv is not None and lo is not None and hi is not None and not lo <= nv <= hi:
                add('value_outside_own_range', p, tk, path, value=nv, min=lo, max=hi)
            q = str(n.get('qualifier') or ''); vk = str(n.get('value_kind') or '')
            if q in ('>', '≥', '>=', '<', '≤', '<=', 'min', 'max', 'Min', 'Max') and vk in ('typical',):
                add('bound_marked_typical', p, tk, path, value=v, qualifier=q, value_kind=vk, printed_text=pt)
            if vk in ('specification', 'limit', 'minimum', 'maximum') and not q and lo is None and hi is None:
                add('specification_without_bound', p, tk, path, value=v, value_kind=vk, printed_text=pt)
            for ae in n.get('alternate_entries') or []:
                if not isinstance(ae, dict): continue
                alo, ahi = num(ae.get('min')), num(ae.get('max'))
                if nv is not None and ((alo is not None and nv < alo) or (ahi is not None and nv > ahi)):
                    add('typical_outside_alternate_limit', p, tk, path, value=nv, alternate=ae)
                av = num(ae.get('value'))
                if av is not None and nv is not None and av != nv and str(ae.get('value_kind') or '') == vk:
                    add('alternate_same_kind_differs', p, tk, path, value=nv, alternate=ae)
            # --- temperatures
            lf = leaf(path); tt = n.get('test_temperature_c')
            if lf == 'kv40' and tt not in (None, 40): add('kv_temperature_mismatch', p, tk, path, test_temperature_c=tt)
            if lf == 'kv100' and tt not in (None, 100): add('kv_temperature_mismatch', p, tk, path, test_temperature_c=tt)
            if pt and lf in TEMP_PROPS and tt is not None:
                temps = [float(x.replace(',', '.')) for x in TEMP_RE.findall(pt)]
                if temps and not any(abs(tt - x) < 0.051 for x in temps):
                    add('printed_temperature_differs', p, tk, path, test_temperature_c=tt, printed_text=pt, printed_temps=temps)
            if pt and F_RE.search(pt) and lf in ('flash_point', 'pour_point', 'cloud_point') and nv is not None:
                fs = [float(x.replace(',', '.')) for x in F_RE.findall(pt)]
                if any(abs(x - nv) < 1e-9 for x in fs) and str(n.get('unit') or '') in ('°C', 'C', '℃'):
                    add('fahrenheit_value_stored_as_celsius', p, tk, path, value=nv, printed_text=pt, unit=n.get('unit'))
            # --- units
            u = str(n.get('unit') or '')
            if lf == 'density' and nv is not None:
                if u.lower() in ('kg/m3', 'kg/m³') and nv < 100: add('density_unit_magnitude', p, tk, path, value=nv, unit=u, printed_text=pt)
                if u.lower() in ('g/cm3', 'g/cm³', 'g/ml', 'kg/l', 'kg/dm3') and nv > 10: add('density_unit_magnitude', p, tk, path, value=nv, unit=u, printed_text=pt)
            if u in ('wt.% or ppm as printed', 'kg/m3 (or as printed)', 'not printed') and st == 'Reported':
                add('ambiguous_unit', p, tk, path, value=v, unit=u, printed_text=pt)
            if pt and nv is not None and lf in ('sulfur', 'Zn', 'P', 'Ca', 'Mg', 'B', 'Mo', 'N', 'S'):
                ptl = pt.lower()
                if ('ppm' in ptl or 'mg/kg' in ptl) and ('%' in u or 'wt' in u.lower()) and 'ppm' not in u.lower():
                    add('ppm_printed_wt_stored', p, tk, path, value=nv, unit=u, printed_text=pt)
                if ('%' in ptl or 'wt' in ptl) and 'ppm' in u.lower() and 'ppm' not in ptl and 'mg/kg' not in ptl:
                    add('wt_printed_ppm_stored', p, tk, path, value=nv, unit=u, printed_text=pt)
            # --- normalised layer
            if 'value_final' in n:
                if n.get('value_final') is None and v is not None and nv is not None:
                    add('final_nulled', p, tk, path, value=v, unit=u, flags=n.get('integration_flags'))
                for fl in n.get('integration_flags') or []:
                    C['_flags'].append(re.sub(r"[-\d.]+ °C|'[^']*'|\d[\d.]*", '#', fl))
            elif num(v) is not None:
                C['_no_final_numeric'].append((p['record_id'], tk, path))
    # --- physical consistency within a product (all tiers)
    def first(name, pred=lambda n: True):
        for tk, path, n in vals.get(name, []):
            if path.count('.') == 0 and num(n.get('value')) is not None and pred(n): return tk, path, n
        return None
    kv40, kv100 = first('kv40'), first('kv100')
    if kv40 and kv100 and kv40[2]['value'] <= kv100[2]['value']:
        add('kv40_not_above_kv100', p, kv40[0], 'kv40/kv100', kv40=kv40[2]['value'], kv100=kv100[2]['value'])
    pp, cp, fp = first('pour_point'), first('cloud_point'), first('flash_point')
    if pp and cp and pp[2]['value'] > cp[2]['value'] + 3:
        add('pour_above_cloud', p, pp[0], 'pour_point/cloud_point', pour=pp[2]['value'], cloud=cp[2]['value'])
    if pp and fp and fp[2]['value'] <= pp[2]['value']:
        add('flash_below_pour', p, fp[0], 'flash_point/pour_point', flash=fp[2]['value'], pour=pp[2]['value'])
    sat, aro = first('saturates'), first('aromatics')
    if sat and aro and sat[2]['value'] + aro[2]['value'] > 100.5:
        add('saturates_plus_aromatics_over_100', p, sat[0], 'saturates/aromatics', saturates=sat[2]['value'], aromatics=aro[2]['value'])
    den, sg = first('density'), first('specific_gravity')
    if den and sg:
        dv = den[2]['value'] * (0.001 if str(den[2].get('unit', '')).lower() in ('kg/m3', 'kg/m³') else 1)
        dt, st_ = den[2].get('test_temperature_c'), sg[2].get('test_temperature_c')
        if dt is not None and st_ is not None and abs(dt - st_) <= 5 and abs(dv - sg[2]['value']) > 0.01:
            add('density_vs_specific_gravity', p, den[0], 'density/specific_gravity', density=den[2]['value'], density_unit=den[2].get('unit'),
                density_t=dt, sg=sg[2]['value'], sg_t=st_)
    # CCS / MRV monotonic in temperature
    for name, sub in (('ccs', 'ccs_viscosity'), ('mrv', 'mrv_viscosity')):
        pts = []
        for tk, t in p['tiers'].items():
            arr = t['doc'].get('fields', {}).get(name)
            if isinstance(arr, list):
                for i, e in enumerate(arr):
                    if not isinstance(e, dict): continue
                    node = e.get(sub) if isinstance(e.get(sub), dict) else e
                    tv = e.get('temperature_c', node.get('test_temperature_c') if isinstance(node, dict) else None)
                    vv = num(node.get('value')) if isinstance(node, dict) else None
                    if tv is not None and vv is not None: pts.append((tv, vv, tk, f'{name}[{i}]'))
        pts.sort()
        for (t1, v1, tk1, p1), (t2, v2, tk2, p2) in zip(pts, pts[1:]):
            if t1 < t2 and v1 < v2:
                add('lowtemp_viscosity_not_monotonic', p, tk1, f'{p1} vs {p2}', colder=(t1, v1), warmer=(t2, v2))
            if t1 == t2 and v1 != v2:
                add('lowtemp_duplicate_temperature', p, tk1, f'{p1} vs {p2}', temperature=t1, values=(v1, v2))
    # API group vs properties (API 1509 Annex E: sat >= 90 %, S <= 0.03 %, VI 80-<120 Group II, >= 120 Group III)
    if p['class'] == 'base_oil':
        g = None
        for tk, t in p['tiers'].items():
            agc = t['doc'].get('fields', {}).get('api_group_chemistry', {})
            node = agc.get('api_group') if isinstance(agc, dict) else None
            if isinstance(node, dict) and node.get('value'): g = (tk, str(node['value']), node, agc.get('chemistry'))
        vi = first('viscosity_index'); s = first('sulfur')
        if g:
            gl = g[1].upper().replace('GROUP', '').strip()
            sval = None
            if s:
                su = str(s[2].get('unit') or '').lower(); sval = s[2]['value'] / 10000 if 'ppm' in su or 'mg/kg' in su else (s[2]['value'] if ('%' in su or 'wt' in su) else None)
            facts = dict(api_group=g[1], vi=vi[2]['value'] if vi else None, sulfur_wt_pct=sval, saturates=sat[2]['value'] if sat else None)
            issues = []
            core = re.sub(r'[^IV+]', '', gl)
            if core.startswith('III') and vi and vi[2]['value'] < 120: issues.append('Group III with VI < 120')
            if core in ('II', 'II+') and vi and vi[2]['value'] >= 120: issues.append('Group II with VI >= 120')
            if core in ('II', 'II+', 'III', 'III+') and vi and vi[2]['value'] < 80: issues.append('Group II/III with VI < 80')
            if core in ('II', 'II+', 'III', 'III+') and sval is not None and sval > 0.03: issues.append('Group II/III with sulfur > 0.03 wt.%')
            if core in ('II', 'II+', 'III', 'III+') and sat and sat[2]['value'] < 90: issues.append('Group II/III with saturates < 90 %')
            if core == 'I' and sat and sat[2]['value'] >= 90 and sval is not None and sval <= 0.03: issues.append('Group I with saturates >= 90 % and sulfur <= 0.03 %')
            chem = json.dumps(g[3], ensure_ascii=False).lower() if g[3] else ''
            if core == 'IV' and chem and 'pao' not in chem and 'polyalphaolefin' not in chem and 'poly-alpha' not in chem and 'polyalpha' not in chem:
                issues.append('Group IV but chemistry does not name PAO')
            if core != 'IV' and ('polyalphaolefin' in chem or 'poly-alpha' in chem or re.search(r'\bpao\b', chem)) and 'not' not in chem:
                issues.append('PAO chemistry but not Group IV')
            if issues: add('api_group_vs_properties', p, g[0], 'api_group_chemistry.api_group', issues=issues, **facts)
            C['_api_labels'].append(g[1])
    # cross-tier product block
    blocks = {tk: t['doc'].get('product', {}) or {} for tk, t in p['tiers'].items()}
    for k in sorted({k for b in blocks.values() for k in b}):
        seen = {json.dumps(b.get(k), ensure_ascii=False, sort_keys=True) for b in blocks.values() if k in b}
        if len(seen) > 1: add('cross_tier_product_block', p, next(iter(blocks)), f'product.{k}', values={tk: b.get(k) for tk, b in blocks.items()})
    rids = {tk: t['doc'].get('record_id') for tk, t in p['tiers'].items()}
    if len(set(rids.values())) > 1 or p['record_id'] not in rids.values():
        add('record_id_mismatch', p, next(iter(rids)), 'record_id', values=rids, folder_id=p['record_id'])
    tv = {tk: t['doc'].get('template_version') for tk, t in p['tiers'].items()}
    if len(set(tv.values())) > 1: add('cross_tier_template_version', p, next(iter(tv)), 'template_version', values=tv)
    # same property in several tiers with different values
    for name, lst in vals.items():
        tiers = {tk for tk, _, _ in lst}
        if len(tiers) > 1:
            vv = {(tk, path): (n.get('value'), n.get('unit'), n.get('status')) for tk, path, n in lst if path.count('.') == 0 and '[' not in path}
            if len({json.dumps(x, ensure_ascii=False) for x in vv.values()}) > 1 and len({k[0] for k in vv}) > 1:
                add('cross_tier_property_differs', p, next(iter(tiers)), name, values={f'{k[0]}:{k[1]}': x for k, x in vv.items()})
    # open questions that mention a discrepancy
    for tk, t in p['tiers'].items():
        for q in t['doc'].get('open_questions', []):
            text = q if isinstance(q, str) else ' '.join(str(x) for x in q.values())
            if re.search(r'(?i)differ|discrepan|inconsisten|contradict|conflict|mismatch|disagree|does not match|swapped|whereas', text):
                C['_oq_discrepancy'].append(dict(record_id=p['record_id'], folder=folder, tier=tk, file=t['file'], text=text))

# identity: duplicate names, supplier variants
names = collections.defaultdict(list); sup = collections.defaultdict(set)
for folder, p in P.items():
    nm = None
    for t in p['tiers'].values():
        pr = t['doc'].get('product', {}) or {}
        nm = nm or pr.get('product_name'); sup[p['supplier_folder']].add(pr.get('supplier'))
    key = re.sub(r'[^a-z0-9]', '', str(nm or '').lower().replace('®', '').replace('™', ''))
    names[key].append(folder)
for k, v in names.items():
    if len(v) > 1: C['duplicate_product_name'].append(dict(name_key=k, folders=v))
for k, v in sup.items():
    if len(v) > 1: C['supplier_name_variants'].append(dict(supplier_folder=k, names=sorted(map(str, v))))

json.dump(C, open(os.path.join(A.SCR, 'audit', 'candidates.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
for k in sorted(C):
    v = C[k]
    print(f'{k}: {len(v)}' + (f'  {collections.Counter(v).most_common(8)}' if k in ('_page_state', '_flags', '_api_labels') else ''))
