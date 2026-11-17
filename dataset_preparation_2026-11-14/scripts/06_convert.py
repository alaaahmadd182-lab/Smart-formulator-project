"""Convert field_evidence CSVs to output JSON for 104 conversion-ready products.

Reads: tables/product_stages.csv, decisions/*.json, field_evidence/*.csv
Writes: json_output/<class_folder>/<SUPPLIER>/<PROD_ID>/<filename>.json

Does NOT touch Products_json. Output folder: dataset_preparation_2026-11-14/json_output/
"""

import csv
import json
import glob
import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent          # dataset_preparation_2026-11-14
PKG_ROOT = ROOT.parent                        # project root
OUT_DIR = ROOT / 'json_output'

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

MISSING_SRC = {'file': None, 'page': None, 'revision_date': None}


def _n(s):
    """Return None for empty / whitespace strings."""
    return s if (s and s.strip()) else None


def _num(s):
    """Coerce a string to int or float; return None if empty."""
    if not s or not s.strip():
        return None
    try:
        f = float(s)
        return int(f) if f == int(f) else f
    except (ValueError, TypeError):
        return _n(s)


def _src(row):
    page = _n(row.get('page', ''))
    if page is not None:
        try:
            page = int(page)
        except (ValueError, TypeError):
            pass
    return {
        'file': _n(row.get('source_file', '')),
        'page': page,
        'revision_date': _n(row.get('revision_date', '')),
    }


def _num_obj(rows, default_unit=None):
    """Build a full numeric value object from a list of evidence rows."""
    rep = [r for r in rows if r['status'] == 'Reported']
    mis = [r for r in rows if r['status'] == 'Missing']
    if rep:
        r = rep[0]
        obj = {
            'value': _num(r.get('value', '')),
            'qualifier': _n(r.get('qualifier', '')),
            'min': _num(r.get('min', '')),
            'max': _num(r.get('max', '')),
            'value_kind': _n(r.get('value_kind', '')),
            'printed_text': _n(r.get('printed_text', '')),
            'unit': _n(r.get('unit', '')) or default_unit,
            'test_temperature_c': _num(r.get('test_temperature_c', '')),
            'method': _n(r.get('method', '')),
            'status': 'Reported',
            'calculation_note': None,
            'source': _src(r),
        }
        if _n(r.get('notes', '')):
            obj['notes'] = r['notes']
        if _n(r.get('basis', '')):
            obj['basis'] = r['basis']
        if len(rep) > 1:
            obj['alternate_entries'] = [_num_obj_alt(a) for a in rep[1:]]
        return obj
    obj = {
        'value': None, 'qualifier': None, 'min': None, 'max': None,
        'value_kind': None, 'printed_text': None,
        'unit': default_unit,
        'test_temperature_c': None, 'method': None,
        'status': 'Missing', 'calculation_note': None,
        'source': dict(MISSING_SRC),
    }
    if mis and _n(mis[0].get('notes', '')):
        obj['calculation_note'] = mis[0]['notes']
    return obj


def _num_obj_alt(r):
    return {
        'value': _num(r.get('value', '')),
        'qualifier': _n(r.get('qualifier', '')),
        'min': _num(r.get('min', '')),
        'max': _num(r.get('max', '')),
        'value_kind': _n(r.get('value_kind', '')),
        'printed_text': _n(r.get('printed_text', '')),
        'unit': _n(r.get('unit', '')),
        'test_temperature_c': _num(r.get('test_temperature_c', '')),
        'method': _n(r.get('method', '')),
        'status': r.get('status', 'Reported'),
        'calculation_note': None,
        'source': _src(r),
        **({'notes': r['notes']} if _n(r.get('notes', '')) else {}),
    }


def _text_obj(rows):
    """Build a text-only value object: {value, status, source}."""
    rep = [r for r in rows if r['status'] == 'Reported']
    mis = [r for r in rows if r['status'] == 'Missing']
    if rep:
        r = rep[0]
        obj = {
            'value': _n(r.get('printed_text', '')),
            'status': 'Reported',
            'source': _src(r),
        }
        if _n(r.get('notes', '')):
            obj['notes'] = r['notes']
        if len(rep) > 1:
            obj['alternate_entries'] = [
                {'value': _n(a.get('printed_text', '')),
                 'status': a.get('status', 'Reported'),
                 'source': _src(a)}
                for a in rep[1:]
            ]
        return obj
    obj = {'value': None, 'status': 'Missing', 'source': dict(MISSING_SRC)}
    if mis and _n(mis[0].get('notes', '')):
        obj['calculation_note'] = mis[0]['notes']
    return obj


def _source_docs(rows):
    """Derive source_documents from unique source files in evidence rows."""
    seen = {}
    for r in rows:
        fname = _n(r.get('source_file', ''))
        if fname and fname not in seen:
            seen[fname] = {
                'file': fname,
                'pages': '',
                'doc_type': _n(r.get('value_class', '')) or '',
                'revision_date': _n(r.get('revision_date', '')) or '',
                'notes': '',
            }
    return list(seen.values())


