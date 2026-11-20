"""Integration review 2026-11-20: write the review findings and the per-batch remediation task list.

tables/integration_review_findings_2026-11-20.csv  findings of the review; 'verification' says how each was established
                                                   (code / diff read, automated audit, cached page text, page image viewed)
tables/remediation_tasks.csv                       per evidence file: audit counts and the work needed before any product of the
                                                   batch can be source-verified (generated from tables/evidence_audit_rows.csv)
Run after 09_audit_evidence.py."""
import csv, os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), 'tables')

F = [
    dict(id='F01', scope='repository', item='Products_json (161 files), tools/data_policy, tools/mandatory_properties, reports/, build_coverage_matrix.py, Coverage_Matrix*.xlsx, __pycache__',
         finding="PR #8 ingested 161 conversion drafts into Products_json and edited the shared policy (source_selection.py DATASET_PREP_PRODUCTS list, added so that test_only_declared_product_files_changed_since_baseline accepts the new files), shared checks and reports",
         verification='git diff ca1d4a7..a636501; source_selection.py diff read', action='restored to ca1d4a7 (commit e795fc8); drafts kept byte-identical in json_output/', status='fixed'),
    dict(id='F02', scope='readiness', item='878 products conversion_ready on main (764 at 07a50e4)',
         finding="rule was identity verified + template established + stage-5 'complete', where 'complete' only means every template field unit has a row; 283 of the 878 are programmatic extractions (S02 Afton 98, S03 Infineum 76, S05 Richful 109); 85 have no Reported row; none is source-verified",
         verification='commit-by-commit trace of tables/stage_summary.json; tables/evidence_audit_products.csv', action='05_stages.py rule changed: 0 conversion-ready; old figure kept as ready_under_previous_rule', status='fixed (downgraded)'),
    dict(id='F03', scope='checks', item='04_checks.py C08 / C10',
         finding="C10 (after P04) read field_evidence/*.csv but only checked row validity: no manifest, no coverage cross-check; C08 failed on main ('9/10 checks pass' in 92c7f50) and the work was merged anyway; 1,069 Reported rows (Afton 446, Infineum 623) have no page",
         verification='04_checks.py on the a636501 state and after restoration', action='C10 discovery + manifest + coverage; C11 validity gate; C12 audit freshness; C07 new rule', status='fixed'),
    dict(id='F04', scope='evidence', item='s22_vanderbilt.csv line 113, VANDERBILT:VANLUBE 0401 function_specific_markers.mo',
         finding="recorded 1.7 %; the sheet prints 'Molybdenum Content, %: 2.1' and 'Zinc Content, %: 1.7'",
         verification='page image DL2-13042 p.1 viewed 2026-11-20', action='correct in fm_s22_vanderbilt.py during source review', status='open'),
    dict(id='F05', scope='evidence', item='s05_richful.csv lines 638-639, RICHFUL:RF2214 function_specific_markers.p / .zn',
         finding="recorded P 5.5 and Zn 5.5 citing page 1; the SDS prints on page 4 'P Content 7.4 m% Zn Content 9.1m% pH value 5.5': the pH value was mapped into both element fields; review column says 'TDS text read in full' but the source is an SDS",
         verification='cached text of DL2-12798, all pages', action='correct during source review; an SDS value stays an SDS value under Rule 2', status='open'),
    dict(id='F06', scope='evidence', item='s04_lubrizol.csv line 41, LUBRIZOL:1038U elements.P',
         finding="recorded P 7 % from the SDS DL2-12194 p.1; no phosphorus content of 7 is printed anywhere in that SDS (the only '7,4 %' is a biodegradation result)",
         verification='cached text of DL2-12194, all pages', action='remove or re-source during source review: the value has no printed source', status='open'),
    dict(id='F07', scope='evidence', item='s18_eni.csv, ENI:ENI MX 5003 (Ca, Zn, P, N, flash point, kv100, density)',
         finding="the table is headed 'Value min | max' (Ca 0.47-0.74, Zn 3.51-4.73, P 3.17-4.27, N 0.87-1.28; flash point 120 in the min column); the evidence records each min as one 'typical' value, drops the max, cites page 1 (table on page 2), has no unit, and printed_text is the bare number",
         verification='page image DL2-11115 p.2 viewed 2026-11-20', action='re-map as ranges / bounds with units and page 2; check every Eni sheet with min / max columns', status='open'),
    dict(id='F08', scope='evidence', item='page citations (BRB, Eni, Lubrizol, ADNOC, Oronite ...)',
         finding="507 Reported numbers are not on the cited page; inspected samples are on another page of the same document (BRB PETROLAD 1846 on p.2 cited p.1; ADNOC ADbase on p.5 cited p.1; Lubrizol 1038 flash point on p.6 cited p.1)",
         verification='09_audit_evidence.py + page text of 4 samples', action='correct the page per row during source review', status='open'),
    dict(id='F09', scope='evidence', item='s47_adnoc.csv, EXISTING:ADNOC_ADBASE_* rows',
         finding='five-grade column table (kv100 2.3 / 3.05 / 4.35 / 6.18 / 8.05 mm2/s ...): the column assignment per grade needs a visual check; cited page 1, table on page 5',
         verification='cached text of DL2-12151', action='visual check of the table before any value is accepted', status='open'),
    dict(id='F10', scope='identity', item='decisions s47 / s54 / s55 / s60',
         finding='six pseudo-products (ADNOC:UNKNOWN_DOC_*, ERGON:UNKNOWN_SPEC_*, BAPCO:UNKNOWN_COA_*) and SHENYANG_GW:CATALOG with non-vocabulary status / relation (C05 failed): documents counted as products',
         verification='04_checks.py C05', action='dec_common.write() removes pseudo-keys and enforces vocabularies; documents keep their notes (relation unresolved_identity, or multi-product for the catalogue)', status='fixed'),
    dict(id='F11', scope='evidence', item='Missing rows',
         finding='9,961 of 12,837 Missing rows carry no note of what was inspected; in the programmatic batches a Missing row can mean only that a pattern did not match',
         verification='09_audit_evidence.py', action="confirm each Missing by reading, or mark it 'not assessed'", status='open'),
    dict(id='F12', scope='reproducibility', item='archive and cache locations',
         finding='01_ocr.py / 01_text_cache.py expected the archive inside the checkout, 04_checks.py had a hard-coded user path, and the caches are not in git: a second worktree could not read the sources',
         verification='code read', action='scripts/paths.py with SF_ARCHIVE_ZIP / SF_TEXT_CACHE / SF_OCR_CACHE', status='fixed'),
    dict(id='F13', scope='scripts', item='scripts/08_merge_into_products_json.py', finding='copies json_output/ into Products_json/',
         verification='code read', action='disabled (exits with a message)', status='fixed'),
]


