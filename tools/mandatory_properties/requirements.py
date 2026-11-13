"""Mandatory Tier 1 requirements (Rule 3) and the checks that decide whether a product meets them (read-only).

Authority for every requirement, and the decisions still open, are in
docs/data_policy_mandatory_review/requirements_review.md. Sources:
  - Smart_Formulator_Minimum_Property_Set.pdf (in the source archive), slides 2-4;
  - Property_Glossary.docx (tiers; "Never infer absent facts"; "A component response needs reference oil, dose and method");
  - json_templates/*.json (field paths and tier numbers).

Every requirement check returns an Outcome with one category (CATEGORIES). Only MET and NOT_APPLICABLE (an approved
applicability rule; none is approved yet) satisfy a requirement. The categories separate an absent value from documented
information that is not (yet) usable, so an unmet requirement is not reported as an absent property:

  absent                              no value is recorded (status Missing, or no entry)
  bound_or_range_needs_assessment     a reported bound, range or direction-less specification value: documented
                                      information, never converted to an exact value; whether it serves the intended use
                                      is a provisional, use-specific decision (REPRESENTATIONS)
  missing_unit_condition_provenance   value present, but its unit, mass basis, test/reference condition or source is not
  invalid_value                       recorded value is not a valid measurement (non-finite, boolean, reversed range,
                                      unsupported or conflicting qualifier, value outside its own recorded range)
  invalid_or_unreproducible_calculation  a Calculated value that no registered check reproduces from traceable inputs
  unresolved_applicability            whether or how the requirement applies is not established
  requirement_unknown                 whether a requirement exists is not known: none is recorded in the record and no
                                      explicit statement says that none is required. This is a statement about the
                                      record; it does not say that the supplier documents are silent
  unresolved_route_association        co-component requirements are recorded, but which route each belongs to is not
                                      established by reviewed evidence, so the completeness of a route is not assessed
  unresolved_source_selection         a value exists, but which source supplies it is pending (Rule 1)

tier1_complete = every blocking (mandatory Tier 1) requirement is satisfied (met, or not applicable under an approved
rule) under REQUIREMENTS_VERSION. formulation_eligible = tier1_complete; no other eligibility gate exists (a new gate
needs a documented authority, requirements_review.md). These two meanings are unchanged since version .3.

Policies approved on 2026-11-11 (version .4; corrected in .5 the same day; requirements_review.md section 4a):
  1. ranges and bounds   a valid, sourced range or bound is documented information, never an absent value, and never
                         replaced by an invented point. It does not satisfy a requirement that needs a point value.
  2. co-components       completeness is assessed per evidenced route: every requirement that applies to the route
                         must have a usable dose, and the route's requirement list must be confirmed by source review.
                         One usable component never completes a route that needs others. Routes are independent, and
                         a component may belong to several. Route evidence is bound to the complete input records by
                         fingerprint: a relevant change makes it stale until re-reviewed. "None required" needs an
                         explicit reviewed assessment (meaning, scope, product, conditions, qualification).
  3. percentage basis    mass, volume or unspecified, established from the unit or from reviewed source evidence
                         (heading, footnote, document-wide convention). An unspecified or volume percentage does not
                         satisfy a wt.% requirement. No volume-to-mass conversion is registered or used.
  4. applicability       a Not Required / Not Applicable label counts only under a rule approved for the product
                         class, requirement and task (APPROVED_APPLICABILITY_RULES; empty). Missing is never N/A.
Evidence documentation, value selection, value form, percentage basis and verification status are separate attributes
of each outcome (tools/mandatory_properties/build_readiness.py); none of them changes the two fields above.
Subtype blocks (VM, PPD) are evaluated and reported but are NOT blocking: they are stored in tier 2 / tier 3 files and
the project rule is that missing Tier 2/3 data does not block (decision C in requirements_review.md).

"Eligible" means eligible under these mandatory-data rules only. It is not a statement of chemical suitability,
compatibility or performance.
"""
import hashlib, json, math, re
from collections import namedtuple

REQUIREMENTS_VERSION = 'mandatory-tier1-2026-11-10.6'

MET, NOT_APPLICABLE = 'met', 'not_applicable_approved_rule'
ABSENT = 'absent'
BOUND = 'bound_or_range_needs_assessment'
META = 'missing_unit_condition_provenance'
INVALID = 'invalid_value'
CALC = 'invalid_or_unreproducible_calculation'
APPL = 'unresolved_applicability'
UNKNOWN = 'requirement_unknown'
ROUTE = 'unresolved_route_association'
SEL = 'unresolved_source_selection'
CATEGORIES = [MET, NOT_APPLICABLE, ABSENT, BOUND, META, INVALID, CALC, APPL, UNKNOWN, ROUTE, SEL]
SATISFIED = {MET, NOT_APPLICABLE}
DOCUMENTED = {MET, NOT_APPLICABLE, BOUND, SEL}

# selection_pending is independent of the category: a requirement can have incomplete metadata AND a pending selection
Outcome = namedtuple('Outcome', 'requirement category reason calculated blocking representation basis selection_pending',
                     defaults=('', False))
BASIS_CLASSES = ('mass', 'volume', 'unspecified')
DEFAULT_TASK = 'mandatory_tier1_documentation'

OK_STATUS = ('Reported', 'Calculated')
INAPPLICABLE_STATUS = ('Not Required', 'Not Applicable', 'N/A')
# Applicability rules that have been APPROVED (policy 4 of 2026-11-11). None is approved: the list is empty, and no
# exemption is assumed. A rule is a dict with id, material_class, requirement, task, authority (document and wording)
# and approved (date). It applies only to a value labelled Not Required / Not Applicable, for that product class,
# requirement and task. A Missing value, or a search that found nothing, never becomes "not applicable".
APPROVED_APPLICABILITY_RULES = []
RULE_KEYS = ('id', 'material_class', 'requirement', 'task', 'authority', 'approved')