def _open_questions(nit_rows):
    return [
        {
            'property': r['template'].replace('not_in_template:', ''),
            'printed_text': _n(r.get('printed_text', '')),
            'notes': _n(r.get('notes', '')),
            'source': _src(r),
        }
        for r in nit_rows if r['status'] == 'Reported'
    ]


def _product_block(pk, dec):
    supplier, prod_id = pk.split(':', 1)
    return {
        'product_id': prod_id,
        'material_id': pk,
        'product_name': dec.get('name', ''),
        'supplier': dec.get('supplier', ''),
    }


# ---------------------------------------------------------------------------
# component_general
# ---------------------------------------------------------------------------

def _compat_restr(rows):
    rep = [r for r in rows if r['status'] == 'Reported']
    mis = [r for r in rows if r['status'] == 'Missing']
    obj = {
        'base_oil_groups': [],
        'co_additives': [],
        'seals': [],
        'exclusions': [],
    }
    if rep:
        r = rep[0]
        obj.update({
            'status': 'Reported',
            'notes': _n(r.get('printed_text', '')),
            'source': _src(r),
        })
    else:
        obj.update({'status': 'Missing', 'source': dict(MISSING_SRC)})
        if mis and _n(mis[0].get('notes', '')):
            obj['notes'] = mis[0]['notes']
    return obj


def build_component_general(pk, by_tmpl, dec, nit_rows):
    rows = by_tmpl.get('component_general', [])
    bf = defaultdict(list)
    for r in rows:
        bf[r['field']].append(r)
    return {
        'template_version': '1.1',
        'material_class': 'additive_component',
        'tier': 1,
        'tier_label': 'Every component (general block)',
        'record_id': pk.replace(':', '_'),
        'product': _product_block(pk, dec),
        'source_documents': _source_docs(rows + nit_rows),
        'component_subtype': None,
        'fields': {
            'function': {
                'primary': _text_obj(bf['function.primary']),
                'secondary': _text_obj(bf['function.secondary']),
            },
            'chemical_family': _text_obj(bf['chemical_family']),
            'active_content': _num_obj(bf['active_content'], 'wt.%'),
            'carrier': {
                'identity': _text_obj(bf['carrier.identity']),
                'share_wt_pct': _num_obj(bf['carrier.share_wt_pct'], 'wt.%'),
            },
            'treat_rate': _num_obj(bf['treat_rate'], 'wt.%'),
            'compatibility_restrictions': _compat_restr(bf['compatibility_restrictions']),
            'function_specific_markers': {
                'tbn': _num_obj(bf['function_specific_markers.tbn'], 'mg KOH/g'),
                'ca':  _num_obj(bf['function_specific_markers.ca'],  'wt.%'),
                'mg':  _num_obj(bf['function_specific_markers.mg'],  'wt.%'),
                'p':   _num_obj(bf['function_specific_markers.p'],   'wt.%'),
                'zn':  _num_obj(bf['function_specific_markers.zn'],  'wt.%'),
                'mo':  _num_obj(bf['function_specific_markers.mo'],  'wt.%'),
            },
        },
        'open_questions': _open_questions(nit_rows),
        'conflicts': [],
    }


# ---------------------------------------------------------------------------
# component_vm
# ---------------------------------------------------------------------------

def _by_entry(rows):
    """Return OrderedDict-like list of (entry, [rows]) preserving insertion order."""
    seen = {}
    order = []
    for r in rows:
        e = r.get('entry', '')
        if e not in seen:
            seen[e] = []
            order.append(e)
        seen[e].append(r)
    return [(e, seen[e]) for e in order]


def _shear_stab_items(rows):
    if not rows:
        return [{'index_type': None,
                 'value': _num_obj([], None),
                 'method': None, 'cycle_count': None, 'usable': None}]
    rep = [r for r in rows if r['status'] == 'Reported']
    idx = None
    meth = None
    if rep:
        pt = rep[0].get('printed_text', '').upper()
        if 'SSI' in pt:
            idx = 'SSI'
        elif 'SVI' in pt:
            idx = 'SVI'
        meth = _n(rep[0].get('method', ''))
    return [{'index_type': idx,
             'value': _num_obj(rows, None),
             'method': meth, 'cycle_count': None, 'usable': None}]


def _treat_range_items(rows):
    entries = _by_entry(rows)
    if not entries or (len(entries) == 1 and entries[0][0] == '' and
                       not any(r['status'] == 'Reported' for r in entries[0][1])):
        return [{'sae_grade': None, 'treat_range_wt_pct': _num_obj([], 'wt.%')}]
    result = []
    for entry, erows in entries:
        result.append({
            'sae_grade': entry or None,
            'treat_range_wt_pct': _num_obj(erows, 'wt.%'),
        })
    return result