def main():
    with open(os.path.join(T, 'integration_review_findings_2026-11-20.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(F[0].keys())); w.writeheader(); w.writerows(F)
    A = list(csv.DictReader(open(os.path.join(T, 'evidence_audit_rows.csv'), encoding='utf-8')))
    P = {p['product_key']: p for p in csv.DictReader(open(os.path.join(T, 'evidence_audit_products.csv'), encoding='utf-8'))}
    by, prods = defaultdict(Counter), defaultdict(set)
    for a in A:
        c = by[a['file']]; c['rows'] += 1; c[a['result']] += 1; prods[a['file']].add(a['product_key'])
        for fl in filter(None, a['flags'].split(' | ')):
            c[fl] += 1
        c['_prog'] += a['extraction'] == 'programmatic'
    out = []
    for f, c in sorted(by.items()):
        acts = []
        if c['page not available']: acts.append(f"add page citations to {c['page not available']} Reported rows")
        if c['number NOT found on cited page']: acts.append(f"re-check {c['number NOT found on cited page']} numbers not on the cited page")
        if c['text row (no number): words NOT found']: acts.append(f"re-check {c['text row (no number): words NOT found']} text rows")
        if c['Missing, no inspection note']: acts.append(f"confirm {c['Missing, no inspection note']} Missing rows by reading (or mark not assessed)")
        for k in ('value form inconsistent', 'numeric Reported row without unit', 'percentage basis unspecified', 'SDS source in an element / marker field'):
            if c[k]: acts.append(f'{c[k]} rows: {k}')
        acts.append('row-by-row source verification and sign-off in tables/source_verification.csv')
        out.append(dict(evidence_file=f, products=len(prods[f]), rows=c['rows'], extraction='programmatic' if c['_prog'] else 'reported read',
                        reported_number_found=c['number found on cited page'], reported_text_found=c['text row (no number): words found'],
                        not_found_or_no_page=c['number NOT found on cited page'] + c['page not available'] + c['text row (no number): words NOT found'],
                        missing_no_note=c['Missing, no inspection note'], products_auto_pass=sum(P[k]['auto_check'] == 'pass' for k in prods[f]), actions='; '.join(acts)))
    with open(os.path.join(T, 'remediation_tasks.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    print(len(F), 'findings;', len(out), 'remediation rows; auto-pass products', sum(o['products_auto_pass'] for o in out),
          [(o['evidence_file'], o['products_auto_pass']) for o in out if o['products_auto_pass']])


if __name__ == '__main__':
    main()
