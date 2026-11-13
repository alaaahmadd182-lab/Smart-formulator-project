"""One-off helper (2026-11-12, route review): replaces the co-component route and statement code in
tools/mandatory_properties/requirements.py. Already applied; do not rerun (it asserts on its anchor texts)."""
R = 'C:\\Users\\windo\\sf-wsA\\'
p = R + 'tools\\mandatory_properties\\requirements.py'
s = open(p, encoding='utf-8').read()


def sub(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


sub("import math, re\n", "import hashlib, json, math, re\n")
sub("REQUIREMENTS_VERSION = 'mandatory-tier1-2026-11-10.5'", "REQUIREMENTS_VERSION = 'mandatory-tier1-2026-11-10.6'")
sub("""  2. co-components       completeness is assessed per evidenced route: every requirement that applies to the route
                         must have a usable dose, and the route's requirement list must be confirmed by source review.
                         One usable component never completes a route that needs others. Routes are independent.
                         Without reviewed route evidence the association is unresolved and completeness is not
                         assessed. "None required" needs an explicit, unqualified, applicable statement.
""", """  2. co-components       completeness is assessed per evidenced route: every requirement that applies to the route
                         must have a usable dose, and the route's requirement list must be confirmed by source review.
                         One usable component never completes a route that needs others. Routes are independent, and
                         a component may belong to several. Route evidence is bound to the complete input records by
                         fingerprint: a relevant change makes it stale until re-reviewed. "None required" needs an
                         explicit reviewed assessment (meaning, scope, product, conditions, qualification).
""")
a = s.index("CO_STATES = (")
b = s.index("def additive_package_requirements(")
s = s[:a] + '''CO_STATES = ('required_usable_dose', 'required_dose_not_usable', 'required_dose_not_recorded')
ROUTE_STATES = ('route_complete', 'route_incomplete', 'recorded_requirements_usable_list_not_confirmed', 'route_evidence_stale',
                'route_evidence_invalid', 'route_association_not_established')
REVIEW_VALIDITY = ('current', 'stale_requires_re_review', 'invalid')
COMBINATIONS = ('all', 'one_of', 'unresolved')
ALL_CO = 'all co-components'
DERIVED_KEYS = ('value_final', 'unit_final', 'min_final', 'max_final', 'integration_flags', 'unit_conversion', 'resolution')
_BOUND_PATH = re.compile(r'(required_co_components|treat_rate_matrix)\\[(\\d+)\\]')
_HEDGE = re.compile(r'\\b(should|may|might|could|normally|typically|generally|usually|in most cases|unless|except|provided that)\\b', re.I)


def record_fingerprint(record):
    """SHA-256 of the complete record as recorded (every key: value, qualifier, min, max, value kind, printed text, unit,
    conditions, method, status, notes, source file, page and revision), without the derived *_final keys. Reviewed
    route evidence stores this for each record it relies on; any relevant change gives a different fingerprint."""
    def strip(x):
        if isinstance(x, dict):
            return {k: strip(v) for k, v in sorted(x.items()) if k not in DERIVED_KEYS}
        if isinstance(x, list):
            return [strip(v) for v in x]
        return x
    return hashlib.sha256(json.dumps(strip(record), ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def record_at(fields, path):
    """The record a route binding names ('required_co_components[i]' or 'treat_rate_matrix[i]'), or None."""
    m = _BOUND_PATH.fullmatch(str(path or ''))
    if not m:
        return None
    lst = fields.get(m.group(1)) or []
    i = int(m.group(2))
    return lst[i] if i < len(lst) and isinstance(lst[i], dict) else None


def co_component_entries(fields, ctx=None):
    """The recorded co-component requirements, one dict per entry (index, role, name, dose, state, outcome). The role
    text carries the supplier's condition as recorded; it is reported, never parsed into a route."""
    ctx = ctx or Context()
    rows = []
    for i, e in enumerate(fields.get('required_co_components') or []):
        if not (isinstance(e, dict) and (e.get('name') or e.get('role'))):
            continue
        dose = e.get('dose_wt_pct')
        if not isinstance(dose, dict) or dose.get('status') in (None, 'Missing'):
            o = _o('required_co_components', ABSENT, 'the requirement is recorded, but no dose is recorded for it')
            state = 'required_dose_not_recorded'
        else:
            o = check_value(dose, 'required_co_components', ctx, mass_basis=True, path='required_co_components')
            state = 'required_usable_dose' if o.category == MET else 'required_dose_not_usable'
        rows.append(dict(index=i, role=e.get('role'), name=e.get('name'), dose=dose if isinstance(dose, dict) else {}, state=state, outcome=o))
    return rows


def explicit_none_required(stmt, product, inline=False):
    """(ok, why not) for a statement offered as "no co-component is required" for `product` as a whole.

    Nothing is inferred from missing metadata, and the meaning is never established by keyword matching. The statement
    must carry the supplier wording, its source page, and an explicit reviewed assessment:
      product                        equal to the product being assessed (an inline statement must name it too)
      kind                           'none_required'
      quote, source file and page    the wording as printed and where it is
      review.reviewed_on             date of the review
      review.meaning                 'no_co_component_required'
      review.unconditional           true or false, stated explicitly
      review.qualification_verbatim  the supplier's qualification exactly as printed; '' only if unconditional is true
      review.scope.component_types   'all' or a list of the component types the statement covers
      review.scope.routes            'all' or a list of the routes / conditions it covers
      review.conditions_verbatim     the conditions as printed ('' if none)
    It is product-wide only if it is unconditional and covers all component types and all routes. Contradictory or
    incomplete metadata is rejected. A hedge word in the quote together with unconditional = true is treated as a
    contradiction that needs re-review (a consistency guard, not the basis of the meaning)."""
    if not isinstance(stmt, dict):
        return False, 'not a structured statement'
    if not product or stmt.get('product') != product:
        return False, f"the statement names product {stmt.get('product')!r}, not {product!r}"
    if stmt.get('kind') != 'none_required':
        return False, "kind is not 'none_required'"
    quote = str(stmt.get('quote') or '').strip()
    if not quote:
        return False, 'the quoted supplier wording is missing'
    src = stmt.get('source') if isinstance(stmt.get('source'), dict) else {}
    f = stmt.get('source_file') or src.get('file')
    pg = stmt.get('page') if stmt.get('page') not in (None, '') else src.get('page')
    if not f or pg in (None, ''):
        return False, 'source file or page is missing'
    if inline and stmt.get('status') != 'Reported':
        return False, 'the inline statement is not status Reported'
    rv = stmt.get('review')
    if not isinstance(rv, dict):
        return False, 'no reviewed assessment of the wording (review) is recorded'
    scope = rv.get('scope')
    missing = [k for k in ('reviewed_on', 'meaning') if not rv.get(k)]
    missing += [k for k in ('unconditional', 'qualification_verbatim', 'conditions_verbatim') if k not in rv]
    if not isinstance(scope, dict) or 'component_types' not in scope or 'routes' not in scope:
        missing.append('scope.component_types / scope.routes')
    if missing:
        return False, 'review metadata incomplete: ' + ', '.join(missing)
    if not isinstance(rv['unconditional'], bool) or not isinstance(rv['qualification_verbatim'], str):
        return False, 'review metadata invalid: unconditional must be true/false and qualification_verbatim a string'
    qual = rv['qualification_verbatim'].strip()
    if rv['unconditional'] and qual:
        return False, 'review metadata contradictory: unconditional is true but a qualification is recorded'
    if not rv['unconditional'] and not qual:
        return False, 'review metadata incomplete: unconditional is false but the qualification is not quoted'
    if qual and qual.lower() not in quote.lower():
        return False, 'review metadata contradictory: the recorded qualification is not part of the quoted wording'
    if rv['unconditional'] and _HEDGE.search(quote):
        return False, ('review metadata contradictory: the quoted wording contains a qualifying word '
                       f'({_HEDGE.search(quote).group(0)!r}) although unconditional is true; re-review needed')
    top = str(stmt.get('scope') or '').strip().lower()
    full = scope['component_types'] == 'all' and scope['routes'] == 'all'
    if top and (top == ALL_CO) != full:
        return False, 'review metadata contradictory: the statement scope and the reviewed scope disagree'
    if rv['meaning'] != 'no_co_component_required':
        return False, f"reviewed meaning is {rv['meaning']!r}, not 'no_co_component_required'"
    if not rv['unconditional']:
        return False, f'the supplier wording is qualified ({qual!r}): not an unconditional statement'
    if not full:
        return False, (f"the statement is limited to component types {scope['component_types']!r} and routes {scope['routes']!r}: "
                       'not a product-wide statement')
    return True, ''


def assess_route(route, fields, by_index):
    """Assessment of one reviewed route against the current record.

    Evidence (co_component_route_evidence.json): product, route_id, label, conditions (as printed), source_file, page,
    quote, reviewed_on, association_basis, required (groups of recorded entries: combination 'all', 'one_of' for
    supplier-stated alternatives, or 'unresolved' where the source does not say; each alternative is a path with the
    fingerprint of the complete record), bound_records (other records the route relies on, e.g. its treat-rate entry),
    unrecorded_requirements (requirements the source states that the record does not hold), requirement_list_confirmed
    (true/false) with list_assessment, and limitations.

    validity: current | stale_requires_re_review (a bound record changed or is gone) | invalid (metadata incomplete).
    state (only for current evidence): route_complete | route_incomplete (a required group has no usable dose, or a
    stated requirement has no recorded dose) | recorded_requirements_usable_list_not_confirmed."""
    out = dict(route=route, groups=[], members=[], state='route_evidence_invalid', validity='invalid', why='')
    need = ('route_id', 'source_file', 'page', 'quote', 'reviewed_on', 'list_assessment')
    bad = [k for k in need if route.get(k) in (None, '')]
    if not isinstance(route.get('required'), list) or not isinstance(route.get('requirement_list_confirmed'), bool):
        bad.append('required / requirement_list_confirmed')
    for g in route.get('required') if isinstance(route.get('required'), list) else []:
        if not isinstance(g, dict) or g.get('combination') not in COMBINATIONS or not g.get('alternatives'):
            bad.append(f"group {(g or {}).get('group')!r}")
    if bad:
        return dict(out, why='review metadata incomplete or invalid: ' + ', '.join(bad))
    bound = list(route.get('bound_records') or []) + [a for g in route['required'] for a in g['alternatives']]
    changed = []
    for b in bound:
        rec = record_at(fields, b.get('path'))
        if rec is None or not b.get('sha256') or record_fingerprint(rec) != b['sha256']:
            changed.append(str(b.get('path')))
    idx = lambda a: int(_BOUND_PATH.fullmatch(a['path']).group(2))
    members = [by_index[idx(a)] for g in route['required'] for a in g['alternatives']
               if _BOUND_PATH.fullmatch(str(a.get('path') or '')) and idx(a) in by_index]
    if changed:
        return dict(out, members=members, state='route_evidence_stale', validity='stale_requires_re_review',
                    why='the record changed since the review, or is no longer present: ' + ', '.join(sorted(set(changed))))
    groups = []
    for g in route['required']:
        alts = [by_index.get(idx(a)) for a in g['alternatives']]
        if any(a is None for a in alts):
            return dict(out, why=f"group {g.get('group')!r} names an entry that is not a recorded requirement")
        ok = [a['state'] == 'required_usable_dose' for a in alts]
        st = ('combination_unresolved' if g['combination'] == 'unresolved' else
              'satisfied' if (all(ok) if g['combination'] == 'all' else any(ok)) else 'no_usable_dose')
        groups.append(dict(group=g.get('group'), combination=g['combination'], members=alts, state=st))
    unrec = route.get('unrecorded_requirements') or []
    if any(g['state'] == 'no_usable_dose' for g in groups) or unrec:
        state = 'route_incomplete'
        why = '; '.join([f"{g['group']}: no usable dose" for g in groups if g['state'] == 'no_usable_dose']
                        + [f"{u.get('component')}: stated by the source, not recorded with a dose" for u in unrec])
    elif route['requirement_list_confirmed'] and not any(g['state'] == 'combination_unresolved' for g in groups):
        state, why = 'route_complete', 'every required group has a usable dose and the requirement list is confirmed by source review'
    else:
        state = 'recorded_requirements_usable_list_not_confirmed'
        why = '; '.join([f"{g['group']}: whether the alternatives combine or substitute is not established" for g in groups
                         if g['state'] == 'combination_unresolved']
                        + ([] if route['requirement_list_confirmed'] else ['the requirement list is not confirmed complete: ' + route['list_assessment']]))
    return dict(out, groups=groups, members=members, state=state, validity='current', why=why)


def co_component_routes(fields, ctx=None):
    """(route assessments, entries without any current route, all entries). A route exists only through reviewed
    evidence; nothing is mapped from the role text. A recorded entry may be a member of several independent routes;
    every membership is kept. Entries named only by stale or invalid evidence have no CURRENT association."""
    ctx = ctx or Context()
    entries = co_component_entries(fields, ctx)
    by_index = {e['index']: e for e in entries}
    routes = [assess_route(r, fields, by_index) for r in ctx.routes if r.get('product') == ctx.product]
    current = {m['index'] for r in routes if r['validity'] == 'current' for m in r['members']}
    return routes, [e for e in entries if e['index'] not in current], entries


def none_required_statements(fields, ctx):
    """[(statement, is inline, ok, why)] for the inline statement of the record and the reviewed sidecar statements of
    this product. Both kinds pass through the same check against the current product."""
    out = []
    inline = fields.get('co_component_requirement_statement')
    if inline is not None:
        st = dict(inline, quote=inline.get('quote') or inline.get('printed_text')) if isinstance(inline, dict) else inline
        out.append((st, True) + explicit_none_required(st, ctx.product, inline=True))
    for x in ctx.statements:
        if isinstance(x, dict) and x.get('product') == ctx.product and x.get('kind') == 'none_required':
            out.append((x, False) + explicit_none_required(x, ctx.product))
    return out


def co_component_outcome(fields, ctx=None):
    """Product-level outcome of the co-component requirement. Met only by (a) a current, evidenced route that is
    complete, or (b) an explicit, reviewed, unconditional, product-wide statement that no co-component is required,
    with no recorded requirement. The count of usable components is informational and establishes nothing. With no
    target route specified this is not a statement about formulation readiness: the reason lists every route."""
    ctx = ctx or Context()
    rid = 'required_co_components'
    routes, unassigned, entries = co_component_routes(fields, ctx)
    usable = [e for e in entries if e['state'] == 'required_usable_dose']
    info = (f'informational only: {len(usable)} of {len(entries)} recorded requirement(s) have a usable dose, which does not '
            'establish the completeness of any route')
    listing = '; '.join(f"{r['route'].get('route_id')}: {r['state']}" for r in routes)
    complete = [r for r in routes if r['state'] == 'route_complete']
    if complete:
        r = complete[0]['route']
        return _o(rid, MET, f"route {r['route_id']!r} is complete ({r['source_file']} p.{r['page']}); routes are assessed separately "
                  f'and this is not a statement about any other route [{listing}] ({info})', rep='structured', basis='mass')
    stmts = none_required_statements(fields, ctx)
    good = [x for x in stmts if x[2]]
    if good and not entries and not routes:
        st = good[0][0]
        src = st.get('source') if isinstance(st.get('source'), dict) else {}
        return _o(rid, MET, 'explicit, reviewed, unconditional and product-wide statement that no co-component is required: '
                  f"{st.get('source_file') or src.get('file')} p.{st.get('page') or src.get('page')}", rep='text')
    if not entries and not routes:
        inline_bad = [x for x in stmts if x[1]]
        if inline_bad:
            return _o(rid, META, 'co_component_requirement_statement is recorded but is not an explicit, reviewed, applicable "none '
                      f'required" statement: {inline_bad[0][3]}')
        if stmts:
            st, _, _, why = stmts[0]
            return _o(rid, UNKNOWN, f"no requirement is recorded; a reviewed supplier statement exists ({st.get('source_file')} "
                      f"p.{st.get('page')}) but does not establish that none is required: {why}")
        return _o(rid, UNKNOWN, 'no co-component requirement is recorded in the product record and no explicit statement that none is '
                  'required is recorded. This describes the record, not the supplier documents: what was inspected is in '
                  'co_component_routes.csv')
    if not routes:
        if entries and not usable:
            bad = [e for e in entries if e['state'] == 'required_dose_not_usable']
            if bad:
                o = bad[0]['outcome']
                return o._replace(requirement=rid, reason=f'{len(entries)} requirement(s) recorded, none with a usable dose, so no route '
                                  f'that includes them can be complete ({o.reason})')
            return _o(rid, ABSENT, f'{len(entries)} requirement(s) recorded, none with a dose: no route that includes them can be complete '
                      '(the requirement is recorded; its dose is not)')
        return _o(rid, ROUTE, f'route association not established by reviewed evidence for {len(unassigned)} of {len(entries)} recorded '
                  f'requirement(s): the completeness of a route is not assessed ({info})')
    open_states = ('recorded_requirements_usable_list_not_confirmed', 'route_evidence_stale', 'route_evidence_invalid')
    if unassigned or any(r['state'] in open_states for r in routes):
        return _o(rid, ROUTE, f'no reviewed route is complete, and at least one is not resolved [{listing}]'
                  + (f'; {len(unassigned)} recorded requirement(s) have no current route association' if unassigned else '') + f' ({info})')
    return _o(rid, ABSENT, f'every reviewed route is incomplete: a requirement documented for it has no usable dose [{listing}] ({info})')


'''.replace('\\\\', '\\') + s[b:]
open(p, 'w', encoding='utf-8', newline='\n').write(s)
import ast
ast.parse(s)
print('ok')
