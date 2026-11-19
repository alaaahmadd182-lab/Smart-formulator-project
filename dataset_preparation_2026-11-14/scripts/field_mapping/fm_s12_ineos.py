"""Field-level mapping, S12 INEOS (DURASYN PAO series).
22 eligible products: 22 base_oil.

Doc format families:
  FORMAT_A : "TYPICAL PROPERTIES" / "Typical Properties" table (19 products).
             4 columns: Property | ISO/ASTM Method | Typical Value | Typical Range.
             OCR reads row-by-row: label, then method, then typical, then range.
             Key issue: ISO method lines like "3104 / D445" start with a digit
             so _extract_num() would match "3104" instead of the actual value.
             Fix: skip lines matching digit+ / LetterCode (ISO std number / ASTM code).
  FORMAT_B : "Technical Data" table (3 products).
             3 columns: Property | Value | ASTM Method.
             Value comes immediately after label (before method), so standard
             strategy 2 finds it correctly without special handling.

All 22 are base_oil; BASE_T1_FIELDS emitted.

Writes field_evidence/s12_ineos.csv.
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
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's12_ineos.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('INEOS:')
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
    """Return (block, section_type)."""
    # "TYPICAL PROPERTIES" or "Typical Properties"
    m = re.search(r'[Tt]ypical\s+[Pp]roperties\b', text)
    if m:
        return text[m.end():m.end()+3000], 'typical_props'

    # "Technical Data" table
    m2 = re.search(r'Technical\s+Data\b', text, re.I)
    if m2:
        return text[m2.end():m2.end()+3000], 'tech_data'

    return text[:3000], 'full_text'

# ── Numeric extraction ────────────────────────────────────────────────
# ISO method number pattern: "3104 / D445" or "12185 / D4052"
_ISO_METHOD = re.compile(r'^\d+\s*/\s*[A-Z]')

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
    """Near-label scan; strategy 1 (same line) + strategy 2 (next 16 lines).
    Skips ISO method lines (e.g. '3104 / D445') that start with a digit.
    """
    m = re.search(_wrap(label_pat), block, re.I)
    if not m:
        return None
    label_line = m.group(0).strip()
    rest_of_line = block[m.end():].split('\n')[0]
    rest_clean = re.sub(r'^[\t:\s]+', '', rest_of_line).strip()
    if rest_clean and not _ISO_METHOD.match(rest_clean):
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
        # Skip ISO standard number / ASTM code lines
        if _ISO_METHOD.match(s):
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
# kv100 pattern before kv40 to avoid partial match of "100" on "40" label
BASE_PROPS = [
    (r'[Vv]iscosity[^\n]*(,|@|at)\s*100\s*[°?]',  'kv100',          'cSt',  '100'),
    (r'[Vv]iscosity[^\n]*(,|@|at)\s*40\s*[°?]',   'kv40',           'cSt',  '40'),
    (r'[Vv]iscosity\s+[Ii]ndex',                   'viscosity_index','',     ''),
    (r'[Ss]pecific\s+[Gg]ravity',                  'specific_gravity','',    '15.6'),
    (r'[Dd]ensity(?!\s+[Ii]ndex)',                 'density',        'kg/m3',''),
    (r'[Ff]lash\s*[Pp]oint',                       'flash_point',    '°C',   ''),
    (r'[Pp]our\s+[Pp]oint',                        'pour_point',     '°C',   ''),
    (r'[Nn]oack|[Vv]olatility',                    'noack',          '%',    ''),
    (r'[Cc][Cc][Ss]|[Cc]old\s+[Cc]rank',           'ccs',            'mPa.s',''),
]

def extract_numeric(text):
    block, _ = find_data_block(text)
    results = {}
    for label_pat, fkey, default_unit, default_temp in BASE_PROPS:
        if fkey in results:
            continue
        r = find_prop(block, label_pat)
        if r:
            raw, label_line = r
            results[fkey] = (raw, label_line, default_unit, default_temp)
    return results

def extract_api_group(text):
    for pat, label in [
        (r'PAO\b|polyalphaolefin|poly.alpha.olefin|poly\s+alpha\s+olefin', 'Group IV'),
        (r'Group\s+IV', 'Group IV'),
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

def emit_numeric(pk, field, fkey, extracted, src_file, sha, rev):
    if fkey in extracted:
        raw, label_line, default_unit, default_temp = extracted[fkey]
        val, qual, lo, hi, vk, unit_v = _parse(raw)
        unit = unit_v or default_unit
        if vk not in ('typical', 'bound', 'range'):
            return _missing(pk, 'base_oil_tier1', field, src_file, sha, rev)
        return _reported(pk, 'base_oil_tier1', field, raw, unit, qual, lo, hi, vk,
                         default_temp, src_file, sha, rev,
                         notes=f'From properties table: {label_line[:60]}')
    return _missing(pk, 'base_oil_tier1', field, src_file, sha, rev)

# ── Field list ────────────────────────────────────────────────────────
BASE_T1_FIELDS = [
    'api_group_chemistry.api_group', 'api_group_chemistry.chemistry',
    'kv40', 'kv100', 'viscosity_index', 'density',
    'ccs_at_temp', 'ccs_temperature',
]
# Maps template field -> fkey in extracted dict
# specific_gravity is extracted as 'specific_gravity' but maps to 'density' field
FIELD_FKEY = {
    'kv40': 'kv40', 'kv100': 'kv100', 'viscosity_index': 'viscosity_index',
    'density': ('density', 'specific_gravity'),  # try density first, then specific_gravity
}

def base_oil_rows(pk, text, sha, fname, rev):
    rows = []
    ext = extract_numeric(text)
    ag  = extract_api_group(text)

    for f in BASE_T1_FIELDS:
        if f == 'api_group_chemistry.api_group':
            rows.append(_text_field(pk, 'base_oil_tier1', f, ag, fname, sha, rev)
                        if ag else _missing(pk, 'base_oil_tier1', f, fname, sha, rev))
        elif f == 'api_group_chemistry.chemistry':
            rows.append(_missing(pk, 'base_oil_tier1', f, fname, sha, rev))
        elif f == 'density':
            # Try 'density' fkey first; fall back to 'specific_gravity'
            if 'density' in ext:
                rows.append(emit_numeric(pk, f, 'density', ext, fname, sha, rev))
            elif 'specific_gravity' in ext:
                rows.append(emit_numeric(pk, f, 'specific_gravity', ext, fname, sha, rev))
            else:
                rows.append(_missing(pk, 'base_oil_tier1', f, fname, sha, rev))
        elif f in FIELD_FKEY and not isinstance(FIELD_FKEY[f], tuple):
            rows.append(emit_numeric(pk, f, FIELD_FKEY[f], ext, fname, sha, rev))
        else:
            rows.append(_missing(pk, 'base_oil_tier1', f, fname, sha, rev))

    return rows

# ── Main loop ─────────────────────────────────────────────────────────
def main():
    rows   = []
    n_done = 0

    for pk in sorted(ELIGIBLE):
        doc_links = prod_docs.get(pk, [])

        if not doc_links:
            for f in BASE_T1_FIELDS:
                rows.append(_missing(pk, 'base_oil_tier1', f, '', '', ''))
            n_done += 1
            continue

        link, text = select_best_doc(doc_links)
        if link is None:
            link_fallback = doc_links[0]
            sha   = link_fallback['sha256']
            fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
            rev   = get_rev_date(sha)
            for f in BASE_T1_FIELDS:
                rows.append(_missing(pk, 'base_oil_tier1', f, fname, sha, rev))
            n_done += 1
            continue

        sha   = link['sha256']
        fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
        rev   = get_rev_date(sha)

        rows.extend(base_oil_rows(pk, text, sha, fname, rev))
        n_done += 1

    write_rows('s12_ineos.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
