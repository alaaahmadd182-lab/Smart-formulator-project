"""One-off helper (2026-11-11, gap fixes): edits tools/mandatory_properties/requirements.py. Already applied; do not rerun
(each replacement asserts that its target text occurs exactly once, so a second run stops without changing anything)."""
R = 'C:\\Users\\windo\\sf-wsA\\'
p = R + 'tools\\mandatory_properties\\requirements.py'
s = open(p, encoding='utf-8').read()


def sub(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


def block(start, end, new):
    global s
    a, b = s.index(start), s.index(end)
    assert a < b
    s = s[:a] + new + s[b:]


# ---- docstring and categories
sub("""  requirement_unknown                 whether a requirement exists is not known: the supplier documents are silent
                                      (required co-components; silence is never read as "none required")
""", """  requirement_unknown                 whether a requirement exists is not known: none is recorded in the record and no
                                      explicit statement says that none is required. This is a statement about the
                                      record; it does not say that the supplier documents are silent
  unresolved_route_association        co-component requirements are recorded, but which route each belongs to is not
                                      established by reviewed evidence, so the completeness of a route is not assessed
""")
sub("""  2. co-components       a recorded supplier requirement with a usable dose is met; a recorded requirement without a
                         usable dose leaves its route incomplete; "none required" needs an explicit, applicable
                         statement; silence is requirement_unknown. Route-level detail: build_readiness.py.
  3. percentage basis    mass, volume or unspecified, established from the unit or from reviewed source evidence
                         (heading, footnote, document-wide convention). An unspecified or volume percentage does not
                         satisfy a wt.% requirement; volume is converted only by volume_to_mass_percent().
""", """  2. co-components       completeness is assessed per evidenced route: every requirement that applies to the route
                         must have a usable dose, and the route's requirement list must be confirmed by source review.
                         One usable component never completes a route that needs others. Routes are independent.
                         Without reviewed route evidence the association is unresolved and completeness is not
                         assessed. "None required" needs an explicit, unqualified, applicable statement.
  3. percentage basis    mass, volume or unspecified, established from the unit or from reviewed source evidence
                         (heading, footnote, document-wide convention). An unspecified or volume percentage does not
                         satisfy a wt.% requirement. No volume-to-mass conversion is registered or used.
""")
sub("""UNKNOWN = 'requirement_unknown'
SEL = 'unresolved_source_selection'
CATEGORIES = [MET, NOT_APPLICABLE, ABSENT, BOUND, META, INVALID, CALC, APPL, UNKNOWN, SEL]""",
    """UNKNOWN = 'requirement_unknown'
ROUTE = 'unresolved_route_association'
SEL = 'unresolved_source_selection'
CATEGORIES = [MET, NOT_APPLICABLE, ABSENT, BOUND, META, INVALID, CALC, APPL, UNKNOWN, ROUTE, SEL]""")
sub("""Outcome = namedtuple('Outcome', 'requirement category reason calculated blocking representation basis', defaults=('',))""",
    """# selection_pending is independent of the category: a requirement can have incomplete metadata AND a pending selection
Outcome = namedtuple('Outcome', 'requirement category reason calculated blocking representation basis selection_pending',
                     defaults=('', False))""")
sub("""    order = [BOUND, SEL, META, CALC, INVALID, APPL, UNKNOWN, ABSENT]""", """    order = [BOUND, SEL, META, CALC, INVALID, APPL, ROUTE, UNKNOWN, ABSENT]""")

# ---- interpretations
block("    ('I-6', '[Approved policy 3, 2026-11-11]", "    ('I-7',", """    ('I-6', '[Approved policy 3, 2026-11-11] The basis of a percentage is mass, volume or unspecified. It is established '
            'from the recorded unit or from reviewed source evidence (heading, footnote or explicit document-wide convention) '
            'in treat_rate_basis_evidence.json. An unspecified "%" stays unspecified, and a volume percentage stays volume: '
            'neither satisfies a wt.% requirement. No volume-to-mass conversion is registered or used; volume evidence is '
            'listed separately and never fills a wt.% field.'),
""")
block("    ('I-8', '[Approved policy 2, 2026-11-11]", "    ('I-9',", """    ('I-8', '[Approved policy 2, 2026-11-11] Package co-components are assessed per evidenced route. A route is complete '
            'only if every requirement that applies to it has a usable mass-basis dose and its requirement list is confirmed '
            'by source review; one usable component never completes a route that needs others, and routes are independent. '
            'Without reviewed route evidence the association is unresolved and completeness is not assessed. The product-level '
            'requirement is met only by a complete evidenced route or by an explicit, unqualified, applicable statement that '
            'none is required. An empty record is "not recorded", never supplier silence.'),
""")

# ---- context: reviewed route evidence
sub("""        self.statements = statements or []   # reviewed co-component statements (co_component_statements.json)
""", """        self.statements = statements or []   # reviewed co-component statements (co_component_statements.json)
        self.routes = routes or []           # reviewed route evidence (co_component_route_evidence.json)
""")
sub("""    def __init__(self, page_text=None, pending=None, basis_evidence=None, product=None, material_class=None, task=None,
                 statements=None):""", """    def __init__(self, page_text=None, pending=None, basis_evidence=None, product=None, material_class=None, task=None,
                 statements=None, routes=None):""")

# ---- volume conversion: preserved, unregistered, unused
block("def volume_to_mass_percent(", "def _o(rid, cat", '''def volume_to_mass_percent(vol_pct, component_density, mixture_density, component_density_temp_c, mixture_density_temp_c):
    """NOT REGISTERED AND NOT USED. Arithmetic only: vol.% x rho_component / rho_mixture.

    Kept for a later decision. It checks only what its numeric arguments can show: finite numbers, a volume percentage
    in [0, 100], positive densities, and equal temperature arguments. It does NOT and cannot establish where the
    densities come from, whether they are in the same unit, whether they belong to this component and this mixture, or
    whether a conversion is applicable to the product. Those need reviewed source evidence that the project does not
    have, so no value is converted and no wt.% field is filled from volume evidence. Returns (value, '') or (None, reason)."""
    for name, x in (('volume percentage', vol_pct), ('component density', component_density), ('mixture density', mixture_density)):
        if not finite(x):
            return None, f'{name} is not a finite number ({x!r})'
    if not 0 <= vol_pct <= 100:
        return None, f'volume percentage {vol_pct} is outside 0-100'
    if component_density <= 0 or mixture_density <= 0:
        return None, 'a density is not positive'
    if not (finite(component_density_temp_c) and finite(mixture_density_temp_c)):
        return None, 'a density temperature is not stated'
    if abs(component_density_temp_c - mixture_density_temp_c) > 1e-9:
        return None, f'densities are at different temperatures ({component_density_temp_c} vs {mixture_density_temp_c} °C)'
    return vol_pct * component_density / mixture_density, ''


''')
sub("""def _o(rid, cat, why='', calc=False, blocking=True, rep=None, basis=''):
    return Outcome(rid, cat, why, calc, blocking, rep, basis)""",
    """def _o(rid, cat, why='', calc=False, blocking=True, rep=None, basis=''):
    return Outcome(rid, cat, why, calc, blocking, rep, basis, False)""")
sub("""            return _o(rid, META, f'volume basis ({how}): not usable where wt.% is required; a conversion needs the registered '
                      'calculation volume_to_mass_percent with stated density inputs', is_calc, rep=rep, basis=basis)""",
    """            return _o(rid, META, f'volume basis ({how}): not usable where wt.% is required; no volume-to-mass conversion is '
                      'registered', is_calc, rep=rep, basis=basis)""")

# ---- selection status independent of the category
block("def _sel(o, ctx, prop):", "def base_oil_requirements(", '''def _sel(o, ctx, prop):
    """Rule 1 selection status from the source-selection ledger, independent of the outcome category.

    selection_pending is set whenever the ledger lists the property as pending, whatever else is wrong with the value
    (missing unit, condition or source, a range, an invalid value). The category changes to unresolved_source_selection
    only where the value would otherwise be satisfied or a documented range/bound; in every other case the category
    keeps the first defect and the pending selection is added to the reason, so neither hides the other."""
    why = ctx.pending.get((ctx.product, prop))
    if not why:
        return o
    if o.category in (MET, BOUND):
        return o._replace(category=SEL, reason=f'source selection pending: {why}', selection_pending=True)
    return o._replace(selection_pending=True, reason=(o.reason + '; ' if o.reason else '') + f'in addition, the source selection is pending: {why}')


''')

# ---- co-components: route-level completeness
block("CO_STATES = (", "def additive_package_requirements(", '''CO_STATES = ('required_usable_dose', 'required_dose_not_usable', 'required_dose_not_recorded')
ROUTE_STATES = ('route_complete', 'route_incomplete', 'recorded_requirements_usable_list_not_confirmed', 'route_evidence_invalid',
                'route_association_not_established')
ALL_CO = 'all co-components'


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


def explicit_none_required(stmt, product=None):
    """(ok, why not) for a "none required" statement. It must be a structured, sourced, unqualified statement covering
    all co-components: kind 'none_required', scope 'all co-components', the quoted supplier wording, a source file and
    page, and no qualification. Free text in a value field is not such a statement, and a qualified wording
    ("should be needed", "normally", "may") is kept as printed and never upgraded."""
    if not isinstance(stmt, dict):
        return False, 'not a structured statement'
    if product is not None and stmt.get('product') not in (None, product):
        return False, 'the statement is for another product'
    if stmt.get('kind') != 'none_required':
        return False, "kind is not 'none_required'"
    if str(stmt.get('scope') or '').strip().lower() != ALL_CO:
        return False, f"scope is {stmt.get('scope')!r}, not {ALL_CO!r}"
    if not str(stmt.get('quote') or '').strip():
        return False, 'the quoted supplier wording is missing'
    src = stmt.get('source') if isinstance(stmt.get('source'), dict) else {}
    f, pg = stmt.get('source_file') or src.get('file'), stmt.get('page') if stmt.get('page') not in (None, '') else src.get('page')
    if not f or pg in (None, ''):
        return False, 'source file or page is missing'
    if str(stmt.get('qualification') or '').strip():
        return False, f"the supplier wording is qualified ({stmt.get('qualification')}): not an unconditional statement"
    return True, ''


def _route_members(route, by_index):
    """The recorded entries a reviewed route names, or None if the evidence no longer matches the record."""
    out = []
    for m in route.get('members') or []:
        e = by_index.get(m.get('entry_index'))
        if e is None or e['role'] != m.get('role') or e['name'] != m.get('name') or e['dose'].get('value') != m.get('dose_value'):
            return None
        out.append(e)
    return out or None


def co_component_routes(fields, ctx=None):
    """(routes, unassigned entries, all entries). A route exists only through reviewed evidence
    (co_component_route_evidence.json: product, route_id, label, conditions, source page, quoted wording, the member
    entries, and whether the source review confirmed that the passage lists every co-component the route requires).
    Nothing is mapped from the role text. Route states:
      route_complete                                  every member has a usable dose and the requirement list is confirmed
      recorded_requirements_usable_list_not_confirmed every member usable, but the list is not confirmed complete
      route_incomplete                                a member has no usable dose
      route_evidence_invalid                          the evidence no longer matches the record
    Entries that no reviewed route names are unassigned: route association not established, completeness not assessed."""
    ctx = ctx or Context()
    entries = co_component_entries(fields, ctx)
    by_index = {e['index']: e for e in entries}
    routes, assigned = [], set()
    for r in [x for x in ctx.routes if x.get('product') == ctx.product]:
        ok = all(r.get(k) not in (None, '') for k in ('route_id', 'source_file', 'page', 'quote')) and isinstance(r.get('members'), list)
        members = _route_members(r, by_index) if ok else None
        if members is None:
            routes.append(dict(route=r, members=[], state='route_evidence_invalid'))
            continue
        assigned |= {m['index'] for m in members}
        if any(m['state'] != 'required_usable_dose' for m in members):
            state = 'route_incomplete'
        elif r.get('requirement_list_confirmed') is True:
            state = 'route_complete'
        else:
            state = 'recorded_requirements_usable_list_not_confirmed'
        routes.append(dict(route=r, members=members, state=state))
    return routes, [e for e in entries if e['index'] not in assigned], entries


def co_component_outcome(fields, ctx=None):
    """Product-level outcome of the co-component requirement. Met only by (a) an evidenced route that is complete, or
    (b) an explicit, unqualified, applicable statement that no co-component is required and no recorded requirement.
    The count of usable components is reported for information and never establishes completeness."""
    ctx = ctx or Context()
    rid = 'required_co_components'
    routes, unassigned, entries = co_component_routes(fields, ctx)
    usable = [e for e in entries if e['state'] == 'required_usable_dose']
    info = (f'informational only: {len(usable)} of {len(entries)} recorded requirement(s) have a usable dose, which does not '
            'establish the completeness of any route')
    complete = [r for r in routes if r['state'] == 'route_complete']
    if complete:
        r = complete[0]['route']
        return _o(rid, MET, f"route {r['route_id']!r} is complete: every requirement listed for it ({r['source_file']} p.{r['page']}) has "
                  f'a usable dose and the list is confirmed by source review; other routes are assessed separately ({info})',
                  rep=complete[0]['members'][0]['outcome'].representation, basis='mass')
    stmt = fields.get('co_component_requirement_statement')
    if stmt is not None:
        ok, why = explicit_none_required(dict(stmt, quote=stmt.get('quote') or stmt.get('printed_text')) if isinstance(stmt, dict) else stmt)
        if ok and not entries and isinstance(stmt, dict) and stmt.get('status') == 'Reported':
            return _o(rid, MET, 'explicit, unqualified statement in the record that no co-component is required', rep='text')
        if not entries:
            return _o(rid, META, f'co_component_requirement_statement is recorded but is not an explicit, applicable "none required" '
                      f'statement: {why or "it is not status Reported"}')
    full = [x for x in ctx.statements if explicit_none_required(x, ctx.product)[0] and x.get('product') == ctx.product]
    if full and not entries:
        return _o(rid, MET, f"explicit, unqualified statement that no co-component is required, confirmed by source review: "
                  f"{full[0]['source_file']} p.{full[0]['page']}", rep='text')
    if entries:
        if not usable:
            bad = [e for e in entries if e['state'] == 'required_dose_not_usable']
            if bad:
                o = bad[0]['outcome']
                return o._replace(requirement=rid, reason=f'{len(entries)} requirement(s) recorded, none with a usable dose, so no route '
                                  f'that includes them can be complete ({o.reason})')
            return _o(rid, ABSENT, f'{len(entries)} requirement(s) recorded, none with a dose: no route that includes them can be complete '
                      '(the requirement is recorded; its dose is not)')
        if unassigned or not routes:
            return _o(rid, ROUTE, f'route association not established by reviewed evidence for {len(unassigned)} of {len(entries)} recorded '
                      f'requirement(s): the completeness of a route is not assessed ({info})')
        inc = [r for r in routes if r['state'] == 'route_incomplete']
        if inc:
            return _o(rid, ABSENT, f"route {inc[0]['route']['route_id']!r} is incomplete: a requirement listed for it has no usable dose; "
                      f'no evidenced route is complete ({info})')
        return _o(rid, ROUTE, f'no evidenced route is complete: the requirement list of each route is not confirmed by source review, or its '
                  f'evidence no longer matches the record ({info})')
    part = [x for x in ctx.statements if x.get('product') == ctx.product and x.get('kind') == 'none_required']
    if part:
        x = part[0]
        return _o(rid, UNKNOWN, f"no requirement is recorded; a supplier statement covers {x.get('scope')} only"
                  + (f" and is qualified ({x.get('qualification')})" if x.get('qualification') else '')
                  + f" ({x.get('source_file')} p.{x.get('page')}); whether other co-components are required is not established")
    return _o(rid, UNKNOWN, 'no co-component requirement is recorded in the product record and no explicit statement that none is '
              'required is recorded. This describes the record, not the supplier documents: what was inspected is in '
              'co_component_routes.csv')


''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
import ast
ast.parse(s)
print('ok')
