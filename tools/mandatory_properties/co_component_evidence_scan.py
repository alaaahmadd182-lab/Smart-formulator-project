"""Search the packages' own source pages for explicit supplier statements about required co-components (VM, PPD,
booster) - decision B evidence (read-only; nothing in the product data is changed).

A statement is classified by its wording only:
  none_required      the supplier says no supplemental / additional co-component is needed, or that the package already
                     contains it (e.g. "already contains a pour point depressant (PPD) so no supplemental PPD should be needed")
  required_or_named  the supplier names a co-component to be used with the package ("in combination with ... viscosity
                     modifier", "+ Infineum D2359 at 1.93 %", "booster required")
An empty co-component list in a record is not evidence of absence. A 'none_required' statement covers only the
co-component type it names (a PPD statement says nothing about a VM). Findings are evidence for a reviewer.

Usage: python tools/mandatory_properties/co_component_evidence_scan.py [--out reports/mandatory_properties/co_component_evidence.csv]
"""
import argparse, collections, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [os.path.join(ROOT, 'tools', 'data_policy')]
import policy_lib as P  # noqa: E402

CO = r'(?:pour\s+point\s+depressants?|PPDs?|viscosity\s+(?:index\s+)?(?:modifiers?|improvers?)|VIIs?|VMs?|boosters?|co-?additives?)'
NONE = re.compile(r'(?:no\s+(?:supplemental|additional|extra|further)\s+' + CO + r'|already\s+contains?\s+(?:an?\s+)?' + CO +
                  r'|without\s+(?:the\s+need\s+for\s+|any\s+|an?\s+)?' + CO + r'|does\s+not\s+require\s+(?:an?\s+|any\s+)?' + CO + r')', re.I)
REQ = re.compile(r'(?:in\s+combination\s+with|together\s+with|combined\s+with|used\s+with|requires?|required|plus|\+)[^.\n]{0,80}' + CO +
                 r'|' + CO + r'[^.\n]{0,40}(?:required|is\s+needed|must\s+be)', re.I)
NAMED = re.compile(r'\+\s*(?:Infineum|HiTEC|LUBRIZOL|Eni|Afton)[^\n]{0,40}at\s+[\d.]+\s*%', re.I)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(ROOT, 'reports', 'mandatory_properties', 'co_component_evidence.csv'))
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    prods = P.load_products()
    ar = P.Archive()
    rows = []
    for pid, p in sorted(prods.items()):
        if p['class'] != 'additive_package':
            continue
        files = set()
        for d in p['files'].values():
            for _, n in P.value_objects(d.get('fields', {})):
                f = (n.get('source') or {}).get('file')
                if f and not str(f).lower().startswith('http'):
                    files.add(f)
        t1 = next((d for d in p['files'].values() if d.get('tier') == 1), {})
        recorded = [e for e in (t1.get('fields') or {}).get('required_co_components') or []
                    if isinstance(e, dict) and (e.get('dose_wt_pct') or {}).get('status') not in (None, 'Missing')]
        hits = []
        for f in sorted(files):
            for i, t in enumerate(ar.pages(f) or []):
                flat = re.sub(r'\s+', ' ', t)
                for rx, kind in ((NONE, 'none_required'), (NAMED, 'required_or_named'), (REQ, 'required_or_named')):
                    for m in rx.finditer(flat):
                        quote = flat[max(0, m.start() - 60): m.end() + 60].strip()
                        if not any(h['quote'] == quote for h in hits):
                            hits.append(dict(kind=kind, file=f, page=i + 1, quote=quote))
        none_q = [h for h in hits if h['kind'] == 'none_required']
        req_q = [h for h in hits if h['kind'] == 'required_or_named']
        rows.append(dict(product=pid, recorded_co_components=len(recorded),
                         none_required_statements=len(none_q), required_or_named_statements=len(req_q),
                         finding=('explicit "none required" statement found (covers only the co-component it names)' if none_q else
                                  'co-components named or required by the supplier' if req_q else
                                  'no explicit statement found in the text layer of the cited pages'),
                         evidence=' || '.join(f"[{h['kind']}] {h['file']} p.{h['page']}: {h['quote'][:220]}" for h in (none_q + req_q)[:4])))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    print(f'packages: {len(rows)}')
    for k, v in collections.Counter(r['finding'] for r in rows).most_common():
        print(f'  {v}: {k}')
    print(f'  packages with a recorded co-component: {sum(1 for r in rows if r["recorded_co_components"])}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
