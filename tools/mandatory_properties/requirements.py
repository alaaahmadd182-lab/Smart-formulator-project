"""Mandatory Tier 1 requirements (Rule 3) and the checks that decide whether a product meets them (read-only).

Sources of the requirements:
  - Smart_Formulator_Minimum_Property_Set.pdf (in the source archive), slides 2-4: base oils "Tier 1 - blocking, all six
    required"; additive packages "Tier 1 - route-defining ... as blocking as its numbers" (8 items); additive components
    "A - every component" (6 items), "B - viscosity modifier - adds", "C - pour point depressant - adds";
  - Property_Glossary.docx (same tiers; specific gravity is optional and never used as density; never infer absent facts);
  - json_templates/*.json (field paths; base-oil specific_gravity is optional).
Interpretations that are not stated in those documents are listed in INTERPRETATIONS and in
docs/data_policy_mandatory_review/eligibility_interface.md; they need reviewer confirmation.

"Eligible" means eligible under these mandatory-data rules only. It does not mean chemical suitability, compatibility
or proof of performance.
"""
import re

REQUIREMENTS_VERSION = 'mandatory-tier1-2026-11-10'

OK_STATUS = ('Reported', 'Calculated')
INAPPLICABLE_STATUS = ('Not Required', 'Not Applicable', 'N/A')
# Applicability rules that have been APPROVED and may turn a requirement into "not applicable". None is approved yet:
# the 'Not Required' labels on SHELL_RISELLA_X_415/420/430 cite a "proposed project applicability rule", so they do
# not satisfy a requirement.
APPROVED_APPLICABILITY_RULES = {}

INTERPRETATIONS = [
    ('I-1', 'A numeric requirement needs a point value or a two-sided range (min and max). A one-sided bound alone '
            '(e.g. "minimum 4.0") does not satisfy it, because a calculation cannot use it.'),
    ('I-2', 'CCS "vs temperature" is satisfied by at least one CCS value with its test temperature; the slide lists '
            '-15/-20/-25/-30 °C as the possible pairings, not as four required points.'),
    ('I-3', 'Component "primary and secondary function": the secondary function is optional (not every component '
            'has one); the primary function is required.'),
    ('I-4', 'Component function-specific marker: required only for the functions the slide names (detergent: TBN + Ca '
            'or Mg; ZDDP: P + Zn; molybdenum: Mo). For other functions the slide defines no marker, so the item does '
            'not apply (rule CG-6-APPL). If the function itself is missing, applicability cannot be established and '
            'the item is missing.'),
    ('I-5', 'Viscosity modifiers and pour point depressants must also meet their subtype block (slide 4: "VMs and PPDs '
            'stay components, but need response data on top"). The template numbering of vm.json (tier 2) and '
            'ppd.json (tier 3) is file numbering, not a statement that the blocks are optional. Subtype fields that '
            'sit in a non-VM general.json are ignored.'),
    ('I-6', 'A treat rate must be on a stated mass basis (wt.%, wt%, mass %). A bare "%" or "vol.%" does not establish '
            'the wt.% basis the slides require.'),
    ('I-7', 'A response (thickening, pour point, low temperature) is usable only with its reference oil, dose and test '
            'method (slide 4 rule); a calculated response also needs its inputs and arithmetic to check.'),
    ('I-8', 'Package "required VM / PPD / booster architecture" is satisfied by at least one reported co-component. '
            'The schema has no field for a sourced statement that none is required; such a statement would need a '
            'schema decision before it could satisfy the item.'),
]


# ---------------------------------------------------------------- value-object checks
def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def has_text(vo):
    v = vo.get('value') if isinstance(vo, dict) else None
    return v is not None and str(v).strip() != ''


def has_number(vo):
    """Point value or a two-sided range. Zero is a valid value (I-1)."""
    if not isinstance(vo, dict):
        return False, 'no value object'
    v, lo, hi = vo.get('value'), vo.get('min'), vo.get('max')
    q = str(vo.get('qualifier') or '').strip().lower()
    kind = str(vo.get('value_kind') or '').strip().lower()
    bound = re.fullmatch(r'(>|>=|≥|<|<=|≤|min\.?|minimum|max\.?|maximum)', q) or re.search(r'minimum|maximum|lower bound|upper (bound|limit)', kind)
    if isinstance(v, list) and len(v) == 2 and all(_num(x) for x in v):
        return True, ''
    if _num(v) and not bound:
        return True, ''
    if _num(v):
        return False, f'only a one-sided bound is recorded (qualifier {vo.get("qualifier")!r}, value_kind {vo.get("value_kind")!r})'
    if _num(lo) and _num(hi):
        return True, ''
    if _num(lo) or _num(hi):
        return False, 'only a one-sided bound is recorded'
    return False, 'no numeric value'


