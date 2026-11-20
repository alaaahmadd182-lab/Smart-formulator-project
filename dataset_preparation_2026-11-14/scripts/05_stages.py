"""Preparation stages per product, blocker log and cross-batch reconciliation candidates (run after 03_register.py).

The five stages are kept apart; a later stage is never implied by an earlier one:
  1 candidate detected            a product key exists (a name was seen)
  2 identity verified             >= 1 document whose SUBJECT (or printed grade on a multi-grade document) is this product was read
                                  in an identity decision; 'verified, open question' when its record carries an unresolved identity /
                                  alias / conflict note; 'candidate only' when it is only mentioned, or named from a file name
  3 class and template            'established' only for one of the three template classes without an open scope / fit question
  4 technical evidence reviewed   from tables/field_mapping_status.csv; a 'programmatic extraction' is reported as such, never as a review
  5 field-level mapping           'mapped: every template field has a row (generated; not source-verified)' when the batch script filled
                                  every field unit; 'complete (source-verified)' only with a sign-off row in tables/source_verification.csv
  conversion_ready (rule of the 2026-11-20 integration review) = stage 2 'verified' + stage 3 'established' + evidence READ (not
      programmatic) + source verification recorded + automated audit pass (09_audit_evidence.py: every Reported number found on its
      cited page, no OCR row without visual check, no SDS row in an element field, no value-form / unit / % basis flag, every Missing row
      states what was inspected) + no blockers. The earlier rule (2 + 3 + 'complete') is kept as 'ready_under_previous_rule' for
      comparison only; it made 878 products 'ready' from generated mappings alone.
Existing production records are reported separately (their evidence backlog lives in existing_product_comparison_2026-11-12).

Outputs: tables/product_stages.csv, tables/stage_summary.json, tables/blocker_log.csv, tables/reconciliation_candidates.csv.
Reconciliation: product keys from different batches / suppliers whose normalised printed grade is identical are listed; they are
merged ONLY by an entry in decisions_reconciliation.json with a documented basis. Default: 'open: not merged'."""
import csv, json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
T = os.path.join(PKG, 'tables')
OPEN_ID = re.compile(r'(?i)not merged|probably the same|possibly the same|conflict|inconsisten|misprint|customer code|confirm the grade|name from the file name|consolidation question|disagree|redacted')
OPEN_CLASS = re.compile(r'(?i)scope question|template fit|to confirm|provisional|schema gap|not stated|not printed|not established|booster|by brand family|class by series')
TEMPLATES = ('base_oil', 'additive_package', 'additive_component')
SUBJECT = ('subject', 'series sheet', 'grade on a multi-grade', 'covered by multi-grade', 'series / multi-grade')


def rd(n):
    p = os.path.join(T, n)
    return list(csv.DictReader(open(p, encoding='utf-8'))) if os.path.exists(p) else []


