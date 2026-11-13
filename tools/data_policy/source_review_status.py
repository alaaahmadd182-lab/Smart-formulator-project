"""Review state of every coverage-ledger row (read-only; run after lead_review.py and external_review.py).

The ledger labels rows mechanically. This report says, for each product x property row, which review it received:

  archive_lead_review_complete   an archive lead case reviewed with a definite outcome (usable evidence, already
                                 recorded, unrelated mention)
  external_review_complete       an external-source value re-read on an identified copy (external_review.csv: confirmed)
  evidence_unavailable           reviewed, but the evidence does not exist where it was sought: the archive documents do
                                 not print the value (lead outcome insufficient_evidence), or no copy of the external
                                 source could be obtained (inconclusive_source_unavailable)
  evidence_inconclusive          reviewed, but the document's identity could not be established (unresolved_identity)
  not_individually_reviewed      no case-by-case review: the row's state rests on the mechanical classification only
                                 (for example a technical value selected by page class, or Missing with no mention)

A row with both an external and a lead outcome takes the external one (the external source is what is selected).
Writes reports/data_policy/source_review_status.csv. Usage: python tools/data_policy/source_review_status.py
"""
import collections, csv, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P  # noqa: E402

LEAD_STATE = {'usable_evidence': 'archive_lead_review_complete', 'already_recorded': 'archive_lead_review_complete',
              'unrelated_mention': 'archive_lead_review_complete', 'insufficient_evidence': 'evidence_unavailable',
              'unavailable_source': 'evidence_unavailable', 'unresolved_identity': 'evidence_inconclusive'}
EXT_STATE = {'confirmed': 'external_review_complete', 'inconclusive_source_unavailable': 'evidence_unavailable'}
STATES = ('archive_lead_review_complete', 'external_review_complete', 'evidence_unavailable', 'evidence_inconclusive',
          'not_individually_reviewed')


def read(name):
    with open(os.path.join(P.REPORTS, 'data_policy', name), encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    ledger = read('source_coverage_ledger.csv')
    lead = {(r['product'], r['property']): r['outcome'] for r in read('lead_review.csv')}
    ext = {(r['product'], r['property']): r['outcome'] for r in read('external_review.csv')}
    bad = [k for k, o in lead.items() if o not in LEAD_STATE] + [k for k, o in ext.items() if o not in EXT_STATE]
    if bad:
        print('ERROR: unreviewed or unknown outcomes:', bad[:10])
        return 1
    rows = []
    for r in ledger:
        k = (r['product'], r['property'])
        state = EXT_STATE[ext[k]] if k in ext else LEAD_STATE[lead[k]] if k in lead else 'not_individually_reviewed'
        rows.append(dict(product=r['product'], property=r['property'], mandatory=r['mandatory'], status=r['status'],
                         selection_status=r['selection_status'], lead_outcome=lead.get(k, ''), external_outcome=ext.get(k, ''),
                         review_state=state))
    missing = [k for k in list(lead) + list(ext) if k not in {(r['product'], r['property']) for r in ledger}]
    out = os.path.join(P.REPORTS, 'data_policy', 'source_review_status.csv')
    with open(out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    c = collections.Counter(r['review_state'] for r in rows)
    m = collections.Counter(r['review_state'] for r in rows if r['mandatory'] == 'true')
    print(f'ledger rows (product x property): {len(rows)}')
    for s in STATES:
        print(f'  {s}: {c[s]} (mandatory {m[s]})')
    if missing:
        print(f'reviewed cases that are no longer ledger rows: {len(missing)}: {missing[:5]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
