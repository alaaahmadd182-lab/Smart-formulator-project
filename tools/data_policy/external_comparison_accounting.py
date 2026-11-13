"""Account for every value whose selected source is an external (URL) source: is it compared with an SDS value, and
if not, why not (read-only; run after tds_sds_inventory.py, source_coverage_ledger.py and lead_review.py).

One row per value object with status Reported/Calculated whose source is a URL (counting unit: value object, i.e.
product x field path). Each row gets exactly one comparison status:

  paired                                    the inventory holds at least one pair of this external technical value with an SDS value
  inapplicable_non_numeric                  the value is a text, classification, claim or block: no numeric TDS-SDS comparison exists
  inapplicable_selected_source_is_sds       the external source is itself a safety data sheet (registry title)
  inapplicable_different_quantity           reviewed: the SDS prints a different quantity under a similar label
  unavailable_no_sds_document               no SDS-class document is associated with the product
  unavailable_sds_does_not_print_property   SDS documents are associated, and no SDS page mentions the property (text layer)
  unresolved_external_source_not_obtained   no copy of the external source could be obtained: the value was not re-read,
                                            so it is not verified and nothing is concluded from it
  unresolved_sds_identity                   reviewed: the SDS cannot be tied to this exact product
  unresolved_property_outside_coverage_ledger  numeric value of a property the coverage ledger does not cover: not assessed
  unresolved_not_reviewed                   an SDS page mentions the property, no pair exists and no reviewed reason is
                                            recorded (the tool exits 1)

The evidence state of the external source is reported separately (column evidence_state) and is never upgraded here:
'copy read in the external review', 'registry status ... not re-read in the external review', or 'external source not
obtained'. A reviewed reason comes from external_review_decisions.json ('comparison_reviews') or from the lead review.

Writes reports/data_policy/external_comparison_accounting.csv. Exit 1 on an unaccounted value or a contradiction.
Usage: python tools/data_policy/external_comparison_accounting.py
"""
import collections, csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P  # noqa: E402
import tds_sds_inventory as INV  # noqa: E402

STATUSES = ('paired', 'inapplicable_non_numeric', 'inapplicable_selected_source_is_sds', 'inapplicable_different_quantity',
            'unavailable_no_sds_document', 'unavailable_sds_does_not_print_property', 'unresolved_external_source_not_obtained',
            'unresolved_sds_identity', 'unresolved_property_outside_coverage_ledger', 'unresolved_not_reviewed')
LEAD_STATUS = {'unrelated_mention': 'inapplicable_different_quantity', 'unresolved_identity': 'unresolved_sds_identity',
               'insufficient_evidence': 'unavailable_sds_does_not_print_property'}


def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def numeric(n):
    return is_number(n.get('value')) or is_number(n.get('min')) or is_number(n.get('max'))


