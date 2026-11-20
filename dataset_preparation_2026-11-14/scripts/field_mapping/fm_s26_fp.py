"""Field-level mapping, S26 FUNCTIONALPRODUCTS.
20 eligible products: 20 additive_component (viscosity modifiers/tackifiers).

Doc format families:
  FORMAT_A : "Typical Properties" section in SDS (17 products).
             Label line followed by value line. Standard find_prop strategy 2.
             Values include: Specific Gravity, Kinematic/Typical Viscosity, Flash Point.
             kv100 (cSt @ 100C) is in the doc but not in COMP_GEN_FIELDS;
             only chemical_family and treat_rate produce Reported rows.
  FORMAT_B : SDS Section 9 "Physical and Chemical Properties" (2 products).
             Label: value on next line.
  FORMAT_C : Inline product description paragraph (1 product, PARATAC 178).
             Values inline: "2800 cSt @ 100C, Pour Point: 0C, Flash Point: 175C"
             find_prop strategy 1 (rest-of-line) catches Pour Point / Flash Point.

All 20 are additive_component; COMP_GEN_FIELDS emitted.
Treat rate and chemical family are the main extractable fields.

Writes field_evidence/s26_fp.csv.
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
decisions  = json.load(open(os.path.join(PKG, 'decisions', 's26_functional_products.json'), encoding='utf-8'))['products']

ELIGIBLE = {r['product_key'] for r in stages_raw
            if r['product_key'].startswith('FUNCTIONALPRODUCTS:')
            and r['stage2_identity']       == 'verified'
            and r['stage3_class_template'] == 'established'
            and r['stage5_field_mapping']  == 'not started'}

prod_docs = {}
for lk in links_raw:
    pk = lk['product_key']
    if pk in ELIGIBLE:
        prod_docs.setdefault(pk, []).append(lk)

REVIEW = 'SDS text read in full 2026-11-19; extraction from cached text-layer'

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
    """Return the first 2000 chars after the properties section header."""
    m = re.search(r'[Tt]ypical\s+[Pp]roperties\b', text)
    if m:
        return text[m.end():m.end()+2000]

    m2 = re.search(r'Physical\s+and\s+[Cc]hemical\s+[Pp]roperties', text, re.I)
    if m2:
        after = text[m2.end():]
        m10 = re.search(r'(?:SECTION|Section)\s+1[0-9]', after)
        return after[:m10.start()] if m10 else after[:2000]

    return text[:2000]

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
    """Near-label scan; strategy 1 (same line) + strategy 2 (next 16 lines)."""
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

# ── Text-field extractors ─────────────────────────────────────────────
def extract_treat_rate(text):
    for pat in [
        r'[Tt]reatment\s+[Ll]evel[^.]*?(\d+)\s*[-–]\s*(\d+)\s*%',
        r'[Tt]reat\s+[Ll]evel[^.]*?(\d+)\s*[-–]\s*(\d+)\s*%',
        r'at\s+(\d+)\s*[-–]\s*(\d+)\s*%',
        r'(\d+)\s*wt%\s+FUNCTIONAL',
        r'[Rr]ecommended.*at\s+([\d.]+)\s*%',
        r'[Tt]reat\s+[Rr]ate[:\s]+([\d.]+)\s*%',
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
        (r'polymethacrylate|PMA\b|methacrylate.based', 'polymethacrylate (PMA)'),
        (r'OCP|olefin\s*copolymer', 'olefin copolymer (OCP)'),
        (r'polyisobutylene|PIB\b', 'polyisobutylene (PIB)'),
        (r'[Vv]iscosity\s+[Mm]odifier\b', 'viscosity modifier'),
        (r'[Pp]our\s+[Pp]oint\s+[Dd]ep', 'pour point depressant'),
        (r'[Tt]ackifier', 'tackifier'),
        (r'zinc\s+dialkyl\s+dithiophosphate|ZDDP', 'zinc dialkyl dithiophosphate (ZDDP)'),
        (r'[Ss]uccinimide\s+[Dd]ispers', 'succinimide dispersant'),
        (r'[Pp]henolic.*[Aa]ntioxidant|[Hh]indered\s+[Pp]henol', 'hindered phenol antioxidant'),
        (r'[Dd]iphenylamine', 'diphenylamine antioxidant'),
        (r'[Cc]orrosion\s+[Ii]nhibit', 'corrosion inhibitor'),
        (r'[Rr]ust\s+[Ii]nhibit', 'rust inhibitor'),
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

# ── Field lists ───────────────────────────────────────────────────────
COMP_GEN_FIELDS = [
    'function.primary', 'function.secondary', 'chemical_family',
    'active_content', 'carrier.identity', 'carrier.share_wt_pct',
    'treat_rate', 'compatibility_restrictions',
    'function_specific_markers.tbn', 'function_specific_markers.ca',
    'function_specific_markers.mg', 'function_specific_markers.p',
    'function_specific_markers.zn', 'function_specific_markers.mo',
]

def component_rows(pk, text, sha, fname, rev):
    rows = []
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
        else:
            rows.append(_missing(pk, 'component_general', f, fname, sha, rev))

    return rows

# ── Main loop ─────────────────────────────────────────────────────────
def main():
    rows   = []
    n_done = 0

    for pk in sorted(ELIGIBLE):
        doc_links = prod_docs.get(pk, [])

        if not doc_links:
            for f in COMP_GEN_FIELDS:
                rows.append(_missing(pk, 'component_general', f, '', '', ''))
            n_done += 1
            continue

        link, text = select_best_doc(doc_links)
        if link is None:
            link_fallback = doc_links[0]
            sha   = link_fallback['sha256']
            fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
            rev   = get_rev_date(sha)
            for f in COMP_GEN_FIELDS:
                rows.append(_missing(pk, 'component_general', f, fname, sha, rev))
            n_done += 1
            continue

        sha   = link['sha256']
        fname = os.path.basename(docs_inv.get(sha, {}).get('first_path', sha[:12]))
        rev   = get_rev_date(sha)

        rows.extend(component_rows(pk, text, sha, fname, rev))
        n_done += 1

    write_rows('s26_fp.csv', rows)
    from collections import Counter
    sc = Counter(r['status'] for r in rows)
    print(f'Done: {n_done}/{len(ELIGIBLE)} products, {len(rows)} rows')
    print(f'  Reported: {sc["Reported"]}, Missing: {sc["Missing"]}')

if __name__ == '__main__':
    main()
