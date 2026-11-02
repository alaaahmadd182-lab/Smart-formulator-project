"""Resolve Products_json for the origin/main -> integration/reconcile-task3 merge.

Starting point for every file: our validated Task 3 version (HEAD).
From origin/main, carried over only:
  * normalised *_final keys of a value object, when re-deriving them from OUR current value object
    with main's own normalise() gives exactly main's keys (i.e. they are not stale);
  * resolution texts / conflict annotations that agree with the data rules approved 2026-10-24.
Nothing is averaged, no value is chosen between documents, no original key is changed.

Usage: python resolve_json.py <repo> <integrate_products.py from origin/main> <report.json> [--write]
"""
import copy, importlib.util, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
repo, ip_path, report_path = sys.argv[1:4]
WRITE = '--write' in sys.argv
spec = importlib.util.spec_from_file_location('ip', ip_path); ip = importlib.util.module_from_spec(spec); spec.loader.exec_module(ip)
OWN = set(ip.OWN_KEYS)
OURS, MAIN, BASE = 'HEAD', 'origin/main', '553a9fd696102fddfff3f6ecef291ddd8f10ddae'
RULES_NOTE = ('Not resolved. The resolution proposed on origin/main (integrate_products.py) was not adopted under the data '
              'rules approved on 2026-10-24: no automatic averaging of conflicting values and no automatic preference of '
              'TDS over SDS or vice versa. Both values and sources stay as recorded; pending human review. Proposal: ')

# ---- decisions on main's OVERRIDES (product, tier, path) ----
ACCEPT_ANNOTATION = {  # value unchanged; reasoning consistent with the approved rules (revision date / prior user decision)
    ('RICHFUL_RF6077', 2, 'density'), ('RICHFUL_RF6077', 2, 'kv100'),
    ('RICHFUL_RF6088F', 2, 'density'), ('RICHFUL_RF6088F', 2, 'kv100'),
    ('NYNAS_NS_3', 1, 'kv40'), ('NYNAS_NS_3', 1, 'density'), ('NYNAS_NS_3', 2, 'flash_point'), ('NYNAS_NS_3', 3, 'sulfur'),
    ('ARAMCO_LUBEREF_DURA_BS150_YANBU', 3, 'sulfur'), ('ERGON_HYGOLD_L750', 1, 'density'),
}
REJECT_VALUE = {  # override replaces the value (average, TDS-over-SDS, or typical-over-bound): carry no *_final keys
    ('INFINEUM_D3424', 2, 'flash_point'),
    ('RICHFUL_RF6066', 2, 'density'), ('RICHFUL_RF6066', 2, 'kv100'), ('RICHFUL_RF6066', 2, 'tbn'),
    ('RICHFUL_RF6066', 2, 'elements.Zn'), ('RICHFUL_RF6066', 2, 'elements.Ca'),
    ('RICHFUL_RF6069', 2, 'kv100'),
    ('RICHFUL_RF6078', 1, 'treat_rate_matrix[0].treat_rate_wt_pct'), ('RICHFUL_RF6078', 2, 'density'),
    ('RICHFUL_RF6406', 1, 'treat_rate_matrix[10].treat_rate_wt_pct'), ('RICHFUL_RF6406', 2, 'tbn'),
    ('PETRONAS_ETRO_6_PLUS', 1, 'density'),
}
REJECT_ANNOTATION = {  # value unchanged, but justified by the rejected TDS-preference rule: drop 'resolution' only
    ('RICHFUL_RF6081', 2, 'kv100'), ('FORMOSA_150N_GII_PLUS', 2, 'flash_point'),
    ('NYNAS_NYFROST_32', 1, 'kv40'), ('NYNAS_NYFROST_32', 2, 'flash_point'),
    ('PETRONAS_ETRO_6_PLUS', 1, 'kv40'), ('PETRONAS_ETRO_6_PLUS', 2, 'flash_point'), ('PETRONAS_ETRO_6_PLUS', 2, 'noack_volatility'),
    ('PETRO_CANADA_PURITY_L65', 1, 'viscosity_index'),
    ('SHELL_RISELLA_X_415', 1, 'density'), ('SHELL_RISELLA_X_420', 1, 'density'), ('SHELL_RISELLA_X_430', 1, 'density'),
}
assert ACCEPT_ANNOTATION | REJECT_VALUE | REJECT_ANNOTATION == set(ip.OVERRIDES) and \
       len(ACCEPT_ANNOTATION) + len(REJECT_VALUE) + len(REJECT_ANNOTATION) == len(ip.OVERRIDES)

