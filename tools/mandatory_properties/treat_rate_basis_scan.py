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
# Policy 3 (2026-11-11): a document-wide convention is a statement, anywhere in the document, of the basis of its
# percentages ("all percentages are by weight", "treat rates in mass %"). Lines matching CONVENTION are leads to read.
CONVENTION = re.compile(r'(?:all|unless|otherwise|expressed|given|quoted|stated).{0,60}(?:percent|%)'
                        r'|(?:percent|%).{0,40}(?:by weight|by mass|by volume|weight basis|mass basis|volume basis)'
                        r'|(?:treat|dosage|dose).{0,50}(?:wt\.?\s?%|%\s?wt|mass\s?%|%\s?m/m|w/w|vol\.?\s?%|%\s?vol|v/v)', re.I)


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
        text, pages = None, []
        if f and not str(f).startswith('http'):
            try:
                pages = arch.pages(f) or []
                n = int(re.findall(r'\d+', str(pg))[0]) if pg not in (None, '') else None
                text = pages[n - 1] if n and n <= len(pages) else None
            except Exception as e:  # unavailable document: recorded, not hidden
                text = None
        lines = [ln.strip() for ln in (text or '').splitlines() if ln.strip()]
        mass = [ln for ln in lines if MASS.search(ln)]
        vol = [ln for ln in lines if VOL.search(ln)]
        conv = [f'p.{i + 1}: {ln.strip()}' for i, t in enumerate(pages) for ln in (t or '').splitlines() if CONVENTION.search(ln)]
        searched = sum(1 for t in pages if (t or '').strip())
        rows.append(dict(product=pid, file=rel.rsplit('/', 1)[1], path=path, value=vo.get('value'), unit=vo.get('unit'),
                         printed_text=vo.get('printed_text'), source_file=f, page=pg,
                         page_text='available' if text else ('external URL' if str(f).startswith('http') else 'no text layer or unavailable'),
                         mass_lines=' || '.join(mass[:6]), volume_lines=' || '.join(vol[:6]),
                         document_pages_with_text=f'{searched} of {len(pages)}' if pages else '',
                         document_wide_convention_leads=' || '.join(conv[:6])))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ['product'], lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    print(f'{len(rows)} treat-rate values without a mass basis in the recorded unit; {len({r["product"] for r in rows})} products')
    docs = {r['source_file']: r for r in rows}
    print(f'source documents: {len(docs)}; with a document-wide convention lead: '
          f'{sum(1 for r in docs.values() if r["document_wide_convention_leads"])}; external URL: '
          f'{sum(1 for r in docs.values() if r["page_text"] == "external URL")}; without any text layer: '
          f'{sum(1 for r in docs.values() if r["document_pages_with_text"].startswith("0 of"))}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
