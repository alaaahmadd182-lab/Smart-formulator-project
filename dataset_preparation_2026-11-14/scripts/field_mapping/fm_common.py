"""Field-level mapping helpers (stage 4 'technical evidence reviewed' and stage 5 'field-level mapping complete').

One row of field evidence = one printed statement mapped to one template field (or to 'not_in_template:<item>' when the document
prints a property the template has no field for: nothing printed is dropped). Rows never contain a value that is not printed:
  value / min / max     numbers exactly as printed ('180 min' -> qualifier '>=', min 180; '150-250' -> min 150, max 250)
  printed_text          the printed cell, verbatim            unit          the printed unit
  value_kind            'typical' | 'bound' | 'range' | 'text' | 'report-only' (the sheet prints 'Report': no value)
  value_class           what kind of statement it is: 'product sheet, column headed Typical Value' / 'recommended dosage' /
                        'batch certificate' / 'finished-oil formulation example' ... (typical vs specification vs batch kept apart)
  status                Reported | Missing (template vocabulary); a Missing row carries no value and says what was inspected
Units of mapping ('field units') are derived from the JSON templates: every value object, list, scalar and restriction block.
A product's mapping is 'complete' when every field unit of its template(s) has >= 1 row (Reported or Missing) and every
Reported row cites file, page and printed text. 'complete' does not approve any value and creates no JSON."""
import csv, json, os, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
PKG = os.path.dirname(SCRIPTS)
ROOT = os.path.dirname(PKG)
_spec = importlib.util.spec_from_file_location('ident', os.path.join(SCRIPTS, '02_identify.py'))
ident = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ident)
COLS = ['product_key', 'template', 'field', 'entry', 'value', 'qualifier', 'min', 'max', 'value_kind', 'printed_text', 'unit', 'test_temperature_c', 'method', 'conditions',
        'status', 'value_class', 'basis', 'source_file', 'sha256', 'page', 'revision_date', 'notes', 'review']
TEMPLATES = {'component_general': 'additive_component_all_general.json', 'component_vm': 'additive_component_vm.json', 'component_ppd': 'additive_component_ppd.json',
             'package_tier1': 'additive_package_tier1_route_defining.json', 'package_tier2': 'additive_package_tier2_numeric_contribution.json',
             'base_oil_tier1': 'base_oil_tier1_blocking.json', 'base_oil_tier2': 'base_oil_tier2_verification.json', 'base_oil_tier3': 'base_oil_tier3_substitution.json'}


def field_units(tkey):
    """Field units of a template: value objects, lists, scalars; a dict with its own 'status' or 'usable' key is one block unit."""
    d = json.load(open(os.path.join(ROOT, 'json_templates', TEMPLATES[tkey]), encoding='utf-8'))['fields']
    out = []

    def walk(o, p):
        for k, v in o.items():
            if isinstance(v, dict) and not ({'value', 'status'} <= set(v)) and not ('usable' in v or isinstance(v.get('status'), str)):
                walk(v, p + k + '.')
            else:
                out.append(p + k)
    walk(d, '')
    return out


def pages(sha):
    pg, _ = ident.pages_for(sha)
    return pg


def parse_value(txt):
    """Printed cell -> (value, qualifier, min, max, value_kind). Nothing is computed: a range stays a range, a bound stays a bound."""
    t = txt.strip()
    m = re.fullmatch(r'(-?\d+(?:\.\d+)?)\s*-\s*(-?\d+(?:\.\d+)?)', t)
    if m: return '', '', m.group(1), m.group(2), 'range'
    m = re.fullmatch(r'(-?\d+(?:\.\d+)?)\s*(min|max)\b\.?(.*)', t, re.I)
    if m:
        lo = m.group(2).lower() == 'min'
        return '', '>=' if lo else '<=', m.group(1) if lo else '', '' if lo else m.group(1), 'bound'
    m = re.fullmatch(r'-?\d+(?:\.\d+)?', t)
    if m: return t, '', '', '', 'typical'
    if t.lower() == 'report': return '', '', '', '', 'report-only'
    return '', '', '', '', 'text'


def write_rows(name, rows):
    os.makedirs(os.path.join(PKG, 'field_evidence'), exist_ok=True)
    with open(os.path.join(PKG, 'field_evidence', name), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction='ignore'); w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in COLS})
