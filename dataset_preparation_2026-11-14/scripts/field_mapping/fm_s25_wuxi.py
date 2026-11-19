"""Field-level mapping, S25 WUXI + MULTISOL.
22 eligible: 18 additive_component, 4 additive_package (decisions file: 20 comp, 6 pkg).

Doc format families:
  FORMAT_A : "Physical and Chemical Properties:" table (20 products, mostly WUXI SDS).
             3 columns: Property | Limit | Method.
             Values are spec limits: '350 max.', '245 min.', '0.90-1.05', '170 min.'
             Custom find_prop_full + _parse_wuxi preserve the min./max. qualifier.
             'Report' means no spec limit (value not given) -> Missing.
  FORMAT_B : "Typical Data" table (1 product, WUXI:WX3130 TDS).
             4 columns: Item | LimitTest | Typical | Method.
             After label: LimitTest ('Report' or '>=nnn') then Typical value.
             find_prop_full skips 'Report', returns first real numeric line.
  FORMAT_C : "Typical properties" table (1 product, MULTISOL:NOVAD B700, SDS).
             5 columns: Property | Unit | Typical | Method | Specification.
             Unit line ('kg/m3', 'mm2/s') contains a digit so stop condition
             is not triggered; find_prop_full reaches the typical value.

Writes field_evidence/s25_wuxi.csv.
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
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's25_wuxi.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].split(':')[0] in ('WUXI', 'MULTISOL')
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

# ── Section detection ─────────────────────────────────────────────────
def find_data_block(text):
    """Return (block, section_type).
    Priority: Section 9 / "Physical and chemical properties" (WUXI SDS),
    then "Typical Data" (WX3130 TDS), then "Typical properties" (MULTISOL SDS).
    """
    m = re.search(r'Physical\s+and\s+[Cc]hemical\s+[Pp]roperties', text, re.I)
    if m:
        after = text[m.end():]
        m10 = re.search(r'(?:SECTION|Section)\s+1[0-9][^0-9]|Storage and Handling', after)
        block = after[:m10.start()] if m10 else after[:2500]
        if len(block.strip()) > 30:
            return block, 'sec9'

    m2 = re.search(r'[Tt]ypical\s+[Dd]ata\b', text)
    if m2:
        return text[m2.end():m2.end()+2000], 'typical_data'

    m3 = re.search(r'[Tt]ypical\s+[Pp]roperties\b', text, re.I)
    if m3:
        return text[m3.end():m3.end()+2000], 'typical_props'

    return text[:2500], 'full_text'

# ── Numeric extraction ────────────────────────────────────────────────
def _extract_num(s):
    s = s.rstrip('\t').strip()
    s = re.sub(r'\([^)]*\)', '', s).strip()
    m = re.match(r'([<>≥≤]?=?\s*-?\d[\d.,]*)(?:\s*[-–]\s*-?\d[\d.,]*)?', s)
    if m:
        return m.group(0).strip()
    return ''

def _wrap(pat):
    return r'(?:' + pat + r')'

def find_prop_full(block, label_pat):
    """Return (full_value_line, label_line).
    Returns the full value line to preserve 'nnn min.'/'nnn max.' qualifiers.
    Skips 'Report'/'N/A' lines (-> Missing) and method-code lines.
    """
    m = re.search(_wrap(label_pat), block, re.I)
    if not m:
        return None
    label_line = m.group(0).strip()
    after = block[m.end():]
    for ln in after.split('\n')[1:16]:
        s = ln.strip().rstrip('\t').strip()
        if not s:
            continue
        if re.match(r'^\(', s):
            continue
        # Strip leading colon (SDS ": value" format)
        s = re.sub(r'^[:\s]+', '', s)
        # Skip 'Report' / 'N/A' — no value printed
        if s.lower() in ('report', 'n/a', 'nil', '-', 'n.d.', 'none', 'nd'):
            continue
        # Does this line contain a numeric value?
        if _extract_num(s):
            return s, label_line
        # Stop at a long label-like line with no digits
        if len(s) > 25 and re.match(r'^[A-Za-z]', s) and not re.search(r'\d', s):
            break
    return None

def _parse_wuxi(s):
    """Parse WUXI value line: handles 'nnn min.'/'nnn max.', ranges, bounds, typicals.
    Handles European decimal comma (MULTISOL).
    """
    s = s.strip().rstrip('.')  # strip trailing period (OCR artifact)
    s = re.sub(r'\([^)]*\)', '', s).strip()

    # Handle 'nnn min'/'nnn max' BEFORE unit extraction (prevents 'min'/'max' as unit)
    mq = re.match(r'^(-?\d+(?:[.,]\d+)?)\s*(min\.?|max\.?)\s*$', s, re.I)
    if mq:
        v = mq.group(1).replace(',', '.')
        is_max = 'max' in mq.group(2).lower()
        qual = '≤' if is_max else '≥'
        return v, qual, v if qual == '≥' else '', v if qual == '≤' else '', 'bound', ''

    # Extract trailing unit
    um = re.search(r'\s+([a-zA-Z°%][a-zA-Z/°%\s2*]*)\s*$', s)
    unit_v = um.group(1).strip() if um else ''
    if um:
        s = s[:um.start()].strip()

    # Range: nnn-mmm
    mr = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*[-–]\s*(-?\d+(?:[.,]\d+)?)', s)
    if mr:
        return '', '', mr.group(1).replace(',', '.'), mr.group(2).replace(',', '.'), 'range', unit_v

    # Bound: ≥/≤ nnn or >/< nnn
    mb = re.fullmatch(r'([<>≥≤]=?)\s*(-?\d+(?:[.,]\d+)?)', s)
    if mb:
        sym, v = mb.group(1), mb.group(2).replace(',', '.')
        q = {'<': '≤', '>': '≥', '>=': '≥', '<=': '≤', '≥': '≥', '≤': '≤'}.get(sym, sym)
        return '', q, v if q == '≥' else '', v if q == '≤' else '', 'bound', unit_v

    # Typical: plain number (handles European comma decimal like 1,0408)
    mn = re.fullmatch(r'-?\d+(?:[.,]\d+)?', s)
    if mn:
        return s.replace(',', '.'), '', '', '', 'typical', unit_v

    return '', '', '', '', 'text', unit_v

# ── Property patterns ─────────────────────────────────────────────────
# WUXI uses "KV@100" and "KV @ 40" notation; MULTISOL uses "Viscosity at 100"
PKG_PROPS = [
    (r'KV\s*@\s*100|[Vv]iscosity[^\n]*(,|@|at)\s*100|[Kk]inematic.*100',
                                             'kv100',          'cSt',      '100'),
    (r'KV\s*@\s*40|[Vv]iscosity[^\n]*(,|@|at)\s*40',
                                             'kv40',           'cSt',      '40'),
    (r'[Vv]iscosity\s+[Ii]ndex',            'viscosity_index','',         ''),
    (r'[Ss]pecific\s+[Gg]ravity',           'specific_gravity','',        ''),
    (r'[Dd]ensity\b',                        'density',        'g/cm3',   '20'),
    (r'[Ff]lash\s*[Pp]oint',                'flash_point',    '°C',       ''),
    (r'[Pp]our\s+[Pp]oint',                 'pour_point',     '°C',       ''),
    (r'TBN\b|[Tt]otal\s+[Bb]ase|[Bb]ase\s+[Nn]umber',
                                             'tbn',            'mg KOH/g', ''),
    (r'[Ss]ulfated\s+[Aa]sh|[Ss]ulphated\s+[Aa]sh',
                                             'sulfated_ash',   '%',        ''),
    # Elements — anchored to 'content' or 'm%' to avoid false matches on element names
    (r'[Cc]a\s+(?:content|m%)',             'ca',             '%',        ''),
    (r'[Cc]alcium\s+(?:content|%)',         'ca',             '%',        ''),
    (r'[Mm]g\s+(?:content|m%)',             'mg_elem',        '%',        ''),
    (r'[Mm]agnesium\s+(?:content|%)',       'mg_elem',        '%',        ''),
    (r'[Zz]n\s+(?:content|m%)',             'zn',             '%',        ''),
    (r'[Zz]inc\s+(?:content|%)',            'zn',             '%',        ''),
    (r'[Pp]\s+(?:content|m%)',              'p',              '%',        ''),
    (r'[Pp]hosphorus\s+(?:content|%)',      'p',              '%',        ''),
    (r'[Nn]\s+(?:content|m%)',              'n',              '%',        ''),
    (r'[Nn]itrogen\s+(?:content|%)',        'n',              '%',        ''),
    (r'[Ss]ulfur\s+(?:content|m%)|[Ss]ulphur\s+(?:content|m%)',
                                             's',              '%',        ''),
    (r'[Bb]oron\s+(?:content|%)',           'b',              '%',        ''),
    (r'[Mm]olybdenum\s+(?:content|%)',      'mo',             '%',        ''),
]

def extract_numeric(text, props):
    block, _ = find_data_block(text)
    results = {}
    for label_pat, fkey, default_unit, default_temp in props:
        if fkey in results:
            continue
        r = find_prop_full(block, label_pat)
        if r:
            raw, label_line = r
            results[fkey] = (raw, label_line, default_unit, default_temp)
    return results

# ── Text-field extractors ─────────────────────────────────────────────
def extract_treat_rate(text):
    for pat in [
        r'[Rr]ecommended\s+dose[^.]*?([\d.,]+)\s*[-–]\s*([\d.,]+)\s*%',
        r'[Rr]ecommended.*at\s+([\d.,]+)\s*%',
        r'[Tt]reat\s+[Rr]ate[:\s]+([\d.,]+)\s*%',
        r'at\s+([\d.,]+)\s*[-–]\s*([\d.,]+)\s*%',
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
        (r'[Mm]arine\s+[Cc]ylinder|[Mm]arine\s+[Oo]il', 'marine oil additive package'),
        (r'[Dd]iesel\s+[Ee]ngine\s+[Oo]il\s+[Aa]dditive', 'HDEO additive package'),
        (r'[Gg]asoline.*[Dd]iesel|[Dd]iesel.*[Gg]asoline', 'engine oil additive package'),
        (r'[Pp]assenger\s+[Cc]ar|PCMO', 'PCMO additive package'),
        (r'[Hh]eavy\s*[Dd]uty|HDEO', 'HDEO additive package'),
        (r'[Gg]ear\s+[Oo]il\b', 'gear oil additive package'),
        (r'[Hh]ydraulic', 'hydraulic oil additive package'),
        (r'[Ee]ngine\s+[Oo]il\s+[Aa]dditive', 'engine oil additive package'),
        (r'[Mm]otor\s+[Oo]il', 'engine oil additive package'),
        (r'[Cc]rankcase', 'crankcase oil additive package'),
    ]:
        if re.search(pat, text[:2000], re.I):
            return label
    return ''

def extract_chem_family(text):
    for pat, label in [
        (r'[Ss]ulfonate.*[Cc]alcium|[Cc]alcium.*[Ss]ulfonate|[Ss]ulphonate.*calcium', 'calcium sulfonate'),
        (r'[Pp]henate|[Pp]henol.*calcium|[Cc]alcium.*phenol', 'calcium phenate'),
        (r'zinc\s+dialkyl\s+dithiophosphate|ZDDP|zinc.*dithioph', 'zinc dialkyl dithiophosphate (ZDDP)'),
        (r'[Ss]uccinimide\s+[Dd]ispers|polyisobutylene succinimide', 'succinimide dispersant'),
        (r'[Pp]henolic.*[Aa]ntioxidant|[Hh]indered\s+[Pp]henol', 'hindered phenol antioxidant'),
        (r'[Dd]iphenylamine|[Aa]mine.*[Aa]ntioxidant', 'diphenylamine antioxidant'),
        (r'OCP|olefin\s*copolymer', 'olefin copolymer (OCP)'),
        (r'PMA|polymethacrylate', 'polymethacrylate (PMA)'),
        (r'[Pp]our\s+[Pp]oint\s+[Dd]ep', 'pour point depressant'),
        (r'[Vv]iscosity\s+[Mm]odifier', 'viscosity modifier'),
        (r'[Ee][Pp]\s+[Aa]dd|[Ee]xtreme.*[Pp]ressure', 'EP additive'),
        (r'[Cc]orrosion\s+[Ii]nhibit|metal.*deactiv', 'metal deactivator / corrosion inhibitor'),
        (r'[Rr]ust\s+[Ii]nhibit', 'rust inhibitor'),
        (r'[Dd]etergent', 'detergent'),
    ]:
        if re.search(pat, text[:3000], re.I):
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
        val, qual, lo, hi, vk, unit_v = _parse_wuxi(raw)
        unit = unit_v or default_unit
        if vk not in ('typical', 'bound', 'range'):
            return _missing(pk, tmpl, field, src_file, sha, rev)
        # val/lo/hi are already normalized (comma->period); raw is printed_text
        v_stored = val if vk == 'typical' else lo if (vk == 'bound' and qual == '≥') else hi if (vk == 'bound' and qual == '≤') else val
        return {'product_key': pk, 'template': tmpl, 'field': field,
                'entry': 'primary', 'value': v_stored, 'qualifier': qual, 'min': lo, 'max': hi,
                'value_kind': vk, 'printed_text': raw, 'unit': unit,
                'test_temperature_c': default_temp, 'method': '', 'conditions': '',
                'status': 'Reported', 'value_class': 'numeric',
                'basis': '', 'source_file': src_file, 'sha256': sha, 'page': '1',
                'revision_date': rev,
                'notes': f'From properties table: {label_line[:60]}', 'review': REVIEW}
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
                v_num = tr.replace('%', '').strip().split('-')[0].strip()
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

    write_rows('s25_wuxi.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
