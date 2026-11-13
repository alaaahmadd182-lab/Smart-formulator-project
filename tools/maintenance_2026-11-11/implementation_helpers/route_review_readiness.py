"""One-off helper (2026-11-12, route review): route reporting in build_readiness.py. Already applied; do not rerun."""
R = 'C:\\Users\\windo\\sf-wsA\\'
p = R + 'tools\\mandatory_properties\\build_readiness.py'
s = open(p, encoding='utf-8').read()


def sub(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


sub("READINESS_VERSION = 'readiness-2026-11-11.2'", "READINESS_VERSION = 'readiness-2026-11-12.1'")
sub("""SOURCE_INSPECTION = ('confirmed_by_source_review', 'recorded_from_cited_page_not_re_reviewed', 'lead_in_inspected_text_not_reviewed',
                     'not_found_in_inspected_text', 'source_unavailable', 'not_inspected')""",
    """SOURCE_INSPECTION = ('confirmed_by_source_review', 'historical_source_review_not_current', 'recorded_from_cited_page_not_re_reviewed',
                     'lead_in_inspected_text_not_reviewed', 'not_found_in_inspected_text', 'source_unavailable', 'not_inspected')
# what a source review of a route says about its CURRENT applicability: only 'current' evidence is confirmed
INSPECTION_BY_VALIDITY = {'current': 'confirmed_by_source_review', 'stale_requires_re_review': 'historical_source_review_not_current',
                          'invalid': 'historical_source_review_not_current'}""")
sub("""'source_file', 'page', 'requirement_state', 'route_id',
                 'route_state', 'record_state', 'source_inspection', 'inspected', 'qualification', 'detail', 'product_level_outcome']""",
    """'source_file', 'page', 'requirement_state', 'route_id',
                 'route_state', 'review_validity', 'reviewed_on', 'group', 'group_combination', 'group_state', 'requirement_list_confirmed',
                 'record_state', 'source_inspection', 'inspected', 'qualification', 'limitations', 'detail', 'product_level_outcome']""")
sub("""source_file='', page='', requirement_state='', route_id='', route_state='',
                 record_state='', source_inspection='', inspected='', qualification='', detail='')""",
    """source_file='', page='', requirement_state='', route_id='', route_state='',
                 review_validity='', reviewed_on='', group='', group_combination='', group_state='', requirement_list_confirmed='',
                 record_state='', source_inspection='', inspected='', qualification='', limitations='', detail='')""")
a = s.index("        rts, unassigned, entries = R.co_component_routes(fields, ctx)")
b = s.index("        if not entries and not own:")
s = s[:a] + '''        rts, unassigned, entries = R.co_component_routes(fields, ctx)
        routes += route_rows(pid, ctx, rts, entries, statements, lvl, blank)
        own = [x for x in statements if x.get('product') == pid]
''' + s[b:]
sub("def scan_inspection(scan_row):", '''def route_rows(pid, ctx, rts, entries, statements, lvl, blank):
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


def scan_inspection(scan_row):''')
# the summary section
a = s.index("    rq = [r for r in b['routes'] if r['row_kind'] == 'recorded_requirement']\n    rs, ra = cnt(rq, 'requirement_state'), cnt(rq, 'route_state')")
b = s.index("    ac = cnt(b['appl'], 'row_kind')")
s = s[:a] + '''    rq = [r for r in b['routes'] if r['row_kind'] == 'recorded_requirement']
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
''' + s[b:]
sub("""    rq = [r for r in b['routes'] if r['row_kind'] == 'recorded_requirement']
    print('  recorded co-component requirements: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['requirement_state'] for r in rq).most_common())
          + '; route association: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['route_state'] for r in rq).most_common()))""",
    """    rev = [r for r in b['routes'] if r['row_kind'] == 'reviewed_route']
    rq = {(r['product_id'], r['entry_index']): r for r in b['routes'] if r['row_kind'] == 'recorded_requirement'}
    print('  recorded co-component requirements: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['requirement_state'] for r in rq.values()).most_common())
          + f'; reviewed routes {len(rev)}: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['route_state'] for r in rev).most_common())
          + '; without a route: ' + str(sum(r['route_state'] == 'route_association_not_established' for r in b['routes'] if r['row_kind'] == 'recorded_requirement')))""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
import ast
ast.parse(s)
print('ok')
