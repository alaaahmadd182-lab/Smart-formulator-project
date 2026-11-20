"""Field-level mapping, S15 LUBIMAX (Coraplus / Kemipex).
33 eligible products: 19 additive_component, 11 base_oil, 3 additive_package.

Doc format families:
  FORMAT_A : "Characteristics:" section (most products, 2 styles):
             Style 1 – 2-column: label on one line, value on next.
             Style 2 – 3-column: label / ASTM method / value (each on own line).
             Standard find_prop strategy 2 handles both.
  FORMAT_B : Base oil TDS property table: Property / ASTM method / value
             (same 3-row structure, appears after "Applications" section).
  FORMAT_C : SDS "Physical and Chemical Properties" / Section 9 (3 products).

Number format note:
  Values like `1,060 kg/m3` use comma as THOUSANDS separator (not decimal).
  Values like `1.060` use period as decimal.
  Comma-decimal (European) may appear in some docs.
  _clean_thou() strips thousands-commas (comma + exactly 3 digits + non-digit).

Writes field_evidence/s15_lubimax.csv.
"""
import csv, gzip, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fm_common import COLS, field_units, write_rows, PKG

ROOT  = os.path.dirname(PKG)
CACHE = os.path.join(PKG, '_cache', 'ocr')
INV   = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')

links_raw  = list(csv.DictReader(open(os.path.join(PKG, 'tables', 'document_product_links.csv'), encoding='utf-8')))
docs_inv   = {r['sha256']: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}
stages_raw = list(csv.DictReader(open(os.path.join(PKG, 'tables', 'product_stages.csv'), encoding='utf-8')))
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's15_lubimax.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('LUBIMAX:')
            and r['stage2_identity']       == 'verified'
            and r['stage3_class_template'] == 'established'
            and r['stage5_field_mapping']  == 'not started'}

prod_docs = {}
for lk in links_raw:
    pk = lk['product_key']
    if pk in ELIGIBLE:
        prod_docs.setdefault(pk, []).append(lk)

REVIEW = 'TDS text read in full 2026-11-19; extraction from cached text-layer'

def get_text(sha256):
    path = os.path.join(CACHE, sha256 + '.json.gz')
    if not os.path.exists(path):
        return ''
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        d = json.load(f)
    return '\n'.join(p.get('text', '') or '' for p in d.get('pages', []))

DOC_RANK = {'TDS/PDS': 0, 'TDS': 0, 'SDS': 1, 'brochure': 2, 'other': 2, 'unresolved': 3}

def select_best_doc(doc_links):
    scored = []
    for lk in doc_links:
        sha = lk['sha256']
        d   = docs_inv.get(sha, {})
        t   = get_text(sha)
        rank = DOC_RANK.get(d.get('document_type', ''), 4)
        scored.append((rank, -len(t), lk, t))
    if not scored:
        return None, ''
    scored.sort(key=lambda x: (x[0], x[1]))
    return scored[0][2], scored[0][3]

def get_rev_date(sha256):
    d = docs_inv.get(sha256, {})
    dates = d.get('printed_dates', '')
    return str(dates).split(',')[0].strip() if dates else ''