def _thickening_items(rows):
    entries = _by_entry(rows)
    if not entries or not any(r['status'] == 'Reported' for r in rows):
        return [{'reference_oil': None, 'dose_wt_pct': None,
                 'method': None,
                 'delta_kv100_cst': _num_obj([], 'cSt'), 'usable': None}]
    result = []
    for entry, erows in entries:
        rep = [r for r in erows if r['status'] == 'Reported']
        meth = _n(rep[0].get('method', '')) if rep else None
        result.append({
            'reference_oil': entry or None, 'dose_wt_pct': None,
            'method': meth,
            'delta_kv100_cst': _num_obj(erows, 'cSt'), 'usable': None,
        })
    return result


def _psbb_sub(rows, inner_key):
    rep = [r for r in rows if r['status'] == 'Reported']
    meth = _n(rep[0].get('method', '')) if rep else None
    return {
        'reference_oil': None, 'dose_wt_pct': None,
        'method': meth,
        inner_key: _num_obj(rows, None),
        'usable': None,
    }


def build_component_vm(pk, by_tmpl, dec):
    rows = by_tmpl.get('component_vm', [])
    bf = defaultdict(list)
    for r in rows:
        bf[r['field']].append(r)

    def _plain(field_rows):
        rep = [r for r in field_rows if r['status'] == 'Reported']
        return _n(rep[0].get('printed_text', '')) if rep else None

    return {
        'template_version': '1.1',
        'material_class': 'additive_component',
        'tier': 2,
        'tier_label': 'Viscosity modifier - adds to the general block',
        'record_id': pk.replace(':', '_'),
        'product': _product_block(pk, dec),
        'source_documents': _source_docs(rows),
        'component_subtype': 'VM',
        'fields': {
            'polymer_chemistry': {
                'type': _plain(bf['polymer_chemistry.type']),
                'form': _plain(bf['polymer_chemistry.form']),
            },
            'active_polymer': {
                'wt_pct': _num_obj(bf['active_polymer.wt_pct'], 'wt.%'),
                'carrier_identity': _plain(bf['active_polymer.carrier_identity']),
                'carrier_share_wt_pct': _num_obj(bf['active_polymer.carrier_share_wt_pct'], 'wt.%'),
            },
            'treat_range_by_sae_grade': _treat_range_items(bf['treat_range_by_sae_grade']),
            'thickening_response': _thickening_items(bf['thickening_response']),
            'shear_stability': _shear_stab_items(bf['shear_stability']),
            'post_shear_blend_behaviour': {
                'post_shear_kv100': _psbb_sub(bf['post_shear_blend_behaviour.post_shear_kv100'], 'kv100'),
                'hths_150c':        _psbb_sub(bf['post_shear_blend_behaviour.hths_150c'],        'hths'),
                'ccs_impact':       _psbb_sub(bf['post_shear_blend_behaviour.ccs_impact'],       'ccs'),
                'mrv_impact':       _psbb_sub(bf['post_shear_blend_behaviour.mrv_impact'],       'mrv'),
                'low_temp_gelation':_psbb_sub(bf['post_shear_blend_behaviour.low_temp_gelation'],'gelation'),
            },
            'dissolution_blend_temperature': {
                'temperature_c': _num_obj(bf['dissolution_blend_temperature.temperature_c'], '°C'),
                'procedure': _plain(bf['dissolution_blend_temperature.procedure']),
            },
        },
        'open_questions': [],
        'conflicts': [],
    }


# ---------------------------------------------------------------------------
# component_ppd
# ---------------------------------------------------------------------------

def _ppd_compat_env(rows):
    rep = [r for r in rows if r['status'] == 'Reported']
    mis = [r for r in rows if r['status'] == 'Missing']
    obj = {'base_oils': [], 'wax_systems': []}
    if rep:
        r = rep[0]
        obj.update({'status': 'Reported',
                    'notes': _n(r.get('printed_text', '')),
                    'source': _src(r)})
    else:
        obj.update({'status': 'Missing', 'source': dict(MISSING_SRC)})
        if mis and _n(mis[0].get('notes', '')):
            obj['notes'] = mis[0]['notes']
    return obj


def _pp_response_items(rows):
    entries = _by_entry(rows)
    if not entries or not any(r['status'] == 'Reported' for r in rows):
        return [{'reference_oil': None, 'dose_wt_pct': None, 'method': None,
                 'pour_point_change_c': _num_obj([], '°C'), 'usable': None}]
    result = []
    for entry, erows in entries:
        rep = [r for r in erows if r['status'] == 'Reported']
        meth = _n(rep[0].get('method', '')) if rep else None
        result.append({
            'reference_oil': entry or None, 'dose_wt_pct': None, 'method': meth,
            'pour_point_change_c': _num_obj(erows, '°C'), 'usable': None,
        })
    return result


