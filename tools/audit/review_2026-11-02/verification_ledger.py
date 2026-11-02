"""Citation-level verification ledger for the audit findings (read-only on sources).

Inventory (every row is one source used by one finding):
  1. every value citation (the rows of source_checks_v5.csv);
  2. documents cited only in an explanation (CF-166, CF-167: the Afton claims tables);
  3. every source a finding names in its explanation, verification, comparability, nature or follow-up text (API 1509,
     PubChem, ASTM D874, identity_review.md, Internet Archive captures, ...), found with the patterns of
     referenced_sources.REF_PATTERNS. A reference covered by one of the finding's value citations adds no row; any other
     reference needs an entry in referenced_sources.ENTRIES, and a reference without one is listed as unresolved.

Each row is classified by ledger_rules.py from explicit evidence only: the keys verified by check_columns.py
(column_checked_citations.json) and explicit reviewer verdicts (association_review.json, expected_source_results.json,
referenced_sources.py). Nothing is verified by default.

Writes docs/audit_review_2026-11-02/verification_results/citation_ledger.csv and ledger_summary.json.

Usage: python tools/audit/review_2026-11-02/verification_ledger.py
Exit codes: 0 ran and verification is complete (no row in D or E);
            3 ran successfully, verification incomplete (rows in D or E; listed);
            1 could not run (missing input).
"""
import collections, csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import ledger_rules as L
import referenced_sources as RS
import review_lib as R

RES = os.path.join(R.ROOT, 'docs', 'audit_review_2026-11-02', 'verification_results')
TEXT_FIELDS = ('explanation', 'verification', 'verification_priority', 'comparability', 'nature', 'follow_up_reason')
EXPLANATION_DOCS = [  # documents cited only in the explanation text, with the reviewer's verdict
    ('CF-166', 'DL2-11796.pdf', '2', 'claims table (05/18) extracted by afton_matrices.py and read on the 220 dpi render: columns only in 05/18 and the 45 shared cells'),
    ('CF-166', 'DL2-15568.pdf', '2', 'claims table (04/22) extracted and read on the render: columns only in 04/22, added row API CK-4 10W-40; shared cells agree'),
    ('CF-167', 'DL2-11412.PDF', '2', 'claims table (05/18): no API SN, MB 229.3 or RN 0700 column and neither added row; footnote 6 "Formulations, available in Q2 2018"'),
    ('CF-167', 'DL2-14639.pdf', '2', 'claims table (08/18): the two added rows and their marked columns; footnote 6 "11.15% HiTEC® 12252 = 10.8% HiTEC® 12200 + 0.35% HiTEC® 9552"'),
]


def detect_refs(text):
    keys = {f'doc:{m.lower()}' for m in re.findall(r'DL2-\d{5}\.(?:pdf|PDF|jpeg|jpg)', text)}
    keys |= {k for k, p in RS.REF_PATTERNS.items() if re.search(p, text)}
    return keys


def covered(files):
    keys = {f'doc:{os.path.basename(str(f)).split(" (")[0].lower().replace("%20", " ")}' for f in files}
    for p, ks in RS.COVERED_BY_CITATION:
        if any(re.search(p, str(f)) for f in files):
            keys |= ks
    return keys


def load(path, default=None):
    if not os.path.exists(path):
        if default is not None:
            return default
        sys.exit(f'missing input: {path}')
    return json.load(open(path, encoding='utf-8'))


