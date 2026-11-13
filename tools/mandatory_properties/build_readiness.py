"""Separate attributes of every requirement outcome, and the route-, basis- and applicability-level detail of the four
policies approved on 2026-11-11 (read-only on the data; run after co_component_evidence_scan.py, build_eligibility.py
and source_review_status.py).

Nothing here changes or redefines tier1_complete or formulation_eligible (product_eligibility.csv). The outputs keep
five things apart that one eligibility verdict cannot show:

  evidence_documentation   what the RECORD holds:  documented | documented_incomplete (value present, but its unit,
                           condition, basis or source is not) | not_recorded | invalid | calculated_not_reproduced |
                           requirement_unknown | recorded_route_not_assessed | applicability_unresolved |
                           not_applicable_approved_rule.  "not_recorded" describes the record only. Whether a source was
                           inspected, and what was found, is verification_status (and source_inspection for
                           co-components): not recorded, not found in the inspected text, source unavailable and
                           confirmed by source review are four different things.
  value_selection          selected | pending | none.  Taken from the source-selection ledger, independently of the
                           outcome category: a value can have incomplete metadata AND a pending selection. A pending
                           selection blocks every use that needs a selected value.
  value_form               point | closed_range | lower_bound | upper_bound | specification_value_no_direction | text |
                           structured | none.  A range or bound is never replaced by a point.
  percentage_basis         mass | volume | unspecified (dose and treat-rate requirements only)
  verification_status      the review state of the source (source_review_status.csv) where the property is in the
                           coverage ledger; otherwise not_individually_reviewed

Scoped indicators instead of a general "ready" label: selected_point_value says only that this one requirement has a
selected point value with its unit, condition and source. Readiness for a calculation is assessed only against a
NAMED, REGISTERED calculation; unregistered methods are listed as not assessed. No conversion and no range-aware
calculation is registered.

These files describe the mandatory Tier 1 requirements (and the VM/PPD subtype blocks) only. They do not define the
feature inventory of the association-mining dataset, which may also use suitable Tier 2 and Tier 3 properties.

Outputs (reports/mandatory_properties/):
  property_attributes.csv          one row per product x requirement
  product_input_completeness.csv   one row per product: counts of the attributes over its mandatory requirements
  co_component_routes.csv          recorded co-component requirements, reviewed routes, reviewed statements, and
                                   packages with no recorded requirement, each with what was inspected
  percentage_basis.csv             one row per reported value in the dose and treat-rate FIELDS, with its basis class
  volume_dose_evidence.csv         volume-basis dose evidence kept in external_fill_notes (evidence only; never a wt.% value)
  applicability_review.csv         every Not Required / Not Applicable label and every unresolved-applicability outcome
  calculation_readiness.csv        named calculations: registered (with what they assessed) or not registered
  readiness_summary.md             counts, each with its scope

Usage: python tools/mandatory_properties/build_readiness.py [--check]
Exit codes: 0 ok; 1 --check found a difference; 2 a product could not be classified; 3 stale or missing ledger.
"""
import argparse, collections, csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import requirements as R  # noqa: E402
import build_eligibility as BE  # noqa: E402

READINESS_VERSION = 'readiness-2026-11-12.1'
OUT = BE.OUT
REVIEW_STATUS = os.path.join(BE.ROOT, 'reports', 'data_policy', 'source_review_status.csv')
CO_SCAN = os.path.join(OUT, 'co_component_evidence.csv')

EVIDENCE = {R.MET: 'documented', R.BOUND: 'documented', R.SEL: 'documented', R.NOT_APPLICABLE: 'not_applicable_approved_rule',
            R.META: 'documented_incomplete', R.INVALID: 'invalid', R.CALC: 'calculated_not_reproduced',
            R.APPL: 'applicability_unresolved', R.UNKNOWN: 'requirement_unknown', R.ROUTE: 'recorded_route_not_assessed',
            R.ABSENT: 'not_recorded'}
FORM = {'point': 'point', 'range': 'closed_range', 'lower_bound': 'lower_bound', 'upper_bound': 'upper_bound',
        'spec_value': 'specification_value_no_direction', 'text': 'text'}
NUMERIC_FORMS = ('point', 'closed_range', 'lower_bound', 'upper_bound', 'specification_value_no_direction')
SOURCE_INSPECTION = ('confirmed_by_source_review', 'historical_source_review_not_current', 'recorded_from_cited_page_not_re_reviewed',
                     'lead_in_inspected_text_not_reviewed', 'not_found_in_inspected_text', 'source_unavailable', 'not_inspected')
# what a source review of a route says about its CURRENT applicability: only 'current' evidence is confirmed
INSPECTION_BY_VALIDITY = {'current': 'confirmed_by_source_review', 'stale_requires_re_review': 'historical_source_review_not_current',
                          'invalid': 'historical_source_review_not_current'}
VOLUME_WORDING = re.compile(r'vol\.?\s*%|%\s*vol|\(vol\.?\)|by\s+volume|v/v', re.I)