def wr(n, rows, cols):
    with open(os.path.join(T, n), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows)


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    prods, links, docs = rd('product_register.csv'), rd('document_product_links.csv'), rd('document_register.csv')
    fm = {r['product_key']: r for r in rd('field_mapping_status.csv')}
    AUD = {r['product_key']: r for r in rd('evidence_audit_products.csv')}          # 09_audit_evidence.py (automated)
    SV = {r['product_key']: (r['verified_by'] + ', ' + r['date']) for r in rd('source_verification.csv') if r.get('verified_by')}  # human sign-off
    L = defaultdict(list)
    for l in links:
        if l['source'] == 'identity decision':
            L[l['product_key']].append(l)
    out = []
    for p in prods:
        k, notes = p['product_key'], p['notes'] + ' ' + p['identity_evidence']
        ls = L.get(k, [])
        subj = [l for l in ls if l['role'].startswith(SUBJECT) and 'probable' not in l['role']]
        if p['status'] == 'existing' and not p['decision_file'].startswith('s'):
            s2 = 'existing record (no new-archive identity decision)'
        elif p['status'] == 'existing':
            s2 = 'existing record; new-archive documents linked'
        elif not subj:
            s2 = 'candidate only (mentioned / no subject document read)'
        elif OPEN_ID.search(notes):
            s2 = 'verified, open question'
        else:
            s2 = 'verified'
        mc = p['material_class']
        if mc.startswith('out_of'):
            s3 = 'out of template (excluded from conversion; kept in the inventory)'
        elif mc not in TEMPLATES:
            s3 = 'unresolved'
        elif OPEN_CLASS.search(p['notes']):
            s3 = 'open question'
        else:
            s3 = 'established'
        f = fm.get(k, {})
        s4raw, s5raw = f.get('evidence_review', 'not started'), f.get('field_mapping', 'not started')
        prog = 'programmatic' in s4raw
        s4 = 'programmatic extraction (not a reading review)' if prog else ('reported read (' + s4raw + ')' if s4raw != 'not started' else 'not started')
        au = AUD.get(k, {})
        sv = SV.get(k)
        if sv:
            s5 = 'complete (source-verified)'
        elif s5raw == 'complete':
            s5 = 'mapped: every template field has a row (generated; not source-verified)'
        else:
            s5 = s5raw
        ready_prev = 'yes' if (s2 == 'verified' and s3 == 'established' and s5raw == 'complete') else 'no'
        ready = 'yes' if (s2 == 'verified' and s3 == 'established' and not prog and sv and au.get('auto_check') == 'pass' and not f.get('blockers')) else 'no'
        out.append(dict(product_key=k, name=p['name'], supplier=p['supplier'], status=p['status'], material_class=mc, stage1_candidate='yes', stage2_identity=s2,
                        stage3_class_template=s3, stage4_evidence_review=s4, stage5_field_mapping=s5,
                        auto_check=au.get('auto_check', 'not audited' if s5raw == 'complete' else ''), auto_issues=au.get('auto_issues', ''),
                        source_verified=('yes (' + sv + ')') if sv else 'no', conversion_ready=ready, ready_under_previous_rule=ready_prev,
                        subject_documents=len(subj), documents_linked=len(ls), blockers=f.get('blockers', ''), decision_file=p['decision_file']))
    wr('product_stages.csv', out, list(out[0].keys()))
    new = [r for r in out if r['status'] != 'existing']
    mapped = [r for r in out if r['ready_under_previous_rule'] == 'yes']
    summ = dict(products_total=len(out), existing_records=len(out) - len(new), non_existing=len(new),
                stage2_identity=dict(Counter(r['stage2_identity'] for r in new)), stage3_class_template=dict(Counter(r['stage3_class_template'] for r in new)),
                stage4_evidence_review=dict(Counter(r['stage4_evidence_review'].split(' (')[0] for r in out)), stage5_field_mapping=dict(Counter(r['stage5_field_mapping'] for r in out)),
                conversion_ready=sum(r['conversion_ready'] == 'yes' for r in out),
                conversion_ready_rule='identity verified + template established + evidence READ (not programmatic) + sign-off in tables/source_verification.csv + 09_audit_evidence.py pass + no blockers',
                reported_ready_under_previous_rule=len(mapped),
                previous_rule_breakdown=dict(programmatic_extraction=sum(r['stage4_evidence_review'].startswith('programmatic') for r in mapped),
                                             auto_check_pass=sum(r['auto_check'] == 'pass' for r in mapped), auto_check_issues=sum(r['auto_check'] == 'issues' for r in mapped),
                                             source_verified=sum(r['source_verified'] != 'no' for r in mapped)),
                identity_verified_and_template_established=sum(r['stage2_identity'] == 'verified' and r['stage3_class_template'] == 'established' for r in new))
    # blockers
    B = []
    for d in docs:
        txt = d['note'] + ' ' + d['next_action']
        if d['next_action'].lower().startswith('blocker') or re.search(r'(?i)conflict|inconsisten|disagree|redacted', txt):
            B.append(dict(scope='document', key=d['sha256'][:12], file=d['canonical_file'], products=d['products'], issue=d['note'], next_action=d['next_action'], status='unresolved', decision_file=d['decision_file']))
        if d['relation'] in ('unresolved_identity', 'unreadable') and d['identity_status'].startswith('identity reviewed'):
            B.append(dict(scope='document', key=d['sha256'][:12], file=d['canonical_file'], products='', issue='identity reviewed but not established: ' + d['note'], next_action=d['next_action'], status='unresolved', decision_file=d['decision_file']))
    for p in prods:
        if re.search(r'(?i)conflict|inconsisten|disagree|misprint', p['notes']):
            B.append(dict(scope='product', key=p['product_key'], file='', products=p['product_key'], issue=p['notes'], next_action='resolve before conversion', status='unresolved', decision_file=p['decision_file']))
    wr('blocker_log.csv', B, ['scope', 'key', 'file', 'products', 'issue', 'next_action', 'status', 'decision_file'])
    # reconciliation candidates
    rp = os.path.join(PKG, 'decisions_reconciliation.json')
    RJ = json.load(open(rp, encoding='utf-8')) if os.path.exists(rp) else {}
    RD = RJ.get('decisions', {})
    G = defaultdict(list)
    for p in prods:
        n = re.sub(r'(?i)^(eni|lubimax|dowsyn|functional|additin|goncord|syncold)\s+', '', p['name'])
        n = re.sub(r'[^A-Z0-9]', '', n.upper())
        if len(n) >= 4:
            G[n].append(p)
    R = []
    for n, ps in sorted(G.items()):
        if len(ps) > 1:
            keys = sorted(x['product_key'] for x in ps)
            dec = RD.get(' = '.join(keys), {})
            R.append(dict(normalised_grade=n, product_keys=' = '.join(keys), suppliers=' | '.join(sorted({x['supplier'] for x in ps})),
                          same_supplier='yes' if len({x['supplier'] for x in ps}) == 1 else 'no', decision=dec.get('decision', 'open: not merged'), basis=dec.get('basis', '')))
    for m in RJ.get('manual', []):
        R.append(dict(normalised_grade='(manual pair)', product_keys=m['product_keys'], suppliers='', same_supplier='', decision=m['decision'], basis=m['basis']))
    wr('reconciliation_candidates.csv', R, ['normalised_grade', 'product_keys', 'suppliers', 'same_supplier', 'decision', 'basis'])
    summ.update(blockers=len(B), reconciliation_candidates=len(R), reconciliation_open=sum(r['decision'].startswith('open') for r in R))
    json.dump(summ, open(os.path.join(T, 'stage_summary.json'), 'w', encoding='utf-8'), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == '__main__':
    main()