# ── Section detection ─────────────────────────────────────────────────
def find_data_block(text):
    """Return (block, section_type). Try Characteristics, then specs, then Section 9."""
    # "Characteristics:" section (additive components, packages)
    m = re.search(r'[Cc]haracteristics\s*:', text)
    if m:
        return text[m.end():m.end()+2000], 'characteristics'

    # Base oil technical specs table (after Applications, before packaging)
    m2 = re.search(r'[Tt]echnical\s+[Ss]pecification|[Ss]pecifications?\s*:', text)
    if m2:
        return text[m2.end():m2.end()+2000], 'tech_specs'

    # SDS Section 9 / Physical and chemical properties
    m3 = re.search(r'(?:SECTION|Section)\s+9[^0-9]|Physical and chemical properties', text, re.I)
    if m3:
        after = text[m3.end():]
        m10 = re.search(r'(?:SECTION|Section)\s+1[0-9][^0-9]', after)
        block = after[:m10.start()] if m10 else after[:3000]
        return block, 'sds_sec9'

    # Fallback: use text from about 20% in (past product description header)
    cutoff = max(0, len(text) // 5)
    return text[cutoff:cutoff+3000], 'full_text'

# ── Numeric extraction ────────────────────────────────────────────────
def _clean_thou(s):
    """Remove thousands-commas: 1,060 -> 1060 (comma + exactly 3 digits + non-digit)."""
    return re.sub(r'(\d),(\d{3})(?!\d)', r'\1\2', s)

def _extract_num(s):
    s = s.rstrip('\t').strip()
    s = _clean_thou(s)
    s = re.sub(r'\([^)]*\)', '', s).strip()
    m = re.match(r'([<>≥≤]?=?\s*-?\d[\d.,]*)(?:\s*[-–]\s*-?\d[\d.,]*)?', s)
    if m:
        return m.group(0).strip()
    return ''

def _wrap(pat):
    return r'(?:' + pat + r')'

def find_prop(block, label_pat):
    """Near-label scan: strategy 1 (same line) + strategy 2 (next 16 lines)."""
    m = re.search(_wrap(label_pat), block, re.I)
    if not m:
        return None
    label_line = m.group(0).strip()
    rest_of_line = block[m.end():].split('\n')[0]
    rest_clean = re.sub(r'^[\t:\s]+', '', rest_of_line).strip()
    if rest_clean:
        v = _extract_num(rest_clean)
        if v:
            return v, label_line
    after = block[m.end():]
    for ln in after.split('\n')[1:16]:
        s = ln.strip().rstrip('\t').strip()
        if not s:
            continue
        if re.match(r'^\(', s):
            continue
        v = _extract_num(s)
        if v:
            return v, label_line
        if len(s) > 25 and re.match(r'^[A-Za-z]', s) and not re.search(r'\d', s):
            break
    return None

def _parse(s):
    s = s.strip()
    s = re.sub(r'\([^)]*\)', '', s).strip()
    s = _clean_thou(s)
    um = re.search(r'\s+([a-zA-Z°%][a-zA-Z/°% 2*]*)\s*$', s)
    unit_v = um.group(1).strip() if um else ''
    if um:
        s = s[:um.start()].strip()
    mr = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*[-–]\s*(-?\d+(?:[.,]\d+)?)', s)
    if mr:
        a = mr.group(1).replace(',', '.')
        b = mr.group(2).replace(',', '.')
        return '', '', a, b, 'range', unit_v
    mb = re.fullmatch(r'([<>≥≤]=?)\s*(-?\d+(?:[.,]\d+)?)', s)
    if mb:
        sym, v = mb.group(1), mb.group(2).replace(',', '.')
        q = {'<': '≤', '>': '≥', '>=': '≥', '<=': '≤', '≥': '≥', '≤': '≤'}.get(sym, sym)
        return '', q, v if q == '≥' else '', v if q == '≤' else '', 'bound', unit_v
    mn = re.fullmatch(r'-?\d+(?:[.,]\d+)?', s)
    if mn:
        return s.replace(',', '.'), '', '', '', 'typical', unit_v
    return '', '', '', '', 'text', unit_v

# ── Property patterns ─────────────────────────────────────────────────
PKG_PROPS = [
    (r'[Kk]inematic\s+[Vv]iscosity[^)]*(?:@|at)\s*40|[Vv]iscosity[^)]*40\s*[°]?C',
                                             'kv40',           'cSt',    '40'),
    (r'[Kk]inematic\s+[Vv]iscosity[^)]*(?:@|at)\s*100|[Vv]iscosity[^)]*100\s*[°]?C',
                                             'kv100',          'cSt',    '100'),
    (r'[Vv]iscosity\s+[Ii]ndex',             'viscosity_index','',       ''),
    (r'[Ss]pecific\s+[Gg]ravity',            'specific_gravity','',      ''),
    (r'[Rr]elative\s+[Dd]ensity',            'density',        '',       '15'),
    (r'[Dd]ensity(?!\s*[Gg]ravity)(?!\s+at\s+15)', 'density',  'kg/m3',  ''),
    (r'[Ff]lash\s*[Pp]oint|[Ff]lashpoint',  'flash_point',    '°C',     ''),
    (r'[Pp]our\s+[Pp]oint',                  'pour_point',     '°C',     ''),
    (r'[Bb]ase\s+[Nn]umber|TBN\b|[Tt]otal\s+[Bb]ase',
                                             'tbn',            'mg KOH/g',''),
    (r'[Ss]ulfated\s+[Aa]sh|[Ss]ulphated\s+[Aa]sh',
                                             'sulfated_ash',   '%',      ''),
    (r'[Cc]alcium\b',                        'ca',             '%',      ''),
    (r'[Mm]agnesium\b',                      'mg_elem',        '%',      ''),
    (r'[Zz]inc\b',                           'zn',             '%',      ''),
    (r'[Pp]hosphorus\b',                     'p',              '%',      ''),
    (r'[Bb]oron\b',                          'b',              '%',      ''),
    (r'[Mm]olybdenum\b',                     'mo',             '%',      ''),
    (r'[Nn]itrogen\b',                       'n',              '%',      ''),
    (r'[Ss]ulphur(?!\s*at)|[Ss]ulfur(?!\s*at)\b',
                                             's',              '%',      ''),
]

def extract_numeric(text, props):
    block, _ = find_data_block(text)
    results = {}
    for label_pat, fkey, default_unit, default_temp in props:
        if fkey in results:
            continue
        r = find_prop(block, label_pat)
        if r:
            raw, label_line = r
            results[fkey] = (raw, label_line, default_unit, default_temp)
    return results

# ── Text-field extractors ─────────────────────────────────────────────
def extract_treat_rate(text):
    for pat in [
        r'(?:typically used|is recommended)\s+at\s+([\d.,]+)\s*(?:[-–?]\s*([\d.,]+))?\s*wt',
        r'([\d.,]+)\s*[-–?]\s*([\d.,]+)\s*wt\.?\s*%',
        r'at\s+([\d.,]+)\s*[-–?]\s*([\d.,]+)\s*wt\.?\s*%',
        r'([\d.,]+)\s*wt\.?\s*%\s+(?:is recommended|are recommended)',
    ]:
        m = re.search(pat, text[:3000], re.I)
        if m:
            groups = [g for g in m.groups() if g]
            vals = []
            for g in groups:
                try:
                    vals.append(float(g.replace(',', '.')))
                except Exception:
                    pass
            if vals:
                vmin = min(vals)
                vmax = max(vals)
                if 0.05 <= vmin <= 25:
                    if len(vals) >= 2:
                        return f'{vmin}-{vmax}%'
                    return f'{vmin}%'
    # Fallback: scan for "X%" near treat/dose keywords
    for pat in [
        r'[Tt]reat\s+[Rr]ate[^.]*?([\d.,]+)\s*%',
        r'[Rr]ecommended.*?([\d.,]+)\s*%',
    ]:
        m = re.search(pat, text[:3000], re.I)
        if m:
            try:
                v = float(m.group(1).replace(',', '.'))
                if 0.05 <= v <= 25:
                    return f'{v}%'
            except Exception:
                pass
    return ''

def extract_performance_claims(text):
    claims = set()
    for pat in [r'API\s+[A-Z]{2,}(?:[/+][A-Z]{2,})*', r'ACEA\s+[A-Z]\d+(?:[-/][A-Z]\d+)*(?:-\d{2,4})?',
                r'ILSAC\s+GF-\d', r'dexos[12]?\b', r'JASO\s+\w+', r'DIN\s+51\s*\d+',
                r'CES\s+\d+', r'MB[-\s]\d+', r'MAN\s+\d+', r'VW\s+\d+']:
        for x in re.finditer(pat, text, re.I):
            g = x.group(0).strip()
            if len(g) >= 5:
                claims.add(g)
    return '; '.join(sorted(claims))

def extract_sae_grades(text):
    grades = set()
    for x in re.finditer(r'\b\d+W[-–]\d+|\b\d+W\b', text):
        g = x.group(0)
        if re.match(r'^\d+W[-–]\d+$|^\d+W$', g):
            grades.add(g)
    return ', '.join(sorted(grades))

def extract_package_type(text):
    for pat, label in [
        (r'Passenger Car|PCMO', 'PCMO additive package'),
        (r'Heavy\s*[Dd]uty|HDEO', 'HDEO additive package'),
        (r'[Gg]ear\s+[Oo]il\b', 'gear oil additive package'),
        (r'[Hh]ydraulic', 'hydraulic oil additive package'),
        (r'ATF|Automatic Transmission', 'ATF additive package'),
        (r'[Ee]ngine\s+[Oo]il\s+[Aa]dditive', 'engine oil additive package'),
        (r'[Ii]ndustrial', 'industrial oil additive package'),
    ]:
        if re.search(pat, text[:2000], re.I):
            return label
    return ''

def extract_chem_family(text):
    for pat, label in [
        (r'PMA|polymethacrylate|poly.*methacrylate', 'polymethacrylate (PMA)'),
        (r'OCP|olefin\s*copolymer', 'olefin copolymer (OCP)'),
        (r'[Ss]tyre?ne.*[Mm]aleic|SMA\b', 'styrene maleic anhydride copolymer'),
        (r'[Vv]iscosity\s+[Mm]odifier', 'viscosity modifier polymer'),
        (r'[Pp]our\s+[Pp]oint\s+[Dd]ep|PPD\b', 'pour point depressant'),
        (r'[Zz]DDC?P|zinc.*dithioph', 'ZDDP'),
        (r'[Ss]uccinimide', 'succinimide dispersant'),
        (r'[Ss]ulfonate.*[Cc]alcium|[Cc]alcium.*[Ss]ulfonate', 'calcium sulfonate'),
        (r'[Pp]henolic.*[Aa]ntioxidant|[Hh]indered\s+[Pp]henol', 'hindered phenol antioxidant'),
        (r'[Dd]iphenylamine|[Aa]mine.*[Aa]ntioxidant', 'diphenylamine antioxidant'),
        (r'mineral\s+oil\s+carrier|alkyl.*methacrylate', 'alkyl methacrylate copolymer'),
    ]:
        if re.search(pat, text[:3000], re.I):
            return label
    return ''

def extract_api_group(text):
    for pat, label in [
        (r'Group\s+II\+|Group\s+II\s+plus', 'Group II+'),
        (r'Group\s+IV|PAO\b|poly.alpha.olefin', 'Group IV'),
        (r'Group\s+V', 'Group V'),
        (r'Group\s+III', 'Group III'),
        (r'Group\s+II\b', 'Group II'),
        (r'Group\s+I\b', 'Group I'),
    ]:
        if re.search(pat, text[:2000], re.I):
            return label
    return ''

# ── Row building ──────────────────────────────────────────────────────
def _missing(pk, tmpl, field, src_file, sha, rev):
    return {'product_key': pk, 'template': tmpl, 'field': field,
            'entry': 'primary', 'value': '', 'qualifier': '', 'min': '', 'max': '',
            'value_kind': '', 'printed_text': '', 'unit': '',
            'test_temperature_c': '', 'method': '', 'conditions': '',
            'status': 'Missing', 'value_class': 'numeric',
            'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '1',
            'revision_date': rev, 'notes': '', 'review': REVIEW}

def _reported(pk, tmpl, field, printed, unit, qual, lo, hi, vk, temp, method,
              src_file, sha, rev, notes=''):
    val = lo if (vk == 'bound' and qual == '≥') else hi if (vk == 'bound' and qual == '≤') else printed
    return {'product_key': pk, 'template': tmpl, 'field': field,
            'entry': 'primary', 'value': val, 'qualifier': qual, 'min': lo, 'max': hi,
            'value_kind': vk, 'printed_text': printed, 'unit': unit,
            'test_temperature_c': temp, 'method': method, 'conditions': '',
            'status': 'Reported', 'value_class': 'numeric',
            'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '1',
            'revision_date': rev, 'notes': notes, 'review': REVIEW}

def _text_field(pk, tmpl, field, text_val, src_file, sha, rev):
    return {'product_key': pk, 'template': tmpl, 'field': field,
            'entry': 'primary', 'value': '', 'qualifier': '', 'min': '', 'max': '',
            'value_kind': 'text', 'printed_text': text_val, 'unit': '',
            'test_temperature_c': '', 'method': '', 'conditions': '',
            'status': 'Reported', 'value_class': 'text',
            'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '1',
            'revision_date': rev, 'notes': '', 'review': REVIEW}

def emit_numeric(pk, tmpl, field, fkey, extracted, src_file, sha, rev):
    if fkey in extracted:
        raw, label_line, default_unit, default_temp = extracted[fkey]
        val, qual, lo, hi, vk, unit_v = _parse(raw)
        unit = unit_v or default_unit
        if vk not in ('typical', 'bound', 'range'):
            return _missing(pk, tmpl, field, src_file, sha, rev)
        return _reported(pk, tmpl, field, raw, unit, qual, lo, hi, vk,
                         default_temp, '', src_file, sha, rev,
                         notes=f'From characteristics: {label_line[:60]}')
    return _missing(pk, tmpl, field, src_file, sha, rev)

# ── Field lists ───────────────────────────────────────────────────────
PKG_TIER1_FIELDS = [
    'package_type_application.package_type', 'package_type_application.intended_service',
    'performance_claims', 'sae_grades_documented', 'permitted_base_oils_restrictions',
    'route_selector_restrictions', 'treat_rate_matrix', 'required_co_components', 'published_formulations',
]
PKG_TIER2_FIELDS = [
    'tbn', 'sulfated_ash',
    'elements.Ca', 'elements.Mg', 'elements.Zn', 'elements.P',
    'elements.B', 'elements.Mo', 'elements.N', 'elements.S',
    'kv40', 'kv100', 'density', 'specific_gravity', 'flash_point', 'pour_point',
]
PKG_T2_FKEY = {
    'tbn': 'tbn', 'sulfated_ash': 'sulfated_ash',
    'elements.Ca': 'ca', 'elements.Mg': 'mg_elem', 'elements.Zn': 'zn', 'elements.P': 'p',
    'elements.B': 'b', 'elements.Mo': 'mo', 'elements.N': 'n', 'elements.S': 's',
    'kv40': 'kv40', 'kv100': 'kv100', 'density': 'density',
    'specific_gravity': 'specific_gravity', 'flash_point': 'flash_point', 'pour_point': 'pour_point',
}

BASE_T1_FIELDS = [
    'api_group_chemistry.api_group', 'api_group_chemistry.chemistry',
    'kv40', 'kv100', 'viscosity_index', 'density',
    'ccs_at_temp', 'ccs_temperature',
]
BASE_T1_FKEY = {
    'kv40': 'kv40', 'kv100': 'kv100', 'viscosity_index': 'viscosity_index',
    'density': 'density',
}

COMP_GEN_FIELDS = [
    'function.primary', 'function.secondary', 'chemical_family',
    'active_content', 'carrier.identity', 'carrier.share_wt_pct',
    'treat_rate', 'compatibility_restrictions',
    'function_specific_markers.tbn', 'function_specific_markers.ca',
    'function_specific_markers.mg', 'function_specific_markers.p',
    'function_specific_markers.zn', 'function_specific_markers.mo',
]
COMP_FKEY = {
    'function_specific_markers.tbn': 'tbn', 'function_specific_markers.ca': 'ca',
    'function_specific_markers.mg': 'mg_elem', 'function_specific_markers.p': 'p',
    'function_specific_markers.zn': 'zn', 'function_specific_markers.mo': 'mo',
}

# ── Per-class row builders ────────────────────────────────────────────
def package_rows(pk, text, sha, fname, rev):
    rows = []
    ext   = extract_numeric(text, PKG_PROPS)
    pkg_t = extract_package_type(text)
    tr    = extract_treat_rate(text)
    pc    = extract_performance_claims(text)
    sg    = extract_sae_grades(text)

    for f in PKG_TIER1_FIELDS:
        if f == 'package_type_application.package_type':
            rows.append(_text_field(pk, 'package_tier1', f, pkg_t, fname, sha, rev)
                        if pkg_t else _missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'performance_claims':
            rows.append(_text_field(pk, 'package_tier1', f, pc, fname, sha, rev)
                        if pc else _missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'sae_grades_documented':
            rows.append(_text_field(pk, 'package_tier1', f, sg, fname, sha, rev)
                        if sg else _missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'treat_rate_matrix':
            if tr:
                v_num = tr.replace('%', '').strip()
                rows.append(_reported(pk, 'package_tier1', f, tr, '%', '', v_num, '', 'typical', '', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        else:
            rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))

    for f in PKG_TIER2_FIELDS:
        rows.append(emit_numeric(pk, 'package_tier2', f, PKG_T2_FKEY.get(f, f), ext, fname, sha, rev))

    return rows

def base_oil_rows(pk, text, sha, fname, rev):
    rows = []
    ext   = extract_numeric(text, PKG_PROPS)
    ag    = extract_api_group(text)

    for f in BASE_T1_FIELDS:
        if f == 'api_group_chemistry.api_group':
            rows.append(_text_field(pk, 'base_oil_tier1', f, ag, fname, sha, rev)
                        if ag else _missing(pk, 'base_oil_tier1', f, fname, sha, rev))
        elif f == 'api_group_chemistry.chemistry':
            rows.append(_missing(pk, 'base_oil_tier1', f, fname, sha, rev))
        elif f in BASE_T1_FKEY:
            rows.append(emit_numeric(pk, 'base_oil_tier1', f, BASE_T1_FKEY[f], ext, fname, sha, rev))
        else:
            rows.append(_missing(pk, 'base_oil_tier1', f, fname, sha, rev))

    return rows

def component_rows(pk, text, sha, fname, rev):
    rows = []
    ext  = extract_numeric(text, PKG_PROPS)
    chem = extract_chem_family(text)
    tr   = extract_treat_rate(text)

    for f in COMP_GEN_FIELDS:
        if f == 'chemical_family':
            rows.append(_text_field(pk, 'component_general', f, chem, fname, sha, rev)
                        if chem else _missing(pk, 'component_general', f, fname, sha, rev))
        elif f == 'treat_rate':
            if tr:
                v_num = tr.replace('%', '').replace('-', '').strip().split('-')[0].strip()
                rows.append(_reported(pk, 'component_general', f, tr, '%', '', v_num, '', 'typical', '', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, 'component_general', f, fname, sha, rev))
        elif f in COMP_FKEY:
            rows.append(emit_numeric(pk, 'component_general', f, COMP_FKEY[f], ext, fname, sha, rev))
        else:
            rows.append(_missing(pk, 'component_general', f, fname, sha, rev))

    return rows

# ── Main loop ─────────────────────────────────────────────────────────
def main():
    rows   = []
    n_done = 0

    for pk in sorted(ELIGIBLE):
        doc_links = prod_docs.get(pk, [])
        info = decisions.get(pk, {})
        mc   = info.get('material_class', '')

        if not doc_links:
            if mc == 'base_oil':
                for f in BASE_T1_FIELDS:
                    rows.append(_missing(pk, 'base_oil_tier1', f, '', '', ''))
            elif mc == 'additive_component':
                for f in COMP_GEN_FIELDS:
                    rows.append(_missing(pk, 'component_general', f, '', '', ''))
            else:
                for f in PKG_TIER1_FIELDS + PKG_TIER2_FIELDS:
                    rows.append(_missing(pk, 'package_tier1', f, '', '', ''))
            n_done += 1
            continue

        link, text = select_best_doc(doc_links)
        if link is None:
            link_fallback = doc_links[0]
            sha   = link_fallback['sha256']
            fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
            rev   = get_rev_date(sha)
            if mc == 'base_oil':
                for f in BASE_T1_FIELDS:
                    rows.append(_missing(pk, 'base_oil_tier1', f, fname, sha, rev))
            elif mc == 'additive_component':
                for f in COMP_GEN_FIELDS:
                    rows.append(_missing(pk, 'component_general', f, fname, sha, rev))
            else:
                for f in PKG_TIER1_FIELDS + PKG_TIER2_FIELDS:
                    rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
            n_done += 1
            continue

        sha   = link['sha256']
        fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
        rev   = get_rev_date(sha)

        if mc == 'base_oil':
            rows.extend(base_oil_rows(pk, text, sha, fname, rev))
        elif mc == 'additive_component':
            rows.extend(component_rows(pk, text, sha, fname, rev))
        else:
            rows.extend(package_rows(pk, text, sha, fname, rev))

        n_done += 1

    write_rows('s15_lubimax.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
