"""Old-versus-new comparison, step 3: focused checks. Read-only. Exit code 1 if any check fails.

  counting       the 88/42 statistic reconciles with 66/25, and with the reviewed exclusions
  false matches  the two known false revision matches are excluded, keep a preserved link, and feed no proposal
  ledger         every earlier inventory link and every full-text candidate is in the ledger with an allowed status
  identity       grade suffixes are never merged by the search pattern
  proposals      every proposed change cites a new-archive file with a hash, a page and printed text
  preservation   archives, snapshot, working-tree copies of snapshot files, inventory reports, Git state unchanged

Usage: python existing_product_comparison_2026-11-12/scripts/03_checks.py
"""
import csv, hashlib, importlib.util, json, os, re, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
ROOT = os.path.dirname(BASE)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
T = os.path.join(BASE, 'tables')
NEW_ZIP = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip'
INV_ZIP = r'C:\Users\windo\OneDrive\Desktop\SmartFormulator_inventory_review_2026-11-12.zip'
EXPECT = dict(old_archive='6488b08f9729c4988c8e73bfe51dac355f64ee601e78554591a3450ba5f5497a', new_archive='62565d5c7a2afc2203536c241004cd4af7f62866a4bfe4f70801b378cf2c78b1',
              snapshot_manifest='8b63a5b642cf691fb2389692bc4399f6da1ae5d523f2cf44d45cbfb311869fbb', inventory_zip='280d0685cc581ebbf8d1bf25e299deab5249b9b67d85c206b01b702487336124',
              git_status_hash='2de292fe3eabccb9', head='43e7f8b5639f7d7169a2b5691bc187799f0dbe02')