def traceable(vo):
    s = vo.get('source') or {}
    return bool(s.get('file'))


def _status_check(vo, label):
    """Common status logic. Returns (ok, reason) for the status alone; ok None means 'go on checking content'."""
    if not isinstance(vo, dict):
        return False, f'{label}: not present in the record'
    st = vo.get('status')
    if st in INAPPLICABLE_STATUS:
        rule = APPROVED_APPLICABILITY_RULES.get(label)
        if rule:
            return True, f'{label}: not applicable under approved rule {rule}'
        return False, f'{label}: marked {st!r} without an approved applicability rule'
    if st not in OK_STATUS:
        return False, f'{label}: status {st}'
    return None, ''


def check_value(vo, label, numeric=True, need_unit=None, need_temp=False, unit_pattern=None, calc_check=None):
    """Return (ok, reason, calculated). need_unit defaults to numeric."""
    ok, why = _status_check(vo, label)
    if ok is not None:
        return ok, why, False
    need_unit = numeric if need_unit is None else need_unit
    if numeric:
        good, why = has_number(vo)
        if not good:
            return False, f'{label}: {why}', False
    elif not has_text(vo) and not _structured_content(vo):
        return False, f'{label}: status {vo.get("status")} but no value recorded', False
    if need_unit and not vo.get('unit'):
        return False, f'{label}: unit not recorded', False
    if unit_pattern and vo.get('unit') and not re.search(unit_pattern, str(vo['unit']), re.I):
        return False, f'{label}: unit {vo["unit"]!r} does not establish the required basis', False
    if need_temp and not _num(vo.get('test_temperature_c')):
        return False, f'{label}: reference/test temperature not recorded', False
    if vo.get('status') == 'Calculated':
        if calc_check is None:
            return False, f'{label}: calculated, but no registered check can reproduce the calculation', True
        good, why = calc_check(vo)
        if not good:
            return False, f'{label}: calculated value not accepted ({why})', True
        return True, '', True
    if not traceable(vo):
        return False, f'{label}: reported without a source file', False
    return True, '', False


def _structured_content(n):
    """True when a non-value-object block (lists of groups, limits, ...) carries content."""
    if not isinstance(n, dict):
        return False
    for k, v in n.items():
        if k in ('status', 'source', 'notes', 'unit', 'value_final', 'unit_final', 'min_final', 'max_final', 'integration_flags', 'resolution'):
            continue
        if isinstance(v, list) and any(x not in (None, '', {}) for x in v):
            return True
        if isinstance(v, dict) and k not in ('source',) and _structured_content(v):
            return True
        if isinstance(v, str) and v.strip() and k not in ('calculation_note', 'printed_text', 'value_kind', 'method', 'basis'):
            return True
        if _num(v):
            return True
    return False


def check_block(n, label):
    """A restrictions-type block (status + lists + source)."""
    ok, why = _status_check(n, label)
    if ok is not None:
        return ok, why, False
    if not (has_text(n) or _structured_content(n)):
        return False, f'{label}: status {n.get("status")} but the block is empty', False
    if not traceable(n):
        return False, f'{label}: reported without a source file', False
    return True, '', False


# ---------------------------------------------------------------- registered calculation checks (I-7)
_NUM = r'(-?\d+(?:\.\d+)?)'
_DKV = re.compile(r'=\s*KV100 at ' + _NUM + r'%\s*\(' + _NUM + r'\)\s*-\s*KV100 at 0%\s*\(' + _NUM + r'\)\s*in\s*(.+?)\s*=\s*' + _NUM)
_SSI = re.compile(r'\(\s*' + _NUM + r'\s*-\s*' + _NUM + r'\s*\)\s*/\s*' + _NUM + r'\s*x\s*100\s*=\s*' + _NUM)


