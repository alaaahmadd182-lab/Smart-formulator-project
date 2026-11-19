"""Field-level mapping, S07 LANXESS (Additin series).
39 eligible products: 23 additive_component, 14 additive_package, 2 base_oil.

Doc format families:
  FORMAT_A : SDS "Physical and chemical properties" / Section 9.
             Standard LANXESS SDS: Property\n :\n value.
             Covers 15 direct sds_sec9 + 8 specifications products.
  FORMAT_B : "Technical data*" section (13 products, NO Section 9 in same doc).
             OCR reads 2-column table as: all labels (left col) first,
             then all values (right col). Values often start with
             "approx." or "typ." prefix.
             Extraction: paired chunk algorithm - find each label's
             position in the label sequence, map to same-index value.
  FORMAT_C : TDS/PDS brochure / technical report (3 products).
             No structured property table; mostly Missing.

Writes field_evidence/s07_lanxess.csv.
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
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's07_lanxess.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('LANXESS:')
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
    """Return (block, section_type). Section 9 tried before Technical Data."""
    # Section 9 / Physical and chemical properties
    m = re.search(r'(?:SECTION|Section)\s+9[^0-9]|PHYSICAL AND CHEMICAL PROPERTIES|Physical and chemical properties',
                  text, re.I)
    if m:
        after = text[m.end():]
        m10 = re.search(r'(?:SECTION|Section)\s+1[0-9][^0-9]', after)
        block = after[:m10.start()] if m10 else after[:3000]
        if len(block.strip()) > 50:
            return block, 'sds_sec9'

    # Typical properties (some docs)
    m2 = re.search(r'Typical\s+(?:chemical\s+and\s+)?(?:physical\s+)?[Pp]roperties', text, re.I)
    if m2:
        return text[m2.end():m2.end()+2000], 'typical_props'

    return '', 'none'

# ── Numeric extraction ────────────────────────────────────────────────
def _extract_num(s):
    s = s.rstrip('\t').strip()
    s = re.sub(r'\([^)]*\)', '', s).strip()
    m = re.match(r'([<>≥≤]?=?\s*-?\d[\d.,]*)(?:\s*[-–]\s*-?\d[\d.,]*)?', s)
    if m:
        return m.group(0).strip()
    return ''

def _strip_prefix(s):
    return re.sub(r'^(?:approx?\.?|typ(?:ical)?\.?|about|ca\.?|~)\s*', '', s, flags=re.I).strip()

def _wrap(pat):
    return r'(?:' + pat + r')'

def find_prop(block, label_pat):
    """Standard near-label scan; for Section 9 and typical-props format."""
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
    um = re.search(r'\s+([a-zA-Z°%][a-zA-Z/°% 2*]*)\s*$', s)
    unit_v = um.group(1).strip() if um else ''
    if um:
        s = s[:um.start()].strip()
    mr = re.fullmatch(r'(-?\d+(?:[.,]\d+)?)\s*[-–]\s*(-?\d+(?:[.,]\d+)?)', s)
    if mr:
        return '', '', mr.group(1), mr.group(2), 'range', unit_v
    mb = re.fullmatch(r'([<>≥≤]=?)\s*(-?\d+(?:[.,]\d+)?)', s)
    if mb:
        sym, v = mb.group(1), mb.group(2)
        q = {'<': '≤', '>': '≥', '>=': '≥', '<=': '≤', '≥': '≥', '≤': '≤'}.get(sym, sym)
        return '', q, v if q == '≥' else '', v if q == '≤' else '', 'bound', unit_v
    mn = re.fullmatch(r'-?\d+(?:[.,]\d+)?', s)
    if mn:
        return s, '', '', '', 'typical', unit_v
    return '', '', '', '', 'text', unit_v

# ── Technical Data paired extraction ─────────────────────────────────
# Keyword patterns that indicate a chunk is a property LABEL (not a value)
_LABEL_KW = re.compile(
    r'[Vv]iscosity|[Dd]ensity|[Ff]lash|[Pp]our|[Ss]ulphur|[Ss]ulfur'
    r'|[Nn]itrogen|[Pp]hosphorus|[Cc]alcium|[Zz]inc|[Mm]agnesium'
    r'|[Cc]omposition|[Aa]ppearance|[Cc]olou?r|[Cc]opper'
    r'|[Aa]ctive.*sulph|ASTM|ISO\s*\d|DIN\s|TBN|[Bb]ase.*[Nn]umber'
    r'|[Aa]sh|[Rr]efractive|[Pp]henol|[Ff]luidity|[Cc]loud', re.I
)

def _split_chunks(block):
    """Split block at blank/near-blank lines; return non-empty joined chunks."""
    chunks = []
    for chunk in re.split(r'\n[ \t\r]*\n', block):
        chunk = re.sub(r'\s+', ' ', chunk).strip()
        if chunk:
            chunks.append(chunk)
    return chunks

def parse_tech_data_paired(text, props):
    """Extract from LANXESS 2-col Technical Data via paired chunk algorithm.

    Left column (labels) appears first in OCR; right column (values) second.
    Both columns have the same number of entries.
    Strategy:
      - Split block at blank lines into chunks
      - Identify chunks matching property label keywords = label region
      - The last label chunk marks the transition; value region starts immediately after
      - For label at position rank-R (0-based), corresponding value = chunk at
        (last_label_chunk_idx + R)
    """
    m = re.search(r'Technical\s+[Dd]ata\b', text, re.I)
    if not m:
        return {}
    block = text[m.end():m.end()+3000]
    chunks = _split_chunks(block)
    if not chunks:
        return {}

    # Identify all label-like chunk indices
    label_idxs = [i for i, c in enumerate(chunks) if _LABEL_KW.search(c)]
    if not label_idxs:
        return {}

    last_lbl_idx = max(label_idxs)

    # For each property pattern, find its chunk and rank among all label_idxs
    results = {}
    for label_pat, fkey, default_unit, default_temp in props:
        if fkey in results:
            continue
        for i, chunk in enumerate(chunks):
            if i > last_lbl_idx:
                break
            if re.search(_wrap(label_pat), chunk, re.I):
                # Find rank of this chunk among label_idxs
                try:
                    rank = label_idxs.index(i)
                except ValueError:
                    rank = sum(1 for li in label_idxs if li < i)
                # Value is at chunk (last_lbl_idx + rank)
                val_idx = last_lbl_idx + rank
                if 0 <= val_idx < len(chunks):
                    val_raw = _strip_prefix(chunks[val_idx])
                    v = _extract_num(val_raw)
                    if v:
                        results[fkey] = (v, chunk.strip(), default_unit, default_temp)
                break
    return results

# ── Combined extraction ───────────────────────────────────────────────
PKG_PROPS = [
    (r'[Vv]iscosity[^)]*(?:at|@)\s*40|[Kk][Vv]\s*40|mm2/s.*40|40\s*[°]?C.*(?:cSt|mm)',
                                             'kv40',           'cSt',    '40'),
    (r'[Vv]iscosity[^)]*(?:at|@)\s*100|[Kk][Vv]\s*100|mm2/s.*100',
                                             'kv100',          'cSt',    '100'),
    (r'[Vv]iscosity\s+[Ii]ndex',             'viscosity_index','',       ''),
    (r'[Ss]pecific\s+[Gg]ravity',            'specific_gravity','',      ''),
    (r'[Dd]ensity(?!\s*[Gg]ravity)',         'density',        'g/cm3',  '20'),
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

# Base oil additionally needs kv40, kv100, VI from Section 9
BASE_OIL_PROPS = PKG_PROPS  # same patterns; kv40/kv100 patterns already cover it

def extract_numeric(text, props):
    """Try Section 9 first, then Technical Data paired extraction."""
    block, sec_type = find_data_block(text)
    results = {}
    if block:
        for label_pat, fkey, default_unit, default_temp in props:
            if fkey in results:
                continue
            r = find_prop(block, label_pat)
            if r:
                raw, label_line = r
                results[fkey] = (raw, label_line, default_unit, default_temp)

    # Supplement with Technical Data if any fields still missing
    if re.search(r'Technical\s+[Dd]ata\b', text, re.I):
        td_results = parse_tech_data_paired(text, props)
        for fkey, v in td_results.items():
            if fkey not in results:
                results[fkey] = v

    return results

# ── Text-field extractors ─────────────────────────────────────────────
def extract_treat_rate(text):
    for pat in [
        r'[Rr]ecommended.*at\s*([\d.,]+)\s*%',
        r'at\s+a?\s*([\d.,]+)\s*%\s+(?:wt|wt\.|weight|mass)',
        r'([\d.,]+)\s*%\s+(?:wt|wt\.|weight|mass)',
        r'[Tt]reat\s+[Ll]evel[:\s]*([\d.,]+)\s*%',
        r'at\s+([\d.,]+)\s*%\s+by\s+(?:weight|mass)',
    ]:
        m = re.search(pat, text[:3000], re.I)
        if m:
            try:
                v = float(m.group(1).replace(',', '.'))
                if 0.1 <= v <= 25:
                    return str(v) + '%'
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
        (r'Heavy\s*Duty|HDEO', 'HDEO additive package'),
        (r'[Gg]ear\s+[Oo]il\b', 'gear oil additive package'),
        (r'[Hh]ydraulic', 'hydraulic oil additive package'),
        (r'ATF|Automatic Transmission', 'ATF additive package'),
        (r'[Vv]iscosity\s+[Mm]odifier|VM\b', 'viscosity modifier'),
        (r'[Pp]our\s+[Pp]oint\s+[Dd]ep', 'pour point depressant'),
        (r'[Aa]ntioxidant', 'antioxidant additive'),
        (r'[Ee][Pp]\s+[Aa]dditive|[Ee]xtreme\s+[Pp]ressure', 'EP additive'),
        (r'[Ff]riction\s+[Mm]odifier', 'friction modifier'),
        (r'[Ss]ulphur.*carrier|[Ss]ulfur.*carrier', 'sulphur carrier EP additive'),
        (r'[Ii]ndustrial', 'industrial oil additive package'),
    ]:
        if re.search(pat, text[:2000], re.I):
            return label
    return ''

def extract_chem_family(text):
    for pat, label in [
        (r'dialkylpolysulphide|dialkyl\s*polysulfide', 'dialkyl polysulphide'),
        (r'[Ss]uccinimide\s+[Dd]ispers', 'succinimide dispersant'),
        (r'ZDDP|zinc.*thiophosphate|zinc.*dithiophosphate', 'ZDDP'),
        (r'[Ss]ulfonate.*[Cc]alcium|[Cc]alcium.*[Ss]ulfonate', 'calcium sulfonate'),
        (r'[Pp]henolic\s+[Aa]ntioxidant|[Hh]indered\s+[Pp]henol', 'hindered phenol antioxidant'),
        (r'[Dd]iphenylamine|[Aa]mine\s+[Aa]ntioxidant', 'diphenylamine antioxidant'),
        (r'[Ss]ulphurized|[Ss]ulfurized', 'sulphurized additive'),
        (r'[Ff]atty\s+[Aa]mine|organic\s+[Ff]riction\s+[Mm]odifier', 'organic friction modifier'),
        (r'PAO|poly.*alpha.*olefin|polyalphaolefin', 'PAO base oil'),
    ]:
        if re.search(pat, text[:3000], re.I):
            return label
    return ''

def extract_api_group(text):
    for pat, label in [
        (r'Group\s+IV|PAO\b|poly.alpha.olefin', 'Group IV'),
        (r'Group\s+V', 'Group V'),
        (r'Group\s+III', 'Group III'),
        (r'Group\s+II', 'Group II'),
        (r'Group\s+I', 'Group I'),
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
        val, qual, lo, hi, vk, unit_v = _parse(raw)
        unit = unit_v or default_unit
        if vk not in ('typical', 'bound', 'range'):
            return _missing(pk, tmpl, field, src_file, sha, rev)
        return _reported(pk, tmpl, field, raw, unit, qual, lo, hi, vk,
                         default_temp, '', src_file, sha, rev,
                         notes=f'From data section: {label_line[:60]}')
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
                v_str = tr.replace('%', '').strip()
                rows.append(_reported(pk, 'package_tier1', f, tr, '%', '', v_str, '', 'typical', '', '',
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
    ext   = extract_numeric(text, BASE_OIL_PROPS)
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
                v_str = tr.replace('%', '').strip()
                rows.append(_reported(pk, 'component_general', f, tr, '%', '', v_str, '', 'typical', '', '',
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

    write_rows('s07_lanxess.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
