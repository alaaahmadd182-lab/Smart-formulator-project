"""Field-level mapping, S03 Infineum.
76 eligible products (additive_package tier1+tier2 and additive_component general).
Sources: Infineum product data sheets and SDS documents.

Doc format:
  STANDARD : Infineum product sheet with 'Typical Inspections' section.
             4-line groups per property: Property Name / Value / Unit / Method.
             'Performance' section above it with treat rate + performance claims.
  SDS_ONLY : Some products only have SDS (also uses Typical Inspections format).
  NONE     : One product (SV261L) has no Typical Inspections section.

Sources extracted programmatically from cached text-layer, 2026-11-19.
Writes field_evidence/s03_infineum.csv.
"""
import csv, gzip, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fm_common import COLS, field_units, write_rows, PKG

ROOT  = os.path.dirname(PKG)
CACHE = os.path.join(PKG, '_cache', 'ocr')
INV   = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')

# ── Load reference tables ────────────────────────────────────────────
links_raw  = list(csv.DictReader(open(os.path.join(PKG, 'tables', 'document_product_links.csv'), encoding='utf-8')))
docs_inv   = {r['sha256']: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}
stages_raw = list(csv.DictReader(open(os.path.join(PKG, 'tables', 'product_stages.csv'), encoding='utf-8')))
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's03_infineum.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('INFINEUM:')
            and r['stage2_identity']       == 'verified'
            and r['stage3_class_template'] == 'established'
            and r['stage5_field_mapping']  == 'not started'}

prod_docs = {}
for lk in links_raw:
    pk = lk['product_key']
    if pk in ELIGIBLE:
        prod_docs.setdefault(pk, []).append(lk)

REVIEW = 'TDS/SDS text read in full 2026-11-19; extraction from cached text-layer text'

# ── Cache reading ─────────────────────────────────────────────────────
def get_text(sha256):
    path = os.path.join(CACHE, sha256 + '.json.gz')
    if not os.path.exists(path):
        return ''
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        d = json.load(f)
    return '\n'.join(p.get('text', '') or '' for p in d.get('pages', []))

# ── Document selection ────────────────────────────────────────────────
DOC_TYPE_RANK = {'TDS/PDS': 0, 'TDS': 0, 'SDS': 1, 'brochure': 2, 'other': 3, 'unresolved': 4}

def select_best_doc(doc_links):
    """Select document that has 'Typical Inspections' section; prefer TDS over SDS."""
    scored = []
    for lk in doc_links:
        sha = lk['sha256']
        d   = docs_inv.get(sha, {})
        t   = get_text(sha)
        has_ti = 1 if re.search(r'Typical\s+Inspections?', t, re.I) else 0
        rank   = DOC_TYPE_RANK.get(d.get('document_type', ''), 5)
        scored.append((has_ti, -rank, len(t), lk, t))
    if not scored:
        return None, ''
    scored.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    best = scored[0]
    return best[3], best[4]  # (link, text)

def get_rev_date(sha256):
    d = docs_inv.get(sha256, {})
    dates = d.get('printed_dates', '')
    if dates:
        return str(dates).split(',')[0].strip()
    return ''

# ── Typical Inspections parser ────────────────────────────────────────
# Maps property name patterns → (field_key, template)
PROP_PATTERNS = [
    (r'Base\s+Number',                    'tbn',           'package_tier2', 'mg KOH/g', ''),
    (r'TBN|Total\s+Base\s+Number',        'tbn',           'package_tier2', 'mg KOH/g', ''),
    (r'Sulfated\s+Ash',                   'sulfated_ash',  'package_tier2', '%(m)',     ''),
    (r'Calcium',                           'ca',            'package_tier2', '%(m)',     ''),
    (r'Magnesium',                         'mg',            'package_tier2', '%(m)',     ''),
    (r'Zinc',                              'zn',            'package_tier2', '%(m)',     ''),
    (r'Phosphorus',                        'p',             'package_tier2', '%(m)',     ''),
    (r'Boron',                             'b',             'package_tier2', '%(m)',     ''),
    (r'Molybdenum',                        'mo',            'package_tier2', '%(m)',     ''),
    (r'Nitrogen',                          'n',             'package_tier2', '%(m)',     ''),
    (r'Sulfur(?!\s*ated)',                 's',             'package_tier2', '%(m)',     ''),
    (r'Density\s*(?:@|at|,)\s*(?:15|60)', 'density',       'package_tier2', 'kg/m3',   '15'),
    (r'Kinematic\s+Viscosity\s*(?:@|at)\s*100|Viscosity\s+at\s+100', 'kv100', 'package_tier2', 'cSt', '100'),
    (r'Kinematic\s+Viscosity\s*(?:@|at)\s*40|Viscosity\s+at\s+40',  'kv40',  'package_tier2', 'cSt', '40'),
    (r'Flash\s+Point',                    'flash_point',   'package_tier2', '°C',       ''),
    (r'Pour\s+Point',                     'pour_point',    'package_tier2', '°C',       ''),
    # Component-specific
    (r'SSI|Shear\s+Stability\s+Index',    'active_content','component_general', '',     ''),
]