def calc_delta_kv100(entry):
    """ΔKV100 = KV100(dose) - KV100(0) in a named oil: inputs, arithmetic and method must all be checkable."""
    def check(vo):
        m = _DKV.search(str(vo.get('calculation_note') or ''))
        if not m:
            return False, 'calculation note does not state the inputs in a checkable form'
        dose, kv_d, kv_0, oil, res = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4), float(m.group(5))
        if abs((kv_d - kv_0) - res) > 0.006 or not _num(vo.get('value')) or abs(vo['value'] - res) > 1e-9:
            return False, 'arithmetic does not reproduce the recorded value'
        if not traceable(vo):
            return False, 'inputs have no source file'
        if not entry.get('reference_oil') or entry.get('dose_wt_pct') is None:
            return False, 'reference oil or dose not recorded on the response entry'
        if not entry.get('method'):
            return False, 'test method not recorded (slide 4: a response without its method is not usable)'
        return True, ''
    return check


def calc_shear_loss(entry):
    def check(vo):
        m = _SSI.search(str(vo.get('calculation_note') or ''))
        if not m:
            return False, 'calculation note does not state the inputs in a checkable form'
        a, b, c, res = (float(x) for x in m.groups())
        if a != c or abs((a - b) / a * 100 - res) > 0.006:
            return False, 'arithmetic does not reproduce the recorded value'
        if not entry.get('method') or not entry.get('cycle_count'):
            return False, 'method or cycle count not recorded'
        if not entry.get('index_type'):
            return False, 'index type (SSI/PSSI/viscosity loss) not recorded'
        return True, ''
    return check


# ---------------------------------------------------------------- requirement sets
def _any(entries, fn):
    """At least one list entry satisfies fn; returns (ok, first reason, calculated)."""
    reasons, calc = [], False
    for e in entries or []:
        ok, why, c = fn(e)
        if ok:
            return True, '', c
        calc = calc or c
        if why:
            reasons.append(why)
    return False, (reasons[0] if reasons else 'no entries recorded'), calc


def base_oil_requirements(files):
    t1 = files.get(1)
    if t1 is None:
        return [('base_oil.tier1', False, 'no Tier 1 record', False)]
    f = t1.get('fields', {})
    agc = f.get('api_group_chemistry') or {}
    out = []
    for key in ('api_group', 'chemistry'):
        ok, why, c = check_value(agc.get(key), f'api_group_chemistry.{key}', numeric=False)
        out.append((f'api_group_chemistry.{key}', ok, why, c))
    for key in ('kv40', 'kv100'):
        ok, why, c = check_value(f.get(key), key, numeric=True)
        out.append((key, ok, why, c))
    ok, why, c = check_value(f.get('viscosity_index'), 'viscosity_index', numeric=True, need_unit=False)
    out.append(('viscosity_index', ok, why, c))
    ok, why, c = check_value(f.get('density'), 'density', numeric=True, need_temp=True)
    out.append(('density', ok, why, c))
    ccs = f.get('ccs')
    ok, why, c = _any(ccs if isinstance(ccs, list) else [ccs] if ccs else [],
                      lambda e: check_value(e, 'ccs', numeric=True, need_temp=True))
    out.append(('ccs', ok, why if not ok else '', c))
    return out