# ---- decisions on main's CONFLICTS rules (product, substring) ----
CF_ACCEPT = {  # resolved/unresolved annotation kept exactly as main wrote it
    ('AFTON_HITEC_12200', 'MTU 2.0'), ('AFTON_HITEC_12200', 'DDC 93K215'),
    ('LUBRIZOL_CV7540', 'CES 20076'), ('LUBRIZOL_CV7540', 'CES 20077'), ('LUBRIZOL_CV7540', 'CES 20078'),
    ('NYNAS_NS_3', '"property": "kv40"'), ('NYNAS_NS_3', '"property": "density"'),
    ('NYNAS_NS_3', '"property": "flash_point"'), ('NYNAS_NS_3', '"property": "sulfur"'),
    ('RICHFUL_RF6077', 'tier2.density'), ('RICHFUL_RF6077', 'tier2.kv100'),
    ('RICHFUL_RF6088F', 'tier2.density'), ('RICHFUL_RF6088F', 'tier2.kv100'),
    ('ARAMCO_LUBEREF_DURA_BS150_YANBU', '"field": "density"'),
    ('ARAMCO_LUBEREF_DURA_BS150_YANBU', '"field": "sulfur"'), ('ERGON_HYGOLD_L750', 'density_at_15_6_c'),
}
CF_NOT_ADOPTED = {x[:2] for x in ip.CONFLICTS} - CF_ACCEPT
assert len(CF_NOT_ADOPTED) == 23, len(CF_NOT_ADOPTED)


def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=off', *a], cwd=repo, capture_output=True, check=True).stdout


def tree(rev):
    return {f for f in git('ls-tree', '-r', '--name-only', '-z', rev, 'Products_json').decode('utf-8').split('\0') if f.endswith('.json')}


def show(rev, f):
    return git('show', f'{rev}:{f}').decode('utf-8')