def decide(n, f, prop, ext_class, state, ledger_row, pairs, sds_docs, review, lead):
    """(status, reason) for one external-sourced value object."""
    if state == INV.NOT_OBTAINED:
        return 'unresolved_external_source_not_obtained', ('No copy of the external source could be obtained; the value was not re-read and is not '
                                                           'verified.' + (f' {len(pairs)} inventory pair(s) exist and are kept as comparability unknown.' if pairs else ''))
    if ext_class == 'SDS':
        return 'inapplicable_selected_source_is_sds', 'The selected external source is itself a safety data sheet (registry title).'
    if not numeric(n):
        return 'inapplicable_non_numeric', 'Text, classification, claim or block: no numeric technical-SDS comparison exists.'
    if pairs:
        return 'paired', '; '.join(sorted({f"{r['sds_file']} p.{r['sds_page']}: {r['comparability']}" for r in pairs}))
    if review:
        return review['status'], review['reason']
    if ledger_row is None:
        return 'unresolved_property_outside_coverage_ledger', 'Numeric value of a property the coverage ledger does not cover; no SDS comparison was assessed.'
    if not ledger_row['sds_pages_with_label']:
        if not sds_docs:
            return 'unavailable_no_sds_document', 'No SDS-class document is cited by or associated with the product.'
        return 'unavailable_sds_does_not_print_property', ('No SDS page of the associated documents mentions the property (text layer): '
                                                           + ', '.join(sds_docs) + ((' Not searchable: ' + ledger_row['unsearchable_documents'])
                                                                                    if ledger_row['unsearchable_documents'] else ''))
    if lead and lead['outcome'] in LEAD_STATUS:
        return LEAD_STATUS[lead['outcome']], f"lead review ({lead['outcome']}): {lead['reason']}"
    return 'unresolved_not_reviewed', 'An SDS page mentions the property, no pair exists and no reviewed reason is recorded: ' + ledger_row['sds_pages_with_label']


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    rp = os.path.join(P.REPORTS, 'data_policy')

    def read(name):
        with open(os.path.join(rp, name), encoding='utf-8') as fh:
            return list(csv.DictReader(fh))
    reg, ext_state = INV.load_external()
    with open(INV.EXTERNAL_DECISIONS, encoding='utf-8') as fh:
        reviews = json.load(fh).get('comparison_reviews', {})
    ledger = {(r['product'], r['property']): r for r in read('source_coverage_ledger.csv')}
    lead = {(r['product'], r['property']): r for r in read('lead_review.csv')}
    classes = collections.defaultdict(set)
    for r in read('document_classes.csv'):
        classes[r['file']].add(r['class'])
    inv = collections.defaultdict(list)
    for r in read('tds_sds_comparisons.csv'):
        inv[(r['product'], r['property'], r['tds_file'])].append(r)
    prods = P.load_products()
    rows, errors = [], []
    for pid, p in prods.items():
        cited = sorted({P.src(n)[0] for d in p['files'].values() for _, n in P.value_objects(d.get('fields', {})) if P.src(n)[0]})
        for rel, d in p['files'].items():
            for path, n in P.value_objects(d.get('fields', {})):
                f = P.src(n)[0]
                if not INV.is_url(f) or n.get('status') not in ('Reported', 'Calculated'):
                    continue
                prop = INV.prop_of(path)
                lr = ledger.get((pid, prop))
                docs = [x.split(' (')[0].strip() for x in (lr['documents_examined'].split(';') if lr else cited)]
                sds_docs = sorted({x for x in docs if 'SDS' in classes.get(x, ()) or (INV.is_url(x) and INV.external_class(x, reg) == 'SDS')})
                pairs = inv.get((pid, prop, f), [])
                cls = INV.external_class(f, reg)
                state = INV.external_state(f, reg, ext_state)
                status, reason = decide(n, f, prop, cls, state, lr, pairs, sds_docs, reviews.get(f'{pid}|{prop}'), lead.get((pid, prop)))
                if cls is None:
                    errors.append(f'{pid} {path}: URL not in source_registry.json')
                if status == 'paired' and state == INV.NOT_OBTAINED:
                    errors.append(f'{pid} {path}: a source that was not obtained is counted as paired')
                if status == 'unresolved_not_reviewed':
                    errors.append(f'{pid} {path}: not accounted for')
                e = reg.get(f) or {}
                rows.append(dict(product=pid, material_class=d.get('material_class'), tier=d.get('tier'), field=path, property=prop,
                                 value=n.get('value'), min=n.get('min'), max=n.get('max'), qualifier=n.get('qualifier'), value_kind=n.get('value_kind'),
                                 unit=n.get('unit'), test_temperature_c=n.get('test_temperature_c'), method=n.get('method'),
                                 printed_text=n.get('printed_text'), source_url=f, source_revision_date=P.src(n)[2] or '',
                                 registry_title=e.get('title', ''), registry_issuer=e.get('issuer', ''), registry_edition=e.get('edition') or '',
                                 external_class=cls or 'unregistered', evidence_state=state,
                                 ledger_selection_status=lr['selection_status'] if lr else '(not a ledger property)',
                                 inventory_pairs=len(pairs), comparison_status=status, reason=reason))
    out = os.path.join(rp, 'external_comparison_accounting.csv')
    with open(out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    print(f'values with an external selected source (value objects): {len(rows)}; in the coverage ledger: '
          f'{sum(r["ledger_selection_status"] != "(not a ledger property)" for r in rows)} '
          f'(external_selected {sum(r["ledger_selection_status"] == "external_selected" for r in rows)}, '
          f'pending {sum(r["ledger_selection_status"] == "pending" for r in rows)})')
    for scope, sub in (('all', rows), ('ledger external_selected', [r for r in rows if r['ledger_selection_status'] == 'external_selected'])):
        c = collections.Counter(r['comparison_status'] for r in sub)
        print(f'  {scope}: ' + ', '.join(f'{s} {c[s]}' for s in STATUSES if c[s]))
    print('  evidence state: ' + '; '.join(f'{k}: {v}' for k, v in sorted(collections.Counter(('registry-verified, not re-read in the external review' if r['evidence_state'].startswith('registry') else r['evidence_state']) for r in rows).items())))
    print(f'  inventory pairs with an external technical side: {sum(r["inventory_pairs"] for r in rows)} for {sum(r["inventory_pairs"] > 0 for r in rows)} values')
    for e in errors:
        print('ERROR', e)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