def additive_package_requirements(files):
    t1 = files.get(1)
    if t1 is None:
        return [('additive_package.tier1', False, 'no Tier 1 record', False)]
    f = t1.get('fields', {})
    pta = f.get('package_type_application') or {}
    out = []
    for key in ('package_type', 'intended_service'):
        ok, why, c = check_value(pta.get(key), f'package_type_application.{key}', numeric=False)
        out.append((f'package_type_application.{key}', ok, why, c))

    def claim(e):
        ok, why = _status_check(e, 'performance_claims')
        if ok is not None:
            return ok, why, False
        if not e.get('designation'):
            return False, 'performance_claims: entry without a designation', False
        if not e.get('claim_type'):
            return False, 'performance_claims: claim semantics (claim_type) not recorded', False
        return (True, '', False) if traceable(e) else (False, 'performance_claims: no source file', False)
    out.append(('performance_claims',) + _any(f.get('performance_claims'), claim))

    def sae(e):
        ok, why = _status_check(e, 'sae_grades_documented')
        if ok is not None:
            return ok, why, False
        if not e.get('sae_grade'):
            return False, 'sae_grades_documented: entry without a grade', False
        return (True, '', False) if traceable(e) else (False, 'sae_grades_documented: no source file', False)
    out.append(('sae_grades_documented',) + _any(f.get('sae_grades_documented'), sae))

    out.append(('treat_rate_matrix',) + _any(f.get('treat_rate_matrix'), lambda e: check_value(
        (e or {}).get('treat_rate_wt_pct'), 'treat_rate_matrix', numeric=True, unit_pattern=r'wt|mass')))
    for key in ('permitted_base_oils_restrictions', 'route_selector_restrictions'):
        out.append((key,) + check_block(f.get(key), key))

    def coc(e):
        if not isinstance(e, dict):
            return False, 'required_co_components: no entry', False
        if not (e.get('name') or e.get('role')):
            return False, 'required_co_components: entry without a name or role', False
        good, why2, c = check_value(e.get('dose_wt_pct'), 'required_co_components.dose_wt_pct', numeric=True, unit_pattern=r'wt|mass')
        return good, why2, c
    out.append(('required_co_components',) + _any(f.get('required_co_components'), coc))

    def formulation(e):
        ok, why = _status_check(e, 'published_formulations')
        if ok is not None:
            return ok, why, False
        ing = [i for i in e.get('ingredients') or [] if i.get('name') and _num(i.get('wt_pct'))]
        if not ing:
            return False, 'published_formulations: no ingredients with wt.%', False
        total = round(sum(i['wt_pct'] for i in ing), 4)
        if abs(total - 100.0) > 0.005:
            return False, f'published_formulations: ingredients sum to {total} wt.%, not 100.00', False
        return (True, '', False) if traceable(e) else (False, 'published_formulations: no source file', False)
    out.append(('published_formulations',) + _any(f.get('published_formulations'), formulation))
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
    if _DETERGENT.search(text):
        kinds.add('detergent')
    if _ZDDP.search(text):
        kinds.add('zddp')
    if _MOLY.search(text):
        kinds.add('moly')
    known = isinstance(prim, dict) and prim.get('status') in OK_STATUS and has_text(prim)
    return kinds, known


def additive_component_requirements(files):
    g = files.get('general')
    if g is None:
        return [('general', False, 'no general block record', False)]
    f = g.get('fields', {})
    out = []
    fn = f.get('function') or {}
    out.append(('function.primary',) + check_value(fn.get('primary'), 'function.primary', numeric=False))
    out.append(('chemical_family',) + check_value(f.get('chemical_family'), 'chemical_family', numeric=False))
    out.append(('active_content',) + check_value(f.get('active_content'), 'active_content', numeric=True))
    carrier = f.get('carrier') or {}
    out.append(('carrier.identity',) + check_value(carrier.get('identity'), 'carrier.identity', numeric=False))
    out.append(('treat_rate',) + check_value(f.get('treat_rate'), 'treat_rate', numeric=True, unit_pattern=r'wt|mass'))
    out.append(('compatibility_restrictions',) + check_block(f.get('compatibility_restrictions'), 'compatibility_restrictions'))
    kinds, known = component_function(g, files)
    m = f.get('function_specific_markers') or {}
    if not known:
        out.append(('function_specific_markers', False, 'function_specific_markers: applicability cannot be established because the primary function is missing', False))
    else:
        need = []
        if 'detergent' in kinds:
            need += [('tbn',), ('ca', 'mg')]
        if 'zddp' in kinds:
            need += [('p',), ('zn',)]
        if 'moly' in kinds:
            need.append(('mo',))
        if not need:
            out.append(('function_specific_markers', True, 'not applicable: no marker defined for this function (rule CG-6-APPL, I-4)', False))
        for alts in need:
            res = [check_value(m.get(k), f'function_specific_markers.{k}', numeric=True) for k in alts]
            hit = [r for r in res if r[0]]
            out.append((f'function_specific_markers.{"|".join(alts)}', bool(hit), '' if hit else res[0][1], any(r[2] for r in hit or res)))
    if 'vm' in kinds:
        out += vm_requirements(files.get('vm'))
    if 'ppd' in kinds:
        out += ppd_requirements(files.get('ppd'))
    return out


def _response(entries, label, vo_key, calc_factory, extra=()):
    def one(e):
        e = e or {}
        vo = e.get(vo_key)
        for k in ('reference_oil', 'dose_wt_pct', 'method') + tuple(extra):
            if e.get(k) in (None, ''):
                ok, why = _status_check(vo, label)
                if ok is False:
                    return False, why, False
                return False, f'{label}: {k} not recorded (I-7)', (vo or {}).get('status') == 'Calculated'
        return check_value(vo, label, numeric=True, calc_check=calc_factory(e) if calc_factory else None)
    return _any(entries, one)