def approved_rule(rid, ctx=None, rules=None):
    """The approved applicability rule for this requirement, product class and task, or None."""
    rules = APPROVED_APPLICABILITY_RULES if rules is None else rules
    cls = getattr(ctx, 'material_class', None)
    task = getattr(ctx, 'task', None) or DEFAULT_TASK
    for r in rules:
        if all(r.get(k) for k in RULE_KEYS) and r['requirement'] == rid and r['material_class'] == cls and r['task'] == task:
            return r
    return None

# ---------------------------------------------------------------- representations (provisional, use-specific)
# accepted: representations that satisfy the requirement for formulation use. reviewable: documented information that
# needs a use-specific decision (category BOUND). Anything else (text in a numeric field) is invalid.
# Where the source names the representation (treat rate "min / max / typical wt.%"), the rule cites it; the others are
# project interpretations awaiting review (requirements_review.md, decision B-REP).
POINT_ONLY = dict(accepted={'point'}, reviewable={'range', 'lower_bound', 'upper_bound', 'spec_value'},
                  basis='policy 1 of 2026-11-11: documented information; a requirement that needs a point value is not met by a '
                        'range or bound, and no point is derived from it')
DOSE = dict(accepted={'point', 'range'}, reviewable={'lower_bound', 'upper_bound', 'spec_value'},
            basis='source: Minimum Property Set slide 3/4 and glossary, "Treat rate - min / max / typical wt.%"')
TEMPERATURE = dict(accepted={'point', 'range'}, reviewable={'lower_bound', 'upper_bound', 'spec_value'},
                   basis='interpretation: a blend / dissolution temperature can be printed as a range')
REPRESENTATIONS = {
    'kv40': POINT_ONLY, 'kv100': POINT_ONLY, 'viscosity_index': POINT_ONLY, 'density': POINT_ONLY, 'ccs': POINT_ONLY,
    'treat_rate_matrix': DOSE, 'required_co_components': DOSE, 'treat_rate': DOSE, 'vm.treat_range_by_sae_grade': DOSE,
    'ppd.tested_dose_range_wt_pct': DOSE,
    'vm.dissolution_blend_temperature': TEMPERATURE, 'ppd.addition_procedure.blend_temperature_c': TEMPERATURE,
}
DEFAULT_REPRESENTATION = POINT_ONLY

INTERPRETATIONS = [
    ('I-1', '[Approved policy 1, 2026-11-11] Ranges, one-sided bounds and direction-less specification values are '
            'documented information. They are never converted to an exact value, never given an invented midpoint and never '
            'reported as absent. A requirement that needs a point value is not satisfied by them; a calculation may use '
            'them only if its registered method accepts that form (no range-aware method is registered).'),
    ('I-2', 'CCS "vs temperature" is satisfied by at least one CCS value with its test temperature.'),
    ('I-3', 'Component "primary and secondary function": the secondary function is optional; the primary is required.'),
    ('I-4', 'Function-specific markers are required for the functions the slide names (detergent: TBN + Ca or Mg; ZDDP: '
            'P + Zn; molybdenum: Mo). For other functions applicability is unresolved (not assumed inapplicable).'),
    ('I-5', 'VM and PPD subtype blocks are reported but not blocking, because they are stored in tier 2 / tier 3 files and '
            'the project rule says missing Tier 2/3 data does not block. This conflicts with slide 4 ("need response data '
            'on top") and is a decision for the reviewer (decision C).'),
    ('I-6', '[Approved policy 3, 2026-11-11] The basis of a percentage is mass, volume or unspecified. It is established '
            'from the recorded unit or from reviewed source evidence (heading, footnote or explicit document-wide convention) '
            'in treat_rate_basis_evidence.json. An unspecified "%" stays unspecified, and a volume percentage stays volume: '
            'neither satisfies a wt.% requirement. No volume-to-mass conversion is registered or used; volume evidence is '
            'listed separately and never fills a wt.% field.'),
    ('I-7', 'A response is usable only with its reference oil, dose and method (glossary extraction rule). A calculated '
            'value is accepted only if a registered check reproduces it from inputs printed on the cited page and its '
            'conditions match the response record.'),
    ('I-8', '[Approved policy 2, 2026-11-11] Package co-components are assessed per evidenced route. A route is complete '
            'only if every requirement that applies to it has a usable mass-basis dose and its requirement list is confirmed '
            'by source review; one usable component never completes a route that needs others, and routes are independent. '
            'Without reviewed route evidence the association is unresolved and completeness is not assessed. The product-level '
            'requirement is met only by a complete evidenced route or by an explicit, unqualified, applicable statement that '
            'none is required. An empty record is "not recorded", never supplier silence.'),
    ('I-9', '[Approved policy 4, 2026-11-11] A Not Required / Not Applicable label satisfies a requirement only under a rule '
            'approved for the product class, the requirement and the task. No rule is approved. A Missing value or an '
            'unsuccessful search is never treated as not applicable, and no property changes tier.'),
]


# ---------------------------------------------------------------- numeric validation
def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


_LOWER_Q = {'>', '>=', '≥', '⩾', '≮', 'min', 'min.', 'minimum', 'not less than'}
_UPPER_Q = {'<', '<=', '≤', '⩽', '≯', 'max', 'max.', 'maximum', 'not more than'}
_RANGE_Q = {'range', 'min-max', 'min–max'}
_NEUTRAL_Q = {'', '=', '~', '≈', 'typical', 'typ', 'typ.', 'approx', 'approx.', 'approximately', 'about', 'nominal',
              'specification', 'sales specification'}