SDS_UNSPEC = 'SDS reported value; statistical basis unspecified'
ALLOWED = {'completed', 'unresolved', 'excluded with reason', 'not yet assessed'}
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('PASS  ' if ok else 'FAIL  ') + name + (f'  [{detail}]' if detail else ''))


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def rd(p):
    with open(p, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    with open(os.path.join(T, 'corrected_inventory_statistics.json'), encoding='utf-8') as fh:
        st = json.load(fh)
    with open(os.path.join(INV, 'tables', 'inventory_statistics.json'), encoding='utf-8') as fh:
        orig = json.load(fh)
    led = rd(os.path.join(T, 'progress_ledger.csv'))
    inv = rd(os.path.join(INV, 'tables', 'existing_product_matches.csv'))
    cand = rd(os.path.join(T, 'candidate_relationships.csv'))
    fld = rd(os.path.join(T, 'field_level_comparison.csv'))
    prop = rd(os.path.join(T, 'proposed_json_changes_NOT_APPLIED.csv'))

    # Eleventh pass: every action that proposes a JSON change (propose_* and capture_from_old_source) must be in the
    # proposals table, in the counts and under the readiness rules; earlier the prefix filter dropped capture rows.
    bspec = importlib.util.spec_from_file_location('build', os.path.join(HERE, '02_build.py'))
    bmod = importlib.util.module_from_spec(bspec); bspec.loader.exec_module(bmod)
    want = [r for r in fld if bmod.is_proposal(r['recommended_action'])]
    pk = {(r['product_id'], r['field_path'], r['new_source_file'], r['decision_file']) for r in prop}
    check('proposals: every proposing row (propose_* and capture_from_old_source) is in the proposals table, the count and the readiness rules',
          len(prop) == len(want) == st['fields']['proposed']
          and all((r['product_id'], r['field_path'], r['new_source_file'], r['decision_file']) in pk for r in want)
          and not [r for r in want if r['action_readiness'] == 'no action proposed']
          and bmod.is_proposal('capture_from_old_source') and bmod.is_proposal('propose_add') and not bmod.is_proposal('no_change'),
          f'{len(prop)} proposals, {sum(1 for r in prop if r["recommended_action"] == "capture_from_old_source")} capture_from_old_source')
    jq = bmod.JSON_QUOTED
    check('status: no proposal is ready while its old-source statement relies on the JSON quotation or an undocumented earlier comparison',
          not [r for r in prop if r['action_readiness'].startswith('ready') and jq.search(r['old_source_review'])]
          and jq.search('re-read manually: DL2-1.pdf as quoted in the JSON printed_text') and jq.search('values as compared in the ninth pass')
          and not jq.search('re-read manually: DL2-1.pdf whole text (twelfth pass)'),
          f"{sum(1 for r in prop if jq.search(r['old_source_review']))} proposals with such statements")
    ea = [r for r in prop if r['product_id'] == 'EXXONMOBIL_ESTEREX_A34' and r['field_path'] == 'flash_point']
    check('case: Esterex A34 PMCC flash point is a proposal that keeps the D92 COC value selected and adds D93 as an alternate (outcome in_old_source_not_captured)',
          len(ea) == 1 and ea[0]['recommended_action'] == 'capture_from_old_source' and ea[0]['comparison_outcome'] == 'in_old_source_not_captured'
          and 'D93' in ea[0]['new_source_printed'] and '170' in ea[0]['new_source_printed'] and 'COC value stays the selected value' in ea[0]['reason'])

    # counting
    o, b, n, a = st['original_statistic'], st['of_which_byte_identical_to_existing_archive'], st['new_documents_only'], st['new_documents_only_after_reviewed_exclusions']
    check('counting: original statistic is the one in the automated report (88 / 42)', o['links'] == orig['new_documents_naming_existing_product_in_field_or_title'] == 88
          and o['products'] == orig['existing_products_with_new_document_naming_them_in_field_or_title'] == 42)
    check('counting: 88 = 66 new-document links + 22 links to files already in the archive', o['links'] == n['links'] + b['links'] and n['links'] == 66 and n['products'] == 25, f'{n["links"]} + {b["links"]}')
    check('counting: 66 = 59 additional-evidence + 7 revision-candidate links', sum(n['split'].values()) == n['links'])
    check('counting: after the reviewed exclusions 64 links and 5 revision candidates remain', a['links'] == n['links'] - len(st['reviewed_exclusions']) == 64 and st['revision_candidates']['after_reviewed_exclusions'] == 5)
    pl = st['product_linkage']
    check('counting: hash linkage (202) kept beside the text search (194); both + hash-only + text-only + neither = 264',
          pl['with_cited_source_byte_identical_in_new_archive'] == 202 and pl['both'] + pl['hash_only'] + pl['text_only'] + pl['neither'] == pl['products_total'] == 264
          and pl['both'] + pl['hash_only'] == 202 and pl['both'] + pl['text_only'] == pl['named_in_searched_text_of_new_archive'],
          f'both {pl["both"]}, hash only {pl["hash_only"]}, text only {pl["text_only"]}, neither {pl["neither"]}')

    # false matches
    by = {(r['product_id'], r['file']): r for r in led}
    f1 = by.get(('CHEVRON_OLOA_59766', 'DL2-11779.pdf'))
    f2 = next((r for r in led if r['product_id'] == 'YUBASE_6' and r['file'].startswith('OLOA%2055603')), None)
    for label, r in (('OLOA 65770 document DL2-11779.pdf is not an OLOA 59766 revision', f1), ('the OLOA 55603 presentation is not a Yubase 6 revision', f2)):
        check('false match: ' + label, r is not None and r['relationship_status'] == 'excluded with reason' and 'G' in r['reviewed_categories'].split(',')
              and 'D' in r['reviewed_categories'].split(',') and 'Preserved' in r['review_note'])
    bad_files = {r['file'] for r in (f1, f2) if r}
    check('false match: no field row or proposal rests on the two excluded documents for those products',
          not [r for r in fld if r['new_source_file'] in bad_files and r['product_id'] in ('CHEVRON_OLOA_59766', 'YUBASE_6')])
    check('false match: byte-identical files are never revision candidates', not [r for r in led if r['suggested_relationship'].startswith('F') and r['reviewed_categories'] == 'A'])

    # ledger
    keys = {(r['product_id'], r['sha256']) for r in led}
    check('ledger: all 443 earlier inventory links are retained', all((r['product_id'], r['sha256']) in keys for r in inv) and len(inv) == 443)
    check('ledger: all full-text candidates are retained', all((r['product_id'], r['sha256']) in keys for r in cand), f'{len(cand)} candidates, {len(led)} ledger rows')
    check('ledger: no duplicate (product, document) rows', len(keys) == len(led))
    check('ledger: every row has an allowed relationship status', all(r['relationship_status'] in ALLOWED for r in led))
    check('ledger: every link has a separate field-verification and coverage status', all(r['field_verification_status'] and r['source_to_json_coverage'] for r in led))
    check('ledger: unreviewed links are not presented as assessed', all(r['field_verification_status'] == 'not yet assessed' for r in led if r['relationship_status'] == 'not yet assessed'))
    scr_p = os.path.join(T, 'duplicate_source_coverage_screen.csv')
    scr = rd(scr_p) if os.path.exists(scr_p) else []
    check('screen: the duplicate-source coverage screen covers every A link and labels every row as an automated screen, not a reading',
          scr and {(r['product_id'], r['sha256']) for r in scr} == {(r['product_id'], r['sha256']) for r in led if r['reviewed_categories'] == 'A'}
          and all(r['screen_status'].startswith('AUTOMATED SCREEN ONLY') for r in scr), f'{len(scr)} rows')
    # Tenth pass: a duplicate whose coverage was assessed by READING it (decision file, not the hash rule) may say so;
    # every hash-only duplicate still carries no coverage claim.
    def dup_ok(r):
        if r['batch'] == 'automatic (hash)':
            return r['source_to_json_coverage'] == 'not assessed'
        return r['source_to_json_coverage'] == 'not assessed' or r['source_to_json_coverage'].startswith('assessed by reading')
    check('ledger: exact duplicates carry no claim that their content was fully ingested (only a reviewed reading may assess coverage)',
          all(dup_ok(r) for r in led if r['reviewed_categories'] == 'A')
          and not dup_ok(dict(batch='automatic (hash)', source_to_json_coverage='assessed by reading: all captured'))
          and not dup_ok(dict(batch='x', source_to_json_coverage='all values captured')))
    # Tenth pass: generic product numbers (e.g. 'RF6079', 'P-31') count only when the supplier is on the same page, or
    # on the reviewed pages of a reviewed document (scripts/reviewed_generic_alias_pairs.json). Catalogues that name the
    # supplier only on the cover were missed before; known false matches must stay out.
    with open(os.path.join(HERE, 'reviewed_generic_alias_pairs.json'), encoding='utf-8') as fh:
        rg = json.load(fh)
    rp = {(x['product_id'], x['sha256']) for x in rg['reviewed_pairs']}
    via = {(r['product_id'], r['sha256']) for r in cand if r.get('found_via', '').startswith('full-text search + reviewed')}
    lk = [(r['product_id'], r['sha256']) for r in led]
    check('candidates: every reviewed catalogue / generic-alias pair is linked exactly once in the ledger, through the reviewed mapping',
          len(rp) == 18 and rp == via and all(lk.count(k) == 1 for k in rp), f'{len(via & rp)} of {len(rp)} linked')
    check('candidates: every reviewed pair records its document-owner evidence, identity evidence and admitted pages',
          all(x['document_owner_evidence'] and x['identity_evidence'] and x['pages'] for x in rg['reviewed_pairs']))
    fm = {(x['product_id'], x['sha256']) for x in rg['known_false_generic_matches']}
    check('candidates: none of the reviewed false generic matches (other suppliers\' 150N/600N, numbers, Ultra S-8) is a candidate or a ledger link',
          len(fm) == 12 and not (fm & {(r['product_id'], r['sha256']) for r in cand}) and not (fm & set(lk)), f'{len(fm)} known false matches')
    r79all = [r for r in fld if r['product_id'] == 'RICHFUL_RF6079' and r['field_path'] == 'published_formulations']
    r79 = [r for r in r79all if r['new_source_file'] == 'RF6079%20Booklet.pdf']
    check('case: no other RF6079 formulation row selects one printing of the CDP blend RX210314101',
          not [r for r in r79all if r not in r79 and 'RX210314101' in r['new_source_printed']])
    def rf6079_ok(r):
        t = r['new_source_printed'] + ' ' + r['reason']
        return (r['recommended_action'] == 'propose_add_and_record_conflict' and 'unresolved' in r['reason'] and 'no page is preferred' in r['reason']
                and all(x in t for x in ('36.0', '47.35', 'p.8', 'p.11')))
    check('case: RF6079 swapped EHC 50 / EHC 110 shares stay unresolved with both printings (p.8 and p.11) cited',
          len(r79) == 1 and rf6079_ok(r79[0]) and not rf6079_ok(dict(r79[0], reason='EHC50 47.35 selected from p.11', recommended_action='propose_add')))
    check('regression: the generic-alias rule is not relaxed beyond the reviewed pairs (plain full-text candidates unchanged at 1,267)',
          sum(1 for r in cand if r.get('found_via', 'full-text search') == 'full-text search') == 1267)

    # identity
    spec = importlib.util.spec_from_file_location('cand', os.path.join(HERE, '01_candidates.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    rx = m.alias_regex
    cases = [('HiTEC 12204', 'HiTEC® 12204L', False), ('HiTEC 12204L', 'HiTEC® 12204L @ 14.2', True), ('HiTEC 5748', 'HiTEC® 5748A', False), ('HiTEC 5748', 'HiTEC® 5748 4.8', True),
             ('HiTEC 12210', 'HiTEC 12210M', False), ('ETRO 4', 'ETRO 4+', False), ('ETRO 4', 'ETRO 4 Plus', False), ('Lubrizol 3700', 'LUBRIZOL 3700D', False),
             ('OLOA 59766', 'OLOA 65770', False), ('Yubase 4', 'Yubase 4+', False), ('Lubrizol 7077', 'Lubrizol® 7077D', False)]
    wrong = [c for c in cases if bool(rx(c[0]).search(c[1])) != c[2]]
    check('identity: grade suffixes are not merged by the search pattern (11 cases)', not wrong, str(wrong) if wrong else '')
    # Safeguard (fifth pass): every action that can add or change a product value counts, including
    # propose_update_with_history, propose_selection_review*, propose_record_conflict and propose_historical_note.
    # The only exception is an explicitly evidenced, scoped interchangeability NOTE, which transfers no property.
    def p_5748a_any(r, pid='AFTON_HITEC_5748', other='5748A'):
        if r['product_id'] != pid or other not in r['new_source_printed'] or not (r['recommended_action'].startswith('propose') or r['recommended_action'] == 'capture_from_old_source'):
            return False
        scoped_note = (r['recommended_action'] == 'propose_note' and re.search(r'interchang', r['reason'], re.I)
                       and re.search(r'scope', r['reason'], re.I) and re.search(r'no 5748A data', r['reason']))
        return not scoped_note
    check('identity: no value is added or changed for HiTEC 5748 from HiTEC 5748A evidence by ANY proposing action (only a scoped interchangeability note is allowed)',
          not [r for r in prop if p_5748a_any(r)])
    _b = dict(product_id='AFTON_HITEC_5748', new_source_printed='HiTEC 5748A (ND-OCP) Shear Stability Index 25', recommended_action='propose_update_with_history', reason='update SSI')
    check('regression: an incorrect value update of HiTEC 5748 from 5748A text via propose_update_with_history is caught, as are selection review, conflict and an unscoped note; the scoped interchangeability note passes',
          p_5748a_any(_b) and p_5748a_any(dict(_b, recommended_action='propose_selection_review')) and p_5748a_any(dict(_b, recommended_action='propose_record_conflict'))
          and p_5748a_any(dict(_b, recommended_action='propose_historical_note')) and p_5748a_any(dict(_b, recommended_action='propose_note', reason='note the 5748A value'))
          and not p_5748a_any(dict(_b, recommended_action='propose_note', reason='A conditional interchange statement made for one programme. Propose a note with that scope; no 5748A data may be used for HiTEC 5748.'))
          and not p_5748a_any(dict(_b, recommended_action='no_change')))

    # proposals
    check('proposals: every proposed change cites a new-archive file with hash, page and printed text',
          all(len(r['new_source_sha256']) == 64 and r['new_source_page'] and r['new_source_printed'] for r in prop), f'{len(prop)} proposals')
    check('proposals: every field row names an existing product and a resolvable current field or says none exists', all(r['current_status'] != 'product not found' for r in fld))

    # Destination check (sixteenth pass). The build reports a record-level list (open_questions, conflicts, source_documents)
    # as 'top-level list (...)'; 'no such field in the template' is left only for a path that resolves nowhere. A path in
    # parentheses is an explicit 'no template field' label. A conflict entry is never proposed into open_questions.
    def p_dest_bad(r):
        fp = r['field_path']
        if fp.startswith('('):
            return False
        if r['current_status'] in ('no such field in the template', 'product not found') or r['current_status'].startswith('no tier'):
            return True
        top = fp.split(' (')[0].split('[')[0]
        return r['recommended_action'] == 'propose_record_conflict' and top == 'open_questions'
    _d = dict(field_path='open_questions', current_status='top-level list (open_questions), not a template field', recommended_action='propose_note')
    check('proposals: every proposal destination resolves to a template field, a record-level list of the target tier file or an explicit "(no template field)" label; no conflict entry is proposed into open_questions (regression cases)',
          not any(p_dest_bad(r) for r in fld) and not p_dest_bad(_d) and p_dest_bad(dict(_d, recommended_action='propose_record_conflict'))
          and p_dest_bad(dict(_d, field_path='kv41', current_status='no such field in the template')) and not p_dest_bad(dict(_d, field_path='(no template field) density', current_status='no such field in the template')),
          f"{sum(1 for r in fld if r['current_status'].startswith('top-level list'))} rows to record-level lists; invalid: {[(r['product_id'], r['tier'], r['field_path'], r['recommended_action']) for r in fld if p_dest_bad(r)][:5]}")
    # Structural association checks. They test that each proposal carries its explicit product, source, page and
    # route/condition association. They do NOT verify that a value is scientifically right: that is the manual
    # verification recorded per row in new_source_verification / old_source_review.
    cc = [r for r in prop if r['field_path'].startswith('required_co_components')]
    check('structure: every proposed co-component row is tied to an explicit route or recipe (non-empty conditions) or is a name-only / historical note',
          all(r['conditions'].strip() or r['recommended_action'] in ('propose_historical_note', 'propose_note') for r in cc), f'{len(cc)} rows')
    check('structure: co-component doses from recipes are proposed only as route-bound entries',
          all(r['recommended_action'] == 'propose_add_route_bound' for r in cc if 'recipe' in r['value_form'].lower() or 'formulation' in r['value_form'].lower()))
    pf = [r for r in prop if r['field_path'].startswith('published_formulations')]
    check('structure: every proposed formulation row names a formulation identity (oil code or column) and a percentage basis',
          all(re.search(r'LB[BR]|OS\d|IME\d|col', r['new_source_printed'], re.I) and r['percentage_basis'].strip() for r in pf), f'{len(pf)} rows')
    check('structure: specification limits, typicals and batch results are labelled in value_form for every numeric tier-2 proposal',
          all(re.search(r'typical|specification|batch|single value|target|minimum', r['value_form'], re.I) or r['value_form'].startswith(SDS_UNSPEC) for r in prop
              if r['tier'] == '2' and re.match(r'tbn|kv\d|density|flash|pour|elements\.|sulfated', r['field_path'])))
    # Twelfth pass: 'SDS reported value; statistical basis unspecified' is a legitimate class, but such a value may
    # not be promoted: no 'typical' / 'specification' qualifier and no action that adds or selects it as a value.
    PROMOTING = ('propose_add', 'propose_add_route_bound', 'propose_update_with_history', 'propose_selection_review', 'propose_selection_review_and_record_conflict', 'capture_from_old_source')
    def sds_ok(r):
        if not r['value_form'].startswith(SDS_UNSPEC):
            return True
        return r['recommended_action'] not in PROMOTING and not re.search(r'(?i)typical|specification', r.get('qualifier', '') or '')
    check('structure: SDS values with unspecified statistical basis are never promoted to a manufacturer typical or specification',
          all(sds_ok(r) for r in prop)
          and not sds_ok(dict(value_form=SDS_UNSPEC + ' (x)', recommended_action='propose_add', qualifier='SDS reported value'))
          and not sds_ok(dict(value_form=SDS_UNSPEC + ' (x)', recommended_action='propose_record_conflict', qualifier='typical (SDS)'))
          and sds_ok(dict(value_form=SDS_UNSPEC + ' (x)', recommended_action='propose_record_conflict', qualifier='SDS reported value')),
          f"{sum(1 for r in prop if r['value_form'].startswith(SDS_UNSPEC))} SDS-reported rows")
    # Seventh pass: note-only actions (they set no value) are also allowed for batch evidence; every action that can
    # set or change a selected value (update, selection review, route-bound add, ...) is still refused.
    BATCH_OK = ('propose_alternate_entry', 'propose_add', 'propose_open_question_update', 'propose_note', 'propose_historical_note')

    def p_batch(r):
        return 'batch' in r['value_form'].lower() and r['recommended_action'] not in BATCH_OK
    check('structure: no certificate limit, target or batch result is proposed as the preferred general value (alternate entry, first value or note only)',
          not [r for r in prop if p_batch(r)])
    _bb = dict(value_form='batch measurement (single third-party certificate)', recommended_action='propose_update_with_history')
    check('regression: batch evidence proposed through update / selection review / route-bound add is caught; an open-question note is not',
          p_batch(_bb) and p_batch(dict(_bb, recommended_action='propose_selection_review')) and p_batch(dict(_bb, recommended_action='propose_add_route_bound'))
          and not p_batch(dict(_bb, recommended_action='propose_open_question_update')))
    five = ('document_relationship', 'new_source_verification', 'old_source_review', 'current_json_comparison', 'action_readiness')
    check('status: the five statuses are present and filled on every field row', all(all(r.get(k) for k in five) for r in fld))
    check('status: no proposal is ready while its relationship is unresolved or a visual check is outstanding',
          not [r for r in prop if r['action_readiness'].startswith('ready') and (r['document_relationship'] != 'completed' or 'outstanding' in r['new_source_verification'])])
    check('status: no proposal is ready on an automated old-source search alone', not [r for r in prop if r['action_readiness'].startswith('ready') and not r['old_source_review'].startswith('re-read manually')])
    check('status: every ready proposal has a completed relationship, a compared current JSON and no overlap flag',
          not [r for r in prop if r['action_readiness'].startswith('ready') and (r['document_relationship'] != 'completed' or r['current_json_comparison'].startswith('not compared')
                                                                                 or ('ALREADY PRESENT [' in r['current_json_comparison'] and 'ALREADY PRESENT none' not in r['current_json_comparison']))])
    check('status: list-type proposals show the actual current entries, not a count', not [r for r in fld if re.fullmatch(r'list of \d+|object', r['current_value'])])
    d3453 = [r for r in prop if r['product_id'] == 'INFINEUM_D3453']
    # Original rule (checkpoint 2): the D3453 formulation must stay provisional while its three-way comparison is
    # incomplete. Since the fourth pass the old sheet DL2-10220.pdf has been read (as a page image), so the rule is
    # enforced as a condition, and the original incomplete state is kept as a regression case.
    def d3453_ok(r):
        complete = r['old_source_review'].startswith('re-read manually') and not r['current_json_comparison'].startswith('not compared') and r['document_relationship'] == 'completed'
        return r['action_readiness'].startswith('PROVISIONAL') or complete
    check('case: the Infineum D3453 formulation proposal is provisional unless the old source was read, the JSON compared and the relationship completed',
          d3453 and all(d3453_ok(r) for r in d3453)
          and not d3453_ok(dict(d3453[0], action_readiness='ready for reviewer decision', old_source_review='not available locally: ...'))
          and not d3453_ok(dict(d3453[0], action_readiness='ready for reviewer decision', old_source_review='NOT REVIEWED')))
    kv = [r for r in fld if r['product_id'] == 'AFTON_HITEC_12204L' and r['field_path'] == 'kv40']
    check('case: HiTEC 12204L KV40 keeps the printed 42.38 cm2/s and is not proposed as cSt', len(kv) == 1 and 'cm2/s' in kv[0]['unit'] and '42.38 cm2/s' in kv[0]['new_source_printed']
          and 'must NOT be entered as cSt' in kv[0]['reason'])
    tb = [r for r in fld if r['product_id'] == 'LUBRIZOL_16008' and r['field_path'] == 'tbn' and r['new_source_file'] == 'DL2-11514.pdf']
    check('case: the HiTEC 12210M formulation that adds to 100.1 (DL2-12485.pdf p.18) is flagged and not normalised',
          any('100.1' in r['reason'] and 'total_check_passed false' in r['reason'] for r in fld if r['product_id'] == 'AFTON_HITEC_12210M' and r['field_path'] == 'published_formulations'))
    ca = [r for r in fld if r['product_id'] == 'LUBRIZOL_16008' and r['field_path'] == 'elements.Ca']
    check('case: Lubrizol 16008 old "> 182" and new typical 182 are kept distinct; properties are not described as all unchanged',
          len(tb) == 1 and 'greater than 182' in tb[0]['old_source_statement'] and 'Typical 182' in tb[0]['new_source_printed'] and 'not the same information' in tb[0]['reason']
          and len(ca) == 1 and 'NOT all unchanged' in ca[0]['reason'])
    # ---- regression self-tests for the four checks that failed in the third pass and were then refined ----
    # Each refined predicate is run against a synthetic row reproducing the ORIGINAL failure case (must still be
    # caught) and against the legitimate case that had triggered the false alarm (must pass).
    def p_5748a(r):      # violation: a value/entry proposed for HiTEC 5748 from text that names HiTEC 5748A
        return r['product_id'] == 'AFTON_HITEC_5748' and '5748A' in r['new_source_printed'] and r['recommended_action'].startswith(('propose_add', 'propose_alternate'))

    def p_form(r):       # violation: numeric tier-2 proposal without a typical/specification/batch label
        return (r['tier'] == '2' and re.match(r'tbn|kv\d|density|flash|pour|elements\.|sulfated', r['field_path'])
                and not re.search(r'typical|specification|batch|single value|target|minimum', r['value_form'], re.I)
                # thirteenth pass: aligned with the value-form check above (the approved SDS class is a label;
                # its non-promotion is enforced separately by sds_ok)
                and not r['value_form'].startswith(SDS_UNSPEC))

    def p_ready(r):      # violation: ready although the old source was not read by the reviewer
        return r['action_readiness'].startswith('ready') and not r['old_source_review'].startswith('re-read manually')

    base = dict(product_id='AFTON_HITEC_5748', new_source_printed='HiTEC 5748A (ND-OCP) 3.5', recommended_action='propose_add', tier='2', field_path='tbn', value_form='text',
                action_readiness='ready for reviewer decision', old_source_review='automated text search only (1 of 1 cited sources searchable)')
    check('regression: a value proposed for HiTEC 5748 from 5748A text is still caught; a scoped note naming both grades is not',
          p_5748a(base) and p_5748a(dict(base, recommended_action='propose_alternate_entry')) and not p_5748a(dict(base, recommended_action='propose_note')))
    check('regression: an unlabelled numeric tier-2 proposal is still caught; a text field of a tier-2 component file is not',
          p_form(base) and p_form(dict(base, field_path='elements.Ca', value_form='')) and not p_form(dict(base, field_path='polymer_chemistry')) and not p_form(dict(base, value_form='typical'))
          and not p_form(dict(base, field_path='flash_point', value_form=SDS_UNSPEC + ' (x)'))
          and p_form(dict(base, field_path='flash_point', value_form='SDS value (x)')))
    check('regression: ready on an automated or unavailable old source is still caught, also when a manual note merely mentions an automated search',
          p_ready(base) and p_ready(dict(base, old_source_review='not available locally: ...'))
          # fourth-pass build defect: a 'not available locally' statement that mentions another source being
          # 're-read manually' was counted as a reading by 02_build.py; it must stay caught here
          and p_ready(dict(base, old_source_review='not available locally: primary PDS has no local copy. The second cited source was re-read manually'))
          and not p_ready(dict(base, old_source_review='re-read manually: p.2 text. NOT re-read: the earlier edition (automated search only)')))
    check('regression: the live tables contain none of these three violations', not [r for r in prop if p_5748a(r) or p_form(r) or p_ready(r)])
    t16 = [r for r in fld if r['product_id'] == 'LUBRIZOL_16008' and r['field_path'] == 'tbn']
    check('regression: every Lubrizol 16008 TBN row (now more than one source) keeps the 2013 lower bound "> 182" / "greater than 182" visible in its old-source statement',
          len(t16) >= 2 and all('greater than 182' in r['old_source_statement'] or "'> 182'" in r['old_source_statement'] for r in t16)
          and any('188' in r['new_source_printed'] and r['recommended_action'] == 'propose_record_conflict' for r in t16))
    refs = rd(os.path.join(T, 'old_source_references.csv'))
    check('old sources: every reference has a SHA-256 or an explicit statement that it is unavailable', all(len(r['sha256']) == 64 or 'unavailable' in r['availability'] or 'no hash' in r['availability'] for r in refs), f'{len(refs)} references')
    check('old sources: no placeholder hash text remains in the field table', not [r for r in fld if 'external or not an archive member' in r.get('old_source_references', '')])
    check('old sources: rows whose cited source is not available locally say so', all('NOT' in r['old_source_review'] or 'not available' in r['old_source_review'] or 're-read' in r['old_source_review']
                                                                                    for r in fld if 'NO local evidence copy' in r['old_source_references']))

    # preservation
    check('preservation: existing archive bytes unchanged', sha_file(os.path.join(ROOT, 'Manual + Data to share.zip')) == EXPECT['old_archive'])
    check('preservation: new archive bytes unchanged', sha_file(NEW_ZIP) == EXPECT['new_archive'])
    snap = os.path.join(ROOT, 'review_snapshots', 'review_snapshot_2026-11-12')
    check('preservation: frozen snapshot manifest unchanged', sha_file(os.path.join(snap, 'MANIFEST.sha256')) == EXPECT['snapshot_manifest'])
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'data_policy', 'make_review_snapshot.py'), '--name', 'review_snapshot_2026-11-12', '--verify'], cwd=ROOT, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    check('preservation: frozen snapshot verifies against its manifest', r.returncode == 0, (r.stdout.strip().splitlines() or [''])[-1][:120])
    # Fifteenth pass: the authorized Part A publication (PR #7) changed 21 snapshot files (handoff docs, check-result text,
    # regenerated workbook). Each is recorded with its reason and post-publication hash in preservation_baselines.json;
    # every other snapshot file (incl. all product JSON, reports, tools and evidence) must still equal the snapshot.
    PB = json.load(open(os.path.join(HERE, 'preservation_baselines.json'), encoding='utf-8'))
    allowed = {r['path']: r for r in PB['snapshot_files_changed_by_publication']}
    same = diff = missing = pub_ok = 0
    changed = []
    with open(os.path.join(snap, 'MANIFEST.sha256'), encoding='utf-8') as fh:
        for line in fh:
            h, rel = line.rstrip('\n').split('  ', 1)
            p = os.path.join(ROOT, rel)
            if not os.path.exists(p):
                missing += 1
            elif sha_file(p) == h:
                same += 1
            elif rel in allowed and allowed[rel]['snapshot_sha256'] == h and sha_file(p) == allowed[rel]['post_publication_sha256']:
                pub_ok += 1
            else:
                diff += 1; changed.append(rel)
    check('preservation: snapshot files are byte-identical to the snapshot, except the 21 recorded publication changes, which equal their recorded post-publication bytes; no product JSON, report, tool or evidence file is among the exceptions',
          diff == 0 and missing == 0 and pub_ok == len(allowed) == 21 and not any(k.startswith(('Products_json', 'reports', 'tools', 'reconciliation')) for k in allowed),
          f'{same} identical, {pub_ok} recorded publication changes, {diff} unexpected, {missing} missing' + (': ' + '; '.join(changed[:5]) if changed else ''))
    if os.path.exists(INV_ZIP):
        check('preservation: earlier inventory review ZIP not overwritten', sha_file(INV_ZIP) == EXPECT['inventory_zip'])
        with zipfile.ZipFile(INV_ZIP) as z:
            bad = []
            for i in z.infolist():
                rel = i.filename.split('/', 1)[-1] if i.filename.startswith('incoming_dataset_review') else i.filename
                p = os.path.join(INV, rel)
                if os.path.isfile(p) and hashlib.sha256(z.read(i.filename)).hexdigest() != sha_file(p):
                    bad.append(rel)
            check('preservation: original automated inventory reports equal the copies in the earlier review ZIP', not bad, '; '.join(bad[:5]))
    g = subprocess.run('git status --short', cwd=ROOT, capture_output=True, shell=True).stdout
    keep = b''.join(l + b'\n' for l in g.splitlines() if b'incoming_dataset_review_2026-11-12' not in l and b'existing_product_comparison_2026-11-12' not in l)
    # Fifteenth pass: old expectations (HEAD 43e7f8b, status hash 2de292fe3eabccb9) are kept in preservation_baselines.json['old'].
    exp_status = PB['new']['git_status_outside_review_folders']
    check('preservation: Git working state outside the two review folders is exactly the recorded local-only state (review_snapshots/ untracked)',
          [l.decode('utf-8', 'replace') for l in keep.splitlines()] == exp_status, keep.decode('utf-8', 'replace').strip()[:200])
    check('preservation: nothing staged', not subprocess.run('git diff --cached --name-only', cwd=ROOT, capture_output=True, shell=True).stdout.strip())
    pub = PB['new']['published_main']
    anc = subprocess.run(f'git merge-base --is-ancestor {pub} HEAD', cwd=ROOT, shell=True).returncode == 0
    touched = subprocess.run(f'git diff --name-only {pub} HEAD', cwd=ROOT, capture_output=True, shell=True, text=True).stdout.split()
    outside = [t for t in touched if not t.startswith(('existing_product_comparison_2026-11-12/', 'incoming_dataset_review_2026-11-12/'))]
    check('preservation: HEAD contains the published Part A main (8d4626b) and the branch changes nothing outside the two review folders', anc and not outside,
          f'ancestor={anc}; outside={outside[:5]}')
    check('preservation: association mining folder untouched', not subprocess.run('git status --short analysis/association_mining', cwd=ROOT, capture_output=True, shell=True).stdout.strip())

    # ---- thirteenth pass: never-cited reconciliation (stable product_id + sha256 keys) ----
    rec_p = os.path.join(BASE, 'tables', 'never_cited_reconciliation.csv')
    if os.path.exists(rec_p):
        rec = list(csv.DictReader(open(rec_p, encoding='utf-8')))

        def rec_ok(r):
            # 'reviewed' requires coverage assessed by reading; a reclassification alone never counts as coverage
            if r['status'] == 'reviewed' or r['status'] == 'reclassified, coverage assessed':
                return r['coverage_now'].startswith('assessed by reading')
            if r['status'] == 'reclassified, coverage NOT assessed' or r['status'] == 'outstanding':
                return not r['coverage_now'].startswith('assessed by reading')
            return False
        _r = dict(status='reviewed', coverage_now='not assessed')
        check('never-cited reconciliation: 33 baseline keys, every status consistent with its coverage; reclassification alone is not counted as reviewed (regression cases)',
              len(rec) == 33 and len({(r['product_id'], r['sha256']) for r in rec}) == 33 and all(rec_ok(r) for r in rec)
              and not rec_ok(_r) and not rec_ok(dict(_r, status='reclassified, coverage NOT assessed', coverage_now='assessed by reading x'))
              and rec_ok(dict(_r, status='reclassified, coverage NOT assessed')),
              str(__import__('collections').Counter(r['status'] for r in rec)))
    else:
        check('never-cited reconciliation table present', False, 'run 07_never_cited_reconciliation.py')

    # ---- sixteenth pass: a text comparison is not a reading ----
    # 08_progress_measures.py counts 'all N pages' and 'pp.1-N' as full reads. A statement that only says the pages were
    # COMPARED (machine text comparison, word diff, identical text) must not use those phrases for the comparison.
    def p_cmp_as_read(s):
        return bool(re.search(r'all \d+ pages (were )?(compared|diffed|matched)|pp\.1-\d+ (were )?(compared|diffed|matched)', s, re.I))
    check('reading scope: no reading statement presents a page-by-page text comparison as "all N pages" / "pp.1-N" (counted as a full read by the measures; regression cases)',
          not [r for r in led if p_cmp_as_read(r['field_verification_status'])]
          and p_cmp_as_read('all 3 pages compared word by word with the cited X') and p_cmp_as_read('pp.1-23 compared')
          and not p_cmp_as_read('all 10 pages read (text layer); p.5 compared word by word') and not p_cmp_as_read('text of each of its 3 pages compared by machine'),
          str([r['file'] for r in led if p_cmp_as_read(r['field_verification_status'])][:5]))

    fails = [x for x in results if not x[1]]
    print(f'\n{len(results) - len(fails)} of {len(results)} checks passed' + ('' if not fails else '; FAILED: ' + '; '.join(x[0] for x in fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