def find_in_ti_block(block, prop_pattern):
    """Find value/unit/method for a property in the Typical Inspections block.
    Returns (printed_text, unit, method, label_line, temp) or None."""
    m = re.search(prop_pattern + r'[^\n]*\n', block, re.I)
    if not m:
        return None
    label_line = m.group(0).rstrip('\n').strip()
    pos = m.end()
    remaining = block[pos:]
    # Collect next 3 non-empty lines (value, unit, method)
    tokens = []
    for line in remaining.split('\n')[:10]:
        s = line.strip()
        if s:
            tokens.append(s)
        if len(tokens) >= 3:
            break
    if not tokens:
        return None
    value_str  = tokens[0]
    unit_str   = tokens[1] if len(tokens) > 1 else ''
    method_str = tokens[2] if len(tokens) > 2 else ''
    # Validate it's a numeric or bounded value
    if not (re.match(r'^[<>≥≤]?\s*-?\d', value_str) or
            re.search(r'\d+.*(?:minimum|maximum|min\.?|max\.?)', value_str, re.I)):
        return None
    # unit_str might actually be a method if unit is blank
    if unit_str and re.search(r'ASTM|AM-S|ITM|ISO\b|SH/?T', unit_str):
        method_str = unit_str
        unit_str   = ''
    return value_str, unit_str, method_str, label_line

def _parse(s):
    """Value string -> (value, qualifier, lo, hi, vk)"""
    s = s.strip()
    # "100 Minimum" or "100 min." -> bound ≥
    m = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*(?:[Mm]in(?:imum)?\.?)', s)
    if m:
        return '', '≥', m.group(1).replace(',', '.'), '', 'bound'
    # "100 Maximum" / "max."  -> bound ≤
    m = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*(?:[Mm]ax(?:imum)?\.?)', s)
    if m:
        return '', '≤', '', m.group(1).replace(',', '.'), 'bound'
    # "<1.5" or ">5"  -> bound
    m = re.fullmatch(r'(<|>|≥|≤)\s*(-?\d+(?:[.,]\d+)?)', s)
    if m:
        sym, v = m.group(1), m.group(2).replace(',', '.')
        q_map = {'<': '≤', '>': '≥', '≥': '≥', '≤': '≤'}  # treat < as ≤ for display
        q = q_map.get(sym, sym)
        return '', q, v if q == '≥' else '', v if q == '≤' else '', 'bound'
    # Range "X-Y"
    m = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*[-–]\s*(-?\d+(?:[.,]\d+)?)', s)
    if m:
        return '', '', m.group(1).replace(',', '.'), m.group(2).replace(',', '.'), 'range'
    # Plain number
    m = re.fullmatch(r'-?\d+(?:[.,]\d+)?', s)
    if m:
        return s.replace(',', '.'), '', '', '', 'typical'
    return '', '', '', '', 'text'

def parse_typical_inspections(text):
    """Extract Typical Inspections block and return dict of field results."""
    m = re.search(r'Typical\s+Inspections?\s*\n(.*?)(?:\(a\)\s*Not a spec|\Z)', text, re.DOTALL | re.I)
    if not m:
        return {}
    block = m.group(1)
    results = {}
    for pat, fkey, tmpl, default_unit, temp in PROP_PATTERNS:
        result = find_in_ti_block(block, pat)
        if result:
            value_str, unit_str, method_str, label_line = result
            unit = unit_str or default_unit
            results[fkey] = (value_str, unit, method_str, label_line, temp)
    return results