_POINT_K = {'', 'typical', 'single', 'reported', 'sds reported', 'calculated', 'measured'}
_SPEC_K = {'specification', 'target', 'limit'}
_LOWER_K = {'minimum', 'lower bound', 'lower_bound', 'calculated lower bound', 'lower_bound_exclusive'}
_UPPER_K = {'maximum', 'upper bound', 'upper_bound', 'upper_bound_exclusive', 'upper-bound typical', 'upper limit'}
_RANGE_K = {'range'}
_TEXT_K = re.compile(r'description|classification|designation|composition|reported_description')


def _norm(x):
    return re.sub(r'\s+', ' ', str(x or '').strip().lower())


def representation(vo):
    """(kind, detail) for a numeric value object. kind: point, range, lower_bound, upper_bound, spec_value, absent,
    invalid. Never converts a bound or range to an exact value."""
    if not isinstance(vo, dict):
        return 'absent', 'no value object'
    v, lo, hi = vo.get('value'), vo.get('min'), vo.get('max')
    q, k = _norm(vo.get('qualifier')), _norm(vo.get('value_kind'))
    for name, x in (('value', v), ('min', lo), ('max', hi)):
        if isinstance(x, bool):
            return 'invalid', f'{name} is a boolean, not a measurement'
        if isinstance(x, (int, float)) and not math.isfinite(x):
            return 'invalid', f'{name} is not a finite number ({x!r})'
    if isinstance(v, str) and v.strip():
        return 'invalid', f'non-numeric text {v[:40]!r} in a numeric field'
    if isinstance(v, list):
        if len(v) != 2 or not all(finite(x) for x in v):
            return 'invalid', f'value list {v!r} is not a pair of finite numbers'
        if v[0] > v[1]:
            return 'invalid', f'reversed range {v!r}'
        if (lo is not None and lo != v[0]) or (hi is not None and hi != v[1]):
            return 'invalid', 'value list and min/max disagree'
        lo, hi, v = v[0], v[1], None
        k = k or 'range'
    for name, x in (('min', lo), ('max', hi)):
        if x is not None and not finite(x):
            return 'invalid', f'{name} is not a finite number ({x!r})'
    if finite(lo) and finite(hi) and lo > hi:
        return 'invalid', f'reversed range min {lo} > max {hi}'
    if q in _LOWER_Q:
        qd = 'lower_bound'
    elif q in _UPPER_Q:
        qd = 'upper_bound'
    elif q in _RANGE_Q:
        qd = 'range'
    elif q in _NEUTRAL_Q:
        qd = None
    else:
        return 'invalid', f'unsupported qualifier {vo.get("qualifier")!r}'
    if k in _POINT_K:
        kd = 'point'
    elif k in _SPEC_K:
        kd = 'spec_value'
    elif k in _LOWER_K:
        kd = 'lower_bound'
    elif k in _UPPER_K:
        kd = 'upper_bound'
    elif k in _RANGE_K:
        kd = 'range'
    else:
        return 'invalid', f'unsupported value_kind {vo.get("value_kind")!r}'
    if qd and kd in ('lower_bound', 'upper_bound', 'range') and qd != kd:
        return 'invalid', f'conflicting qualifier {vo.get("qualifier")!r} and value_kind {vo.get("value_kind")!r}'
    kind = qd or kd
    note = (f'qualifier {vo.get("qualifier")!r} makes this a {kind.replace("_", " ")} although value_kind is {vo.get("value_kind")!r}'
            if qd and kd in ('point', 'spec_value') else '')
    if kind == 'point':
        if not finite(v):
            return ('absent', 'no numeric value') if v is None and lo is None and hi is None else (
                'invalid', 'point value kind without a numeric value')
        if (finite(lo) and v < lo) or (finite(hi) and v > hi):
            return 'invalid', f'value {v} outside its own recorded range [{lo}, {hi}]'
        return 'point', ''
    if kind == 'spec_value':
        if finite(lo) and finite(hi):
            return 'range', 'specification range'
        if finite(v) or finite(lo) or finite(hi):
            return 'spec_value', f'specification value without a stated direction (value_kind {vo.get("value_kind")!r})'
        return 'absent', 'no numeric value'
    if kind == 'range':
        if finite(lo) and finite(hi):
            if finite(v) and not lo <= v <= hi:
                return 'invalid', f'value {v} outside its own recorded range [{lo}, {hi}]'
            return 'range', note
        return 'invalid', 'range without both endpoints'
    bound = lo if kind == 'lower_bound' else hi
    other = hi if kind == 'lower_bound' else lo
    if finite(v) and finite(bound) and v != bound:
        return 'invalid', f'{kind.replace("_", " ")} recorded as both {v} (value) and {bound} (min/max)'
    if finite(other):
        return 'invalid', f'{kind.replace("_", " ")} with an opposite limit recorded'
    if not (finite(v) or finite(bound)):
        return 'invalid', f'{kind.replace("_", " ")} without a number'
    return kind, note


def decimals_of(x):
    s = repr(float(x)) if isinstance(x, float) else str(x)
    return len(s.split('.')[1]) if '.' in s and not s.endswith('.0') else 0


