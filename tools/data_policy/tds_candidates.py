"""List, for every selected value that comes from an SDS page, what the product's technical documents print for the
same property (Rule 1 review aid; read-only).

For each SDS-sourced selected value it searches the technical (non-SDS) archive pages that the product's records cite,
plus technical pages that name the product, for lines carrying the property's label, and prints them with page numbers.
The output is a reading aid for the reviewer; decisions are recorded in source_selection_decisions.py, not here.

Usage: python tools/data_policy/tds_candidates.py [--product RICHFUL_RF6077] > candidates.txt
"""
import argparse, csv, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import policy_lib as P

LABELS = {
    'kv40': r'(kinematic\s+)?visc\w*.{0,30}(40\s*°?\s*[c℃]|104\s*°?\s*f)|kv\s*40|@\s*40',
    'kv100': r'(kinematic\s+)?visc\w*.{0,30}(100\s*°?\s*[c℃]|212\s*°?\s*f)|kv\s*100|@\s*100',
    'density': r'density|specific\s+gravity|lbs?/\s?gal',
    'specific_gravity': r'specific\s+gravity|relative\s+density',
    'flash_point': r'flash',
    'pour_point': r'pour',
    'noack_volatility': r'noack|evaporation',
    'viscosity_index': r'viscosity\s+index|\bVI\b',
    'tbn': r'base\s+number|\bTBN\b',
    'chemistry': r'hydro(cracked|treated|isomeri|processed)|paraffinic|naphthenic|\bPAO\b|ester|mineral',
    'api_group': r'group\s+(I{1,3}V?|[1-5])\b|API\s+group',
    'intended_service': r'application|engine\s+oil|lubricant',
    'package_type': r'additive\s+package|package',
    'treat_rate_wt_pct': r'treat\s+rate|dosage|mass\s*%|wt\s*%',
    'carrier': r'carrier|diluent|base\s+oil',
    'active_content': r'active|polymer\s+content',
}


def label_for(path):
    keys = [k for k in re.split(r'[.\[\]]', path) if k and not k.isdigit()]
    for k in reversed(keys):
        if k in LABELS:
            return k
        if k in ('identity', 'share_wt_pct'):
            return 'carrier'
        if k == 'wt_pct':
            return 'active_content'
    return keys[-1]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--product'); a = ap.parse_args()
    cls = {(r['file'], r['page']): r['class'] for r in csv.DictReader(open(os.path.join(P.REPORTS, 'data_policy', 'document_classes.csv'), encoding='utf-8'))}
    ar = P.Archive()
    for pid, p in P.load_products().items():
        if a.product and pid != a.product:
            continue
        cited_tech = set()
        sds_vals = []
        for f, d in p['files'].items():
            for vp, n in P.value_objects(d.get('fields', {})):
                fl, pg, _ = P.src(n)
                if not fl:
                    continue
                c = cls.get((fl, '' if pg is None else str(pg)))
                if c == 'TECHNICAL':
                    cited_tech.add(fl)
                elif c == 'SDS' and n.get('status') in ('Reported', 'Calculated'):
                    sds_vals.append((f.split('/')[-1], vp, n))
            for s in d.get('source_documents') or []:
                if s.get('file') and any(cls.get((s['file'], str(x))) == 'TECHNICAL' for x in (s.get('pages') or [1])):
                    cited_tech.add(s['file'])
        if not sds_vals:
            continue
        print(f'\n######## {pid}  technical documents cited: {sorted(cited_tech) or "none"}')
        for f, vp, n in sds_vals:
            fl, pg, _ = P.src(n)
            lab = label_for(vp)
            print(f'--- {f} {vp}: {n.get("value")!r} {n.get("unit") or ""} | SDS {fl} p.{pg} | printed: {str(n.get("printed_text") or "")[:90]!r}')
            for tf in sorted(cited_tech):
                pages = ar.pages(tf) or []
                for i, t in enumerate(pages):
                    lines = [l.strip() for l in t.splitlines()]
                    for j, l in enumerate(lines):
                        if lab in LABELS and re.search(LABELS[lab], l, re.I):
                            ctx = ' | '.join(x for x in lines[j:j + 4] if x)[:160]
                            print(f'      TDS {tf} p.{i + 1}: {ctx}')
                if not pages:
                    print(f'      TDS {tf}: image / no text layer - read visually')


if __name__ == '__main__':
    main()