# ── Performance section parser ────────────────────────────────────────
def parse_performance(text):
    """Extract treat rate, performance claims, SAE grades from Performance section."""
    # Find Performance section
    m = re.search(r'(?:^|\n)Performance\s*\n(.*?)(?:\n\s*Typical\s+Inspections|\Z)', text, re.DOTALL | re.I)
    block = m.group(1) if m else text[:3000]

    # Treat rate: look for "Mass %:" followed by a number, or percentage in text
    treat_rate = ''
    m2 = re.search(r'(?:Mass\s*%|treat\s*(?:rate|level))[:\s]+([\d.]+)', block, re.I)
    if m2:
        treat_rate = m2.group(1) + '%'
    else:
        # Look for a number between 5 and 20 near "%" that looks like a treat rate
        m3 = re.search(r'\b(1[0-9]\.\d|[5-9]\.\d)\s*%?(?:\s*treat|\s*mass)', block, re.I)
        if m3:
            treat_rate = m3.group(1) + '%'

    # Performance claims
    claims = set()
    for pat in [r'API\s+[A-Z]{2,6}(?:[/-][A-Z]{2,6})*', r'ACEA\s+[A-Z]\d+(?:[/-][A-Z]\d+)*(?:-\d{2,4})?',
                r'ILSAC\s+GF-\d', r'dexos[12]?\b', r'JASO\s+\w+', r'Allison\s+\w+',
                r'Caterpillar\s+\w+', r'ZF\s+\w+', r'MB\s+22[0-9]\.\d+']:
        for x in re.finditer(pat, block, re.I):
            claims.add(x.group(0).strip())

    # SAE grades
    sae_grades = set()
    for x in re.finditer(r'\b\d+W[-–]\d+|\b\d+W\b', block):
        g = x.group(0)
        if re.match(r'^\d+W[-–]\d+$|^\d+W$', g):
            sae_grades.add(g)

    return {
        'treat_rate':         treat_rate,
        'performance_claims': '; '.join(sorted(claims)),
        'sae_grades':         ', '.join(sorted(sae_grades)),
    }

# ── Package type / description ────────────────────────────────────────
def extract_package_type(text):
    patterns = [
        (r'PCMO|Passenger Car (?:Motor|Engine) Oil', 'PCMO additive package'),
        (r'Heavy\s*Duty|HDEO|Heavy Duty Diesel', 'HDEO additive package'),
        (r'[Cc]runk[Cc]ase|crankcase', 'crankcase oil additive package'),
        (r'ATF|Automatic\s+Transmission', 'ATF additive package'),
        (r'CVT', 'CVT additive package'),
        (r'Gear\s+Oil|gear\s+oil', 'gear oil additive package'),
        (r'Hydraulic', 'hydraulic oil additive package'),
        (r'Turbine', 'turbine oil additive package'),
        (r'Industrial', 'industrial oil additive package'),
        (r'Viscosity\s+Modifier|VM\b', 'viscosity modifier'),
        (r'Pour\s+Point\s+Dep', 'pour point depressant'),
        (r'Friction\s+Modifier', 'friction modifier'),
        (r'detergent\s+inhibitor', 'DI additive package'),
    ]
    for pat, label in patterns:
        if re.search(pat, text[:2000], re.I):
            return label
    # Fallback: look for "is a/an X" in description
    m = re.search(r'Infineum\s+\S+\s+is\s+(?:a|an)\s+([^.]+\.)', text[:1500], re.I)
    if m:
        return m.group(1).strip()[:100]
    return ''

def extract_chem_family(text):
    m = re.search(r'Infineum\s+\S+\s+is\s+(?:a|an)\s+([^.]+\.)', text[:1500], re.I)
    if m:
        return m.group(1).strip()
    return ''

def extract_permitted_base_oils(text):
    m = re.search(
        r'(?:in|with|using|for use (?:in|with))\s+((?:Group\s*(?:I{1,3}|IV|V|III|II|I)(?:\s*(?:and|&|or|/|\+)?\s*)?)+\s*base\s*(?:oil|stock)s?)',
        text, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r'approved\s+base\s+stock[^\n]*', text, re.I)
    if m:
        return m.group(0).strip()
    return ''