# ---------------------------------------------------------------- context
class Context:
    """What a check may consult besides the record: cited page text (traceability), Rule 1 pending fields, and the
    reviewed treat-rate basis evidence. The default context has no page text, so no calculation can be accepted."""

    def __init__(self, page_text=None, pending=None, basis_evidence=None, product=None, material_class=None, task=None,
                 statements=None, routes=None):
        self.page_text = page_text or (lambda f, p: None)
        self.pending = pending or {}
        self.basis_evidence = basis_evidence or []
        self.product = product
        self.material_class = material_class
        self.task = task or DEFAULT_TASK
        self.statements = statements or []   # reviewed co-component statements (co_component_statements.json)
        self.routes = routes or []           # reviewed route evidence (co_component_route_evidence.json)

    def mass_basis(self, path, vo):
        s = vo.get('source') or {}
        for e in self.basis_evidence:
            if (e['product'] == self.product and e['source_file'] == s.get('file') and str(e['page']) == str(s.get('page'))
                    and path.startswith(e['field']) and (not e.get('values') or vo.get('value') in e['values'])):
                return e
        return None


    def basis_of(self, path, vo):
        """(basis class, how it is established) for a percentage value: 'mass', 'volume' or 'unspecified'. The unit as
        recorded comes first; otherwise reviewed evidence for the value, its table or its whole document."""
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


def _o(rid, cat, why='', calc=False, blocking=True, rep=None, basis=''):
    return Outcome(rid, cat, why, calc, blocking, rep, basis, False)


def _provenance(vo):
    s = (vo or {}).get('source') or {}
    f = s.get('file')
    if not f:
        return 'no source file'
    if not str(f).lower().startswith(('http://', 'https://')) and s.get('page') in (None, ''):
        return 'source file without a page'
    return ''


def _status(item, rid, allow_calc, ctx=None):
    """Common status gate for every item (value object, block, claim, formulation entry)."""
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
        return _o(rid, APPL, f'marked {st!r} without an applicability rule approved for this product class, requirement and task')
    if st == 'Calculated' and not allow_calc:
        return _o(rid, CALC, 'status Calculated, but no calculation is defined for this kind of item', calc=True)
    if st not in OK_STATUS:
        return _o(rid, INVALID, f'unsupported status {st!r}')
    return None


def check_value(vo, rid, ctx=None, numeric=True, need_unit=None, need_temp=False, mass_basis=False, calc=None, path=None):
    """Outcome for one value object. calc: a registered calculation check (vo, ctx) -> (ok, reason)."""
    ctx = ctx or Context()
    gate = _status(vo, rid, allow_calc=True, ctx=ctx)
    if gate:
        return gate
    need_unit = numeric if need_unit is None else need_unit
    is_calc = vo.get('status') == 'Calculated'
    if is_calc:
        if calc is None:
            return _o(rid, CALC, 'calculated, but no registered check can reproduce this calculation', calc=True)
        ok, why = calc(vo, ctx)
        if not ok:
            return _o(rid, CALC, why, calc=True)
    if not numeric:
        v = vo.get('value')
        if isinstance(v, (bool, int, float)) or not (isinstance(v, str) and v.strip()):
            if not _structured(vo):
                return _o(rid, INVALID if v is not None else ABSENT,
                          'no text value recorded' if v is None else f'value {v!r} is not a text value')
        why = _provenance(vo)
        return _o(rid, META, why) if why else _o(rid, MET, '', is_calc, rep='text')
    rep, detail = representation(vo)
    if rep == 'absent':
        return _o(rid, INVALID, f'status {vo.get("status")} but {detail}')
    if rep == 'invalid':
        return _o(rid, INVALID, detail, is_calc)
    if need_unit and not vo.get('unit'):
        return _o(rid, META, 'unit not recorded', is_calc, rep=rep)
    basis = ''
    if mass_basis:
        basis, how = ctx.basis_of(path or rid, vo)
        if basis == 'volume':
            return _o(rid, META, f'volume basis ({how}): not usable where wt.% is required; no volume-to-mass conversion is '
                      'registered', is_calc, rep=rep, basis=basis)
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
    return _o(rid, MET, detail, is_calc, rep=rep, basis=basis)


def _structured(n):
    """A non-value-object block (lists of groups, limits, ...) carries content."""
    if not isinstance(n, dict):
        return False
    for k, v in n.items():
        if k in ('status', 'source', 'notes', 'unit', 'value_final', 'unit_final', 'min_final', 'max_final', 'integration_flags',
                 'resolution', 'calculation_note', 'printed_text', 'value_kind', 'method', 'basis'):
            continue
        if isinstance(v, list) and any(x not in (None, '', {}) for x in v):
            return True
        if isinstance(v, dict) and _structured(v):
            return True
        if isinstance(v, str) and v.strip():
            return True
        if finite(v):
            return True
    return False


def check_block(n, rid, ctx=None):
    gate = _status(n, rid, allow_calc=False, ctx=ctx)
    if gate:
        return gate
    if not (isinstance(n.get('value'), str) and n['value'].strip()) and not _structured(n):
        return _o(rid, INVALID, f'status {n.get("status")} but the block is empty')
    why = _provenance(n)
    return _o(rid, META, why) if why else _o(rid, MET)


# ---------------------------------------------------------------- registered calculation checks
_NUM = r'(-?\d+(?:\.\d+)?)'
_DKV = re.compile(r'KV100 at ' + _NUM + r'\s*%\s*\(' + _NUM + r'\)\s*-\s*KV100 at 0\s*%\s*\(' + _NUM + r'\)\s*in\s*(.+?)\s*=\s*' + _NUM)
_LOSS = re.compile(r'\(\s*' + _NUM + r'\s*-\s*' + _NUM + r'\s*\)\s*/\s*' + _NUM + r'\s*x\s*100\s*=\s*' + _NUM)
_SSI = re.compile(r'\(\s*' + _NUM + r'\s*-\s*' + _NUM + r'\s*\)\s*/\s*\(\s*' + _NUM + r'\s*-\s*' + _NUM + r'\s*\)\s*x\s*100\s*=\s*' + _NUM)
_KV_UNITS = re.compile(r'mm2/s|mm²/s|cst', re.I)