def main():
    F = {f['id']: f for f in load(os.path.join(R.HERE, 'output', 'findings_v5.json'))}
    checks_path = os.path.join(RES, 'source_checks_v5.csv')
    if not os.path.exists(checks_path):
        print('missing input:', checks_path); return 1
    rows = list(csv.DictReader(open(checks_path, encoding='utf-8')))
    colck = set(load(os.path.join(RES, 'column_checked_citations.json')))
    verdicts = dict(load(os.path.join(R.HERE, 'expected_source_results.json'), {}))
    verdicts.update(load(os.path.join(R.HERE, 'association_review.json')))  # the association review wins over older notes
    out = []

    def add(fid, kind, src, page, value, check, cat, how):
        out.append(dict(id=fid, kind=kind, source=src, page=page, value=value, number_check=check, category=cat,
                        category_label=L.LABEL[cat], how_verified=how))

    files_by_id = collections.defaultdict(set)
    for r in rows:
        k = f"{r['id']}#{r['value_index']}#{r['file']}"
        files_by_id[r['id']].add(r['file'])
        cat = L.classify_citation(k, r['result'], colck, verdicts)
        v = verdicts.get(k)
        how = ('value in its grade column and property row (check_columns.py)' if cat == 'A' and k in colck else
               f"{v.get('verdict')}: {v.get('note')}" if isinstance(v, dict) else
               'number found on the cited page; association not reviewed' if cat == 'D' else f"no verdict ({r['result']})")
        add(r['id'], 'value citation', r['file'], r['page'], r['value'], r['result'], cat, how)
    for fid, src, page, note in EXPLANATION_DOCS:
        files_by_id[fid].add(src)
        cat = L.classify_verdict({'verdict': 'verified', 'basis': 'matrix extraction + visual check'})
        add(fid, 'document cited in the explanation', src, page, '-', '-', cat, f'verified: {note}')
    entries = collections.defaultdict(list)
    for e in RS.ENTRIES:
        entries[(e[0], e[1])].append(e)
    used = set()
    for fid, f in F.items():
        refs = detect_refs(' '.join(str(f.get(x) or '') for x in TEXT_FIELDS)) - covered(files_by_id[fid])
        for ref in sorted(refs | {k for (i, k) in entries if i == fid}):
            if ref.startswith('doc:') and ref not in {k for (i, k) in entries if i == fid} and ref in covered(files_by_id[fid]):
                continue
            es = entries.get((fid, ref))
            if not es:
                add(fid, 'referenced source', ref, '-', '-', '-', 'E', 'referenced in the finding text; no verdict recorded')
                continue
            for (_, _, src, page, verdict, basis, note) in es:
                used.add((fid, ref))
                cat = L.classify_verdict({'verdict': verdict, 'basis': basis})
                add(fid, 'referenced source', src, page, '-', '-', cat, f'{verdict} ({basis}): {note}')
    with open(os.path.join(RES, 'citation_ledger.csv'), 'w', encoding='utf-8-sig', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]), lineterminator='\r\n'); w.writeheader(); w.writerows(out)
    S = L.summarize([x['category'] for x in out])
    by_kind = collections.Counter(x['kind'] for x in out)
    S.update(findings=len({x['id'] for x in out}), by_kind=dict(by_kind), no_citation=sorted(set(F) - {x['id'] for x in out}),
             unresolved=[{k: x[k] for k in ('id', 'kind', 'source', 'how_verified')} for x in out if x['category'] in ('D', 'E')])
    json.dump(S, open(os.path.join(RES, 'ledger_summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"sources examined: {S['total']} in {S['findings']} findings ({', '.join(f'{v} {k}s' for k, v in by_kind.items())})")
    for c in ('A', 'B', 'C', 'D', 'E', 'N'):
        print(f'  {c} {L.LABEL[c]}: {S[c]}')
    print(f"fully verified: {S['verified']}; automated text presence only: {S['D']}; unresolved: {S['E']}; not used as evidence: {S['N']}")
    print('findings with no source row:', S['no_citation'])
    for u in S['unresolved']:
        print(f"  UNRESOLVED {u['id']} {u['kind']}: {u['source']} — {u['how_verified'][:120]}")
    print('VERIFICATION COMPLETE:', 'YES' if S['complete'] else f"NO ({S['D'] + S['E']} sources not fully verified)")
    return 0 if S['complete'] else 3


if __name__ == '__main__':
    sys.exit(main())
