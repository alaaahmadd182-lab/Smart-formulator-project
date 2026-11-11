"""Review of the name-match document associations (item 2 of the 2026-11-10 evidence review; read-only on the data).

The coverage ledger associates, besides the files a product cites, archive files that the 2026-10-27 audit document
map linked to the product by name. Those links are a heuristic. This tool records, for every such (product, document)
pair, what the document itself says about product identity, and the reviewed verdict:

  same_product        the document names this exact product/grade (single-product document), or prints a column or row
                      headed with this exact grade
  same_document_copy  byte-identical to a document the product already cites
  other_product       the document is for a different product or grade (e.g. Ultra-S 8 vs S-8, NYNAS S 3B vs Base Stock 20)
  family_document     a series/family document whose grade-level applicability to this product is not established
  unresolved          the identity cannot be established from the document (image-only, no product name)

Evidence from an association may be used only when the verdict is same_product or same_document_copy.
Verdicts are recorded in association_review_decisions.json (pattern rules, each with the reason read on the page).

Usage: python tools/data_policy/association_review.py [--out reports/data_policy/name_match_review.csv]
"""
import argparse, collections, csv, hashlib, io, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P  # noqa: E402

DECISIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'association_review_decisions.json')
VERDICTS = ('same_product', 'same_document_copy', 'other_product', 'family_document', 'unresolved')
USABLE = ('same_product', 'same_document_copy')


def pairs(ledger):
    out = collections.OrderedDict()
    for r in ledger:
        for f, how in re.findall(r'([^;]+?\.(?:pdf|PDF|jpg|jpeg|jfif)) \(([^)]*)\)', r['documents_examined']):
            if how.startswith('name match'):
                out.setdefault((r['product'], f.strip()), None)
        for f, how in re.findall(r'([^;]+?\.(?:pdf|PDF|jpg|jpeg|jfif)) \(([^)]*)\)', r.get('excluded_associations') or ''):
            out.setdefault((r['product'], f.strip()), None)  # excluded by its reviewed verdict, still reported
    return list(out)


def identity_text(ar, f):
    pages = ar.pages(f)
    if not pages or not any(p.strip() for p in pages):
        return '(no text layer)'
    t = ' '.join(pages[:2])
    m = re.findall(r'(?:Product name|PRODUCT NAME|Product Name|Trade name/designation|Product identifier)\s*[:|]?\s*\n?\s*:?\s*([^\n]{2,70})', t)
    head = ' | '.join(x.strip() for x in pages[0].splitlines() if x.strip())[:160]
    return (('name field: ' + '; '.join(dict.fromkeys(x.strip() for x in m if x.strip() not in (':', '')))[:160] + ' || ') if m else '') + 'head: ' + head


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(P.REPORTS, 'data_policy', 'name_match_review.csv'))
    ap.add_argument('--baseline-ref', default='4e83652', help='commit whose ledger defines the reviewed association universe')
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    with open(os.path.join(P.REPORTS, 'data_policy', 'source_coverage_ledger.csv'), encoding='utf-8') as fh:
        ledger = list(csv.DictReader(fh))
    with open(DECISIONS, encoding='utf-8') as fh:
        rules = json.load(fh)['rules']
    prods = P.load_products()
    ar = P.Archive()
    sha = {}

    def h(f):
        if f not in sha:
            m = ar.member(f)
            sha[f] = hashlib.sha256(ar.z.read(m)).hexdigest() if m else None
        return sha[f]
    # the association universe is frozen at the revision-2 ledger (as in lead_review.py): an association reviewed as the
    # same product and then used as evidence becomes 'cited', but stays reported here (now_cited = true)
    base = subprocess.run(['git', 'show', f'{a.baseline_ref}:reports/data_policy/source_coverage_ledger.csv'], cwd=P.ROOT,
                          capture_output=True, text=True, encoding='utf-8')
    if base.returncode != 0:
        raise SystemExit(f'cannot read the revision-2 ledger at {a.baseline_ref}')
    universe = list(dict.fromkeys(pairs(list(csv.DictReader(io.StringIO(base.stdout)))) + pairs(ledger)))
    rows = []
    for pid, f in universe:
        p = prods[pid]
        head = p['files'].get(next(iter(p['files'])))['product']
        cited = set()
        for d in p['files'].values():
            for _, n in P.value_objects(d.get('fields', {})):
                s = (n.get('source') or {}).get('file')
                if s:
                    cited.add(s)
        now_cited = f in cited
        copy_of = sorted(c for c in cited if c != f and h(c) and h(c) == h(f))
        rule = next((r for r in rules if re.fullmatch(r['product'], pid) and (not r.get('documents') or f in r['documents'])), None)
        verdict = 'same_document_copy' if copy_of else (rule['verdict'] if rule else 'not_reviewed')
        rows.append(dict(product=pid, product_name=head.get('product_name'), document=f, identity_text=identity_text(ar, f),
                         copy_of=';'.join(copy_of), verdict=verdict,
                         reason=('byte-identical to cited ' + ';'.join(copy_of)) if copy_of else (rule['reason'] if rule else ''),
                         usable_as_evidence=str(verdict in USABLE).lower(), now_cited=str(now_cited).lower()))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    print(f'name-match associations (revision-2 universe + current): {len(rows)} pairs, {len({r["product"] for r in rows})} products; '
          f'now cited as evidence: {sum(r["now_cited"] == "true" for r in rows)}')
    print('verdicts: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['verdict'] for r in rows).most_common()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
