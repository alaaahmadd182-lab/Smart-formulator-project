"""Field-level mapping, S13 XINXING (Jinzhou Xinxing Petroleum Additive Co., Ltd.).
18 eligible: 15 additive_component, 3 additive_package (XT-3205, XT-63297, XT-64223).

Doc format families:
  FORMAT_A : "SPECIFICATIONS / TYPICAL DATA" table (16 products, TDS/PDS docs).
             3-column layout: ITEM | TYPICAL DATA | TEST METHOD.
             OCR reads row by row: label\\nvalue\\nmethod.
             Values: ranges (172-192), bounds (?180 -> >=180, ?0.15 -> >=0.15),
             'Report'/'Actual measurement' (skip), or typical.
             OCR artifact: "?" represents "degrees" in labels (e.g. 20?C) but also
             ">=/<=" in value rows; preprocess: ?digit -> >=digit for value lines.
             Since all mineral-bound values on the properties we extract are minima,
             preprocessing "?" -> ">=" is safe for the extracted fields.
  FORMAT_B : SDS inline format (2 products, T-106D and one other).
             "Label: nnnmax" or "Label: nnnmin" on the same line.
             Strategy 1 (rest of same line) extracts the value directly.

Writes field_evidence/s13_xinxing.csv.
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
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's13_jinzhou.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('XINXING:')
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
    """Replace ?digit with >=digit for XINXING value rows.
    Safe because all bound-valued properties we extract (TBN/Ca/Mg/Zn/P/N/Mo/B/flash)
    are minimum requirements in XINXING spec sheets.
    Does NOT touch ?digit when preceded by alphanumeric (e.g. 20?C in label lines).
    Also replaces nnnmin -> >=nnn and nnnmax -> <=nnn for SDS inline format.
    """
    # ?digit at value line start (preceded by non-alphanumeric)
    block = re.sub(r'(?<![a-zA-Z0-9])\?(\d)', r'≥\1', block)
    return block

# ── Section detection ─────────────────────────────────────────────────
def find_data_block(text):
    for pat in [r'SPECIFICATIONS?\b', r'TYPICAL\s+DATA\b']:
        m = re.search(pat, text)
        if m:
            after = text[m.end():]
            end = re.search(r'STORAGE\b|PACKAGE\b|PACKING\b', after)
            block = after[:end.start()] if end else after[:2500]
            if len(block.strip()) > 20:
                return preprocess(block)
    return preprocess(text[:2500])

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

def find_prop(block, label_pat):
    m = re.search(_wrap(label_pat), block, re.I)
    if not m:
        return None
    label_line = m.group(0).strip()
    rest_of_line = block[m.end():].split('\n')[0]
    rest_clean = re.sub(r'^[\t:\s]+', '', rest_of_line).strip()
    # For SDS inline format: "Label: 395min" -> handle nnnmin/nnnmax
    if rest_clean:
        v = _extract_num_minmax(rest_clean)
        if v:
            return v, label_line
    after = block[m.end():]
    for ln in after.split('\n')[1:16]:
        s = ln.strip().rstrip('\t').strip()
        if not s:
            continue
        if re.match(r'^\(', s):
            continue
        # Skip 'Report', 'Actual measurement', 'Visual' type lines
        if re.match(r'^(?:Report|Actual|Visual|None|N/A)', s, re.I):
            continue
        # Skip method codes
        if re.match(r'^(?:ASTM|GB|SH|Q/|DIN|IP|ISO|EN)\s', s, re.I):
            continue
        # Skip 'not available' type
        if re.match(r'^[Nn]ot\s+(?:available|established|applicable|determined)', s):
            continue
        v = _extract_num_minmax(s)
        if v:
            return v, label_line
        if len(s) > 25 and re.match(r'^[A-Za-z]', s) and not re.search(r'\d', s):
            break
    return None

def _extract_num_minmax(s):
    """Extract number from s, handling nnnmin, nnnmax, ranges, bounds."""
    s = s.strip()
    # nnnmin / nnnmax (SDS inline format)
    mm = re.match(r'(-?\d+(?:\.\d+)?)\s*(min|max)\b', s, re.I)
    if mm:
        v, suffix = mm.group(1), mm.group(2).lower()
        return f'{"≥" if suffix == "min" else "≤"}{v}'
    return _extract_num(s)

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
ALL_PROPS = [
    (r'[Kk]inematic\s+[Vv]iscosity|[Vv]iscosity\s*@\s*100',
                                             'kv100',          'cSt',      '100'),
    (r'[Vv]iscosity\s*@\s*40',              'kv40',           'cSt',      '40'),
    (r'[Dd]ensity(?!\s*index)',              'density',        'kg/m3',    '20'),
    (r'[Ff]lash\s*[Pp]oint|[Ff]lashpoint',  'flash_point',    'degC',     ''),
    (r'[Pp]our\s+[Pp]oint',                 'pour_point',     'degC',     ''),
    (r'TBN\b|[Tt]otal\s+[Bb]ase\s+[Nn]umber',
                                             'tbn',            'mg KOH/g', ''),
    (r'[Ss]ulfated\s+[Aa]sh|[Ss]ulphated\s+[Aa]sh',
                                             'sulfated_ash',   '%',        ''),
    (r'Ca\s*m%|[Cc]alcium\s*(?:m%|content|/?\s*wt%)',
                                             'ca',             '%',        ''),
    (r'Mg\s*m%|[Mm]ag(?:nesium)?\s*(?:m%|content)',
                                             'mg_elem',        '%',        ''),
    (r'Zn\s*m%|[Zz]inc\s*(?:m%|content)',   'zn',             '%',        ''),
    (r'P\s+m%|[Pp]hosphorus\s*(?:m%|content)|^P\s',
                                             'p',              '%',        ''),
    (r'Mo\s*m%|[Mm]o(?:lybdenum)?\s*(?:m%|content)',
                                             'mo',             '%',        ''),
    (r'N\s+m%|[Nn]itrogen\s*(?:m%|content)|^N\s',
                                             'n',              '%',        ''),
    (r'B\s*m%|[Bb]oron\s*(?:m%|content)',   'b',              '%',        ''),
    (r'\bS\s+m%|[Ss]ulf?ur\s*(?:m%|content|wt%)',
                                             's_elem',         '%',        ''),
]

def extract_numeric(text):
    block = find_data_block(text)
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
        r'[Rr]ecommended\s+[Dd]osage[^\n]*?from\s+([\d.]+)\s*%\s+to\s+([\d.]+)\s*%',
        r'[Rr]ecommended\s+[Dd]osage[^\n]*?(\d+(?:\.\d+)?)\s*%\s+to\s+(\d+(?:\.\d+)?)\s*%',
        r'[Rr]ecommended\s+[Dd]osage\s+.*?is\s+([\d.]+)\s*[-–]\s*([\d.]+)\s*%',
        r'[Rr]ecommended\s+[Dd]osage[^.]*?([\d.]+)\s*[-–]\s*([\d.]+)\s*%',
        r'[Rr]ecommend(?:ed)?\s+(?:add(?:ition)|treat[^\n]*?)\s*([\d.]+)\s*[-–%]\s*([\d.]+)?%?',
        r'[Tt]reat(?:ment)?\s+[Rr]ate[:\s]+([\d.]+)\s*[-–]\s*([\d.]+)\s*%',
    ]:
        m = re.search(pat, text[:3000], re.I | re.S)
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
        (r'[Cc]alcium\s+[Ss]ulph?onate|sulphonate.*[Cc]alcium', 'calcium sulfonate'),
        (r'[Mm]agnesium\s+[Ss]ulph?onate', 'magnesium sulfonate'),
        (r'[Cc]alcium\s+[Pp]henate', 'calcium phenate'),
        (r'ZDDP|[Zz]inc\s+[Dd]ithioph|zinc.*dithioph', 'zinc dialkyl dithiophosphate (ZDDP)'),
        (r'[Ss]uccinimide\s+[Dd]ispers|[Pp]olyisobutylene\s+[Ss]uccin', 'succinimide dispersant'),
        (r'[Vv]iscosity\s+[Mm]odifier|EPM|OCP\b', 'viscosity modifier'),
        (r'[Pp]our\s+[Pp]oint\s+[Dd]ep', 'pour point depressant'),
        (r'[Dd]etergent', 'detergent'),
        (r'[Dd]ispers', 'dispersant'),
        (r'[Aa]ntiwear|anti-wear', 'antiwear additive'),
        (r'[Aa]ntiox', 'antioxidant'),
    ]:
        if re.search(pat, text[:3000], re.I):
            return label
    return ''

def extract_package_type(text):
    for pat, label in [
        (r'[Gg]asoline\s+[Ee]ngine|[Pp]etrol\s+[Ee]ngine', 'PCMO additive package'),
        (r'[Dd]iesel\s+[Ee]ngine', 'HDEO additive package'),
        (r'[Ee]ngine\s+[Oo]il\s+[Aa]dditive', 'engine oil additive package'),
        (r'[Gg]ear\s+[Oo]il', 'gear oil additive package'),
        (r'[Ii]nternal\s+[Cc]ombustion', 'engine oil additive package'),
    ]:
        if re.search(pat, text[:3000], re.I):
            return label
    return ''

def extract_performance_claims(text):
    claims = set()
    for pat in [r'API\s+[A-Z]{2,}(?:[/+][A-Z]{2,})*', r'ACEA\s+[A-Z]\d+(?:[-/][A-Z]\d+)*(?:-\d{2,4})?',
                r'ILSAC\s+GF-\d', r'JASO\s+\w+', r'dexos[12]?\b']:
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

# ── Row builders ──────────────────────────────────────────────────────
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
                         notes=f'From SPECIFICATIONS table: {label_line[:60]}')
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
    'elements.B': 'b', 'elements.Mo': 'mo', 'elements.N': 'n', 'elements.S': 's_elem',
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

# ── Per-class builders ────────────────────────────────────────────────
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

    write_rows('s13_xinxing.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
