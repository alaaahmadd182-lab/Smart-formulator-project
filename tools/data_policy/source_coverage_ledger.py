"""Rule 1 coverage ledger: for every product and every TDS/SDS-type numeric property, which technical and SDS documents
were examined, what is selected and why, whether a TDS-SDS comparison exists, and what evidence is unavailable or
unreviewed (read-only on the data).

It does not rely on the audit, conflicts[] or alternate_entries alone. For each product it collects the associated
documents:
  - cited: every archive file cited anywhere in the product's records (values, alternates, conflicts, product block);
  - name match: archive files that name the product but are not cited (from the 2026-10-27 audit document map,
    tools/audit/original_2026-10-27_to_30/intermediate/docmap.json; a heuristic association). Each one carries its
    reviewed identity verdict (association_review_decisions.json); documents reviewed as another product or an
    unestablished family document are excluded and listed in excluded_associations;
and classifies every page of them (document_classes.classify_page; image-only files use the reviewed MANUAL table or
stay unsearchable). It then searches each page for the property label (LABELS below). A label hit means "the document
mentions the property", NOT that a value for this product was read: multi-product tables can mention it for another
grade. Such hits are leads for a reviewer, reported as gaps; they never change data.

Selection status (column selection_status):
  technical_selected           the selected value is from a technical page
  sds_fallback_no_tech_label   the selected value is from an SDS page and no associated technical page mentions the property
  exception / pending          declared in source_selection.EXCEPTIONS / PENDING / PENDING_FIELDS (reason given)
  sds_fallback_reviewed        declared in source_selection.SDS_FALLBACK_FIELDS: technical document read, property not given
  gap_tech_label_unreviewed    SDS selected although an associated technical page mentions the property; not reviewed
  external_selected            the selected value is from a URL source
  missing_label_found          Missing, but an associated document mentions the property (lead not reviewed)
  missing_no_label             Missing; no searchable associated document mentions the property
  missing_not_searchable       Missing; some associated documents have no text layer and were not read for this property
Comparison status (column comparison_status): the inventory result when a TDS-SDS pair exists, otherwise why no
comparison can be made, or 'gap: both classes mention the property; no comparison recorded'.

Usage: python tools/data_policy/source_coverage_ledger.py [--out reports/data_policy/source_coverage_ledger.csv]
Writes only --out. Exit 0.
"""
import argparse, collections, csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P  # noqa: E402
import document_classes as DC  # noqa: E402

DOCMAP = os.path.join(P.ROOT, 'tools', 'audit', 'original_2026-10-27_to_30', 'intermediate', 'docmap.json')
LABELS = {
    'kv40': r'(kinematic\s+)?visc\w*[^\n]{0,40}(\b40\s*°?\s*[c℃]|104\s*°?\s*f)|\bkv\s*40\b',
    'kv100': r'(kinematic\s+)?visc\w*[^\n]{0,40}(\b100\s*°?\s*[c℃]|212\s*°?\s*f)|\bkv\s*100\b',
    'viscosity_index': r'viscosity\s+index|\bV\.?I\.?\b',
    'density': r'(?<!relative )\bdensity\b|lbs?\s*/\s*gal|kg\s*/\s*m3|kg/m³',
    'specific_gravity': r'specific\s+gravity|sp\.\s*gravity|relative\s+density',
    'ccs': r'\bCCS\b|cold[- ]crank',
    'flash_point': r'flash\s*point|\bflash\b',
    'pour_point': r'pour\s*point',
    'noack_volatility': r'noack|evaporation\s+loss',
    'tbn': r'\bTBN\b|base\s+number',
}
SCOPE = {'base_oil': ['kv40', 'kv100', 'viscosity_index', 'density', 'specific_gravity', 'ccs', 'flash_point', 'pour_point', 'noack_volatility'],
         'additive_package': ['kv40', 'kv100', 'density', 'specific_gravity', 'flash_point', 'pour_point', 'tbn'],
         'additive_component': []}
MANDATORY = {'base_oil': {'kv40', 'kv100', 'viscosity_index', 'density', 'ccs'}, 'additive_package': set(), 'additive_component': set()}


def _cited_files(p):
    out = set()
    def rec(n):
        if isinstance(n, dict):
            for k, v in n.items():
                if k == 'file' and isinstance(v, str) and v:
                    out.add(v)
                elif k == 'source_file':
                    for x in (v if isinstance(v, list) else [v]):
                        if isinstance(x, str) and x:
                            out.add(x)
                else:
                    rec(v)
        elif isinstance(n, list):
            for v in n:
                rec(v)
    for d in p['files'].values():
        rec(d)
    return out


