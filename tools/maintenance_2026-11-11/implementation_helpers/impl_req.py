R = 'C:\\Users\\windo\\sf-wsA\\'
p = R + 'tools\\mandatory_properties\\requirements.py'
s = open(p, encoding='utf-8').read()


def sub(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


# ---- docstring
sub("""  unresolved_applicability            whether or how the requirement applies is not established
""", """  unresolved_applicability            whether or how the requirement applies is not established
  requirement_unknown                 whether a requirement exists is not known: the supplier documents are silent
                                      (required co-components; silence is never read as "none required")
""")
sub("""tier1_complete = every blocking (mandatory Tier 1) requirement is satisfied (met, or not applicable under an approved
rule) under REQUIREMENTS_VERSION. formulation_eligible = tier1_complete; no other eligibility gate exists (a new gate
needs a documented authority, requirements_review.md). Documentation coverage (documented but unusable information:
bounds/ranges needing assessment, pending source selections) is reported separately (documentation_status), never as
completeness.
""", """tier1_complete = every blocking (mandatory Tier 1) requirement is satisfied (met, or not applicable under an approved
rule) under REQUIREMENTS_VERSION. formulation_eligible = tier1_complete; no other eligibility gate exists (a new gate
needs a documented authority, requirements_review.md). These two meanings are unchanged since version .3.

Policies approved on 2026-11-11 (version .4; requirements_review.md section 4):
  1. ranges and bounds   a valid, sourced range or bound is documented information, never an absent value, and never
                         replaced by an invented point. It does not satisfy a requirement that needs a point value.
  2. co-components       a recorded supplier requirement with a usable dose is met; a recorded requirement without a
                         usable dose leaves its route incomplete; "none required" needs an explicit, applicable
                         statement; silence is requirement_unknown. Route-level detail: build_readiness.py.
  3. percentage basis    mass, volume or unspecified, established from the unit or from reviewed source evidence
                         (heading, footnote, document-wide convention). An unspecified or volume percentage does not
                         satisfy a wt.% requirement; volume is converted only by volume_to_mass_percent().
  4. applicability       a Not Required / Not Applicable label counts only under a rule approved for the product
                         class, requirement and task (APPROVED_APPLICABILITY_RULES; empty). Missing is never N/A.
Evidence documentation, value selection, value form, percentage basis and verification status are separate attributes
of each outcome (tools/mandatory_properties/build_readiness.py); none of them changes the two fields above.
""")
sub("REQUIREMENTS_VERSION = 'mandatory-tier1-2026-11-10.3'", "REQUIREMENTS_VERSION = 'mandatory-tier1-2026-11-10.4'")
sub("""APPL = 'unresolved_applicability'
SEL = 'unresolved_source_selection'
CATEGORIES = [MET, NOT_APPLICABLE, ABSENT, BOUND, META, INVALID, CALC, APPL, SEL]""",
    """APPL = 'unresolved_applicability'
UNKNOWN = 'requirement_unknown'
SEL = 'unresolved_source_selection'
CATEGORIES = [MET, NOT_APPLICABLE, ABSENT, BOUND, META, INVALID, CALC, APPL, UNKNOWN, SEL]""")
sub("""Outcome = namedtuple('Outcome', 'requirement category reason calculated blocking representation')
""", """Outcome = namedtuple('Outcome', 'requirement category reason calculated blocking representation basis', defaults=('',))
BASIS_CLASSES = ('mass', 'volume', 'unspecified')
DEFAULT_TASK = 'mandatory_tier1_documentation'
""")
sub("""# Applicability rules that have been APPROVED. None is approved yet (requirements_review.md, decisions C, D, F).
APPROVED_APPLICABILITY_RULES = {}
""", """# Applicability rules that have been APPROVED (policy 4 of 2026-11-11). None is approved: the list is empty, and no
# exemption is assumed. A rule is a dict with id, material_class, requirement, task, authority (document and wording)
# and approved (date). It applies only to a value labelled Not Required / Not Applicable, for that product class,
# requirement and task. A Missing value, or a search that found nothing, never becomes "not applicable".
APPROVED_APPLICABILITY_RULES = []
RULE_KEYS = ('id', 'material_class', 'requirement', 'task', 'authority', 'approved')


def approved_rule(rid, ctx=None, rules=None):
    \"\"\"The approved applicability rule for this requirement, product class and task, or None.\"\"\"
    rules = APPROVED_APPLICABILITY_RULES if rules is None else rules
    cls = getattr(ctx, 'material_class', None)
    task = getattr(ctx, 'task', None) or DEFAULT_TASK
    for r in rules:
        if all(r.get(k) for k in RULE_KEYS) and r['requirement'] == rid and r['material_class'] == cls and r['task'] == task:
            return r
    return None
""")
sub("""POINT_ONLY = dict(accepted={'point'}, reviewable={'range', 'lower_bound', 'upper_bound', 'spec_value'},
                  basis='interpretation: a formulation calculation needs a point value; ranges and bounds are kept for review')""",
    """POINT_ONLY = dict(accepted={'point'}, reviewable={'range', 'lower_bound', 'upper_bound', 'spec_value'},
                  basis='policy 1 of 2026-11-11: documented information; a requirement that needs a point value is not met by a '
                        'range or bound, and no point is derived from it')""")
sub("""    ('I-1', 'Ranges, one-sided bounds and direction-less specification values are documented information. They are never '
            'converted to an exact value and never rejected as absent; whether they serve a property\\'s intended use is a '
            'provisional, property-specific decision (REPRESENTATIONS). Until decided, the requirement is not satisfied: '
            'the product is not Tier 1 complete; the information is reported in the documentation coverage.'),""",
    """    ('I-1', '[Approved policy 1, 2026-11-11] Ranges, one-sided bounds and direction-less specification values are '
            'documented information. They are never converted to an exact value, never given an invented midpoint and never '
            'reported as absent. A requirement that needs a point value is not satisfied by them; a calculation may use '
            'them only if its registered method accepts that form (no range-aware method is registered).'),""")
sub("""    ('I-6', 'A treat rate or dose must be on a mass basis: stated in the recorded unit (wt.%, mass %) or established from '
            'the cited page (heading or footnote) in treat_rate_basis_evidence.json. A bare "%" without such evidence is '
            'missing its basis; the basis is never guessed.'),""",
    """    ('I-6', '[Approved policy 3, 2026-11-11] The basis of a percentage is mass, volume or unspecified. It is established '
            'from the recorded unit or from reviewed source evidence (heading, footnote or explicit document-wide convention) '
            'in treat_rate_basis_evidence.json. An unspecified "%" stays unspecified, and a volume percentage stays volume: '
            'neither satisfies a wt.% requirement. Volume is converted to mass only by the registered calculation '
            'volume_to_mass_percent with stated density inputs.'),""")
sub("""    ('I-8', 'Package co-component architecture: met by a reported co-component with a mass-basis dose, or by a sourced '
            'statement that no co-component is required (proposed field co_component_requirement_statement; no record '
            'has one yet). Without either, applicability is unresolved; a co-component is never required merely because '
            'the schema cannot say "none".'),""",
    """    ('I-8', '[Approved policy 2, 2026-11-11] Package co-components: the requirement is met by a recorded supplier '
            'requirement with a usable mass-basis dose, or by an explicit, applicable statement that none is required. A '
            'recorded requirement without a usable dose leaves its route incomplete. Silence is "requirement unknown", '
            'never "none required". The product-level outcome says only that at least one recorded requirement is usable; '
            'completeness is assessed per route and condition (co_component_routes.csv), not for formulation in general.'),
    ('I-9', '[Approved policy 4, 2026-11-11] A Not Required / Not Applicable label satisfies a requirement only under a rule '
            'approved for the product class, the requirement and the task. No rule is approved. A Missing value or an '
            'unsuccessful search is never treated as not applicable, and no property changes tier.'),""")

# ---- context
sub("""    def __init__(self, page_text=None, pending=None, basis_evidence=None, product=None):
        self.page_text = page_text or (lambda f, p: None)
        self.pending = pending or {}
        self.basis_evidence = basis_evidence or []
        self.product = product
""", """    def __init__(self, page_text=None, pending=None, basis_evidence=None, product=None, material_class=None, task=None,
                 statements=None):
        self.page_text = page_text or (lambda f, p: None)
        self.pending = pending or {}
        self.basis_evidence = basis_evidence or []
        self.product = product
        self.material_class = material_class
        self.task = task or DEFAULT_TASK
        self.statements = statements or []   # reviewed co-component statements (co_component_statements.json)
""")
sub("""def _o(rid, cat, why='', calc=False, blocking=True, rep=None):
    return Outcome(rid, cat, why, calc, blocking, rep)
""", """    def basis_of(self, path, vo):
        \"\"\"(basis class, how it is established) for a percentage value: 'mass', 'volume' or 'unspecified'. The unit as
        recorded comes first; otherwise reviewed evidence for the value, its table or its whole document.\"\"\"
        return percentage_basis(vo, self.mass_basis(path, vo))


_MASS_UNIT = re.compile(r'wt|mass|weight|m/m|w/w', re.I)
_VOLUME_UNIT = re.compile(r'vol|v/v', re.I)


def percentage_basis(vo, evidence=None):
    u = str((vo or {}).get('unit') or '')
    if _MASS_UNIT.search(u):
        return 'mass', f'recorded unit {u!r}'
    if _VOLUME_UNIT.search(u):
        return 'volume', f'recorded unit {u!r}'
    if evidence:
        b = str(evidence.get('basis') or '').lower()
        cls = 'volume' if _VOLUME_UNIT.search(b) else 'mass' if _MASS_UNIT.search(b) else None
        if cls:
            return cls, (f"reviewed evidence ({evidence.get('evidence_kind') or 'page wording'}, scope "
                         f"{evidence.get('scope') or 'value'}): {evidence.get('source_file')} p.{evidence.get('page')}")
    return 'unspecified', f'unit {u!r} states no basis and no reviewed source evidence establishes one'


def volume_to_mass_percent(vol_pct, component_density, mixture_density, component_density_temp_c, mixture_density_temp_c):
    \"\"\"Mass percentage of a component from its volume percentage: wt.% = vol.% x rho_component / rho_mixture.

    Both densities must be stated, positive, in the same unit and at the same temperature, and vol.% must be a point
    value in [0, 100]. Returns (value, '') or (None, reason). Nothing is assumed: without both densities at one
    temperature there is no conversion. No recorded value needs this calculation at present.\"\"\"
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


def _o(rid, cat, why='', calc=False, blocking=True, rep=None, basis=''):
    return Outcome(rid, cat, why, calc, blocking, rep, basis)
""")

# ---- status gate and applicability
sub("""def _status(item, rid, allow_calc):
    \"\"\"Common status gate for every item (value object, block, claim, formulation entry).\"\"\"
    if not isinstance(item, dict):
        return _o(rid, ABSENT, 'not present in the record')
    st = item.get('status')
    if st in (None, 'Missing'):
        return _o(rid, ABSENT, f'status {st or "not recorded"}')
    if st in INAPPLICABLE_STATUS:
        rule = APPROVED_APPLICABILITY_RULES.get(rid)
        if rule:
            return _o(rid, NOT_APPLICABLE, f'not applicable under approved rule {rule}')
        return _o(rid, APPL, f'marked {st!r} without an approved applicability rule')""",
    """def _status(item, rid, allow_calc, ctx=None):
    \"\"\"Common status gate for every item (value object, block, claim, formulation entry).\"\"\"
    if not isinstance(item, dict):
        return _o(rid, ABSENT, 'not present in the record')
    st = item.get('status')
    if st in (None, 'Missing'):
        # policy 4: a missing value is never "not applicable", whatever rules exist
        return _o(rid, ABSENT, f'status {st or "not recorded"}')
    if st in INAPPLICABLE_STATUS:
        rule = approved_rule(rid.split('[')[0], ctx)
        if rule:
            return _o(rid, NOT_APPLICABLE, f'not applicable under approved rule {rule["id"]} ({rule["authority"]})')
        return _o(rid, APPL, f'marked {st!r} without an applicability rule approved for this product class, requirement and task')""")
sub("""    ctx = ctx or Context()
    gate = _status(vo, rid, allow_calc=True)
    if gate:
        return gate
    need_unit = numeric if need_unit is None else need_unit""",
    """    ctx = ctx or Context()
    gate = _status(vo, rid, allow_calc=True, ctx=ctx)
    if gate:
        return gate
    need_unit = numeric if need_unit is None else need_unit""")
sub("""    if mass_basis and not re.search(r'wt|mass|weight|m/m|w/w', str(vo.get('unit') or ''), re.I):
        ev = ctx.mass_basis(path or rid, vo)
        if not ev:
            return _o(rid, META, f'unit {vo.get("unit")!r} does not state a mass basis and no page evidence establishes one', is_calc, rep=rep)
    if need_temp and not finite(vo.get('test_temperature_c')):
        return _o(rid, META, 'reference/test temperature not recorded', is_calc, rep=rep)
    why = _provenance(vo)
    if why:
        return _o(rid, META, why, is_calc, rep=rep)
    policy = REPRESENTATIONS.get(rid.split('[')[0], DEFAULT_REPRESENTATION)
    if rep not in policy['accepted']:
        return _o(rid, BOUND, f'{rep.replace("_", " ")}{": " + detail if detail else ""} (provisional rule: {policy["basis"]})', is_calc, rep=rep)
    return _o(rid, MET, detail, is_calc, rep=rep)""",
    """    basis = ''
    if mass_basis:
        basis, how = ctx.basis_of(path or rid, vo)
        if basis == 'volume':
            return _o(rid, META, f'volume basis ({how}): not usable where wt.% is required; a conversion needs the registered '
                      'calculation volume_to_mass_percent with stated density inputs', is_calc, rep=rep, basis=basis)
        if basis != 'mass':
            return _o(rid, META, f'percentage basis unspecified: {how}', is_calc, rep=rep, basis=basis)
    if need_temp and not finite(vo.get('test_temperature_c')):
        return _o(rid, META, 'reference/test temperature not recorded', is_calc, rep=rep, basis=basis)
    why = _provenance(vo)
    if why:
        return _o(rid, META, why, is_calc, rep=rep, basis=basis)
    policy = REPRESENTATIONS.get(rid.split('[')[0], DEFAULT_REPRESENTATION)
    if rep not in policy['accepted']:
        return _o(rid, BOUND, f'{rep.replace("_", " ")}{": " + detail if detail else ""} ({policy["basis"]})', is_calc, rep=rep, basis=basis)
    return _o(rid, MET, detail, is_calc, rep=rep, basis=basis)""")
sub("""def check_block(n, rid):
    gate = _status(n, rid, allow_calc=False)""", """def check_block(n, rid, ctx=None):
    gate = _status(n, rid, allow_calc=False, ctx=ctx)""")
sub("""    order = [BOUND, SEL, META, CALC, INVALID, APPL, ABSENT]""", """    order = [BOUND, SEL, META, CALC, INVALID, APPL, UNKNOWN, ABSENT]""")

# ---- co-components
a = s.index("    entries = [e for e in f.get('required_co_components') or [] if isinstance(e, dict) and (e.get('name') or e.get('role'))")
b = s.index("    def formulation(e):")
s = s[:a] + """    out.append(co_component_outcome(f, ctx))

""" + s[b:]
sub("""def additive_package_requirements(files, ctx=None):""", '''CO_STATES = ('required_usable_dose', 'required_dose_not_usable', 'required_dose_not_recorded',
             'none_required_explicit', 'none_required_partial', 'requirement_unknown')


def co_component_entries(fields, ctx=None):
    """Route-level view of the recorded co-component requirements: one dict per recorded entry (role, name, state,
    outcome). The role text carries the supplier's condition (claim, grade, route) as recorded."""
    ctx = ctx or Context()
    rows = []
    for i, e in enumerate(fields.get('required_co_components') or []):
        if not (isinstance(e, dict) and (e.get('name') or e.get('role'))):
            continue
        dose = e.get('dose_wt_pct')
        if not isinstance(dose, dict) or dose.get('status') in (None, 'Missing'):
            o = _o('required_co_components', ABSENT, 'the supplier requirement is recorded, but no dose is recorded for it')
            state = 'required_dose_not_recorded'
        else:
            o = check_value(dose, 'required_co_components', ctx, mass_basis=True, path='required_co_components')
            state = 'required_usable_dose' if o.category == MET else 'required_dose_not_usable'
        rows.append(dict(index=i, role=e.get('role'), name=e.get('name'), dose=dose if isinstance(dose, dict) else {}, state=state, outcome=o))
    return rows


def co_component_statements(ctx):
    """Reviewed supplier statements for this product (co_component_statements.json). A statement counts as "none
    required" for the product only if it is explicit, has its page and quoted wording, and covers all co-components."""
    return [x for x in (ctx.statements if ctx else []) if x.get('product') == ctx.product and x.get('kind') == 'none_required'
            and x.get('source_file') and x.get('page') not in (None, '') and str(x.get('quote') or '').strip()]


def co_component_outcome(fields, ctx=None):
    """Product-level outcome of the co-component requirement (policy 2). It keeps the earlier meaning: met when at
    least one recorded supplier requirement has a usable dose, or when an explicit statement says none is required.
    It does not say that every route is complete: route-level states are in co_component_entries()."""
    ctx = ctx or Context()
    rid = 'required_co_components'
    rows = co_component_entries(fields, ctx)
    usable = [r for r in rows if r['state'] == 'required_usable_dose']
    if usable:
        o = usable[0]['outcome']
        note = (f'{len(usable)} of {len(rows)} recorded co-component requirement(s) have a usable dose; completeness is per route '
                'and condition (co_component_routes.csv), not a statement about every route')
        return o._replace(requirement=rid, reason=(o.reason + '; ' if o.reason else '') + note)
    stmt = fields.get('co_component_requirement_statement')
    if not rows and isinstance(stmt, dict) and stmt.get('status') in OK_STATUS:
        return check_value(stmt, rid, ctx, numeric=False)
    full = [x for x in co_component_statements(ctx) if str(x.get('scope') or '').lower() == 'all co-components']
    if not rows and full:
        return _o(rid, MET, f"explicit statement that no co-component is required: {full[0]['source_file']} p.{full[0]['page']}")
    if rows:
        bad = [r for r in rows if r['state'] == 'required_dose_not_usable']
        if bad:
            o = bad[0]['outcome']
            return o._replace(requirement=rid, reason=f'{len(rows)} recorded co-component requirement(s), none with a usable dose: '
                              f'route incomplete ({o.reason})')
        return _o(rid, ABSENT, f'{len(rows)} supplier co-component requirement(s) recorded without a dose: the route is incomplete '
                  '(the requirement is known; its dose is not documented)')
    part = [x for x in co_component_statements(ctx)]
    if part:
        return _o(rid, UNKNOWN, f"a statement covers {part[0].get('scope')} only ({part[0]['source_file']} p.{part[0]['page']}); "
                  'whether other co-components are required is not known')
    return _o(rid, UNKNOWN, 'the supplier documents are silent: no co-component requirement is recorded and no explicit statement '
              'says that none is required (silence is not "none required")')


def additive_package_requirements(files, ctx=None):''')
sub("""    for k in ('permitted_base_oils_restrictions', 'route_selector_restrictions'):
        out.append(check_block(f.get(k), k))""", """    for k in ('permitted_base_oils_restrictions', 'route_selector_restrictions'):
        out.append(check_block(f.get(k), k, ctx))""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
import ast
ast.parse(s)
print('ok')