def _low_temp_items(rows):
    entries = _by_entry(rows)
    if not entries or not any(r['status'] == 'Reported' for r in rows):
        return [{'reference_oil': None, 'dose_wt_pct': None, 'test_temperature_c': None,
                 'mrv': _num_obj([], 'mPa.s'), 'ccs': _num_obj([], 'mPa.s'),
                 'yield_stress': _num_obj([], 'Pa'), 'usable': None}]
    result = []
    for entry, erows in entries:
        result.append({
            'reference_oil': entry or None, 'dose_wt_pct': None, 'test_temperature_c': None,
            'mrv': _num_obj(erows, 'mPa.s'), 'ccs': _num_obj([], 'mPa.s'),
            'yield_stress': _num_obj([], 'Pa'), 'usable': None,
        })
    return result


def build_component_ppd(pk, by_tmpl, dec):
    rows = by_tmpl.get('component_ppd', [])
    bf = defaultdict(list)
    for r in rows:
        bf[r['field']].append(r)

    # addition_procedure: check sub-field rows first, fall back to block row
    ap_proc_rows = bf['addition_procedure.procedure']
    ap_temp_rows = bf['addition_procedure.blend_temperature_c']
    ap_block_rows = bf['addition_procedure']

    if ap_proc_rows or ap_temp_rows:
        rep_proc = [r for r in ap_proc_rows if r['status'] == 'Reported']
        ap_proc = _n(rep_proc[0].get('printed_text', '')) if rep_proc else None
        ap_temp = _num_obj(ap_temp_rows, '°C')
    else:
        ap_proc = None
        ap_temp = _num_obj(ap_block_rows, '°C')

    return {
        'template_version': '1.1',
        'material_class': 'additive_component',
        'tier': 3,
        'tier_label': 'Pour point depressant - adds to the general block',
        'record_id': pk.replace(':', '_'),
        'product': _product_block(pk, dec),
        'source_documents': _source_docs(rows),
        'component_subtype': 'PPD',
        'fields': {
            'chemistry': _text_obj(bf['chemistry']),
            'active_content': _num_obj(bf['active_content'], 'wt.%'),
            'carrier': {
                'identity': _text_obj(bf['carrier.identity']),
                'share_wt_pct': _num_obj(bf['carrier.share_wt_pct'], 'wt.%'),
            },
            'tested_dose_range_wt_pct': _num_obj(bf['tested_dose_range_wt_pct'], 'wt.%'),
            'pour_point_response': _pp_response_items(bf['pour_point_response']),
            'low_temp_response': _low_temp_items(bf['low_temp_response']),
            'compatibility_envelope': _ppd_compat_env(bf['compatibility_envelope']),
            'addition_procedure': {
                'procedure': ap_proc,
                'blend_temperature_c': ap_temp,
            },
        },
        'open_questions': [],
        'conflicts': [],
    }


# ---------------------------------------------------------------------------
# package tier1
# ---------------------------------------------------------------------------

def _pkg_text_field(rows):
    rep = [r for r in rows if r['status'] == 'Reported']
    mis = [r for r in rows if r['status'] == 'Missing']
    if rep:
        r = rep[0]
        obj = {'value': _n(r.get('printed_text', '')), 'status': 'Reported', 'source': _src(r)}
        if _n(r.get('notes', '')):
            obj['notes'] = r['notes']
        return obj
    obj = {'value': None, 'status': 'Missing', 'source': dict(MISSING_SRC)}
    if mis and _n(mis[0].get('notes', '')):
        obj['notes'] = mis[0]['notes']
    return obj


def _performance_claims(rows):
    entries = _by_entry(rows)
    has_rep = any(r['status'] == 'Reported' for r in rows)
    if not has_rep:
        item = {'designation': None, 'claim_type': None, 'scope': None,
                'evidence_class': None, 'status': 'Missing', 'source': dict(MISSING_SRC)}
        mis = [r for r in rows if r['status'] == 'Missing' and _n(r.get('notes', ''))]
        if mis:
            item['notes'] = mis[0]['notes']
        return [item]
    result = []
    for entry, erows in entries:
        rep = [r for r in erows if r['status'] == 'Reported']
        if rep:
            r = rep[0]
            result.append({
                'designation': _n(r.get('printed_text', '')),
                'claim_type': None, 'scope': None,
                'evidence_class': _n(r.get('value_class', '')),
                'status': 'Reported',
                'source': _src(r),
            })
    return result or [{'designation': None, 'claim_type': None, 'scope': None,
                       'evidence_class': None, 'status': 'Missing', 'source': dict(MISSING_SRC)}]


def _sae_grades_docs(rows):
    entries = _by_entry(rows)
    has_rep = any(r['status'] == 'Reported' for r in rows)
    if not has_rep:
        item = {'sae_grade': None, 'status': 'Missing', 'source': dict(MISSING_SRC)}
        mis = [r for r in rows if r['status'] == 'Missing' and _n(r.get('notes', ''))]
        if mis:
            item['notes'] = mis[0]['notes']
        return [item]
    result = []
    for entry, erows in entries:
        rep = [r for r in erows if r['status'] == 'Reported']
        if rep:
            r = rep[0]
            result.append({
                'sae_grade': _n(r.get('printed_text', '')) or entry or None,
                'status': 'Reported',
                'source': _src(r),
            })
    return result