def _same_oil(a, b):
    n = lambda x: re.sub(r'[\s#]+', '', str(x or '')).lower()
    return n(a) == n(b) and n(a) != ''


def _result_matches(stored, recomputed, stated):
    if not finite(stored):
        return False, f'stored value {stored!r} is not a finite number'
    tol = 0.5 * 10 ** (-decimals_of(stored)) + 1e-9
    if abs(stored - stated) > 1e-9:
        return False, f'stored value {stored} differs from the result stated in the calculation note ({stated})'
    if abs(stored - recomputed) > tol:
        return False, f'stored value {stored} does not reproduce the recomputed result {recomputed:.6g}'
    return True, ''


def _inputs_on_page(vo, ctx, numbers):
    s = vo.get('source') or {}
    if _provenance(vo):
        return False, f'calculation inputs not traceable ({_provenance(vo)})'
    text = ctx.page_text(s.get('file'), s.get('page'))
    if not text:
        return False, f'calculation inputs cannot be verified: no text for {s.get("file")} p.{s.get("page")}'
    flat = text.replace(',', '.')
    missing = [x for x in numbers if not re.search(r'(?<![\d.])' + re.escape(x) + r'(?![\d])', flat)]
    if missing:
        return False, f'input value(s) {", ".join(missing)} not found on {s.get("file")} p.{s.get("page")}'
    return True, ''


def calc_delta_kv100(entry):
    """ΔKV100 = KV100(dose) - KV100(0 %) in the named reference oil, matched to the response record."""
    def check(vo, ctx):
        m = _DKV.search(str(vo.get('calculation_note') or ''))
        if not m:
            return False, 'calculation note does not state the inputs as "KV100 at d% (a) - KV100 at 0% (b) in <oil> = r"'
        dose, kv_d, kv_0, oil, res = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        if not finite(entry.get('dose_wt_pct')) or abs(float(dose) - entry['dose_wt_pct']) > 1e-9:
            return False, f'dose in the calculation ({dose} %) differs from the response record ({entry.get("dose_wt_pct")!r})'
        if not _same_oil(oil, entry.get('reference_oil')):
            return False, f'reference oil in the calculation ({oil!r}) differs from the response record ({entry.get("reference_oil")!r})'
        if entry.get('usable') is False:
            return False, 'the response record is marked usable: false'
        if not entry.get('method'):
            return False, 'test method not recorded on the response (glossary: a response needs reference oil, dose and method)'
        if vo.get('test_temperature_c') != 100:
            return False, 'test temperature of ΔKV100 is not 100 °C'
        if not _KV_UNITS.search(str(vo.get('unit') or '')):
            return False, f'result unit {vo.get("unit")!r} is not a kinematic-viscosity unit'
        if not _KV_UNITS.search(str(vo.get('printed_text') or '')):
            return False, 'input viscosity unit as printed is not an established kinematic-viscosity unit'
        ok, why = _result_matches(vo.get('value'), float(kv_d) - float(kv_0), float(res))
        if not ok:
            return False, why
        return _inputs_on_page(vo, ctx, [kv_d, kv_0])
    return check


def index_kind(index_type):
    """'viscosity_loss', 'ssi' or None, from the recorded index type wording ('no SSI printed' is not an SSI)."""
    t = str(index_type or '').lower()
    if re.search(r'viscosity\s+loss|% *loss', t):
        return 'viscosity_loss'
    if re.search(r'\bno\s+p?ssi\b', t):
        return None
    if re.search(r'\bp?ssi\b|shear\s+stability\s+index', t):
        return 'ssi'
    return None


def calc_shear_index(entry):
    """Shear stability: SSI = (V0 - Vs) / (V0 - Vb) x 100 (needs the base-oil viscosity Vb). A % viscosity loss,
    (V0 - Vs) / V0 x 100, is a different index and does not satisfy an SSI/PSSI requirement."""
    def check(vo, ctx):
        idx = str(entry.get('index_type') or '').lower()
        note = str(vo.get('calculation_note') or '')
        if not idx:
            return False, 'index type not recorded'
        if index_kind(idx) != 'ssi':
            return False, f'index type {entry.get("index_type")!r} is not SSI/PSSI, which the requirement names'
        m = _SSI.search(note)
        if not m:
            return False, 'calculation note does not state SSI inputs as "(V0 - Vs) / (V0 - Vb) x 100 = r"'
        v0, vs, v0b, vb, res = (float(x) for x in m.groups())
        if v0b != v0:
            return False, 'SSI formula inputs are inconsistent (V0 differs in numerator and denominator)'
        if v0 - vb == 0:
            return False, 'SSI denominator V0 - Vb is zero'
        if not entry.get('method') or not finite(entry.get('cycle_count')):
            return False, 'method or cycle count not recorded'
        cyc = re.search(r'(\d+)\s*cycles', note)
        if cyc and int(cyc.group(1)) != entry['cycle_count']:
            return False, f'cycle count in the calculation ({cyc.group(1)}) differs from the record ({entry["cycle_count"]})'
        ok, why = _result_matches(vo.get('value'), (v0 - vs) / (v0 - vb) * 100, res)
        if not ok:
            return False, why
        return _inputs_on_page(vo, ctx, [m.group(1), m.group(2), m.group(4)])
    return check


