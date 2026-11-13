"""Reading aid for the manual review (read-only). Prints cached page text of a new or an existing source document, or the
current JSON content of a product as flat field rows.

  python show.py new  <file name in the new archive> [pages e.g. 1,2,5-7] [max chars per page]
  python show.py old  <file name in the existing archive> [pages] [max chars per page]
  python show.py json <product_id> [substring filter on the field path]
  python show.py grep <new|old> <file name> <regex>          (lines matching, with page numbers)
"""
import csv, gzip, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(BASE)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'data_policy'))


def pages_of(side, name):
    if side == 'new':
        with open(os.path.join(INV, 'manifest', 'file_manifest.csv'), encoding='utf-8') as fh:
            rows = [r for r in csv.DictReader(fh) if r['filename'] == name]
        if not rows:
            sys.exit('not in the new archive: ' + name)
        sha, folder = rows[0]['sha256'], 'text'
    else:
        with open(os.path.join(INV, '_cache', 'reference.json'), encoding='utf-8') as fh:
            ms = [m for m in json.load(fh)['archive']['members'] if m['name'] == name]
        if not ms:
            sys.exit('not in the existing archive: ' + name)
        sha, folder = ms[0]['sha256'], 'ref_text'
    p = os.path.join(INV, '_cache', folder, sha + '.txt.gz')
    if not os.path.exists(p):
        sys.exit(f'{name}: no text layer cached (sha256 {sha})')
    with gzip.open(p, 'rt', encoding='utf-8') as fh:
        return sha, fh.read().split('\f')


def sel(spec, n):
    if not spec or spec == 'all':
        return list(range(1, n + 1))
    out = []
    for part in spec.split(','):
        a, _, b = part.partition('-')
        out += list(range(int(a), int(b or a) + 1))
    return [i for i in out if 1 <= i <= n]


def flat(node, path=''):
    if isinstance(node, dict):
        if 'status' in node and ('value' in node or 'printed_text' in node):
            yield path, node
            return
        for k, v in node.items():
            yield from flat(v, f'{path}.{k}' if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from flat(v, f'{path}[{i}]')
    else:
        yield path, node


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    a = sys.argv[1:]
    if a[0] in ('new', 'old'):
        sha, pages = pages_of(a[0], a[1])
        lim = int(a[3]) if len(a) > 3 else 6000
        print(f'## {a[1]} sha256={sha} pages={len(pages)}')
        for i in sel(a[2] if len(a) > 2 else '', len(pages)):
            t = re.sub(r'[ \t]+', ' ', pages[i - 1])
            t = re.sub(r'\n\s*\n+', '\n', t).strip()
            print(f'--- page {i} ---\n{t[:lim]}')
    elif a[0] == 'grep':
        sha, pages = pages_of(a[1], a[2])
        rx = re.compile(a[3], re.I)
        for i, t in enumerate(pages, 1):
            ls = t.splitlines()
            for j, l in enumerate(ls):
                if rx.search(l):
                    print(f'p{i}: ' + ' | '.join(x.strip() for x in ls[max(0, j - 1): j + 4] if x.strip())[:300])
    elif a[0] == 'brief':
        import policy_lib as P
        p = P.load_products()[a[1]]
        for fn, d in p['files'].items():
            pr = d.get('product') or {}
            print(f'## tier {d.get("tier")} {os.path.basename(fn)} | {pr.get("product_name")} | {pr.get("supplier")} | src={pr.get("source_file")} rev={pr.get("revision_date")}')
            miss, claims = [], 0
            for path, n in flat(d.get('fields', {})):
                if not isinstance(n, dict):
                    continue
                if path.startswith('performance_claims'):
                    claims += 1
                    continue
                if n.get('status') == 'Missing':
                    miss.append(path)
                    continue
                s = n.get('source') or {}
                v = n.get('value') if n.get('value') is not None else (n.get('printed_text') or {k: x for k, x in n.items() if k not in ('source', 'status') and x not in (None, '', [], {})})
                print(f'  {path} = {str(v)[:110]} {n.get("unit") or ""} [{n.get("value_kind") or ""}/{n.get("status")}] {str(s.get("file"))[-28:]} p{s.get("page")}')
            print(f'  claims: {claims}; Missing: {", ".join(miss)}')
            print(f'  open_questions: {len(d.get("open_questions") or [])}; conflicts: {len(d.get("conflicts") or [])}')
    elif a[0] == 'json':
        import policy_lib as P
        p = P.load_products()[a[1]]
        filt = a[2].lower() if len(a) > 2 else ''
        for fn, d in p['files'].items():
            print(f'## {fn} tier={d.get("tier")} product={json.dumps(d.get("product"), ensure_ascii=False)[:400]}')
            print('   source_documents:', json.dumps(d.get('source_documents'), ensure_ascii=False)[:700])
            for path, n in flat(d.get('fields', {})):
                if filt and filt not in path.lower():
                    continue
                if isinstance(n, dict):
                    s = n.get('source') or {}
                    if n.get('status') == 'Missing' and n.get('value') is None:
                        print(f'  {path}: Missing')
                        continue
                    if n.get('value') is None and not n.get('printed_text'):
                        extra = {k: v for k, v in n.items() if k not in ('source', 'status') and v not in (None, '', [], {})}
                        print(f'  {path}: {json.dumps(extra, ensure_ascii=False)[:300]} status={n.get("status")} src={str(s.get("file"))[-40:]} p{s.get("page")}')
                        continue
                    print(f'  {path}: value={n.get("value")!r} q={n.get("qualifier")} min={n.get("min")} max={n.get("max")} kind={n.get("value_kind")} '
                          f'unit={n.get("unit")} T={n.get("test_temperature_c")} method={n.get("method")} status={n.get("status")} '
                          f'printed={str(n.get("printed_text"))[:110]!r} src={s.get("file")} p{s.get("page")} rev={s.get("revision_date")}')
                elif n not in (None, '', [], {}):
                    print(f'  {path}: {str(n)[:260]!r}')
            for k in ('open_questions', 'conflicts'):
                for q in d.get(k) or []:
                    print(f'  [{k}] {json.dumps(q, ensure_ascii=False)[:330]}')


if __name__ == '__main__':
    main()