def collect(node, path, out):
    """Value objects by path, with the same traversal as integrate_products.walk (no modification)."""
    if isinstance(node, dict):
        if 'status' in node and 'value' in node and not isinstance(node['status'], dict):
            out[path] = node
        for k, v in node.items():
            if k not in ('source', 'alternate_entries') and k not in OWN:
                collect(v, f'{path}.{k}' if path else k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            collect(v, f'{path}[{i}]', out)


def strip_main(d):
    """main's document with everything integrate_products.py adds removed."""
    d = copy.deepcopy(d)
    def rec(n):
        if isinstance(n, dict):
            for k in list(n):
                if k in OWN: n.pop(k)
            for v in n.values(): rec(v)
        elif isinstance(n, list):
            for v in n: rec(v)
    rec(d.get('fields', {}))
    for i, c in enumerate(d.get('conflicts', [])):
        if isinstance(c, dict):
            c.pop('resolved', None); c.pop('final_resolution', None)
    return d


def expected_own(node, path):
    n = copy.deepcopy({k: v for k, v in node.items() if k not in OWN})
    flags = ip.normalise(n, path)
    if flags:
        n['integration_flags'] = flags
    return {k: n[k] for k in n if k in OWN}


def main_own(node):
    return {k: node[k] for k in node if k in OWN}


rep = {'files': 0, 'written': 0, 'unchanged_from_ours': 0, 'errors': [], 'kept_nodes': 0, 'stale_dropped': [],
       'no_main_counterpart': 0, 'override_decisions': [], 'conflict_decisions': [], 'review_flags': [], 'base_mismatch_strings': []}
ours_t, main_t, base_t = tree(OURS), tree(MAIN), tree(BASE)
for f in sorted(ours_t | main_t):
    rep['files'] += 1
    if f not in ours_t:
        rep['errors'].append((f, 'file exists only on main')); continue
    raw = show(OURS, f); ours = json.loads(raw)
    result = copy.deepcopy(ours)
    product, tier = os.path.basename(os.path.dirname(f)), ours.get('tier')
    if f in main_t:
        mdoc = json.loads(show(MAIN, f))
        if f not in base_t:
            rep['errors'].append((f, 'on main but not in merge base')); continue
        base = json.loads(show(BASE, f)); sm = strip_main(mdoc)
        # main may wrap bare-string conflicts as {"note": s}; compare with that unwrapped
        sm_cf = [c['note'] if isinstance(c, dict) and set(c) == {'note'} and isinstance(b, str) else c
                 for c, b in zip(sm.get('conflicts', []), base.get('conflicts', []))]
        if sm_cf != base.get('conflicts', []) or {k: v for k, v in sm.items() if k != 'conflicts'} != {k: v for k, v in base.items() if k != 'conflicts'}:
            rep['errors'].append((f, 'main changed original (non-generated) content; resolve by hand'))
            continue
        rn, mn = {}, {}
        collect(result.get('fields', {}), '', rn); collect(mdoc.get('fields', {}), '', mn)
        for p, node in rn.items():
            key = (product, tier, p)
            m = mn.get(p)
            if m is None:
                rep['no_main_counterpart'] += 1; continue
            mo, eo = main_own(m), expected_own(node, p)
            if key in REJECT_VALUE:
                rep['override_decisions'].append({'file': f, 'path': p, 'decision': 'rejected (value-changing)',
                                                  'main_value_final': mo.get('value_final'), 'our_value': node.get('value'),
                                                  'main_resolution': mo.get('resolution')})
                continue
            if key in REJECT_ANNOTATION:
                rep['override_decisions'].append({'file': f, 'path': p, 'decision': 'resolution text not adopted; normalised keys checked',
                                                  'main_resolution': mo.get('resolution')})
                mo = {k: v for k, v in mo.items() if k != 'resolution'}
            if key in ACCEPT_ANNOTATION:
                rep['override_decisions'].append({'file': f, 'path': p, 'decision': 'accepted (annotation, value unchanged)',
                                                  'main_resolution': mo.get('resolution')})
                eo_cmp = dict(eo, resolution=mo.get('resolution'))
            else:
                eo_cmp = eo
            if mo == eo_cmp:
                for k in m:  # main's key order
                    if k in mo: node[k] = mo[k]
                rep['kept_nodes'] += 1
                uc = mo.get('unit_conversion', '')
                if 'does not match printed text' in uc or mo.get('value_final', 0) is None and node.get('value') is not None:
                    rep['review_flags'].append({'file': f, 'path': p, 'note': uc or 'value_final null', 'value': node.get('value'),
                                                'printed_text': node.get('printed_text'), 'unit': node.get('unit')})
            else:
                rep['stale_dropped'].append({'file': f, 'path': p, 'main': mo, 'rederived_from_ours': eo_cmp,
                                             'our_value': node.get('value'), 'our_unit': node.get('unit')})
        # conflicts
        for i, c in enumerate(result.get('conflicts', [])):
            if not isinstance(c, dict):
                hit = [x for x in ip.CONFLICTS if x[0] == product and x[1] in c]
                if hit: rep['base_mismatch_strings'].append((f, i, hit[0][:2], 'string conflict left as text, not annotated'))
                continue
            text = json.dumps({k: v for k, v in c.items() if k not in ('final_resolution', 'resolved')}, ensure_ascii=False)
            hit = [x for x in ip.CONFLICTS if x[0] == product and x[1] in text]
            if len(hit) != 1:
                continue
            rule = hit[0]
            if rule[:2] in CF_ACCEPT:
                c['resolved'], c['final_resolution'] = rule[2], rule[3]
                dec = 'accepted' + (' (resolved)' if rule[2] else ' (kept unresolved)')
            else:
                proposal = rule[3]
                mref = re.search(r'(?:tier(\d) )?fields\.([\w.\[\]]+?)\.resolution', proposal)
                if mref:
                    ov = ip.OVERRIDES.get((product, int(mref.group(1) or tier), mref.group(2)))
                    if ov and ov.get('resolution'):
                        proposal += ' ' + ov['resolution']
                c['resolved'], c['final_resolution'] = False, RULES_NOTE + proposal
                dec = 'not adopted (left unresolved)'
            rep['conflict_decisions'].append({'file': f, 'index': i, 'rule': list(rule[:2]), 'decision': dec})
    if result == ours:
        out = raw; rep['unchanged_from_ours'] += 1
    else:
        fm = ip.fmt_of(raw)
        out = (json.dumps(result, indent=2, ensure_ascii=fm['ensure_ascii']) + fm['tail']).replace('\n', fm['nl'])
    if WRITE:
        with open(ip.long_path(os.path.normpath(os.path.join(repo, f))), "w", encoding='utf-8', newline='') as fh:
            fh.write(out)
        rep['written'] += 1

with open(report_path, 'w', encoding='utf-8') as fh:
    json.dump(rep, fh, indent=1, ensure_ascii=False)
print({k: (len(v) if isinstance(v, list) else v) for k, v in rep.items()})