def calc_viscosity_loss(entry):
    """% viscosity loss = (V0 - Vs) / V0 x 100: reproducible on its own; used for reporting, it is not an SSI."""
    def check(vo, ctx):
        m = _LOSS.search(str(vo.get('calculation_note') or ''))
        if not m:
            return False, 'calculation note does not state "(V0 - Vs) / V0 x 100 = r"'
        v0, vs, v0b, res = (float(x) for x in m.groups())
        if v0 != v0b:
            return False, 'formula inputs are inconsistent (V0 differs in numerator and denominator)'
        if v0 == 0:
            return False, 'denominator V0 is zero'
        ok, why = _result_matches(vo.get('value'), (v0 - vs) / v0 * 100, res)
        if not ok:
            return False, why
        return _inputs_on_page(vo, ctx, [m.group(1), m.group(2)])
    return check


# ---------------------------------------------------------------- requirement sets
def _any(rid, entries, fn):
    """At least one entry meets fn. Otherwise the most informative outcome: documented (bound, pending) before
    defective (meta, calc, invalid) before unresolved applicability before absent."""
    outs = [fn(e) for e in (entries or [])]
    for o in outs:
        if o.category in SATISFIED:
            return o._replace(requirement=rid)
    order = [BOUND, SEL, META, CALC, INVALID, APPL, ROUTE, UNKNOWN, ABSENT]
    for cat in order:
        hit = [o for o in outs if o.category == cat]
        if hit:
            return hit[0]._replace(requirement=rid)
    return _o(rid, ABSENT, 'no entries recorded')


def _sel(o, ctx, prop):
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


def base_oil_requirements(files, ctx=None):
    ctx = ctx or Context()
    t1 = files.get(1)
    if t1 is None:
        return [_o('base_oil.tier1', ABSENT, 'no Tier 1 record')]
    f = t1.get('fields', {})
    agc = f.get('api_group_chemistry') or {}
    out = [check_value(agc.get(k), f'api_group_chemistry.{k}', ctx, numeric=False) for k in ('api_group', 'chemistry')]
    for k in ('kv40', 'kv100'):
        out.append(_sel(check_value(f.get(k), k, ctx, need_temp=False), ctx, k))
    out.append(_sel(check_value(f.get('viscosity_index'), 'viscosity_index', ctx, need_unit=False), ctx, 'viscosity_index'))
    out.append(_sel(check_value(f.get('density'), 'density', ctx, need_temp=True), ctx, 'density'))
    ccs = f.get('ccs')
    ccs = ccs if isinstance(ccs, list) else [ccs] if ccs else []
    out.append(_sel(_any('ccs', ccs, lambda e: check_value(e, 'ccs', ctx, need_temp=True)), ctx, 'ccs'))
    return out


CO_STATES = ('required_usable_dose', 'required_dose_not_usable', 'required_dose_not_recorded')
ROUTE_STATES = ('route_complete', 'route_incomplete', 'recorded_requirements_usable_list_not_confirmed', 'route_evidence_stale',
                'route_evidence_invalid', 'route_association_not_established')
REVIEW_VALIDITY = ('current', 'stale_requires_re_review', 'invalid')
COMBINATIONS = ('all', 'one_of', 'unresolved')
ALL_CO = 'all co-components'
DERIVED_KEYS = ('value_final', 'unit_final', 'min_final', 'max_final', 'integration_flags', 'unit_conversion', 'resolution')
_BOUND_PATH = re.compile(r'(required_co_components|treat_rate_matrix)\[(\d+)\]')
_HEDGE = re.compile(r'\b(should|may|might|could|normally|typically|generally|usually|in most cases|unless|except|provided that)\b', re.I)


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


def additive_package_requirements(files, ctx=None):
    ctx = ctx or Context()
    t1 = files.get(1)
    if t1 is None:
        return [_o('additive_package.tier1', ABSENT, 'no Tier 1 record')]
    f = t1.get('fields', {})
    pta = f.get('package_type_application') or {}
    out = [check_value(pta.get(k), f'package_type_application.{k}', ctx, numeric=False) for k in ('package_type', 'intended_service')]

    def entry_check(rid, required):
        def fn(e):
            gate = _status(e, rid, allow_calc=False)
            if gate:
                return gate
            for k in required:
                if not (isinstance(e.get(k), str) and e[k].strip()):
                    return _o(rid, INVALID if e.get(k) not in (None, '') else META, f'{k} not recorded')
            why = _provenance(e)
            return _o(rid, META, why) if why else _o(rid, MET)
        return fn
    out.append(_any('performance_claims', f.get('performance_claims'), entry_check('performance_claims', ('designation', 'claim_type'))))
    out.append(_any('sae_grades_documented', f.get('sae_grades_documented'), entry_check('sae_grades_documented', ('sae_grade',))))
    out.append(_any('treat_rate_matrix', f.get('treat_rate_matrix'), lambda e: check_value(
        (e or {}).get('treat_rate_wt_pct'), 'treat_rate_matrix', ctx, mass_basis=True, path='treat_rate_matrix')))
    for k in ('permitted_base_oils_restrictions', 'route_selector_restrictions'):
        out.append(check_block(f.get(k), k, ctx))

    out.append(co_component_outcome(f, ctx))

    def formulation(e):
        gate = _status(e, 'published_formulations', allow_calc=False)
        if gate:
            return gate
        ing = e.get('ingredients') or []
        if not ing:
            return _o('published_formulations', INVALID, 'no ingredients recorded')
        for i in ing:
            w = (i or {}).get('wt_pct')
            if not (i or {}).get('name') or not finite(w) or w < 0:
                return _o('published_formulations', INVALID, f'ingredient {i!r} lacks a name or a finite, non-negative wt.%')
        total = sum(i['wt_pct'] for i in ing)
        if abs(total - 100.0) > 0.005:
            return _o('published_formulations', INVALID, f'ingredients sum to {round(total, 4)} wt.%, not 100.00')
        if e.get('total_wt_pct') is not None and (not finite(e['total_wt_pct']) or abs(e['total_wt_pct'] - total) > 0.005):
            return _o('published_formulations', INVALID, f'recorded total {e.get("total_wt_pct")!r} differs from the sum {round(total, 4)}')
        res = [check_value((r or {}).get('result'), 'published_formulations.result', ctx) for r in e.get('results') or []]
        if not any(r.category == MET for r in res):
            return _o('published_formulations', ABSENT if not res else res[0].category, 'no measured result recorded for the formulation')
        why = _provenance(e)
        return _o('published_formulations', META, why) if why else _o('published_formulations', MET)
    out.append(_any('published_formulations', f.get('published_formulations'), formulation))
    return out