DOSE_REQUIREMENT = {'treat_range_by_sae_grade': 'vm.treat_range_by_sae_grade', 'tested_dose_range_wt_pct': 'ppd.tested_dose_range_wt_pct'}

ATTR_COLUMNS = ['product_id', 'material_class', 'requirement', 'blocking', 'outcome_category', 'evidence_documentation', 'value_selection',
                'value_form', 'percentage_basis', 'verification_status', 'open_conflict', 'selected_point_value', 'calculated', 'reason']
PRODUCT_COLUMNS = ['product_id', 'material_class', 'mandatory_requirements', 'evidence_documented', 'evidence_documented_incomplete',
                   'evidence_not_recorded', 'requirement_unknown', 'recorded_route_not_assessed', 'applicability_unresolved',
                   'invalid_or_not_reproduced', 'selections_pending', 'numeric_selected_point_values', 'numeric_ranges_or_bounds',
                   'percentage_basis_unspecified', 'percentage_basis_volume', 'all_mandatory_evidence_documented', 'tier1_complete',
                   'formulation_eligible', 'requirements_version', 'readiness_version', 'source_snapshot_sha256']
ROUTE_COLUMNS = ['product_id', 'row_kind', 'entry_index', 'role_and_condition_as_recorded', 'name', 'dose_value', 'dose_min', 'dose_max',
                 'dose_unit_as_recorded', 'percentage_basis', 'basis_established_by', 'source_file', 'page', 'requirement_state', 'route_id',
                 'route_state', 'review_validity', 'reviewed_on', 'group', 'group_combination', 'group_state', 'requirement_list_confirmed',
                 'record_state', 'source_inspection', 'inspected', 'qualification', 'limitations', 'detail', 'product_level_outcome']
BASIS_COLUMNS = ['product_id', 'material_class', 'field', 'context_as_recorded', 'value', 'min', 'max', 'unit_as_recorded', 'basis_class',
                 'basis_established_by', 'basis_is_mass', 'value_outcome_category', 'value_outcome_reason', 'source_file', 'page']
VOLUME_COLUMNS = ['product_id', 'material_class', 'record_file', 'field_as_recorded', 'grade_or_context', 'record_status', 'source', 'evidence_as_recorded', 'use']
APPL_COLUMNS = ['product_id', 'material_class', 'row_kind', 'field_or_requirement', 'tier', 'blocking', 'label_or_category', 'approved_rule',
                'result', 'detail']
CALC_COLUMNS = ['calculation', 'status', 'required_inputs', 'authority', 'values_assessed', 'accepted', 'not_accepted', 'note']


def attributes(category, representation, selection_pending=False):
    """(evidence_documentation, value_selection, value_form, selected_point_value) for one outcome. The selection status
    comes from the ledger flag, not from the category, so it survives any other defect of the value."""
    form = FORM.get(representation or '', 'structured' if category == R.MET else 'none')
    if category in (R.ABSENT, R.UNKNOWN, R.APPL, R.NOT_APPLICABLE, R.ROUTE):
        form = 'none'
    pending = bool(selection_pending) or category == R.SEL
    sel = 'pending' if pending else 'selected' if category in (R.MET, R.BOUND, R.META, R.INVALID, R.CALC) else 'none'
    point = ('yes' if category == R.MET and form == 'point' and not pending else 'no') if form in NUMERIC_FORMS else 'not_numeric'
    return EVIDENCE[category], sel, form, point


def open_conflict_properties(p):
    out = set()
    for d in p['files'].values():
        for c in d.get('conflicts') or []:
            if isinstance(c, dict) and c.get('resolved') is not True:
                out.add(str(c.get('field') or c.get('property') or '').replace('[', '.').split('.')[-1].strip())
    return out