def _treat_rate_matrix(rows):
    entries = _by_entry(rows)
    has_rep = any(r['status'] == 'Reported' for r in rows)
    if not has_rep:
        return [{'claim': None, 'sae_grade': None,
                 'treat_rate_wt_pct': _num_obj([], 'wt.%')}]
    result = []
    for entry, erows in entries:
        rep = [r for r in erows if r['status'] == 'Reported']
        if rep:
            r = rep[0]
            pt = r.get('printed_text', '')
            claim = pt.split('|')[0].strip() if '|' in pt else _n(pt)
            result.append({
                'claim': claim, 'sae_grade': None,
                'treat_rate_wt_pct': _num_obj(erows, 'wt.%'),
            })
    return result or [{'claim': None, 'sae_grade': None,
                       'treat_rate_wt_pct': _num_obj([], 'wt.%')}]


def _restrictions(rows, arr_keys):
    rep = [r for r in rows if r['status'] == 'Reported']
    mis = [r for r in rows if r['status'] == 'Missing']
    obj = {k: [] for k in arr_keys}
    if rep:
        r = rep[0]
        obj.update({'status': 'Reported',
                    'notes': _n(r.get('printed_text', '')),
                    'source': _src(r)})
    else:
        obj.update({'status': 'Missing', 'source': dict(MISSING_SRC)})
        if mis and _n(mis[0].get('notes', '')):
            obj['notes'] = mis[0]['notes']
    return obj


def _required_co_comps(rows):
    entries = _by_entry(rows)
    has_rep = any(r['status'] == 'Reported' for r in rows)
    if not has_rep:
        item = {'role': None, 'name': None, 'dose_wt_pct': _num_obj([], 'wt.%')}
        mis = [r for r in rows if r['status'] == 'Missing' and _n(r.get('notes', ''))]
        if mis:
            item['notes'] = mis[0]['notes']
        return [item]
    result = []
    for entry, erows in entries:
        rep = [r for r in erows if r['status'] == 'Reported']
        if rep:
            r = rep[0]
            result.append({
                'role': None,
                'name': _n(r.get('printed_text', '')),
                'dose_wt_pct': _num_obj(erows, 'wt.%'),
            })
    return result


def _published_formulations(rows):
    entries = _by_entry(rows)
    has_rep = any(r['status'] == 'Reported' for r in rows)
    _missing_form = {
        'formulation_id': None,
        'ingredients': [{'name': None, 'wt_pct': None}],
        'total_wt_pct': None, 'total_check_passed': None, 'results': [],
        'status': 'Missing', 'source': dict(MISSING_SRC),
    }
    if not has_rep:
        item = dict(_missing_form)
        mis = [r for r in rows if r['status'] == 'Missing' and _n(r.get('notes', ''))]
        if mis:
            item['notes'] = mis[0]['notes']
        return [item]
    result = []
    for entry, erows in entries:
        rep = [r for r in erows if r['status'] == 'Reported']
        if rep:
            r = rep[0]
            result.append({
                'formulation_id': entry or None,
                'ingredients': [{'name': _n(r.get('printed_text', '')), 'wt_pct': None}],
                'total_wt_pct': None, 'total_check_passed': None, 'results': [],
                'status': 'Reported', 'source': _src(r),
            })
    return result


def build_package_tier1(pk, by_tmpl, dec, nit_rows):
    rows = by_tmpl.get('package_tier1', [])
    bf = defaultdict(list)
    for r in rows:
        bf[r['field']].append(r)
    return {
        'template_version': '1.1',
        'material_class': 'additive_package',
        'tier': 1,
        'tier_label': 'Route-defining - makes a recipe legitimate or invalid',
        'record_id': pk.replace(':', '_'),
        'product': _product_block(pk, dec),
        'source_documents': _source_docs(rows + nit_rows),
        'fields': {
            'package_type_application': {
                'package_type':     _pkg_text_field(bf['package_type_application.package_type']),
                'intended_service': _pkg_text_field(bf['package_type_application.intended_service']),
            },
            'performance_claims': _performance_claims(bf['performance_claims']),
            'sae_grades_documented': _sae_grades_docs(bf['sae_grades_documented']),
            'permitted_base_oils_restrictions': _restrictions(
                bf['permitted_base_oils_restrictions'],
                ['permitted_api_groups', 'permitted_grades', 'exclusions', 'allowed_combinations']),
            'route_selector_restrictions': _restrictions(
                bf['route_selector_restrictions'],
                ['limits', 'exclusions', 'allowed_combinations']),
            'treat_rate_matrix': _treat_rate_matrix(bf['treat_rate_matrix']),
            'required_co_components': _required_co_comps(bf['required_co_components']),
            'published_formulations': _published_formulations(bf['published_formulations']),
        },
        'open_questions': _open_questions(nit_rows),
        'conflicts': [],
    }


