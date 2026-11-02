"""Phase B validation of the reconciled Products_json (working tree) against HEAD, origin/main and the templates.

Usage: python validate.py <repo> <integrate_products.py from origin/main> <resolve_json.py> <out.json>
"""
import collections, copy, importlib.util, json, os, re, subprocess, sys
from decimal import Decimal
sys.stdout.reconfigure(encoding='utf-8')
repo, ip_path, rj_path, out_path = sys.argv[1:5]
def mod(name, p):
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ip = mod('ip', ip_path)
OWN = set(ip.OWN_KEYS)
ALLOWED_STATUS = set(json.load(open(os.path.join(repo, 'json_templates', 'base_oil_tier1_blocking.json'), encoding='utf-8'))['_template_notes']['status_vocabulary']) | {'N/A'}
TOP = ('template_version', 'material_class', 'tier', 'tier_label', 'record_id', 'product', 'fields', 'open_questions', 'conflicts')
# keys that may only appear because a rejected override was carried over
FORBIDDEN_FINAL = {'status_final', 'source_final', 'qualifier_final', 'method_final', 'test_temperature_c_final'}


def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=off', *a], cwd=repo, capture_output=True, check=True).stdout


def tree(rev):
    return sorted(f for f in git('ls-tree', '-r', '--name-only', '-z', rev, 'Products_json').decode('utf-8').split('\0') if f.endswith('.json'))


def work_files():
    out = []
    root = ip.long_path(os.path.normpath(os.path.join(repo, 'Products_json')))
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.json'):
                rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/')
                out.append('Products_json/' + rel)
    return sorted(out)


def read_work(f):
    with open(ip.long_path(os.path.normpath(os.path.join(repo, f))), encoding='utf-8') as fh:
        return fh.read()


