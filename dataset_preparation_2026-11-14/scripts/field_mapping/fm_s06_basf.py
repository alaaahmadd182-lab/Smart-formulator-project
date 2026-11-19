"""Field-level mapping, S06 BASF.
72 eligible products: 34 base_oil (Group V synthetics: PAG, ester, polyol-ester),
12 additive_package, 26 additive_component.

Doc format families:
  FORMAT_A : Additive packages / components (IRGALUBE, IRGANOX, IRGASTAB, XPDL, …).
             Section "Typical chemical and physical properties".
             Tab-separated: Label<TAB>Value[unit]  (value may include unit).
  FORMAT_B : Base oils (BREOX, SYNATIVE, PLURACOL, PLURASAFE).
             Section "Physical data" or "Technical data".
             3-column: Characteristic<TAB>Unit<TAB>Value; method on next line in parens.
             Viscosity sub-property: "at 40 ?C<TAB><TAB>52" (parent header sets unit).
  FORMAT_C : Old BREOX/Cognis brochures.
             Section "TYPICAL PHYSICAL PROPERTIES".
             Whitespace-padded 3 cols: Property   Unit/Condition   Value.

Value artifacts in BASF text extraction:
  ??N   -> -N   (negative number, en-dash replaced by ??)
  A???B -> A–B  (range, en-dash replaced by ???)
  >?N   -> >N   (comparison qualifier)
  <?N   -> <N
  ? alone in unit positions = ° (degree sign) or trademark (ignore)

Sources extracted programmatically from cached text-layer, 2026-11-19.
Writes field_evidence/s06_basf.csv.
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
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's06_basf.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('BASF:')
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
    best = scored[0]
    return best[2], best[3]

def get_rev_date(sha256):
    d = docs_inv.get(sha256, {})
    dates = d.get('printed_dates', '')
    if dates:
        return str(dates).split(',')[0].strip()
    return ''

# ── Value string cleaning ─────────────────────────────────────────────
def clean_v(s):
    """Remove BASF PDF-extraction artifacts from a value string."""
    s = s.strip()
    # Remove thin space (U+2009) used in some BASF docs
    s = s.replace(' ', '')
    # °N where N is digit = negative number (PDF minus-sign rendering artifact)
    s = re.sub(r'^°(?=\d)', '-', s)
    # ??N -> -N (negative number via double question-mark)
    s = re.sub(r'^\?\?', '-', s)
    # A???B -> range: 'A-B'
    s = re.sub(r'(\d)\?\?\?(\d)', r'\1-\2', s)
    # A ? B -> range (single ? between numbers = en-dash)
    s = re.sub(r'(\d)\s*\?\s*(\d)', r'\1-\2', s)
    # Leading >? or <? -> > or <
    s = re.sub(r'([><])\?', r'\1', s)
    # Trailing ? after a digit
    s = re.sub(r'(\d)\?$', r'\1', s)
    return s.strip()

def _parse(s):
    """Value string -> (value, qualifier, lo, hi, vk, unit_from_val)"""
    s = clean_v(s)
    # Pull unit from end of string if present (e.g. "95 mm2/s", "1.02 g/cm3", "125 ?C (PM)")
    # Remove method in parens
    s = re.sub(r'\([^)]*\)', '', s).strip()
    # Extract unit suffix
    um = re.search(r'\s+([a-zA-Z°%][a-zA-Z/°% 2*]*)\s*$', s)
    unit_v = um.group(1).strip() if um else ''
    if um:
        s = s[:um.start()].strip()
    s = clean_v(s)
    # Range A-B or A ? B
    m = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*[-–]\s*(-?\d+(?:[.,]\d+)?)', s)
    if m:
        return '', '', m.group(1).replace(',','.'), m.group(2).replace(',','.'), 'range', unit_v
    # > / >= / < / <=
    m = re.fullmatch(r'([<>≥≤]=?)\s*(-?\d+(?:[.,]\d+)?)', s)
    if m:
        sym, v = m.group(1), m.group(2).replace(',','.')
        q = {'<': '≤', '>': '≥', '>=': '≥', '<=': '≤', '≥': '≥', '≤': '≤'}.get(sym, sym)
        lo = v if q == '≥' else ''
        hi = v if q == '≤' else ''
        return '', q, lo, hi, 'bound', unit_v
    # Plain number (possibly negative)
    m = re.fullmatch(r'-?\d+(?:[.,]\d+)?', s)
    if m:
        return s.replace(',','.'), '', '', '', 'typical', unit_v
    return '', '', '', '', 'text', unit_v

# ── Data section detection ────────────────────────────────────────────
SEC_PATTERNS = [
    ('typical_props', r'Typical\s+(?:chemical\s+and\s+)?(?:physical\s+)?[Pp]roperties'),
    ('technical_data', r'Technical\s+[Dd]ata'),
    ('physical_data',  r'Physical\s+[Dd]ata'),
    ('typ_phys_props', r'TYPICAL\s+PHYSICAL\s+PROPERTIES|Typical\s+Physical\s+Properties'),
    ('product_data',   r'Product\s+[Dd]ata'),  # often empty section
    ('sds_sec9',       r'(?:SECTION|Section)\s+9[^0-9]'),
]

def find_data_block(text):
    """Return (block_text, section_type) for the first usable data section."""
    for sec_type, pat in SEC_PATTERNS:
        m = re.search(pat, text, re.I)
        if not m:
            continue
        after = text[m.end():]
        # Skip 'product data are issued as a separate' (empty section)
        if sec_type == 'product_data' and re.search(r'are issued as a separate', after[:200], re.I):
            continue
        if sec_type == 'sds_sec9':
            # For SDS, grab Section 9 content until Section 10
            m10 = re.search(r'(?:SECTION|Section)\s*10[^0-9]', after)
            block = after[:m10.start()] if m10 else after[:2000]
        else:
            # Grab up to 2000 chars (plenty for property block)
            block = after[:2000]
        if len(block.strip()) > 50:
            return block, sec_type
    return '', 'none'

# ── Property extraction ───────────────────────────────────────────────
def _wrap(pat):
    """Wrap label pattern in non-capturing group to prevent | alternation escaping."""
    return r'(?:' + pat + r')'

def _extract_num(s):
    """Extract first numeric token from a line string. Returns string or ''."""
    # Remove trailing tab, method in parens, thin space
    s = s.rstrip('\t').strip().replace('\u2009', '')
    s = re.sub(r'\([^)]+\)', '', s).strip()
    # Apply BASF artifact cleaning
    s = clean_v(s)
    # Match a numeric value at start: optional qualifier, optional minus, digits
    # Qualifier ([<>≥≤]) is OPTIONAL — plain numbers like '52', '212' must also match
    m = re.match(r'([<>≥≤]?=?\s*-?\d[\d.,]*)(?:\s*[-–]\s*-?\d[\d.,]*)?', s)
    if m:
        return m.group(0).strip()  # return matched numeric portion (incl. range if present)
    return ''

def find_prop(block, label_pat):
    """Unified property extractor: find label, then return first numeric from same or next lines.

    Handles all BASF PDF table formats:
    - Each cell on its own line ending with \\t\\n (most BASF docs)
    - Inline tab-separated: Label\\tValue[unit] (some BASF docs like XPDL)
    - SDS Section 9 colon format: Label: value
    Returns (raw_value_str, label_line) or None.
    """
    m = re.search(_wrap(label_pat), block, re.I)
    if not m:
        return None
    label_line = m.group(0).strip()

    # Strategy 1: check the same line for a numeric value after the label match
    # e.g. "TBN\t150 ? 170 (ASTM D2896)" or "Label:\t95 mm2/s"
    rest_of_line = block[m.end():].split('\n')[0]
    # Strip leading tab/colon/space
    rest_clean = re.sub(r'^[\t:\s]+', '', rest_of_line).strip()
    if rest_clean:
        v = _extract_num(rest_clean)
        if v:
            return v, label_line

    # Strategy 2: scan next lines for the first numeric value
    # Handles cell-per-line format where value is 1-4 lines after the label
    after = block[m.end():]
    for ln in after.split('\n')[1:12]:
        s = ln.strip().rstrip('\t').strip()
        if not s:
            continue
        # Skip lines that look like method citations: "(ASTM D...)"
        if re.match(r'^\(', s):
            continue
        # Skip lines that are clearly unit-only or header-only (non-numeric letters only)
        # unless they might have a numeric somewhere
        v = _extract_num(s)
        if v:
            return v, label_line
        # Stop at next section header (long capitalized text without digits)
        if len(s) > 20 and re.match(r'^[A-Za-z]', s) and not re.search(r'\d', s):
            break
    return None

# ── Property definitions ──────────────────────────────────────────────
# (label_pat, field_key, default_unit, default_temp)
# For kv40/kv100: search directly for the temperature condition label
BASE_OIL_PROPS = [
    (r'(?:at|@)\s*40\s*[°?o]?C|cSt\s*@\s*40|mm2/s\s*@\s*40|\bKV\s*@\s*40|[Vv]iscosity\s*(?:at|@)\s*40',
                                                     'kv40',           'mm2/s', '40'),
    (r'(?:at|@)\s*100\s*[°?o]?C|cSt\s*@\s*100|mm2/s\s*@\s*100|\bKV\s*@\s*100|[Vv]iscosity\s*(?:at|@)\s*100',
                                                     'kv100',          'mm2/s', '100'),
    (r'[Vv]iscosity\s+[Ii]ndex',                    'viscosity_index','',      ''),
    (r'[Dd]ensity[;,]?\s*(?:(?:at\s+|@\s*)(?:20|15)|(?:20|15))?',
                                                     'density',        'g/cm3', '20'),
    (r'[Ss]pecific\s+[Gg]ravity',                   'specific_gravity','',     ''),
    (r'[Ff]lash\s+[Pp]oint',                        'flash_point',    '°C',    ''),
    (r'[Pp]our\s+[Pp]oint',                         'pour_point',     '°C',    ''),
]

PKG_COMP_PROPS = BASE_OIL_PROPS + [
    (r'TBN|[Tt]otal\s+[Bb]ase\s+[Nn]umber|[Bb]ase\s+[Nn]umber', 'tbn',  'mg KOH/g', ''),
    (r'[Ss]ulfated\s+[Aa]sh',                       'sulfated_ash',   '%',     ''),
    (r'[Cc]alcium',                                  'ca',             '%',     ''),
    (r'[Mm]agnesium',                                'mg',             '%',     ''),
    (r'[Zz]inc',                                     'zn',             '%',     ''),
    (r'[Pp]hosphorus',                               'p',              '%',     ''),
    (r'[Bb]oron',                                    'b',              '%',     ''),
    (r'[Mm]olybdenum',                               'mo',             '%',     ''),
    (r'[Nn]itrogen',                                 'n',              '%',     ''),
    (r'[Ss]ulfur(?!\s*ated)',                        's',              '%',     ''),
]

def extract_numeric(text, props):
    """Extract all properties. Returns dict field_key -> (raw_str, label, unit, temp)."""
    block, _sec_type = find_data_block(text)
    if not block:
        return {}
    results = {}
    for label_pat, fkey, default_unit, default_temp in props:
        if fkey in results:
            continue
        r = find_prop(block, label_pat)
        if r:
            raw, label_line = r
            results[fkey] = (raw, label_line, default_unit, default_temp)
    return results

# ── Treat rate / performance for packages / components ────────────────
def extract_treat_rate(text):
    for pat in [
        r'treat\s+(?:level|rate)[^\n]*?([\d.]+)\s*%',
        r'recommended[^\n]*?([\d.]+)\s*%',
        r'typical\s+treat[^\n]*?([\d.]+)\s*%',
        r'([\d.]+)\s*%\s+in\s+(?:mineral|base)\s+oil',
        r'0\.\d+\s*%',  # treat rates are usually < 2%
    ]:
        m = re.search(pat, text, re.I)
        if m:
            v = m.group(1) if m.lastindex else m.group(0).rstrip('%').strip()
            try:
                f = float(v)
                if 0.1 <= f <= 20:
                    return str(f) + '%'
            except Exception:
                pass
    return ''

def extract_performance_claims(text):
    claims = set()
    for pat in [r'API\s+[A-Z]{2,}(?:[/+][A-Z]{2,})*', r'ACEA\s+[A-Z]\d+(?:[-/][A-Z]\d+)*(?:-\d{2,4})?',
                r'ILSAC\s+GF-\d', r'dexos[12]?\b', r'JASO\s+\w+', r'DIN\s+51\s*\d+']:
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
        (r'PCMO|Passenger Car (?:Motor|Engine) Oil', 'PCMO additive package'),
        (r'Heavy\s*Duty|HDEO', 'HDEO additive package'),
        (r'[Tt]urbine', 'turbine oil additive package'),
        (r'[Cc]irculating', 'circulating oil additive package'),
        (r'[Gg]ear\s+[Oo]il|gear oil', 'gear oil additive package'),
        (r'[Hh]ydraulic', 'hydraulic oil additive package'),
        (r'ATF|Automatic Transmission', 'ATF additive package'),
        (r'[Vv]iscosity\s+[Mm]odifier|VM\b', 'viscosity modifier'),
        (r'[Pp]our\s+[Pp]oint\s+[Dd]ep', 'pour point depressant'),
        (r'[Aa]ntioxidant', 'antioxidant additive'),
        (r'[Cc]orrosion\s+[Ii]nhibit', 'corrosion inhibitor'),
        (r'TBN\s+[Bb]ooster|[Aa]shless.*[Bb]ooster', 'TBN booster'),
        (r'[Dd]etergent\s+[Ii]nhibit', 'DI additive package'),
        (r'[Ii]ndustrial', 'industrial oil additive package'),
    ]:
        if re.search(pat, text[:2000], re.I):
            return label
    return ''

def extract_chem_family(text):
    for pat, label in [
        (r'PAG|polyalkylene glycol|polyalkylenglycol', 'polyalkylene glycol (PAG)'),
        (r'polyol.ester|polyol ester|trimethylolpropane', 'synthetic polyol ester'),
        (r'TMP.ester|trimethylolpropane ester', 'trimethylolpropane ester'),
        (r'di.ester|diester', 'synthetic diester'),
        (r'phenolic\s+antioxidant|hindered phenol', 'hindered phenol antioxidant'),
        (r'amine\s+antioxidant|diphenylamine', 'diphenylamine antioxidant'),
        (r'thiocarbamate|dithiocarbamate', 'dithiocarbamate'),
        (r'phosphorothioate|zinc.*thiophosphate|ZDDP', 'ZDDP'),
        (r'boron.*ester|alkyl.*borate', 'boron ester'),
        (r'succinimide', 'succinimide dispersant'),
        (r'fatty\s+amine|oleyl\s+amine', 'fatty amine'),
    ]:
        if re.search(pat, text[:3000], re.I):
            return label
    return ''

def extract_api_group(text):
    """Derive API group from product description for base oils."""
    if re.search(r'Group\s+V|PAG|polyalkylene\s+glycol|ester\s+base|polyol.ester|diester|synthetic\s+ester', text[:2000], re.I):
        return 'V'
    if re.search(r'Group\s+IV|PAO|poly.?alpha.?olefin', text[:2000], re.I):
        return 'IV'
    if re.search(r'Group\s+III', text[:2000], re.I):
        return 'III'
    return ''

def extract_chemistry(text):
    """Derive chemistry description from product text."""
    for pat, label in [
        (r'PAG|polyalkylene glycol|polyalkylenglycol|poly(?:alkylene|oxyalkylene).*glycol', 'polyalkylene glycol (PAG)'),
        (r'polyol.ester|TMP.ester|trimethylolpropane', 'synthetic polyol ester'),
        (r'di.ester|diester|neopentyl|adipate', 'synthetic diester'),
        (r'poly.?alpha.?olefin|PAO', 'polyalphaolefin (PAO)'),
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
    val = lo if (vk=='bound' and qual=='≥') else hi if (vk=='bound' and qual=='≤') else printed
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
    """Emit one row for a numeric field, Reported if found else Missing."""
    if fkey in extracted:
        raw, label_line, default_unit, default_temp = extracted[fkey]
        val, qual, lo, hi, vk, unit_v = _parse(raw)
        unit = unit_v or default_unit
        if vk not in ('typical', 'bound', 'range'):
            return _missing(pk, tmpl, field, src_file, sha, rev)
        return _reported(pk, tmpl, field, raw, unit, qual, lo, hi, vk, default_temp, '',
                         src_file, sha, rev,
                         notes=f'From data section: {label_line[:60]}')
    return _missing(pk, tmpl, field, src_file, sha, rev)

# ── Field lists ───────────────────────────────────────────────────────
BASE_TIER1_FIELDS = [
    'api_group_chemistry.api_group',
    'api_group_chemistry.chemistry',
    'kv40', 'kv100', 'viscosity_index', 'density', 'specific_gravity', 'ccs',
]
BASE_TIER2_FIELDS = ['mrv', 'noack_volatility', 'pour_point', 'flash_point']
BASE_TIER3_FIELDS = ['sulfur', 'saturates', 'aromatics', 'cloud_point', 'wax_content']

BASE_FKEY = {
    'kv40': 'kv40', 'kv100': 'kv100', 'viscosity_index': 'viscosity_index',
    'density': 'density', 'specific_gravity': 'specific_gravity',
    'ccs': 'ccs', 'mrv': 'mrv', 'noack_volatility': 'noack_volatility',
    'pour_point': 'pour_point', 'flash_point': 'flash_point',
    'sulfur': 's', 'saturates': 'saturates', 'aromatics': 'aromatics',
    'cloud_point': 'cloud_point', 'wax_content': 'wax_content',
}

PKG_TIER1_FIELDS = [
    'package_type_application.package_type',
    'package_type_application.intended_service',
    'performance_claims', 'sae_grades_documented',
    'permitted_base_oils_restrictions', 'route_selector_restrictions',
    'treat_rate_matrix', 'required_co_components', 'published_formulations',
]
PKG_TIER2_FIELDS = [
    'tbn', 'sulfated_ash',
    'elements.Ca', 'elements.Mg', 'elements.Zn', 'elements.P',
    'elements.B', 'elements.Mo', 'elements.N', 'elements.S',
    'kv40', 'kv100', 'density', 'specific_gravity', 'flash_point', 'pour_point',
]
PKG_T2_FKEY = {
    'tbn': 'tbn', 'sulfated_ash': 'sulfated_ash',
    'elements.Ca': 'ca', 'elements.Mg': 'mg', 'elements.Zn': 'zn', 'elements.P': 'p',
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
    'function_specific_markers.mg': 'mg', 'function_specific_markers.p': 'p',
    'function_specific_markers.zn': 'zn', 'function_specific_markers.mo': 'mo',
}

# ── Per-class row builders ────────────────────────────────────────────
def base_oil_rows(pk, text, sha, fname, rev):
    rows = []
    ext  = extract_numeric(text, BASE_OIL_PROPS)
    api  = extract_api_group(text)
    chem = extract_chemistry(text)

    for f in BASE_TIER1_FIELDS:
        if f == 'api_group_chemistry.api_group':
            if api:
                rows.append(_text_field(pk, 'base_oil_tier1', f, api, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'base_oil_tier1', f, fname, sha, rev))
        elif f == 'api_group_chemistry.chemistry':
            if chem:
                rows.append(_text_field(pk, 'base_oil_tier1', f, chem, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'base_oil_tier1', f, fname, sha, rev))
        else:
            fkey = BASE_FKEY.get(f, f)
            rows.append(emit_numeric(pk, 'base_oil_tier1', f, fkey, ext, fname, sha, rev))

    for f in BASE_TIER2_FIELDS:
        fkey = BASE_FKEY.get(f, f)
        rows.append(emit_numeric(pk, 'base_oil_tier2', f, fkey, ext, fname, sha, rev))

    for f in BASE_TIER3_FIELDS:
        fkey = BASE_FKEY.get(f, f)
        rows.append(emit_numeric(pk, 'base_oil_tier3', f, fkey, ext, fname, sha, rev))

    return rows

def package_rows(pk, text, sha, fname, rev):
    rows = []
    ext  = extract_numeric(text, PKG_COMP_PROPS)
    pkg_t = extract_package_type(text)
    tr    = extract_treat_rate(text)
    pc    = extract_performance_claims(text)
    sg    = extract_sae_grades(text)

    for f in PKG_TIER1_FIELDS:
        if f == 'package_type_application.package_type':
            if pkg_t:
                rows.append(_text_field(pk, 'package_tier1', f, pkg_t, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'performance_claims':
            if pc:
                rows.append(_text_field(pk, 'package_tier1', f, pc, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'sae_grades_documented':
            if sg:
                rows.append(_text_field(pk, 'package_tier1', f, sg, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        elif f == 'treat_rate_matrix':
            if tr:
                v_str = tr.replace('%','').strip()
                rows.append(_reported(pk, 'package_tier1', f, tr, '%', '', v_str, '', 'typical', '', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))
        else:
            rows.append(_missing(pk, 'package_tier1', f, fname, sha, rev))

    for f in PKG_TIER2_FIELDS:
        fkey = PKG_T2_FKEY.get(f, f)
        rows.append(emit_numeric(pk, 'package_tier2', f, fkey, ext, fname, sha, rev))

    return rows

def component_rows(pk, text, sha, fname, rev):
    rows = []
    ext  = extract_numeric(text, PKG_COMP_PROPS)
    chem = extract_chem_family(text)
    tr   = extract_treat_rate(text)

    for f in COMP_GEN_FIELDS:
        if f == 'chemical_family':
            if chem:
                rows.append(_text_field(pk, 'component_general', f, chem, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'component_general', f, fname, sha, rev))
        elif f == 'treat_rate':
            if tr:
                v_str = tr.replace('%','').strip()
                rows.append(_reported(pk, 'component_general', f, tr, '%', '', v_str, '', 'typical', '', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, 'component_general', f, fname, sha, rev))
        elif f in COMP_FKEY:
            fkey = COMP_FKEY[f]
            rows.append(emit_numeric(pk, 'component_general', f, fkey, ext, fname, sha, rev))
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
                for f in BASE_TIER1_FIELDS:
                    rows.append(_missing(pk, 'base_oil_tier1', f, '', '', ''))
            elif mc == 'additive_component':
                for f in COMP_GEN_FIELDS:
                    rows.append(_missing(pk, 'component_general', f, '', '', ''))
            else:
                for f in PKG_TIER1_FIELDS:
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
                for f in BASE_TIER1_FIELDS + BASE_TIER2_FIELDS + BASE_TIER3_FIELDS:
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

    write_rows('s06_basf.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