# ---------------------------------------------------------------------------
# package tier2
# ---------------------------------------------------------------------------

def build_package_tier2(pk, by_tmpl, dec, nit_rows):
    rows = by_tmpl.get('package_tier2', [])
    bf = defaultdict(list)
    for r in rows:
        bf[r['field']].append(r)

    sg = _num_obj(bf['specific_gravity'], 'dimensionless')
    sg_rep = [r for r in bf['specific_gravity'] if r['status'] == 'Reported']
    sg['reference_condition'] = _n(sg_rep[0].get('conditions', '')) if sg_rep else None

    fp = _num_obj(bf['flash_point'], '°C')
    fp_rep = [r for r in bf['flash_point'] if r['status'] == 'Reported']
    fp['flash_method'] = _n(fp_rep[0].get('method', '')) if fp_rep else None

    return {
        'template_version': '1.1',
        'material_class': 'additive_package',
        'tier': 2,
        'tier_label': 'Numeric contribution to the finished oil',
        'record_id': pk.replace(':', '_'),
        'product': _product_block(pk, dec),
        'source_documents': _source_docs(rows + nit_rows),
        'fields': {
            'tbn': _num_obj(bf['tbn'], 'mg KOH/g'),
            'sulfated_ash': _num_obj(bf['sulfated_ash'], 'wt.%'),
            'elements': {
                'Ca': _num_obj(bf['elements.Ca'], 'wt.%'),
                'Mg': _num_obj(bf['elements.Mg'], 'wt.%'),
                'Zn': _num_obj(bf['elements.Zn'], 'wt.%'),
                'P':  _num_obj(bf['elements.P'],  'wt.%'),
                'B':  _num_obj(bf['elements.B'],  'wt.%'),
                'Mo': _num_obj(bf['elements.Mo'], 'wt.%'),
                'N':  _num_obj(bf['elements.N'],  'wt.%'),
                'S':  _num_obj(bf['elements.S'],  'wt.%'),
            },
            'kv40': _num_obj(bf['kv40'], 'cSt'),
            'kv100': _num_obj(bf['kv100'], 'cSt'),
            'density': _num_obj(bf['density'], 'kg/m3 (or as printed)'),
            'specific_gravity': sg,
            'flash_point': fp,
            'pour_point': _num_obj(bf['pour_point'], '°C'),
        },
        'open_questions': _open_questions(nit_rows),
        'conflicts': [],
    }


# ---------------------------------------------------------------------------
# base_oil tiers
# ---------------------------------------------------------------------------

def _api_group_chem(rows):
    rep = [r for r in rows if r['status'] == 'Reported']
    mis = [r for r in rows if r['status'] == 'Missing']
    if rep:
        r = rep[0]
        api_grp = {
            'value': _n(r.get('printed_text', '')),
            'status': 'Reported',
            'source': _src(r),
        }
        if _n(r.get('notes', '')):
            api_grp['notes'] = r['notes']
        return {
            'api_group': api_grp,
            'chemistry': {'value': None, 'status': 'Missing', 'source': dict(MISSING_SRC)},
        }
    api_grp = {'value': None, 'status': 'Missing', 'source': dict(MISSING_SRC)}
    if mis and _n(mis[0].get('notes', '')):
        api_grp['notes'] = mis[0]['notes']
    return {
        'api_group': api_grp,
        'chemistry': {'value': None, 'status': 'Missing', 'source': dict(MISSING_SRC)},
    }


def _ccs_items(rows):
    entries = _by_entry(rows)
    has_rep = any(r['status'] == 'Reported' for r in rows)
    if not has_rep:
        item = {
            'value': None, 'qualifier': None, 'min': None, 'max': None,
            'value_kind': None, 'printed_text': None, 'unit': 'mPa.s',
            'test_temperature_c': None, 'method': None,
            'status': 'Missing', 'calculation_note': None,
            'source': dict(MISSING_SRC),
        }
        mis = [r for r in rows if r['status'] == 'Missing' and _n(r.get('notes', ''))]
        if mis:
            item['calculation_note'] = mis[0]['notes']
        return [item]
    result = []
    for entry, erows in entries:
        rep = [r for r in erows if r['status'] == 'Reported']
        if rep:
            r = rep[0]
            obj = {
                'value': _num(r.get('value', '')),
                'qualifier': _n(r.get('qualifier', '')),
                'min': _num(r.get('min', '')),
                'max': _num(r.get('max', '')),
                'value_kind': _n(r.get('value_kind', '')),
                'printed_text': _n(r.get('printed_text', '')),
                'unit': _n(r.get('unit', '')) or 'mPa.s',
                'test_temperature_c': _num(r.get('test_temperature_c', '')),
                'method': _n(r.get('method', '')),
                'status': 'Reported',
                'calculation_note': None,
                'source': _src(r),
            }
            if _n(r.get('notes', '')):
                obj['notes'] = r['notes']
            result.append(obj)
    return result