def _field(doc, prop):
    f = doc.get('fields', {})
    n = f.get(prop)
    if isinstance(n, list):  # ccs: first entry with a value, else first entry
        return next((x for x in n if isinstance(x, dict) and x.get('status') in ('Reported', 'Calculated')), n[0] if n else None)
    return n


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(P.REPORTS, 'data_policy', 'source_coverage_ledger.csv'))
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    import source_selection as S
    declared = {}
    for pid, props, why in S.EXCEPTIONS:
        for x in props.split(','):
            declared[(pid, x.strip())] = ('exception', why)
    for pid, props, why in S.PENDING:
        for x in props.split(','):
            declared[(pid, x.strip())] = ('pending', why)
    for pid, prop, why in S.PENDING_FIELDS:
        declared[(pid, prop)] = ('pending', why)
    for pid, prop, why in S.SDS_FALLBACK_FIELDS:
        declared[(pid, prop)] = ('sds_fallback_reviewed', why)
    with open(os.path.join(P.REPORTS, 'data_policy', 'document_classes.csv'), encoding='utf-8') as fh:
        cls = {(r['file'], r['page']): r['class'] for r in csv.DictReader(fh)}
    with open(os.path.join(P.REPORTS, 'data_policy', 'tds_sds_comparisons.csv'), encoding='utf-8') as fh:
        comps = collections.defaultdict(list)
        for r in csv.DictReader(fh):
            comps[(r['product'], r['property'])].append(r)
    with open(DOCMAP, encoding='utf-8') as fh:
        docmap = json.load(fh)
    named = collections.defaultdict(set)
    for key, v in docmap.items():
        if not v.get('cited_by'):
            for folder in v.get('names') or []:
                named[folder.split('/')[-1]].add(os.path.basename(v['path']))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'association_review_decisions.json'), encoding='utf-8') as fh:
        arules = json.load(fh)['rules']

    def assoc_verdict(pid, f):
        """Reviewed verdict of a name-match association (association_review.py); byte-identical copies are checked
        there, here a same-name copy of a cited file is never a name-match."""
        r = next((r for r in arules if re.fullmatch(r['product'], pid) and (not r.get('documents') or f in r['documents'])), None)
        return r['verdict'] if r else None
    prods = P.load_products()
    ar = P.Archive()
    page_cache = {}

    def doc_pages(f):
        """[(page_no, class, text)] or None if not searchable."""
        if f in page_cache:
            return page_cache[f]
        res = None
        if not str(f).lower().startswith('http'):
            pages = ar.pages(f)
            base = os.path.basename(str(f)).replace('%20', ' ')
            if pages and any(x.strip() for x in pages) and base not in DC.MANUAL:
                res = [(i + 1, DC.classify_page(pages, i)[0], pages[i]) for i in range(len(pages))]
        page_cache[f] = res
        return res

    rows = []
    for pid in sorted(prods):
        p = prods[pid]
        props = SCOPE[p['class']]
        if not props:
            continue
        cited = _cited_files(p)
        docs, excluded = [(f, 'cited') for f in sorted(cited)], []
        for f in sorted(named.get(pid, set()) - {os.path.basename(c) for c in cited}):
            v = assoc_verdict(pid, f)
            if v in ('same_product', 'same_document_copy'):
                docs.append((f, f'name match ({v.replace("_", " ")}, reviewed)'))
            elif v is None:
                docs.append((f, 'name match (unverified)'))
            else:
                excluded.append(f'{f} ({v})')
        for prop in props:
            node, tier = None, None
            for d in p['files'].values():
                if prop in d.get('fields', {}):
                    node, tier = _field(d, prop), d.get('tier')
                    break
            if node is None and prop != 'specific_gravity':
                continue
            node = node or {}
            src = node.get('source') or {}
            sel_file, sel_page = src.get('file'), src.get('page')
            sel_cls = 'EXTERNAL' if str(sel_file).startswith('http') else cls.get((str(sel_file), str(sel_page).split()[0] if sel_page not in (None, '') else ''))
            tech, sds, unsearch, lines = [], [], [], []
            for f, how in docs:
                pg = doc_pages(f)
                if str(f).startswith('http'):
                    continue
                if pg is None:
                    manual = DC.MANUAL.get(os.path.basename(f).replace('%20', ' '), ('no text layer',))[0]
                    if manual != 'SDS':  # an unreadable SDS cannot hide a technical value
                        unsearch.append(f'{f} ({how}; {manual})')
                    continue
                for n, c, t in pg:
                    if re.search(LABELS[prop], t, re.I):
                        (tech if c == 'TECHNICAL' else sds if c == 'SDS' else []).append(f'{f} p.{n} ({how})')
                        hit = next((ln.strip() for ln in t.splitlines() if re.search(LABELS[prop], ln, re.I)), '')
                        lines.append(f'{os.path.basename(f)} p.{n}: {hit[:90]}')
            status, reason = None, ''
            st = node.get('status')
            dec = declared.get((pid, prop))
            if st in ('Reported', 'Calculated'):
                if dec:
                    status, reason = dec
                elif sel_cls == 'TECHNICAL':
                    status, reason = 'technical_selected', 'technical value selected (Rule 1)'
                elif sel_cls == 'EXTERNAL':
                    status, reason = 'external_selected', 'value from a URL source (source_registry.json)'
                elif sel_cls == 'SDS':
                    other_tech = [x for x in tech if not x.startswith(f'{sel_file} ')]
                    if other_tech:
                        status, reason = 'gap_tech_label_unreviewed', 'SDS selected; an associated technical page mentions the property: ' + '; '.join(other_tech[:4])
                    else:
                        status, reason = 'sds_fallback_no_tech_label', 'no associated searchable technical page mentions the property'
                        if unsearch:
                            status, reason = 'gap_tech_label_unreviewed', 'SDS selected; associated documents without a text layer were not read for this property'
                else:
                    status, reason = 'unclassified_source', f'selected source class {sel_cls!r}'
            else:
                hits = tech + sds
                if dec:
                    status, reason = dec
                elif hits:
                    status, reason = 'missing_label_found', 'status Missing; associated document mentions the property: ' + '; '.join(hits[:4])
                elif unsearch:
                    status, reason = 'missing_not_searchable', 'status Missing; associated documents without a text layer not read for this property'
                else:
                    status, reason = 'missing_no_label', 'no searchable associated document mentions the property'
            cp = comps.get((pid, prop), [])
            if cp:
                comparison = '; '.join(sorted({c['comparability'] + ' -> ' + c['proposed_screen'] for c in cp}))
            elif tech and sds:
                comparison = 'gap: both document classes mention the property; no TDS-SDS comparison recorded'
            elif tech and not sds:
                comparison = 'not possible: no associated SDS page mentions the property'
            elif sds and not tech:
                comparison = 'not possible: no associated technical page mentions the property'
            else:
                comparison = 'not possible: no associated searchable document mentions the property'
            rows.append(dict(product=pid, material_class=p['class'], tier=tier, property=prop, mandatory=str(prop in MANDATORY[p['class']]).lower(),
                             status=st, selected_file=sel_file, selected_page=sel_page, selected_class=sel_cls,
                             selection_status=status, selection_reason=reason,
                             technical_pages_with_label='; '.join(tech), sds_pages_with_label='; '.join(sds),
                             comparison_status=comparison, first_label_lines=' | '.join(lines[:4]), unsearchable_documents='; '.join(unsearch),
                             documents_examined='; '.join(f'{f} ({how})' for f, how in docs),
                             excluded_associations='; '.join(excluded)))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    sys.path.insert(0, os.path.join(P.ROOT, 'tools', 'mandatory_properties'))
    import build_eligibility as BE
    with open(a.out.replace('.csv', '.meta.json'), 'w', encoding='utf-8', newline='') as fh:
        json.dump({'source_snapshot_sha256': BE.snapshot_sha256(P.PRODUCTS), 'rows': len(rows),
                   'note': 'Exact-byte snapshot of Products_json the ledger was built from; build_eligibility.py refuses a mismatch.'},
                  fh, indent=2)
        fh.write('\n')
    print(f'ledger rows: {len(rows)} ({len({r["product"] for r in rows})} products)')
    for k, n in collections.Counter(r['selection_status'] for r in rows).most_common():
        print(f'  {k}: {n}  (mandatory: {sum(1 for r in rows if r["selection_status"] == k and r["mandatory"] == "true")})')
    print('comparison:')
    for k, n in collections.Counter(r['comparison_status'].split(':')[0].split(' ->')[0] for r in rows).most_common():
        print(f'  {k}: {n}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