# ── Row building ──────────────────────────────────────────────────────
def _missing(pk, tmpl, field, src_file, sha, rev):
    return {
        'product_key': pk, 'template': tmpl, 'field': field,
        'entry': 'primary', 'value': '', 'qualifier': '', 'min': '', 'max': '',
        'value_kind': '', 'printed_text': '', 'unit': '',
        'test_temperature_c': '', 'method': '', 'conditions': '',
        'status': 'Missing', 'value_class': 'numeric',
        'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '',
        'revision_date': rev, 'notes': '', 'review': REVIEW,
    }

def _reported(pk, tmpl, field, printed, unit, qual, lo, hi, vk, temp, method,
              src_file, sha, rev, notes='', basis=''):
    val = lo if (vk == 'bound' and qual == '≥') else hi if (vk == 'bound' and qual == '≤') else printed
    return {
        'product_key': pk, 'template': tmpl, 'field': field,
        'entry': 'primary', 'value': val, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': temp, 'method': method, 'conditions': '',
        'status': 'Reported', 'value_class': 'numeric',
        'basis': basis, 'source_file': src_file, 'sha256': sha, 'page': '',
        'revision_date': rev, 'notes': notes, 'review': REVIEW,
    }

def _text_field(pk, tmpl, field, text_val, src_file, sha, rev, notes=''):
    return {
        'product_key': pk, 'template': tmpl, 'field': field,
        'entry': 'primary', 'value': '', 'qualifier': '', 'min': '', 'max': '',
        'value_kind': 'text', 'printed_text': text_val, 'unit': '',
        'test_temperature_c': '', 'method': '', 'conditions': '',
        'status': 'Reported', 'value_class': 'text',
        'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '',
        'revision_date': rev, 'notes': notes, 'review': REVIEW,
    }

# ── Field lists ───────────────────────────────────────────────────────
PKG_TIER1_FIELDS = [
    'package_type_application.package_type',
    'package_type_application.intended_service',
    'performance_claims',
    'sae_grades_documented',
    'permitted_base_oils_restrictions',
    'route_selector_restrictions',
    'treat_rate_matrix',
    'required_co_components',
    'published_formulations',
]

PKG_TIER2_FIELDS = [
    'tbn', 'sulfated_ash',
    'elements.Ca', 'elements.Mg', 'elements.Zn', 'elements.P',
    'elements.B', 'elements.Mo', 'elements.N', 'elements.S',
    'kv40', 'kv100', 'density', 'specific_gravity',
    'flash_point', 'pour_point',
]

TIER2_FKEY = {
    'tbn':          'tbn',
    'sulfated_ash': 'sulfated_ash',
    'elements.Ca':  'ca',
    'elements.Mg':  'mg',
    'elements.Zn':  'zn',
    'elements.P':   'p',
    'elements.B':   'b',
    'elements.Mo':  'mo',
    'elements.N':   'n',
    'elements.S':   's',
    'kv40':         'kv40',
    'kv100':        'kv100',
    'density':      'density',
    'specific_gravity': 'density',  # will be blank for density if only SG label found
    'flash_point':  'flash_point',
    'pour_point':   'pour_point',
}

COMP_GEN_FIELDS = [
    'function.primary',
    'function.secondary',
    'chemical_family',
    'active_content',
    'carrier.identity',
    'carrier.share_wt_pct',
    'treat_rate',
    'compatibility_restrictions',
    'function_specific_markers.tbn',
    'function_specific_markers.ca',
    'function_specific_markers.mg',
    'function_specific_markers.p',
    'function_specific_markers.zn',
    'function_specific_markers.mo',
]

COMP_FKEY = {
    'function_specific_markers.tbn': 'tbn',
    'function_specific_markers.ca':  'ca',
    'function_specific_markers.mg':  'mg',
    'function_specific_markers.p':   'p',
    'function_specific_markers.zn':  'zn',
    'function_specific_markers.mo':  'mo',
    'active_content':                'active_content',
}