_DETERGENT = re.compile(r'detergent|sulfonate|sulphonate|phenate|salicylate', re.I)
_ZDDP = re.compile(r'ZDDP|ZDTP|zinc\s+dialkyl|zinc\s+dithiophosphate', re.I)
_MOLY = re.compile(r'molybden|\bmoly\b|MoDTC|MoDTP', re.I)
_VM = re.compile(r'viscosity\s+(index\s+)?(modifier|improver)|\bVII\b|\bVM\b', re.I)
_PPD = re.compile(r'pour\s+point\s+depressant|\bPPD\b', re.I)


def component_function(general, files):
    f = (general or {}).get('fields', {})
    prim = (f.get('function') or {}).get('primary') or {}
    fam = f.get('chemical_family') or {}
    text = ' '.join(str(x.get('value') or '') for x in (prim, fam) if isinstance(x, dict) and x.get('status') in OK_STATUS)
    kinds = set()
    if _VM.search(text) or 'vm' in files:
        kinds.add('vm')
    if _PPD.search(text) or 'ppd' in files:
        kinds.add('ppd')
    for name, rx in (('detergent', _DETERGENT), ('zddp', _ZDDP), ('moly', _MOLY)):
        if rx.search(text):
            kinds.add(name)
    known = isinstance(prim, dict) and prim.get('status') in OK_STATUS and isinstance(prim.get('value'), str) and prim['value'].strip() != ''
    return kinds, known


def _active_basis(o, vo):
    """Glossary: active content "wt.% with basis". Met only if the record names the basis."""
    if o.category != MET:
        return o
    text = ' '.join(str(vo.get(k) or '') for k in ('notes', 'calculation_note', 'printed_text', 'basis'))
    if not re.search(r'basis|as supplied|share|of (the )?product|section 3', text, re.I):
        return o._replace(category=META, reason='basis of the active content not stated (glossary: "wt.% with basis")')
    return o


def additive_component_requirements(files, ctx=None):
    ctx = ctx or Context()
    g = files.get('general')
    if g is None:
        return [_o('general', ABSENT, 'no general block record')]
    f = g.get('fields', {})
    out = [check_value((f.get('function') or {}).get('primary'), 'function.primary', ctx, numeric=False),
           check_value(f.get('chemical_family'), 'chemical_family', ctx, numeric=False),
           _active_basis(check_value(f.get('active_content'), 'active_content', ctx), f.get('active_content') or {}),
           check_value((f.get('carrier') or {}).get('identity'), 'carrier.identity', ctx, numeric=False),
           check_value(f.get('treat_rate'), 'treat_rate', ctx, mass_basis=True, path='treat_rate'),
           check_block(f.get('compatibility_restrictions'), 'compatibility_restrictions')]
    kinds, known = component_function(g, files)
    m = f.get('function_specific_markers') or {}
    if not known:
        out.append(_o('function_specific_markers', APPL, 'applicability cannot be established: the primary function is not recorded'))
    else:
        need = []
        if 'detergent' in kinds:
            need += [('tbn',), ('ca', 'mg')]
        if 'zddp' in kinds:
            need += [('p',), ('zn',)]
        if 'moly' in kinds:
            need.append(('mo',))
        if not need:
            out.append(_o('function_specific_markers', APPL, 'the slide names markers only for detergents, ZDDP and molybdenum '
                          'compounds; whether this function needs one is not stated (I-4)'))
        for alts in need:
            rid = f'function_specific_markers.{"|".join(alts)}'
            out.append(_any(rid, [m.get(k) for k in alts], lambda vo: check_value(vo, rid, ctx)))
    if 'vm' in kinds:
        out += [o._replace(blocking=False) for o in vm_requirements(files.get('vm'), ctx)]
    if 'ppd' in kinds:
        out += [o._replace(blocking=False) for o in ppd_requirements(files.get('ppd'), ctx)]
    return out


def _response(rid, entries, vo_key, calc_factory, ctx, extra=()):
    def one(e):
        e = e or {}
        vo = e.get(vo_key)
        gate = _status(vo, rid, allow_calc=True)
        if gate:
            return gate
        for k in ('reference_oil', 'dose_wt_pct', 'method') + tuple(extra):
            if e.get(k) in (None, ''):
                return _o(rid, META if vo.get('status') != 'Calculated' else CALC, f'{k} not recorded on the response (I-7)',
                          vo.get('status') == 'Calculated')
        if not finite(e.get('dose_wt_pct')):
            return _o(rid, INVALID, f'dose {e.get("dose_wt_pct")!r} is not a finite number')
        if e.get('usable') is False:
            return _o(rid, META, 'the response record is marked usable: false', vo.get('status') == 'Calculated')
        return check_value(vo, rid, ctx, calc=calc_factory(e) if calc_factory else None)
    return _any(rid, entries, one)


