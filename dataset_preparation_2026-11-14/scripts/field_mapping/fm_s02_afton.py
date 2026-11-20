"""Field-level mapping, S02 Afton Chemical.
101 eligible products (additive_package tier1+tier2 and additive_component general).
Sources: product bulletins and specification sheets from Afton archive.

Doc format families observed:
  BULLETIN : Multi-page product bulletin with 'Typical Characteristics' section.
             Label line (possibly with trailing tabs), value on next non-empty line.
             Method sometimes embedded in label (PMCC, COC).
  SPEC     : 'Sales Specification Sheet' with Min/Target/Max columns.
             Columns collapse in text extraction; extract by property order.
  SHORT    : Very short doc with no numeric data (all fields Missing).

Sources extracted programmatically from cached text-layer, 2026-11-19.
Writes field_evidence/s02_afton.csv.
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
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's02_afton.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('AFTON:')
            and r['stage2_identity']       == 'verified'
            and r['stage3_class_template'] == 'established'
            and r['stage5_field_mapping']  == 'not started'}

prod_docs = {}
for lk in links_raw:
    pk = lk['product_key']
    if pk in ELIGIBLE:
        prod_docs.setdefault(pk, []).append(lk)

REVIEW = 'TDS text read in full 2026-11-19; extraction from cached text-layer text'

# ── Cache reading ─────────────────────────────────────────────────────
def get_text(sha256):
    path = os.path.join(CACHE, sha256 + '.json.gz')
    if not os.path.exists(path):
        return ''
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        d = json.load(f)
    return '\n'.join(p.get('text', '') or '' for p in d.get('pages', []))

# ── Document selection ────────────────────────────────────────────────
def select_tds(doc_links):
    """Select primary TDS. Returns (primary_link, alt_links)."""
    tds = [lk for lk in doc_links
           if docs_inv.get(lk['sha256'], {}).get('document_type', '') in ('TDS/PDS', 'TDS')]
    if not tds:
        tds = doc_links
    if len(tds) == 1:
        return tds[0], []
    # Prefer longer doc (more data) among same type
    scored = []
    for lk in tds:
        t = get_text(lk['sha256'])
        scored.append((len(t), lk))
    scored.sort(key=lambda x: x[0], reverse=True)
    primary = scored[0][1]
    alts    = [s[1] for s in scored[1:]]
    return primary, alts

def get_rev_date(sha256):
    d = docs_inv.get(sha256, {})
    dates = d.get('printed_dates', '')
    if dates:
        return str(dates).split(',')[0].strip()
    return ''

# ── Format detection ──────────────────────────────────────────────────
def detect_format(text):
    if re.search(r'Sales Specification (?:Sheet|Characteristics)', text, re.I):
        return 'sales_spec'
    if re.search(r'Typical Characteristics', text, re.I):
        return 'bulletin'
    return 'short'

# ── TC block extraction ───────────────────────────────────────────────
def get_tc_block(text):
    """Find the actual Typical Characteristics section (not TOC reference).
    Returns (block_text, start_pos) or ('', -1)."""
    # Find all occurrences; use the one followed by actual property data
    for m in re.finditer(r'Typical Characteristics', text, re.I):
        after = text[m.end():m.end() + 1000]
        if re.search(r'(?:Appearance|Density|Viscosity|Flash\s+Point|TBN|Total\s+Base|Nitrogen|Phosphorus|Zinc|Boron|Specific\s+Gravity|Kinematic)',
                     after, re.I):
            # Extract until next major section
            end_m = re.search(
                r'\n(?:Handling Information|Performance Profile|Performance\s*\n|Recommended Dosage|Application\s*\n|Key Performance|Recommended Treat|Product (?:Introduction|Information)|Conclusion)',
                after, re.I)
            block = after[:end_m.start()] if end_m else after[:800]
            return block, m.end()
    return '', -1

# ── Value parsing ──────────────────────────────────────────────────────
def _parse(s):
    """Printed value string -> (value, qualifier, lo, hi, vk)"""
    s = s.strip()
    if not s:
        return '', '', '', '', 'text'
    # "120 min." or "120min." or "120 minimum" -> bound ≥
    m = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*(?:min\.?|minimum)', s, re.I)
    if m:
        return '', '≥', m.group(1).replace(',', '.'), '', 'bound'
    # "120 max." -> bound ≤
    m = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*(?:max\.?|maximum)', s, re.I)
    if m:
        return '', '≤', '', m.group(1).replace(',', '.'), 'bound'
    # "7.60 [0.910]" -> take value in [] (secondary unit)
    m = re.search(r'\[(-?\d+(?:[.,]\d+)?)\]', s)
    if m:
        return m.group(1).replace(',', '.'), '', '', '', 'typical'
    # "0.959 (g/ml)" -> strip parens unit
    m = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*(?:\([^)]*\))?', s)
    if m and m.group(1):
        return m.group(1).replace(',', '.'), '', '', '', 'typical'
    # Range "X-Y"
    m = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*[-–]\s*(-?\d+(?:[.,]\d+)?)', s)
    if m:
        return '', '', m.group(1).replace(',', '.'), m.group(2).replace(',', '.'), 'range'
    # Bound ≥X ≤X
    m = re.fullmatch(r'([≥≤])\s*(-?\d+(?:[.,]\d+)?)', s)
    if m:
        q, v = m.group(1), m.group(2).replace(',', '.')
        return '', q, v if q == '≥' else '', v if q == '≤' else '', 'bound'
    return '', '', '', '', 'text'

# ── Property label regex patterns ─────────────────────────────────────
# Maps field key -> regex matching the label in the TC block (case-insensitive)
PROP_RE = {
    'density':      r'Density\s*(?:at|@|,)\s*(?:15|20|60)',
    'sg':           r'Specific\s+Gravity\s*(?:@|at)\s*15',
    'kv100':        r'(?:Kinematic\s+)?Viscosity\s*(?:at|@|,)\s*100',
    'kv40':         r'(?:Kinematic\s+)?Viscosity\s*(?:at|@|,)\s*40',
    'flash_point':  r'Flash\s+Point',
    'tbn':          r'Total\s+Base\s+Number',
    'pour_point':   r'Pour\s+Point',
    'ca':           r'Calcium',
    'mg':           r'Magnesium',
    'zn':           r'Zinc',
    'p':            r'Phosphorus',
    'b':            r'Boron',
    'n':            r'Nitrogen',
    'mo':           r'Molybdenum',
    's':            r'Sulfur',
    'sulfated_ash': r'Sulfated\s+Ash',
}

# Maps field key -> unit as printed most commonly
UNIT_MAP = {
    'density':     'g/ml',
    'sg':          '',
    'kv100':       'cSt',
    'kv40':        'cSt',
    'flash_point': '°C',
    'tbn':         'mg KOH/g',
    'pour_point':  '°C',
    'ca':          '% wt',
    'mg':          '% wt',
    'zn':          '% wt',
    'p':           '% wt',
    'b':           '% wt',
    'n':           '% wt',
    'mo':          '% wt',
    's':           '% wt',
    'sulfated_ash':'% wt',
}

TEMP_MAP = {
    'density':     '15',
    'sg':          '15.6',
    'kv100':       '100',
    'kv40':        '40',
    'flash_point': '',
    'pour_point':  '',
}

def _extract_method_from_label(label_line):
    """Extract abbreviated method from label text, e.g. '(PMCC)' -> 'PMCC'."""
    m = re.search(r'\((PMCC|COC|ASTM[^)]*|ISO[^)]*)\)', label_line, re.I)
    if m:
        return m.group(1)
    return ''

def find_prop_in_block(block, prop_key):
    """Find value for a property in the TC block.
    Returns (printed_text, unit, qualifier, lo, hi, vk, method, label_line) or None."""
    pat = PROP_RE.get(prop_key)
    if not pat:
        return None
    m = re.search(pat + r'[^\n]*', block, re.I)
    if not m:
        return None
    label_line = m.group(0)
    pos = m.end()
    remaining = block[pos:]
    # Scan next lines for a value
    for line in remaining.split('\n')[:10]:
        line = line.strip()
        if not line:
            continue
        # Reject if it's another label (contains letter words > 3 chars)
        if re.match(r'^[A-Za-z]{4}', line) and not re.match(r'^[≥≤]?\s*\d', line):
            break
        # Check if it looks like a value
        if re.match(r'^(?:[≥≤<>]?\s*-?\d|\d|\[)', line):
            value, qual, lo, hi, vk = _parse(line)
            # Determine unit from label
            unit = ''
            u_m = re.search(r'(?:g/ml|g/cm3|kg/L|kg/m3|lbs/gal|cSt|mm2/s|mm\?/s|cP|mg KOH/g|%\s*(?:wt|weight|m%|M)|ppm|Sp\s*Gr)', label_line + ' ' + line, re.I)
            if u_m:
                unit = u_m.group(0).strip()
            else:
                unit = UNIT_MAP.get(prop_key, '')
            method = _extract_method_from_label(label_line)
            temp   = TEMP_MAP.get(prop_key, '')
            printed = line
            return printed, unit, qual, lo, hi, vk, method, label_line, temp
    return None

# ── Sales Spec Sheet extraction ───────────────────────────────────────
def extract_sales_spec(text):
    """Extract values from Sales Specification Sheet format.
    Returns dict: prop_key -> (printed, unit, qualifier, lo, hi, vk, method)"""
    results = {}
    # Props in common Sales Spec sheets
    spec_pats = {
        'flash_point': r'Flash\s+Pt\.?\s*,?\s*\?C\s*\(PMCC\)',
        'density':     r'Sp\.?\s*Gr\.?\s*@?\s*15\.6',
        'kv100':       r'Visc(?:osity)?\s*@?\s*100',
        'p':           r'Phosphorus',
        'b':           r'Boron',
        's':           r'Sulfur',
        'n':           r'Nitrogen',
    }
    # For each property, find Min/Target/Max by looking at the numeric block
    # Strategy: find all property lines, then find the numeric block after all instruments
    prop_order = []
    for key, pat in spec_pats.items():
        if re.search(pat, text, re.I):
            m = re.search(pat + r'[^\n]*', text, re.I)
            if m:
                prop_order.append((m.start(), key, m.group(0)))
    if not prop_order:
        return results
    prop_order.sort()
    n_props = len(prop_order)
    # Extract all numbers appearing in the text after the properties section
    # Find the numeric block: after the last instrument line
    last_prop_end = max(m_start for m_start, _, _ in prop_order) + 200
    after = text[last_prop_end:]
    # Extract number tokens
    nums = re.findall(r'(?<!\w)-?\d+(?:\.\d+)?(?!\w)', after)
    # Expect 3*n_props numbers (Min, Target, Max) but may have missing values
    # Try to pick the "Target" column (middle): index 1, 4, 7, ...
    target_vals = {}
    if len(nums) >= n_props:
        # Try sets of 3
        if len(nums) >= 3 * n_props:
            for i, (_, key, label) in enumerate(prop_order):
                idx = i * 3 + 1  # Target index
                if idx < len(nums):
                    v = nums[idx]
                    target_vals[key] = (v, label)
        else:
            # Just take the first n_props values
            for i, (_, key, label) in enumerate(prop_order):
                if i < len(nums):
                    target_vals[key] = (nums[i], label)
    for key, (v_str, label) in target_vals.items():
        value, qual, lo, hi, vk = _parse(v_str)
        unit = UNIT_MAP.get(key, '')
        method = _extract_method_from_label(label)
        temp = TEMP_MAP.get(key, '')
        results[key] = (v_str, unit, qual, lo, hi, vk, method, label, temp)
    return results

# ── Text-based extractors ─────────────────────────────────────────────
def extract_package_type(text):
    """Extract package type from title/subtitle."""
    # Look for the subtitle line after the main title
    patterns = [
        (r'Passenger Car (?:Engine|Motor) Oil (?:Additive|Package)', 'PCMO additive package'),
        (r'Heavy\s*Duty Diesel Engine Oil (?:Additive|Package)', 'HDEO additive package'),
        (r'Diesel Engine Oil (?:Additive|Package)', 'diesel engine oil additive package'),
        (r'(?:Automatic|Auto)\s*Transmission Fluid.*(?:Additive|Package)', 'ATF additive package'),
        (r'(?:Dual|Wet)\s*Clutch.*(?:Additive|Package|Fluid)', 'DCT/wet clutch additive package'),
        (r'(?:Manual|MT|MTF).*(?:Transmission|Gear).*(?:Additive|Package)', 'MTF/gear oil additive package'),
        (r'Gear\s*Oil.*(?:Additive|Package)', 'gear oil additive package'),
        (r'Hydraulic.*(?:Additive|Package)', 'hydraulic oil additive package'),
        (r'Industrial.*(?:Additive|Package)', 'industrial oil additive package'),
        (r'Turbine.*(?:Additive|Package)', 'turbine oil additive package'),
        (r'CVT.*(?:Additive|Package|Fluid)', 'CVT additive package'),
        (r'(?:Axle|Driveline).*(?:Additive|Package)', 'axle/driveline additive package'),
    ]
    for pat, label in patterns:
        if re.search(pat, text, re.I):
            return label
    # Fallback: look for explicit "X Additive Package" or "X Additive" near top
    m = re.search(r'\n([^\n]{5,80}(?:Additive Package|Additive|Package))', text[:800])
    if m:
        return m.group(1).strip()
    return ''

def extract_treat_rate(text):
    """Extract treat rate from intro / product description text.
    Returns (printed_text, lo, hi, vk) or None."""
    # "at a treat rate of 10.8 wt%" or "at X% weight"
    m = re.search(
        r'(?:at a treat rate of|recommended.*?treat rate of|at)\s+([\d.]+)\s*(?:wt%|wt\.?%|% weight|% wt)',
        text, re.I)
    if m:
        v = m.group(1)
        return f'{v}%', v, '', 'typical'
    # "at X% for" or "at X% with"
    m = re.search(r'\bat\s+([\d.]+)\s*%\s*(?:for|with|in|when)', text, re.I)
    if m:
        v = m.group(1)
        return f'{v}%', v, '', 'typical'
    # "treat-rate of X%" or "X% treat-rate"
    m = re.search(r'([\d.]+)\s*%\s*treat[- ]rate', text, re.I)
    if m:
        v = m.group(1)
        return f'{v}%', v, '', 'typical'
    m = re.search(r'treat[- ]rate.*?([\d.]+)\s*%', text, re.I)
    if m:
        v = m.group(1)
        return f'{v}%', v, '', 'typical'
    # "dosage of X%" or "dosage is X%"
    m = re.search(r'[Dd]osage\s+(?:of|is|at)\s+([\d.]+)\s*%', text)
    if m:
        v = m.group(1)
        return f'{v}%', v, '', 'typical'
    # Range: "X% to Y%" or "X-Y%"
    m = re.search(
        r'(?:treat rate of|at)\s+([\d.]+)\s*%?\s*(?:to|[-–])\s*([\d.]+)\s*%',
        text, re.I)
    if m:
        lo, hi = m.group(1), m.group(2)
        return f'{lo}-{hi}%', lo, hi, 'range'
    return None

def extract_performance_claims(text):
    """Extract performance standard claims (API, ACEA, OEM specs) from text."""
    claims = set()
    patterns = [
        r'API\s+[A-Z]{2,4}(?:[/-][A-Z]{2,4})*(?:\s*\d{4})?',
        r'ACEA\s+[A-Z]\d+(?:[/-][A-Z]\d+)*(?:-\d{2,4})?',
        r'ILSAC\s+GF-\d',
        r'dexos[12]?\s*(?:Gen\s*\d+)?',
        r'JASO\s+\w+',
        r'MB\s+22[0-9]\.\d+',
        r'VW\s+\d{3}\.\d{2}',
        r'BMW\s+LL-\d{2}',
        r'RN\s*\d{4}',
        r'MERCON[®\w]*(?:\s+LV)?',
        r'DEXRON[®\w]*(?:-\w+)?',
        r'ZF\s+\w+',
        r'MAN\s+\w+',
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, re.I):
            claims.add(m.group(0).strip())
    if claims:
        return '; '.join(sorted(claims))
    return ''

def extract_permitted_base_oils(text):
    """Extract base oil group info from text."""
    m = re.search(
        r'(?:in|with|using)\s+(Group\s*(?:I{1,3}|IV|V|III|II|I)(?:\s*(?:and|&|or|/|\+)?\s*Group\s*(?:I{1,3}|IV|V|III|II|I))*)',
        text, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(
        r'(Group\s*(?:I{1,3}|IV|V|III|II|I)(?:\s*(?:(?:and|&|or|/|\+)\s*)?(?:Group\s*)?(?:I{1,3}|IV|V|III|II|I))*\s*base\s*(?:oil|stock)s?)',
        text, re.I)
    if m:
        return m.group(1).strip()
    return ''

def extract_sae_grades(text):
    """Extract SAE viscosity grades mentioned in text."""
    grades = set()
    for m in re.finditer(r'(?:SAE\s+)?\b(?:\d+W[-–]\d+|\d+W|\d{2,3})\b', text):
        g = m.group(0).strip()
        if re.match(r'^\d+W[-–]\d+$|^\d+W$', g):
            grades.add('SAE ' + g if not g.startswith('SAE') else g)
    return ', '.join(sorted(grades)) if grades else ''

def extract_chem_family(text):
    """Extract chemical family / function description for components."""
    # Look for "HiTEC XXXX is a/an ..." sentence
    m = re.search(
        r'HiTEC[®?\s]+\S+\s+is\s+(?:a|an)\s+([^.]+\.)',
        text[:1500], re.I)
    if m:
        return m.group(1).strip()
    # From subtitle line "HiTEC® XXXX\nSubtitle"
    m = re.search(r'HiTEC[®?\s]+\S+\s*\n([^\n]{5,80})', text[:800])
    if m:
        return m.group(1).strip()
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
    return {
        'product_key': pk, 'template': tmpl, 'field': field,
        'entry': 'primary', 'value': lo if vk == 'bound' and qual == '≥' else hi if vk == 'bound' and qual == '≤' else printed,
        'qualifier': qual, 'min': lo, 'max': hi, 'value_kind': vk,
        'printed_text': printed, 'unit': unit, 'test_temperature_c': temp,
        'method': method, 'conditions': '',
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

# ── Package rows ──────────────────────────────────────────────────────
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

# Map tier2 field names to extraction keys
TIER2_KEY = {
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
    'specific_gravity': 'sg',
    'flash_point':  'flash_point',
    'pour_point':   'pour_point',
}

def package_rows(pk, text, sha, fname, rev, fmt):
    rows = []
    tmpl1 = 'package_tier1'
    tmpl2 = 'package_tier2'

    # ── Tier 1 ──
    pkg_type    = extract_package_type(text)
    perf_claims = extract_performance_claims(text)
    base_oils   = extract_permitted_base_oils(text)
    sae         = extract_sae_grades(text)
    tr          = extract_treat_rate(text)

    for f in PKG_TIER1_FIELDS:
        if f == 'package_type_application.package_type':
            if pkg_type:
                rows.append(_text_field(pk, tmpl1, f, pkg_type, fname, sha, rev))
            else:
                rows.append(_missing(pk, tmpl1, f, fname, sha, rev))
        elif f == 'package_type_application.intended_service':
            # Same info source as package_type
            rows.append(_missing(pk, tmpl1, f, fname, sha, rev))
        elif f == 'performance_claims':
            if perf_claims:
                rows.append(_text_field(pk, tmpl1, f, perf_claims, fname, sha, rev))
            else:
                rows.append(_missing(pk, tmpl1, f, fname, sha, rev))
        elif f == 'sae_grades_documented':
            if sae:
                rows.append(_text_field(pk, tmpl1, f, sae, fname, sha, rev))
            else:
                rows.append(_missing(pk, tmpl1, f, fname, sha, rev))
        elif f == 'permitted_base_oils_restrictions':
            if base_oils:
                rows.append(_text_field(pk, tmpl1, f, base_oils, fname, sha, rev))
            else:
                rows.append(_missing(pk, tmpl1, f, fname, sha, rev))
        elif f == 'treat_rate_matrix':
            if tr:
                printed, lo, hi, vk = tr
                qual = '' if vk == 'typical' else ''
                rows.append(_reported(pk, tmpl1, f, printed, '%', '', lo, hi, vk, '', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, tmpl1, f, fname, sha, rev))
        else:
            rows.append(_missing(pk, tmpl1, f, fname, sha, rev))

    # ── Tier 2 numeric ──
    if fmt == 'bulletin':
        block, _ = get_tc_block(text)
        extracted = {}
        for key in set(TIER2_KEY.values()):
            result = find_prop_in_block(block, key)
            if result:
                extracted[key] = result
    elif fmt == 'sales_spec':
        extracted = extract_sales_spec(text)
    else:
        extracted = {}

    for f in PKG_TIER2_FIELDS:
        key = TIER2_KEY.get(f, f)
        result = extracted.get(key)
        if result:
            printed, unit, qual, lo, hi, vk, method, label_line, temp = result
            rows.append(_reported(pk, tmpl2, f, printed, unit, qual, lo, hi, vk, temp, method,
                                  fname, sha, rev,
                                  notes=f'Extracted from TC block: {label_line.strip()[:80]}'))
        else:
            rows.append(_missing(pk, tmpl2, f, fname, sha, rev))
    return rows

# ── Component rows ────────────────────────────────────────────────────
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

# Component tier2 (VM) fields
COMP_VM_FIELDS = [
    'chemistry',
    'active_content',
    'carrier.identity',
    'carrier.share_wt_pct',
    'tested_dose_range_wt_pct',
    'pour_point_response',
    'low_temp_response',
    'compatibility_envelope',
    'addition_procedure.procedure',
    'addition_procedure.blend_temperature_c',
]

COMP_NUMERIC_FIELDS = {
    'function_specific_markers.tbn': 'tbn',
    'function_specific_markers.ca':  'ca',
    'function_specific_markers.mg':  'mg',
    'function_specific_markers.p':   'p',
    'function_specific_markers.zn':  'zn',
    'function_specific_markers.mo':  'mo',
}

def component_rows(pk, text, sha, fname, rev, fmt):
    rows = []
    tmpl = 'component_general'

    chem = extract_chem_family(text)
    tr   = extract_treat_rate(text)

    if fmt == 'bulletin':
        block, _ = get_tc_block(text)
        extracted = {}
        for key in set(COMP_NUMERIC_FIELDS.values()):
            result = find_prop_in_block(block, key)
            if result:
                extracted[key] = result
        # Also extract density/kv/flash for general properties if present
        for extra in ('density', 'kv100', 'kv40', 'flash_point'):
            result = find_prop_in_block(block, extra)
            if result:
                extracted[extra] = result
    else:
        extracted = {}

    for f in COMP_GEN_FIELDS:
        if f == 'chemical_family':
            if chem:
                rows.append(_text_field(pk, tmpl, f, chem, fname, sha, rev))
            else:
                rows.append(_missing(pk, tmpl, f, fname, sha, rev))
        elif f == 'treat_rate':
            if tr:
                printed, lo, hi, vk = tr
                rows.append(_reported(pk, tmpl, f, printed, '%', '', lo, hi, vk, '', '',
                                      fname, sha, rev))
            else:
                rows.append(_missing(pk, tmpl, f, fname, sha, rev))
        elif f in COMP_NUMERIC_FIELDS:
            key = COMP_NUMERIC_FIELDS[f]
            result = extracted.get(key)
            if result:
                printed, unit, qual, lo, hi, vk, method, label_line, temp = result
                rows.append(_reported(pk, tmpl, f, printed, unit, qual, lo, hi, vk, temp, method,
                                      fname, sha, rev,
                                      notes=f'From TC block: {label_line.strip()[:80]}'))
            else:
                rows.append(_missing(pk, tmpl, f, fname, sha, rev))
        else:
            rows.append(_missing(pk, tmpl, f, fname, sha, rev))
    return rows

# ── Main loop ─────────────────────────────────────────────────────────
def main():
    rows = []
    n_eligible = len(ELIGIBLE)
    n_done = 0

    for pk in sorted(ELIGIBLE):
        doc_links = prod_docs.get(pk, [])
        if not doc_links:
            # No documents at all
            info    = decisions.get(pk, {})
            mc      = info.get('material_class', '')
            tmpl_s  = info.get('template', '')
            is_comp = (mc == 'additive_component')
            fields  = COMP_GEN_FIELDS if is_comp else PKG_TIER1_FIELDS + PKG_TIER2_FIELDS
            tmpl    = 'component_general' if is_comp else 'package_tier1'
            for f in fields:
                rows.append(_missing(pk, tmpl, f, '', '', ''))
            n_done += 1
            continue

        primary, alts = select_tds(doc_links)
        sha   = primary['sha256']
        fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
        rev   = get_rev_date(sha)
        text  = get_text(sha)
        fmt   = detect_format(text)

        info   = decisions.get(pk, {})
        mc     = info.get('material_class', '')
        tmpl_s = info.get('template', '')
        is_comp = (mc == 'additive_component')

        if is_comp:
            rows.extend(component_rows(pk, text, sha, fname, rev, fmt))
        else:
            rows.extend(package_rows(pk, text, sha, fname, rev, fmt))

        n_done += 1

    write_rows('s02_afton.csv', rows)
    from collections import Counter
    status_ctr = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{n_eligible} products, {len(rows)} rows')
    print(f'  Reported: {status_ctr["Reported"]}, Missing: {status_ctr["Missing"]}')

if __name__ == '__main__':
    main()
