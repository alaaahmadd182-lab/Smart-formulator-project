"""Show what integrate_products.py would change in given product files, value object by value object (read-only).

The repository's product data is deliberately not fully re-derived by integrate_products.py (README, "Data integration"),
so a full --write run would touch many unrelated files. This helper applies the script's own derivation (normalise,
ANNOTATIONS, CONFLICTS) to the named files in memory and prints every key that would differ, so changed records can be
kept consistent with the script without running it on the whole repository.

Usage: python tools/data_policy/integration_diff.py Products_json/.../file.json [...]
       python tools/data_policy/integration_diff.py --changed     (the product files changed against HEAD)
Exit codes: 0 no differences; 1 differences found.
"""
import copy, importlib.util, json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P


def integrate_module():
    spec = importlib.util.spec_from_file_location('integrate_products', os.path.join(P.ROOT, 'integrate_products.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def derived(I, relpath):
    d = P.load(relpath)
    product = relpath.rsplit('/', 2)[1]
    nodes = {}
    I.walk(d.get('fields', {}), '', nodes)
    for (p, t, path), a in I.ANNOTATIONS.items():
        if p == product and t == d.get('tier') and path in nodes:
            nodes[path]['resolution'] = a['resolution']
    for c in d.get('conflicts', []):
        if isinstance(c, dict):
            text = json.dumps({k: v for k, v in c.items() if k not in I.CONFLICT_KEYS}, ensure_ascii=False)
            hit = [x for x in I.CONFLICTS if x[0] == product and x[1] in text]
            if len(hit) == 1:
                c.update({'resolved': hit[0][2], 'final_resolution': hit[0][4]})
    return d


def diff(a, b, path=''):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                out.append(f'{path}.{k}: {"missing now" if k not in a else "would be removed"} -> {json.dumps(b.get(k), ensure_ascii=False)[:120]}')
            else:
                out += diff(a[k], b[k], f'{path}.{k}')
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, f'{path}[{i}]')
    elif a != b:
        out.append(f'{path}: {json.dumps(a, ensure_ascii=False)[:100]} -> {json.dumps(b, ensure_ascii=False)[:100]}')
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    files = sys.argv[1:]
    if files == ['--changed']:
        files = [f for f in subprocess.run(['git', 'diff', '--name-only', 'HEAD', '--', 'Products_json'], cwd=P.ROOT, capture_output=True,
                                           text=True, encoding='utf-8').stdout.splitlines() if f]
    I = integrate_module()
    n = 0
    for f in files:
        dd = diff(P.load(f), derived(I, f))
        for x in dd:
            print(f'{f}: {x}')
        n += len(dd)
    print(f'{n} differences in {len(files)} files')
    return 1 if n else 0


if __name__ == '__main__':
    sys.exit(main())