def vm_requirements(vm, ctx=None):
    ctx = ctx or Context()
    if vm is None:
        return [_o('vm', ABSENT, 'viscosity modifier: no vm.json subtype record')]
    f = vm.get('fields', {})
    out = []
    pc = f.get('polymer_chemistry') or {}
    gate = _status(pc, 'vm.polymer_chemistry', allow_calc=False)
    if gate:
        out.append(gate)
    elif not (pc.get('type') and pc.get('form')):
        out.append(_o('vm.polymer_chemistry', ABSENT, 'type or form not recorded'))
    else:
        why = _provenance(pc)
        out.append(_o('vm.polymer_chemistry', META, why) if why else _o('vm.polymer_chemistry', MET))
    ap = f.get('active_polymer') or {}
    out.append(check_value(ap.get('wt_pct'), 'vm.active_polymer.wt_pct', ctx))
    ci = ap.get('carrier_identity')
    out.append(_o('vm.active_polymer.carrier_identity', MET if ci else ABSENT, '' if ci else 'not recorded'))
    out.append(_any('vm.treat_range_by_sae_grade', f.get('treat_range_by_sae_grade'), lambda e: check_value(
        (e or {}).get('treat_range_wt_pct'), 'vm.treat_range_by_sae_grade', ctx, mass_basis=True, path='treat_range_by_sae_grade')))
    out.append(_response('vm.thickening_response', f.get('thickening_response'), 'delta_kv100_cst', calc_delta_kv100, ctx))

    def ssi(e):
        e = e or {}
        vo = e.get('value')
        gate = _status(vo, 'vm.shear_stability', allow_calc=True)
        if gate:
            return gate
        if e.get('usable') is False:
            return _o('vm.shear_stability', META, 'the record is marked usable: false', vo.get('status') == 'Calculated')
        if not e.get('method') or not finite(e.get('cycle_count')):
            return _o('vm.shear_stability', CALC if vo.get('status') == 'Calculated' else META, 'method or cycle count not recorded',
                      vo.get('status') == 'Calculated')
        if index_kind(e.get('index_type')) != 'ssi':
            return _o('vm.shear_stability', CALC if vo.get('status') == 'Calculated' else META,
                      f'index type {e.get("index_type")!r} is not SSI/PSSI, which the requirement names', vo.get('status') == 'Calculated')
        return check_value(vo, 'vm.shear_stability', ctx, need_unit=False, calc=calc_shear_index(e))
    out.append(_any('vm.shear_stability', f.get('shear_stability'), ssi))
    psb = f.get('post_shear_blend_behaviour') or {}
    for key, vok in (('post_shear_kv100', 'kv100'), ('hths_150c', 'hths'), ('ccs_impact', 'ccs'), ('mrv_impact', 'mrv'), ('low_temp_gelation', 'gelation')):
        out.append(_response(f'vm.post_shear_blend_behaviour.{key}', [psb.get(key) or {}], vok, None, ctx))
    dbt = f.get('dissolution_blend_temperature') or {}
    out.append(check_value(dbt.get('temperature_c'), 'vm.dissolution_blend_temperature', ctx))
    return out


def ppd_requirements(ppd, ctx=None):
    ctx = ctx or Context()
    if ppd is None:
        return [_o('ppd', ABSENT, 'pour point depressant: no ppd.json subtype record')]
    f = ppd.get('fields', {})
    out = [check_value(f.get('chemistry'), 'ppd.chemistry', ctx, numeric=False),
           check_value(f.get('active_content'), 'ppd.active_content', ctx),
           check_value((f.get('carrier') or {}).get('identity'), 'ppd.carrier.identity', ctx, numeric=False),
           check_value(f.get('tested_dose_range_wt_pct'), 'ppd.tested_dose_range_wt_pct', ctx, mass_basis=True, path='tested_dose_range_wt_pct'),
           _response('ppd.pour_point_response', f.get('pour_point_response'), 'pour_point_change_c', None, ctx)]
    for key in ('mrv', 'yield_stress', 'ccs'):
        out.append(_response(f'ppd.low_temp_response.{key}', f.get('low_temp_response'), key, None, ctx, extra=('test_temperature_c',)))
    out.append(check_block(f.get('compatibility_envelope'), 'ppd.compatibility_envelope'))
    ap = f.get('addition_procedure') or {}
    out.append(_o('ppd.addition_procedure', MET if ap.get('procedure') else ABSENT, '' if ap.get('procedure') else 'procedure not recorded'))
    out.append(check_value(ap.get('blend_temperature_c'), 'ppd.addition_procedure.blend_temperature_c', ctx))
    return out


CHECKERS = {'base_oil': base_oil_requirements, 'additive_package': additive_package_requirements,
            'additive_component': additive_component_requirements}


def summarize(outcomes):
    """(tier1_complete, formulation_eligible) from blocking outcomes: both mean "all mandatory Tier 1 requirements
    satisfied under REQUIREMENTS_VERSION" (the interface meaning agreed for product_eligibility.csv)."""
    complete = all(o.category in SATISFIED for o in outcomes if o.blocking)
    return complete, complete


def documentation_status(outcomes):
    """Companion measure, NOT completeness: every blocking requirement has documented information, even if a range,
    bound or pending source selection keeps it from being satisfied."""
    return all(o.category in DOCUMENTED for o in outcomes if o.blocking)