def _mrv_items(rows):
    entries = _by_entry(rows)
    has_rep = any(r['status'] == 'Reported' for r in rows)
    if not has_rep:
        return [{'test_temperature_c': None,
                 'mrv_viscosity': _num_obj([], 'mPa.s'),
                 'yield_stress': _num_obj([], 'Pa')}]
    result = []
    for entry, erows in entries:
        rep = [r for r in erows if r['status'] == 'Reported']
        if rep:
            r = rep[0]
            result.append({
                'test_temperature_c': _num(r.get('test_temperature_c', '')),
                'mrv_viscosity': _num_obj(erows, 'mPa.s'),
                'yield_stress': _num_obj([], 'Pa'),
            })
    return result


def build_base_oil_tier1(pk, by_tmpl, dec, nit_rows):
    rows = by_tmpl.get('base_oil_tier1', [])
    bf = defaultdict(list)
    for r in rows:
        bf[r['field']].append(r)

    fields = {
        'api_group_chemistry': _api_group_chem(bf['api_group_chemistry']),
        'kv40': _num_obj(bf['kv40'], 'cSt'),
        'kv100': _num_obj(bf['kv100'], 'cSt'),
        'viscosity_index': _num_obj(bf['viscosity_index'], None),
        'density': _num_obj(bf['density'], 'kg/m3'),
        'ccs': _ccs_items(bf['ccs']),
    }
    sg_rows = bf['specific_gravity']
    if sg_rows:
        sg = _num_obj(sg_rows, 'dimensionless')
        sg_rep = [r for r in sg_rows if r['status'] == 'Reported']
        sg['reference_condition'] = _n(sg_rep[0].get('conditions', '')) if sg_rep else None
        fields['specific_gravity'] = sg

    return {
        'template_version': '1.1',
        'material_class': 'base_oil',
        'tier': 1,
        'tier_label': 'Blocking - all six required',
        'record_id': pk.replace(':', '_'),
        'product': _product_block(pk, dec),
        'source_documents': _source_docs(rows + nit_rows),
        'fields': fields,
        'open_questions': _open_questions(nit_rows),
        'conflicts': [],
    }


def build_base_oil_tier2(pk, by_tmpl, dec):
    rows = by_tmpl.get('base_oil_tier2', [])
    bf = defaultdict(list)
    for r in rows:
        bf[r['field']].append(r)
    return {
        'template_version': '1.1',
        'material_class': 'base_oil',
        'tier': 2,
        'tier_label': 'Verification of the finished oil - cold flow and volatility',
        'record_id': pk.replace(':', '_'),
        'product': _product_block(pk, dec),
        'source_documents': _source_docs(rows),
        'fields': {
            'mrv': _mrv_items(bf['mrv']),
            'noack_volatility': _num_obj(bf['noack_volatility'], 'wt.%'),
            'flash_point': _num_obj(bf['flash_point'], '°C'),
            'pour_point': _num_obj(bf['pour_point'], '°C'),
        },
        'open_questions': [],
        'conflicts': [],
    }


def build_base_oil_tier3(pk, by_tmpl, dec):
    rows = by_tmpl.get('base_oil_tier3', [])
    bf = defaultdict(list)
    for r in rows:
        bf[r['field']].append(r)
    return {
        'template_version': '1.1',
        'material_class': 'base_oil',
        'tier': 3,
        'tier_label': 'Substitution justification - only when swapping a stock',
        'record_id': pk.replace(':', '_'),
        'product': _product_block(pk, dec),
        'source_documents': _source_docs(rows),
        'fields': {
            'sulfur': _num_obj(bf['sulfur'], 'wt.% or ppm as printed'),
            'saturates': _num_obj(bf['saturates'], 'wt.% as printed'),
            'aromatics': _num_obj(bf['aromatics'], 'wt.% as printed'),
            'cloud_point': _num_obj(bf['cloud_point'], '°C'),
            'wax_content': _num_obj(bf['wax_content'], 'wt.%'),
        },
        'open_questions': [],
        'conflicts': [],
    }


# ---------------------------------------------------------------------------
# output path
# ---------------------------------------------------------------------------

