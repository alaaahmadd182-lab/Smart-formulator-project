"""Reading aid for item E (treat-rate mass basis): for every treat-rate-type value whose recorded unit does not state a
mass basis, print the basis wording found on its cited page (read-only).

Basis words searched on the cited page: wt / weight / mass / w/w / m/m (mass) and vol / volume / v/v (volume), plus the
table heading or footnote lines that contain '%'. The output is evidence for a reviewer; this script decides nothing.
Reviewed results are recorded in treat_rate_basis_evidence.json.

Usage: python tools/mandatory_properties/treat_rate_basis_scan.py [--out reports/mandatory_properties/treat_rate_basis_scan.csv]
"""
import argparse, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [os.path.join(ROOT, 'tools', 'data_policy')]
import policy_lib as P  # noqa: E402

MASS = re.compile(r'\bwt\.?\s*%|%\s*wt\b|\bweight\b|\bby\s+mass\b|\bmass\s*%|%\s*\(?m/m\)?|\bw/w\b|\bwt\b', re.I)
VOL = re.compile(r'\bvol\.?\s*%|%\s*vol\b|\bvolume\b|\bv/v\b|\bby\s+vol', re.I)
MASS_BASIS = re.compile(r'wt|mass|weight|m/m|w/w', re.I)


def targets(prods):
    for pid, p in sorted(prods.items()):
        for rel, d in p['files'].items():
            f = d.get('fields', {})
            items = []
            if p['class'] == 'additive_package' and d.get('tier') == 1:
                items += [(f'treat_rate_matrix[{i}]', (e or {}).get('treat_rate_wt_pct')) for i, e in enumerate(f.get('treat_rate_matrix') or [])]
                items += [(f'required_co_components[{i}]', (e or {}).get('dose_wt_pct')) for i, e in enumerate(f.get('required_co_components') or [])]
            if p['class'] == 'additive_component' and d.get('tier') == 1:
                items.append(('treat_rate', f.get('treat_rate')))
            for path, vo in items:
                if isinstance(vo, dict) and vo.get('status') in ('Reported', 'Calculated') and not MASS_BASIS.search(str(vo.get('unit') or '')):
                    yield pid, rel, path, vo


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(ROOT, 'reports', 'mandatory_properties', 'treat_rate_basis_scan.csv'))
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    prods = P.load_products()
    arch = P.Archive()
    rows = []
    for pid, rel, path, vo in targets(prods):
        s = vo.get('source') or {}
        f, pg = s.get('file'), s.get('page')
        text = None
        if f and not str(f).startswith('http'):
            try:
                pages = arch.pages(f)
                n = int(re.findall(r'\d+', str(pg))[0]) if pg not in (None, '') else None
                text = pages[n - 1] if n and n <= len(pages) else None
            except Exception as e:  # unavailable document: recorded, not hidden
                text = None
        lines = [ln.strip() for ln in (text or '').splitlines() if ln.strip()]
        mass = [ln for ln in lines if MASS.search(ln)]
        vol = [ln for ln in lines if VOL.search(ln)]
        rows.append(dict(product=pid, file=rel.rsplit('/', 1)[1], path=path, value=vo.get('value'), unit=vo.get('unit'),
                         printed_text=vo.get('printed_text'), source_file=f, page=pg,
                         page_text='available' if text else ('external URL' if str(f).startswith('http') else 'no text layer or unavailable'),
                         mass_lines=' || '.join(mass[:6]), volume_lines=' || '.join(vol[:6])))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ['product'], lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    print(f'{len(rows)} treat-rate values without a mass basis in the recorded unit; {len({r["product"] for r in rows})} products')
    return 0


if __name__ == '__main__':
    sys.exit(main())