def vm_requirements(vm):
    if vm is None:
        return [('vm', False, 'viscosity modifier: no vm.json subtype record (I-5)', False)]
    f = vm.get('fields', {})
    out = []
    pc = f.get('polymer_chemistry') or {}
    ok, why = _status_check(pc, 'vm.polymer_chemistry')
    if ok is None:
        ok, why = (bool(pc.get('type')) and bool(pc.get('form'))), 'vm.polymer_chemistry: type or form not recorded'
        ok = ok and traceable(pc)
        why = '' if ok else why
    out.append(('vm.polymer_chemistry', ok, why, False))
    ap = f.get('active_polymer') or {}
    out.append(('vm.active_polymer.wt_pct',) + check_value(ap.get('wt_pct'), 'vm.active_polymer.wt_pct', numeric=True))
    ci = ap.get('carrier_identity')
    out.append(('vm.active_polymer.carrier_identity', bool(ci), '' if ci else 'vm.active_polymer.carrier_identity: not recorded', False))
    out.append(('vm.treat_range_by_sae_grade',) + _any(f.get('treat_range_by_sae_grade'), lambda e: check_value(
        (e or {}).get('treat_range_wt_pct'), 'vm.treat_range_by_sae_grade', numeric=True, unit_pattern=r'wt|mass')))
    out.append(('vm.thickening_response',) + _response(f.get('thickening_response'), 'vm.thickening_response', 'delta_kv100_cst', calc_delta_kv100))
    def ssi(e):
        e = e or {}
        return check_value(e.get('value'), 'vm.shear_stability', numeric=True, need_unit=False, calc_check=calc_shear_loss(e)) \
            if e.get('method') and e.get('cycle_count') else (False, 'vm.shear_stability: method or cycle count not recorded (I-7)',
                                                                (e.get('value') or {}).get('status') == 'Calculated')
    out.append(('vm.shear_stability',) + _any(f.get('shear_stability'), ssi))
    psb = f.get('post_shear_blend_behaviour') or {}
    for key, vok in (('post_shear_kv100', 'kv100'), ('hths_150c', 'hths'), ('ccs_impact', 'ccs'), ('mrv_impact', 'mrv'), ('low_temp_gelation', 'gelation')):
        e = psb.get(key) or {}
        out.append((f'vm.post_shear_blend_behaviour.{key}',) + _response([e], f'vm.post_shear_blend_behaviour.{key}', vok, None))
    dbt = f.get('dissolution_blend_temperature') or {}
    out.append(('vm.dissolution_blend_temperature',) + check_value(dbt.get('temperature_c'), 'vm.dissolution_blend_temperature', numeric=True))
    return out


def ppd_requirements(ppd):
    if ppd is None:
        return [('ppd', False, 'pour point depressant: no ppd.json subtype record (I-5)', False)]
    f = ppd.get('fields', {})
    out = [('ppd.chemistry',) + check_value(f.get('chemistry'), 'ppd.chemistry', numeric=False),
           ('ppd.active_content',) + check_value(f.get('active_content'), 'ppd.active_content', numeric=True),
           ('ppd.carrier.identity',) + check_value((f.get('carrier') or {}).get('identity'), 'ppd.carrier.identity', numeric=False),
           ('ppd.tested_dose_range_wt_pct',) + check_value(f.get('tested_dose_range_wt_pct'), 'ppd.tested_dose_range_wt_pct', numeric=True),
           ('ppd.pour_point_response',) + _response(f.get('pour_point_response'), 'ppd.pour_point_response', 'pour_point_change_c', None)]
    for key in ('mrv', 'yield_stress', 'ccs'):
        out.append((f'ppd.low_temp_response.{key}',) + _response(f.get('low_temp_response'), f'ppd.low_temp_response.{key}', key, None, extra=('test_temperature_c',)))
    out.append(('ppd.compatibility_envelope',) + check_block(f.get('compatibility_envelope'), 'ppd.compatibility_envelope'))
    ap = f.get('addition_procedure') or {}
    out.append(('ppd.addition_procedure', bool(ap.get('procedure')), '' if ap.get('procedure') else 'ppd.addition_procedure: procedure not recorded', False))
    out.append(('ppd.addition_procedure.blend_temperature_c',) + check_value(ap.get('blend_temperature_c'), 'ppd.addition_procedure.blend_temperature_c', numeric=True))
    return out


CHECKERS = {'base_oil': base_oil_requirements, 'additive_package': additive_package_requirements,
            'additive_component': additive_component_requirements}