def _read(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def dose_items(p):
    """(field, context as recorded, value object) for every value in a dose / treat-rate FIELD of a product."""
    for key, d in p['files'].items():
        f = d.get('fields', {})
        for i, e in enumerate(f.get('treat_rate_matrix') or []):
            e = e if isinstance(e, dict) else {}
            yield f'treat_rate_matrix[{i}]', 'treat_rate_matrix', f"claim: {e.get('claim')}; SAE grade: {e.get('sae_grade')}", e.get('treat_rate_wt_pct')
        for i, e in enumerate(f.get('required_co_components') or []):
            if isinstance(e, dict):
                yield f'required_co_components[{i}]', 'required_co_components', f"role: {e.get('role')}; name: {e.get('name')}", e.get('dose_wt_pct')
        if p['class'] == 'additive_component' and key == 'general' and isinstance(f.get('treat_rate'), dict):
            yield 'treat_rate', 'treat_rate', '', f['treat_rate']
        for i, e in enumerate(f.get('treat_range_by_sae_grade') or []):
            e = e if isinstance(e, dict) else {}
            yield f'vm.treat_range_by_sae_grade[{i}]', 'treat_range_by_sae_grade', f"SAE grade: {e.get('sae_grade')}", e.get('treat_range_wt_pct')
        if key == 'ppd' and isinstance(f.get('tested_dose_range_wt_pct'), dict):
            yield 'ppd.tested_dose_range_wt_pct', 'tested_dose_range_wt_pct', '', f['tested_dose_range_wt_pct']


def volume_evidence(pid, p):
    """Volume-basis dose evidence kept in external_fill_notes, exactly as recorded. It is evidence only: the wt.% fields
    stay Missing and nothing is converted."""
    for key, d in p['files'].items():
        for n in d.get('external_fill_notes') or []:
            if not isinstance(n, dict):
                continue
            text = ' '.join(str(n.get(k) or '') for k in ('notes', 'value', 'unit'))
            if not VOLUME_WORDING.search(text):
                continue
            prop = str(n.get('property') or '')
            ctx = re.search(r'\[([^\]]+)\]', prop)
            yield dict(product_id=pid, material_class=p['class'], record_file=str(key), field_as_recorded=prop,
                       grade_or_context=ctx.group(1) if ctx else '', record_status=n.get('status'), source=n.get('source'),
                       evidence_as_recorded=n.get('notes'),
                       use='evidence only: volume basis; not a wt.% value, not converted, not used in any calculation')


def src(vo):
    s = (vo or {}).get('source') or {}
    return s.get('file') or '', '' if s.get('page') is None else s.get('page')


def unobtained_sources():
    """External sources that the external review could not obtain (external_review_decisions.json)."""
    p = os.path.join(BE.ROOT, 'tools', 'data_policy', 'external_review_decisions.json')
    with open(p, encoding='utf-8') as fh:
        ev = json.load(fh)['evidence']
    return sorted({e['registry_url'] for e in ev.values() if e.get('authenticity') == 'not_obtained' and e.get('registry_url')})


def route_rows(pid, ctx, rts, entries, statements, lvl, blank):
    """Rows of co_component_routes.csv for one package: one row per (recorded requirement, route) membership - a
    requirement that belongs to several routes gets one row for each, with that route's own assessment - one row per
    requirement without any route, one per reviewed route, one per requirement the source states that the record does
    not hold, and one per reviewed statement. Stale or invalid route evidence is reported as a historical review,
    never as confirmed for the current record."""
    out = []

    def entry_row(e, **kw):
        dv = e['dose']
        ok = dv.get('status') in R.OK_STATUS
        cls, how = ctx.basis_of('required_co_components', dv) if ok else ('', '')
        f, pg = src(dv)
        return dict(blank, product_id=pid, row_kind='recorded_requirement', entry_index=e['index'], role_and_condition_as_recorded=e['role'],
                    name=e['name'], dose_value=dv.get('value'), dose_min=dv.get('min'), dose_max=dv.get('max'),
                    dose_unit_as_recorded=dv.get('unit') if ok else '', percentage_basis=cls, basis_established_by=how, source_file=f, page=pg,
                    requirement_state=e['state'], record_state='recorded', product_level_outcome=lvl, **kw)
    seen = set()
    for r in rts:
        x = r['route']
        common = dict(route_id=x.get('route_id'), route_state=r['state'], review_validity=r['validity'], reviewed_on=x.get('reviewed_on') or '',
                      requirement_list_confirmed=x.get('requirement_list_confirmed'), source_inspection=INSPECTION_BY_VALIDITY[r['validity']])
        if r['validity'] == 'current':
            for g in r['groups']:
                for e in g['members']:
                    seen.add(e['index'])
                    out.append(entry_row(e, group=g['group'], group_combination=g['combination'], group_state=g['state'],
                                         detail=e['outcome'].reason, **common))
        else:   # the evidence names these entries, but its association is not verified for the record as it is now
            for e in r['members']:
                out.append(entry_row(e, detail='historical association only: ' + r['why'], **common))
        for u in x.get('unrecorded_requirements') or []:
            out.append(dict(blank, product_id=pid, row_kind='requirement_stated_by_source_not_in_record', name=u.get('component'),
                            source_file=x.get('source_file'), page=x.get('page'), requirement_state='required_dose_not_recorded',
                            record_state='not_recorded', detail=f"{u.get('quote')} | dose: {u.get('dose')} | proposed: {u.get('proposed_correction')}",
                            product_level_outcome=lvl, **common))
        out.append(dict(blank, product_id=pid, row_kind='reviewed_route', role_and_condition_as_recorded=x.get('conditions'), name=x.get('label'),
                        source_file=x.get('source_file'), page=x.get('page'), record_state='recorded',
                        limitations=' | '.join(x.get('limitations') or []),
                        detail=f"{r['why']} || association: {x.get('association_basis')} || read: {x.get('read_how')} || quote: {x.get('quote')}",
                        product_level_outcome=lvl, **common))
    for e in entries:
        if e['index'] not in seen:
            out.append(entry_row(e, route_state='route_association_not_established', source_inspection='recorded_from_cited_page_not_re_reviewed',
                                 detail=e['outcome'].reason))
    for st in [x for x in statements if x.get('product') == pid]:
        ok, why = R.explicit_none_required(st, pid)
        rv = st.get('review') if isinstance(st.get('review'), dict) else {}
        out.append(dict(blank, product_id=pid, row_kind='reviewed_statement', role_and_condition_as_recorded=rv.get('conditions_verbatim') or '',
                        name=json.dumps(rv.get('scope'), ensure_ascii=False) if rv else st.get('scope'), source_file=st.get('source_file'),
                        page=st.get('page'), requirement_state='none_required_explicit' if ok else 'statement_not_sufficient: ' + why,
                        reviewed_on=rv.get('reviewed_on') or '', record_state='recorded', source_inspection='confirmed_by_source_review',
                        qualification=rv.get('qualification_verbatim', ''), detail=st.get('quote'), product_level_outcome=lvl))
    return out


def scan_inspection(scan_row):
    """(source_inspection, what was inspected) for a package without a recorded requirement, from the scan."""
    if not scan_row:
        return 'not_inspected', 'no scan result'
    insp = (f"text layer of {scan_row.get('documents_inspected') or 'no document'} ({scan_row.get('pages_with_text', '0')} page(s) with text); "
            f"not inspected: {scan_row.get('not_inspected') or 'nothing'}")
    f = scan_row.get('finding', '')
    if f.startswith('source text unavailable'):
        # nothing was inspected: 'source_unavailable' only where the external review could not obtain the source at all;
        # an archive file without a text layer exists and is simply not inspected by a text search
        gone = [u for u in unobtained_sources() if u in (scan_row.get('not_inspected') or '')]
        return ('source_unavailable', insp + '; could not be obtained: ' + '; '.join(gone)) if gone else ('not_inspected', insp)
    if f.startswith('not found'):
        return 'not_found_in_inspected_text', insp
    return 'lead_in_inspected_text_not_reviewed', insp + '; lead: ' + (scan_row.get('evidence') or '')[:300]


def build():
    rows, outcomes, problems, snapshot = BE.build()
    prods, _ = BE.load_products()
    review = {(r['product'], r['property']): r['review_state'] for r in _read(REVIEW_STATUS)}
    scan = {r['product']: r for r in _read(CO_SCAN)}
    with open(BE.BASIS, encoding='utf-8') as fh:
        basis_ev = json.load(fh)['evidence']
    statements, route_ev = BE.load_statements(), BE.load_routes()

    attrs, per = [], collections.defaultdict(list)
    conflicts = {pid: open_conflict_properties(p) for pid, p in prods.items()}
    for o in outcomes:
        pid = o['product_id']
        ev, sel, form, point = attributes(o['category'], o['representation'], o['selection_pending'])
        prop = o['requirement'].split('[')[0].split('.')[-1]
        a = dict(product_id=pid, material_class=o['material_class'], requirement=o['requirement'], blocking=o['blocking'],
                 outcome_category=o['category'], evidence_documentation=ev, value_selection=sel, value_form=form,
                 percentage_basis=o['percentage_basis'], verification_status=review.get((pid, prop), 'not_individually_reviewed'),
                 open_conflict=prop in conflicts[pid], selected_point_value=point, calculated=o['calculated'], reason=o['reason'])
        attrs.append(a)
        if o['blocking']:
            per[pid].append(a)

    products = []
    for r in rows:
        a = per[r['product_id']]
        c = collections.Counter(x['evidence_documentation'] for x in a)
        products.append(dict(
            product_id=r['product_id'], material_class=r['material_class'], mandatory_requirements=len(a),
            evidence_documented=c['documented'] + c['not_applicable_approved_rule'], evidence_documented_incomplete=c['documented_incomplete'],
            evidence_not_recorded=c['not_recorded'], requirement_unknown=c['requirement_unknown'],
            recorded_route_not_assessed=c['recorded_route_not_assessed'], applicability_unresolved=c['applicability_unresolved'],
            invalid_or_not_reproduced=c['invalid'] + c['calculated_not_reproduced'],
            selections_pending=sum(x['value_selection'] == 'pending' for x in a),
            numeric_selected_point_values=sum(x['selected_point_value'] == 'yes' for x in a),
            numeric_ranges_or_bounds=sum(x['value_form'] in NUMERIC_FORMS[1:] for x in a),
            percentage_basis_unspecified=sum(x['percentage_basis'] == 'unspecified' for x in a),
            percentage_basis_volume=sum(x['percentage_basis'] == 'volume' for x in a),
            all_mandatory_evidence_documented=len(a) == c['documented'] + c['not_applicable_approved_rule'],
            tier1_complete=r['tier1_complete'], formulation_eligible=r['formulation_eligible'],
            requirements_version=R.REQUIREMENTS_VERSION, readiness_version=READINESS_VERSION, source_snapshot_sha256=snapshot))

    routes, basis_rows, volume_rows = [], [], []
    blank = dict(entry_index='', role_and_condition_as_recorded='', name='', dose_value='', dose_min='', dose_max='', dose_unit_as_recorded='',
                 percentage_basis='', basis_established_by='', source_file='', page='', requirement_state='', route_id='', route_state='',
                 review_validity='', reviewed_on='', group='', group_combination='', group_state='', requirement_list_confirmed='',
                 record_state='', source_inspection='', inspected='', qualification='', limitations='', detail='')
    for pid in sorted(prods):
        p = prods[pid]
        ctx = R.Context(basis_evidence=basis_ev, product=pid, material_class=p['class'], statements=statements, routes=route_ev)
        volume_rows += list(volume_evidence(pid, p))
        for field, path, context, vo in dose_items(p):
            if isinstance(vo, dict) and vo.get('status') in R.OK_STATUS:
                cls, how = ctx.basis_of(path, vo)
                o = R.check_value(vo, DOSE_REQUIREMENT.get(path, path), ctx, mass_basis=True, path=path)
                f, pg = src(vo)
                basis_rows.append(dict(product_id=pid, material_class=p['class'], field=field, context_as_recorded=context,
                                       value=vo.get('value'), min=vo.get('min'), max=vo.get('max'), unit_as_recorded=vo.get('unit'),
                                       basis_class=cls, basis_established_by=how, basis_is_mass=cls == 'mass',
                                       value_outcome_category=o.category, value_outcome_reason=o.reason, source_file=f, page=pg))
        if p['class'] != 'additive_package' or 1 not in p['files']:
            continue
        fields = p['files'][1].get('fields', {})
        level = R.co_component_outcome(fields, ctx)
        lvl = f'{level.category}: {level.reason}'
        rts, unassigned, entries = R.co_component_routes(fields, ctx)
        routes += route_rows(pid, ctx, rts, entries, statements, lvl, blank)
        own = [x for x in statements if x.get('product') == pid]
        if not entries and not own:
            how, insp = scan_inspection(scan.get(pid))
            routes.append(dict(blank, product_id=pid, row_kind='no_recorded_requirement', record_state='not_recorded', source_inspection=how,
                               inspected=insp, detail=level.reason, product_level_outcome=lvl))

    appl = []
    sys.path.insert(0, os.path.join(BE.ROOT, 'tools', 'data_policy'))
    import policy_lib
    for pid in sorted(prods):
        p = prods[pid]
        for key, d in p['files'].items():
            for path, n in policy_lib.value_objects(d.get('fields', {})):
                if n.get('status') in R.INAPPLICABLE_STATUS:
                    appl.append(dict(product_id=pid, material_class=p['class'], row_kind='label_in_record', field_or_requirement=path,
                                     tier=d.get('tier'), blocking='', label_or_category=n.get('status'), approved_rule='none',
                                     result='unresolved: no rule is approved for this product class, requirement and task',
                                     detail=str(n.get('notes') or n.get('calculation_note') or '')[:300]))
    for o in outcomes:
        if o['category'] in (R.APPL, R.NOT_APPLICABLE):
            appl.append(dict(product_id=o['product_id'], material_class=o['material_class'], row_kind='requirement_outcome',
                             field_or_requirement=o['requirement'], tier='', blocking=o['blocking'], label_or_category=o['category'],
                             approved_rule='none' if o['category'] == R.APPL else 'see detail',
                             result='unresolved' if o['category'] == R.APPL else 'not applicable under an approved rule', detail=o['reason']))

    def calc_counts(req):
        c = [o for o in outcomes if o['requirement'] == req and o['calculated']]
        return len(c), sum(o['category'] in R.SATISFIED for o in c), sum(o['category'] not in R.SATISFIED for o in c)
    calcs = []
    for name, req, inputs, auth in (
            ('delta_kv100_thickening', 'vm.thickening_response', 'KV100 at the dose and at 0 % in the named reference oil; dose; method; all printed on the cited page',
             'requirements.calc_delta_kv100; glossary: a response needs reference oil, dose and method'),
            ('shear_stability_index', 'vm.shear_stability', 'V0, Vs and the base-oil viscosity Vb; method; cycle count; printed on the cited page',
             'requirements.calc_shear_index: SSI = (V0 - Vs) / (V0 - Vb) x 100')):
        n, ok, bad = calc_counts(req)
        calcs.append(dict(calculation=name, status='registered: verifies a recorded Calculated value', required_inputs=inputs, authority=auth,
                          values_assessed=n, accepted=ok, not_accepted=bad,
                          note='A recorded calculated value is accepted only if the check reproduces it from inputs printed on the cited page.'))
    calcs.append(dict(calculation='viscosity_loss_percent', status='registered: verification check, not used by any requirement',
                      required_inputs='V0 and Vs printed on the cited page', authority='requirements.calc_viscosity_loss: (V0 - Vs) / V0 x 100',
                      values_assessed=0, accepted=0, not_accepted=0, note='A % viscosity loss is not an SSI and does not satisfy the SSI requirement.'))
    calcs.append(dict(calculation='volume_to_mass_percent', status='not registered: code preserved, unused',
                      required_inputs='not defined: the function takes numbers only and cannot establish the source, unit or applicability of the densities',
                      authority='requirements.volume_to_mass_percent (arithmetic only)', values_assessed='', accepted='', not_accepted='',
                      note=f'No conversion is performed. {len(volume_rows)} volume-basis evidence entries are listed in volume_dose_evidence.csv and fill no wt.% field.'))
    for name, where in (('viscosity_index_from_kv40_kv100', 'Minimum Property Set slide 2: "Viscosity index - dimensionless, from KV40 / KV100" (ASTM D2270)'),
                        ('finished_formula_mass_balance', 'Minimum Property Set slide 5: "Mass balance = 100.00 wt.%"'),
                        ('batch_mass_from_dose', 'Minimum Property Set slide 5: "Batch mass = dose / 100 x batch kg"'),
                        ('any range-aware calculation', 'policy 1: a range may be used only where the method supports it')):
        calcs.append(dict(calculation=name, status='not registered: not assessed', required_inputs='not defined in the project', authority=where,
                          values_assessed='', accepted='', not_accepted='',
                          note='No documented, reproducible implementation exists in the project, so input readiness for it is not assessed '
                               'and no product is called ready for it.'))
    return dict(rows=rows, outcomes=outcomes, problems=problems, snapshot=snapshot, attrs=attrs, products=products, routes=routes,
                basis=basis_rows, volume=volume_rows, appl=appl, calcs=calcs)


def render(b):
    c = BE._csv
    files = {'property_attributes.csv': c(b['attrs'], ATTR_COLUMNS), 'product_input_completeness.csv': c(b['products'], PRODUCT_COLUMNS),
             'co_component_routes.csv': c(b['routes'], ROUTE_COLUMNS), 'percentage_basis.csv': c(b['basis'], BASIS_COLUMNS),
             'volume_dose_evidence.csv': c(b['volume'], VOLUME_COLUMNS),
             'applicability_review.csv': c(b['appl'], APPL_COLUMNS), 'calculation_readiness.csv': c(b['calcs'], CALC_COLUMNS)}
    blocking = [a for a in b['attrs'] if a['blocking']]
    cnt = lambda rows, key: collections.Counter(r[key] for r in rows)
    classes = list(R.CHECKERS)

    def table(key, values, rows=blocking):
        t = collections.defaultdict(collections.Counter)
        for r in rows:
            t[r['material_class']][r[key]] += 1
        out = ['| Material class | ' + ' | '.join(values) + ' |', '|---|' + '---:|' * len(values)]
        return out + [f'| {k} | ' + ' | '.join(str(t[k][v]) for v in values) + ' |' for k in classes]
    ev_vals = ['documented', 'documented_incomplete', 'not_recorded', 'requirement_unknown', 'recorded_route_not_assessed',
               'applicability_unresolved', 'invalid', 'calculated_not_reproduced', 'not_applicable_approved_rule']
    md = ['# Requirement attributes and policy detail (companion to the eligibility outputs)', '',
          f'Generated by `python tools/mandatory_properties/build_readiness.py`. Readiness version `{READINESS_VERSION}`; requirements '
          f'version `{R.REQUIREMENTS_VERSION}`; source snapshot SHA-256 `{b["snapshot"]}`.', '',
          '`tier1_complete` and `formulation_eligible` are defined and reported only in `product_eligibility.csv`; nothing here changes '
          'them. These files cover the mandatory Tier 1 requirements and the VM/PPD subtype blocks. They are not the feature inventory '
          'of the association-mining dataset.', '',
          f'## Mandatory requirement outcomes: {len(blocking)} in {len(b["rows"])} products', '',
          '### Evidence documentation (what the record holds)', '',
          '"not_recorded" describes the record. It does not say that a source was searched or that the supplier is silent; the review '
          'state of the source is the verification status below.', '']
    md += table('evidence_documentation', ev_vals)
    md += ['', '### Value selection (from the source-selection ledger, independent of the outcome category)', '']
    md += table('value_selection', ['selected', 'pending', 'none'])
    md += ['', '### Value form (a range or bound is documented information and is never replaced by a point)', '']
    md += table('value_form', ['point', 'closed_range', 'lower_bound', 'upper_bound', 'specification_value_no_direction', 'text', 'structured', 'none'])
    md += ['', '### Verification status of the source', '',
           'Scope: only the base-oil properties in the coverage ledger have a review state; every other requirement shows '
           '`not_individually_reviewed`.', '']
    md += table('verification_status', sorted(cnt(blocking, 'verification_status')))
    rb = [a for a in blocking if a['value_form'] in NUMERIC_FORMS[1:]]
    md += ['', f'### Documented ranges and bounds: {len(rb)} mandatory outcomes in {len({a["product_id"] for a in rb})} products', '',
           '| Requirement | closed_range | lower_bound | upper_bound | of which selection pending |', '|---|---:|---:|---:|---:|']
    t = collections.defaultdict(collections.Counter)
    for a in rb:
        t[a['requirement']][a['value_form']] += 1
        t[a['requirement']]['pending'] += a['value_selection'] == 'pending'
    md += [f'| `{k}` | {v["closed_range"]} | {v["lower_bound"]} | {v["upper_bound"]} | {v["pending"]} |' for k, v in sorted(t.items())]
    pend = [a for a in blocking if a['value_selection'] == 'pending']
    pc = cnt(pend, 'outcome_category')
    md += ['', f'### Pending selections: {len(pend)} mandatory outcomes in {len({a["product_id"] for a in pend})} products', '',
           'Scope: mandatory Tier 1 properties that the source-selection ledger lists as pending. The ledger also holds pending '
           'selections of non-mandatory properties, which are outside these files.', '',
           'By outcome category: ' + ', '.join(f'{k} {v}' for k, v in sorted(pc.items())) + '. A pending selection whose value also has '
           'a metadata defect keeps the category of the defect; it is still pending.', '',
           '| Requirement | Pending | Products (category if not unresolved_source_selection) |', '|---|---:|---|']
    tp = collections.defaultdict(list)
    for a in pend:
        tp[a['requirement']].append(a['product_id'] + ('' if a['outcome_category'] == R.SEL else f' ({a["outcome_category"]})'))
    md += [f'| `{k}` | {len(v)} | {", ".join(sorted(v))} |' for k, v in sorted(tp.items())]
    bc = collections.defaultdict(collections.Counter)
    for r in b['basis']:
        bc[r['field'].split('[')[0]][r['basis_class']] += 1
    un = [r for r in b['basis'] if r['basis_class'] == 'unspecified']
    mass_bad = [r for r in b['basis'] if r['basis_class'] == 'mass' and r['value_outcome_category'] != R.MET]
    md += ['', f'## Percentage basis: {len(b["basis"])} reported values in the dose and treat-rate fields', '',
           'Scope: values with status Reported or Calculated in `treat_rate_matrix[].treat_rate_wt_pct`, '
           '`required_co_components[].dose_wt_pct`, the component `treat_rate`, `vm.treat_range_by_sae_grade[]` and '
           '`ppd.tested_dose_range_wt_pct`. Volume evidence kept outside these fields is counted separately below.', '',
           '| Field | mass | volume | unspecified |', '|---|---:|---:|---:|']
    md += [f'| `{k}` | {v["mass"]} | {v["volume"]} | {v["unspecified"]} |' for k, v in sorted(bc.items())]
    md += ['', f'- {len(un)} values in {len({r["product_id"] for r in un})} products have an unspecified basis. They stay as printed.',
           f'- `basis_is_mass` says only that the basis is mass. It is not a usability verdict: {len(mass_bad)} mass-basis value(s) are not '
           'met for another reason (`value_outcome_category`).',
           f'- Volume-basis dose evidence outside the dose fields (`volume_dose_evidence.csv`): {len(b["volume"])} entries in '
           f'{len({r["product_id"] for r in b["volume"]})} product(s), kept as recorded in `external_fill_notes`. They fill no wt.% field '
           'and nothing is converted.', '']
    rq = [r for r in b['routes'] if r['row_kind'] == 'recorded_requirement']
    uniq = {(r['product_id'], r['entry_index']): r for r in rq}
    rs = cnt(uniq.values(), 'requirement_state')
    rev = [r for r in b['routes'] if r['row_kind'] == 'reviewed_route']
    no_route = [r for r in rq if r['route_state'] == 'route_association_not_established']
    shared = collections.Counter((r['product_id'], r['entry_index']) for r in rq if r['route_id'])
    nr = cnt([r for r in b['routes'] if r['row_kind'] == 'no_recorded_requirement'], 'source_inspection')
    pk = collections.Counter(r['product_level_outcome'].split(':')[0] for r in {r['product_id']: r for r in b['routes']}.values())
    md += ['## Co-component requirements', '',
           f'Recorded requirements: {len(uniq)} in {len({k[0] for k in uniq})} packages. By dose state: '
           + ', '.join(f'{x} {rs[x]}' for x in R.CO_STATES) + '.', '',
           f'Reviewed routes: {len(rev)} in {len({r["product_id"] for r in rev})} packages. By state: '
           + (', '.join(f'{k} {v}' for k, v in sorted(cnt(rev, 'route_state').items())) or 'none') + '. By validity of the review: '
           + (', '.join(f'{k} {v}' for k, v in sorted(cnt(rev, 'review_validity').items())) or 'none')
           + f'. Requirement lists confirmed complete: {sum(str(r["requirement_list_confirmed"]).lower() == "true" for r in rev)}.', '',
           f'Route memberships (one row per requirement and route): {sum(shared.values())}; requirements that belong to more than one route: '
           f'{sum(1 for v in shared.values() if v > 1)}; recorded requirements with no route association: {len(no_route)} in '
           f'{len({r["product_id"] for r in no_route})} packages. Requirements stated by a source and not held by the record: '
           f'{sum(r["row_kind"] == "requirement_stated_by_source_not_in_record" for r in b["routes"])}.', '',
           'A route exists only through reviewed evidence bound to the record by fingerprint; nothing is mapped from the role text. '
           'Routes are assessed separately, and no target route is specified, so nothing here is a statement of formulation readiness. '
           'A usable dose on one requirement establishes nothing about a route.', '',
           f'Reviewed supplier statements: {sum(r["row_kind"] == "reviewed_statement" for r in b["routes"])} (a qualified or partial '
           'statement is not "none required"; see `qualification`).', '',
           'Packages with no recorded requirement, by what was inspected: ' + (', '.join(f'{k} {v}' for k, v in sorted(nr.items())) or 'none')
           + '. "Not recorded" is a fact about the record; "not found in the inspected text" is a keyword search of text layers, not a '
           'source review, and is never read as supplier silence.', '',
           'Product-level outcome of the requirement: ' + ', '.join(f'{k} {v}' for k, v in sorted(pk.items())) + '.', '']
    ac = cnt(b['appl'], 'row_kind')
    md += ['## Applicability', '', f'Approved applicability rules: {len(R.APPROVED_APPLICABILITY_RULES)}. Labels in the records without a rule: '
           f'{ac["label_in_record"]} value objects in {len({r["product_id"] for r in b["appl"] if r["row_kind"] == "label_in_record"})} '
           f'products. Requirement outcomes in category unresolved_applicability: '
           f'{sum(r["label_or_category"] == R.APPL for r in b["appl"] if r["row_kind"] == "requirement_outcome")}. All stay unresolved.', '',
           '## Calculations', '', '| Calculation | Status | Values assessed | Accepted | Not accepted |', '|---|---|---:|---:|---:|']
    md += [f'| {x["calculation"]} | {x["status"]} | {x["values_assessed"]} | {x["accepted"]} | {x["not_accepted"]} |' for x in b['calcs']]
    md += ['', 'No product is described as ready for calculation in general, and no conversion is registered.', '']
    files['readiness_summary.md'] = '\n'.join(md)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--check', action='store_true', help='compare with existing outputs; write nothing')
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        b = build()
    except BE.StaleInput as e:
        print(f'STOP: {e}')
        return 3
    if b['problems']:
        print('\n'.join(b['problems']))
        return 2
    files = render(b)
    if a.check:
        bad = []
        for name, text in files.items():
            p = os.path.join(a.out, name)
            if not os.path.exists(p):
                bad.append(name); continue
            with open(p, encoding='utf-8', newline='') as fh:
                if fh.read().replace('\r\n', '\n') != text:
                    bad.append(name)
        print('up to date' if not bad else 'DIFFERS: ' + ', '.join(bad))
        return 1 if bad else 0
    os.makedirs(a.out, exist_ok=True)
    for name, text in files.items():
        with open(os.path.join(a.out, name), 'w', encoding='utf-8', newline='') as fh:
            fh.write(text)
    blocking = [x for x in b['attrs'] if x['blocking']]
    print(f'{len(b["attrs"])} requirement outcomes ({len(blocking)} mandatory) for {len(b["rows"])} products; snapshot {b["snapshot"]}')
    for key in ('evidence_documentation', 'value_selection', 'value_form'):
        print(f'  {key}: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(x[key] for x in blocking).most_common()))
    print('  basis of values in the dose fields: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['basis_class'] for r in b['basis']).most_common())
          + f'; volume evidence entries outside the fields: {len(b["volume"])}')
    rev = [r for r in b['routes'] if r['row_kind'] == 'reviewed_route']
    rq = {(r['product_id'], r['entry_index']): r for r in b['routes'] if r['row_kind'] == 'recorded_requirement'}
    print('  recorded co-component requirements: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['requirement_state'] for r in rq.values()).most_common())
          + f'; reviewed routes {len(rev)}: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['route_state'] for r in rev).most_common())
          + '; without a route: ' + str(sum(r['route_state'] == 'route_association_not_established' for r in b['routes'] if r['row_kind'] == 'recorded_requirement')))
    print('  packages with no recorded requirement: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(
        r['source_inspection'] for r in b['routes'] if r['row_kind'] == 'no_recorded_requirement').most_common()))
    print(f'  applicability: approved rules {len(R.APPROVED_APPLICABILITY_RULES)}; labels without a rule '
          f'{sum(r["row_kind"] == "label_in_record" for r in b["appl"])}; unresolved outcomes '
          f'{sum(r["row_kind"] == "requirement_outcome" for r in b["appl"])}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