# ── Package rows ──────────────────────────────────────────────────────
def package_rows(pk, text, sha, fname, rev):
    rows  = []
    ti    = parse_typical_inspections(text)
    perf  = parse_performance(text)
    pkg_t = extract_package_type(text)
    base  = extract_permitted_base_oils(text)

    for f in PKG_TIER1_FIELDS:
        if f == 'package_type_application.package_type':
            if pkg_t:
                rows.append(_text_field(pk, 'package_tier1', f, pkg_t, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'performance_claims':
            pc = perf.get('performance_claims', '')
            if pc:
                rows.append(_text_field(pk, 'package_tier1', f, pc, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'sae_grades_documented':
            sg = perf.get('sae_grades', '')
            if sg:
                rows.append(_text_field(pk, 'package_tier1', f, sg, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'permitted_base_oils_restrictions':
            if base:
                rows.append(_text_field(pk, 'package_tier1', f, base, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'treat_rate_matrix':
            tr = perf.get('treat_rate', '')
            if tr:
                v_str = tr.replace('%', '').strip()
                rows.append(_reported(pk, 'package_tier1', f, tr, '%', '', v_str, '', 'typical', '', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        else:
            rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))

    for f in PKG_TIER2_FIELDS:
        fkey = TIER2_FKEY.get(f, f)
        result = ti.get(fkey)
        if result:
            value_str, unit, method, label_line, temp = result
            printed, qual, lo, hi, vk = _parse(value_str)
            rows.append(_reported(pk, 'package_tier2', f, value_str, unit, qual, lo, hi, vk, temp, method,
                                  fname, sha, rev,
                                  notes=f'From Typical Inspections: {label_line[:80]}'))
        else:
            rows.append(_missing(pk, 'package_tier2', f, fname, sha, rev))
    return rows

# ── Component rows ────────────────────────────────────────────────────
def component_rows(pk, text, sha, fname, rev):
    rows = []
    tmpl = 'component_general'
    ti   = parse_typical_inspections(text)
    chem = extract_chem_family(text)

    # Treat rate from text
    tr = ''
    m_tr = re.search(r'(?:dosage|treat\s*rate|dose)[^\n]*?([\d.]+)\s*%', text, re.I)
    if m_tr:
        tr = m_tr.group(1) + '%'

    for f in COMP_GEN_FIELDS:
        if f == 'chemical_family':
            if chem:
                rows.append(_text_field(pk, tmpl, f, chem, fname, sha, rev))
            else:
                rows.append(_missing(pk, tmpl, f, fname, sha, rev))
        elif f == 'treat_rate':
            if tr:
                v_str = tr.replace('%', '').strip()
                rows.append(_reported(pk, tmpl, f, tr, '%', '', v_str, '', 'typical', '', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, tmpl, f, fname, sha, rev))
        elif f in COMP_FKEY:
            fkey = COMP_FKEY[f]
            result = ti.get(fkey)
            if result:
                value_str, unit, method, label_line, temp = result
                printed, qual, lo, hi, vk = _parse(value_str)
                rows.append(_reported(pk, tmpl, f, value_str, unit, qual, lo, hi, vk, temp, method,
                                      fname, sha, rev,
                                      notes=f'From Typical Inspections: {label_line[:80]}'))
            else:
                rows.append(_missing(pk, tmpl, f, fname, sha, rev))
        else:
            rows.append(_missing(pk, tmpl, f, fname, sha, rev))
    return rows

# ── Main loop ─────────────────────────────────────────────────────────
def main():
    rows   = []
    n_done = 0

    for pk in sorted(ELIGIBLE):
        doc_links = prod_docs.get(pk, [])
        info = decisions.get(pk, {})
        mc   = info.get('material_class', '')
        is_comp = (mc == 'additive_component')

        if not doc_links:
            fields = COMP_GEN_FIELDS if is_comp else PKG_TIER1_FIELDS + PKG_TIER2_FIELDS
            tmpl   = 'component_general' if is_comp else 'package_tier1'
            for f in fields:
                rows.append(_missing(pk, tmpl, f, '', '', ''))
            n_done += 1
            continue

        link, text = select_best_doc(doc_links)
        if link is None:
            fields = COMP_GEN_FIELDS if is_comp else PKG_TIER1_FIELDS + PKG_TIER2_FIELDS
            tmpl   = 'component_general' if is_comp else 'package_tier1'
            for f in fields:
                rows.append(_missing(pk, tmpl, f, '', '', ''))
            n_done += 1
            continue

        sha   = link['sha256']
        fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
        rev   = get_rev_date(sha)

        if is_comp:
            rows.extend(component_rows(pk, text, sha, fname, rev))
        else:
            rows.extend(package_rows(pk, text, sha, fname, rev))

        n_done += 1

    write_rows('s03_infineum.csv', rows)
    from collections import Counter
    status_ctr = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {status_ctr["Reported"]}, Missing: {status_ctr["Missing"]}')

if __name__ == '__main__':
    main()