def collect(node, path, out):
    if isinstance(node, dict):
        if 'status' in node and 'value' in node and not isinstance(node['status'], dict):
            out[path] = node
        for k, v in node.items():
            if k not in ('source', 'alternate_entries') and k not in OWN:
                collect(v, f'{path}.{k}' if path else k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            collect(v, f'{path}[{i}]', out)


def strip(d):
    d = copy.deepcopy(d)
    def rec(n):
        if isinstance(n, dict):
            for k in list(n):
                if k in OWN: n.pop(k)
            for v in n.values(): rec(v)
        elif isinstance(n, list):
            for v in n: rec(v)
    rec(d.get('fields', {}))
    for c in d.get('conflicts', []):
        if isinstance(c, dict): c.pop('resolved', None); c.pop('final_resolution', None)
    return d


def statuses(node, out):
    if isinstance(node, dict):
        if 'status' in node and not isinstance(node['status'], dict): out.append(node['status'])
        for k, v in node.items():
            if k not in ('source',): statuses(v, out)
    elif isinstance(node, list):
        for v in node: statuses(v, out)


def sources(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ('source', 'source_file') and v:
                for s in (v if isinstance(v, list) else [v]):
                    if isinstance(s, dict) and (s.get('file') or s.get('url')): out.add((s.get('file') or s.get('url'), str(s.get('page'))))
                    elif isinstance(s, str): out.add((s, ''))
            sources(v, out)
    elif isinstance(node, list):
        for v in node: sources(v, out)


TEMPLATES = {}
for t in os.listdir(os.path.join(repo, 'json_templates')):
    d = json.load(open(os.path.join(repo, 'json_templates', t), encoding='utf-8'))
    TEMPLATES[t] = d


def template_for(f, d):
    base = os.path.basename(f)
    if d.get('material_class') == 'additive_component':
        return {'general.json': 'additive_component_all_general.json', 'vm.json': 'additive_component_vm.json',
                'ppd.json': 'additive_component_ppd.json'}.get(base)
    for name, t in TEMPLATES.items():
        if t['material_class'] == d.get('material_class') and t['tier'] == d.get('tier'):
            return name


def template_findings(f, d):
    out = []
    for k in TOP:
        if k not in d: out.append(f'missing top-level key {k}')
    tn = template_for(f, d)
    if not tn: return out + ['no matching template']
    t = TEMPLATES[tn]
    if d.get('tier') != t['tier']: out.append(f'tier {d.get("tier")} != template {t["tier"]}')
    if d.get('tier_label') != t['tier_label']: out.append(f'tier_label differs from template')
    for k in t['fields']:
        if k not in d.get('fields', {}) and k != 'specific_gravity': out.append(f'template field absent: {k}')
    for k in d.get('fields', {}):
        if k not in t['fields']: out.append(f'field not in template: {k}')
    st = []; statuses(d.get('fields', {}), st)
    for s in st:
        if s not in ALLOWED_STATUS: out.append(f'status not allowed: {s!r}')
    return out


R = collections.defaultdict(list); C = collections.Counter()
head_t, main_t, work_t = tree('HEAD'), tree('origin/main'), work_files()
C['files_head'], C['files_main'], C['files_work'] = len(head_t), len(main_t), len(work_t)
if set(head_t) != set(work_t): R['file_set_differs_from_head'] = sorted(set(head_t) ^ set(work_t))
if not set(main_t) <= set(work_t): R['main_files_missing'] = sorted(set(main_t) - set(work_t))
ids_head, ids_work = set(), set()
src_head, src_work = set(), set()
tf_head, tf_work = collections.Counter(), collections.Counter()
for f in work_t:
    raw = read_work(f)
    if re.search(r'^(<<<<<<<|>>>>>>>|=======$)', raw, re.M): R['conflict_markers'].append(f)
    try:
        w = json.loads(raw)
    except Exception as e:
        R['invalid_json'].append((f, str(e))); continue
    C['parsed'] += 1
    h = json.loads(git('show', f'HEAD:{f}').decode('utf-8')) if f in head_t else None
    m = json.loads(git('show', f'origin/main:{f}').decode('utf-8')) if f in main_t else None
    # 1. no loss vs HEAD: original content identical
    if h is not None and strip(w) != h: R['original_content_changed_vs_head'].append(f)
    ids_work.add((w.get('record_id'), w.get('material_class'), w.get('tier'), os.path.basename(f)))
    if h is not None: ids_head.add((h.get('record_id'), h.get('material_class'), h.get('tier'), os.path.basename(f)))
    sources(w, src_work)
    if h is not None: sources(h, src_head)
    # 2. templates (compare with HEAD)
    for x in template_findings(f, w): tf_work[re.sub(r': .*', '', x)] += 1; R['template_findings_work'].append((f, x))
    if h is not None:
        for x in template_findings(f, h): tf_head[re.sub(r': .*', '', x)] += 1
    # 3. finals: forbidden keys, staleness, conversions
    wn = {}; collect(w.get('fields', {}), '', wn)
    for p, n in wn.items():
        own = {k: n[k] for k in n if k in OWN}
        if not own: C['nodes_without_finals'] += 1; continue
        C['nodes_with_finals'] += 1
        bad = FORBIDDEN_FINAL & set(own)
        if bad: R['forbidden_final_keys'].append((f, p, sorted(bad)))
        e = copy.deepcopy({k: v for k, v in n.items() if k not in OWN}); fl = ip.normalise(e, p)
        if fl: e['integration_flags'] = fl
        exp = {k: e[k] for k in e if k in OWN}
        if 'resolution' in own: exp['resolution'] = own['resolution']; C['resolution_annotations'] += 1
        if own != exp: R['stale_finals'].append((f, p, own, exp))
        # dimensional check of conversions
        u, uf = n.get('unit'), own.get('unit_final')
        if uf is not None and u is not None:
            C[f'conversion {u!r} -> {uf!r}'] += 1
        for k in ('value', 'min', 'max'):
            v, vf = n.get(k), own.get(f'{k}_final')
            if isinstance(v, (int, float)) and not isinstance(v, bool) and vf is not None and isinstance(vf, (int, float)):
                fam = ip.family(p); rule = ip.UNITS.get(fam, {}).get(str(u).strip().lower()) if fam else None
                factor = Decimal(rule[1]) if rule else Decimal(1)
                if abs(Decimal(str(v)) * factor - Decimal(str(vf))) > Decimal('0.0001') * max(Decimal(1), abs(Decimal(str(vf)))):
                    R['conversion_mismatch'].append((f, p, k, v, u, vf, uf))
        if ip.family(p) == 'density' and own.get('value_final') is not None and n.get('test_temperature_c') is None and \
                not any('no temperature' in x for x in own.get('integration_flags', [])):
            R['density_temperature_not_flagged'].append((f, p))
    # 4. conflicts
    hc = h.get('conflicts', []) if h else []
    if len(w.get('conflicts', [])) != len(hc): R['conflict_count_changed'].append(f)
    for c in w.get('conflicts', []):
        C['conflict_entries'] += 1
        if isinstance(c, dict) and 'resolved' in c:
            C[f"conflict resolved={c['resolved']}"] += 1
    # 5. main's finals accounted for
    if m is not None:
        mn = {}; collect(m.get('fields', {}), '', mn)
        for p, n in mn.items():
            if any(k in n for k in OWN):
                C['main_nodes_with_finals'] += 1
                if p not in wn: C['main_final_node_path_absent_in_work'] += 1
                elif any(k in wn[p] for k in OWN):
                    C['main_final_node_kept'] += 1
                else:
                    C['main_final_node_dropped'] += 1

C['record_tier_ids_head'], C['record_tier_ids_work'] = len(ids_head), len(ids_work)
if not ids_head <= ids_work: R['record_tiers_lost'] = sorted(map(str, ids_head - ids_work))
C['source_refs_head'], C['source_refs_work'] = len(src_head), len(src_work)
if src_head - src_work: R['source_refs_lost'] = sorted(map(str, src_head - src_work))
if src_work - src_head: R['source_refs_added'] = sorted(map(str, src_work - src_head))
R['template_finding_counts_head'] = dict(tf_head); R['template_finding_counts_work'] = dict(tf_work)
with open(out_path, 'w', encoding='utf-8') as fh:
    json.dump({'counts': C, 'results': R}, fh, indent=1, ensure_ascii=False, default=str)
for k, v in sorted(C.items()): print(f'{k}: {v}')
for k, v in R.items():
    if k.startswith('template_finding'): print(k, v)
    elif k != 'template_findings_work': print(f'{k}: {len(v)}', v[:5] if isinstance(v, list) else v)
