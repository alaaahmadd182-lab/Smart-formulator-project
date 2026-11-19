"""Field-level mapping, S21 MINGYUE (Jinzhou Mingyue Lubricant Additive).
19 eligible: 18 additive_component, 1 additive_package (MY-P3065).

Doc format families:
  FORMAT_A : "CHARACTERISTICS" table (most products, SDS docs).
             3 columns: Item | Specification | Test Method.
             OCR reads row by row: label\nvalue\nmethod\nlabel\nvalue...
             OCR issues: "kg/m3" splits to "kg/m\\n3)" and "mm2/s" to "mm\\n2/s)"
             Fix: skip OCR artifact lines matching /^digit+[/)]word*$/.
             Values may use "?" as range sep (900.0?920.0) or bound marker (?180=>=180).
             Preprocessing: (digit)?digit -> digit-digit (range), ?digit -> >=digit (bound).
  FORMAT_B : "Physical Characteristics" section (MY-P3065 additive package).
             Label (with method in parens) followed by value on next line.
             Same approach as FORMAT_A.
  FORMAT_C : SDS Section 9 (MY-T106A, MY-T106D).
             Standard label\nvalue format with "not available" for most properties.
             Flash Point and Density extractable.

Writes field_evidence/s21_mingyue.csv.
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
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's21_mingyue.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('MINGYUE:')
            and r['stage2_identity']       == 'verified'
            and r['stage3_class_template'] == 'established'
            and r['stage5_field_mapping']  == 'not started'}

prod_docs = {}
for lk in links_raw:
    pk = lk['product_key']
    if pk in ELIGIBLE:
        prod_docs.setdefault(pk, []).append(lk)

REVIEW = 'TDS/SDS text read in full 2026-11-19; extraction from cached text-layer'

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

# ── OCR preprocessing ─────────────────────────────────────────────────
def preprocess(block):
    """Fix MINGYUE OCR artefacts before extraction.
    1. digit?digit or digit ?digit -> range (900.0?920.0 -> 900.0-920.0)
    2. ?digit at value start -> >=digit (bound: ?180 -> >=180)
    """
    # Range: digit(s+?)digit -> digit-digit (with optional surrounding whitespace)
    block = re.sub(r'(\d)\s*\?\s*(\d)', r'\1-\2', block)
    # Bound: "?" immediately before a digit, not preceded by alphanumeric
    block = re.sub(r'(?<![a-zA-Z0-9])\?(\d)', r'≥\1', block)
    return block

# ── Section detection ─────────────────────────────────────────────────
def find_data_block(text):
    """Return (block, section_type).
    Priority: CHARACTERISTICS, Physical Characteristics, Section 9.
    """
    m = re.search(r'CHARACTERISTICS\b', text)
    if m:
        after = text[m.end():]
        m_end = re.search(r'PACKING AND HANDLING|STORAGE|storage and handling', after, re.I)
        block = after[:m_end.start()] if m_end else after[:2500]
        if len(block.strip()) > 30:
            return preprocess(block), 'characteristics'

    m2 = re.search(r'Physical\s+Characteristics\b', text, re.I)
    if m2:
        return preprocess(text[m2.end():m2.end()+2000]), 'phys_char'

    m3 = re.search(r'(?:SECTION|Section)\s+9[^0-9]|Physical and chemical properties', text, re.I)
    if m3:
        after = text[m3.end():]
        m10 = re.search(r'(?:SECTION|Section)\s+1[0-9][^0-9]', after)
        block = after[:m10.start()] if m10 else after[:2500]
        return preprocess(block), 'sec9'

    return preprocess(text[:2500]), 'full_text'

# ── Numeric extraction ────────────────────────────────────────────────
# OCR artifact pattern: short line like "3)" or "2/s)" from split "kg/m3" or "mm2/s"
_OCR_ARTIFACT = re.compile(r'^\d+[/\)][a-zA-Z0-9]*\)?$')

def _extract_num(s):
    s = s.rstrip('\t').strip()
    s = re.sub(r'\([^)]*\)', '', s).strip()
    m = re.match(r'([<>≥≤]?=?\s*-?\d[\d.,]*)(?:\s*[-–]\s*-?\d[\d.,]*)?', s)
    if m:
        return m.group(0).strip()
    return ''

def _wrap(pat):
    return r'(?:' + pat + r')'

def find_prop(block, label_pat):
    """Near-label scan; strategy 1 + strategy 2 (next 16 lines).
    Skips OCR artifacts (3), 2/s) from split exponent units.
    """
    m = re.search(_wrap(label_pat), block, re.I)
    if not m:
        return None
    label_line = m.group(0).strip()
    rest_of_line = block[m.end():].split('\n')[0]
    rest_clean = re.sub(r'^[\t:\s]+', '', rest_of_line).strip()
    if rest_clean and not _OCR_ARTIFACT.match(rest_clean):
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
        # Skip OCR artifact lines from split exponent units
        if _OCR_ARTIFACT.match(s):
            continue
        # Skip lines that are clearly method codes (GB/T, SH/T, ASTM, etc.)
        if re.match(r'^(?:GB|SH|Q|ASTM|DIN|IP|ISO|EN)\s*/?\w', s, re.I):
            continue
        # Skip 'not available' / 'not established' etc.
        if re.match(r'^[Nn]ot\s+(available|established|applicable|determined)', s):
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
    um = re.search(r'\s+([a-zA-Z°%][a-zA-Z/°%\s2*]*)\s*$', s)
    unit_v = um.group(1).strip() if um else ''
    if um:
        s = s[:um.start()].strip()
    mr = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*[-–]\s*(-?\d+(?:[.,]\d+)?)', s)
    if mr:
        return '', '', mr.group(1).replace(',', '.'), mr.group(2).replace(',', '.'), 'range', unit_v
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
# Combined patterns for both component and package
ALL_PROPS = [
    (r'[Kk]inematic\s+[Vv]iscosity|[Vv]iscosity,\s*cSt,?\s*100|[Vv]iscosity[^\n]*100\s*[°?]',
                                             'kv100',          'cSt',      '100'),
    (r'[Vv]iscosity,\s*cSt,?\s*40|[Vv]iscosity[^\n]*40\s*[°?]',
                                             'kv40',           'cSt',      '40'),
    (r'[Vv]iscosity\s+[Ii]ndex',            'viscosity_index','',         ''),
    (r'[Dd]ensity(?!\s*index)',              'density',        'kg/m3',    '20'),
    (r'[Ff]lash\s*[Pp]oint|[Ff]lashpoint',  'flash_point',    '°C',       ''),
    (r'[Pp]our\s+[Pp]oint',                 'pour_point',     '°C',       ''),
    (r'TBN\b|[Tt]otal\s+[Bb]ase\s+[Nn]umber',
                                             'tbn',            'mg KOH/g', ''),
    (r'[Ss]ulfated\s+[Aa]sh|[Ss]ulphated\s+[Aa]sh',
                                             'sulfated_ash',   '%',        ''),
    (r'[Cc]a\s*\(mass\)|[Cc]alcium\s*(?:\(mass\)|content|/?\s*%)',
                                             'ca',             '%',        ''),
    (r'[Mm]ag(?:nesium)?\s*(?:\(mass\)|content|/?\s*%)',
                                             'mg_elem',        '%',        ''),
    (r'[Zz]n\s*\(mass\)|[Zz]inc\s*(?:\(mass\)|content)',
                                             'zn',             '%',        ''),
    (r'[Pp]\s*\(mass\)|[Pp]hosphorus\s*(?:\(mass\)|content)',
                                             'p',              '%',        ''),
    (r'[Nn]\s*\(mass\)|[Nn]itrogen\s*(?:\(mass\)|content)',
                                             'n',              '%',        ''),
    (r'[Ss]\s*\(mass\)|[Ss]ulph?ur\s*(?:\(mass\)|content)',
                                             's',              '%',        ''),
]

def extract_numeric(text):
    block, _ = find_data_block(text)
    results = {}
    for label_pat, fkey, default_unit, default_temp in ALL_PROPS:
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
        r'[Dd]osage\s*\n\s*mass%\s*\n\s*([\d.]+)',
        r'[Dd]osage[:\s]+([\d.]+)\s*(?:mass)?%',
        r'[Rr]ecommended.*?(\d+)\s*[-–]\s*(\d+)\s*(?:mass)?\s*%',
        r'[Tt]reat\s+[Rr]ate[:\s]+([\d.]+)\s*%',
        r'at\s+([\d.]+)\s*[-–]\s*([\d.]+)\s*%',
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
                vmin, vmax = min(vals), max(vals)
                if 0.05 <= vmin <= 25:
                    if len(vals) >= 2 and vmax != vmin:
                        return f'{vmin}-{vmax}%'
                    return f'{vmin}%'
    return ''

def extract_chem_family(text):
    for pat, label in [
        (r'[Ss]ulfonate.*(?:[Cc]alcium|[Mm]agnesium)|(?:[Cc]alcium|[Mm]agnesium).*[Ss]ulfonate',
         lambda m: ('calcium' if 'calcium' in m.lower() or 'Ca' in m else 'magnesium') + ' sulfonate'),
        (r'[Cc]alcium\s+[Ss]ulphonate|[Cc]alcium\s+[Ss]ulfonate', 'calcium sulfonate'),
        (r'[Mm]agnesium\s+[Ss]ulph?onate', 'magnesium sulfonate'),
        (r'[Pp]henate|[Pp]henol.*(?:[Cc]alcium|[Mm]agnesium)', 'calcium phenate'),
        (r'ZDDP|zinc.*dithioph', 'zinc dialkyl dithiophosphate (ZDDP)'),
        (r'[Ss]uccinimide\s+[Dd]ispers|polyisobutylene succinimide', 'succinimide dispersant'),
        (r'[Pp]olyisobutylene\s+[Ss]uccin', 'succinimide dispersant'),
        (r'[Vv]iscosity\s+[Mm]odifier', 'viscosity modifier'),
        (r'[Pp]our\s+[Pp]oint\s+[Dd]ep', 'pour point depressant'),
        (r'[Dd]etergent', 'detergent'),
        (r'[Dd]ispers', 'dispersant'),
    ]:
        if callable(label):
            m = re.search(pat, text[:3000], re.I)
            if m:
                return label(m.group(0))
        else:
            if re.search(pat, text[:3000], re.I):
                return label
    return ''

def extract_package_type(text):
    for pat, label in [
        (r'[Cc]ar\s*&?\s*[Mm]otorcycle|JASO\s+MA', 'PCMO/motorcycle engine oil additive package'),
        (r'[Gg]asoline\s+[Ee]ngine\s+[Oo]il', 'PCMO additive package'),
        (r'[Dd]iesel\s+[Ee]ngine\s+[Oo]il', 'HDEO additive package'),
        (r'[Ee]ngine\s+[Oo]il\s+[Aa]dditive', 'engine oil additive package'),
        (r'[Gg]ear\s+[Oo]il', 'gear oil additive package'),
    ]:
        if re.search(pat, text[:2000], re.I):
            return label
    return ''

def extract_sae_grades(text):
    grades = set()
    for x in re.finditer(r'\b\d+W[-–]\d+|\b\d+W\b', text):
        g = x.group(0)
        if re.match(r'^\d+W[-–]\d+$|^\d+W$', g):
            grades.add(g)
    return ', '.join(sorted(grades))

def extract_performance_claims(text):
    claims = set()
    for pat in [r'API\s+[A-Z]{2,}(?:[/+][A-Z]{2,})*', r'ACEA\s+[A-Z]\d+(?:[-/][A-Z]\d+)*(?:-\d{2,4})?',
                r'ILSAC\s+GF-\d', r'JASO\s+\w+', r'dexos[12]?\b']:
        for x in re.finditer(pat, text, re.I):
            g = x.group(0).strip()
            if len(g) >= 5:
                claims.add(g)
    return '; '.join(sorted(claims))

# ── Row building ──────────────────────────────────────────────────────
def _missing(pk, tmpl, field, src_file, sha, rev):
    return {'product_key': pk, 'template': tmpl, 'field': field,
            'entry': 'primary', 'value': '', 'qualifier': '', 'min': '', 'max': '',
            'value_kind': '', 'printed_text': '', 'unit': '',
            'test_temperature_c': '', 'method': '', 'conditions': '',
            'status': 'Missing', 'value_class': 'numeric',
            'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '1',
            'revision_date': rev, 'notes': '', 'review': REVIEW}

def _reported(pk, tmpl, field, printed, unit, qual, lo, hi, vk, temp,
              src_file, sha, rev, notes=''):
    val = lo if (vk == 'bound' and qual == '≥') else hi if (vk == 'bound' and qual == '≤') else printed
    return {'product_key': pk, 'template': tmpl, 'field': field,
            'entry': 'primary', 'value': val, 'qualifier': qual, 'min': lo, 'max': hi,
            'value_kind': vk, 'printed_text': printed, 'unit': unit,
            'test_temperature_c': temp, 'method': '', 'conditions': '',
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
                         default_temp, src_file, sha, rev,
                         notes=f'From CHARACTERISTICS table: {label_line[:60]}')
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
    ext   = extract_numeric(text)
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
                v_num = tr.replace('%', '').strip().split('-')[0].strip()
                rows.append(_reported(pk, 'package_tier1', f, tr, '%', '', v_num, '', 'typical', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        else:
            rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))

    for f in PKG_TIER2_FIELDS:
        rows.append(emit_numeric(pk, 'package_tier2', f, PKG_T2_FKEY.get(f, f), ext, fname, sha, rev))

    return rows

def component_rows(pk, text, sha, fname, rev):
    rows = []
    ext  = extract_numeric(text)
    chem = extract_chem_family(text)
    tr   = extract_treat_rate(text)

    for f in COMP_GEN_FIELDS:
        if f == 'chemical_family':
            rows.append(_text_field(pk, 'component_general', f, chem, fname, sha, rev)
                        if chem else _missing(pk, 'component_general', f, fname, sha, rev))
        elif f == 'treat_rate':
            if tr:
                v_num = tr.replace('%', '').strip().split('-')[0].strip()
                rows.append(_reported(pk, 'component_general', f, tr, '%', '', v_num, '', 'typical', '',
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
            if mc == 'additive_component':
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
            if mc == 'additive_component':
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

        if mc == 'additive_component':
            rows.extend(component_rows(pk, text, sha, fname, rev))
        else:
            rows.extend(package_rows(pk, text, sha, fname, rev))

        n_done += 1

    write_rows('s21_mingyue.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
