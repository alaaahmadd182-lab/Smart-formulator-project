"""Field-level mapping, S10 BRB International.
51 eligible products: 33 additive_component, 18 additive_package.

Doc format families:
  FORMAT_A : "Typical Data" section (product data sheets).
             Table: Parameter | Test method | Unit | Value
             OCR layout: each row split as 4 lines (parameter, method, unit, value).
             Comma decimal (0,901 -> 0.901).
  FORMAT_B : "Typical chemical and physical properties" section (some SDS docs).
             Same BRB property: value line format.
  FORMAT_C : SDS Section 9 "Physical and chemical properties".
  FORMAT_D : Performance/specifications doc (no numeric data table).

Writes field_evidence/s10_brb.csv.
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
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's10_brb.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('BRB:')
            and r['stage2_identity']       == 'verified'
            and r['stage3_class_template'] == 'established'
            and r['stage5_field_mapping']  == 'not started'}

prod_docs = {}
for lk in links_raw:
    pk = lk['product_key']
    if pk in ELIGIBLE:
        prod_docs.setdefault(pk, []).append(lk)

REVIEW = 'TDS/SDS text read in full 2026-11-19; extraction from cached text-layer'

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

# ── Data section detection ────────────────────────────────────────────
def find_data_block(text):
    """Return (block_text, section_type)."""
    # FORMAT_A: BRB "Typical Data" section
    m_td = re.search(r'Typical\s+Data\b', text, re.I)
    if m_td:
        return text[m_td.end():m_td.end()+2000], 'typical_data'

    # FORMAT_B: "Typical chemical/physical properties"
    m_typ = re.search(r'Typical\s+(?:chemical\s+and\s+)?(?:physical\s+)?[Pp]roperties', text, re.I)
    if m_typ:
        return text[m_typ.end():m_typ.end()+2000], 'typical_props'

    # Technical Data section
    m_tech = re.search(r'Technical\s+[Dd]ata\b', text, re.I)
    if m_tech:
        return text[m_tech.end():m_tech.end()+2000], 'technical_data'

    # FORMAT_C: SDS Section 9
    m_sds = re.search(
        r'(?:SECTION|Section)\s+9[^0-9]|PHYSICAL AND CHEMICAL PROPERTIES|Physical and chemical properties',
        text, re.I)
    if m_sds:
        after = text[m_sds.end():]
        m10 = re.search(r'(?:SECTION|Section)\s+1[0-9][^0-9]', after)
        block = after[:m10.start()] if m10 else after[:3000]
        if len(block.strip()) > 50:
            return block, 'sds_sec9'

    return '', 'none'

# ── Number extraction ─────────────────────────────────────────────────
def _clean_brb_num(s):
    """Space as thousands separator in BRB numbers."""
    return re.sub(r'(\d)\s+(\d)', r'\1\2', s)

def _extract_num(s):
    s = s.rstrip('\t').strip()
    s = re.sub(r'\([^)]*\)', '', s).strip()
    s = _clean_brb_num(s)
    m = re.match(r'([<>≥≤]?=?\s*-?\d[\d.,]*)(?:\s*[-–]\s*-?\d[\d.,]*)?', s)
    if m:
        return m.group(0).strip()
    return ''

def _wrap(pat):
    return r'(?:' + pat + r')'

def find_prop(block, label_pat):
    """Find label, return (raw_value, label_line) or None."""
    m = re.search(_wrap(label_pat), block, re.I)
    if not m:
        return None
    label_line = m.group(0).strip()

    # Strategy 1: check same line
    rest_of_line = block[m.end():].split('\n')[0]
    rest_clean = re.sub(r'^[\t:\s]+', '', rest_of_line).strip()
    if rest_clean:
        v = _extract_num(rest_clean)
        if v:
            return v, label_line

    # Strategy 2: scan next lines
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
    """Value string -> (value, qualifier, lo, hi, vk)."""
    s = s.strip()
    s = re.sub(r'\([^)]*\)', '', s).strip()
    s = _clean_brb_num(s).strip()
    um = re.search(r'\s+([a-zA-Z°%][a-zA-Z/°% 2*]*)\s*$', s)
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
        lo = v if q == '≥' else ''
        hi = v if q == '≤' else ''
        return '', q, lo, hi, 'bound', unit_v
    mn = re.fullmatch(r'-?\d+(?:[.,]\d+)?', s)
    if mn:
        return s.replace(',', '.'), '', '', '', 'typical', unit_v
    return '', '', '', '', 'text', unit_v

# ── Property definitions ──────────────────────────────────────────────
# BRB reports: Density @ 20°C (Kg/l), Flashpoint/Flash Point, Viscosity @ 20°C (mPa.s, dynamic)
# kv40/kv100 (kinematic at 40/100°C) are present for some additive packages
PKG_PROPS = [
    (r'[Vv]iscosity[^)]*(?:at|@)\s*40|mm2/s[^)]*40|cSt.*40|KV.*40',
                                             'kv40',           'cSt',    '40'),
    (r'[Vv]iscosity[^)]*(?:at|@)\s*100|mm2/s[^)]*100|cSt.*100|KV.*100',
                                             'kv100',          'cSt',    '100'),
    (r'[Vv]iscosity\s+[Ii]ndex',             'viscosity_index','',       ''),
    (r'[Ss]pecific\s+[Gg]ravity',            'specific_gravity','',      ''),
    (r'[Dd]ensity(?!\s*[Gg]ravity)',         'density',        'g/cm3',  '20'),
    (r'[Ff]lash\s*[Pp]oint|[Ff]lashpoint',  'flash_point',    '°C',     ''),
    (r'[Pp]our\s+[Pp]oint',                  'pour_point',     '°C',     ''),
    (r'[Bb]ase\s+[Nn]umber|TBN\b|[Tt]otal\s+[Bb]ase',
                                             'tbn',            'mg KOH/g',''),
    (r'[Ss]ulfated\s+[Aa]sh',               'sulfated_ash',   '%',      ''),
    (r'[Cc]alcium\b',                        'ca',             '%',      ''),
    (r'[Mm]agnesium\b',                      'mg_elem',        '%',      ''),
    (r'[Zz]inc\b',                           'zn',             '%',      ''),
    (r'[Pp]hosphorus\b',                     'p',              '%',      ''),
    (r'[Bb]oron\b',                          'b',              '%',      ''),
    (r'[Mm]olybdenum\b',                     'mo',             '%',      ''),
    (r'[Nn]itrogen\b',                       'n',              '%',      ''),
    (r'[Ss]ulfur(?!\s*ated)\b',              's',              '%',      ''),
]

def extract_numeric(text, props):
    block, _sec = find_data_block(text)
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

# ── Text-field extractors ─────────────────────────────────────────────
def extract_treat_rate(text):
    for pat in [
        r'([\d.,]+)\s*(?:to|and|-)\s*([\d.,]+)\s*%\s*(?:wt|wt\.|weight)',
        r'at\s+a?\s*([\d.,]+)\s*%\s+(?:wt|wt\.|weight)',
        r'([\d.,]+)\s*%\s+(?:wt|wt\.|weight)',
        r'[Rr]ecommended.*at\s+([\d.,]+)\s*%',
        r'at\s+([\d.,]+)\s*%\s+by\s+(?:weight|mass)',
        r'[Tt]reat\s+[Ll]evel[:\s]+([\d.,]+)\s*%',
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
        (r'Passenger Car (?:Motor|Engine) Oil|PCMO', 'PCMO additive package'),
        (r'Heavy\s*Duty|HDEO', 'HDEO additive package'),
        (r'[Gg]ear\s+[Oo]il\b', 'gear oil additive package'),
        (r'[Hh]ydraulic', 'hydraulic oil additive package'),
        (r'ATF|Automatic Transmission', 'ATF additive package'),
        (r'[Vv]iscosity\s+[Mm]odifier|VM\b', 'viscosity modifier'),
        (r'[Pp]our\s+[Pp]oint\s+[Dd]ep', 'pour point depressant'),
        (r'[Aa]ntioxidant', 'antioxidant additive'),
        (r'[Cc]orrosion\s+[Ii]nhibit', 'corrosion inhibitor'),
        (r'[Ff]oam\s+[Ii]nhibit', 'foam inhibitor'),
        (r'[Ii]ndustrial\s+[Gg]ear', 'industrial gear oil additive'),
        (r'[Ii]ndustrial', 'industrial oil additive package'),
    ]:
        if re.search(pat, text[:2000], re.I):
            return label
    return ''

def extract_chem_family(text):
    for pat, label in [
        (r'[Ss]uccinimide\s+[Dd]ispers', 'succinimide dispersant'),
        (r'ZDDP|zinc.*thiophosphate|zinc.*dithiophosphate', 'ZDDP'),
        (r'[Ss]ulfonate.*[Cc]alcium|[Cc]alcium.*[Ss]ulfonate', 'calcium sulfonate'),
        (r'[Pp]henolic\s+[Aa]ntioxidant|[Hh]indered\s+[Pp]henol', 'hindered phenol antioxidant'),
        (r'[Dd]iphenylamine|[Aa]mine\s+[Aa]ntioxidant', 'diphenylamine antioxidant'),
        (r'[Ss]ulfurized', 'sulfurized additive'),
        (r'[Ff]atty\s+[Aa]mine|[Ff]riction\s+[Mm]odifier', 'friction modifier'),
        (r'[Ss]ilicone', 'silicone antifoam'),
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
        return _reported(pk, tmpl, field, raw.replace(',', '.'), unit, qual, lo, hi, vk,
                         default_temp, '', src_file, sha, rev,
                         notes=f'From data section: {label_line[:60]}')
    return _missing(pk, tmpl, field, src_file, sha, rev)

# ── Field lists ───────────────────────────────────────────────────────
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
                v_str = tr.replace('%', '').strip()
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
    ext  = extract_numeric(text, PKG_PROPS)
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
                v_str = tr.replace('%', '').strip()
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

    write_rows('s10_brb.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