def _out_paths(pk, mc, has_vm, has_ppd):
    """Return list of (json_obj_key, relative_path_from_OUT_DIR) for this product."""
    supplier = pk.split(':', 1)[0]
    prod_id_raw = pk.split(':', 1)[1]
    folder_id = f'{supplier}_{prod_id_raw}'

    if mc == 'additive_component':
        base = Path('Additive_components_json') / supplier / folder_id
        paths = [('component_general', base / 'general.json')]
        if has_vm:
            paths.append(('component_vm', base / 'vm.json'))
        if has_ppd:
            paths.append(('component_ppd', base / 'ppd.json'))
        return paths
    elif mc == 'additive_package':
        base = Path('Additive_packages_json') / supplier / folder_id
        return [
            ('package_tier1', base / 'tier1_route_defining.json'),
            ('package_tier2', base / 'tier2_numeric_contribution.json'),
        ]
    elif mc == 'base_oil':
        base = Path('Base_oils_json') / supplier / folder_id
        return [
            ('base_oil_tier1', base / f'{folder_id}__base_oil_tier1_blocking.json'),
            ('base_oil_tier2', base / f'{folder_id}__base_oil_tier2_verification.json'),
            ('base_oil_tier3', base / f'{folder_id}__base_oil_tier3_substitution.json'),
        ]
    return []


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    # 1. Load product stages (conversion-ready set)
    stages_path = ROOT / 'tables' / 'product_stages.csv'
    stages = {r['product_key']: r
              for r in csv.DictReader(open(stages_path, encoding='utf-8'))}
    cr_pks = {pk for pk, r in stages.items()
              if r.get('conversion_ready', '').lower() == 'yes'}
    print(f'Conversion-ready products: {len(cr_pks)}')

    # 2. Load decisions (for name/supplier info)
    decisions = {}
    for f in glob.glob(str(ROOT.parent / 'dataset_preparation_2026-11-14' / 'decisions' / '*.json')):
        d = json.load(open(f, encoding='utf-8'))
        for pk, v in d.get('products', {}).items():
            decisions[pk] = v
    # Also try decisions folder at the right level
    for f in glob.glob(str(ROOT / 'decisions' / '*.json')):
        d = json.load(open(f, encoding='utf-8'))
        for pk, v in d.get('products', {}).items():
            decisions[pk] = v

    # 3. Load all field evidence
    all_rows = []
    ev_dir = ROOT / 'field_evidence'
    for fpath in sorted(glob.glob(str(ev_dir / '*.csv'))):
        for r in csv.DictReader(open(fpath, encoding='utf-8')):
            all_rows.append(r)

    # 4. Group rows by product_key
    rows_by_pk = defaultdict(list)
    for r in all_rows:
        rows_by_pk[r['product_key']].append(r)

    # 5. Convert each CR product
    files_written = 0
    files_failed = []
    warnings = []

    for pk in sorted(cr_pks):
        prows = rows_by_pk.get(pk, [])
        if not prows:
            warnings.append(f'WARN {pk}: no evidence rows found')
            continue

        # Group by template
        by_tmpl = defaultdict(list)
        nit_rows = []
        for r in prows:
            tmpl = r['template']
            if tmpl.startswith('not_in_template:'):
                nit_rows.append(r)
            else:
                by_tmpl[tmpl].append(r)

        mc = stages[pk]['material_class']
        dec = decisions.get(pk, {'name': pk.split(':', 1)[1], 'supplier': pk.split(':', 1)[0]})

        has_vm = bool(by_tmpl.get('component_vm'))
        has_ppd = bool(by_tmpl.get('component_ppd'))

        # Build JSON objects
        built = {}
        try:
            if mc == 'additive_component':
                built['component_general'] = build_component_general(pk, by_tmpl, dec, nit_rows)
                if has_vm:
                    built['component_vm'] = build_component_vm(pk, by_tmpl, dec)
                if has_ppd:
                    built['component_ppd'] = build_component_ppd(pk, by_tmpl, dec)
            elif mc == 'additive_package':
                built['package_tier1'] = build_package_tier1(pk, by_tmpl, dec, nit_rows)
                built['package_tier2'] = build_package_tier2(pk, by_tmpl, dec, nit_rows)
            elif mc == 'base_oil':
                built['base_oil_tier1'] = build_base_oil_tier1(pk, by_tmpl, dec, nit_rows)
                built['base_oil_tier2'] = build_base_oil_tier2(pk, by_tmpl, dec)
                built['base_oil_tier3'] = build_base_oil_tier3(pk, by_tmpl, dec)
        except Exception as e:
            files_failed.append(f'{pk}: build error: {e}')
            continue

        # Write output files
        for obj_key, rel_path in _out_paths(pk, mc, has_vm, has_ppd):
            if obj_key not in built:
                continue
            out_path = OUT_DIR / rel_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(out_path, 'w', encoding='utf-8') as fh:
                    json.dump(built[obj_key], fh, ensure_ascii=False, indent=2)
                files_written += 1
            except Exception as e:
                files_failed.append(f'{pk} {rel_path}: write error: {e}')

    # 6. Summary
    print(f'Files written: {files_written}')
    if warnings:
        print(f'Warnings ({len(warnings)}):')
        for w in warnings:
            print(f'  {w}')
    if files_failed:
        print(f'Failed ({len(files_failed)}):')
        for f in files_failed:
            print(f'  {f}')
    else:
        print('No failures.')


if __name__ == '__main__':
    main()
